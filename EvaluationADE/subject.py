
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
    self.heading: list of heading
    self.vel: list of (v_x,v_y)
    self.acc: list of (a_x,a_y)
    self.acc_rate: list of (da_x,da_y)
    self.steer: list of (0: straight, float: steer angle)
    self.steer_rate: list of (0: straight, float: steer rate)
    self.steer_freq: int of steer frequency 
    self.brake: list of (0: no brake, 1: brake)
    self.brake_distance:list of (0: no brake, int: brake distance)
    self.brake_freq: int of brake frequency 
    self.lane_change: list of (0: no lane change, 1: lane change)
    self.lane_change_freq: int of lane change frequency
    seld.cross_line: list of (0: no cross line, int: cross line distance)
    self.cross_line_freq: int of cross line frequency
    self.edges: list of edges located in
    self.lanes: list of lanes located in
    self.pos_lane: list of (x,y) relative to the lane located in
    self.mileage: float of mileage
    self.ttc: list of time to collision
    self.pet: list of post encroachment time
    '''
    def __init__(self):
        pass

    def acceleration(self)->list:
        '''
        calculate acceleration
        :return: list of acceleration
        '''
        print('acceleration')
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
        get steer state sequence and calculate steer rate and steer frequency
        :return: steer frequency
        '''
        pass

    def brake(self)->int:
        '''
        get brake state sequence and calculate brake distance and brake frequency
        :return: brake_fraq
        '''
        pass

    def lane_change(self)->int:
        '''
        get lane change state sequence and calculate lane change frequency
        :return: lane change frequency
        '''
        pass

    def cross_line(self)->int:
        '''
        get cross line state sequence and calculate cross line frequency
        :return: cross line frequency
        '''
        pass




        