import evennia
from evennia import DefaultScript
from random import randint
from typeclasses.characters import Character
from world import rules

WEATHER = {
    "tatooine": [
        {"desc": "sunny and hot", "probability": 85, "survival": 0, "message": ""},
        {"desc": "windy", "probability": 95, "survival": 25,
         "message": "A cross wind picks up.  The wind causes debris to hit you.", "damage": 2},
        {"desc": "sandstorm", "probability": 100, "survival": 90,
         "message": "A sandstorm whips up.  The stinging sand tears at your skin.", "damage": 10}],
    "abregado-rae": [
        {"desc": "warm with a light breeze", "probability": 60, "survival": 0, "message": ""},
        {"desc": "light showers", "probability": 80, "survival": 0, "message": ""},
        {"desc": "thunderstorms", "probability": 90, "survival": 10, "message": "You are pelted with hail and debris.",
         "damage": 2},
        {"desc": "severe thunderstorms", "probability": 100, "survival": 40,
         "message": "Lightning strikes nearby and causes burns.", "damage": 10}]
}


class WeatherScript(DefaultScript):
    def at_script_creation(self):
        self.key = "weather"
        self.desc = "Script controlling weather changes"
        self.interval = 60 * 60 * 2
        self.repeats = -1

    def at_repeat(self):
        zonemasters = evennia.search_tag(category="zonemaster")
        for master in zonemasters:
            zone = master.tags.get(category="zonemaster")
            probability = randint(0, 100)
            planet = master.tags.get(category="planet")
            prev_weather = master.db.weather
            weather = next(item for item in WEATHER.get(planet) if item.get("probability") >= probability)

            if prev_weather == weather:
                continue

            master.db.weather = weather
            rooms = evennia.search_tag(zone, category="zone")
            for room in rooms:
                if room.tags.get("outside"):
                    room.msg_contents("The weather is changing.")
                    self.check_survival(room, weather)

    def check_survival(self, room, weather):
        if weather.get("survival") > 0:
            players = sorted([char for char in room.contents if char.is_typeclass(Character, exact=False)])
            for player in players:
                self.test_player_survival(player, room, weather)

    def test_player_survival(self, player, room, weather):
        roll = rules.roll_skill(player, "survival")
        if roll < weather.get("survival"):
            damage = weather.get("damage")
            player.health.damage(damage)
            player.msg(weather.get("message"))
            player.msg("You take %s points in damage." % damage)
