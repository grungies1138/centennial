class Mammal:
    self.arms = 2
    self.legs = 2
    self.eyes = 2
    def __init__(self):
        pass

class Human(Mammal):
    self.hair = ""
    def __init__(self, hair):
        Mammal.__init__(self)
        self.hair = hair

