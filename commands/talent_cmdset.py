from evennia import default_cmds, CmdSet
from commands.talent_commands import AimCommand, AnticipateCommand, AssassinateCommand, BombCommand, BombardCommand, \
    BribeCommand, \
    CastigateCommand, CommandCommand, ControlledBurstCommand, ConvinceCommand, CounterCommand, CoverCommand, \
    CoverFireCommand, SnipeCommand, HealCommand, DefuseCommand, DetectCommand, DisarmCommand, DisassembleCommand, \
    DisguiseCommand, DoubleFrontCommand, DrawdownCommand, EludeCommand, FenceCommand, FindCommand, FlurryCommand, \
    FocusedFireCommand, FocusedStrikeCommand, GambitCommand, GatherInfoCommand, GrappleCommand, GuardCommand, \
    HackCommand, HideCommand, HostileTakeoverCommand, InvestCommand, KTaraCommand, LuckyCommand, MedicateCommand, \
    ObserveCommand, OperateCommand, OrderCommand, ParryCommand, PlanningCommand, PrepareCommand, QuickshotCommand, \
    RallyCommand, RebukeCommand, RecoverCommand, RepairCommand, RiposteCommand, RiskyMoveCommand, ShieldCommand, \
    SneakCommand, SnipeCommand, SpotCommand, StealCommand, StrategyCommand, StunCommand, SurgeryCommand, \
    TallowRollCommand, \
    TinkerCommand, TrackCommand, TrickShotCommand, TripwireCommand, BattlemindCommand, ElectricJudgmentCommand, \
    ForceEnlightenmentCommand, ForceHealingCommand, ForceLightCommand


class AimCmdSet(CmdSet):
    key = "AimCmdSet"

    def at_cmdset_creation(self):
        self.add(AimCommand())


class AnticipateCmdSet(CmdSet):
    key = "AnticipateCmdSet"

    def at_cmdset_creation(self):
        self.add(AnticipateCommand())


class AssassinateCmdSet(CmdSet):
    key = "AssassinateCmdSet"

    def at_cmdset_creation(self):
        self.add(AssassinateCommand())


class BombCmdSet(CmdSet):
    key = "BombCmdSet"

    def at_cmdset_creation(self):
        self.add(BombCommand())


class BombardCmdSet(CmdSet):
    key = "BombardCmdSet"

    def at_cmdset_creation(self):
        self.add(BombardCommand())


class BribeCmdSet(CmdSet):
    key = "BribeCmdSet"

    def at_cmdset_creation(self):
        self.add(BribeCommand())


class CastigateCmdSet(CmdSet):
    key = "CastigateCmdSet"

    def at_cmdset_creation(self):
        self.add(CastigateCommand())


class CommandCmdSet(CmdSet):
    key = "CommandCmdSet"

    def at_cmdset_creation(self):
        self.add(CommandCommand())


class ControlledBurstCmdSet(CmdSet):
    key = "ControlledBurstCmdSet"

    def at_cmdset_creation(self):
        self.add(ControlledBurstCommand())


class ConvinceCmdSet(CmdSet):
    key = "ConvinceCmdSet"

    def at_cmdset_creation(self):
        self.add(ConvinceCommand())


class CounterCmdSet(CmdSet):
    key = "ConvinceCmdSet"

    def at_cmdset_creation(self):
        self.add(CounterCommand())


class CoverCmdSet(CmdSet):
    key = "ConvinceCmdSet"

    def at_cmdset_creation(self):
        self.add(CoverCommand())


class CoverFireCmdSet(CmdSet):
    key = "ConvinceCmdSet"

    def at_cmdset_creation(self):
        self.add(CoverFireCommand())


class DefuseCmdSet(CmdSet):
    key = "DefuseCmdSet"

    def at_cmdset_creation(self):
        self.add(DefuseCommand())


class DetectCmdSet(CmdSet):
    key = "DetectCmdSet"

    def at_cmdset_creation(self):
        self.add(DetectCommand())


class DisarmCmdSet(CmdSet):
    key = "DisarmCmdSet"

    def at_cmdset_creation(self):
        self.add(DisarmCommand())


class DisassembleCmdSet(CmdSet):
    key = "DisassembleCmdSet"

    def at_cmdset_creation(self):
        self.add(DisassembleCommand())


class DisguiseCmdSet(CmdSet):
    key = "DisguiseCmdSet"

    def at_cmdset_creation(self):
        self.add(DisguiseCommand())


class DoubleFrontCmdSet(CmdSet):
    key = "DoubleFrontCmdSet"

    def at_cmdset_creation(self):
        self.add(DoubleFrontCommand())


class DrawdownCmdSet(CmdSet):
    key = "DrawdownCmdSet"

    def at_cmdset_creation(self):
        self.add(DrawdownCommand())


class EludeCmdSet(CmdSet):
    key = "EludeCmdSet"

    def at_cmdset_creation(self):
        self.add(EludeCommand())


class FenceCmdSet(CmdSet):
    key = "FenceCmdSet"

    def at_cmdset_creation(self):
        self.add(FenceCommand())


class FindCmdSet(CmdSet):
    key = "FindCmdSet"

    def at_cmdset_creation(self):
        self.add(FindCommand())


class FlurryCmdSet(CmdSet):
    key = "FlurryCmdSet"

    def at_cmdset_creation(self):
        self.add(FlurryCommand())


class FocusedFireCmdSet(CmdSet):
    key = "FocusedFireCmdSet"

    def at_cmdset_creation(self):
        self.add(FocusedFireCommand())


class FocusedStrikeCmdSet(CmdSet):
    key = "FocusedStrikeCmdSet"

    def at_cmdset_creation(self):
        self.add(FocusedStrikeCommand())


class GambitCmdSet(CmdSet):
    key = "GambitCmdSet"

    def at_cmdset_creation(self):
        self.add(GambitCommand())


class GatherInfoCmdSet(CmdSet):
    key = "GatherInfoCmdSet"

    def at_cmdset_creation(self):
        self.add(GatherInfoCommand())


class GrappleCmdSet(CmdSet):
    key = "GrappleCmdSet"

    def at_cmdset_creation(self):
        self.add(GrappleCommand())


class GuardCmdSet(CmdSet):
    key = "GuardCmdSet"

    def at_cmdset_creation(self):
        self.add(GuardCommand())


class HackCmdSet(CmdSet):
    key = "HackCmdSet"

    def at_cmdset_creation(self):
        self.add(HackCommand())


class HideCmdSet(CmdSet):
    key = "HideCmdSet"

    def at_cmdset_creation(self):
        self.add(HideCommand())


class HostileTakeoverCmdSet(CmdSet):
    key = "HostileTakeoverCmdSet"

    def at_cmdset_creation(self):
        self.add(HostileTakeoverCommand())


class InvestCmdSet(CmdSet):
    key = "InvestCmdSet"

    def at_cmdset_creation(self):
        self.add(InvestCommand())


class KTaraCmdSet(CmdSet):
    key = "KTaraCmdSet"

    def at_cmdset_creation(self):
        self.add(KTaraCommand())


class LuckyCmdSet(CmdSet):
    key = "LuckyCmdSet"

    def at_cmdset_creation(self):
        self.add(LuckyCommand())


class MedicateCmdSet(CmdSet):
    key = "MedicateCmdSet"

    def at_cmdset_creation(self):
        self.add(MedicateCommand())


class ObserveCmdSet(CmdSet):
    key = "ObserveCmdSet"

    def at_cmdset_creation(self):
        self.add(ObserveCommand())


class OperateCmdSet(CmdSet):
    key = "OperateCmdSet"

    def at_cmdset_creation(self):
        self.add(OperateCommand())


class OrderCmdSet(CmdSet):
    key = "OrderCmdSet"

    def at_cmdset_creation(self):
        self.add(OrderCommand())


class ParryCmdSet(CmdSet):
    key = "ParryCmdSet"

    def at_cmdset_creation(self):
        self.add(ParryCommand())


class PlanningCmdSet(CmdSet):
    key = "PlanningCmdSet"

    def at_cmdset_creation(self):
        self.add(PlanningCommand())


class PrepareCmdSet(CmdSet):
    key = "PrepareCmdSet"

    def at_cmdset_creation(self):
        self.add(PrepareCommand())


class QuickshotCmdSet(CmdSet):
    key = "QuickshotCmdSet"

    def at_cmdset_creation(self):
        self.add(QuickshotCommand())


class RallyCmdSet(CmdSet):
    key = "RallyCmdSet"

    def at_cmdset_creation(self):
        self.add(RallyCommand())


class RebukeCmdSet(CmdSet):
    key = "RebukeCmdSet"

    def at_cmdset_creation(self):
        self.add(RebukeCommand())


class RecoverCmdSet(CmdSet):
    key = "RecoverCmdSet"

    def at_cmdset_creation(self):
        self.add(RecoverCommand())


class RepairCmdSet(CmdSet):
    key = "RepairCmdSet"

    def at_cmdset_creation(self):
        self.add(RepairCommand())


class RiposteCmdSet(CmdSet):
    key = "RiposteCmdSet"

    def at_cmdset_creation(self):
        self.add(RiposteCommand())


class RiskyMoveCmdSet(CmdSet):
    key = "RiskyMoveCmdSet"

    def at_cmdset_creation(self):
        self.add(RiskyMoveCommand())


class ShieldCmdSet(CmdSet):
    key = "ShieldCmdSet"

    def at_cmdset_creation(self):
        self.add(ShieldCommand())


class SneakCmdSet(CmdSet):
    key = "SneakCmdSet"

    def at_cmdset_creation(self):
        self.add(SneakCommand())


class SnipeCmdSet(CmdSet):
    key = "SnipeCmdSet"

    def at_cmdset_creation(self):
        self.add(SnipeCommand())


class SpotCmdSet(CmdSet):
    key = "SpotCmdSet"

    def at_cmdset_creation(self):
        self.add(SpotCommand())


class StealCmdSet(CmdSet):
    key = "StealCmdSet"

    def at_cmdset_creation(self):
        self.add(StealCommand())


class StrategyCmdSet(CmdSet):
    key = "StrategyCmdSet"

    def at_cmdset_creation(self):
        self.add(StrategyCommand())


class StunCmdSet(CmdSet):
    key = "StunCmdSet"

    def at_cmdset_creation(self):
        self.add(StunCommand())


class SurgeryCmdSet(CmdSet):
    key = "SurgeryCmdSet"

    def at_cmdset_creation(self):
        self.add(SurgeryCommand())


class TallowRollCmdSet(CmdSet):
    key = "TallowRollCmdSet"

    def at_cmdset_creation(self):
        self.add(TallowRollCommand())


class TinkerCmdSet(CmdSet):
    key = "TinkerCmdSet"

    def at_cmdset_creation(self):
        self.add(TinkerCommand())


class TrackCmdSet(CmdSet):
    key = "TrackCmdSet"

    def at_cmdset_creation(self):
        self.add(TrackCommand())


class TrickShotCmdSet(CmdSet):
    key = "TrickShotCmdSet"

    def at_cmdset_creation(self):
        self.add(TrickShotCommand())


class TripwireCmdSet(CmdSet):
    key = "TripwireCmdSet"

    def at_cmdset_creation(self):
        self.add(TripwireCommand())


# Force Talents

class BattlemindCmdSet(CmdSet):
    key = "BattlemindCmdSet"

    def at_cmdset_creation(self):
        self.add(BattlemindCommand())


class ElectricJudgmentCmdSet(CmdSet):
    key = "ElectricJudgmentCmdSet"

    def at_cmdset_creation(self):
        self.add(ElectricJudgmentCommand())


class ForceEnlightenmentCmdSet(CmdSet):
    key = "ForceEnlightenmentCmdSet"

    def at_cmdset_creation(self):
        self.add(ForceEnlightenmentCommand())


class ForceHealingCmdSet(CmdSet):
    key = "ForceHealingCmdSet"

    def at_cmdset_creation(self):
        self.add(ForceHealingCommand())


class ForceLightCmdSet(CmdSet):
    key = "ForceLightCmdSet"

    def at_cmdset_creation(self):
        self.add(ForceLightCommand())
