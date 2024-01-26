from map import map, edge, lane, junction
from enum import Enum
from subject import subject

def TTC(    pos_lane_target:float,  pos_lane_follow:float, 
            v_target:float,         v_follow:float, 
            a_target:float=None,    a_follow:float=None, 
            type:str='ttc'                                  ):
    '''
    :param v_target: speed of front vehicle
    :param v_follow: speed of following vehicle
    :param a_target: acceleration of front vehicle, can ba None if TTCtype is TTC, MTTC
    :param a_follow: acceleration of following vehicle, can ba None if TTCtype is TTC
    '''
    type=type.lower()
    #TTC
    if type == 'ttc':
        return None if v_follow-v_target <= 0 \
        else abs(pos_lane_follow - pos_lane_target) / (v_follow - v_target) 
    
    #MTTC,take  into consideration
    elif type == 'mttc':
        delta_v = v_follow-v_target
        d = abs(pos_lane_follow - pos_lane_target)
        mttc1 = (-delta_v + (delta_v**2 + 2*a_follow*d)**0.5)/a_follow
        mttc2 = (-delta_v - (delta_v**2 + 2*a_follow*d)**0.5)/a_follow
        return None if mttc1 < 0 and mttc2 < 0\
            else mttc1 if mttc2 < 0\
            else mttc2 if mttc1 < 0\
            else min(mttc1, mttc2)
    
    #ETTC
    elif type == 'ettc':
        delta_v = v_follow-v_target
        delta_a = a_follow-a_target
        d = abs(pos_lane_follow - pos_lane_target)
        ettc1 = (-delta_v + (delta_v**2 + 2*delta_a*d)**0.5)/delta_a
        ettc2 = (-delta_v - (delta_v**2 + 2*delta_a*d)**0.5)/delta_a
        return None if ettc1 < 0 and ettc2 < 0\
            else ettc1 if ettc2 < 0\
            else ettc2 if ettc1 < 0\
            else min(ettc1, ettc2)
    else:
        raise Exception('TTC type error, should be TTC, MTTC or ETTC')