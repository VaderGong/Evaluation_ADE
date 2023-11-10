
class subject:
    '''
    vehicle, pedestrian, cyclist, etc.
    self.id: unique id
    self.type: vehicle, pedestrian, cyclist, etc.
    self.length: length of the subject
    self.width: width of the subject
    self.valid: list of valid boolean
    self.pos: list of (x,y)
    self.rel_pos: list of (x,y) relative to the lane located in
    self.vel: list of (v_x,v_y)
    self.acc: list of (a_x,a_y)
    self.acc_rate: list of (da_x,da_y)
    self.steer: list of (0: straight, 1: left, 2: right)
    self.steer_freq: int of steer frequency 
    self.brake: list of (0: no brake, 1: brake)
    self.brake_freq: int of brake frequency 
    self.edges: list of edges located in
    self.lanes: list of lanes located in
    self.pos_lane: list of (x,y) relative to the lane located in
    self.mileage: float of mileage
    '''
    def __init__(self):
        pass

    def acceleration(self)->list:
        '''
        calculate acceleration
        :return: list of acceleration
        '''
        pass

    def acceleration_rate(self)->list:
        '''
        calculate acceleration rate
        :return: list of acceleration rate
        '''
        pass

    def mileage(self)->float:
        '''
        calculate mileage
        :return: mileage
        '''
        pass

    def steer(self)->int:
        '''
        get steer state sequence and calculate steer frequency
        :return: steer frequency
        '''
        pass

    def brake(self)->int:
        '''
        get brake state sequence and calculate brake frequency
        :return: brake_fraq
        '''
        pass


        