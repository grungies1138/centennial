"""
In-Game Mail system
Evennia Contribution - grungies1138 2016
A simple Brandymail style @mail system that uses the Msg class from Evennia Core.
Installation:
    import MailCommand from this module into the default Player or Character command set
"""

from evennia import default_cmds, search_object
from evennia.utils import create, utils, evtable, evform
from evennia.comms.models import Msg


_HEAD_CHAR = "|015-|n"
_SUB_HEAD_CHAR = "-"
_WIDTH = 78


class CmdMail(default_cmds.MuxCommand):
    """
    Commands that allow either IC or OOC communications
    Usage:
        @mail       - Displays all the mail a player has in their mailbox
        @mail <#>   - Displays a specific message
        @mail <players>=<subject>/<message>
                - Sends a message to the comma separated list of players.
        @mail/delete <#> - Deletes a specific message
        @mail/forward <player list>=<#>[/<Message>]
                - Forwards an existing message to the specified list of players,
                  original message is delivered with optional Message prepended.
        @mail/reply <#>=<message>
                - Replies to a message #.  Prepends message to the original
                  message text.
    Switches:
        delete  - deletes a message
        forward - forward a received message to another object with an optional message attached.
        reply   - Replies to a received message, appending the original message to the bottom.
    Examples:
        @mail 2
        @mail Griatch=New mail/Hey man, I am sending you a message!
        @mail/delete 6
        @mail/forward feend78 Griatch=You guys should read this.
        @mail/reply 9=Thanks for the info!
    """
    key = "@mail"
    aliases = ["mail"]
    lock = "cmd:all()"
    help_category = "General"
    player_caller = True
    character_mail = True

    def func(self):
        caller = self.get_caller()
        subject = ""
        body = ""
        if self.switches or self.args:
            if "delete" in self.switches:
                try:
                    if not self.lhs:
                        caller.msg("No Message ID given.  Unable to delete.")
                        return
                    else:
                        if self.get_all_mail()[int(self.lhs) - 1]:
                            self.get_all_mail()[int(self.lhs) - 1].delete()
                            caller.msg("Message %s deleted" % self.lhs)
                        else:
                            caller.msg("That message does not exist.")
                            return
                except ValueError:
                    caller.msg("Usage: @mail/delete <message ID>")
            elif "forward" in self.switches:
                try:
                    if not self.rhs:
                        caller.msg("Cannot forward a message without a player list.  Please try again.")
                        return
                    elif not self.lhs:
                        caller.msg("You must define a message to forward.")
                        return
                    else:
                        if "/" in self.rhs:
                            message_number, message = self.rhs.split("/")
                            if self.get_all_mail()[int(message_number) - 1]:
                                old_message = self.get_all_mail()[int(message_number) - 1]

                                self.send_mail(self.lhslist, "FWD: " + old_message.header,
                                               message + "\n---- Original Message ----\n" + old_message.message,
                                               caller)
                                caller.msg("Message forwarded.")
                            else:
                                caller.msg("Message does not exist.")
                                return
                        else:
                            if self.get_all_mail()[int(self.rhs) - 1]:
                                old_message = self.get_all_mail()[int(self.rhs) - 1]
                                self.send_mail(self.lhslist, "FWD: " + old_message.header,
                                               "\n---- Original Message ----\n" + old_message.message, caller)
                                caller.msg("Message forwarded.")
                                old_message.tags.remove("u", category="mail")
                                old_message.tags.add("f", category="mail")
                            else:
                                caller.msg("Message does not exist.")
                                return
                except ValueError:
                    caller.msg("Usage: @mail/forward <player list>=<#>[/<Message>]")
            elif "reply" in self.switches:
                try:
                    if not self.rhs:
                        caller.msg("You must define a message to reply to.")
                        return
                    elif not self.lhs:
                        caller.msg("You must supply a reply message")
                        return
                    else:
                        if self.get_all_mail()[int(self.lhs) - 1]:
                            old_message = self.get_all_mail()[int(self.lhs) - 1]
                            self.send_mail(old_message.senders, "RE: " + old_message.header,
                                           self.rhs + "\n---- Original Message ----\n" + old_message.message,
                                           caller)
                            old_message.tags.remove("u", category="mail")
                            old_message.tags.add("r", category="mail")
                            return
                        else:
                            caller.msg("Message does not exist.")
                            return
                except ValueError:
                    caller.msg("Usage: @mail/reply <#>=<message>")
            else:
                if self.rhs:
                    if "/" in self.rhs:
                        subject, body = self.rhs.split("/", 1)
                    else:
                        body = self.rhs
                    self.send_mail(self.lhslist, subject, body, caller)
                else:
                    message = self.get_all_mail()[int(self.lhs) - 1]

                    messageForm = []
                    if message:
                        messageForm.append(_HEAD_CHAR * _WIDTH)
                        messageForm.append("|wFrom:|n %s" % message.senders[0].key)
                        messageForm.append("|wSent:|n %s" % message.db_date_created.strftime("%m/%d/%Y %H:%M:%S"))
                        messageForm.append("|wSubject:|n %s" % message.header)
                        messageForm.append(_SUB_HEAD_CHAR * _WIDTH)
                        messageForm.append(message.message)
                        messageForm.append(_HEAD_CHAR * _WIDTH)
                    caller.msg("\n".join(messageForm))
                    message.tags.remove("u", category="mail")
                    message.tags.add("o", category="mail")

        else:
            messages = self.get_all_mail()

            if messages:
                table = evtable.EvTable("|wID:|n", "|wFrom:|n", "|wSubject:|n", "|wDate:|n", "|wSta:|n",
                                        table=None, border="header", header_line_char=_SUB_HEAD_CHAR, width=_WIDTH)
                index = 1
                for message in messages:
                    table.add_row(index, message.senders[0], message.header,
                                  message.db_date_created.strftime("%m/%d/%Y"),
                                  str(message.db_tags.last().db_key.upper()))
                    index += 1

                table.reformat_column(0, width=6)
                table.reformat_column(1, width=17)
                table.reformat_column(2, width=34)
                table.reformat_column(3, width=13)
                table.reformat_column(4, width=7)

                caller.msg(_HEAD_CHAR * _WIDTH)
                caller.msg(table)
                caller.msg(_HEAD_CHAR * _WIDTH)
            else:
                caller.msg("Sorry, you don't have any messages.")

    def get_all_mail(self):
        """
        Returns a list of all the messages where the caller is a recipient.
        Returns:
            messages (list): list of Msg objects.
        """
        # mail_messages = Msg.objects.get_by_tag(category="mail")
        # messages = []

        caller = self.get_caller()
        messages = []
        if self.character_mail:
            messages = Msg.objects.get_by_tag(category="mail", raw_queryset=True).filter(db_receivers_players=caller.player)
        else:
            messages = Msg.objects.get_by_tag(category="mail", raw_queryset=True).filter(db_receivers_players=caller)
        return messages

    def send_mail(self, recipients, subject, message, caller):
        """
        Function for sending new mail.  Also useful for sending notifications from objects or systems.
        Args:
            recipients (list): list of Player or character objects to receive the newly created mails.
            subject (str): The header or subject of the message to be delivered.
            message (str): The body of the message being sent.
            caller (obj): The object (or Player or Character) that is sending the message.
        """
        recobjs = []
        if self.character_mail:
            for char in recipients:
                if caller.player.search(char) is not None:
                    recobjs.append(caller.player.search(char))
        else:
            for char in recipients:
                if caller.search(char) is not None:
                    recobjs.append(caller.search(char))

        print(str(recobjs))
        if recobjs:
            lock_string = ""
            for recipient in recobjs:
                recipient.msg("You have received a new @mail from %s" % caller)

                new_message = create.create_message(caller, message, receivers=recipient, header=subject)
                new_message.tags.add("U", category="mail")

            caller.msg("You sent a your message.")
            return
        else:
            caller.msg("No valid players found.  Cannot send message.")
            return


    def get_caller(self):
        caller = None
        if self.character_mail:
            caller = self.character
        else:
            caller = self.caller
        return caller