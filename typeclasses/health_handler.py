from evennia import DefaultScript
import random

WOUNDS = {"mortal": 75, "severe": 50, "moderate": 25}

HEALTH_STATUS = {"natural": 1, "medkit": 2, "cannister": 4, "tank": 8}

BASE_HEAL_RATE = 5


class HealthHandler(DefaultScript):
    def at_script_creation(self):
        self.db.key = "health_handler_%i" % random.randint(1, 10000)
        self.db.desc = "health handler"
        self.db.character = None
        self.persistent = True
        self.interval = 144 * 60  # every 15 minutes
        self.db.max_health = 0
        self.db.current_health = 0
        self.db.temp_health = 0
        self.db.mod = 0
        self.db.wounds = {}
        self.db.heal_rate = BASE_HEAL_RATE
        self.db.health_status = 1

    def get(self):
        return self.db.current_health + self.db.temp_health + self.db.mod

    def set_max_health(self, value):
        """Sets the initial Max health value."""
        self.db.max_health = value

    def damage(self, value):
        if value > self.db.temp_health:
            overflow = value - self.db.temp_health
            self.db.temp_health = 0
            self.db.current_health -= overflow
        elif value <= self.db.temp_health:
            self.db.temp_health -= value
        else:
            self.db.current_health -= value

    def mod(self, value):
        self.db.mod += value

    def set_character(self, char):
        self.db.character = char

    def heal(self, value):
        if value >= self.db.max_health:
            self.db.current_health = self.db.max_health
            self.db.heal_rate = HEALTH_STATUS.get("natural")

    def wound(self, value):
        if value.lower() in WOUNDS:
            self.db.wounds.update(value)
        else:
            self.db.character.msg("That is not a valid Wound")

    def get_wound(self):
        return self.db.wounds

    def set_heal_status(self, status):
        if status.lower() in HEALTH_STATUS:
            self.db.health_status = HEALTH_STATUS.get(status.lower())

    def at_repeat(self):
        heal_amount = self.db.max_health / (self.db.heal_rate * self.db.health_status)
        self.heal(heal_amount)
