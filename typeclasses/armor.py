from typeclasses.objects import Object
from world.rules import parse_accuracy, parse_damage, parse_item_health
from commands.library import header


class Armor(Object):
    def at_object_creation(self):
        self.db.destroyed = False
        self.db.components = []
        self.db.template = ""
        self.db.health = 0
        self.db.max_health = 0
        self.db.description = ""

    def durability(self):
        # calculate durability based on components
        return self.db.durability

    def protection_types(self):
        # What types of damage does this armor protect against.
        return self.db.protection_types

    def mass(self):
        # calculate mass
        return self.db.mass

    def return_appearance(self, looker):
        message = []

        message.append("|y%s|n" % self.key)
        message.append(self.db.description)
        message.append(header())
        message.append("|wHealth:|n %s" % parse_item_health(self))
        message.append("|wDurability:|n %s" % parse_damage(self.db.durability))
        types = "%s" % ', '.join(t for t in self.protection_types())
        message.append("|wProtection Types:|n %s" % types)
        message.append("|wMass:|n %s" % self.db.mass)
        message.append(header())
        message2 = []
        for line in message:
            message2.append(unicode(line))
        return "\n".join(message2)

    def at_drop(self, dropper):
        if dropper.db.wearing == self:
            dropper.msg("%s removed from being worn.")
            dropper.db.wearing = None
