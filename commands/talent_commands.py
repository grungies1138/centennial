from evennia import default_cmds


class AimCommand(default_cmds.MuxCommand):
    """
    This command allows you to target a specific area (head, legs, arms, torso, near) for added benefits.
    """

    key = "+aim"
    aliases = []
    locks = "cmd:all()"
    help_category = "General"

    def func(self):
        pass


class AnticipateCommand(default_cmds.MuxCommand):
    """
    Defensive Option that uses your intellect to avoid attacks.
    """

    key = "+anticipate"
    aliases = []
    locks = "cmd.all()"
    help_category = "General"

    def func(self):
        pass


class AssassinateCommand(default_cmds.MuxCommand):
    """
    This command makes a surprise attack against a target from stealth, causing increased damage and having increased accuracy.
    This is an EPIC level talent and its use requires a Destiny Point.

    ** NOTE ** Using tihs command is considered a Dark act and will cause an alignment shift.
    """

    key = "+assassinate"
    aliases = []
    locks = "cmd_all()"
    help_category = "General"

    def func(self):
        pass


class BombCommand(default_cmds.MuxCommand):
    """
    This command allows you to place an explosive at a location or on an object, set to detonate at a specific time.
    """

    key = "+bomb"
    aliases = []
    locks = "cmd_all()"
    help_category = "General"

    def func(self):
        pass


class BombardCommand(default_cmds.MuxCommand):
    """
    This command allows you to use a vehicles weapons to cause massive damage to an adjacent area, hitting all targets there.
    This is an EPIC level talent and its use requires a Destiny Point.
    """

    key = "+bombard"
    aliases = []
    locks = "cmd_all()"
    help_category = "General"

    def func(self):
        pass


class BribeCommand(default_cmds.MuxCommand):
    """
    This command grants access to an NPCs Basic Command Menu even if you do not control the NPC.
    """

    key = "+bribe"
    aliases = []
    locks = "cmd_all()"
    help_category = "General"

    def func(self):
        pass


class CastigateCommand(default_cmds.MuxCommand):
    """
    This command damages the targets ability to fight when successful.
    """

    key = "+castigate"
    aliases = []
    locks = "cmd_all()"
    help_category = "General"

    def func(self):
        pass


class CommandCommand(default_cmds.MuxCommand):
    """
    This command grants access to an NPCs Basic Command Menu even if you do not control the NPC.
    """

    key = "+command"
    aliases = []
    locks = "cmd_all()"
    help_category = "General"

    def func(self):
        pass


class ControlledBurstCommand(default_cmds.MuxCommand):
    """
    This command allows you to target multiple objects (up to three) to attack in your area.
    """

    key = "+controlled burst"
    aliases = []
    locks = "cmd_all()"
    help_category = "General"

    def func(self):
        pass


class ConvinceCommand(default_cmds.MuxCommand):
    """
    This command grants access to an NPCs Advanced Command Menu even if you do not control the NPC.
    This is an EPIC level talent and its use requires a Destiny Point.
    """

    key = "+convince"
    aliases = []
    locks = "cmd_all()"
    help_category = "General"

    def func(self):
        pass


class CounterCommand(default_cmds.MuxCommand):
    """
    Defensive option that attempts to strike back at your opponent after they attack.
    """

    key = "+counter"
    aliases = []
    locks = "cmd_all()"
    help_category = "General"

    def func(self):
        pass


class CoverCommand(default_cmds.MuxCommand):
    """
    Defensive option that attempts to use your survival instincts to hide behind objects.
    """

    key = "+cover"
    aliases = []
    locks = "cmd_all()"
    help_category = "General"

    def func(self):
        pass


class CoverFireCommand(default_cmds.MuxCommand):
    """
    Decreases attack ability of targets (up to 2).
    """

    key = "+cover fire"
    aliases = []
    locks = "cmd_all()"
    help_category = "General"

    def func(self):
        pass


class DefuseCommand(default_cmds.MuxCommand):
    """
    Deactivates a currently activated bomb.
    """

    key = "+defuse"
    aliases = []
    locks = "cmd:all()"
    help_category = "General"

    def func(self):
        pass


class DetectCommand(default_cmds.MuxCommand):
    """
    Lowers the defense of the target substantially
    """

    key = "+detect"
    aliases = []
    locks = "cmd:all()"
    help_category = "General"

    def func(self):
        pass


class DisarmCommand(default_cmds.MuxCommand):
    """
    Successful attack with this talent causes the defender to drop their weapon
    """

    key = "+disarm"
    aliases = []
    locks = "cmd:all()"
    help_category = "General"

    def func(self):
        pass


class DisassembleCommand(default_cmds.MuxCommand):
    """
    Get parts from an item
    """

    key = "+disassemble"
    aliases = []
    locks = "cmd:all()"
    help_category = "General"

    def func(self):
        pass


class DisguiseCommand(default_cmds.MuxCommand):
    """
    Conceal Identity with fake ID/Desc
    """

    key = "disguise"
    aliases = []
    locks = "cmd_all()"
    help_category = "General"

    def func(self):
        pass


class DoubleFrontCommand(default_cmds.MuxCommand):
    """
    Boost ship's shields temporarily
    """

    key = "+double front"
    aliases = []
    locks = "cmd:all()"
    help_category = "General"

    def func(self):
        pass


class DrawdownCommand(default_cmds.MuxCommand):
    """
    Can wield and attack with weapon at same time
    """

    key = "+drawdown"
    aliases = []
    locks = "cmd:all()"
    help_category = "General"

    def func(self):
        pass


class EludeCommand(default_cmds.MuxCommand):
    """
    Auto-Miss on non-epic attacks.Auto
    """

    key = "+elude"
    aliases = []
    locks = "cmd:all()"
    help_category = "General"

    def func(self):
        pass


class FenceCommand(default_cmds.MuxCommand):
    """
    find credits from salvagable parts in an area
    """

    key = "+fence"
    aliases = []
    locks = "cmd:all()"
    help_category = "General"

    def func(self):
        pass


class FindCommand(default_cmds.MuxCommand):
    """
    Gives a more detailed report than 'look'
    """

    key = "+find"
    aliases = []
    locks = "cmd:all()"
    help_category = "General"

    def func(self):
        pass


class FlurryCommand(default_cmds.MuxCommand):
    """
    Massive Endurance Strike, 1/2 on miss
    """

    key = "+flurry"
    aliases = []
    locks = "cmd:all()"
    help_category = "General"

    def func(self):
        pass


class FocusedFireCommand(default_cmds.MuxCommand):
    """
    Target a specific location for added benefits
    """

    key = "+focused fire"
    aliases = []
    locks = "cmd:all()"
    help_category = "General"

    def func(self):
        pass


class FocusedStrikeCommand(default_cmds.MuxCommand):
    """
    Target a specific location for added benefits
    """

    key = "+focused strike"
    aliases = []
    locks = "cmd:all()"
    help_category = "General"

    def func(self):
        pass


class GambitCommand(default_cmds.MuxCommand):
    """
    Defensive Option
    """

    key = "+gambit"
    aliases = []
    locks = "cmd:all()"
    help_category = "General"

    def func(self):
        pass


class GatherInfoCommand(default_cmds.MuxCommand):
    """
    Locate what system or area a target is in
    """

    key = "+gather info"
    aliases = []
    locks = "cmd:all()"
    help_category = "General"

    def func(self):
        pass


class GrappleCommand(default_cmds.MuxCommand):
    """
    Attempt to remove target's weapon
    """

    key = "+grapple"
    aliases = []
    locks = "cmd:all()"
    help_category = "General"

    def func(self):
        pass


class GuardCommand(default_cmds.MuxCommand):
    """
    Defensive Option to take hit for ally
    """

    key = "+guard"
    aliases = []
    locks = "cmd:all()"
    help_category = "General"

    def func(self):
        pass


class HackCommand(default_cmds.MuxCommand):
    """
    Access locked locations/items
    """

    key = "+hack"
    aliases = []
    locks = "cmd:all()"
    help_category = "General"

    def func(self):
        pass


class HealCommand(default_cmds.MuxCommand):
    """
    Access locked locations/items
    """

    key = "+heal"
    aliases = []
    locks = "cmd:all()"
    help_category = "General"

    def func(self):
        pass


class HideCommand(default_cmds.MuxCommand):
    """
    Prevents other PCs from seeing you in a room
    """

    key = "+hide"
    aliases = []
    locks = "cmd:all()"
    help_category = "General"

    def func(self):
        pass


class HostileTakeoverCommand(default_cmds.MuxCommand):
    """
    Ability to take profits from a vendor not owned by the Character
    """

    key = "+hostile takeover"
    aliases = []
    locks = "cmd:all()"
    help_category = "General"

    def func(self):
        pass


class InvestCommand(default_cmds.MuxCommand):
    """
    Increase profits at current location (temp)
    """

    key = "+invest"
    aliases = []
    locks = "cmd:all()"
    help_category = "General"

    def func(self):
        pass


class KTaraCommand(default_cmds.MuxCommand):
    """
    Cannot be defended
    """

    key = "+ktara strike"
    aliases = []
    locks = "cmd:all()"
    help_category = "General"

    def func(self):
        pass


class LuckyCommand(default_cmds.MuxCommand):
    """
    Boost a skill for character
    """

    key = "+lucky"
    aliases = []
    locks = "cmd:all()"
    help_category = "General"

    def func(self):
        pass


class MedicateCommand(default_cmds.MuxCommand):
    """
    Increases HP recovery time
    """

    key = "+medicate"
    aliases = []
    locks = "cmd:all()"
    help_category = "General"

    def func(self):
        pass


class ObserveCommand(default_cmds.MuxCommand):
    """
    Gives a more detailed report than 'look'
    """

    key = "+observe"
    aliases = []
    locks = "cmd:all()"
    help_category = "General"

    def func(self):
        pass


class OperateCommand(default_cmds.MuxCommand):
    """
    Install cybernetic upgrades
    """

    key = "+operate"
    aliases = []
    locks = "cmd:all()"
    help_category = "General"

    def func(self):
        pass


class OrderCommand(default_cmds.MuxCommand):
    """
    Give Access to Command Options for NPCs
    """

    key = "+order"
    aliases = []
    locks = "cmd:all()"
    help_category = "General"

    def func(self):
        pass


class ParryCommand(default_cmds.MuxCommand):
    """
    Defensive Option
    """

    key = "+parry"
    aliases = []
    locks = "cmd:all()"
    help_category = "General"

    def func(self):
        pass


class PlanningCommand(default_cmds.MuxCommand):
    """
    Clears area of traps/bombs and puts in an attack bonus for player list
    """

    key = "+planning"
    aliases = []
    locks = "cmd:all()"
    help_category = "General"

    def func(self):
        pass


class PrepareCommand(default_cmds.MuxCommand):
    """
    Clears area of traps/bombs and puts in a defensive bonus for player list
    """

    key = "+prepare"
    aliases = []
    locks = "cmd:all()"
    help_category = "General"

    def func(self):
        pass


class QuickshotCommand(default_cmds.MuxCommand):
    """
    Defensive Option
    """

    key = "+quickshot"
    aliases = []
    locks = "cmd:all()"
    help_category = "General"

    def func(self):
        pass


class RallyCommand(default_cmds.MuxCommand):
    """
    Recover Endurance for another character
    """

    key = "+rally"
    aliases = []
    locks = "cmd:all()"
    help_category = "General"

    def func(self):
        pass


class RebukeCommand(default_cmds.MuxCommand):
    """
    Give Access to Command Options for Enemy NPCs
    """

    key = "+rebuke"
    aliases = []
    locks = "cmd:all()"
    help_category = "General"

    def func(self):
        pass


class RecoverCommand(default_cmds.MuxCommand):
    """
    Find whole items
    """

    key = "+recover"
    aliases = []
    locks = "cmd:all()"
    help_category = "General"

    def func(self):
        pass


class RepairCommand(default_cmds.MuxCommand):
    """
    Restore lost endurance on item
    """

    key = "+repair"
    aliases = []
    locks = "cmd:all()"
    help_category = "General"

    def func(self):
        pass


class RiposteCommand(default_cmds.MuxCommand):
    """
    Defensive Option: take Damage to counter attack
    """

    key = "+riposte"
    aliases = []
    locks = "cmd:all()"
    help_category = "General"

    def func(self):
        pass


class RiskyMoveCommand(default_cmds.MuxCommand):
    """
   Attacks that do not reach hit level 3 instead do damage to the attacker
    """

    key = "+risky move"
    aliases = []
    locks = "cmd:all()"
    help_category = "General"

    def func(self):
        pass


class ShieldCommand(default_cmds.MuxCommand):
    """
    Defensive Option for Self/Others
    """

    key = "+shield"
    aliases = []
    locks = "cmd:all()"
    help_category = "General"

    def func(self):
        pass


class SneakCommand(default_cmds.MuxCommand):
    """
    May enter a room without an enter message
    """

    key = "+sneak"
    aliases = []
    locks = "cmd:all()"
    help_category = "General"

    def func(self):
        pass


class SnipeCommand(default_cmds.MuxCommand):
    """
    Cannot be defended, shot from adjacent location
    """

    key = "+snipe"
    aliases = []
    locks = "cmd:all()"
    help_category = "General"

    def func(self):
        pass


class SpotCommand(default_cmds.MuxCommand):
    """
    Look into next room
    """

    key = "+spot"
    aliases = []
    locks = "cmd:all()"
    help_category = "General"

    def func(self):
        pass


class StealCommand(default_cmds.MuxCommand):
    """
    Steal Credits/Items from NPCs / PCs
    """

    key = "+steal"
    aliases = []
    locks = "cmd:all()"
    help_category = "General"

    def func(self):
        pass


class StrategyCommand(default_cmds.MuxCommand):
    """
    Boost a skill for another character
    """

    key = "+strategy"
    aliases = []
    locks = "cmd:all()"
    help_category = "General"

    def func(self):
        pass


class StunCommand(default_cmds.MuxCommand):
    """
    Massive Endurance Hit, 1/2 on miss
    """

    key = "+stun"
    aliases = []
    locks = "cmd:all()"
    help_category = "General"

    def func(self):
        pass


class SurgeryCommand(default_cmds.MuxCommand):
    """
    Reduces wound severity
    """

    key = "+surgery"
    aliases = []
    locks = "cmd:all()"
    help_category = "General"

    def func(self):
        pass


class TallowRollCommand(default_cmds.MuxCommand):
    """
    Cannot be defended
    """

    key = "+tallow roll"
    aliases = []
    locks = "cmd:all()"
    help_category = "General"

    def func(self):
        pass


class TinkerCommand(default_cmds.MuxCommand):
    """
    Temporarily increase the quality of Equipment
    """

    key = "+tinker"
    aliases = []
    locks = "cmd:all()"
    help_category = "General"

    def func(self):
        pass


class TrackCommand(default_cmds.MuxCommand):
    """
    Locate what system a target is in
    """

    key = "+track"
    aliases = []
    locks = "cmd:all()"
    help_category = "General"

    def func(self):
        pass


class TrickShotCommand(default_cmds.MuxCommand):
    """
    Cannot be defended
    """

    key = "+trick shot"
    aliases = []
    locks = "cmd:all()"
    help_category = "General"

    def func(self):
        pass


class TripwireCommand(default_cmds.MuxCommand):
    """
    Sets a bomb at the current location to detonate when a specific individual (or list of people) enters.
    """

    key = "+tripwire"
    aliases = []
    locks = "cmd:all()"
    help_category = "General"

    def func(self):
        pass


# Force Talents

class BattlemindCommand(default_cmds.MuxCommand):
    """
    Temporarily increases attack values of self and allies.
    """

    key = "+battlemind"
    aliases = []
    locks = "cmd.all()"
    help_category = "General"

    def func(self):
        pass


class ElectricJudgmentCommand(default_cmds.MuxCommand):
    """
    Deals Hit Point damage and significant endurance damage to target.
    """

    key = "+electric judgment"
    aliases = []
    locks = "cmd.all()"
    help_category = "General"

    def func(self):
        pass


class ForceEnlightenmentCommand(default_cmds.MuxCommand):
    """
    Recovers endurance for target.
    """

    key = "+force enlightenment"
    aliases = []
    locks = "cmd.all()"
    help_category = "General"

    def func(self):
        pass


class ForceHealingCommand(default_cmds.MuxCommand):
    """
    Recovers hit points for target.
    """

    key = "+force healing"
    aliases = []
    locks = "cmd.all()"
    help_category = "General"

    def func(self):
        pass


class ForceLightCommand(default_cmds.MuxCommand):
    """
    Deals massive damage to a target with a dark alignment.
    """

    key = "+force light"
    aliases = []
    locks = "cmd.all()"
    help_category = "General"

    def func(self):
        pass
