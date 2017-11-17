from evennia import default_cmds
from evennia.utils.evmenu import EvMenu
from commands.library import titlecase, notify, node_formatter, options_formatter, exit_message
from typeclasses.characters import Character


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
        EvMenu(self.caller, "commands.combat_commands",
               startnode="menu_start_node",
               node_formatter=node_formatter,
               options_formatter=options_formatter,
               cmd_on_exit=exit_message)


def menu_start_node(caller):
    text = "Please select your target."
    options = ()

    for char in _online_characters(viewer=caller):
        node_dict = {"desc": char.name, "goto": "select_action", "exec": _wrapper(caller, "temp_target", char)}
        options += (node_dict,)

    node_dict = {"desc": "Several", "goto": "select_targets", "exec": _wrapper(caller, "targets", "")}
    options += (node_dict,)

    node_dict = {"desc": "All", "goto": "select_action", "exec": _wrapper(caller, "temp_target", "all")}
    options += (node_dict,)

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
