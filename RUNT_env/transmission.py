import numpy as np
import myutils

def get_distance(position1, position2):
    '''
    get distance of p1 and p2
    args:
        position1, position2: positions
    return:
        distance between p1 and p2
    '''
    position1 = np.array(position1)
    position2 = np.array(position2)
    return np.sqrt(sum(abs(position1 - position2)*abs(position1 - position2)))

def get_direct_channel_gain(distance, lamb, maf):
    '''
    get THz direct channel gain from UE to BS
    args:
        distance: distance from transmitter to receiver
        lamb:  carrier wavelength
        maf:  medium absorption factor
    return:
        direct channel gain
    '''
    return (lamb/(4*np.pi*distance))*np.exp(-maf*distance/2)*np.cos(2*np.pi*distance)

def get_cascade_channel_gain(distance1, distance2, lamb, maf, phase_shift, receive_res, trans_res):
    '''
    get THz cascade channel gain from UE to RIS to BS
    args:
        distance1: distance from UE to RIS
        distance2: distance from RIS to BS
        lamb:  carrier wavelength
        maf:  medium absorption factor
        phase_shift: phase shift matrix of RIS
        receive_res: receive array response vector of RIS
        trans_res: transmit array response vector of RIS
    return:
        cascade channel gain
    '''
    assert len(phase_shift) == len(receive_res)
    assert len(phase_shift) == len(trans_res)
    echo = -(maf*(distance1+distance2)/2)-(np.cos(2*np.pi*(distance1+distance2)))
    golf = (lamb/(8*np.sqrt(pow(np.pi, 3))*distance1*distance2))*np.exp(echo)
    mike = sum(receive_res*np.cos(phase_shift)*trans_res)
    #print(echo, golf, mike)
    return golf*mike

def get_channel_gain(ris_uav, ue, bs, cfg):
    '''
    Sum of direct and cascade channel gain.
    args:
        ris_uav: RIS-UAV object
        ue: UE object
        bs: BS object
        cfg: config object
    return:
        channel gain
    '''
    lamb = cfg['carrier_wavelength']
    maf = cfg['medium_absorption_factor']
    phase_shift = ris_uav.get_phase()
    receive_res = ris_uav.get_receive_array_response()
    trans_res = ris_uav.get_transmit_array_response()
    distance1 = get_distance(ue.get_position(), ris_uav.get_position())
    distance2 = get_distance(ris_uav.get_position(), bs.get_position())
    distance3 = get_distance(ue.get_position(), bs.get_position())
    dcg = get_direct_channel_gain(distance3, lamb, maf)
    ccg = get_cascade_channel_gain(distance1, distance2, lamb, maf, 
                                        phase_shift, receive_res, trans_res)
    #print('args:', distance1, distance2, lamb, maf, phase_shift, receive_res, trans_res)
    #print('channel gain',dcg,ccg)
    return (dcg+ccg)

def get_interference(channel_gain, channel_gain_list, power_list, offload_action):
    '''Get interference of given channel gain in noma transmission'''
    interference = 0
    for i in range(len(channel_gain_list)):
        interference += ((channel_gain_list[i]<channel_gain)*
                            offload_action[i]*channel_gain_list[i]*power_list[i])
    return interference

def get_NOMA_SINR(channel_gain_list, power_list, offload_action, power_of_noise):
    '''
    Get NOMA SINR of given channel gain list, power list, offload action and power of noise
    args:
        channel_gain_list: channel gain list
        power_list: power list
        offload_action: offload action
        power_of_noise: power of noise
    return:
        SINR list
    '''
    assert len(channel_gain_list) == len(power_list)
    assert len(channel_gain_list) == len(offload_action)
    SINR_list = []
    for i in range(len(channel_gain_list)):
        SINR_list.append((power_list[i]*pow(channel_gain_list[i], 2))/
            (get_interference(channel_gain_list[i], channel_gain_list, power_list, offload_action)
                +power_of_noise))
    return SINR_list

def get_transmission_rate(band_width, SINR):
    '''
    Get transmission rate
    args:
        band_width: band width
        SINR: signal to interference and noise ratio
    return:
        transmission rate
    '''
    return band_width*myutils.log(2, 1+SINR)


if __name__ == '__main__':
    x1 = np.array([1,2,4])
    x2 = np.array([1,3,19])
    print(get_distance(x1, x2))
    print(get_direct_channel_gain(2, 1e-5, 0.1))
    print(get_cascade_channel_gain(3, 1, 1e-5, 0.1, [0, 0, 0],
                                    np.array([1, 1, 1]), np.array([1, 1, 1])))
    import ris_uav, bs, ue, config
    cfg = config.get_args()
    RIS = ris_uav.RisUav(cfg)
    BS = bs.BS(cfg)
    UE = ue.UE(cfg)
    print(get_channel_gain(RIS, UE, BS, cfg))
