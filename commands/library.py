import re
from django.conf import settings
from django.utils.timezone import utc
import evennia
from evennia.utils.ansi import ANSIString, ANSI_PARSER
from evennia.utils import evtable, create
from evennia.server.sessionhandler import SESSIONS
from evennia.utils import evtable
from evennia.contrib import rplanguage

HEAD_CHAR = "|015-|n"
SUB_HEAD_CHAR = "-"
MAX_WIDTH = 78


def titlecase(s):
    return re.sub(r"[A-Za-z]+('[A-Za-z]+)?",
                  lambda mo: mo.group(0)[0].upper() +
                             mo.group(0)[1:].lower(), s)


def notify(caller, lockstring, message):
    session_list = SESSIONS.get_sessions()

    for session in session_list:
        player = session.get_puppet()
        if caller.locks.check_lockstring(player, lockstring):
            player.msg(message)


def header(header_text=None, width=MAX_WIDTH, fill_char=HEAD_CHAR):
    header_string = ""
    if header_text and len(header_text) < width:
        header_repeat = (width - len(header_text)) // 2
        header_string = fill_char * header_repeat + header_text + fill_char * header_repeat
        if header_string < width:
            header_string += fill_char * (width - len(header_string))

    else:
        header_string = fill_char * width
    return header_string


#    #######################   MENU UTILITY  #######################
def node_formatter(nodetext, optionstext, caller=None):
    separator1 = "|010_|n" * 78 + "\n\n"
    separator2 = "\n" + "|010_|n" * 78 + "\n\n|330You may type '|540q|n' |330or|n '|540quit|n' " \
                                         "|330at any time to quit this application.|n\n" + "|010_|n" * 78 + "\n\n"
    return separator1 + nodetext + separator2 + optionstext


def options_formatter(optionlist, caller=None):
    options = []
    for key, option in optionlist:
        options.append("|w%s|n: %s" % (key, option))

    if len(options) > 6:
        if len(options) % 2 > 0:
            colA = options[:len(options) / 2 + 1]
            colB = options[len(options) / 2 + 1:]
        else:
            colA = options[:len(options) / 2]
            colB = options[len(options) / 2:]
        table = evtable.EvTable(table=[colA, colB], border=None)

        table.reformat_column(0, width=40)
        table.reformat_column(1, width=40)

        return str(table) + "\n"

    else:
        return "\n".join(options)


def exit_message(caller, menu):
    caller.msg("Exiting +orgs.  Goodbye.")


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in xrange(0, len(l), n):
        yield l[i:i + n]


def translate(text, language):
    return rplanguage.obfuscate_language(text, key=language, level=1.0)
