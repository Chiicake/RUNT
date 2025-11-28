import ue
import bs
import ris_uav
import gymnasium as gym
import numpy as np
import transmission as ts
import myutils as utils


class RuntSystem(gym.Env):
    '''
    A prototype envirment model
    args:
        cfg: a dict containing the configuration of the system
    '''
    def __init__(self, cfg) -> None:
        super().__init__()
        np.random.seed(cfg['seed'])
        self.bs = bs.BS(cfg)
        self.ris_uav = ris_uav.RisUav(cfg)
        self.n_ues = cfg['n_UE']
        self.ue_list = [ue.UE(cfg) for i in range(self.n_ues)]
        self.channel_gain_list = [1 for i in range(self.n_ues)]
        self.transmission_rate_list = [1000 for i in range(self.n_ues)]
        self.bandwidth = cfg['bandwidth']
        self.cfg = cfg

    def step(self, action):
        '''
        Get next state and system consumption based on action
        args:
            action: composed of (offload_decision, computation_capacity_allocate, transmission_power_list,
            phase_change,movement_vector)
        outputs:
            state: the state at the beginning of next time slot
            total_consumption: the total consumption of system
        '''
        (offload_decision, computation_capacity_allocate, transmission_power_list,
            phase_change,movement_vector) = self.action_decomposition(action)# Decompose action
        self.RIS_phase_change(phase_change)
        UAV_movement_consumption = self.UAV_movement(movement_vector)
        self.renovate_transmission_rate_list(offload_decision, transmission_power_list)
        total_consumption = (self.task_execution(offload_decision, computation_capacity_allocate,
                                                transmission_power_list)
                            + UAV_movement_consumption)
        self.new_ts()
        state = self.get_state()
        return state, -total_consumption

    def renovate_transmission_rate_list(self, offload_decision, transmission_power_list):
        '''
        Calculate transmission rate of every ue based on the action and renovate the list.
        args:
            offload_decision: a list of 0 and 1, 0 means local execute, 1 means offload
            transmission_power_list: a list of transmission power of every ue
        '''
        # A process without output
        for i in range(self.n_ues):
            self.channel_gain_list[i] = ts.get_channel_gain(self.ris_uav,
                                                            self.ue_list[i], self.bs, self.cfg)
        SINR_list = ts.get_NOMA_SINR(self.channel_gain_list, transmission_power_list,
                                    offload_decision, self.cfg['power_of_noise'])
        for i in range(self.n_ues):
            self.transmission_rate_list[i] = ts.get_transmission_rate(self.bandwidth, SINR_list[i])

    def task_execution(self, offload_decision, computation_capacity_allocate, transmission_power_list):
        '''
        Execute the task of every ue based on the action and return the total consumption.
        args:
            offload_decision: a list of 0 and 1, 0 means local execute, 1 means offload
            computation_capacity_allocate: a list of computation capacity allocated to every ue
            transmission_power_list: a list of transmission power of every ue
        outputs:
            total_consumption: the total consumption of system
        '''
        total_consumption = 0
        for i in range(self.n_ues):
            if offload_decision[i] == 1:#offload
                MEC_execute_consumption = self.bs.add_task(self.ue_list[i].get_task_consumption(),
                                                            computation_capacity_allocate[i])
                total_consumption += self.ue_list[i].offload(transmission_power_list[i], 
                                                            self.transmission_rate_list[i],
                                                            MEC_execute_consumption)
            if offload_decision[i] == 0:
                total_consumption += self.ue_list[i].local_execute()
        return total_consumption


    def reset(self, seed=-999):
        '''
        Reset the system state and return the initial state
        args:
            seed: the seed of random number generator
        outputs:
            state: the initial state
            info: a dict containing the information of the system
        '''
        if seed == -999:
            seed = self.cfg['seed']#use the seed in cfg
        np.random.seed(seed=seed)
        cfg = self.cfg
        self.bs = bs.BS(cfg)
        self.ris_uav = ris_uav.RisUav(cfg)
        self.n_ues = cfg['n_UE']
        self.ue_list = [ue.UE(cfg) for i in range(self.n_ues)]
        info = {}
        return self.get_state(), info

    def close(self):
        return super().close()

    def render(self):
        pass

    def new_ts(self):
        '''Start a new time slot and renovate the system state'''
        for i in self.ue_list:
            i.new_ts()
        self.bs.new_ts()

    def get_state(self):
        '''
        Get the state of system
        outputs:
            state_list: a list of state at format of [task_computation_consumption_list,
                task_size_list, task_time_limit_list, ue_remaining_execution_time_list,
                ris_uav_position, bs_mec_current_computation_capacity] which is of length 4*n_ues+4
        '''
        task_computation_consumption_list = []
        task_size_list = []
        task_time_limit_list = []
        ue_remaining_execution_time_list = []
        for i in self.ue_list:
            task_computation_consumption_list.append(i.get_task_consumption())
            task_size_list.append(i.get_task_size())
            task_time_limit_list.append(i.get_task_time_limit())
            ue_remaining_execution_time_list.append(i.get_remaining_execution_time())
        state_list = (task_computation_consumption_list+task_size_list+task_time_limit_list
            +ue_remaining_execution_time_list+self.ris_uav.get_position()
            +[self.bs.get_mec_current_computation_capacity()])
        return state_list

    def action_decomposition(self, action):
        '''
        Decompose the action into offload_decision, computation_capacity_allocate, transmission_power_list,
        phase_change,movement_vector
        args:
            action: composed of (offload_decision, computation_capacity_allocate, transmission_power_list,
            phase_change,movement_vector)
        outputs:
            offload_decision: a list of 0 and 1, 0 means local execute, 1 means offload
            computation_capacity_allocate: a list of computation capacity allocated to every ue
            transmission_power_list: a list of transmission power of every ue
            phase_change: a list of phase change of every ris element
            movement_vector: a list of movement vector of uav
        '''
        assert len(action) == 3*self.n_ues+3+self.ris_uav.get_n_elements()
        offload_decision = action[:self.n_ues]
        computation_capacity_allocate = action[self.n_ues:2*self.n_ues]
        transmission_power_list = action[2*self.n_ues:3*self.n_ues]
        phase_change = action[3*self.n_ues:3*self.n_ues+self.ris_uav.get_n_elements()]
        movement_vector = action[3*self.n_ues+self.ris_uav.get_n_elements():]
        return (offload_decision, computation_capacity_allocate, transmission_power_list,
                phase_change,movement_vector)

    def UAV_movement(self, movement_vector):
        '''
        Move the UAV based on the movement_vector
        args:
            movement_vector: a list of movement vector of uav
        outputs:
            UAV_consumption: the consumption of UAV
        '''
        return self.ris_uav.UAV_move(movement_vector)

    def RIS_phase_change(self, phase_change):
        '''
        Change the phase of RIS based on the phase_change
        args:
            phase_change: a list of phase change of every ris element
        '''
        self.ris_uav.change_phase(phase_change)


if __name__ == '__main__':
    import config as Cfg
    cfg = Cfg.get_args()
    runt = RuntSystem(cfg)
    '''print(runt.get_state())
    runt.new_ts()
    print(runt.get_state())
    offload_action = [0, 0, 0, 1, 1]
    power = [2, 3, 5, 2, 3]
    cc_allocation = [1000, 2000, 233, 1432, 844]
    runt.renovate_transmission_rate_list(offload_action, power)
    print(runt.task_execution(offload_action, cc_allocation, power))
    runt.new_ts()
    print(runt.get_state())'''
    
    '''action = [1,1,1,1,1,1000,244,1234,433,1200,5,4,3,4,2,1,3,4,2,3,1,4,2]
    a, b, c, d, e = runt.action_decomposition(action)
    print(a, b, c, d, e)
    print(''.join(['=']*80))
    print(runt.get_state())
    print(runt.step(action))
    print(runt.transmission_rate_list)'''

    '''offload_action = [0, 0, 0, 1, 1]
    power = [2, 3, 5, 2, 3]
    cc_allocation = [1000, 2000, 233, 1432, 844]
    runt.renovate_transmission_rate_list(offload_action, power)
    print(runt.channel_gain_list)

    print(ts.get_channel_gain(runt.ris_uav,runt.ue_list[0],runt.bs,runt.cfg))'''

    action = [1,1,1,1,1,1000,244,1234,433,1200,5,4,3,4,2,1,3,4,2,3,-100,0,0]
    a, b, c, d, e = runt.action_decomposition(action)
    print(a, b, c, d, e)
    print(''.join(['=']*80))
    print(runt.get_state())
    print(runt.step(action))
    print(runt.transmission_rate_list)
    #[5445.82505648535, 961.027951144475, 640.6853007629834, 4805.139755722368, 1281.3706015259665]