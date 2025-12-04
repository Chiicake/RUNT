'''
RIS-UAV model
'''
import numpy as np
from RUNT_env import myutils as utils


class Uav(object):
    '''
    UAV model
    '''
    def __init__(self, cfg) -> None:
        '''
        init args:
            uav_position: the initial position of UAV
            max_mov: the maximum movement distance of UAV in one move
        '''
        self.position = np.array(cfg['uav_position'])
        self.max_mov = cfg['uav_max_mov']
        #UAV活动区域
        self.area = cfg['uav_area']
        self.max_flight_time = cfg['uav_max_flight_time']
        self.weight_of_uav = cfg['weight_of_uav']
        self.weight_of_time = cfg['weight_of_time']

    def move(self, velocity):
        '''
        UAV movement based on the UAV movement equation in UAV model
            args:
                velocity: UAV movement vector
            returns:
                The new position of UAV after movement
        '''
        velocity = np.array(velocity)
        #The velocity is limited by the maximum movement distance of UAV
        new_position = (velocity*min(1, self.max_mov/np.sqrt((velocity*velocity).sum()))
            +self.position)
        #The new position is limited by the area of UAV
        new_position = np.clip(new_position, self.area[0], self.area[1])
        movement_vector = new_position - self.position
        UAV_consumption = utils.get_uav_energy_consumption(movement_vector,
            self.max_flight_time, self.weight_of_uav)*(1-self.weight_of_time)*0.05
        self.position = new_position
        return UAV_consumption

    def get_position(self):
        '''Get current position of UAV.'''
        return self.position

    def __repr__(self) -> str:
        return str(self.position)

class Ris(object):
    '''RIS model'''
    def __init__(self, cfg) -> None:
        '''
        init args:
            n_element: num of reflection element in RIS
            phase_shift: phase shift matrix of RIS
            receive_array_response: receive array response of RIS
            transmit_array_response: transmit array response of RIS
        '''
        self.n_element = cfg['n_element']
        self.phase_shift = np.array([0 for i in range(cfg['n_element'])])
        self.receive_array_response = np.array([1 for i in range(cfg['n_element'])])
        self.transmit_array_response = np.array([1 for i in range(cfg['n_element'])])

    def change_phase(self, new_phase):
        '''
        change the phase shift matrix to the input
            args:
                new_phase: the new phase shift matrix
            returns:
                the new phase shift matrix
        '''
        new_phase = np.array(new_phase)
        assert len(new_phase) == self.n_element
        self.phase_shift = new_phase
        return self.phase_shift

    def get_phase(self):
        """
        Returns the phase shift value.
        """
        return self.phase_shift

    def __repr__(self) -> str:
        return str(self.phase_shift)

class RisUav(object):
    '''
    UAV equipped with RIS
        functions:
        uav_move: change the position of UAV
        change_phase: change the phase shift matrix of RIS
        get_position: get current position of UAV
        get_phase: get current phase shift matrix of RIS
    '''
    def __init__(self, cfg) -> None:
        '''
        init args:
            uav_position: the initial position of UAV
            max_mov: the maximum movement distance of UAV in one move
            n_element: num of reflection element in RIS
        '''
        self.uav = Uav(cfg)
        self.ris = Ris(cfg)

    def UAV_move(self, velocity):
        '''
        UAV movement based on the UAV movement equation in UAV model
            args:
                velocity: UAV movement vector
            returns:
                The new position of UAV after movement
        '''
        assert len(velocity) == 3
        return self.uav.move(velocity=velocity)

    def change_phase(self, new_phase):
        '''
        Change the phase shift matrix to the input
            args:
                new_phase: the new phase shift matrix
            returns:
                the new phase shift matrix
        '''
        self.ris.change_phase(new_phase=new_phase)
        return self.ris

    def get_position(self):
        '''get the current position of RIS-UAV'''
        return list(self.uav.get_position())

    def get_phase(self):
        '''get the current phase shift of RIS'''
        return self.ris.get_phase()

    def get_receive_array_response(self):
        '''get the receive array response of RIS'''
        return self.ris.receive_array_response

    def get_transmit_array_response(self):
        '''get the transmit array response of RIS'''
        return self.ris.transmit_array_response

    def get_n_elements(self):
        '''get number of reflection elements in RIS'''
        return self.ris.n_element

    def get_uav_max_mov(self):
        '''get maximum movement distance of UAV'''
        return self.uav.max_mov

    def __repr__(self) -> str:
        return 'RIS-UAV\n\tUAV:'+str(self.uav)+'\n\tRIS:'+str(self.ris)+'\n'


if __name__ == '__main__':
    import config as cfg
    cfg = cfg.get_args()
    RIS_UAV = RisUav(cfg)
    RIS_UAV.change_phase([1,2,3,4,6])
    print(RIS_UAV.UAV_move([3,5,100]))
    print(RIS_UAV.UAV_move([3,5,100]))
    print(RIS_UAV.UAV_move([3,5,100]))
    print(RIS_UAV.get_position())
