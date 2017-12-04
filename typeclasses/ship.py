from typeclasses.objects import Object
from world.rules import parse_accuracy, parse_damage, parse_item_health
from commands.library import header


class Ship(Object):
    def at_object_creation(self):
        self.db.min_crew = 0
        self.db.passengers = 0
        self.db.pilot = None
        self.db.hull = 0
        self.db.max_hull = 0
        self.db.shields = 0
        self.db.max_shields = 0
        self.db.weapons = {}
        self.db.cargo = 0
        self.db.max_cargo = 0
        self.db.gunners = []
        self.db.hangar = False
        self.db.hangar_capacity = 0
        self.db.size = 0
        self.db.ship_class = ""
        self.db.can_land = False
        self.db.speed = 0
        self.db.has_hyperdrive = False
        self.db.cost = 0
        self.db.board_room = None

    def at_object_receive(self, obj, source_location):
        obj.move_to(self.db.board_room)
