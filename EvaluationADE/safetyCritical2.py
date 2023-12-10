from subject import *
from map import *
def segment_integrals(arr):
    '''
    :param arr: n*1
    :return: m*1
    '''
    diff_arr = np.diff(arr)
    positive_indices = np.where(diff_arr > 0)[0]
    diff_positive_indices = np.diff(positive_indices)
    segment_end_indices = np.concatenate(([positive_indices[0]], positive_indices[np.where(diff_positive_indices != 1)[0] + 1], [len(arr) - 1]))
    
    segment_integrals = []
    for start_index, end_index in zip(segment_end_indices[:-1], segment_end_indices[1:]):
        segment_values = arr[start_index+1:end_index+1]
        segment_integral = np.trapz(segment_values)
        segment_integrals.append(segment_integral)
    
    return segment_integrals

class safetyCritical2:
    def __init__(self,subjects:subjects,entity):
        #entity: map or edge
        self.subjects = subjects
        self.entity = entity
# Collison Time Metrics--------------------------------------------------------------

    def TET(self,threshold):
        '''
        :param threshold: the threshold of time
        :return: segmented Time Exposed TTC
        '''
        TET=np.zeros(1)
        if type(self.entity) == map:
            for id in self.subjects.subjects:
                subject=self.subjects.subjects[id]
                validTTC=subject.TTC[subject.valid]
                validTTC[validTTC>=threshold]=0.0
                validTTC[validTTC<threshold]=1.0
                diffTTC=np.concatenate(validTTC[0],np.diff(validTTC))#1*n
                TETbegin=np.where(diffTTC==1.0)[0]
                TETend=np.where(diffTTC==-1.0)[0]
                if len(TETbegin)!=len(TETend):
                    np.append(TETend,len(validTTC)-1)
                subject.TET=(TETend-TETbegin)*subject.sample_time
                TET=np.concatenate(TET,(TETend-TETbegin)*subject.sample_time)
        else:
            for id in self.subjects.subjects:
                subject=self.subjects.subjects[id]
                validTTC=subject.TTC[subject.edges==self.entity.id]
                validTTC[validTTC>=threshold]=0.0
                validTTC[validTTC<threshold]=1.0
                diffTTC=np.concatenate(validTTC[0],np.diff(validTTC))#1*n
                TETbegin=np.where(diffTTC==1.0)[0]
                TETend=np.where(diffTTC==-1.0)[0]
                if len(TETbegin)!=len(TETend):
                    np.append(TETend,len(validTTC)-1)
                TET=np.concatenate(TET,(TETend-TETbegin)*subject.sample_time)
        return TET[1:]
    
    def TIT(self,threshold):
        
                    
                

# Collision Risk Metrics--------------------------------------------------------------



# Collision Vel/Acc Metrics--------------------------------------------------------------