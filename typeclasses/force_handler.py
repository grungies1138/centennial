from evennia import DefaultScript
import random


class ForceHandler(DefaultScript):
    def at_script_creation(self):
        self.db.attack = 0
        self.db.defend = 0
        self.db.neutral = 0
        self.db.alignment = 0
        self.db.key = "Force_handler_%i" % random.randint(1, 10000)
        self.db.desc = "Force Handler"
        self.db.character = None
        self.persistent = True

    def get_attack(self):
        return self.db.attack

    def get_defend(self):
        return self.db.defend

    def get_neutral(self):
        return self.db.neutral

    def get_force(self):
        return (self.get_attack() + self.get_defend() + self.get_neutral()) / 3

    def set_attack(self, value):
        self.db.attack += int(value)

    def set_defend(self, value):
        self.db.defend += int(value)

    def set_neutral(self, value):
        self.db.neutral += int(value)

    def set_character(self, char):
        self.db.character = char

    def get_alignment(self):
        return self.db.alignment

    def set_alignment(self, value):
        self.db.alignment = value
