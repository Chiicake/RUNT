import numpy as np
import random
import myutils


class Task(object):

    def __init__(self, cfg):
        self.task_size_average = cfg['task_size_average']
        self.task_size_variance = cfg['task_size_variance']
        self.task_comsumption_average = cfg['task_comsumption_average']
        self.task_comsumption_variance = cfg['task_comsumption_variance']
        self.task_time_average = cfg['task_time_average']
        self.task_time_variance = cfg['task_time_variance']
        self.task_arrival_rate = cfg['task_arrival_rate']

        self.task_arrive = 1 if np.random.rand() < self.task_arrival_rate else 0
        self.task_size = self.task_arrive*np.random.normal(self.task_size_average,
                                                            np.sqrt(self.task_size_variance))
        self.computation_consumption = self.task_arrive*np.random.normal(self.task_comsumption_average,
                                                        np.sqrt(self.task_comsumption_variance))
        self.time_limit = 1e6 if not self.task_arrive else np.random.normal(self.task_time_average,
                                        np.sqrt(self.task_time_variance))

    def get_new_task(self):
        self.task_arrive = 1 if np.random.rand() < self.task_arrival_rate else 0
        self.task_size = self.task_arrive*np.random.normal(self.task_size_average,
                                                            np.sqrt(self.task_size_variance))
        self.computation_consumption = self.task_arrive*np.random.normal(self.task_comsumption_average,
                                                        np.sqrt(self.task_comsumption_variance))
        self.time_limit = 1e6 if not self.task_arrive else np.random.normal(self.task_time_average,
                                        np.sqrt(self.task_time_variance))


    def get_computation_consumption(self):
        return self.computation_consumption

    def get_task_size(self):
        return self.task_size

    def get_time_limit(self):
        return self.time_limit

    def __repr__(self) -> str:
        return ('Task\n\tTask size:'+str(self.task_size)+
                '\n\tComputation consumption:'+str(self.computation_consumption)+
                '\n\tTime limit:'+str(self.time_limit))


class UE(object):

    def __init__(self, cfg) -> None:
        self.computation_capacity = cfg['UE_computation_capacity']
        self.position = np.array([np.random.uniform(-cfg['UE_distribution'], cfg['UE_distribution']),
                        np.random.uniform(-cfg['UE_distribution'], cfg['UE_distribution']), 0])
        self.task = Task(cfg)
        self.remaining_execution_time = 0
        self.energy_efficiency = cfg['UE_energy_efficiency_parameter']
        self.maximum_transmit_power = cfg['UE_energy_efficiency_parameter']
        self.time_interval = cfg['time_interval']
        self.weight_of_time = cfg['weight_of_time']

    def new_task(self):
        self.task.get_new_task()

    def local_execute(self):
        '''
        Execute task locally
        output:
            Total consumption for execute the task locally
        '''
        time_consumption = (self.remaining_execution_time+
                            self.task.computation_consumption/self.computation_capacity)
        self.remaining_execution_time += time_consumption
        energy_consumption = myutils.get_compute_energy_consumption(self.task.computation_consumption,
                                                self.computation_capacity, self.energy_efficiency)
        return self.weight_of_time*time_consumption+(1-self.weight_of_time)*energy_consumption


    def offload(self, transmit_power, transmittion_rate, MEC_execute_consumption):
        '''
        Offload the task on UE to MEC server
        args:
            transmit_power
            transmittion_rate
            MEC_execute_consumption
        output:
            Total consumption for offloading the task
        '''
        if transmit_power > self.maximum_transmit_power:
            transmit_power = self.maximum_transmit_power
        trans_time_consumption = self.get_task_size()/(transmittion_rate or 1e4)
        #T_T
        #Sometimes there will be a mistake leading the result of transrate == 0 and cause a collapse.
        #I could not handle it so I assume the transrate is 1e5 if the calculated transrate == 0
        #QAQ
        trans_energy_consumption = transmit_power*trans_time_consumption
        #print('Trans:' ,trans_energy_consumption, trans_time_consumption, transmittion_rate)
        return (MEC_execute_consumption+self.weight_of_time*trans_time_consumption+
                    (1-self.weight_of_time)*trans_energy_consumption)

    def new_ts(self):
        '''Start a new time slot'''
        self.new_task()
        self.remaining_execution_time -= self.time_interval
        self.remaining_execution_time = max(0, self.remaining_execution_time)

    def get_remaining_execution_time(self):
        return self.remaining_execution_time

    def get_task_size(self):
        return self.task.get_task_size()

    def get_task_consumption(self):
        return self.task.get_computation_consumption()

    def get_task_time_limit(self):
        return self.task.get_time_limit()

    def get_position(self):
        return self.position

    def __repr__(self) -> str:
        return 'UE\n\tPosition:'+str(self.position)+'\n\t'+self.task.__repr__()+'\n'


if __name__ == '__main__':
    import config as Cfg
    cfg = Cfg.get_args()
    ue = UE(cfg)
    print(ue)
