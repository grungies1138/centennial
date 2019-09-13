"""
Talents are divided into several types

Passive Talents
    talent format : {<talent name>:
                        {"requirements":
                            {"skills":
                                {[<skill>: <min_level>, ...]},
                            "talents":
                                {[<talent>, ...]}

                            }
                        }
                    }

Active Talents
    talent format : {<talent name>:
                        {"requirements":
                            {"skills":
                                {[<skill>: <min_level>, ...]}
                            "talents":
                                {[<talent>, ...]}
                            },
                        "command":
                            "<commandset path>"
                        }
                    }

Force Talents
     talent format : {<talent name>:
                        {"requirements":
                            {"skills":
                                {[<skill>: <min_level>, ...]}
                            "talents":
                                {[<talent>, ...]}
                            },
                        "command":
                            "<commandset path>"
                        }
                    }
"""
BASE_SKILL_MIN = 1
EPIC_SKILL_MIN = 75

BASE_SKILL_LEVEL1 = 5
BASE_SKILL_LEVEL2 = 15
BASE_SKILL_LEVEL3 = 20

FORCE_TIER_1 = 1
FORCE_TIER_2 = 50
FORCE_TIER_3 = 100

PASSIVE_TALENTS = {
    "athletics 1": {"requirements": {"skills": {"athletics": 1}}, "boost": {"athletics": BASE_SKILL_LEVEL1}},
    "athletics 2": {"requirements": {"talent": "athletics 1"}, "boost": {"athletics": BASE_SKILL_LEVEL2}},
    "athletics 3": {"requirements": {"talent": "athletics 2"}, "boost": {"athletics": BASE_SKILL_LEVEL3}},
    "business 1": {"requirements": {"skills": {"business": 1}}, "boost": {"business": BASE_SKILL_LEVEL1}},
    "business 2": {"requirements": {"talent": "business 1"}, "boost": {"business": BASE_SKILL_LEVEL2}},
    "business 3": {"requirements": {"talent": "business 2"}, "boost": {"business": BASE_SKILL_LEVEL3}},
    "command 1": {"requirements": {"skills": {"command": 1}}, "boost": {"command": BASE_SKILL_LEVEL1}},
    "command 2": {"requirements": {"talent": "command 1"}, "boost": {"command": BASE_SKILL_LEVEL2}},
    "command 3": {"requirements": {"talent": "command 2"}, "boost": {"command": BASE_SKILL_LEVEL3}},
    "dodge 1": {"requirements": {"skills": {"dodge": 1}}, "boost": {"dodge": BASE_SKILL_LEVEL1}},
    "dodge 2": {"requirements": {"talent": "dodge 1"}, "boost": {"dodge": BASE_SKILL_LEVEL2}},
    "dodge 3": {"requirements": {"talent": "dodge 2"}, "boost": {"dodge": BASE_SKILL_LEVEL3}},
    "explosives 1": {"requirements": {"skills": {"explosives": 1}}, "boost": {"explosives": BASE_SKILL_LEVEL1}},
    "explosives 2": {"requirements": {"talent": "explosives 1"}, "boost": {"explosives": BASE_SKILL_LEVEL2}},
    "explosives 3": {"requirements": {"talent": "explosives 2"}, "boost": {"explosives": BASE_SKILL_LEVEL3}},
    "firearms 1": {"requirements": {"skills": {"firearms": 1}}, "boost": {"firearms": BASE_SKILL_LEVEL1}},
    "firearms 2": {"requirements": {"talent": "firearms 1"}, "boost": {"firearms": BASE_SKILL_LEVEL2}},
    "firearms 3": {"requirements": {"talent": "firearms 2"}, "boost": {"firearms": BASE_SKILL_LEVEL3}},
    "gambling 1": {"requirements": {"skills": {"gambling": 1}}, "boost": {"gambling": BASE_SKILL_LEVEL1}},
    "gambling 2": {"requirements": {"talent": "gambling 1"}, "boost": {"gambling": BASE_SKILL_LEVEL2}},
    "gambling 3": {"requirements": {"talent": "gambling 2"}, "boost": {"gambling": BASE_SKILL_LEVEL3}},
    "heavy weapons 1": {"requirements": {"skills": {"heavy weapons": 1}},
                        "boost": {"heavy weapons": BASE_SKILL_LEVEL1}},
    "heavy weapons 2": {"requirements": {"heavy weapons": "business 1"}, "boost": {"heavy weapons": BASE_SKILL_LEVEL2}},
    "heavy weapons 3": {"requirements": {"talent": "heavy weapons 2"}, "boost": {"heavy weapons": BASE_SKILL_LEVEL3}},
    "influence 1": {"requirements": {"skills": {"influence": 1}}, "boost": {"influence": BASE_SKILL_LEVEL1}},
    "influence 2": {"requirements": {"talent": "influence 1"}, "boost": {"influence": BASE_SKILL_LEVEL2}},
    "influence 3": {"requirements": {"talent": "influence 2"}, "boost": {"influence": BASE_SKILL_LEVEL3}},
    "intellect 1": {"requirements": {"skills": {"intellect": 1}}, "boost": {"intellect": BASE_SKILL_LEVEL1}},
    "intellect 2": {"requirements": {"talent": "intellect 1"}, "boost": {"intellect": BASE_SKILL_LEVEL2}},
    "intellect 3": {"requirements": {"talent": "intellect 2"}, "boost": {"intellect": BASE_SKILL_LEVEL3}},
    "mechanical 1": {"requirements": {"skills": {"mechanical": 1}}, "boost": {"mechanical": BASE_SKILL_LEVEL1}},
    "mechanical 2": {"requirements": {"talent": "mechanical 1"}, "boost": {"mechanical": BASE_SKILL_LEVEL2}},
    "mechanical 3": {"requirements": {"talent": "mechanical 2"}, "boost": {"mechanical": BASE_SKILL_LEVEL3}},
    "medicine 1": {"requirements": {"skills": {"medicine": 1}}, "boost": {"medicine": BASE_SKILL_LEVEL1}},
    "medicine 2": {"requirements": {"talent": "medicine 1"}, "boost": {"medicine": BASE_SKILL_LEVEL2}},
    "medicine 3": {"requirements": {"talent": "medicine 2"}, "boost": {"medicine": BASE_SKILL_LEVEL3}},
    "melee 1": {"requirements": {"skills": {"melee": 1}}, "boost": {"melee": BASE_SKILL_LEVEL1}},
    "melee 2": {"requirements": {"talent": "melee 1"}, "boost": {"melee": BASE_SKILL_LEVEL2}},
    "melee 3": {"requirements": {"talent": "melee 2"}, "boost": {"melee": BASE_SKILL_LEVEL3}},
    "perception 1": {"requirements": {"skills": {"perception": 1}}, "boost": {"perception": BASE_SKILL_LEVEL1}},
    "perception 2": {"requirements": {"talent": "perception 1"}, "boost": {"perception": BASE_SKILL_LEVEL2}},
    "perception 3": {"requirements": {"talent": "perception 2"}, "boost": {"perception": BASE_SKILL_LEVEL3}},
    "piloting 1": {"requirements": {"skills": {"piloting": 1}}, "boost": {"piloting": BASE_SKILL_LEVEL1}},
    "piloting 2": {"requirements": {"talent": "piloting 1"}, "boost": {"piloting": BASE_SKILL_LEVEL2}},
    "piloting 3": {"requirements": {"talent": "piloting 2"}, "boost": {"piloting": BASE_SKILL_LEVEL3}},
    "quickdraw 1": {"requirements": {"skills": {"quickdraw": 1}}, "boost": {"quickdraw": BASE_SKILL_LEVEL1}},
    "quickdraw 2": {"requirements": {"talent": "quickdraw 1"}, "boost": {"quickdraw": BASE_SKILL_LEVEL2}},
    "quickdraw 3": {"requirements": {"talent": "quickdraw 2"}, "boost": {"quickdraw": BASE_SKILL_LEVEL3}},
    "salvage 1": {"requirements": {"skills": {"salvage": 1}}, "boost": {"salvage": BASE_SKILL_LEVEL1}},
    "salvage 2": {"requirements": {"talent": "salvage 1"}, "boost": {"salvage": BASE_SKILL_LEVEL2}},
    "salvage 3": {"requirements": {"talent": "salvage 2"}, "boost": {"salvage": BASE_SKILL_LEVEL3}},
    "security 1": {"requirements": {"skills": {"security": 1}}, "boost": {"security": BASE_SKILL_LEVEL1}},
    "security 2": {"requirements": {"talent": "security 1"}, "boost": {"security": BASE_SKILL_LEVEL2}},
    "security 3": {"requirements": {"talent": "security 2"}, "boost": {"security": BASE_SKILL_LEVEL3}},
    "stealth 1": {"requirements": {"skills": {"stealth": 1}}, "boost": {"stealth": BASE_SKILL_LEVEL1}},
    "stealth 2": {"requirements": {"talent": "stealth 1"}, "boost": {"stealth": BASE_SKILL_LEVEL2}},
    "stealth 3": {"requirements": {"talent": "stealth 2"}, "boost": {"stealth": BASE_SKILL_LEVEL3}},
    "streetwise 1": {"requirements": {"skills": {"streetwise": 1}}, "boost": {"streetwise": BASE_SKILL_LEVEL1}},
    "streetwise 2": {"requirements": {"talent": "streetwise 1"}, "boost": {"streetwise": BASE_SKILL_LEVEL2}},
    "streetwise 3": {"requirements": {"talent": "streetwise 2"}, "boost": {"streetwise": BASE_SKILL_LEVEL3}},
    "survival 1": {"requirements": {"skills": {"survival": 1}}, "boost": {"survival": BASE_SKILL_LEVEL1}},
    "survival 2": {"requirements": {"talent": "survival 1"}, "boost": {"survival": BASE_SKILL_LEVEL2}},
    "survival 3": {"requirements": {"talent": "survival 2"}, "boost": {"survival": BASE_SKILL_LEVEL3}}
    }

ACTIVE_TALENTS = {
    "aim": {"requirements": {"skills": {"firearms": BASE_SKILL_MIN}}, "command": "commands.talent_cmdset.AimCmdSet"},
    "anticipate": {"requirements": {"skills": {"intellect": BASE_SKILL_MIN}},
                   "command": "commands.talent_cmdset.AnticipateCmdSet"},
    "assassinate": {"requirements": {"skills": {"stealth": EPIC_SKILL_MIN}},
                    "command": "commands.talent_cmdset.AssassinateCmdSet", "dark": 1},
    "bomb": {"requirements": {"skills": {"explosives": BASE_SKILL_MIN}},
             "command": "commands.talent_cmdset.BombCmdSet"},
    "bombard": {"requirements": {"skills": {"heavy weapons": EPIC_SKILL_MIN}},
                "command": "commands.talent_cmdset.BombardCmdSet"},
    "bribe": {"requirements": {"skills": {"business": BASE_SKILL_MIN}},
              "command": "commands.talent_cmdset.BribeCmdSet"},
    "castigate": {"requirements": {"skills": {"command": BASE_SKILL_MIN}},
                  "command": "commands.talent_cmdset.CastigateCmdSet"},
    "command": {"requirements": {"skills": {"command": BASE_SKILL_MIN}},
                "command": "commands.talent_cmdset.CommandCmdSet"},
    "controlled burst": {"requirements": {"skills": {"heavy weapons": BASE_SKILL_MIN}},
                         "command": "commands.talent_cmdset.ControlledBurstCmdSet"},
    "convince": {"requirements": {"skills": {"influence": EPIC_SKILL_MIN}},
                 "command": "commands.talent_cmdset.ConvinceCmdSet"},
    "counter": {"requirements": {"skills": {"athletics": BASE_SKILL_MIN}},
                "command": "commands.talent_cmdset.CounterCmdSet"},  # granite or tile?
    "cover": {"requirements": {"skills": {"survival": BASE_SKILL_MIN}},
              "command": "commands.talent_cmdset.CoverCmdSet"},
    "cover fire": {"requirements": {"skills": {"heavy weapons": BASE_SKILL_MIN}},
                   "command": "commands.talent_cmdset.CoverFireCmdSet"},
    "defuse": {"requirements": {"skills": {"explosives": BASE_SKILL_MIN}},
               "command": "commands.talent_cmdset.DefuseCmdSet"},
    "detect": {"requirements": {"skills": {"perception": EPIC_SKILL_MIN}},
               "command": "commands.talent_cmdset.DetectCmdSet"},
    "disarm": {"requirements": {"skills": {"melee": EPIC_SKILL_MIN}}, "command": "commands.talent_cmdset.DisarmCmdSet"},
    "disassemble": {"requirements": {"skills": {"salvage": BASE_SKILL_MIN}},
                    "command": "commands.talent_cmdset.DisassembleCmdSet"},  # No Disassemble Stephanie!
    "disguise": {"requirements": {"skills": {"streetwise": BASE_SKILL_MIN}},
                 "command": "command.talent_cmdset.DisguiseCmdSet"},
    "double front": {"requirements": {"skills": {"piloting": BASE_SKILL_MIN}},
                     "command": "commands.talent_cmdset.DoubleFrontCmdSet"},
    "drawdown": {"requirements": {"skills": {"quickdraw": BASE_SKILL_MIN}},
                 "command": "commands.talent_cmdset.DrawdownCmdSet"},
    "elude": {"requirements": {"skills": {"dodge": EPIC_SKILL_MIN}}, "command": "commands.talent_cmdset.EludeCmdSet"},
    "fence": {"requirements": {"skills": {"salvage": BASE_SKILL_MIN}}, "command": "commands.talent_cmdset.FenceCmdSet"},
    "find": {"requirements": {"skills": {"perception": BASE_SKILL_MIN}},
             "command": "commands.talent_cmdset.FindCmdSet"},
    "flurry": {"requirements": {"skills": {"athletics": BASE_SKILL_MIN}},
               "command": "commands.talent_cmdset.FlurryCmdSet"},
    "focused fire": {"requirements": {"skills": {"piloting": BASE_SKILL_MIN}},
                     "command": "commands.talent_cmdset.FocusedFireCmdSet"},
    "focused strike": {"requirements": {"skills": {"athletics": BASE_SKILL_MIN}},
                       "command": "commands.talent_cmdset.FocusedStrikeCmdSet"},
    "gambit": {"requirements": {"skills": {"gambling": BASE_SKILL_MIN}},
               "command": "commands.talent_cmdset.GambitCmdSet"},
    "gather info": {"requirements": {"skills": {"streetwise": BASE_SKILL_MIN}},
                    "command": "commands.talent_cmdset.GatherInfoCmdSet"},
    "grapple": {"requirements": {"skills": {"dodge": BASE_SKILL_MIN}},
                "command": "commands.talent_cmdset.GrappleCmdSet"},
    "guard": {"requirements": {"skills": {"security": BASE_SKILL_MIN}},
              "command": "commands.talent_cmdset.GuardCmdSet"},
    "hack": {"requirements": {"skills": {"security": EPIC_SKILL_MIN}}, "command": "commands.talent_cmdset.HackCmdSet"},
    "hide": {"requirements": {"skills": {"stealth": BASE_SKILL_MIN}}, "command": "commands.talent_cmdset.HideCmdSet"},
    "hostile takeover": {"requirements": {"skills": {"buisness": EPIC_SKILL_MIN}},
                         "command": "commands.talent_cmdset.HostileTakeoverCmdSet"},
    "invest": {"requirements": {"skills": {"buisness": BASE_SKILL_MIN}},
               "command": "commands.talent_cmdset.InvestCmdSet"},
    "ktara strike": {"requirements": {"skills": {"athletics": EPIC_SKILL_MIN}},
                     "command": "commands.talent_cmdset.KTaraCmdSet"},
    "lucky": {"requirements": {"skills": {"gambling": BASE_SKILL_MIN}},
              "command": "commands.talent_cmdset.LuckyCmdSet"},
    "medicate": {"requirements": {"skills": {"medicine": BASE_SKILL_MIN}},
                 "command": "commands.talent_cmdset.MedicateCmdSet"},
    "observe": {"requirements": {"skills": {"security": BASE_SKILL_MIN}},
                "command": "commands.talent_cmdset.ObserveCmdSet"},
    "operate": {"requirements": {"skills": {"medicine": EPIC_SKILL_MIN}},
                "command": "commands.talent_cmdset.OperateCmdSet"},
    "order": {"requirements": {"skills": {"command": BASE_SKILL_MIN}}, "command": "commands.talent_cmdset.OrderCmdSet"},
    "parry": {"requirements": {"skills": {"melee": BASE_SKILL_MIN}}, "command": "commands.talent_cmdset.ParryCmdSet"},
    "planning": {"requirements": {"skills": {"intellect": EPIC_SKILL_MIN}},
                 "command": "commands.talent_cmdset.PlanningCmdSet"},
    "prepare": {"requirements": {"skills": {"survival": EPIC_SKILL_MIN}},
                "command": "commands.talent_cmdset.PrepareCmdSet"},
    "quickshot": {"requirements": {"skills": {"quickdraw": BASE_SKILL_MIN}},
                  "command": "commands.talent_cmdset.QuickshotCmdSet"},
    "rally": {"requirements": {"skills": {"influence": BASE_SKILL_MIN}},
              "command": "commands.talent_cmdset.RallyCmdSet"},
    "rebuke": {"requirements": {"skills": {"command": EPIC_SKILL_MIN}},
               "command": "commands.talent_cmdset.RebukeCmdSet"},
    "recover": {"requirements": {"skills": {"salvage": EPIC_SKILL_MIN}},
                "command": "commands.talent_cmdset.RecoverCmdSet"},
    "repair": {"requirements": {"skills": {"mechanical": BASE_SKILL_MIN}},
               "command": "commands.talent_cmdset.RepairCmdSet"},
    "riposte": {"requirements": {"skills": {"melee": BASE_SKILL_MIN}},
                "command": "commands.talent_cmdset.RiposteCmdSet"},
    "risky move": {"requirements": {"skills": {"gambling": EPIC_SKILL_MIN}},
                   "command": "commands.talent_cmdset.RiskyMoveCmdSet"},
    "shield": {"requirements": {"skills": {"mechanical": BASE_SKILL_MIN}},
               "command": "commands.talent_cmdset.ShieldCmdSet"},
    "sneak": {"requirements": {"skills": {"stealth": BASE_SKILL_MIN}}, "command": "commands.talent_cmdset.SneakCmdSet"},
    "snipe": {"requirements": {"skills": {"firearms": EPIC_SKILL_MIN}},
              "command": "commands.talent_cmdset.SnipeCmdSet"},
    "spot": {"requirements": {"skills": {"perception": BASE_SKILL_MIN}},
             "command": "commands.talent_cmdset.SpotCmdSet"},
    "steal": {"requirements": {"skills": {"streetwise": EPIC_SKILL_MIN}},
              "command": "commands.talent_cmdset.StealCmdSet"},
    "strategy": {"requirements": {"skills": {"intellect": BASE_SKILL_MIN}},
                 "command": "commands.talent_cmdset.StrategyCmdSet"},
    "stun": {"requirements": {"skills": {"firearms": BASE_SKILL_MIN}}, "command": "commands.talent_cmdset.StunCmdSet"},
    "surgery": {"requirements": {"skills": {"medicine": BASE_SKILL_MIN}},
                "command": "commands.talent_cmdset.SurgeryCmdSet"},
    "tallow roll": {"requirements": {"skills": {"piloting": EPIC_SKILL_MIN}},
                    "command": "commands.talent_cmdset.TallowRollCmdSet"},
    "tinker": {"requirements": {"skills": {"mechanical": EPIC_SKILL_MIN}},
               "command": "commands.talent_cmdset.TinkerCmdSet"},
    "track": {"requirements": {"skills": {"survival": BASE_SKILL_MIN}},
              "command": "commands.talent_cmdset.TrackCmdSet"},
    "trick shot": {"requirements": {"skills": {"quickdraw": EPIC_SKILL_MIN}},
                   "command": "commands.talent_cmdset.TrickShotCmdSet"},
    "tripwire": {"requirements": {"skills": {"explosives": EPIC_SKILL_MIN}},
                 "command": "commands.talent_cmdset.TripwireCmdSet"},
}

MENU_TALENTS = {
    "army commander 1": {"requirements": {"skills": {"command": 75}}},
    "army commander 2": {"requirements": {"skills": {"command": 150}, "talents": ["army commander 1"]}},
    "fleet commander 1": {"requirements": {"skills": {"command": 75}}},
    "fleet commander 2": {"requirements": {"skills": {"command": 150}, "talents": ["fleet commander 1"]}},
    "sims menu 1": {"requirements": {"skills": {"influence": 75}}},
    "shii-cho": {"requirements": {"skills": {"melee": 1}}},
    "makashi": {"requirements": {"skills": {"melee": 1}}}
}

FORCE_TALENTS = {
    "meditation 1": {"requirements": {}, "boost": {"knowledge": BASE_SKILL_LEVEL1}},
    "meditation 2": {"requirements": {"talent": "meditation 1"}, "boost": {"knowledge": BASE_SKILL_LEVEL2}},
    "meditation 3": {"requirements": {"talent": "meditation 2"}, "boost": {"knowledge": BASE_SKILL_LEVEL2}},
    "aggressive 1": {"requirements": {}, "boost": {"attack": BASE_SKILL_LEVEL1}},
    "aggressive 2": {"requirements": {"talent": "aggressive 1"}, "boost": {"attack": BASE_SKILL_LEVEL2}},
    "aggressive 3": {"requirements": {"talent": "aggressive 2"}, "boost": {"attack": BASE_SKILL_LEVEL2}},
    "defensive 1": {"requirements": {}, "boost": {"defend": BASE_SKILL_LEVEL1}},
    "defensive 2": {"requirements": {"talent": "defend 1"}, "boost": {"defend": BASE_SKILL_LEVEL2}},
    "defensive 3": {"requirements": {"talent": "defend 2"}, "boost": {"defend": BASE_SKILL_LEVEL2}},
    # Force Active Talents
    "battlemind": {"requirements": {"force": FORCE_TIER_2}, "command": "commands.talent_cmdset.BattleMindCmdSet"},
    "electric judgment": {"requirements": {"force": FORCE_TIER_3},
                          "command": "commands.talent_cmdset.ElectricJudgmentCmdSet"},
    "force enlightenment": {"requirements": {"force": FORCE_TIER_1},
                            "command": "commands.talent_cmdset.ForceEnlightenmentCmdSet"},
    "force healing": {"requirements": {"force": FORCE_TIER_1}, "command": "commands.talent_cmdset.ForceHealingCmdSet"},
    "force light": {"requirements": {"force": FORCE_TIER_3}, "command": "commands.talent_cmdset.ForceLightCmdset"}

}

TALENTS = dict(PASSIVE_TALENTS.items() + ACTIVE_TALENTS.items() + MENU_TALENTS.items())
