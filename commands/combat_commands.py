from evennia import default_cmds
from evennia.utils.evmenu import EvMenu
from commands.library import titlecase, notify, node_formatter, options_formatter
from typeclasses.characters import Character
from world.rules import roll_skill


# DAMAGE = Weapon Damage - (Weapon Damage * % END)

class AttackCommand(default_cmds.MuxCommand):
    """
    Command used to initiate combat with another character, NPC, or Army

    Usage:
        +attack
    """

    key = "+attack"
    aliases = ["attack"]
    lock = "cmd:all()"
    help_category = "General"

    def func(self):
        if self.args:
            target = self.caller.search(self.args)
            if not target:
                self.caller.msg("That is not a valid combat target.")
                return
            if self.caller.db.wielding:
                challenge = roll_skill(self.caller, self.caller.db.wielding.db.skill)
            else:
                challenge = roll_skill(self.caller, 'athletics')
            defense = roll_skill(target, "dodge")
            
            if challenge > defense:
                if self.caller.db.wielding:
                    calculated_damage = self.caller.db.wielding.damage()
                else:
                    calculated_damage = roll_skill(self.caller, self.caller.skills.get("melee")) / 40
                if target.db.wearing and not target.db.wearing.db.destroyed:
                    calculated_damage = calculated_damage - target.db.wearing.durability()
                    target.db.wearing.apply_damage(self.parse_hit(challenge, defense, calculated_damage))
                    self.caller.location.msg_contents("%s has attacked %s and hit their armor." %
                                                      (self.caller.key, target.key))
                else:
                    target.health.damage(self.parse_hit(challenge, defense, calculated_damage))
                    self.caller.location.msg_contents("%s has attacked %s and hit for damage." % (self.caller.key,
                                                                                                  target.key))
            else:
                self.caller.location.msg_contents("%s has attacked %s and missed." % (self.caller.key, target.key))
        else:
            self.caller.msg("You must select a valid target.")
            # EvMenu(self.caller, "commands.combat_commands",
            #        startnode="menu_start_node",
            #        node_formatter=node_formatter,
            #        options_formatter=options_formatter,
            #        cmd_on_exit=exit_message)

    def parse_hit(self, challenge, defense, damage):
        difference = challenge - defense

        if difference >= 40:
            return damage * 2
        elif difference >= 30:
            return damage * 1.5
        elif difference >= 20:
            return damage
        elif difference >= 10:
            return damage * .75
        else:
            return damage * .5


def menu_start_node(caller):
    text = "Please select your target."
    options = ()

    chars = _online_characters(viewer=caller)

    for char in chars:
        node_dict = {"desc": char.name, "goto": "select_action", "exec": _wrapper(caller, "temp_target", char)}
        options += (node_dict,)

    if len(chars) > 0:
        node_dict = {"desc": "Several", "goto": "select_targets", "exec": _wrapper(caller, "targets", "")}
        options += (node_dict,)

        node_dict = {"desc": "All", "goto": "select_action", "exec": _wrapper(caller, "temp_target", "all")}
        options += (node_dict,)
    else:
        text += "\n\nNo targets are available.  Please exit the attack menu by pressing 'q'."

    return text, options


def select_targets(caller):
    if caller.ndb._menutree.targets:
        targets = caller.ndb._menutree.targets
    else:
        targets = []

    text = "Please select a target.\n\nCurrent Targets:"

    for target in targets:
        text += "|-" + target + "\n"

    options = ({"desc": "Add Target", "goto": "add_target"})

    if len(targets) > 0:
        options += ({"desc": "Remove Target", "goto": "remove_target"},)

    options += ({"desc": "Done", "goto": "select_action"},)

    return text, options


def select_action(caller):
    pass


def _wrapper(caller, attr, value):
    return lambda caller: setattr(caller.ndb._menutree, attr, value)


def _list_characters(caller):
    return sorted([char for char in caller.location.contents if char.is_typeclass(Character, exact=False)])


def _online_characters(viewer=None):
    characters = [char for char in _list_characters(viewer) if char.sessions]
    if viewer:
        characters = [char for char in characters if char != viewer]

    return characters


def exit_message(caller, menu):
    caller.msg("Exiting +attack")
