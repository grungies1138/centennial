"""
    Comlinks are objects used for IC live, in-game communication between characters.

    Comlinks are made up of connections to Frequencies which inherit from Channel.
    Each frequency cont
"""

from typeclasses.objects import Object
from typeclasses.channels import Channel
from typeclasses.characters import Character
from evennia import default_cmds, CmdSet, DefaultScript
from evennia.comms.models import TempMsg, ChannelDB
from evennia.utils import create


def find_frequency(freq):
    frequencies = ChannelDB.objects.channel_search(freq)
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

    def at_msg_receive(self, msg, from_obj=None, **kwargs):
        pass

    def frequencies(self):
        return [freq for freq in ChannelDB.objects.get_subscriptions(self)]

    def add_frequency(self, freq):
        if len(self.frequencies()) < 5:
            frequency = find_frequency(freq)

            if frequency is not None:
                if frequency.connect(self):
                    self.message_holder("Frequency added.")
                else:
                    self.message_holder("There was a problem adding the frequency.  Contact a staff member.")
            else:
                new_freq = create.create_channel(freq, typeclass=Frequency)
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
        pass

    def decrypt(self, freq):
        pass


class ComlinkCmd(default_cmds.MuxCommand):
    """
    Allows usage of the comlink device.

    Usage:
        |w+comlink <character or frequency>=[: or ;]<message>|n - this
            command sends a message to the character or frequency selected.
            |yNOTE:|n the selected frequency must be in the frequency list
            on the comlink device.

        |w+comlink/add <0000-9999>[=<label>]|n - This adds the given frequency to the
            list of tuned frequencies for this comlink with an optional label.  Up to
            5 frequencies can be saved at a time.

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
