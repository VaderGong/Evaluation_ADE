from test_class1 import *
class D(B ):
    def __init__(self):
        super().__init__()
        self.g = 7
        self.h = 8
class E(C,A):
    def __init__(self):
        super().__init__()
        self.i = 9
        self.j = 10