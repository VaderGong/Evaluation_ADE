from map import map, edge, lane, junction
from enum import Enum
from subject import subject

class TTCtype(Enum):
    TTC = 1
    MTTC = 2
    ETTC = 3

class SafetyCritical:
    def __init__(self,entity)  -> None:
        self.TTC=None
        self.PET=None
        self.DRAC=None
        self.TIT=None
        self.TET=None
        self.TTCtype=None

    def isConflict(self,v1:subject,v2:subject) -> None:
        """
        judge if v1 and v2 is conflict
        return True if conflict
        """
    pass

    def TTC(self, v_target:float, v_follow:float, a_target:float=None, a_follow:float=None, type:str='TTC'):
        '''
        :param v_target:   
        :param v_follow:      
        '''

        #TTC
        
        #MTTC

        #ETTC
        self.TTCtype=TTCtype
        ret=[]
        self.TTC=ret
        return ret
        
        
        
    def PET(self):# -> list:
        """
        return list of (PET value, time, v1 id, v2 id)
        """
        
        ret=[]
        self.PET=ret
        return ret
      
    def TET(self,threshold):# -> list:
        """
        """
        if self.TTC==None:
            self.TTC()
        else:
            pass
        ret=[]
        self.TET=ret
        return ret
    def TIT(self,threshold):# -> list:
        """
        """
        if self.TTC==None:
            self.TTC()
        else:
            pass
        ret=[]
        self.TIT=ret
        return ret
        
    def TimeToIntersection(self) -> None:
        pass
    
    def CTM(self) -> None:
        """"""
        #judge if TTC,TIT,TET has been computed
        if self.TTC==None:
            self.TTC()
        
        if self.TET==None:
            self.TET()
        
        if self.TIT==None:
            self.TIT()
    def TTCD(self) -> None:
        """"""
        pass
    
    def mnpETTC(self) -> None:
        if self.TTCtype !=3:
            self.TTC(3)
    def DRAC(self):# -> list:
        ret=[]
        self.DRAC=ret
        return ret
       
    
    def BrakeReactionTime(self) -> None:
        self.isConflict()
        pass
    
    def ConflictIntensity(self) -> None:
        self.isConflict()
        pass
    def PSD(self) -> None:
        """
        compute Proportion of Stopping Distance
        """
    def CrashPotentialIndex(self) -> None:
        if self.DRAC==None:
            self.DRAC()
    
    
    