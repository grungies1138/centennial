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

class Dog(Mammal):
    self.legs = 4
    self.arms=0
    def __init__(self):
        pass