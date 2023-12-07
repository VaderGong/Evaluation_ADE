import numpy as np
import xml.dom.minidom as minidom
import matplotlib.pyplot as plt
class map:
    def __init__(self):
        self.edges = {}
        self.junctions = {}

    def loadfromxml(self, xml_path):
        DomTree = minidom.parse(xml_path)
        collection = DomTree.documentElement

        edges = collection.getElementsByTagName("edge")
        for edge_ in edges:
            id = str(edge_.getAttribute("id"))
            lanes = edge_.getElementsByTagName("lane")
            l_list=[]
            for lane_ in lanes:
                id = str(lane_.getAttribute("id"))
                width = float(lane_.getAttribute("width"))
                shape_ = lane_.getAttribute("shape")
                shape_ = shape_.split(" ")
                shape = [i.split(',') for i in shape_]
                shape = [[float(i[0]),float(i[1])] for i in shape]
                l = lane(id, width, shape, [])
                l_list.append(l)
            e = edge(id, l_list)
            self.edges[id] = e
            l_list=[]

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

    def visualize(self):
        for edge in self.edges.values():
            for lane in edge.lanes:
                x=[point[0] for point in lane.shape]
                y=[point[1] for point in lane.shape]
                plt.plot(x, y, linewidth=lane.width, color='blue',alpha=0.1)
        for junction in self.junctions.values():
            x=[point[0] for point in junction.shape]
            y=[point[1] for point in junction.shape]
            plt.fill(x, y, color='red',alpha=0.1)
        

class lane:
    '''
    self.id: id string
    self.index: index of lane in the edge
    self.width: width of the lane
    self.shape: list of (x,y) representing the fold line of lane center
    self.subjects: 2D ordered array of subjects located in, first dimension represents time_id , second dimension represents subjects
    self.vehicles: 2D ordered array of vehicles located in, first dimension represents time_id , second dimension represents vehicles
    '''
    def __init__(self, id, width, shape, subjects):
        self.id = id
        self.width = width
        self.shape = shape
        self.subjects = subjects
        self.vehicles = [[subject for subject in time if subject.type== 'vehicle'] for time in self.subjects]

    def speed_disrtibution(self)->tuple:
        '''
        calculate speed distribution
        :return: list of speed distribution
        :return: standard deviation of speed distribution
        '''
        speed_list = [np.linalg.norm(vehicle.vel[time_id]) 
                      for time_id in range(len(self.vehicles)) 
                      for vehicle in self.vehicles[time_id] ]

        return speed_list,np.std(speed_list)

    def headway(self)->list:
        '''
        calculate headway
        :return: list of headway
        '''
        headway_list = [    self.vehicles[time_id][vehicle_index+1].pos_lane[time_id][0] 
                            - self.vehicles[time_id][vehicle_index].pos_lane[time_id][0] 
                            for time_id in range(len(self.vehicles)) 
                            for vehicle_index in range(len(self.vehicles[time_id])-1)   ]
        return headway_list

    def time_haedway(self)->list:
        '''
        calculate time headway
        :return: list of time headway
        '''
        time_headway_list = [   self.vehicles[time_id][vehicle_index+1].pos_lane[time_id][0] 
                                - self.vehicles[time_id][vehicle_index].pos_lane[time_id][0]
                                /np.linalg.norm(self.vehicles[time_id][vehicle_index].vel[time_id])
                                for time_id in range(len(self.vehicles))
                                for vehicle_index in range(len(self.vehicles[time_id])-1)   ]
        return time_headway_list

    def sectional_flow_rate(self)->float:
        '''
        calculate sectional flow rate
        :return: sectional flow rate
        '''
        num = 0
        vehicles_now = set(self.vehicles[0])
        for time_id in range(1,len(self.vehicles)):
            vehicles_next = set(self.vehicles[time_id])
            num += len(vehicles_next - vehicles_now)
            vehicles_now = vehicles_next
        return num/len(self.vehicles)  #此处除以帧数，实际应考虑帧时间，即return/帧时间

class edge:
    '''
    self.id: id string
    self.lanes: list of lanes located in        
    '''
    def __init__(self, id, lanes):
        self.id = id
        self.lanes = lanes

    def speed_disrtibution(self)->tuple:
        '''
        calculate speed distribution
        :return: list of speed distribution
        :return: standard deviation of speed distribution
        '''
        speed_list = [np.linalg.norm(vehicle.vel[time_id])
                        for lane in self.lanes
                        for time_id in range(len(lane.vehicles))
                        for vehicle in lane.vehicles[time_id]]
        return speed_list,np.std(speed_list)

    def headway(self)->list:
        '''
        calculate headway
        :return: list of headway
        '''
        headway_list = [    lane.vehicles[time_id][vehicle_index+1].pos_lane[time_id][0] 
                            - lane.vehicles[time_id][vehicle_index].pos_lane[time_id][0] 
                            for lane in self.lanes
                            for time_id in range(len(lane.vehicles)) 
                            for vehicle_index in range(len(lane.vehicles[time_id])-1)   ]
        return headway_list

    def time_haedway(self)->list:
        '''
        calculate time headway
        :return: list of time headway
        '''
        time_headway_list = [   lane.vehicles[time_id][vehicle_index+1].pos_lane[time_id][0] 
                                - lane.vehicles[time_id][vehicle_index].pos_lane[time_id][0]
                                /np.linalg.norm(lane.vehicles[time_id][vehicle_index].vel[time_id])
                                for lane in self.lanes
                                for time_id in range(len(lane.vehicles))
                                for vehicle_index in range(len(lane.vehicles[time_id])-1)   ]
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

class junction:
    '''
    self.id: id string
    self.loc: (x,y) representing the center of junction
    self.shape: list of (x,y) representing the fold line of junction outline
    self.subjects: list of vehicles located in
    '''
    def __init__(self, id, loc, shape, subjects):
        self.id = id
        self.shape = shape
        self.loc = loc
        self.subjects = subjects
        
def main():
    m = map()
    m.loadfromxml("testData/Town04.net.xml")
    m.visualize()
    plt.show()

if __name__ == "__main__":
    main()