
import gymnasium as gym
import numpy as np
from RUNT_env.RUNT_System import RuntSystem


class RuntBoxEnv(RuntSystem):
    '''A RUNT environment with box action space'''
    def __init__(self, cfg) -> None:
        super().__init__(cfg)
        self.n_action_space = 3*self.n_ues+3+self.ris_uav.get_n_elements()
        self.action_space = gym.spaces.Box(low=0, high=1,
                                           shape=(self.n_action_space,), dtype=np.float32)
        self.n_observation_space = 4*self.n_ues+4
        self.observation_space = gym.spaces.Box(low=0, high=1,
                                                shape=(self.n_observation_space,), dtype=np.float32)

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
        RUNT_action = self.action_data_process(action)
        raw_observation, reward = super().step(RUNT_action)
        observation = self.observation_data_process(raw_observation)
        return observation, reward, False, False, {}

    def reset(self, seed=999):
        return super().reset(seed=seed)

    def render(self):
        return super().render()

    def action_data_process(self, raw_action):
        '''
        Transform the action from the agent to RUNT_System-form.
        i.e. transform the action from box-form to (offload_decision, computation_capacity_allocate,
            transmission_power_list, phase_change,movement_vector)-form which is len=3*self.n_ues+self.ris_uav.get_n_elements()+3
        args:
            raw_action: the action from the agent
        return:
            action: the action in RUNT_System-form
        '''
        action_offload_decision = [(0 if i<0.5 else 1) for i in raw_action[0:self.n_ues]]
        action_computation_capacity_allocate = ([(i*self.bs.get_mec_current_computation_capacity())
                                                /(np.sum(np.array(raw_action[self.n_ues:2*self.n_ues])
                                                *np.array(action_offload_decision))+1e-6)
                                                for i in raw_action[self.n_ues:2*self.n_ues]])
        action_transmission_power_list = [i*self.cfg['UE_maximum_transmit_power'] 
                                        for i in raw_action[2*self.n_ues:3*self.n_ues]]
        action_phase_change = [i*2*np.pi for i 
                                in raw_action[3*self.n_ues:3*self.n_ues+self.ris_uav.get_n_elements()]]
        action_movement_vector = [(i-0.5)*self.ris_uav.get_uav_max_mov()
                                    for i in raw_action[3*self.n_ues+self.ris_uav.get_n_elements():]]
        action = (action_offload_decision
                +action_computation_capacity_allocate
                +action_transmission_power_list
                +action_phase_change
                +action_movement_vector)
        return action

    def observation_data_process(self, raw_observation):
        '''
        Transform the observation from RUNT_System to observation_space-form
        i.e. transform the observation from 
        args:
            raw_observation: the observation from RUNT_System which is a list
                state at format of [task_computation_consumption_list,
                task_size_list, task_time_limit_list, ue_remaining_execution_time_list,
                ris_uav_position, bs_mec_current_computation_capacity] which is of length 4*n_ues+4
        return:
            observation: the observation in observation_space-form
        '''
        #print('raw_observation:', raw_observation)
        observation_task_computation_consumption_list = [min(1, i/(2*self.cfg['task_comsumption_average'])) for i in raw_observation[0:self.n_ues]]
        observation_task_size_list = [min(1, i/(2*self.cfg['task_size_average'])) for i in raw_observation[self.n_ues:2*self.n_ues]]
        observation_task_time_limit_list = [i/max(raw_observation[2*self.n_ues:3*self.n_ues]) for i in raw_observation[2*self.n_ues:3*self.n_ues]]
        observation_ue_remaining_execution_time_list = [min(1, i/20) for i in raw_observation[3*self.n_ues:4*self.n_ues]]
        observation_ris_uav_position = [(raw_observation[4*self.n_ues+i]-self.cfg['uav_area'][0][i])/(self.cfg['uav_area'][1][i]-self.cfg['uav_area'][0][i]) for i in range(3)]
        #[i/(max(raw_observation[4*self.n_ues:4*self.n_ues+3])+1) for i in raw_observation[4*self.n_ues:4*self.n_ues+3]]
        observation_bs_mec_current_computation_capacity = raw_observation[-1]/self.cfg['MEC_computation_capacity']
        observation = (observation_task_computation_consumption_list
                        +observation_task_size_list
                        +observation_task_time_limit_list
                        +observation_ue_remaining_execution_time_list
                        +observation_ris_uav_position
                        +[observation_bs_mec_current_computation_capacity])
        return observation


if __name__ == '__main__':
    import config as Cfg
    import numpy as np
    cfg = Cfg.get_args()
    env = RuntBoxEnv(cfg)
    env.reset()
    '''print(env.get_state())
    print(env.step(np.array([1,1,1,1,1,1000,244,1234,433,1200,5,4,3,4,2,1,3,4,2,3,100,0,0])))'''
    action = env.action_space.sample()
    print(env.action_data_process(action))
    print(env.step(action))
    print(type(env.action_space))