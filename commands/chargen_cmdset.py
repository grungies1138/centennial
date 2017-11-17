from evennia import CmdSet
from commands import chargen, chargen_menu

class ChargenCmdSet(CmdSet):
    def at_cmdset_creation(self):
        """
        Add the commands from chargen.py
        """
        self.add(chargen.SpecialCommand())
        self.add(chargen.FullnameCommand())
        self.add(chargen.AgeCommand())
        self.add(chargen.FinalizeCommand())

#        self.add(chargen_menu.ChargenMenuCommand())
