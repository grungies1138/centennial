from typeclasses.objects import Object
from world.rules import parse_accuracy, parse_damage


class Weapon(Object):
    def at_object_creation(self):
        self.db.modes = []  # Single | Burst | Auto | Stun | Thrown
        self.db.hands = 1  # 1 or 2 (or more for more odd species and the like)
        self.db.components = []  # list of the components that comprise this item
        self.db.skill = ""  # associated skill or stat used in the game system to track the use of this item.
        self.db.template = ""
        self.db.health = 0
        self.db.max_health = 0

    def accuracy(self):
        # Look at components and find all the accuracy related component values and add them together.
        return self.db.accuracy

    def damage(self):
        # Same as accuracy, but for damage
        return self.db.damage

    def damage_type(self):
        # returns the types of damage dealt by the weapon.  Optional.
        return self.db.damage_type

    def durability(self):
        # same as accuracy, but for durability
        return self.db.durability

    def mass(self):
        # same as above but for mass
        return self.db.mass

    def return_appearance(self, looker):
        message = []

        message.append("|w%s|n" % self.key)
        message.append("|wAccuracy:|n %s" % parse_accuracy(self.accuracy()))
        message.append("|wDamage:|n %s" % parse_damage(self.damage))
        message.append("|wDamage Type: |n %s" % self.damage_type())
        message.append("|wHealth:|n %s" % self.parse_health())
        message.append("|wMass:|n %s" % self.mass())
        message.append("|wRequired Skill:|n %s" % self.db.skill)

        message2 = []
        for line in message:
            message2.append(unicode(line))
        return "\n".join(message2)

    def parse_health(self):
        current = self.db.health
        max_health = self.db.db.max_health

        if max_health > 0:
            percent = int(current / max_health * 100)
        else:
            percent = 0

        if percent > 75:
            return '|230Good|n'
        elif percent > 50:
            return '|450Damaged|n'
        elif percent > 25:
            return '|550Seriously Damaged|n'
        elif percent > 10:
            return '|500Critically Damaged|n'
        elif percent > 0:
            return '|305Nearly Destroyed|n'
        else:
            return '|[300Destroyed|n'
