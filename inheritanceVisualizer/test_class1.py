class A():
    def __init__(self):
        self.a = 1
        self.b = 2
class B(A):
    def __init__(self):
        super().__init__()
        self.c = 3
        self.d = 4
class C(B):
    def __init__(self):
        super().__init__()
        self.e = 5
        self.f = 6