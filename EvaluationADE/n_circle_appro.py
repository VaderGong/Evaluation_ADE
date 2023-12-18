import numpy as np
import math
from matplotlib import pyplot as plt
class n_circle:
    '''
    self.n: the number of circles
    self.r: the radius of circle
    self.centers: list of (x,y) of center
    self.centers_lane: list of (x,y) of center relative to the lane
    '''
    def __init__(self, heading, pos:list, width:float, length:float):
        '''
        :param pos: (x,y) of center
        :param pos_lane: (x,y) of center relative to the lane
        :param width: width of lane
        :param length: length of lane
        '''
        self.r = width/2
        self.n, self.centers=self.c(heading, pos, length, self.r)

    def c(self, heading, pos, length, r)->list:
        '''
        :return: list of (x,y)
        '''
        n = int(math.ceil(length/(2*r)))
        centers = []
        backcenter = (pos[0]-length/2*np.cos(heading), pos[1]-length/2*np.sin(heading))
        d = (length-2*r)/(n-1)
        c1 = (backcenter[0]+r*np.cos(heading), backcenter[1]+r*np.sin(heading))
        centers.append(c1)
        for i in range(1,n):
            centers.append((c1[0]+i*d*np.cos(heading), c1[1]+i*d*np.sin(heading)))
        
        return n, centers
            

def main():
    test = n_circle(math.pi/6, (0,0), 4, 10)
    print(test.n)
    print(test.centers)
    print(test.r)
    fig, ax = plt.subplots()

    plt.xlim(-15,15)
    plt.ylim(-15,15)
    for center in test.centers:
        circle = plt.Circle(center, test.r, color='r', fill=False)
        ax.add_artist(circle)
    ax.set_aspect('equal')
    plt.show()
    
if __name__ == '__main__':  
    main()

    

    


