"""
    Weapon Types: Pistol, carbine, rifle, heavy, melee, thrown

    Damage Types: Energy, Flechette, Stun, Kinetic, explosive, slashing


"""

DL_17 = {
    "key": "DL-17",
    "typeclass": "typeclasses.weapon.Weapon",
    "health": 20,
    "max_health": 20,
    "skill": "Firearms",
    "accuracy": 30,
    "damage": 2,
    "damage_type": "Energy",
    "durability": 10,
    "mass": 2,
    "manufacturer": "Blastech Industries",
    "description": "Simple blast vest that offers protection to most species vital organs."
}

DL_44 = {
    "key": "DL-44",
    "typeclass": "typeclasses.weapon.Weapon",
    "health": 20,
    "max_health": 20,
    "skill": "Firearms",
    "accuracy": 28,
    "damage": 3,
    "damage_type": "Energy",
    "durability": 12,
    "mass": 2,
    "manufacturer": "Blastech Industries",
    "description": "This compact heavy pistol packs a big punch for such a small package."
}

LIGHTSABER = {
    "key": "Lightsaber",
    "typeclass": "typeclasses.weapon.Weapon",
    "health": 20,
    "max_health": 20,
    "skill": "Melee",
    "accuracy": 0,
    "damage": 10,
    "damage_type": "Energy",
    "durability": 100,
    "mass": 2,
    "description": "A small handled item that produces a blade of pure energy.  There is a distinctive snap-hiss when "
                   "ignited followed by a low hum."
}
