class map:
    def __init__(self):
        self.edges=[edge()]
        self.junctions=[junction()]
        pass

class lane:
    '''
    self.id: id string
    self.width: width of the lane
    self.shape: list of (x,y) representing the fold line of lane center
    self.subjects: 2D ordered list of subjects located in, first dimension represents time_id , second dimension represents subjects
    '''
    def __init__(self):
        pass

    def speed_disrtibution(self)->tuple:
        '''
        calculate speed distribution
        :return: list of speed distribution
        :return: standard deviation of speed distribution
        '''
        pass

    def headway(self)->list:
        '''
        calculate headway
        :return: list of headway
        '''
        pass

    def time_haedway(self)->list:
        '''
        calculate time headway
        :return: list of time headway
        '''
        pass

    def sectional_flow_rate(self)->float:
        '''
        calculate sectional flow rate
        :return: sectional flow rate
        '''
        pass

class edge:
    '''
    self.id: id string
    self.lanes: list of lanes located in        
    '''
    def __init__(self):
        self.lanes=[lane()]
        pass

    def speed_disrtibution(self)->tuple:
        '''
        calculate speed distribution
        :return: list of speed distribution
        :return: standard deviation of speed distribution
        '''
        pass

    def headway(self)->list:
        '''
        calculate headway
        :return: list of headway
        '''
        pass

    def time_haedway(self)->list:
        '''
        calculate time headway
        :return: list of time headway
        '''
        pass

    def sectional_flow_rate(self)->float:
        '''
        calculate sectional flow rate
        :return: sectional flow rate
        '''
        pass

class junction:
    '''
    self.id: id string
    self.shape: list of (x,y) representing the fold line of junction outline
    self.subjects: list of vehicles located in
    '''
    def __init__(self):
        pass
