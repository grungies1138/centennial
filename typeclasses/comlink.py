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
from evennia.utils import logger
from evennia.utils.utils import make_iter
import re


FREQUENCIES_PER_COMLINK = 5


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

    def msg(self, msgobj, header=None, senders=None, sender_strings=None,
            keep_log=None, online=False, emit=False, external=False):
        """
       Send the given message to all accounts connected to channel. Note that
       no permission-checking is done here; it is assumed to have been
       done before calling this method. The optional keywords are not used if
       persistent is False.
       Args:
           msgobj (Msg, TempMsg or str): If a Msg/TempMsg, the remaining
               keywords will be ignored (since the Msg/TempMsg object already
               has all the data). If a string, this will either be sent as-is
               (if persistent=False) or it will be used together with `header`
               and `senders` keywords to create a Msg instance on the fly.
           header (str, optional): A header for building the message.
           senders (Object, Account or list, optional): Optional if persistent=False, used
               to build senders for the message.
           sender_strings (list, optional): Name strings of senders. Used for external
               connections where the sender is not an account or object.
               When this is defined, external will be assumed.
           keep_log (bool or None, optional): This allows to temporarily change the logging status of
               this channel message. If `None`, the Channel's `keep_log` Attribute will
               be used. If `True` or `False`, that logging status will be used for this
               message only (note that for unlogged channels, a `True` value here will
               create a new log file only for this message).
           online (bool, optional) - If this is set true, only messages people who are
               online. Otherwise, messages all accounts connected. This can
               make things faster, but may not trigger listeners on accounts
               that are offline.
           emit (bool, optional) - Signals to the message formatter that this message is
               not to be directly associated with a name.
           external (bool, optional): Treat this message as being
               agnostic of its sender.
       Returns:
           success (bool): Returns `True` if message sending was
               successful, `False` otherwise.
       """
        senders = make_iter(senders) if senders else []
        if isinstance(msgobj, basestring):
            # given msgobj is a string - convert to msgobject (always TempMsg)
            if senders and hasattr(senders[0], "db"):
                __channel_passwords = senders[0].db.__channel_passwords
                if type(__channel_passwords) is dict:
                    # password = __channel_passwords.get(self)
                    # lockstring = "read:decrypt({})".format(password) if password else "read:true()"

            msgobj = TempMsg(senders=senders, header=header, message=msgobj, channels=[self],
                             lockstring=lockstring or "read:true()")
        # we store the logging setting for use in distribute_message()
        msgobj.keep_log = keep_log if keep_log is not None else self.db.keep_log

        # start the sending
        msgobj = self.pre_send_message(msgobj)
        if not msgobj:
            return False
        msgobj = self.message_transform(msgobj, emit=emit,
                                        sender_strings=sender_strings,
                                        external=external)
        self.distribute_message(msgobj, online=online)
        self.post_send_message(msgobj)
        return True

    def distribute_message(self, msgobj, online=False, **kwargs):
        """
       Method for grabbing all listeners that a message should be
       sent to on this channel, and sending them a message.
       Args:
           msgobj (Msg or TempMsg): Message to distribute.
           online (bool): Only send to receivers who are actually online
               (not currently used):
           **kwargs (dict): Arbitrary, optional arguments for users
               overriding the call (unused by default).
       Notes:
           This is also where logging happens, if enabled.
       """
        # get all accounts or objects connected to this channel and send to them
        if online:
            subs = self.subscriptions.online()
        else:
            subs = self.subscriptions.all()
        for entity in subs:
            # if the entity is muted, we don't send them a message
            if entity in self.mutelist:
                continue
            try:
                # note our addition of the from_channel keyword here. This could be checked
                # by a custom account.msg() to treat channel-receives differently.
                if msgobj.access(entity, "read"):
                    entity.msg(msgobj.message, from_obj=msgobj.senders, options={"from_channel": self.id})
                else:
                    entity.msg("[scrambled message]", from_obj=msgobj.senders, options={"from_channel": self.id})
            except AttributeError as e:
                logger.log_trace("%s\nCannot send msg to '%s'." % (e, entity))

        if msgobj.keep_log:
            # log to file
            logger.log_file(msgobj.message, self.attributes.get("log_file") or "channel_%s.log" % self.key)


class ComlinkCmdSet(CmdSet):
    key = "ComlinkCmdSet"

    def at_cmdset_creation(self):
        self.add(ComlinkCmd())


class Comlink(Object):
    def at_object_creation(self):
        self.cmdset.add(ComlinkCmdSet)
        self.db.speaker = False
        self.db.passwords = {}

    def at_msg_receive(self, text=None, source=None):
        self.message_holder(text)

    def frequencies(self):
        return [freq for freq in Frequency.objects.all() if self in freq.subscriptions.all()]

    def add_frequency(self, freq):
        if len(self.frequencies()) < FREQUENCIES_PER_COMLINK:
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
        if self.obj.location is Character:
            if speaker:
                self.obj.location.location.msg_contents(prefix + message)
            else:
                self.obj.location.msg(prefix + message)

    def encrypt(self, freq, password):
        frequency = find_frequency(freq)

        if frequency:
            if frequency in self.frequencies():
                self.obj.db.passwords.append({"frequency": freq, "password": password})
            else:
                self.message_holder("That frequency is not saved on your comlink.")
        else:
            self.message_holder("There was a problem setting a password on that frequency.  Contact a staff member.")

    def decrypt(self, freq):
        frequency = [fq for fq in self.obj.db.passwords if fq.get("frequency") == freq]

        if frequency:
            self.obj.db.password.remove(frequency)
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

        |w+comlink/broadcast [: or ;]<message>|n - This sends an area-wide
            message across all comlinks in your current zone.

        |w+comlink [: or ;]<message>|n - Sends a message to the last sent to
            location. (person or frequency)

        |w+comlink/add <0000-9999>|n - This adds the given frequency
            to the list of tuned frequencies for this comlink.  Up to 5
            frequencies can be saved at a time.

        |w+comlink/remove <0000-9999>|n - This removes the given frequency
            from the the list of tuned frequencies on the device.

        |w+comlink/encrypt <0000-9999>=<password>|n - Encrypt messages on a
            specific frequency.  Also allows the device to receive encrypted
            message.

        |w+comlink/decrypt <0000-9999>|n - Removes encryption from the
            frequency.  The device will no longer be able to send or receive
            encrypted messages on the specified frequency.

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
                if not self.args or "=" not in self.args:
                    self.caller.msg(comlink_prefix + "Usage: |w+comlink/encrypt <0000-9999>=<password>|n")
                    return
                if self.lhs not in self.obj.frequencies:
                    self.caller.msg(comlink_prefix + "That frequency is not added to this Comlink.  Please add it "
                                                     "before encrypting.")
                    return
                if self.parse_freq(self.lhs):
                    self.obj.db.passwords[self.lhs] = self.rhs
                    self.caller.msg(comlink_prefix + "Frequency encrypted successfully.")
            if "decrypt" in self.switches:
                if not self.args:
                    self.caller.msg(comlink_prefix + "Usage: |w+comlink/decrypt <0000-9999>|n")
                    return
                if self.args not in self.obj.db.passwords.keys():
                    self.caller.msg(comlink_prefix + "That frequency is not encrypted.")
                    return
                if self.parse_freq(self.args):
                    self.obj.decrypt(self.args)
                    return
            if "broadcast" in self.switches:
                pass
            if "list" in self.switches:
                table = evtable.EvTable("Frequency:", "Password:", border="header", header_line_char="-")
                table.reformat_column(0, width=12)
                for freq in self.obj.frequencies():
                    password = [pwd for pwd in self.obj.db.passwords if freq.get("password")]
                    if password:
                        table.add_row(freq.key, password[0])
                    else:
                        table.add_row(freq.key, '')

                self.caller.msg(unicode(table))
                return

            if "slice" in self.switches:
                self.obj.message_holder("Not yet implemented.")
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
