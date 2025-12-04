'''BS-MEC model'''
from RUNT_env import myutils


class Mec(object):
    '''MEC model'''
    def __init__(self, cfg) -> None:
        self.time_interval = cfg['time_interval']
        self.computation_capacity = cfg['MEC_computation_capacity']
        self.current_computation_capacity = cfg['MEC_computation_capacity']
        self.task_list = [] #[computation_capacity_allocated, time_lasts] for a task
        self.weight_of_time = cfg['weight_of_time']
        self.energy_efficiency_parameter = cfg['MEC_energy_efficiency_parameter']

    def add_task(self, cpu_cycles_required, computation_capacity_allocated):
        '''
        Add a task to MEC server task list
        args:
            cpu_cycles_required: cpu cycles required of the task
            computation_capacity_allocated: MEC computation capacity allocated to the task
        return:
            weighted sum of time and energy consumption
        '''
        assert computation_capacity_allocated <= self.current_computation_capacity+1e-6, 'MEC computation capacity overflow'
        self.current_computation_capacity -= computation_capacity_allocated
        time_lasts = cpu_cycles_required/max(computation_capacity_allocated, 1e3)
        self.task_list.append([computation_capacity_allocated, time_lasts])
        energy_consumption = myutils.get_compute_energy_consumption(cpu_cycles_required,
                computation_capacity_allocated, self.energy_efficiency_parameter)
        return self.weight_of_time*time_lasts+(1-self.weight_of_time)*energy_consumption

    def new_ts(self):
        '''Renovate the task list at the beginning of a new time slot.'''
        for task in self.task_list:
            task[1] -= self.time_interval
            if task[1] <= 0:
                self.current_computation_capacity += task[0]
        self.task_list = [[computation_capacity_allocated, time_lasts] for
                    computation_capacity_allocated, time_lasts in self.task_list if time_lasts > 0]

    def get_current_computation_capacity(self):
        '''Get current available compuatation capacity of MEC.'''
        return self.current_computation_capacity

    def get_task_list(self):
        '''Return current task list'''
        return self.task_list

    def __repr__(self) -> str:
        return ('MEC\n\tTask list:'+str(self.task_list)+'\n\tAvailable computation capacity:'
                +str(self.current_computation_capacity))


class BS(object):
    '''BS model'''
    def __init__(self, cfg) -> None:
        self.mec = Mec(cfg)
        self.position = cfg['BS_position']

    def new_ts(self):
        '''Renovate the state at the beginning of a new time slot.'''
        self.mec.new_ts()

    def add_task(self, cpu_cycles_required, computation_capacity_allocated):
        '''
        Add a task to MEC server task list
        args:
            cpu_cycles_required: cpu cycles required of the task
            computation_capacity_allocated: MEC computation capacity allocated to the task
        '''
        return self.mec.add_task(cpu_cycles_required, computation_capacity_allocated)

    def get_mec_current_computation_capacity(self):
        '''Get current available compuatation capacity of MEC.'''
        return self.mec.get_current_computation_capacity()

    def get_mec_task_list(self):
        '''Return current task list on MEC'''
        return self.mec.get_task_list

    def get_position(self):
        '''Get position of BS'''
        return self.position

    def __repr__(self) -> str:
        return 'BS position:'+str(self.position)+'\n'+self.mec.__repr__()+'\n'


if __name__ == '__main__':
    import config as cfg
    cfg = cfg.get_args()

    bs = BS(cfg=cfg)
    print(bs)
    print('consumption', bs.add_task(10000,232))
    print(bs.position)
