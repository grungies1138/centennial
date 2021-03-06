"""
    Comlinks are objects used for IC live, in-game communication between characters.

    Comlinks are made up of connections to Frequencies which inherit from Channel.
    Each frequency cont
"""

from typeclasses.objects import Object
from typeclasses.channels import Channel
from evennia import default_cmds, CmdSet, DefaultScript
from evennia.comms.models import TempMsg, Msg
from evennia.utils import create, evtable, logger
from evennia.comms.channelhandler import CHANNELHANDLER
from evennia.utils.utils import make_iter, inherits_from, lazy_property
from world.languages import translate
import evennia
import re


FREQUENCIES_PER_COMLINK = 5
SCRAMBLED_MESSAGE = "[scrambled message]"


def find_frequency(freq):
    frequencies = Frequency.objects.channel_search(freq)
    if not frequencies:
        return None

    if len(frequencies) > 1:
        return None

    return frequencies[0]


class Frequency(Channel):
    def channel_prefix(self, msg, emit=False):
        return "|=m<|n|045%s|n|=m>|n: " % self.key

    def msg(self, msgobj, header=None, senders=None, sender_strings=None,
            keep_log=None, online=False, emit=False, external=False):
        senders = make_iter(senders) if senders else []
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
                    entity.msg(msgobj.message, from_obj=msgobj.senders,
                               options={"from_channel": self.key, "msgobj": msgobj})
                else:
                    entity.msg("[scrambled message]", from_obj=msgobj.senders,
                               options={"from_channel": self.key, "msgobj": msgobj})
            except AttributeError as e:
                logger.log_trace("%s\nCannot send msg to '%s'." % (e, entity))

        if msgobj.keep_log:
            # log to file
            logger.log_file(msgobj.message, self.attributes.get("log_file") or "channel_%s.log" % self.key)

    def pose_transform(self, msgobj, sender_string):
        """
        Hook method. Detects if the sender is posing, and modifies the
        message accordingly.
        Args:
            msgobj (Msg or TempMsg): The message to analyze for a pose.
            sender_string (str): The name of the sender/poser.
        Returns:
            string (str): A message that combines the `sender_string`
                component with `msg` in different ways depending on if a
                pose was performed or not (this must be analyzed by the
                hook).
        """
        return msgobj.message
        # pose = False
        # message = msgobj.message
        # message_start = message.lstrip()
        # if message_start.startswith((':', ';')):
        #     pose = True
        #     message = message[1:]
        #     if not message.startswith((':', "'", ',')):
        #         if not message.startswith(' '):
        #             message = ' ' + message
        # if pose:
        #     return '%s%s' % (msgobj.senders[0], message)
        # else:
        #     return '%s says, "%s"' % ("Ghost", message)


class ComlinkCmdSet(CmdSet):
    key = "ComlinkCmdSet"

    def at_cmdset_creation(self):
        self.add(ComlinkCmd())


class Comlink(Object):
    def at_object_creation(self):
        self.cmdset.add(ComlinkCmdSet)
        self.db.speaker = False
        self.db.passwords = {}
        self.tags.add("comlink")

    def return_appearance(self, looker):
        return "See: |whelp +comlink|n"

    def at_drop(self, dropper):
        tags = self.tags.get(category="comlink_holder")
        for tag in tags:
            self.tags.remove(tag, category="comlink_holder")

    def at_get(self, getter):
        self.tags.add(getter.key, category="comlink_holder")

    def at_msg_receive(self, text=None, source=None):
        self.message_holder(text)

    def msg(self, text="", from_obj=None, **kwargs):
        if kwargs.get("options"):
            msgobj = kwargs.get("options").get("msgobj")
        else:
            msgobj = None
        if msgobj:
            message = ""
            freq = str(kwargs.get("options").get("from_channel"))
            passwd = self.db.passwords.get(freq) or None
            msg_pass = msgobj.tags.get(category="password") or None
            language = msgobj.tags.get(category="language") or None
            if language:
                if hasattr(self.location, "db.languages"):
                    if language in self.location.db.languages:
                        message = msgobj.message
                    else:
                        message = translate(msgobj.message, language)
            else:
                message = msgobj.message
            if msg_pass:
                if passwd == msg_pass:
                    self.at_msg_receive(text=message)
                else:
                    self.at_msg_receive(text="|=m<|n|045%s|n|=m>|n: %s" % (freq, SCRAMBLED_MESSAGE))
            else:
                self.at_msg_receive(text=message)

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
        if inherits_from(self.location, "typeclasses.characters.Character"):
            if speaker:
                self.location.location.msg_contents(message)
            else:
                self.location.msg(message)

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
            separated list) or frequency selected. |yNOTE:|n the selected frequency must be in the frequency list on
            the comlink device.

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

        if not aelf.args:
            self.caller.msg("See: |whelp +comlink|n")
            return

        if self.switches:
            if "add" in self.switches:
                if not self.args:
                    self.caller.msg(comlink_prefix + "Usage: |w+comlink/add <0000-9999>")
                    return
                if self.parse_freq(self.args):
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
                if self.lhs not in [freq.key for freq in self.obj.frequencies()]:
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
                    password = self.obj.db.passwords.get(freq.key) or None
                    if password:
                        table.add_row(freq.key, password)
                    else:
                        table.add_row(freq.key, '')

                self.caller.msg(unicode(table))
                return

            if "slice" in self.switches:
                self.obj.message_holder("Not yet implemented.")
                return
        else:
            if "=" in self.args:
                msg = Msg(senders=self.obj, message=self.parse_message(self.rhs, self.caller))

                frequency = [freq for freq in self.obj.frequencies() if freq.key == self.lhs] or None

                if frequency:
                    msg.tags.add(self.obj.db.passwords.get(frequency.key), category="password")
                    self.obj.db.last_msg = frequency
                    frequency.msg(msg)
                else:
                    comm = evennia.search_tag(self.lhs, category="comlink_holder")[0] or None
                    if comm:
                        self.obj.db.last_msg = comm
                        comm.msg(msgobj=msg)
                    else:
                        self.caller.msg(comlink_prefix + "No user or Frequency with that name.  Please try again.")
            else:
                msg = Msg(senders=self.obj, message=self.parse_message(self.args, self.caller))

                last = self.obj.db.last_msg

                if last:
                    if last in self.obj.frequencies():
                        msg.tags.add(self.obj.db.passwords.get(last.key), category="password")
                        last.msg(msg)
                    else:
                        last.msg(msg)
                else:
                    self.caller.msg(comlink_prefix + "There is no previously defined Frequency or User.  Please select "
                                                     "the message destination and try again.")

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

    @staticmethod
    def parse_message(message, sender):
        if message[0] == ":":
            return "%s %s" % (sender.key, message[1:])
        elif message[0] == ";":
            return "%s%s" % (sender.key, message[1:])
        else:
            return "%s says, \"%s\"" % (sender.key, message)
