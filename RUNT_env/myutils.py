'''utils'''

import numpy as np

def log(base, x):
    '''
    log function
    args:
        base: base of log
        x: input of log
    return:
        log(base, x)
    '''
    return np.log(x)/np.log(base)

def get_compute_energy_consumption(cpu_cycles_required, computation_capacity ,energy_efficiency):
    '''
    Get compute energy consumption of task
    args:
        cpu_cycles_required: cpu cycles required of task
        computation_capacity: computation capacity using to compute the task
        energy_efficiency: energy efficiency of hardware
    return:
        compute energy consumption of task
    '''
    return energy_efficiency*pow(cpu_cycles_required, 2)*computation_capacity

def get_uav_energy_consumption(movement_vector, time, weight_of_UAV):
    '''
    Get UAV energy consumption
    args:
        movement_vector: movement vector of UAV
        time: time of UAV moving
        weight_of_UAV: weight of UAV
    return:
        UAV energy consumption
    '''
    return (weight_of_UAV*pow(np.linalg.norm(movement_vector), 2))/(2*time)

if __name__ == '__main__':
    print(get_compute_energy_consumption(9000,4500,10e-11))
    print(get_uav_energy_consumption([1,1,1], 0.5, 0.25))