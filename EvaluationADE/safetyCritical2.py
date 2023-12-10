from subject import *
from map import *
def segment_integrals(arr):
    """
    :param arr: n*1 float array, 0 and segmented positive values
    :return: m*1 float array, the integral of each segment
    """
    posIdx = np.where(arr > 0.0)[0]
    diffIdx = np.diff(posIdx)
    SegBeginIdx = np.concatenate((np.array([0]),posIdx[np.where(diffIdx != 1)[0] + 1]))
    SegBeginIdx = np.append(SegBeginIdx, posIdx[-1]+1)
    segment_integrals = np.array([np.sum(arr[SegBeginIdx[i]:SegBeginIdx[i + 1]]) for i in range(len(SegBeginIdx) - 1)])
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
                diffTTC=np.concatenate((validTTC[0],np.diff(validTTC)))#1*n
                TETbegin=np.where(diffTTC==1.0)[0]
                TETend=np.where(diffTTC==-1.0)[0]
                if len(TETbegin)!=len(TETend):
                    np.append(TETend,len(validTTC)-1)
                subject.TET=(TETend-TETbegin)*subject.sample_time
                TET=np.concatenate((TET,(TETend-TETbegin)*subject.sample_time))
        else:
            for id in self.subjects.subjects:
                subject=self.subjects.subjects[id]
                validTTC=subject.TTC[subject.edges==self.entity.id]
                validTTC[validTTC>=threshold]=0.0
                validTTC[validTTC<threshold]=1.0
                diffTTC=np.concatenate((validTTC[0],np.diff(validTTC)))#1*n
                TETbegin=np.where(diffTTC==1.0)[0]
                TETend=np.where(diffTTC==-1.0)[0]
                if len(TETbegin)!=len(TETend):
                    np.append(TETend,len(validTTC)-1)
                TET=np.concatenate((TET,(TETend-TETbegin)*subject.sample_time))
        return TET[1:]
    
    def TIT(self,threshold):
        """
        :param threshold: the threshold of time
        :return: segmented Time Integrated TTC
        """
        TIT=np.zeros(1)
        if type(self.entity)==map:
            for id in self.subjects.subjects:
                subject=self.subjects.subjects[id]
                validTTC=subject.TTC[subject.valid]
                TTCLessThrs=threshold-validTTC
                subject.TIT=segment_integrals(TTCLessThrs)
                TIT=np.concatenate((TIT,subject.TIT))
        else:
            for id in self.subjects.subjects:
                subject=self.subjects.subjects[id]
                validTTC=subject.TTC[subject.edges==self.entity.id]
                TTCLessThrs=threshold-validTTC
                nowTIT=segment_integrals(TTCLessThrs)
                TIT=np.concatenate((TIT,nowTIT))
        return TIT[1:]

                    
                

# Collision Risk Metrics--------------------------------------------------------------

    def CollisionProbability(self,delta):
        """
        :param delta: scale parameter
        :return: segmented Collision Probability
        """
        CP=np.zeros(1)
        if type(self.entity)==map:
            for id in self.subjects.subjects:
                subject=self.subjects.subjects[id]
                validTTC=subject.TTC[subject.valid]
                scaledTTC=validTTC/delta
                CP=np.concatenate((CP,np.exp(scaledTTC)))
        else:
            for id in self.subjects.subjects:
                subject=self.subjects.subjects[id]
                validTTC=subject.TTC[subject.edges==self.entity.id]
                scaledTTC=validTTC/delta
                CP=np.concatenate((CP,np.exp(scaledTTC)))
        return CP[1:]
    
    def SeverityIndex(self,PRT):
        """
        exp(-TTC^2/PRT^2)
        :param PRT:perception and braking reaction time
        :return: segmented Severity Index
        """
        SI=np.zeros(1)
        if type(self.entity)==map:
            for id in self.subjects.subjects:
                subject=self.subjects.subjects[id]
                validTTC=subject.TTC[subject.valid]
                nowSI=np.exp(-np.square(validTTC/PRT)/2)
                np.concatenate((SI,nowSI))
        else:
            for id in self.subjects.subjects:
                subject=self.subjects.subjects[id]
                validTTC=subject.TTC[subject.edges==self.entity.id]
                nowSI=np.exp(-np.square(validTTC/PRT)/2)
                np.concatenate((SI,nowSI))
        return SI[1:]
    
# Collision Vel/Acc Metrics--------------------------------------------------------------
    def RequiredDecelerationRate(self):
        """
        Speed/(2*PET)
        :return: segmented Required Deceleration Rate
        """
        RDR=np.zeros(1)
        if type(self.entity)==map:
            for id in self.subjects.subjects:
                subject=self.subjects.subjects[id]
                validPET=subject.PET[subject.valid]
                validSpeed=np.linalg.norm(subject.vel[subject.valid],axis=1)
                nowRDR=validSpeed/(2*validPET)
                np.concatenate((RDR,nowRDR))
        else:
            for id in self.subjects.subjects:
                subject=self.subjects.subjects[id]
                validPET=subject.PET[subject.edges==self.entity.id]
                validSpeed=np.linalg.norm(subject.vel[subject.edges==self.entity.id],axis=1)
                nowRDR=validSpeed/(2*validPET)
                np.concatenate((RDR,nowRDR))
        return RDR[1:]
    
    def CriticalSpeed(self,alpha):
        """
        PET*alpha/0.039
        :param alpha: the coefficient 
        :return: segmented Critical Speed
        """
        CS=np.zeros(1)
        if type(self.entity)==map:
            for id in self.subjects.subjects:
                subject=self.subjects.subjects[id]
                validPET=subject.PET[subject.valid]
                nowCS=validPET*alpha/0.039
                np.concatenate((CS,nowCS))
        else:
            for id in self.subjects.subjects:
                subject=self.subjects.subjects[id]
                validPET=subject.PET[subject.edges==self.entity.id]
                nowCS=validPET*alpha/0.039
                np.concatenate((CS,nowCS))
        return CS[1:]