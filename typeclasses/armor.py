from typeclasses.objects import Object
from world.rules import parse_accuracy, parse_damage, parse_item_health
from commands.library import header
from typeclasses.item_creation import Item


class Armor(Item):
    def at_object_creation(self):
        self.db.destroyed = False
        self.db.health = 0
        self.db.max_health = 0

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
        message = [f"|y{self.key}|n",
                   self.db.description,
                   header(),
                   f"|wHealth:|n {parse_item_health(self)}",
                   f"|wDurability:|n {parse_damage(self.db.durability)}",
                   f"|wProtection Types:|n {', '.join(t for t in self.protection_types())}",
                   f"|wMass:|n {self.db.mass}",
                   header()
                   ]
        return "\n".join([str(m) for m in message])

    def at_drop(self, dropper):
        if dropper.db.wearing == self:
            dropper.msg("%s removed from being worn." % self.key)
            dropper.db.wearing = None

    def apply_damage(self, value):
        if value >= self.db.health:
            self.db.health = 0
            self.db.destroyed = True
        else:
            self.db.health -= value

    def repair(self, value):
        if (self.db.health + value) >= self.db.max_health:
            self.db.health = self.db.max_health
        else:
            self.db.health = self.db.health + value
