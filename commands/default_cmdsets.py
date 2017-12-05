"""
Command sets

All commands in the game must be grouped in a cmdset.  A given command
can be part of any number of cmdsets and cmdsets can be added/removed
and merged onto entities at runtime.

To create new commands to populate the cmdset, see
`commands/command.py`.

This module wraps the default command sets of Evennia; overloads them
to add/remove commands from the default lineup. You can create your
own cmdsets by inheriting from them or directly from `evennia.CmdSet`.

"""


from evennia import default_cmds, CmdSet
from commands.command import SheetCommand, CheckCommand, OOCCommand, WhoCommand, CmdInventory, CmdPage, TimeCommand, \
    CmdWield, CmdUnwield, CmdWear, CmdUnwear, CmdRepose
from commands.bbs_commands import CreateBoardCommand, ViewAllBoardsCommand, LockBoardCommand, JoinBoardCommand, \
    ViewBoardsCommand, LeaveBoardCommand, DeleteBoardCommand, AddPostCommand, ReadBoardCommand, AddPostCommentCommand, \
    LikeCommand, DeletePostCommand
from commands.chargen_menu import ChargenMenuCommand
# from commands.vendor_commands import VendorMenuCommand
from commands.job_commands import AddJobCommand
from commands.mail_commands import CmdMail
from evennia.commands.default import help
from commands.org_commands import OrgCommand
from commands.combat_commands import AttackCommand


class ChargenCmdSet(default_cmds.CharacterCmdSet):
    """
    Commands allowed to be used while in the Chargen Menu
    """
    key = "ChargeCmdSet"
    priority = 2

    def at_cmdset_creation(self):
        self.add(SheetCommand())
        self.add(help.CmdHelp())


class CharacterCmdSet(default_cmds.CharacterCmdSet):
    """
    The `CharacterCmdSet` contains general in-game commands like `look`,
    `get`, etc available on in-game Character objects. It is merged with
    the `AccountCmdSet` when an Account puppets a Character.
    """
    key = "DefaultCharacter"

    def at_cmdset_creation(self):
        """
        Populates the cmdset
        """
        super(CharacterCmdSet, self).at_cmdset_creation()
        #
        # any commands you add below will overload the default ones.
        #
        self.add(SheetCommand())
        self.add(CheckCommand())
        self.add(CmdMail())
        self.add(CreateBoardCommand())
        self.add(ViewAllBoardsCommand())
        self.add(LockBoardCommand())
        self.add(JoinBoardCommand())
        self.add(ViewBoardsCommand())
        self.add(LeaveBoardCommand())
        self.add(DeleteBoardCommand())
        self.add(AddPostCommand())
        self.add(ReadBoardCommand())
        self.add(AddPostCommentCommand())
        self.add(DeletePostCommand())
        self.add(ChargenMenuCommand())
        self.add(OOCCommand())
        self.add(LikeCommand())
        self.add(AddJobCommand())
        self.add(CmdInventory())
        self.add(CmdPage())
        self.add(TimeCommand())
        self.add(OrgCommand())
        self.add(AttackCommand())
        self.add(CmdWield())
        self.add(CmdUnwield())
        self.add(CmdWear())
        self.add(CmdUnwear())
        self.add(CmdRepose())


class AccountCmdSet(default_cmds.AccountCmdSet):
    """
    This is the cmdset available to the Account at all times. It is
    combined with the `CharacterCmdSet` when the Account puppets a
    Character. It holds game-account-specific commands, channel
    commands, etc.
    """
    key = "DefaultAccount"

    def at_cmdset_creation(self):
        """
        Populates the cmdset
        """
        super(AccountCmdSet, self).at_cmdset_creation()
        #
        # any commands you add below will overload the default ones.
        #
        self.add(WhoCommand())


class UnloggedinCmdSet(default_cmds.UnloggedinCmdSet):
    """
    Command set available to the Session before being logged in.  This
    holds commands like creating a new account, logging in, etc.
    """
    key = "DefaultUnloggedin"

    def at_cmdset_creation(self):
        """
        Populates the cmdset
        """
        super(UnloggedinCmdSet, self).at_cmdset_creation()
        #
        # any commands you add below will overload the default ones.
        #


class SessionCmdSet(default_cmds.SessionCmdSet):
    """
    This cmdset is made available on Session level once logged in. It
    is empty by default.
    """
    key = "DefaultSession"

    def at_cmdset_creation(self):
        """
        This is the only method defined in a cmdset, called during
        its creation. It should populate the set with command instances.

        As and example we just add the empty base `Command` object.
        It prints some info.
        """
        super(SessionCmdSet, self).at_cmdset_creation()
        #
        # any commands you add below will overload the default ones.
        #
