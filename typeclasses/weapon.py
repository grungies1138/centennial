from typeclasses.objects import Object
from world.rules import parse_accuracy, parse_damage, parse_item_health
from commands.library import header
from typeclasses.item_creation import Item


class Weapon(Item):
    def at_object_creation(self):
        self.db.modes = []  # Single | Burst | Auto | Stun | Thrown
        self.db.hands = 1  # 1 or 2 (or more for more odd species and the like)
        self.db.skill = ""  # associated skill or stat used in the game system to track the use of this item.
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
        message = ["|y%s|n" % self.key, self.db.description, header(),
                   "|wAccuracy:|n %s" % parse_accuracy(self.accuracy()),
                   "|wDamage:|n %s" % parse_damage(self.db.damage), "|wDamage Type: |n %s" % self.damage_type(),
                   "|wHealth:|n %s" % parse_item_health(self), "|wMass:|n %s" % self.mass(),
                   "|wRequired Skill:|n %s" % self.db.skill, header()]

        message2 = []
        for line in message:
            message2.append(unicode(line))
        return "\n".join(message2)

    def at_drop(self, dropper):
        if dropper.db.wielding == self:
            dropper.db.wielding = None
            dropper.msg("%s removed from being wielded." % self.key)
