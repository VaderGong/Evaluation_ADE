from map import map, edge, lane, junction
from enum import Enum
from subject import subject
class TTCtype(Enum):
    TTC = 1
    MTTC = 2
    ETTC = 3
    


class SafetyCritical:
    def __init__(self,entity) :
        self.TTC=None
        self.PET=None
        self.DRAC=None
        self.TIT=None
        self.TET=None
        self.TTCtype=None

    def isConflict(self,v1:subject,v2:subject):
        """
        judge if v1 and v2 is conflict
        return True if conflict
        """
    pass

    def TTC(self,type:TTCtype=1):
        """
        return list of (TTC value, time, v1 id, v2 id)
        """
        self.TTCtype=TTCtype
        ret=[]
        self.TTC=ret
        return ret
        
        
        
    def PET(self):
        """
        return list of (PET value, time, v1 id, v2 id)
        """
        
        ret=[]
        self.PET=ret
        return ret
      
    def TET(self,threshold):
        """
        """
        if self.TTC==None:
            self.TTC()
        else:
            pass
        ret=[]
        self.TET=ret
        return ret
    def TIT(self,threshold):
        """
        """
        if self.TTC==None:
            self.TTC()
        else:
            pass
        ret=[]
        self.TIT=ret
        return ret
        
    def TimeToIntersection(self):
        pass
    
    def CTM(self):
        """"""
        #judge if TTC,TIT,TET has been computed
        if self.TTC==None:
            self.TTC()
        
        if self.TET==None:
            self.TET()
        
        if self.TIT==None:
            self.TIT()
    def TTCD(self):
        """"""
        pass
    
    def mnpETTC(self):
        if self.TTCtype !=3:
            self.TTC(3)
    def DRAC(self):
        ret=[]
        self.DRAC=ret
        return ret
       
    
    def BrakeReactionTime(self):
        self.isConflict()
        pass
    
    def ConflictIntensity(self):
        self.isConflict()
        pass
    def PSD(self):
        """
        compute Proportion of Stopping Distance
        """
    def CrashPotentialIndex(self):
        if self.DRAC==None:
            self.DRAC()
    
    
    