import numpy as np
class subject:
    '''
    vehicle, pedestrian, cyclist, etc.
    self.id: unique id
    self.type: vehicle, pedestrian, cyclist, etc.
    self.length: length of the subject
    self.width: width of the subject
    self.valid: array of valid boolean
    self.pos: array of (x,y)
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
    '''
    def __init__(self) -> None:
        self.id=None
        self.pos=np.array([[0,0],[1,0],[1,1],[2,1]])
        self.vel=np.array([[0,0],[10,0],[0,10],[10,0]])
        self.valid=np.array([False,True,True,True])
        self.sample_time=0.1

    def acceleration(self):
        '''
        calculate acceleration
        :return: list of acceleration
        '''
        valid_vel=self.vel[self.valid]
        valid_acc=(valid_vel[1:]-valid_vel[:-1])/self.sample_time
        valid_acc=np.concatenate((np.zeros((1,2)),valid_acc),axis=0)
        self.acc=np.zeros((len(self.vel),2))
        
        self.acc[self.valid]=valid_acc
        return self.acc
        

    def acceleration_rate(self):
        '''
        calculate acceleration rate
        :return: list of acceleration rate
        '''
        valid_acc=self.acc[self.valid]
        valid_acc_rate=(valid_acc[1:]-valid_acc[:-1])/self.sample_time
        valid_acc_rate=np.concatenate((np.zeros((1,2)),valid_acc_rate),axis=0)
        self.acc_rate=np.zeros((len(self.vel),2))
        self.acc_rate[self.valid]=valid_acc_rate
        return self.acc_rate
        

    def mileage(self)->float:
        '''
        calculate mileage
        :return: mileage
        '''
        valid_pos=self.pos[self.valid]
        diff=np.diff(valid_pos,axis=0)
        dist = np.linalg.norm(diff, axis=1)
        self.mileage=np.sum(dist)
        return self.mileage
    def steer_rate(self):
        '''
        calculate steer rate
        :return: array of steer rate
        '''
        valid_heading=self.heading[self.valid]
        valid_steer_rate=(valid_heading[1:]-valid_heading[:-1])/self.sample_time
        valid_steer_rate=np.concatenate((np.zeros((1,2)),valid_steer_rate),axis=0)
        self.steer_rate=np.zeros((len(self.heading),2))
        self.steer_rate[self.valid]=valid_steer_rate
        return self.steer_rate
        
    def steer_frequency(self,angle_threshold=60):
        '''
        get steer state sequence and calculate  steer frequency steer angle
        :return: steer frequency
        '''
        valid_steer=self.steer[self.valid]
        

    def brake(self,threshold=2):
        '''
        get brake state sequence and calculate brake distance and brake frequency
        :return: brake_fraq
        '''
        valid_acc=self.acc[self.valid]
        valid_vel=self.vel[self.valid]
        isBraking=np.sum(np.multiply(valid_acc,valid_vel),axis=1)<0.0
        isBraking=isBraking*(np.linalg.norm(valid_acc,axis=1)>threshold)
        self.brake=np.zeros((len(self.vel),2),dtype=bool)
        self.brake[self.valid]=isBraking
        self.brake_freq=np.sum(np.diff(self.brake,axis=0)==1)
        #compute brake distance
        brakeBegin=np.where(np.diff(self.brake,axis=0)==-1)
        brakeEnd=np.where(np.diff(self.brake,axis=0)==1)
        brake_pos=np.where(self.brake,self.pos,0.0)
        diff=np.diff(brake_pos,axis=0)
        dist=np.linalg.norm(diff,axis=1)
        inted_dist=np.cumsum(dist)
        for i in range(len(brakeBegin)):
            inted_dist[brakeBegin[i]:brakeEnd[i]]-=inted_dist[brakeBegin[i]]
        self.brake_distance=np.zeros((len(self.vel),2))
        self.brake_distance[self.brake]=inted_dist
        return self.brake_freq
        

    def lane_change(self)->int:
        '''
        get lane change state sequence and calculate lane change frequency
        :return: lane change frequency
        '''
        valid_lane=self.lanes[self.valid]
        diff=np.diff(valid_lane,axis=0)
        valid_lane_change=np.concatenate((np.array([0],dtype=bool),diff!=0),axis=0)
        self.lane_change=np.zeros((len(self.lanes),2),dtype=bool)
        self.lane_change[self.valid]=valid_lane_change
        self.lane_change_freq=np.sum(valid_lane_change)
        return self.lane_change_freq
        

    def cross_line(self)->int:
        '''
        get cross line state sequence and calculate cross line frequency
        :return: cross line frequency
        '''
        pass




if __name__ == '__main__':
    veh=subject()
    veh.acceleration()