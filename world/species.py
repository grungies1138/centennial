"""
Species template:

    {<species name>: {
                      "skills": {<skill>: <mod>, ...},
                      "languages": [<list of languages>],
                      "talents": [<list of default talents>]
                      }

    All species fields are optional.

"""

SPECIES = {"wookiee": {"skills": {"mechanical": 1, "stealth": -1}, "languages": ["shyriiwook"], "talents": []},
           "human": {"skills": {}, "languages": ["basic"], "talents": []},
           "aqualish": {"skills": {"melee": 1, "influence": -1}, "languages": [], "talents": []},
           "arcona": {"skills": {}, "languages": [], "talents": []},
           "arkanian": {"skills": {"perception": 1, "streetwise": -1}, "languages": [], "talents": []},
           "barabel": {"skills": {"dodge": 1, "survival": -1}, "languages": [], "talents": []},
           "bith": {"skills": {"perception": 1, "athletics": -1}, "languages": [], "talents": []},
           "bothan": {"skills": {"stealth": 1, "business": -1}, "languages": [], "talents": []},
           "chadra-fan": {"skills": {"perception": 1, "heavy weapons": -1}, "languages": [], "talents": []},
           "chiss": {"skills": {"command": 1, "gambling": -1}, "languages": [], "talents": []},
           "devaronian": {"skills": {}, "languages": ["basic"], "talents": []},
           "dug": {"skills": {"althletics": 1, "quickdraw": -1}, "languages": [], "talents": []},
           "duros": {"skills": {"piloting": 1, "explosives": -1}, "languages": [], "talents": []},
           "falleen": {"skills": {"influence": 1, "salvage": -1}, "languages": [], "talents": []},
           "gamorrean": {"skills": {"melee": 1, "mechanical": -1}, "languages": [], "talents": []},
           "gand": {"skills": {"perception": 1, "medicine": -1}, "languages": [], "talents": []},
           "gran": {"skills": {"business": 1, "streetwise": -1}, "languages": [], "talents": []},
           "gungan": {"skills": {"melee": 1, "streetwise": -1}, "languages": [], "talents": []},
           "hutt": {"skills": {"business": 1, "athletics": -1}, "languages": ["huttese", "basic"], "talents": []},
           "ishi tib": {"skills": {"perception": 1, "survival": -1}, "languages": [], "talents": []},
           "ithorian": {"skills": {"intellect": 1, "firearms": -1}, "languages": [], "talents": []},
           "kubaz": {"skills": {"intellect": 1, "gambling": -1}, "languages": [], "talents": []},
           "mon calamari": {"skills": {"command": 1, "survival": -1}, "languages": [], "talents": []},
           "neimoidian": {"skills": {"business": 1, "perception": -1}, "languages": [], "talents": []},
           "nikto": {"skills": {"survival": 1, "command": -1}, "languages": [], "talents": []},
           "quarren": {"skills": {"piloting": 1, "influence": -1}, "languages": [], "talents": []},
           "rodian": {"skills": {"firearms": 1, "intellect": -1}, "languages": [], "talents": []},
           "shistavanen": {"skills": {"athletics": 1, "influence": -1}, "languages": [], "talents": []},
           "sullustan": {"skills": {"business": 1, "command": -1}, "languages": [], "talents": []},
           "talz": {"skills": {"heavy weapons": 1, "intellect": -1}, "anguages": [], "talents": []},
           "togorian": {"skills": {"melee": 1, "security": -1}, "laguages": [], "talents": []},
           "twi'lek": {"skills": {}, "languages": [], "talents": []},
           "weequay": {"skills": {"firearms": 1, "influence": -1}, "languages": [], "talents": []},
           "whiphid": {"skills": {"survival": 1, "mechanical": -1}, "languages": [], "talents": []},
           "zeltron": {"skills": {"influence": 1, "intellect": -1}, "languages": [], "talents": []},
           "nagai": {"skills": {"firearms": 1, "perception": -1}, "languages": [], "talents": []}
           }
