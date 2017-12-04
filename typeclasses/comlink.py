"""
    Comlinks are objects used for IC live, in-game communication between characters.
"""

from typeclasses.objects import Object
from typeclasses.channels import Channel
from evennia import default_cmds, CmdSet, DefaultScript


class Frequency(Channel):
    def channel_prefix(self, msg, emit=False):
        return "|=m<|n|045%s|n|=m>|n:" % self.key


class ComlinkHandler(DefaultScript):
    def at_script_creation(self):
        self.persistent = True
        self.key = "Comlink_Handler"
        self.desc = "Script to handle all of the comlink communications."

    def join_frequency(self, freq):



class ComlinkCmdSet(CmdSet):
    key = "ComlinkCmdSet"


class Comlink(Object):
    def at_object_creation(self):
        self.cmdset.add(commands.comlink_cmdset.ComlinkCmdSet)


class ComlinkCmd(default_cmds.MuxCommand):
    """
    Allows usage of the comlink device.

    Usage:
        |w+comlink <character or frequency>=[: or ;]<message>|n - this
            command sends a message to the character or frequency selected.
            |yNOTE:|n the selected frequency must be in the frequency list
            on the comlink device.

        |w+comlink/add <0000-9999>|n - This adds the given frequency to the
            list of tuned frequencies for this comlink.  Up to 5 frequencies
            can be saved at a time.

        |w+comlink/remove <0000-9999>|n - This removes the given frequency
            from the the list of tuned frequencies on the device.

        |w+comlink/encrypt <0000-9999>=<password>|n - Encrypt messages on a
            specific frequency.  Also allows the device to receive encrypted
            message.

        |w+comlink/decrypt <0000-9999>|n - Removes encryption from the
            frequency.  The device will no longer be able to send or receive
            encrypted messages on the specified frequency.

        |w+comlink/broadcast [: or ;]<message>|n - This sends an area-wide
            message across all comlink in your local area.  (i.e. city,
            ship or zone)

        |w+comlink [: or ;]<message>|n - Sends a message to the last sent to
            location. (person or frequency)

        |w+comlink/slice <0000-9999>|n - Attempt to force decryption of the
            messages on a specific frequency.
    """
