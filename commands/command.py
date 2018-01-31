"""
Commands

Commands describe the input the player can do to the game.

"""

import time
from evennia import Command as BaseCommand
from evennia import default_cmds, search_object
from evennia.utils import create, utils, evtable, evform, gametime, inherits_from, delay
from library import titlecase, header
from world import rules
from evennia.server.sessionhandler import SESSIONS
from evennia import search_object
from evennia.contrib import custom_gametime
from server.conf.settings import TIME_GAME_EPOCH, TIME_FACTOR, TIME_UNITS, GREAT_RESYNCHRONIZATION, BATTLE_OF_YAVIN, \
    OLD_REPUBLIC, TREAT_OF_CORUSCANT, RUUSAN_REFORMATION


class SheetCommand(BaseCommand):
    """
    Displays a simple sheet to view stats and such.
    """

    key = "+sheet"
    aliases = ["she"]
    lock = "cmd:perm(Player)"
    help_category = "General"

    def func(self):
        row_separator = "\n" + "-" * 78
        self.caller.msg("------------------------------ Character Sheet ------------------------------")
        table = evtable.EvTable("|wSkill Name:|n", "|wSkill Level:|n", table=None, border=None,
                                pad_width=0, width=78)

        for key in self.caller.skills.get_skills():
            table.add_row("%s:" % titlecase(key.name), "|y%s|n" % titlecase(key.value))

        table.reformat_column(0, width=20)

        message = []

        if self.caller.db.xp > 100 or (self.caller.db.special == "experience" and self.caller.db.xp > 90):
            level_string = "|wXP:|n %s |Y(can level)|n" % self.caller.db.xp
        else:
            level_string = "|wXP:|n %s" % self.caller.db.xp
        message.append("|wFullname:|n {}              |wAge:|n {}    |wLevel:|n {}   {}"
                       .format(self.caller.db.fullname, self.caller.db.age, self.caller.db.level, level_string))
        message.append("-" * 78)

        titled_languages = []
        if hasattr(self.caller, "db.languages"):
            for lang in self.caller.db.languages:
                titled_languages.append(titlecase(lang))

        titled_talents = []

        for talent in self.caller.db.talents:
            titled_talents.append(titlecase(talent))

        talents_table = evtable.EvTable("|wTalents:|n", "|wLanguages:|n", border=None,
                                        table=[titled_talents, titled_languages])
        # for talent in titled_talents:
        #     talents_table.add_row(talent)

        talents_table.reformat_column(0, width=26)
        talents_table.reformat_column(1, width=26)


        self.caller.msg("\n".join(message))
        self.caller.msg(table)
        self.caller.msg(row_separator)
        self.caller.msg(talents_table)
        self.caller.msg(row_separator)
        self.caller.msg("|wHealth:|n %s|-|-|wEndurance:|n %s / %s" % (self.parse_health(self.caller),
                                                                      self.caller.endurance.get(),
                                                                      self.caller.endurance.db.max_endurance))
        self.caller.msg("|wWielding:|n %s|-|-|wWearing:|n %s" % (self.caller.db.wielding, self.caller.db.wearing))
        self.caller.msg(row_separator)


    @staticmethod
    def parse_health(target):
        current = float(target.health.get())
        max_health = float(target.health.db.max_health)

        if max_health > 0:
            percent = int(current / max_health * 100)
        else:
            percent = 0

        if percent > 75:
            return '|230Good|n'
        elif percent > 50:
            return '|450Injured|n'
        elif percent > 25:
            return '|550Seriously Injured|n'
        elif percent > 10:
            return '|500Critically Injured|n'
        elif percent > 0:
            return '|305Mortally Wounded|n'
        else:
            return '|[300Deceased|n'


class CheckCommand(BaseCommand):
    key = "+check"
    aliases = ["check"]
    lock = "cmd:perm(Player)"
    help_category = "Skills"

    def func(self):
        command_input = self.args.strip()

        if not command_input:
            self.caller.msg("You must select a skill to check")
            return
        die_roll = rules.roll_skill(self.caller, command_input)

        if not die_roll:
            self.caller.msg("There was an error.  Please try again.  If this error persists, please contact a staff "
                            "member.")
            return

        self.caller.msg("You rolled %d" % die_roll)


class OOCCommand(default_cmds.MuxCommand):
    """
    Send an OOC message just to the people in your current room.

    Usage:
        ooc [:, ;]<text>

    """

    key = "ooc"
    aliases = []
    lock = "cmd:all()"
    help_category = "General"

    def func(self):
        if not self.args:
            self.caller.msg("Huh?")

        prefix = "|w<|n|005OOC|n|w>|n"

        speech = self.args.strip()

        if speech[0] == ":":
            speech_text = speech[1:]
            self.caller.location.msg_contents("%s %s %s" % (prefix, self.caller.name, speech_text))
        elif speech[0] == ";":
            speech_text = speech[1:]
            self.caller.location.msg_contents("%s %s%s" % (prefix, self.caller.name, speech_text))
        else:
            self.caller.location.msg_contents("%s %s says, \"%s\"" % (prefix, self.caller.name, speech))


class CmdUseEquipment(default_cmds.MuxCommand):
    """
    Ues Equipment which effects a skill check with the equipment's modification.

    Usage:
        +use <item>

    """

    key = "+use"
    lock = "cmd:perm(Player)"
    help_category = "General"

    def func(self):
        if not self.args:
            self.caller.msg("You must choose an item to use")
            return

        item = self.caller.search(self.args)
        equipment = None
        consumable = None

        if inherits_from(item, "typeclasses.equipment.Equipment"):
            equipment = item
        elif inherits_from(item, "typeclasses.consumable.Consumable"):
            consumable = item

        if not equipment:
            self.caller.msg("That is not a valid item.  Please check the name and try again.")
            return

        if not inherits_from(equipment, "typeclasses.equipment.Equipment"):
            self.caller.msg("That is not a piece equipment or a consumable.  Please select one and try again.")
            return

        if equipment not in self.caller.contents:
            self.caller.msg("That item is not in your inventory.")
            return

        func = equipment.function()

        func_skills = func.get("skills")
        health_mod = func.get("health")

        if func_skills:
            for skill in func_skills.keys():
                self.notify_room(skill, self.caller.skills.get(skill))

        if health_mod:
            self.caller.health.heal(health_mod)
            self.caller.location.msg_contents("%s has used a %s to heal themselves." % (self.caller.key, equipment.key))

    def notify_room(self, skill, value):
        players = self.caller.location.contents

        for player in players:
            if self.caller.locks.check_lockstring(player, "dummy:perm(Admin)"):
                player.msg("%s checked %s: %s (%s)" % (self.caller.key, skill, rules.parse_skill_check(value), value))
            else:
                player.msg("%s checked %s: %s" % (self.caller.key, skill, rules.parse_skill_check(value)))


class WhoCommand(default_cmds.MuxCommand):
    """
    Shows the currently connected players.

    Usage:
        who
        +who

    """

    key = "+who"
    aliases = []
    locks = "cmd:all()"
    help_category = "General"

    def func(self):
        session_list = SESSIONS.get_sessions()

        table = evtable.EvTable(" |wName:|n", "|wIdle:|n", "|wConn:|n", "|wAffiliation:|n", table=None,
                                border='header', header_line_char='-', width=78)

        for session in session_list:
            player = session.get_account()
            idle = time.time() - session.cmd_last_visible
            conn = time.time() - session.conn_time
            if session.get_puppet():
                affiliation = session.get_puppet().db.affiliation
            else:
                affiliation = ""
            flag = None
            if player.locks.check_lockstring(player, "dummy:perm(Admin)"):
                flag = "|y!|n"
            elif player.locks.check_lockstring(player, "dummy:perm(Builder)"):
                flag = "|g&|n"
            elif player.locks.check_lockstring(player, "dummy:perm(Helper)"):
                flag = "|r$|n"
            else:
                flag = " "
            table.add_row(flag + utils.crop(player.name), utils.time_format(idle, 0),
                          utils.time_format(conn, 0), affiliation)

        table.reformat_column(0, width=24)
        table.reformat_column(1, width=12)
        table.reformat_column(2, width=12)
        table.reformat_column(3, width=30)

        self.caller.msg("|b-|n" * 78)
        self.caller.msg("|yStar Wars: Centennial|n".center(78))
        self.caller.msg("|b-|n" * 78)
        self.caller.msg(table)
        self.caller.msg("|b-|n" * 78)
        self.caller.msg("Total Connected: %s" % SESSIONS.account_count())
        whotable = evtable.EvTable("", "", "", header=False, border=None)
        whotable.reformat_column(0, width=26)
        whotable.reformat_column(1, width=26)
        whotable.reformat_column(2, width=26)
        whotable.add_row("|y!|n - Administrators", "|g&|n - Storytellers", "|r$|n - Player Helpers")
        self.caller.msg(whotable)
        self.caller.msg("|b-|n" * 78)


class CmdInventory(default_cmds.MuxCommand):
    """
        view inventory
        Usage:
          inventory
          inv
        Shows your inventory.
        """
    key = "inventory"
    aliases = ["inv", "i"]
    locks = "cmd:all()"
    arg_regex = r"$"

    def func(self):
        items = self.caller.contents
        if not items:
            string = "You are not carrying anything."
        else:
            table = evtable.EvTable(border="header")
            for item in items:
                table.add_row("|C%s|n" % item.name)
            string = "|wYou are carrying:|n\n%s" % table
        self.caller.msg(string)


class CmdWield(default_cmds.MuxCommand):
    """
    Command to allow the user to wield a weapon from their inventory.

    Usage:
        +wield <weapon>
    """

    key = "+wield"
    locks = "cmd:perm(Player)"
    help_category = "Combat"

    def func(self):
        if not self.args:
            self.caller.msg("You must choose a weapon to wield.")
            return

        obj = self.caller.search(self.args)

        if not obj:
            self.caller.msg("That is not a valid item.  Please check the name and try again.")
            return

        if not inherits_from(obj, "typeclasses.weapon.Weapon"):
            self.caller.msg("That is not a weapon.  Please choose a weapon to wield and try again.")
            return

        if obj.location != self.caller:
            self.caller.msg("That item is not in your inventory.")
            return

        if self.caller.db.wielding:
            self.caller.msg("You are already wielding a weapon.  Please +unwield first, then try again")
            return

        self.caller.db.wielding = obj
        self.caller.msg("You have readied %s for combat" % obj.key)


class CmdUnwield(default_cmds.MuxCommand):
    """
    Removes a weapon from a wielded state.

    Usage:
        +unwield
    """

    key = "+unwield"
    locks = "cmd:perm(Player)"
    help_category = "Combat"

    def func(self):
        if not self.caller.db.wielding:
            self.caller.msg("You are not currently wielding anything.")
            return
        self.caller.db.wielding = None
        self.caller.msg("You have unwielded your weapon.")


class CmdWear(default_cmds.MuxCommand):
    """
    Command to put on armor.

    Usage:
        +wear <armor>
    """

    key = "+wear"
    locks = "cmd:perm(Player)"
    help_category = "Combat"

    def func(self):
        if not self.args:
            self.caller.msg("You must choose armor to wear.")
            return

        obj = self.caller.search(self.args)

        if not obj:
            self.caller.msg("That is not a valid item.  Please check the name and try again.")
            return

        if not inherits_from(obj, "typeclasses.armor.Armor"):
            self.caller.msg("That is not armor.  Please choose armor to wear and try again.")
            return

        if obj.location != self.caller:
            self.caller.msg("That item is not in your inventory.")
            return

        if self.caller.db.wearing:
            self.caller.msg("You are already wearing armor.  Please +unwear first, then try again.")
            return

        self.caller.db.wearing = obj
        self.caller.msg("You are now protected by your %s" % obj.key)


class CmdUnwear(default_cmds.MuxCommand):
    """
    Command removes worn armor.

    Usage:
        +unwear
    """

    key = "+unwear"
    locks = "cmd:perm(Player)"
    help_category = "Combat"

    def func(self):
        if not self.caller.db.wearing:
            self.caller.msg("You are not currently wearing armor.")
            return
        self.caller.db.wearing = None
        self.caller.msg("You have removed your armor.")


class CmdPage(default_cmds.MuxCommand):
    """
    send a private message to another player
    Usage:
      page[/switches] [<player>,<player>,... = <message>]
      tell        ''
      page <number>
    Switch:
      last - shows who you last messaged
      list - show your last <number> of tells/pages (default)
    Send a message to target user (if online). If no
    argument is given, you will get a list of your latest messages.
    """

    key = "page"
    aliases = ['p']
    locks = "cmd:not pperm(page_banned)"
    help_category = "Comms"

    # this is used by the COMMAND_DEFAULT_CLASS parent
    player_caller = True

    def func(self):
        if 'last' in self.switches:
            self.caller.msg("You last paged: %s" % self.caller.db.last_paged)
            return

        if '=' not in self.args:
            if not self.caller.db.last_paged:
                self.caller.msg("You have no previous paged player.  Please enter the name of a person to page.")
                return
            text = ""
            valid_chars = []
            for item in self.caller.db.last_paged:
                search_char = search_object(item)
                if len(search_char) > 0:
                    char = search_char[0]
                else:
                    char = None
                if char:
                    if not char.sessions.all():
                        self.caller.msg("Player %s is not currently connected." % str(char.key))
                    valid_chars.append(char.key)
                    if self.args[:1] == ":":
                        text = "%s %s" % (self.caller.key, self.args[1:])
                    elif self.args[:1] == ";":
                        text = "%s%s" % (self.caller.key, self.args[1:])
                    else:
                        text = "%s pages: %s" % (self.caller.key, self.args)
                    char.msg("From far away, %s" % text)
                else:
                    self.caller.msg("That is not a valid character name.")
            if len(valid_chars) > 0:
                names = str(valid_chars[0])
                for name in valid_chars[1:]:
                    names += ", %s" % str(name)
                self.caller.msg("You paged %s: %s" % (names, text))
            else:
                self.caller.msg("No valid recipient found.")
        else:
            text = ""
            valid_chars = []
            to_send = self.lhs.split()
            for item in to_send:
                search_char = search_object(item)
                if len(search_char) > 0:
                    char = search_char[0]
                else:
                    char = None
                if char:
                    if not char.sessions.all():
                        self.caller.msg("Player %s is not currently connected." % str(char.key))
                    valid_chars.append(char.key)
                    if self.rhs[:1] == ":":
                        text = "%s %s" % (self.caller.key, self.rhs[1:])
                    elif self.rhs[:1] == ";":
                        text = "%s%s" % (self.caller.key, self.rhs[1:])
                    else:
                        text = "%s pages: %s" % (self.caller.key, self.rhs)
                    char.msg("From far away, %s" % text)
                else:
                    self.caller.msg("That is not a valid character name.")

            names = str(valid_chars[0])
            for name in valid_chars[1:]:
                names += ", %s" % str(name)

            self.caller.msg("You paged %s: %s" % (names, text))
            self.caller.db.last_paged = self.lhslist


class TimeCommand(default_cmds.MuxCommand):
    """
    Usage:
        +time

    This command displays the current in-game time based on the Galactic Standard Calendar.

    |wGalactic Standard Calendar:|n         |wDays of the week:|n
        Elona                               Primeday
        Kelona                              Centaxday
        Tapani Day                          Taungsday
        Selona                              Zhellday
        Expansion Week                      Benduday
        Telona
        Nelona
        Productivity Day                |wMeasurements:|n
        Helona                              minute = 60 seconds
        Shelova Week                        hour = 60 minutes
        Melona                              day = 24 hours
        Yelona                              week = 5 days
        Harvest Day                         month = 7 weeks
        Relona                              year = 10 months + 3 weeks + 3 days
        Welona
        Winter Fete - End of the year festival week.
    """

    key = "+time"
    aliases = ["time"]
    help_category = "General"

    def func(self):
        base_year = TIME_UNITS.get("year")
        current = gametime.gametime(absolute=True)
        years = int(current / base_year)
        remainder = int(current % base_year)
        date_string = self.parse_date(remainder)
        year, month, week, day, hour, min, sec = custom_gametime.custom_gametime(absolute=True)
        message = []
        message.append("\n")
        message.append("|wCurrent Date & Time|n")
        message.append("|-{:0>2d}:{:0>2d}:{:0>2d} {}".format(hour, min, sec, date_string))
        message.append("|wYears since:|n")

        old_republic = "{:,}".format((OLD_REPUBLIC / base_year) + years)
        message.append("|-Founding of the Old Republic: |051%s|n" % old_republic)

        treaty = "{:,}".format((TREAT_OF_CORUSCANT / base_year) + years)
        message.append("|-Signing of the Treaty of Coruscant: |051%s|n" % treaty)

        ruusan = "{:,}".format((RUUSAN_REFORMATION / base_year) + years)
        message.append("|-Ruusan Reformation: |051%s|n" % ruusan)

        great_resync = "{:,}".format((GREAT_RESYNCHRONIZATION / base_year) + years)
        message.append("|-Great Resynchronization: |051%s|n" % great_resync)

        battle_of_yavin = "{:,}".format((BATTLE_OF_YAVIN / base_year) + years)
        message.append("|-Battle of Yavin: |051%s|n" % battle_of_yavin)
        message.append("\n")

        self.caller.msg("\n".join(message))

    def parse_date(self, seconds):
        month = ""
        week = ""
        day = ""
        date = 0

        calculated_days = seconds / TIME_UNITS.get("day")
        if calculated_days <= 35:
            month = "Elona"
            day_of_week_remainder = calculated_days % 5
            if day_of_week_remainder == 1:
                day = "Primeday"
            elif day_of_week_remainder == 2:
                day = "Centaxday"
            elif day_of_week_remainder == 3:
                day = "Taungsday"
            elif day_of_week_remainder == 4:
                day = "Zhellday"
            else:
                day = "Benduday"

            date = calculated_days

        elif calculated_days >= 36 and calculated_days <= 70:
            month = "Kelona"
            day_of_week_remainder = (calculated_days - 35) % 5
            if day_of_week_remainder == 1:
                day = "Primeday"
            elif day_of_week_remainder == 2:
                day = "Centaxday"
            elif day_of_week_remainder == 3:
                day = "Taungsday"
            elif day_of_week_remainder == 4:
                day = "Zhellday"
            else:
                day = "Benduday"

            date = calculated_days - 35

        elif calculated_days >= 71 and calculated_days <= 71:
            day = "Tapani Day"

        elif calculated_days >= 72 and calculated_days <= 107:
            month = "Selona"
            day_of_week_remainder = (calculated_days - 71) % 5
            if day_of_week_remainder == 1:
                day = "Primeday"
            elif day_of_week_remainder == 2:
                day = "Centaxday"
            elif day_of_week_remainder == 3:
                day = "Taungsday"
            elif day_of_week_remainder == 4:
                day = "Zhellday"
            else:
                day = "Benduday"

            date = calculated_days - 71

        elif calculated_days >= 108 and calculated_days <= 112:
            week = "Expansion Week"
            day_of_week_remainder = (calculated_days - 107) % 5
            if day_of_week_remainder == 1:
                day = "Primeday"
            elif day_of_week_remainder == 2:
                day = "Centaxday"
            elif day_of_week_remainder == 3:
                day = "Taungsday"
            elif day_of_week_remainder == 4:
                day = "Zhellday"
            else:
                day = "Benduday"

        elif calculated_days >= 113 and calculated_days <= 147:
            month = "Telona"
            day_of_week_remainder = (calculated_days - 112) % 5
            if day_of_week_remainder == 1:
                day = "Primeday"
            elif day_of_week_remainder == 2:
                day = "Centaxday"
            elif day_of_week_remainder == 3:
                day = "Taungsday"
            elif day_of_week_remainder == 4:
                day = "Zhellday"
            else:
                day = "Benduday"

            date = calculated_days - 112

        elif calculated_days >= 148 and calculated_days <= 182:
            month = "Nelona"
            day_of_week_remainder = (calculated_days - 147) % 5
            if day_of_week_remainder == 1:
                day = "Primeday"
            elif day_of_week_remainder == 2:
                day = "Centaxday"
            elif day_of_week_remainder == 3:
                day = "Taungsday"
            elif day_of_week_remainder == 4:
                day = "Zhellday"
            else:
                day = "Benduday"

            date = calculated_days - 147

        elif calculated_days >= 183 and calculated_days <= 183:
            day = "Tapani Day"

        elif calculated_days >= 184 and calculated_days <= 217:
            month = "Helona"
            day_of_week_remainder = (calculated_days - 183) % 5
            if day_of_week_remainder == 1:
                day = "Primeday"
            elif day_of_week_remainder == 2:
                day = "Centaxday"
            elif day_of_week_remainder == 3:
                day = "Taungsday"
            elif day_of_week_remainder == 4:
                day = "Zhellday"
            else:
                day = "Benduday"

            date = calculated_days - 183

        elif calculated_days >= 218 and calculated_days <= 222:
            week = "Shelova Week"
            day_of_week_remainder = (calculated_days - 217) % 5
            if day_of_week_remainder == 1:
                day = "Primeday"
            elif day_of_week_remainder == 2:
                day = "Centaxday"
            elif day_of_week_remainder == 3:
                day = "Taungsday"
            elif day_of_week_remainder == 4:
                day = "Zhellday"
            else:
                day = "Benduday"

        elif calculated_days >= 223 and calculated_days <= 257:
            month = "Melona"
            day_of_week_remainder = (calculated_days - 222) % 5
            if day_of_week_remainder == 1:
                day = "Primeday"
            elif day_of_week_remainder == 2:
                day = "Centaxday"
            elif day_of_week_remainder == 3:
                day = "Taungsday"
            elif day_of_week_remainder == 4:
                day = "Zhellday"
            else:
                day = "Benduday"

            date = calculated_days - 222

        elif calculated_days >= 258 and calculated_days <= 292:
            month = "Yelona"
            day_of_week_remainder = (calculated_days - 257) % 5
            if day_of_week_remainder == 1:
                day = "Primeday"
            elif day_of_week_remainder == 2:
                day = "Centaxday"
            elif day_of_week_remainder == 3:
                day = "Taungsday"
            elif day_of_week_remainder == 4:
                day = "Zhellday"
            else:
                day = "Benduday"

            date = calculated_days - 257

        elif calculated_days >= 293 and calculated_days <= 293:
            day = "Harvest Day"

        elif calculated_days >= 294 and calculated_days <= 327:
            month = "Relona"
            day_of_week_remainder = (calculated_days - 293) % 5
            if day_of_week_remainder == 1:
                day = "Primeday"
            elif day_of_week_remainder == 2:
                day = "Centaxday"
            elif day_of_week_remainder == 3:
                day = "Taungsday"
            elif day_of_week_remainder == 4:
                day = "Zhellday"
            else:
                day = "Benduday"

            date = calculated_days - 293

        elif calculated_days >= 328 and calculated_days <= 362:
            month = "Welona"
            day_of_week_remainder = (calculated_days - 327) % 5
            if day_of_week_remainder == 1:
                day = "Primeday"
            elif day_of_week_remainder == 2:
                day = "Centaxday"
            elif day_of_week_remainder == 3:
                day = "Taungsday"
            elif day_of_week_remainder == 4:
                day = "Zhellday"
            else:
                day = "Benduday"

            date = calculated_days - 327

        else:
            week = "Winter Fete"
            day_of_week_remainder = (calculated_days - 362) % 5
            if day_of_week_remainder == 1:
                day = "Primeday"
            elif day_of_week_remainder == 2:
                day = "Centaxday"
            elif day_of_week_remainder == 3:
                day = "Taungsday"
            elif day_of_week_remainder == 4:
                day = "Zhellday"
            else:
                day = "Benduday"


        date_string = "%s" % day


        if date:
            date_string += ", %s of " % date

        if week:
            date_string += " of %s" % week

        if month:
            date_string += "%s" % month

        return date_string


class CmdRepose(default_cmds.MuxCommand):
    """
    Command to view the last few poses made in the current room

    Usage:
        +repose
    """

    key = "+repose"
    locks = "cmd:perm(Player)"

    def func(self):
        location = self.caller.location
        poses = location.db.poses

        message = []
        message.append("Pose list for %s" % location.key)
        message.append("|b%s|n" % header())

        for pose in poses:
            message.append("|w%s|n|-%s" % (pose.get('name'), pose.get('time')))
            message.append(pose.get('pose'))
            message.append(header())

        message2 = []
        for line in message:
            message2.append(unicode(line))
        self.caller.msg("\n".join(message2))


class CmdOOC(default_cmds.MuxCommand):
    """
    Send the character to the OOC area.

    Usage:
        +ooc
    """

    key = "+ooc"
    locks = "cmd:perm(Player)"

    def func(self):
        if not self.caller.db.ic_location:
            self.caller.msg("You do not have an IC Location.  To enter the IC world, proceed to the IC Launchpad.")
            return

        if self.caller.db.status == 'IC':
            self.caller.db.ic_location = self.caller.location
            limbo = self.caller.search("Limbo", global_search=True)
            self.caller.move_to(limbo)
            self.caller.db.status = 'OOC'
        else:
            self.caller.msg("You are already OOC.  type |w+ic|n to return to the IC world.")


class CmdIC(default_cmds.MuxCommand):
    """
    Send the character back to the IC realm

    Usage:
        +ic
    """

    key = "+ic"
    locks = "cmd:perm(Player)"

    def func(self):
        if self.caller.db.status == 'IC':
            self.caller.msg("You are not OOC. type |w+ooc|n to move to the OOC realm")
            return
        if not self.caller.db.ic_location:
            self.caller.msg("You have no IC location.  If you are seeing this area and have already been in the IC "
                            "realm, please contact a staff member.")
            return
        self.caller.move_to(self.caller.db.ic_location)
        self.caller.db.status = 'IC'


class CmdJoin(default_cmds.MuxCommand):
    """
    Allows an admin to join a character's current location.

    Usage:
        +join <character>
    """

    key = "+join"
    locks = "cmd:perm(Admin)"

    def func(self):
        if not self.args:
            self.caller.msg("You must define a character to join.")
            return
        char = self.caller.search(self.args, global_search=True)
        if not char:
            self.caller.msg("That is not a valid character.  Please try again.")
            return

        self.caller.msg("Joining %s in 5 seconds." % char.key)
        char.location.msg_contents("%s will be joining this location in 5 seconds." % self.caller.key)
        yield 5
        self.caller.move_to(char.location)


class CmdPose(default_cmds.MuxCommand):
    """
    Used to display to the room the actions of the character.  No name is prepended.

    Text formatting help:
        ||/ - carriage return
        ||- - tab

    Usage:
        +pose <text>
    """

    key = "+pose"
    locks = "cmd:perm(Player)"

    def func(self):
        if not self.args:
            self.caller.msg("Use |w+pose <text>|n to pose.")
            return

        self.caller.location.msg_contents("|/%s|/" % self.args)
