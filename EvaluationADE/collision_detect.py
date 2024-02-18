from n_circle_appro import n_circle

import numpy as np

from enum import Enum

class collision_type(Enum):
    '''
    collision type
    '''
    head_on = 1
    rear_end = 2
    angle = 3
    side_swipe = 4

class pos(Enum):
    '''
    relative position
    '''
    front = 1
    back = 2
    side = 3

def normalize_angle(angle):
    angle = (angle + np.pi) % (2*np.pi) - np.pi
    return angle
  
def collision_detect(n_circle1:n_circle, 
                 n_circle2:n_circle)->bool:
    '''
    :param n_circle1: n_circle
    :param n_circle2: n_circle
    :return: True if collision, False if not
    '''
    for center1 in n_circle1.centers:
        for center2 in n_circle2.centers:
            if (center1[0]-center2[0])**2+(center1[1]-center2[1])**2 < (n_circle1.r+n_circle2.r)**2:
                return True
    return False

def collision_type_detect(heading1, 
                      pos1, 
                      width1, 
                      length1, 
                      heading2, 
                      pos2, 
                      width2, 
                      length2):
    '''
    :param heading1: heading of vehicle 1
    :param pos1: (x,y) of center of vehicle 1
    :param width1: width of vehicle 1
    :param length1: length of vehicle 1
    :param heading2: heading of vehicle 2
    :param pos2: (x,y) of center of vehicle 2
    :param width2: width of vehicle 2
    :param length2: length of vehicle 2
    :return: collision type
    '''
    #这里认为输入的heading是角度值
    #弧度制是
    #relative_heading = normalize_angle(np.radians(heading1-heading2))
    heading1 = normalize_angle(np.radians(heading1))
    heading2 = normalize_angle(np.radians(heading2))
    relative_heading = heading1-heading2
    relative_heading = normalize_angle(relative_heading)
    relative_heading = np.abs(relative_heading)

    relative_pos = (pos1[0]-pos2[0], pos1[1]-pos2[1])
    relative_pos_angle = np.arctan2(relative_pos[1], relative_pos[0])
    
    diagonal_angle1 = np.arctan2(width1, length1)

    pos_angle = np.abs(normalize_angle(relative_pos_angle-heading1))
    if pos_angle < diagonal_angle1:
        pos_ = pos.back
    elif pos_angle > np.pi-diagonal_angle1:
        pos_ = pos.front
    else:
        pos_ = pos.side
    
    collision_type_ = collision_type.angle

    if pos_ == pos.back:
        if relative_heading < np.pi/6:
            collision_type_ = collision_type.rear_end
    elif pos_ == pos.front:
        if relative_heading < np.pi/6:
            collision_type_ = collision_type.rear_end
        elif relative_heading > np.pi*5/6:
            collision_type_ = collision_type.head_on
    elif pos_ == pos.side:
        if relative_heading < np.pi/6:
            collision_type_ = collision_type.side_swipe
    
    return collision_type_

def collision_relative_speed(v1,
                             v2):
    return np.linalg.norm(v1-v2)


        
