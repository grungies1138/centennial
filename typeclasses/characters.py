"""
Characters

Characters are (by default) Objects setup to be puppeted by Accounts.
They are what you "see" in game. The Character class in this module
is setup to be the "default" character type created by the default
creation commands.

"""
from evennia import DefaultCharacter
from commands.library import header
from evennia.utils.utils import lazy_property


class Character(DefaultCharacter):
    """
    The Character defaults to reimplementing some of base Object's hook methods with the
    following functionality:

    at_basetype_setup - always assigns the DefaultCmdSet to this object type
                    (important!)sets locks so character cannot be picked up
                    and its commands only be called by itself, not anyone else.
                    (to change things, use at_object_creation() instead).
    at_after_move(source_location) - Launches the "look" command after every move.
    at_post_unpuppet(account) -  when Account disconnects from the Character, we
                    store the current location in the pre_logout_location Attribute and
                    move it to a None-location so the "unpuppeted" character
                    object does not need to stay on grid. Echoes "Account has disconnected"
                    to the room.
    at_pre_puppet - Just before Account re-connects, retrieves the character's
                    pre_logout_location Attribute and move it back on the grid.
    at_post_puppet - Echoes "AccountName has entered the game" to the room.

    """

    def at_object_creation(self):
        self.db.xp = 0
        self.db.level = 0
        self.db.read_posts = []
        self.db.talents = []
        self.scripts.delete(key='endurance')
        self.scripts.delete(key='health')
        self.scripts.delete(key='force')
        self.scripts.delete(key='skills')
        self.scripts.add('typeclasses.endurance_handler.EnduranceHandler', key='endurance')
        self.scripts.add('typeclasses.health_handler.HealthHandler', key='health')
        self.scripts.add('typeclasses.skill_handler.SkillHandler', key='skills')
        self.endurance.set_character(self)
        self.endurance.set_max(40)
        self.health.set_character(self)
        self.health.set_max_health(40)
        self.skills.set_character(self)

    def at_post_puppet(self):
        self.location.msg_contents("%s has connected" % self.key)
        self.execute_cmd("look")
        self.execute_cmd("@mail")

    @lazy_property
    def endurance(self):
        return [s for s in self.scripts.get(key='endurance') if s.is_valid()][0]

    @lazy_property
    def force(self):
        return [s for s in self.scripts.get(key='force') if s.is_valid()][0]

    @lazy_property
    def health(self):
        return [s for s in self.scripts.get(key='health') if s.is_valid()][0]

    @lazy_property
    def skills(self):
        return [s for s in self.scripts.get(key='skills') if s.is_valid()][0]

    def get_attributes(self):
        return self.db.attributes

    def return_appearance(self, looker):
        if not looker:
            return
        visible = (con for con in self.contents if con != looker and con.access(looker, "view"))

        message = [header(self.key), self.db.desc, header(), "Carrying:"]
        for con in visible:
            if self.db.wearing == con:
                message.append(f"{con.key} |230[Wearing]|n")
            elif self.db.wielding == con:
                message.append(f"{con.key} |230[Wielding]|n")
            else:
                message.append(con.key)
        return "\n".join(message)

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('character:sheet', kwargs={'object_id': self.id})
