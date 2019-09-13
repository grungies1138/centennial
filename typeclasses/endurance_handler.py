from evennia import DefaultScript
import random


class EnduranceHandler(DefaultScript):
    def at_script_creation(self):
        self.db.max_endurance = 0
        self.db.endurance = 0
        self.key = "endurance_handler_%i" % random.randint(0, 10000)
        self.desc = "Endurance Handler"
        self.interval = 60 * 15
        self.db.character = None
        self.repeats = -1
        self.persistent = True

    def get(self):
        return self.db.endurance

    def increment(self, value):
        if (self.db.endurance + value) <= self.db.max_endurance:
            self.db.endurance += value
        else:
            self.db.endurance = self.db.max_endurance

    def decrement(self, value):
        if self.db.endurance - value <= (self.db.max_endurance / 2) * -1:
            raise EnduranceException("Endurance is drained.  Action cannot be performed.")
        self.db.endurance -= value

    def set_character(self, char):
        self.db.character = char

    def set_max(self, value):
        self.db.max_endurance = value
        self.db.endurance = value

    def at_repeat(self):
        if self.db.endurance < self.db.max_endurance:
            self.increment(self.db.max_endurance / 10)


class EnduranceException(Exception):
    pass
