"""
    Comlinks are objects used for IC live, in-game communication between characters.

    Comlinks are made up of connections to Frequencies which inherit from Channel.
    Each frequency cont
"""

from typeclasses.objects import Object
from typeclasses.channels import Channel
from typeclasses.characters import Character
from evennia import default_cmds, CmdSet, DefaultScript
from evennia.comms.models import TempMsg
from evennia.utils import create, evtable
from evennia.comms.channelhandler import CHANNELHANDLER
# from commands.library import header
import re


def find_frequency(freq):
    frequencies = Frequency.objects.channel_search(freq)
    if not frequencies:
        return None

    if len(frequencies) > 1:
        return None

    return frequencies[0]


class Frequency(Channel):
    def channel_prefix(self, msg, emit=False):
        return "|=m<|n|045%s|n|=m>|n:" % self.key


class ComlinkCmdSet(CmdSet):
    key = "ComlinkCmdSet"

    def at_cmdset_creation(self):
        self.add(ComlinkCmd())


class Comlink(Object):
    def at_object_creation(self):
        self.cmdset.add(ComlinkCmdSet)
        self.db.speaker = False
        self.db.passwords = []

    def at_msg_receive(self, msg, from_obj=None, **kwargs):
        pass

    def frequencies(self):
        return [freq for freq in Frequency.objects.all() if self in freq.subscriptions.all()]

    def add_frequency(self, freq):
        if len(self.frequencies()) < 5:
            frequency = find_frequency(freq)

            if frequency is not None:
                if frequency.connect(self):
                    self.message_holder("Frequency added.")
                else:
                    self.message_holder("There was a problem adding the frequency.  Contact a staff member.")
            else:
                lockstring = "send:all();listen:all()"
                new_freq = create.create_channel(freq, typeclass="comlink.Frequency", locks=lockstring)
                CHANNELHANDLER.update()
                if new_freq.connect(self):
                    self.message_holder("Frequency added.")
                else:
                    self.message_holder("There was a problem adding the frequency.  Contact a staff member.")
        else:
            self.message_holder("You have too many saved frequencies.  Remove one if you wish to add this one.")

    def remove_frequency(self, freq):
        if len(self.frequencies()) > 0:
            frequency = find_frequency(freq)
            if frequency is not None:
                if frequency in self.frequencies():
                    disconnect = frequency.disconnect(self)
                    if disconnect:
                        self.message_holder("Frequency removed.")
                    else:
                        self.message_holder("There was a problem.  Contact a staff member.")
                else:
                    self.message_holder("That frequency is not saved on this comlink.")
            else:
                self.message_holder("Frequency not found.")
        else:
            self.message_holder("You currently have no saved frequencies.")

    def message_holder(self, message, speaker=False):
        prefix = "|rComlink:|n "
        if self.location is Character:
            if speaker:
                self.location.location.msg_contents(prefix + message)
            else:
                self.location.msg(prefix + message)

    def encrypt(self, freq, password):
        frequency = find_frequency(freq)

        if frequency:
            if frequency in self.frequencies():
                self.db.passwords.append({"frequency": freq, "password": password})
            else:
                self.message_holder("That frequency is not saved on your comlink.")
        else:
            self.message_holder("There was a problem setting a password on that frequency.  Contact a staff member.")

    def decrypt(self, freq):
        frequency = [fq for fq in self.db.passwords if fq.get("frequency") == freq]

        if frequency:
            self.db.password.remove(frequency)
            self.message_holder("Frequency decrypted.")
        else:
            self.message_holder("Frequency not found.")


class ComlinkCmd(default_cmds.MuxCommand):
    """
    Allows usage of the comlink device.

    Usage:
        |w+comlink <character list or frequency>=[: or ;]<message>|n - this
            command sends a message to the character or characters (space
            separated list) or frequency selected. |yNOTE:|n the selected frequency must be in the frequency list
            on the comlink device.

        |w+comlink/add <0000-9999>|n - This adds the given frequency
            to the list of tuned frequencies for this comlink.  Up to 5
            frequencies can be saved at a time.

        |w+comlink/remove <0000-9999>|n - This removes the given frequency
            from the the list of tuned frequencies on the device.

        |w+comlink/encrypt <0000-9999>=<password>|n - Encrypt messages on a
            specific frequency.  Also allows the device to receive encrypted
            message.

        |w+comlink/decipher <0000-9999>=<password>|n - Set the password used to
            decipher encrypted messages on an encrypted frequency.

        |w+comlink/decrypt <0000-9999>|n - Removes encryption from the
            frequency.  The device will no longer be able to send or receive
            encrypted messages on the specified frequency.

        |w+comlink/broadcast [: or ;]<message>|n - This sends an area-wide
            message across all comlinks in your current zone.

        |w+comlink [: or ;]<message>|n - Sends a message to the last sent to
            location. (person or frequency)

        |w+comlink/slice <0000-9999>|n - Attempt to force decryption of the
            messages on a specific frequency.

        |w+comlink/list|n - Displays the current list of frequencies and associated
            passwords if applicable.
    """

    key = "+comlink"
    locks = "cmd:perm(Player)"
    help_category = "Comlinks"

    def func(self):
        comlink_prefix = "|rComlink:|n "
        if self.switches:
            if "add" in self.switches:
                if not self.args:
                    self.caller.msg(comlink_prefix + "Usage: |w+comlink/add <0000-9999>")
                    return
                if self.parse_freq(self.args):
                    self.caller.msg("Parsed Frequency.")
                    self.obj.add_frequency(self.args)

                    return
                else:
                    self.caller.msg("Invalid Frequency number.  Please try again.")
                    return
            if "remove" in self.switches:
                if self.parse_freq(self.args):
                    self.obj.remove_frequency(self.args)
                    return
                else:
                    self.caller.msg("Invalid Frequency number.  Please try again.")
                    return
            if "encrypt" in self.switches:
                pass
            if "decipher" in self.switches:
                pass
            if "decrypt" in self.switches:
                pass
            if "broadcast" in self.switches:
                pass
            if "list" in self.switches:
                table = evtable.EvTable("Frequency:", "Password", border="header", header_line_char="-")
                table.reformat_column(0, width=12)
                for freq in self.obj.frequencies():
                    password = [pwd for pwd in self.obj.db.passwords if freq.get("password")]
                    table.add_row(freq, password)

                self.caller.msg(unicode(table))
                return

            if "slice" in self.switches:
                self.caller.msg(comlink_prefix + "Not yet implemented.")
        else:
            if "=" in self.args:
                pass
            else:
                pass

    @staticmethod
    def parse_freq(freq_string):
        if len(freq_string) > 4:
            return False
        match = re.match(r"[0-9]{1,4}", freq_string)
        if match:
            if len(match.groups()) > 1:
                return False
            else:
                return True
