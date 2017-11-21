from typeclasses.objects import Object


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
