from typeclasses.objects import Object
from commands.library import header
from world.rules import parse_accuracy, parse_damage, parse_item_health
from evennia.utils import delay
from typeclasses.item_creation import Item


class Consumable(Item):
    def at_object_creation(self):
        self.db.addictive = False

    # Potency can have impact on the strength of the consumable for healing or other effects.
    # It also has the added benefit of, possibly, being used to measure the chance of addiction.
    def potency(self):
        # calculate potency from components
        return self.db.potency

    # Quality along with Potency measure the effectiveness of the consumable
    def quality(self):
        # calculate quality from components
        return self.db.quality

    # Optional property that defines different delivery methods of the consumable.
    # Delivery methods vary based on theme, but can include:
    #   Oral (taken by mouth)
    #   Inhalation (a powder or vapor breathed in through the lungs)
    #   Injection (requiring some form of injector)
    #   Suppository (taken rectally)
    #   Topical ( rubbed onto skin)
    #   Sublingual (placed under the tongue)
    def delivery(self):
        # calculate delivery method from components
        return self.db.delivery

    def duration(self):
        # How long the effects last in minutes.  Based on quality times potency times 100.
        # A duration of 0 has an immediate and non-lasting effect.
        if not self.db.duration:
            return self.potency() * self.quality() * 100
        else:
            return self.db.duration

    def effect(self):
        # what the consumable actually does.
        return self.db.effect

    def return_appearance(self, looker):
        message = []

        if looker.locks.check_lockstring(looker, "dummy:perm(Admin)"):
            message.append("|y%s|n (%s)" % (self.key, self.id))
        else:
            message.append("|y%s|n" % self.key)
        message.append(self.db.description)
        message.append(header())
        message.append("|wPotency:|n %s" % self.parse_potency(self.potency()))
        message.append("|wQuality:|n %s" % self.parse_potency(self.quality()))
        message.append("|wDelivery:|n %s" % self.delivery())
        message.append("|wDuration:|n %s" % self.duration())
        message.append(header())

        message2 = []
        for line in message:
            message2.append(unicode(line))
        return "\n".join(message2)

    def parse_potency(self, value):
        if value >= 1.5:
            return "Extremely High"
        elif value >= 1.2:
            return "Very High"
        elif value >= .9:
            return "High"
        elif value >= .7:
            return "Medium"
        elif value >= .5:
            return "Low"
        else:
            return "Very Low"

    def activate(self, target):
        target.health.set_heal_status('medkit')

