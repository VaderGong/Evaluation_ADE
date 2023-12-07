import numpy as np
import csv
import matplotlib.pyplot as plt
from map import map
from n_circle_appro import *
class subject:
    '''
    vehicle, pedestrian, cyclist, etc.
    self.id: unique id
    self.type: vehicle, pedestrian, cyclist, etc.
    self.length: length of the subject
    self.width: width of the subject
    self.valid: array of valid boolean
    self.pos: array of (x,y)
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
    self.lanePos: list of (x,y) relative to the lane located in
    self.mileage: float of mileage
    '''
    def __init__(self,id,type=None,length=None,width=None,valid=None,pos=None,heading=None,edges=None,lanes=None,vel=None,lanePos=None,sample_time=0.1) -> None:
        # self.id=None
        # self.pos=np.array([[0,0],[1,0],[1,1],[2,1]])
        # self.vel=np.array([[0,0],[10,0],[0,10],[10,0]])
        # self.valid=np.array([False,True,True,True])
        # self.sample_time=0.1
        self.id=id
        self.type=type
        self.length=length
        self.width=width
        self.valid=valid
        self.pos=pos
        self.heading=heading
        self.edges=edges
        self.lanes=lanes
        self.vel=vel
        self.pos_lane=lanePos
        self.sample_time=sample_time
        self.n_circle=n_circle(self.width,self.length)
    def velocity(self):
        '''
        calculate velocity
        :return: list of velocity
        '''
        valid_pos=self.pos[self.valid]
        valid_vel=(valid_pos[1:]-valid_pos[:-1])/self.sample_time
        valid_vel=np.concatenate((np.zeros((1,2)),valid_vel),axis=0)
        self.vel=np.zeros((len(self.pos),2))
        self.vel[self.valid]=valid_vel
        return self.vel
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
        heading_diff=valid_heading[1:]-valid_heading[:-1]
        heading_diff[heading_diff<-180]+=360
        heading_diff[heading_diff>180]-=360
        valid_steer_rate=heading_diff/self.sample_time
        
        valid_steer_rate=np.concatenate((np.zeros(1),valid_steer_rate),axis=0)
        self.steer_rate=np.zeros(len(self.heading))
        self.steer_rate[self.valid]=valid_steer_rate
        return self.steer_rate
        
    def steer_frequency(self,angle_threshold=60):
        '''
        get steer state sequence and calculate  steer frequency steer angle
        :return: steer frequency
        '''
        valid_steer=self.steer[self.valid]
        

    def brake(self,threshold=4):
        '''
        get brake state sequence and calculate brake distance and brake frequency
        :return: brake_freq
        '''
        valid_acc=self.acc[self.valid]
        valid_vel=self.vel[self.valid]
        isBraking=np.sum(np.multiply(valid_acc,valid_vel),axis=1)<0.0
        isBraking=isBraking*(np.linalg.norm(valid_acc,axis=1)>threshold)
        self.brake=np.zeros((len(self.vel)),dtype=bool)
        self.brake[self.valid]=isBraking
        self.brake_freq=np.sum(np.diff(self.brake,axis=0)==1)
        #compute brake distance
        brakeBegin=np.where(np.diff(self.brake.astype(int),axis=0)==1)[0]
        brakeEnd=np.where(np.diff(self.brake.astype(int),axis=0)==-1)[0]
        brake_pos=self.pos[self.brake]
        diff=np.diff(self.pos,axis=0)
        dist=np.linalg.norm(diff,axis=1)
        inted_dist=np.cumsum(dist)
        if len(brakeBegin)!=len(brakeEnd):
            brakeEnd=np.append(brakeEnd,-1)
        for i in range(len(brakeBegin)):
            try:
                inted_dist[brakeBegin[i]:brakeEnd[i]]-=inted_dist[brakeBegin[i]]
            except:
                print(self.id)
                print(i)
                print(brakeBegin)
                print(brakeEnd)
                print(inted_dist.shape)
        self.brake_distance=np.zeros(len(self.vel))
        inted_dist=np.concatenate((np.array([0]),inted_dist),axis=0)
        self.brake_distance[self.brake]=inted_dist[self.brake]
        
        return self.brake_freq
        

    def lane_change(self)->int:
        '''
        get lane change state sequence and calculate lane change frequency
        :return: lane change frequency
        '''
        valid_lane=self.lanes[self.valid]
        valid_lane_change=np.concatenate((np.array([0],dtype=bool),valid_lane[1:]!=valid_lane[:-1]),axis=0)
        self.lane_change=np.zeros(len(self.lanes),dtype=bool)
        self.lane_change[self.valid]=valid_lane_change
        self.lane_change_freq=np.sum(valid_lane_change)
        return self.lane_change_freq
        

    def cross_line(self)->int:
        '''
        get cross line state sequence and calculate cross line frequency
        :return: cross line frequency
        '''
        pass
    def checkValid(self):
        diff=np.diff(self.valid,axis=0)
        abs_diff=np.abs(diff)
        if np.sum(abs_diff)>2:
            print(self.id)
class subjects:
    def __init__(self,sample_time=0.1) -> None:
        self.subjects={}
        self.beginFrame=0
        self.subjectNum=0
        self.frameNum=0
        self.sample_time=sample_time
    def initFromCSV(self,csvFile):
        with open(csvFile) as f:
            reader=csv.DictReader(f)
            #preprocess
            idSet=set()
            frameSet=set()
            rowList=[]
            
            #check if the csv file contains velocity and acceleration
            self.hasVelocity=False
            if 'xVelocity' in reader.fieldnames and 'yVelocity' in reader.fieldnames:
                self.hasVelocity=True
            self.hasAcceleration=False
            if 'xAcceleration' in reader.fieldnames and 'yAcceleration' in reader.fieldnames:
                self.hasAcceleration=True
            
            for row in reader:
                idSet.add(row['id'])
                frameSet.add(int(row['frame']))
                rowList.append(row)
            self.beginFrame=min(frameSet)
            self.frameNum=len(frameSet)
            self.subjectNum=len(idSet)
            for id in idSet:
                self.subjects[id]=subject(id=id,sample_time=self.sample_time)
                self.subjects[id].pos=np.zeros((len(frameSet),2))
                self.subjects[id].valid=np.zeros(len(frameSet),dtype=bool)
                self.subjects[id].heading=np.zeros(len(frameSet))
                self.subjects[id].lanePos=np.zeros((len(frameSet),2))
                self.subjects[id].edges=np.empty(len(frameSet),dtype=np.str_)
                self.subjects[id].lanes=np.empty(len(frameSet),dtype=np.str_)
                if self.hasVelocity:
                    self.subjects[id].vel=np.zeros((len(frameSet),2))
                if self.hasAcceleration:
                    self.subjects[id].acc=np.zeros((len(frameSet),2))
        for row in rowList:
            if self.subjects[row['id']].length is None:
                self.subjects[row['id']].length=row['Length']
            if self.subjects[row['id']].width is None:
                self.subjects[row['id']].width=row['Width']
            frame=int(row['frame'])-self.beginFrame
            self.subjects[row['id']].pos[frame]=np.array([float(row['Pos'].strip('()').split(',')[0]),float(row['Pos'].strip('()').split(',')[1])])
            self.subjects[row['id']].valid[frame]=True
            self.subjects[row['id']].heading[frame]=float(row['Angle'])
            self.subjects[row['id']].lanePos[frame]=np.array([float(row['LanePos']),float(row['LateralLanePos'])])
            self.subjects[row['id']].edges[frame]=row['Edge']
            self.subjects[row['id']].lanes[frame]=row['Lane']
            if self.hasVelocity:
                self.subjects[row['id']].vel[frame]=np.array([float(row['xVelocity']),float(row['yVelocity'])])
            if self.hasAcceleration:
                self.subjects[row['id']].acc[frame]=np.array([float(row['xAcceleration']),float(row['yAcceleration'])])
        if not self.hasVelocity:
            for id in self.subjects:
                self.subjects[id].velocity()
            
    def speed(self,bins=1000):
        """
        calculate speed distribution
        :return: speed distribution
        """
        speed=np.zeros(1)
        for id in self.subjects:
            valid_vel=self.subjects[id].vel[self.subjects[id].valid]
            subjectSpeed=np.linalg.norm(valid_vel,axis=1).flatten()
            speed=np.concatenate((speed,subjectSpeed))
        plt.hist(speed,bins=1000,log=True,width=(max(speed)-min(speed))/1000)
        plt.xlim(0,max(speed))
        plt.xlabel('Speed')
        plt.ylabel('Count')
        plt.show()
        
        counts,bin_edges=np.histogram(speed,bins=bins)
        
        counts[0]-=1
        return counts,bin_edges
    def accMagnitude(self,bins=1000):
        """
        calculate acceleration magnitude distribution
        :return: acceleration magnitude distribution
        """
        acc=np.zeros(1)
        for id in self.subjects:
            if not self.hasAcceleration:
                self.subjects[id].acceleration()
            valid_acc=self.subjects[id].acc[self.subjects[id].valid]
            subjectAcc=np.linalg.norm(valid_acc,axis=1).flatten()
            acc=np.concatenate((acc,subjectAcc))
        plt.hist(acc,bins=1000,log=True,width=(max(acc)-min(acc))/1000)
        plt.xlim(0,max(acc))
        plt.xlabel('Acceleration Magnitude')
        plt.ylabel('Count')
        plt.show()
        counts,bin_edges=np.histogram(acc,bins=bins)
        counts[0]-=1
        return counts,bin_edges
    def accRateMagnitude(self,bins=1000):
        """
        calculate acceleration rate magnitude distribution
        :return: acceleration rate magnitude distribution
        """
        accRate=np.zeros(1)
        for id in self.subjects:
            self.subjects[id].acceleration_rate()
            valid_accRate=self.subjects[id].acc_rate[self.subjects[id].valid]
            subjectAccRate=np.linalg.norm(valid_accRate,axis=1).flatten()
            accRate=np.concatenate((accRate,subjectAccRate))
        counts,bin_edges=np.histogram(accRate,bins=bins)
        counts[0]-=1
        return counts,bin_edges
    def steerRate(self,bins=1000):
        """
        calculate steer rate distribution
        :return: steer rate distribution
        """
        steerRate=np.zeros(1)
        for id in self.subjects:
            self.subjects[id].steer_rate()
            subjectSteerRate=self.subjects[id].steer_rate[self.subjects[id].valid].flatten()
            steerRate=np.concatenate((steerRate,subjectSteerRate))
        counts,bin_edges=np.histogram(steerRate,bins=bins)
        return counts,bin_edges
    def brake(self,threshold=4):
        """
        calculate brake frequency and brake distance
        :return: brake frequency and brake distance
        """
        brakeFreq=0
        brakeDist=np.zeros(1)
        for id in self.subjects:
            brakeFreq+=self.subjects[id].brake(threshold)
            diffDist=np.diff(self.subjects[id].brake_distance,axis=0)
            finalDist=diffDist[diffDist<0]
            finalDist=-finalDist
            brakeDist=np.concatenate((brakeDist,finalDist))
        return brakeFreq, brakeDist[1:]
    def laneChange(self):
        """
        calculate lane change frequency and lane change position
        :return: lane change frequency and lane change position
        """
        laneChangePos=np.zeros((1,2))
        laneChangeFreq=0
        for id in self.subjects:
            laneChangeFreq+=self.subjects[id].lane_change()
            laneChangePos=np.concatenate((laneChangePos,self.subjects[id].pos[self.subjects[id].lane_change]),axis=0)
        laneChangePos=laneChangePos[1:]
        return laneChangeFreq,laneChangePos
    def checkValid(self):
        for id in self.subjects:
            self.subjects[id].checkValid()

if __name__ == '__main__':
    s=subjects(sample_time=1)
    Path='testData/test.csv'
    Path="C:\\Users\\LENOVO\\Desktop\\Lib\\Data&Scripts\\processed_tracks.csv"
    s.initFromCSV(Path)
    s.checkValid()
    # m = map()
    # m.loadfromxml("testData/Town04.net.xml")
    # m.visualize()
    s.speed()
    counts,bin_edges=s.accMagnitude(bins=1000)
    counts=np.log(counts+1)
    print(counts.shape)
    # laneChangeFreq,laneChangePos=s.laneChange()   
    # x=laneChangePos[:,0]
    # y=laneChangePos[:,1]
    # plt.plot(x,y,'.',color='red')
    # plt.show()
    # plt.bar(bin_edges[:-1],counts)
    # plt.xlim(min(bin_edges),max(bin_edges))
    # plt.xlabel('Acceleration Magnitude')
    # plt.ylabel('Log(Count)')
    # plt.show()
    # brakeFreq,brakeDist=s.brake(2)
    # plt.hist(brakeDist,bins=1000)
    # plt.xlabel('Brake Distance')
    # plt.ylabel('Count')
    # plt.show()