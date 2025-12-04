'''
System configuration
'''
import argparse


def get_args():
    """ 
    get system configuration
    """
    parser = argparse.ArgumentParser(description="systemconfig")

    parser.add_argument('--BS_position', default=[0, 0, 10], type=int, help="position of BS antenna")
    parser.add_argument('--MEC_computation_capacity', default=5000, type=int, help="computation capacity of MEC server")
    parser.add_argument('--MEC_energy_efficiency_parameter', default=10e-11, type=int, help="energy efficiency parameter of MEC server")

    parser.add_argument('--uav_max_mov', default=10, type=int, help="maximum movement distance of UAV")
    parser.add_argument('--uav_position', default=[0, 0, 0], type=list, help="initial UAV position")
    parser.add_argument('--uav_max_flight_time', default=0.5, type=int, help="max uav flight time in a time slot")
    parser.add_argument('--uav_area', default=[[-10, -10, 0], [10, 10, 10]], type=list, help="area of UAV")
    parser.add_argument('--weight_of_uav', default=0.25, type=int, help="weight of UAV")
    parser.add_argument('--n_element', default=5, type=int, help="number of reflection element in RIS")

    parser.add_argument('--task_size_average', default=450, type=int, help="average task size")
    parser.add_argument('--task_size_variance', default=100, type=int, help="variance of task size")
    parser.add_argument('--task_comsumption_average', default=4500, type=int, help="average task comsumption")
    parser.add_argument('--task_comsumption_variance', default=1000, type=int, help="variance of task comsumption")
    parser.add_argument('--task_time_average', default=5, type=int, help="average task time limit")
    parser.add_argument('--task_time_variance', default=1, type=int, help="variance of time limit")
    parser.add_argument('--task_arrival_rate', default=0.3, type=int, help="task arrival rate")

    parser.add_argument('--n_UE', default=5, type=int, help="number of UE")
    parser.add_argument('--UE_distribution', default=10, type=int, help="distribution of UEs")
    parser.add_argument('--UE_computation_capacity', default=1000, type=int, help="computation capacity of UE")
    parser.add_argument('--UE_idle_power', default=0.1, type=int, help="idle power of UE")
    parser.add_argument('--UE_maximum_transmit_power', default=5, type=int, help="maximum transmit power of UE")
    parser.add_argument('--UE_energy_efficiency_parameter', default=10e-11, type=int, help="energy efficiency parameter of UE")

    parser.add_argument('--weight_of_time', default=0.5, type=int, help="weight of time")
    parser.add_argument('--time_interval', default=5, type=int, help="time interval between two time slot")
    
    parser.add_argument('--bandwidth', default=1e14, type=int, help="bandwidth of THz frequency band")
    '''(pow(10, (-174/10))*pow(10, -3)*bandwidth)'''
    parser.add_argument('--power_of_noise', default=4e-7, type=int, help="power of noise in communication")
    parser.add_argument('--carrier_wavelength', default=3e-5, type=int, help="carrier wavelength of THz frequency band")
    parser.add_argument('--carrier_central_frequency', default=1e13, type=int, help="central frequency of THz frequency band")
    parser.add_argument('--medium_absorption_factor', default=0.1, type=int, help="medium absorption factor")
    parser.add_argument('--seed', default=777, type=int, help="medium absorption factor")

    args = parser.parse_args([])
    args = {**vars(args)}
    '''print(args.items())
    print(''.join(['=']*80))
    print("\t\t\t\tSystem Config")
    print(''.join(['=']*80))
    tplt = "{:^40}\t{:^20}"
    print(tplt.format("Name", "Value"))
    for k,v in args.items():
        print(tplt.format(k,str(v)))   
    print(''.join(['=']*80))  '''
    return args


if __name__ == '__main__':
    args = get_args()
    print(''.join(['=']*80))
    print("\t\t\tSystem Config")
    print(''.join(['=']*80))
    tplt = "{:^40}\t{:^20}"
    print(tplt.format("Name", "Value"))
    for k,v in args.items():
        print(tplt.format(k,str(v)))   
    print(''.join(['=']*80))

