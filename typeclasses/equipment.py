from typeclasses.objects import Object
from commands.library import header
from world.rules import parse_accuracy, parse_damage, parse_item_health
from typeclasses.item_creation import Item


class Equipment(Item):
    def at_object_creation(self):
        self.db.description = ""
        self.db.components = []
        self.db.template = ""
        self.db.required_skill = ""

    def function(self):
        # calculate function from components.  Including associated skills to modify
        # Return a dictionary of type: {"skill1": "mod", "skill2": "mod", etc...}
        return self.db.function

    def durability(self):
        # Calculate durability from components
        return self.db.durability

    def mass(self):
        # calculate mass from components
        return self.db.mass

    def return_appearance(self, looker):
        message = ["|y%s|n" % self.key, self.db.description, header(),
                   "|wRequired Skill:|n %s" % self.db.required_skill, "|wFunction:|n %s" % parse_damage(self.function),
                   "|wDurability:|n %s" % parse_damage(self.durability), "|wMass:|n %s" % self.mass(), header()]

        message2 = []
        for line in message:
            message2.append(unicode(line))
        return "\n".join(message2)
