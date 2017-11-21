from typeclasses.objects import Object
from world.rules import parse_accuracy, parse_damage, parse_item_health


class Armor(Object):
    def at_object_creation(self):
        self.db.destroyed = False
        self.db.components = []
        self.db.template = ""
        self.db.health = 0
        self.db.max_health = 0

    def durability(self):
        # calculate durability based on components
        return self.db.durability

    def protection_types(self):
        # What types of damage does this armor protect against.
        return self.db.protections_types

    def mass(self):
        # calculate mass
        return self.db.mass

    def return_appearance(self, looker):
        message = []

        message.append("|y%s|n" % self.key)
        message.append("|wHealth:|n %s" % parse_item_health(self.db.health))
        message.append("|wDurability:|n %s" % parse_damage(self.db.durability))
        types = [type for type in self.protection_types()]
        message.append("|wProtection Types:|n %s" % types)
        message.append("|wMass:|n %s" % self.db.mass)

        message2 = []
        for line in message:
            message2.append(unicode(line))
        return "\n".join(message2)
