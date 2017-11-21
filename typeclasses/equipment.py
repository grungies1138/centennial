from typeclasses.objects import Object
from commands.library import header
from world.rules import parse_accuracy, parse_damage, parse_item_health


class Equipment(Object):
    def at_object_creation(self):
        self.db.description = ""
        self.db.components = []
        self.db.template = ""
        self.db.required_skill = ""

    def function(self):
        # calculate function from components.  Including associated skills to modify
        return self.db.function

    def durability(self):
        # Calculate durability from components
        return self.db.durability

    def mass(self):
        # calculate mass from components
        return self.db.mass

    def return_appearance(self, looker):
        message = []

        message.append("|y%s|n" % self.key)
        message.append(self.db.description)
        message.append(header())
        message.append("|wRequired Skill:|n %s" % self.db.required_skill)
        message.append("|wFunction:|n %s" % parse_damage(self.function))
        message.append("|wDurability:|n %s" % parse_damage(self.durability))
        message.append("|wMass:|n %s" % self.mass())
        message.append(header())

        message2 = []
        for line in message:
            message2.append(unicode(line))
        return "\n".join(message2)
