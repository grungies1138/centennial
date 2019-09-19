import operator
from evennia import default_cmds
from evennia.utils.evmenu import EvMenu
from world import classes, species
from commands.library import titlecase, node_formatter, options_formatter
from world.destinies import DESTINIES
from world.talents import TALENTS, FORCE_TALENTS
from evennia.contrib import rplanguage


class ChargenMenuCommand(default_cmds.MuxCommand):
    """
    Starts the Character Generation process.

    Usage:
        +chargen

    """

    key = "+chargen"
    aliases = []
    locks = "cmd:perm(Player)"
    help_category = "Chargen"

    def func(self):
        EvMenu(self.caller, "commands.chargen_menu",
               startnode="menu_start_node",
               cmdset_mergetype="Replace",
               node_formatter=node_formatter,
               auto_help=False,
               options_formatter=options_formatter,
               cmd_on_exit=exit_message)


def menu_start_node(caller):
    caller.cmdset.add("commands.default_cmdsets.ChargenCmdSet")
    if caller.db.chargencomplete == 1:
        text = "Initial Character Generation has been completed.  Please choose from one of the following options."
        options = ()
        if (caller.db.xp >= 100) or (caller.db.xp >= 90 and caller.db.destiny == "experience"):
            options += ({"desc": "Select Classes to level up in.", "goto": "askLevelSelect"},)

        if caller.db.destiny_pool > 0 and (
                    caller.db.level % 5 == 0 or (caller.db.destiny == "talented" and caller.db.level % 2 == 0)):
            options += ({"desc": "Talents", "goto": "askTalentSelect"},)

        return text, options

    text = \
        """
        Welcome to Character Generation!
        Please select an item that you wish to modify/set.

        You can 'quit' or just 'q' to quit this menu at any time.
        """

    options = ({"desc": "Set Personals",
                "goto": "ask_personal"},)

    if (caller.db.xp >= 100) or (caller.db.xp >= 90 and caller.db.destiny == "experience"):
        options += ({"desc": "Select Classes to level up in.", "goto": "askLevelSelect"},)

    if caller.db.level > 0 and ((len(caller.db.talents) < 1) or
                                (caller.db.destiny == "talented" and (len(caller.db.talents) < 3))):
        options += ({"desc": "Talents", "goto": "askTalentSelect"},)

    if caller.db.destiny_pool > 0:
        options += ({"desc": "Languages", "goto": "askLanguageSelect"},)

    options += ({"desc": "Reset Chargen", "goto": "confirm_chargen"},)

    options += ({"desc": "Finalize", "goto": "confirm_finalize"},)

    return text, options


def askLanguageSelect(caller):
    all_languages = rplanguage.available_languages()
    character_languages = caller.db.languages
    available = []

    if character_languages:
        for lang in all_languages:
            if lang not in character_languages:
                available.append(lang)
    else:
        available = all_languages

    current_text = ""
    if character_languages:
        for lang in character_languages:
            current_text += "|y%s|n, " % titlecase(lang)

    available_text = ""
    for lang in available:
        available_text += titlecase(lang).strip() + ", "

    text = """
    Languages are the way that various species communicate throughout the Galaxy.  
    You can choose as many languages as you have Destiny Pool Points(DPP).  You 
    are granted one language per DPP spent.  Those with the Translator destiny 
    are granted two languages per point.  (NOTE: for those with the Translator 
    destiny, each language costs .5 Destiny points.  Any fractional points left
    at chargen completion will be lost.)
    
    You currently have %s Destiny Pool points.
    
    Currently selected languages:
    %s
    
    Available languages:
    %s
    
    Please enter the language you would like to purchase.
    """ % (caller.db.destiny_pool, current_text, available_text)

    options = ({"key": "_default",
                "exec": purchase_language,
                "goto": "askLanguageSelect"},)
    if character_languages is not None and len(character_languages) > 0:
        options += ({"desc": "Unlearn Language",
                     "key": "unlearn",
                     "goto": "ask_unlearn_language"},)

    options += ({"desc": "Go Back",
                "key": "back",
                 "goto": "menu_start_node"},)

    return text, options


def ask_unlearn_language(caller):
    char_langs = caller.db.languages
    char_langs_text = ""

    if char_langs:
        for ind, lang in enumerate(char_langs):
            if ind < len(char_langs) - 1:
                char_langs_text += "%s, " % titlecase(lang)
            else:
                char_langs_text += "%s" % titlecase(lang)

    text = "Please select the language you wish to unlearn.\n\nCurrently learned languages:\n%s" % char_langs_text

    options = ({"key": "_default",
                "exec": unlearn_language,
                "goto": "ask_unlearn_language"},
               {"desc": "Go Back",
                "key": "back",
                "goto": "askLanguageSelect"})

    return text, options


def unlearn_language(caller, caller_input):
    selected_language = caller_input.strip().lower()
    if selected_language in caller.db.languages:
        caller.db.languages.remove(selected_language)
    else:
        caller.msg("That is not one of your learned languages.")


def purchase_language(caller, caller_input):
    selected_language = caller_input.lower().strip()
    all_languages = rplanguage.available_languages()
    character_languages = caller.db.languages

    if character_languages and selected_language in character_languages:
        caller.msg("You already have that language:  Please choose another.")
        return

    if selected_language not in all_languages:
        caller.msg("That is not a valid language")
        return

    if caller.db.destiny_pool == 0:
        caller.msg("You do not have enough Destiny Points to purchase that language.")
        return

    if hasattr(caller.db.languages, 'append'):
        caller.db.languages.append(selected_language)
    else:
        caller.db.languages = []
        caller.db.languages.append(selected_language)

    if caller.db.destiny == 'translator':
        caller.db.destiny_pool -= .5
        caller.db.max_dp -= .5
    else:
        caller.db.destiny_pool -= 1
        caller.db.max_dp -= 1

    caller.msg("You have selected %s" % titlecase(selected_language))


def askTalentSelect(caller):
    current_talents = ""
    for talent in caller.db.talents:
        current_talents += "|y%s|n\n" % titlecase(talent)

    if (len(caller.db.talents) < 1) or (caller.db.destiny == "talented" and (len(caller.db.talents) < 3)):
        caller.msg(
            "You have chosen all the talents allows at this point.  After you are IC you will be able to level up and "
            "select more.  Thank you.")
        caller.execute_cmd("back")

    text = \
        """
        Below you will see a list of talents that you are qualified to take.  PLEASE CHOOSE CAREFULLY.  
        |whelp Talents|n for more detail.\n\nCurrent Talents:\n%s\n\n You currently have |w%s|n Destiny Points to spend.
        \n\n
        """ % (current_talents, caller.db.destiny_pool)

    text += "Available Talents:\n"
    for talent in _parse_talents(caller):
        text += titlecase(talent).strip() + ", "

    text += "\n\nPlease type the name of the talent you wish to purchase or type |wback|n to return to the previous " \
            "menu."

    options = ({"key": "_default",
                "exec": purchase_talent,
                "goto": "askTalentSelect"},
               {"desc": "Go Back",
                "key": "back",
                "goto": "menu_start_node"},)

    return text, options


def purchase_talent(caller, caller_input):
    selected_talent = caller_input.lower().strip()
    all_talents = dict(TALENTS.items() + FORCE_TALENTS.items())

    if selected_talent not in all_talents:
        caller.msg("That is not a valid talent.  Please try again.")
        return

    if selected_talent in caller.db.talents:
        caller.msg("You have already selected that talent.  Please try again.")
        return
    if caller.db.destiny_pool == 0:
        caller.msg("You do not have any more Destiny Points.")
        return

    talent = all_talents.get(selected_talent)

    if "boost" in talent:
        for skill, value in talent.get("boost").items():
            caller.skills.improve(skill, value)
    if "command" in talent:
        caller.cmdset.add(talent.get("command"))
    caller.db.talents.append(str(selected_talent))
    if (len(caller.db.talents) >= 1) or (len(caller.db.talents) >= 3 and caller.db.destiny == "talented"):
        caller.db.destiny_pool -= 1
        caller.db.max_dp -= 1

    caller.msg("You have selected %s." % titlecase(selected_talent))


def _parse_talents(caller):
    talents = dict(TALENTS)
    if caller.db.destiny == "force":
        talents.update(FORCE_TALENTS)

    available_talents = []
    for key, value in talents.items():
        if key in caller.db.talents:
            continue
        available = False
        requirements = value.get("requirements")
        _skills = {}
        _talents = {}
        if "skills" in requirements:
            _skills = requirements.get("skills")
            for skill, val in _skills.items():
                char_skill = caller.skills.get(skill)

                if char_skill:
                    if char_skill >= value:
                        available = True
        if "talent" in requirements:
            _talents = requirements.get("talent")
            if _talents in caller.db.talents:
                available = True

        if available:
            available_talents.append(key)

    return sorted(available_talents)


def confirm_finalize(caller):
    text = "Are you |rsure|n you wish to finalize Character Generation? This cannot be undone.  " \
           "Only proceed if you are absolutely sure you wish to close Chargen."

    options = ({"key": ("Y", "Yes", "y", "yes"),
                "desc": "Yes",
                "exec": finalize_chargen,
                "goto": "quit_node"},
               {"key": ("N", "No", "n", "no"),
                "desc": "No",
                "goto": "menu_start_node"})

    return text, options


def finalize_chargen(caller):
    athletics_modifier = caller.skills.get("athletics") / 4

    if caller.db.destiny == "durable":
        basehp = 60
    else:
        basehp = 40
    maxhealth = basehp + athletics_modifier
    caller.health.set_max_health(maxhealth)
    caller.health.heal(maxhealth)

    caller.db.chargencomplete = 1

    caller.msg("Health calculated and set.  Starting credits distributed.  You may now proceed to the IC world.")


def ask_personal(caller):
    text = "Please select the items you wish set.  Darkened items have already been completed.  You may, of course, " \
           "select them again to change values."

    options = ()

    if caller.db.fullname:
        options += ({"desc": "|xSet Fullname|n",
                     "goto": "askFullname"},)
    else:
        options += ({"desc": "Set Fullname",
                     "goto": "askFullname"},)

    if caller.db.age:
        options += ({"desc": "|xSet Age|n",
                     "goto": "askAge"},)
    else:
        options += ({"desc": "Set Age",
                     "goto": "askAge"},)

    if caller.db.species:
        options += ({"desc": "|xSet Species|n",
                     "goto": "askSpecies"},)
    else:
        options += ({"desc": "Set Species",
                     "goto": "askSpecies"},)

    if caller.db.destiny:
        options += ({"desc": "|xSet Destiny|n",
                     "goto": "askDestiny"},)
    else:
        options += ({"desc": "Set Destiny",
                     "goto": "askDestiny"},)

    if caller.db.affiliation:
        options += ({"desc": "|xSet Starting Affiliation|n",
                     "goto": "askOrg"},)
    else:
        options += ({"desc": "Set Starting Affiliation",
                     "goto": "askOrg"},)

    options += ({"desc": "Return to Previous",
                 "goto": "menu_start_node"},)

    return text, options


def confirm_chargen(caller):
    text = "Are you sure you want to reset chargen? |wYes|n or |wNo|n\n\n|y*** Warning ***|n This will remove all " \
           "progress in chargen and reset you back to nothing, just as you started."

    options = ({"key": ("Y", "Yes", "y", "yes"),
                "desc": "Yes",
                "exec": reset_chargen,
                "goto": "menu_start_node"},
               {"key": ("N", "No", "n", "no"),
                "desc": "No",
                "goto": "menu_start_node"})

    return text, options


def reset_chargen(caller):
    caller.db.xp = 0
    caller.db.level = 0
    del caller.db.age
    del caller.db.credits
    del caller.db.affiliation
    del caller.db.species
    del caller.db.fullname
    del caller.db.destiny
    del caller.db.destiny_pool
    del caller.db.max_dp
    caller.db.talents = []
    caller.skills.clear_skills()
    caller.db.languages = []
    del caller.db.spoken_lang

    caller.msg("All levels have been removed and attributes have been reset.  Please begin again.")


def askSpecies(caller):
    text = "Please select the species you would like your character to be. type |whelp list species|n to see the " \
           "list of available species.  |whelp <species>|n to read about a specific selection."

    options = ({"key": "_default",
                "exec": setSpecies,
                "goto": "menu_start_node"})

    return text, options


def setSpecies(caller, raw_string):
    if caller.db.level > 0:
        caller.msg("You may not change your species after you select levels.  Please use the reset option if you wish "
                   "to start over.")
        return

    selected_species = raw_string.strip().lower()

    caller.msg("Selected Species: %s" % titlecase(selected_species))
    if selected_species in list(species.SPECIES.keys()):
        caller.db.species = selected_species
        species_langs = species.SPECIES.get(selected_species).get('languages')
        if hasattr(species_langs, "append"):
            caller.db.languages = species_langs
            caller.db.spoken_lang = species_langs[0]

    else:
        caller.msg("|rError:|n That is not a valid species.")


def askOrg(caller):
    text = "Please select the starting Affiliation for your character."
    options = ({"desc": "Hutt",
                "exec": lambda caller: setattr(caller.db, "affiliation", "Hutt"),
                "goto": "menu_start_node"},
               {"desc": "Imperial",
                "exec": lambda caller: setattr(caller.db, "affiliation", "Imperial"),
                "goto": "menu_start_node"},
               {"desc": "Independent",
                "exec": lambda caller: setattr(caller.db, "affiliation", "Independent"),
                "goto": "menu_start_node"},
               {"desc": "Jedi",
                "exec": lambda caller: setattr(caller.db, "affiliation", "Jedi"),
                "goto": "menu_start_node"},
               {"desc": "New Republic",
                "exec": lambda caller: setattr(caller.db, "affiliation", "NR"),
                "goto": "menu_start_node"})

    return text, options


def askDestiny(caller):
    text = "Please enter the destiny ability you would like to choose for your character.\n Here are the accepted " \
           "selections.  Please choose carefully.  Each has its own advantages and disadvantages.\n\n"

    for destiny in DESTINIES:
        text += "|w" + titlecase(destiny) + "|n - " + DESTINIES.get(destiny).get("description") + "\n\n"

    options = ({"key": "_default",
                "exec": setDestiny,
                "goto": "menu_start_node"})

    return text, options


def setDestiny(caller, raw_string):
    if caller.db.level > 0:
        caller.msg("|rYou cannot change your Destiny attribute after you have selected levels.|n")
        return

    destiny = raw_string.strip().lower()

    if destiny not in DESTINIES:
        caller.msg("|rThat was not a valid destiny.  Please try again.|n")
    else:
        force_scripts = caller.scripts.get("force")
        if force_scripts:
            for script in force_scripts:
                caller.scripts.delete(script)

        caller.db.destiny = destiny

        if destiny == "experience":
            caller.db.xp = 700
        else:
            caller.db.xp = 500

        if destiny == "wealth":
            caller.db.credits = 20000
        else:
            caller.db.credits = 2000

        if destiny == "talented":
            caller.db.free_talents = 3
        else:
            caller.db.free_talents = 1

        if destiny == "destined":
            caller.db.max_dp = 15
            caller.db.destiny_pool = 15
        else:
            caller.db.max_dp = 10
            caller.db.destiny_pool = 10

        if destiny == "force":
            caller.scripts.add('typeclasses.force_handler.ForceHandler', key='force')

        caller.msg("Destiny Attribute set to %s" % destiny.title())


def askAge(caller):
    text = "Please enter your character's Age or <return> to go back."
    options = ({"key": "_default",
                "exec": setAge,
                "goto": "menu_start_node"})
    return text, options


def setAge(caller, raw_string):
    age = raw_string.strip()
    if not age:
        caller.msg("Returning")
    else:
        caller.db.age = age
        caller.msg("Age set to %s" % age)


def setFullname(caller, raw_string):
    name = raw_string.strip()
    if not name:
        caller.msg("Returning")
    else:
        caller.db.fullname = name
        caller.msg("Fullname set to %s" % caller.db.fullname)


def askFullname(caller):
    text = "Please enter your characters Full Name or <return> to go back."
    options = ({"key": "_default",
                "exec": setFullname,
                "goto": "menu_start_node"})

    return text, options


def _wrapper(caller, i):
    return lambda caller: setattr(caller.ndb._menutree, "selected_level", i)


def askLevelSelect(caller):
    xp = caller.db.xp
    if caller.db.destiny == "experience":
        num_levels = xp / 90
    else:
        num_levels = xp / 100

    options = ()
    text = "You currently have |w%s|n xp.  You have enough for |y%s|n levels.  Please choose the class that you wish " \
           "to level in." % (xp, num_levels)

    for item in sorted(get_levels(caller)):
        node_dict = {"desc": item.title(), "goto": "confirm_class", "exec": _wrapper(caller, item)}
        options += (node_dict,)

    return text, options


def confirm_class(caller):
    text = "Are you sure you want to level up in %s? |wYes|n or |wNo|n" % caller.ndb._menutree.selected_level.title()

    options = ({"key": ("Y", "Yes", "y", "yes"),
                "desc": "Yes",
                "exec": set_class,
                "goto": "menu_start_node"},
               {"key": ("N", "No", "n", "no"),
                "desc": "No",
                "goto": "menu_start_node"})

    return text, options


def set_class(caller):
    if not caller.db.destiny:
        caller.msg("|rYou have not selected a Destiny attribute yet.  That must be selected before taking levels.|n")
        return
    if not caller.db.species:
        caller.msg("|rYou have not selected a species yet.  That must be selected before taking levels.|n")
        return
    if not caller.ndb._menutree.selected_level:
        caller.msg("There was a problem.  Report this issue to the admins.")
    else:
        all_classes = dict(classes.BASE_CLASSES.items() + classes.BASE_PRESTIGE.items() +
                           classes.FORCE_BASE_CLASSES.items() +
                           classes.FORCE_PRESTIGE_CLASSES.items() + classes.FORCE_MASTER_CLASSES.items())

        base_classes = dict(classes.BASE_CLASSES.items() + classes.BASE_PRESTIGE.items())

        force_classes = dict(classes.FORCE_BASE_CLASSES.items() +
                             classes.FORCE_PRESTIGE_CLASSES.items() + classes.FORCE_MASTER_CLASSES.items())
        class_to_level = all_classes[caller.ndb._menutree.selected_level]

        if class_to_level:
            if caller.ndb._menutree.selected_level in base_classes:
                for attribute, value in class_to_level.items():
                    caller.skills.add(name=attribute, base=value)
            elif caller.ndb._menutree.selected_level in force_classes:
                caller.force.set_attack(class_to_level.get("attack"))
                caller.force.set_defend(class_to_level.get("defend"))
                caller.force.set_neutral(class_to_level.get("neutral"))
            else:
                caller.msg("That is not a valid class.  Please try again.")
                return
        if caller.db.destiny == "experience":
            caller.db.xp -= 90
        else:
            caller.db.xp -= 100

        caller.db.level += 1
        chosen_species = caller.db.species

        for key, amount in species.SPECIES.get(chosen_species).get('skills'):
            caller.skills.add(name=key, base=amount)
        caller.msg("You have leveled up in %s" % caller.ndb._menutree.selected_level.title())


def quit_node(caller):
    text = "Goodbye"
    options = ()

    return text, options


def get_levels(caller):
    classes_to_return = []
    prestige_attributes = []

    for skill in caller.skills.get_skills():
        if skill.base >= 50:
            prestige_attributes.append(skill.name)

    for item in classes.BASE_PRESTIGE:
        prime_attribute = max(classes.BASE_PRESTIGE[item].items(), key=operator.itemgetter(1))[0]
        if prime_attribute in prestige_attributes:
            classes_to_return.append(item)

    for item in classes.BASE_CLASSES:
        classes_to_return.append(item)

    if caller.db.destiny == "force":
        for item in classes.FORCE_BASE_CLASSES:
            classes_to_return.append(item)

    if not caller.db.jedi and "jedi" in classes_to_return:
        classes_to_return.remove("jedi")

    if not caller.db.sith and "sith" in classes_to_return:
        classes_to_return.remove("sith")

    return classes_to_return


def exit_message(caller, menu):
    caller.cmdset.delete("commands.default_cmdsets.ChargenCmdSet")
    caller.msg("Exiting +chargen.  Goodbye.")
