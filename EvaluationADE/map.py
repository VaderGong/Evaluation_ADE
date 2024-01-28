import numpy as np
import xml.dom.minidom as minidom
import matplotlib.pyplot as plt
from subject import subjects
from tqdm import tqdm
from matplotlib.transforms import ScaledTranslation
from TTC import TTC

#map--------------------------------------------------------------------------------------------
class map:
    def __init__(self):
        self.edges = {}
        self.junctions = {}

    def loadfromxml(self, xml_path):
        DomTree = minidom.parse(xml_path)
        collection = DomTree.documentElement

        edges = collection.getElementsByTagName("edge")
        for edge_ in edges:
           
            lanes = edge_.getElementsByTagName("lane")
            l_dict = {}
            for lane_ in lanes:
                id = str(lane_.getAttribute("id"))
                width = float(lane_.getAttribute("width"))
                shape_ = lane_.getAttribute("shape")
                shape_ = shape_.split(" ")
                shape = [i.split(',') for i in shape_]
                shape = [[float(i[0]),float(i[1])] for i in shape]
                l = lane(id, width, shape, [])
                l_dict[id] = l
            id = str(edge_.getAttribute("id"))
            e = edge(id, l_dict)
            self.edges[id] = e
            l_dict={}

        junctions = collection.getElementsByTagName("junction")
        for junction_ in junctions:
            if junction_.getAttribute("type") == "internal":
                continue
            id = str(junction_.getAttribute("id"))
            loc = [float(junction_.getAttribute("x")) , float(junction_.getAttribute("y"))]
            shape_ = junction_.getAttribute("shape")
            shape_ = shape_.split(" ")
            shape = [i.split(',') for i in shape_]
            shape = [[float(i[0]),float(i[1])] for i in shape]
            j = junction(id, loc, shape, [])
            self.junctions[id] = j
    
    def load_vehicles(self, subjects:subjects):
        for edge in self.edges.values():
            for lane in edge.lanes.values():
                lane.subjects = [[] for i in range(subjects.frameNum)]
        for subject in tqdm(subjects.subjects.values()):
            for i in range(subjects.frameNum):
                if subject.valid[i]:
                    self.edges[subject.edges[i]].lanes[subject.lanes[i]].subjects[i].append(subject)
        #依lane上相对位置排序
        for edge in self.edges.values():
            for lane in edge.lanes.values():
                for i in range(subjects.frameNum):
                    if lane.subjects[i] != []:
                        lane.subjects[i].sort(key=lambda x:x.lanePos[i][0])
                     
    def visualize_map(self, size=(400,5), show=True):
        #get the current figure and axes
        fig, ax = plt.subplots(figsize=size)
        for edge in self.edges.values():
            for lane in edge.lanes.values():
                x=[point[0] for point in lane.shape]
                y=[point[1] for point in lane.shape]
                dpi_scale_trans = ScaledTranslation(0, 0, fig.dpi_scale_trans)
                trans = ax.transData + dpi_scale_trans
                ax.plot(x, y, linewidth=lane.width, color='blue', alpha=0.1, transform=trans)
        for junction in self.junctions.values():
            x=[point[0] for point in junction.shape]
            y=[point[1] for point in junction.shape]
            ax.fill(x, y, color='red',alpha=0.1)
        if show:
            plt.show()
        
    
    def visualize_scene(self, subjects:subjects, t_lim, size=(400,5)):
        plt.figure(figsize=size)
        for edge in self.edges.values():
            for lane in edge.lanes.values():
                x=[point[0] for point in lane.shape]
                y=[point[1] for point in lane.shape]
                plt.plot(x, y, linewidth=lane.width, color='blue',alpha=0.1)
        for junction in self.junctions.values():
            x=[point[0] for point in junction.shape]
            y=[point[1] for point in junction.shape]
            plt.fill(x, y, color='red',alpha=0.1)
        for t_index in range(t_lim):
            sub=[]
            for subject in subjects.subjects.values():
                if subject.valid[t_index]:
                    sub_=plt.plot(subject.pos[t_index][0],subject.pos[t_index][1],'.',color='red',alpha=0.5)
                    sub.append(sub_[0])
            plt.draw()
            plt.pause(0.1)
            for sub_ in sub:
                sub_.remove()

#lane--------------------------------------------------------------------------------------------
class lane:
    '''
    self.id: 
    id string
    self.index: 
    index of lane in the edge
    self.width: 
    width of the lane
    self.shape: 
    list of (x,y) representing the fold line of lane center
    self.subjects: 
    2D ordered array of subjects located in, first dimension represents time_id , second dimension represents subjects
    self.vehicles: 
    2D ordered array of vehicles located in, first dimension represents time_id , second dimension represents vehicles
    '''
    def __init__(self, id, width, shape, subjects=None):
        '''
        :param id: id string
        :param width: width of the lane
        :param shape: list of (x,y) representing the fold line of lane center
        :param subjects: 2D ordered array of subjects located in, first dimension represents time_id , second dimension represents subjects
        '''
        self.id = id
        self.width = width
        self.shape = shape
        self.subjects = subjects

    def speed_disrtibution(self)->tuple:
        '''
        calculate speed distribution
        :return: list of speed distribution
        :return: standard deviation of speed distribution
        '''
        speed_list = [np.linalg.norm(vehicle.vel[time_id]) 
                      for time_id in range(len(self.subjects)) 
                      for vehicle in self.subjects[time_id] ]

        return speed_list,np.std(speed_list)

    def headway(self)->list:
        '''
        calculate headway
        :return: list of headway
        '''
        headway_list = [    self.subjects[time_id][vehicle_index+1].pos_lane[time_id][0] 
                            - self.subjects[time_id][vehicle_index].pos_lane[time_id][0] 
                            for time_id in range(len(self.subjects)) 
                            for vehicle_index in range(len(self.subjects[time_id])-1)   ]
        return headway_list

    def time_headway(self)->list:
        '''
        calculate time headway
        :return: list of time headway
        '''
        time_headway_list = [   self.subjects[time_id][vehicle_index+1].pos_lane[time_id][0] 
                                - self.subjects[time_id][vehicle_index].pos_lane[time_id][0]
                                /np.linalg.norm(self.subjects[time_id][vehicle_index].vel[time_id])
                                for time_id in range(len(self.subjects))
                                for vehicle_index in range(len(self.subjects[time_id])-1)   ]
        return time_headway_list

    def sectional_flow_rate(self)->float:
        '''
        calculate sectional flow rate
        :return: sectional flow rate
        '''
        num = 0
        subjects_now = set(self.subjects[0])
        for time_id in range(1,len(self.subjects)):
            subjects_next = set(self.subjects[time_id])
            num += len(subjects_next - subjects_now)
            subjects_now = subjects_next
        return num/len(self.subjects)  #此处除以帧数，实际应考虑帧时间，即return/帧时间
    
    def calculate_TTC(self):
        '''
        calculate TTC
        :return: list of TTC
        '''
        for i in range(len(self.subjects)):
            for j in range(len(self.subjects[i])-1):
                target = self.subjects[i][j+1]
                follow = self.subjects[i][j]
                target_pos = target.lanePos[i][0]
                follow_pos = follow.lanePos[i][0]
                target_vel = np.linalg.norm(target.vel[i])
                follow_vel = np.linalg.norm(follow.vel[i])
                ttc = TTC(pos_lane_target=target_pos, pos_lane_follow=follow_pos, v_target=target_vel, v_follow=follow_vel, type='ttc')
                follow.ttc[i] = ttc
    
#edge--------------------------------------------------------------------------------------------
class edge:
    '''
    self.id: 
    id string
    self.lanes: 
    list of lanes located in        
    '''
    def __init__(self, id, lanes):
        self.id = id
        #lanes是一个字典
        self.lanes = lanes

    def speed_disrtibution(self, draw_mode='value', save_path=None)->tuple:
        '''
        calculate speed distribution
        :return: list of speed distribution
        :return: standard deviation of speed distribution
        '''
        #统计时间内所有车的数量，如小于2没有意义
        
        speed_list = [np.linalg.norm(vehicle.vel[time_id])
                        for lane in self.lanes
                        for time_id in range(len(lane.subjects))
                        for vehicle in lane.subjects[time_id]]
        if draw_mode == 'value':
            plt.clf()
            plt.hist(speed_list, bins=100)
            plt.xlabel('speed')
            plt.ylabel('number')
            plt.title('speed distribution: '+self.id)
            if save_path != None:
                plt.savefig(save_path)
            else:
                plt.show()
        return speed_list,np.std(speed_list)

    def headway(self, draw_mode='value', save_path = None)->list:
        '''
        calculate headway
        :return: list of headway
        '''
        #统计时间内所有车的数量，如小于2没有意义
        num=[]
        for lane in self.lanes.values():
            for time_id in range(len(lane.subjects)):
                num.append(len(lane.subjects[time_id]))
        if max(num)<=2:
            return None
        headway_list = [    lane.subjects[time_id][vehicle_index+1].lanePos[time_id][0] 
                            - lane.subjects[time_id][vehicle_index].lanePos[time_id][0] 
                            for lane in self.lanes.values()
                            for time_id in range(len(lane.subjects)) 
                            for vehicle_index in range(len(lane.subjects[time_id])-1)   ]
        if draw_mode == 'value':
            plt.clf()
            plt.hist(headway_list, bins=100, density=True,alpha=0.5,
                    histtype='stepfilled', color='steelblue',
                    edgecolor='steelblue')
            plt.xlabel('headway')
            plt.ylabel('number')
            plt.title('headway distribution: '+self.id)
            if save_path != None:
                plt.savefig(save_path)
            else:
                plt.show()
        return headway_list

    def time_headway(self, draw_mode='value', save_path=None)->list:
        '''
        calculate time headway
        :return: list of time headway
        '''
        time_headway_list = [   lane.subjects[time_id][vehicle_index+1].pos_lane[time_id][0] 
                                - lane.subjects[time_id][vehicle_index].pos_lane[time_id][0]
                                /np.linalg.norm(lane.subjects[time_id][vehicle_index].vel[time_id])
                                for lane in self.lanes
                                for time_id in range(len(lane.subjects))
                                for vehicle_index in range(len(lane.subjects[time_id])-1)   ]
        if draw_mode == 'value':
            plt.clf()
            plt.hist(time_headway_list, bins=100)
            plt.xlabel('time headway')
            plt.ylabel('number')
            plt.title('time headway distribution: '+self.id)
            if save_path != None:
                plt.savefig(save_path)
            else:
                plt.show()
        return time_headway_list

    def sectional_flow_rate(self)->float:
        '''
        calculate sectional flow rate
        :return: sectional flow rate
        '''
        flow_rate = 0
        for lane in self.lanes:
            flow_rate += lane.sectional_flow_rate()
        return flow_rate
    
    def viusalize(self, t_lim):
        plt.clf()
        for lane in self.lanes.values():
            print(lane.width)
            x=[point[0] for point in lane.shape]
            y=[point[1] for point in lane.shape]

            plt.plot(x, y, linewidth=lane.width, color='blue',alpha=0.1)

        for t_index in range(t_lim):
            sub=[]
            for lane in self.lanes.values():
                for subject in lane.subjects[t_index]:
                    sub_=plt.plot(subject.pos[t_index][0],subject.pos[t_index][1],'.',color='red',alpha=0.5)
                    sub.append(sub_[0])
                if lane.subjects[t_index] != []:
                    sub_=plt.plot(lane.subjects[t_index][0].pos[t_index][0],lane.subjects[t_index][0].pos[t_index][1],'.',color='k',alpha=1)
                    sub.append(sub_[0])
            plt.draw()
            plt.pause(0.1)
            for sub_ in sub:
                sub_.remove()

    def calculate_TTC(self):
        '''
        calculate TTC
        :return: list of TTC
        '''
        for lane in self.lanes.values():
            lane.calculate_TTC()
#junction--------------------------------------------------------------------------------------------
class junction:
    '''
    self.id: 
    id string
    self.loc: 
    (x,y) representing the center of junction
    self.shape: 
    list of (x,y) representing the fold line of junction outline
    self.subjects: 
    list of subjects located in
    '''
    def __init__(self, id, loc, shape, subjects=None):
        self.id = id
        self.shape = shape
        self.loc = loc
        self.subjects = subjects
        
def main():

    s=subjects(sample_time=1)
    s.initFromCSV("../testData/processed_tracks2.csv")
    m = map()
    m.loadfromxml("../testData/highDmap.net.xml")
    m.load_vehicles(s)

    # m.visualize_scene(s, 500)
    #draw ttc distribution
    for edge in m.edges.values():
        edge.calculate_TTC()
    ttc_list=[]
    for edge in tqdm(m.edges.values()):
        for lane in edge.lanes.values():
            for time_id in range(len(lane.subjects)):
                for subject in lane.subjects[time_id]:
                        ttc_list.append(subject.ttc[time_id])
                print(len(ttc_list))
    ttc_list = [i for i in ttc_list if i != None and i > 0 and i <100]
    print(ttc_list)
    plt.hist(ttc_list, bins=100, width = (max(ttc_list)-min(ttc_list))/100)
    plt.xlabel('TTC')
    plt.ylabel('number')
    plt.title('TTC distribution')
    plt.show()
    '''
    #draw ttc distribution
    for edge in m.edges.values():
        edge.calculate_TTC()
    ttc_list=[]
    for edge in tqdm(m.edges.values()):
        for lane in edge.lanes.values():
            for time_id in range(len(lane.subjects)):
                for subject in lane.subjects[time_id]:
                        ttc_list.append(subject.ttc[time_id])
                print(len(ttc_list))
    ttc_list = [i for i in ttc_list if i != None and i > 0 and i <1000]
    print(ttc_list)
    plt.hist(ttc_list, bins=100, width = (max(ttc_list)-min(ttc_list))/100)
    plt.xlabel('TTC')
    plt.ylabel('number')
    plt.title('TTC distribution')
    plt.show()

    '''
    
if __name__ == "__main__":
    main()