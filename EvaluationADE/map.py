class map:
    def __init__(self):
        pass

class lane:
    '''
    self.id: id string
    self.width: width of the lane
    self.shape: list of (x,y) representing the fold line of lane center
    self.subjects: 2D list of subjects located in, first dimension represents time_id , second dimension represents subjects
    '''
    def __init__(self):
        pass

class edge:
    '''
    self.id: id string
    self.lanes: list of lanes located in        
    '''
    def __init__(self):
        pass

class junction:
    '''
    self.id: id string
    self.shape: list of (x,y) representing the fold line of junction outline
    self.vehicles: list of vehicles located in
    '''
    def __init__(self):
        pass
