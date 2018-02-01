"""
Room

Rooms are simple containers that has no location of their own.

"""
import evennia
import datetime
from typeclasses.characters import Character
from typeclasses.objects import Object
from evennia import DefaultRoom
from commands.library import header, titlecase
from evennia.utils import evtable
from world.weather import WeatherScript


class Room(DefaultRoom):
    """
    Rooms are like any Object, except their location is None
    (which is default). They also use basetype_setup() to
    add locks so they cannot be puppeted or picked up.
    (to change that, use at_object_creation instead)

    See examples/object.py for a list of
    properties and methods available on all Objects.
    """
    def at_object_creation(self):
        self.ndb.room_messages = {}

    def return_appearance(self, looker):
        zonemaster = self.get_zonemaster()

        zone = self.tags.get(category="zone")
        planet = None
        if zonemaster:
            planet = zonemaster.tags.get(category="planet")
        message = []
        if zone and planet:
            message.append(header(' {} - {} - {} '.format(self.key, titlecase(zone), titlecase(planet))))
        else:
            message.append(header(' {} '.format(self.key)))
        message.append(self.db.desc)
        message.append(header())

        if zonemaster and zonemaster.db.weather:
            message.append("|020Weather:|n %s" % titlecase(zonemaster.db.weather.get("desc")))
            message.append(header())
        chars = self.list_characters()
        objects = self.list_non_characters()
        colored_objects = []
        for obj in objects:
            colored_objects.append("|135%s|n" % obj.key)
        exits = []
        if self.exits:
            for exit in self.exits:
                if exit.access(looker, "view"):
                    exits.append("|w<|n|b%s|n|w>|n - %s" % (exit.key, exit.destination))
        table = evtable.EvTable("|wCharacters and Objects:|n", "|wExits:|n", table=[chars + colored_objects, exits], border=None)
        table.reformat_column(0, width=39, align="l")
        message.append(table)
        message.append("\n")

        message2 = []
        for line in message:
            message2.append(unicode(line))
        return "\n".join(message2)

    def list_characters(self):
        return sorted([char for char in self.contents if char.is_typeclass(Character, exact=False)])

    def online_characters(self, viewer=None):
        characters = [char for char in self.list_characters() if char.sessions]
        if viewer:
            characters = [char for char in characters if viewer.can_see(char)]

    def list_non_characters(self):
        return list(Object.objects.filter_family(db_location=self))

    def get_zonemaster(self):
        if self.tags.get(category="zone"):
            if len(evennia.search_tag(self.tags.get(category="zone"), category="zonemaster")) > 0:
                return evennia.search_tag(self.tags.get(category="zone"), category="zonemaster")[0]
            else:
                return None
        else:
            return None

    def get_weather(self):
        zonemaster = self.get_zonemaster()
        if zonemaster:
            return zonemaster.db.weather
        else:
            return None

    def at_object_receive(self, obj, source_location):
        if obj.has_account:
            weather = self.get_weather()
            if weather:
                weather_script = evennia.ScriptDB.objects.filter(db_key="weather").first()
                weather_script.test_player_survival(obj, self, weather)

    def add_pose(self, sender, text):
        pose = {'name': sender, 'time': datetime.datetime.now(), 'pose': text}

        self.db.poses.append(pose)
