"""
Item Creation Sytem

    The item creation system contrib is intented to create a highly modular and customizable system for creating
    any type of item for a game or system.  This system consists of 3 major subsystems.

    1. Components and Component templates
    2. Items and Item Templates
    3. Workbench


    1. Components

    Components are the most fundamental piece of the Item Creation system.  Components are the 'parts' used to create
    items.

    For example: A sword is made up of a blade, a hilt and a pommel.  Each of these are components.  Thus each of these
    would have a separate entry in the item's template.

    Components consist of a few key properties.

        Cost:           Cost of all components are combined to calculate the total value of the created item.
        Categories:     This is a list of the categories the component falls under.  The type of slots it can fill on
                        the item.
        Mods:           A dictionary of the stat modifiers that the item applies.
        Size:           The size restriction of the item.  This allows for size groupings to that larger scale
                        components cannot be added to smaller items in an unrealistic way.


    2. Items and Item Templates

    Item templates are like the schematics that are used to build items.
"""

from typeclasses.objects import Object
from evennia import default_cmds, CmdSet
from evennia.utils.evmenu import EvMenu
from evennia.utils import evtable
from commands.library import titlecase, node_formatter, options_formatter, header, chunks


class Component(Object):
    """
    Fundamental element of the Item creation system.
    """
    def at_object_creation(self):
        self.db.cost = 0
        self.db.mass = 0
        self.db.categories = []  # The 'type' of the component
        self.db.mods = {}  # the configurable stat modifiers the item incurs.  Ex: Accuracy: 1, Damage: 5, Dexterity:
        # -10
        self.db.size = 0  # optional setting to help determine size requirement/restriction on certain components.
        # -1 applies to all sizes.
        self.db.template = ""


class Item(Object):
    """
    Item base class.  Contains functions important to building, maintaining and destroying items.
    """
    def at_object_creation(self):
        self.db.description = ""
        self.db.components = []
        self.db.template = ""

    def install_component(self, comp):
        pass

    def remove_component(self, comp):
        pass

    def list_components(self):
        return self.db.components

    def get_template(self):
        return self.db.template


COMPONENTS = {
    "durasteel": {"categories": ["material"], "mods": {"durability": 6, "accuracy": -1}, "cost": 30, "mass": 4},
    "plasteel": {"categories": ["material"], "mods": {"durability": 3}, "cost": 15, "mass": 2},
    "dynaplast": {"categories": ["material"], "mods": {"durability": 1}, "cost": 5, "mass": 1},
    "standard grip": {"categories": ["grip"], "mods": {"accuracy": 2}, "cost": 15, "mass": 2},
    "small energy cell": {"categories": ["energy cell"], "mods": {"damage": 4}, "cost": 15, "mass": 1,
                          "damage_type": "energy"},
    "pistol scope": {"categories": ["scope"], "mods": {"accuracy": 2}, "cost": 25, "mass": 1},
    "burst oscillator": {"categories": ["oscillator"], "mods": {"modes": "burst"}, "cost": 30, "mass": 10}
}

ITEM_TEMPLATES = {
    "light blaster pistol": {"required": {"material": 1, "grip": 1, "energy cell": 1}, "optional": {"oscillator": 1},
                             "optional_count": 1, "desc": "Small hold-out blaster."},
    "medium blaster rifle": {"required": {"material": 2, "grip": 2, "energy cell": 1},
                             "optional": {"scope": 1, "oscillator": 1},
                             "optional_count": 1, "desc": "long rifle that does more damage."}
}


class Workbench(Object):
    def at_object_creation(self):
        self.db.components = []
        self.db.templates = []
        self.cmdset.add("typeclasses.item_creation.WorkbenchCmdSet", permanent=True)
        self.db.desc = "This workbench allows you to modify and create items.  Type |w+workbench|n to begin."

    def return_appearance(self, looker):
        looker.msg(header(" Workbench "))
        looker.msg(self.db.desc)
        looker.msg(header())

        components = [titlecase(c) for c in self.db.components]
        templates = [titlecase(t) for t in self.db.templates]

        table = evtable.EvTable("|wAvailable Templates|n", "|wAvailable Components|n", table=[templates, components],
                                border=None)
        table.reformat_column(0, width=39, align="l")
        looker.msg(unicode(table))


class WorkbenchCmdSet(CmdSet):
    key = "WorkbenchCmdSet"

    def at_cmdset_creation(self):
        self.add(CmdWorkbench())
        self.add(CmdWorkbenchTemplates())


class CmdWorkbenchTemplates(default_cmds.MuxCommand):
    """
    Usage:
        +workbench/templates

    Displays a list of the templates available on the workbench.
    """

    key = "+templates"
    aliases = ["+temp"]
    help_category = "Items"

    def func(self):
        # templates = [t for t in self.obj.db.templates]
        self.caller.msg(self.obj.db.templates)


"""
Item Menu Workflow

User
    Build Item
        View Available Templates
        Choose Template
            Choose Component (one options for each component type in the template)
                Install component from inventory
                    Skill Check to determine success or failure
                Purchase Component
    Upgrade Item
        Choose Item
            Choose Component to Remove
                Skill check to determine success or failure
            Choose Component to Install
                Skill check to determine success or failure
    Repair Item
        Choose Item
            Skill check to determine success or failure
    Purchase Item?
    
Owner
    Add templates
    Add components
    Add inventory
"""


class CmdWorkbench(default_cmds.MuxCommand):
    """
    Usage:
        +workbench

    Initiates the workbench menu system to allow for creating and improving items.
    """

    key = "+workbench"
    aliases = ["+work"]
    help_category = "Items"

    def func(self):
        self.caller.ndb.current_workbench = self.obj
        EvMenu(self.caller, "typeclasses.item_creation",
               startnode="menu_start_node",
               node_formatter=node_formatter,
               options_formatter=options_formatter,
               cmd_on_exit=exit_message)


def menu_start_node(caller):
    text = "Welcome to the Workbench!  Here you will be able to create new or modify existing items.  Please choose " \
           "from an option below to begin."

    options = ({"desc": "Upgrade Item", "goto": "improve_item_start"},
               {"desc": "Build Item", "goto": "create_item_start"},
               {"desc": "Repair Item", "goto": "repair_item_start"})

    if caller.locks.check_lockstring(caller, "dummy:perm(Admin)"):
        options += ({"desc": "Add Templates", "goto": "admin_add_template"},
                    {"desc": "Add Component", "goto": "admin_add_component"})

    return text, options


def _wrapper(caller, attr, value):
    return lambda caller: setattr(caller.ndb._menutree, attr, value)


def repair_item_start(caller):
    pass


def admin_add_template(caller):
    pass


def admin_add_component(caller):
    pass


def create_item_start(caller):
    text = "Welcome to the Item Creation system.  Here you will begin crafting a new item from a series of templates." \
           "  Below are the template types available at this workbench."

    options = ()

    templates = caller.ndb.current_workbench.db.templates

    for temp in templates:
        node_dict = {"desc": titlecase(temp), "goto": "create_item_select_comp_type",
                     "exec": _wrapper(caller, "selected_template", temp)}
        options += (node_dict,)

    options += ({"desc": "Go Back", "key": "back", "goto": "menu_start_node"},)

    return text, options


def create_item_select_comp_type(caller):
    template = ITEM_TEMPLATES.get(caller.ndb._menutree.selected_template)
    caller.ndb._menutree.optional_count = template.get("optional_count")
    if not hasattr(caller.ndb._menutree, "required"):
        required = {}
        for item, value in template.get("required").items():
            component_list = []
            for i in range(value):
                component_list.append(None)
            required.update({item: component_list})
        caller.ndb._menutree.required = required

    if "optional" in template:
        if not hasattr(caller.ndb._menutree, "optional"):
            optional = {}
            for item, value in template.get("optional").items():
                component_list = []
                for i in range(value):
                    component_list.append(None)
                optional.update({item: component_list})
            caller.ndb._menutree.optional = optional

    text = "You have selected the |w%s|n template.  From here, you must choose the components to add to the template " \
           "to complete the item creation." % caller.ndb._menutree.selected_template

    text += "\n\n|wCurrent |rRequired|w item slots:|n\n"

    for item, slots in caller.ndb._menutree.required.items():
        text += "%s: %s\n" % (titlecase(item), str(slots))

    if "optional" in template:
        text += "\n\n|wCurrent Optional item slots:|n\n"
        for item, slots in caller.ndb._menutree.optional.items():
            text += "%s: %s\n" % (titlecase(item), str(slots))

        text += "Available optional slots: %s" % template.get("optional_count")

    text += "\n\nPlease select the slot you wish to fill.  All required slots must be filled before you will be " \
            "allowed to proceed to the creation process.  Optional component slots may be left blank.  Select " \
            "|wCancel|n to deselect your template and start over."

    options = ()

    for item, slots in caller.ndb._menutree.required.items():
        node_dict = {"desc": titlecase(item), "goto": "select_comp_slot",
                     "exec": _wrapper(caller, "selected_slot", item)}
        options += (node_dict,)

    if "optional" in template:
        for item, slots in caller.ndb._menutree.optional.items():
            node_dict = {"desc": titlecase(item), "goto": "select_comp_slot",
                         "exec": _wrapper(caller, "selected_slot", item)}
            options += (node_dict,)

    options += ({"desc": "Cancel", "key": "cancel", "goto": "create_item_start", "exec": cancel_item_create},)

    return text, options


def cancel_item_create(caller):
    del caller.ndb._menutree.required
    del caller.ndb._menutree.optional


def select_comp_slot(caller):
    slot = caller.ndb._menutree.selected_slot
    text = "Please select the component listed below from those available at this location.  Or choose to install " \
           "your own."

    options = ()

    for comp in _get_components(caller, type=slot):
        node_dict = {"desc": titlecase(comp), "goto": "confirm_install_comp",
                     "exec": _wrapper(caller, "selected_comp", comp)}
        options += (node_dict,)

    options += ({"desc": "Install from Inventory", "goto": "install_from_inventory"},
                {"desc": "Go Back", "goto": "create_item_select_comp_type"})

    return text, options


def confirm_install_comp(caller):
    slot = caller.ndb._menutree.selected_slot
    comp = caller.ndb._menutree.selected_comp

    text = "Are you sure you want to install %s into the %s slot?" % (comp, slot)

    options = ({"desc": "Yes", "goto": "create_item_select_comp_type", "exec": install_comp},
               {"desc": "No", "goto": "create_item_select_comp_type"})

    return text, options


def install_comp(caller):
    slot = caller.ndb._menutree.selected_slot
    comp = caller.ndb._menutree.selected_comp
    comp_slot = caller.ndb._menutree.required.get(slot)
    opt_slot = caller.ndb._menutree.optional.get(slot)
    if comp_slot:
        if isinstance(comp_slot, list):
            try:
                position = comp_slot.index(None)
                if position <= len(comp_slot):
                    comp_slot[position] = comp
                else:
                    raise ValueError
                caller.ndb._menutree.required[slot] = comp_slot
            except ValueError:
                caller.msg("|rWarning:|n No empty slots available.  Please remove an item before installing a new one.")
    if opt_slot:
        # Make sure opt_slot is a list
        if isinstance(opt_slot, list):
            try:
                # Find the position of the next empty slot
                position = opt_slot.index(None)

                if position <= len(opt_slot):
                    optional_item_list = []
                    for item, value in caller.ndb._menutree.optional.items():
                        for thing in value:
                            if thing is not None:
                                optional_item_list.append(item)

                    if len(optional_item_list) < caller.ndb._menutree.optional_count:
                        opt_slot[position] = comp
                        caller.ndb._menutree.optional[slot] = opt_slot
                    else:
                        raise ValueError(
                            "|rWarning:|n Optional component slots are full.  If you wish to install this component, "
                            "you will need to remove another.")
                else:
                    raise ValueError(
                        "|rWarning:|n No empty slots available.  Please remove an item before installing a new one.")

            except ValueError as vEx:
                caller.msg(vEx)


def install_from_inventory(caller):
    pass


def improve_item_start(caller):
    text = "The first step toward improving an item is, of course, selecting the item you want to improve!  Below " \
           "is a list of the items in your inventory.  Please select the item you wish to modify."

    options = ()

    for item in caller.contents:
        node_dict = {"desc": titlecase(item.key), "goto": "improve_item_select_comp",
                     "exec": _wrapper(caller, "selected_item", item)}
        options += (node_dict,)

    options = ({"desc": "Go Back", "key": "back", "goto": "menu_start_node"})
    return text, options


def exit_message(caller, menu):
    caller.msg("Exiting Workbench.  Goodbye.")


def _get_components(caller, **kwargs):
    comp_type = ""
    contents = False
    if "caller_contents" in kwargs:
        contents = kwargs["caller_contents"]

    if "type" in kwargs:
        comp_type = kwargs['type']

    components = {}
    if contents:
        for comp in caller.contents:
            components.update({comp: COMPONENTS.get(comp)})
    else:
        for comp in caller.ndb.current_workbench.db.components:
            components.update({comp: COMPONENTS.get(comp)})

    if comp_type:
        return {key: props for key, props in components.items() if comp_type in props["categories"]}
    else:
        return components
