from evennia import DefaultScript
from world import rules
import random


class SkillHandler(DefaultScript):
    def at_script_creation(self):
        self.db.key = "skill_handler_%i" % random.randint(1, 10000)
        self.db.desc = "skill handler"
        self.db.character = None
        self.persistent = True
        self.db.skills = []

    def get(self, name):
        actual = [s.actual for s in self.db.skills if s.name == name]
        if actual:
            return int(actual[0])
        else:
            return 0

    def get_skills(self):
        """
        Returns a list of skills
        """
        return sorted(self.db.skills)

    def add(self, **kwargs):
        if 'name' not in kwargs:
            raise SkillException('Name is required')
        if 'base' not in kwargs:
            raise SkillException('Base is required')

        existing = [s for s in self.db.skills if s.name == kwargs.get('name')]

        if existing:
            existing[0].base += kwargs.get('base')
        else:
            skill = dict(name=kwargs.get('name'),
                         base=kwargs.get('base'))

            new_skill = Skill(skill)
            if 'mod' in kwargs:
                skill.update(mod=kwargs.get('mod'))
            else:
                skill.update(mod=0)

            self.db.skills.append(new_skill)

    def improve(self, skill, value):
        attribute = [s for s in self.db.skills if s.name == skill]

        if attribute:
            attribute[0].base += value
        else:
            raise SkillException("Skill does not exist.")

    def mod(self, skill, value):
        existing = [s for s in self.db.skills if s.name == skill]
        if existing:
            existing.mod += value
        else:
            SkillException("Skill does not exist.")

    def reset_mod(self, skill):
        s = [s for s in self.db.skills if s.name == skill]
        if s:
            s[0].mod = 0
        else:
            raise SkillException("SKill does not exist.")

    def set_character(self, char):
        self.db.character = char

    def clear_skills(self):
        self.db.skills = []


class SkillException(Exception):
    def __init__(self, msg):
        self.msg = msg


class Skill(object):
    def __init__(self, data):
        if "name" not in data:
            raise SkillException("Name is a required key.")

        if "base" not in data:
            raise SkillException("Base is a required key.")

        self._data = data

    def __repr__(self):
        return self.name

    def __str__(self):
        # return "%s: %s" % (self.name, rules.get_skill_name(self.name, self.actual))
        return self.name + " : " + self.value

    @property
    def base(self):
        return self._data['base']

    @base.setter
    def base(self, value):
        self._data['base'] = value

    @property
    def name(self):
        return self._data['name']

    @property
    def mod(self):
        return self._data['mod']

    @mod.setter
    def mod(self, value):
        self._data['mod'] = value

    @property
    def actual(self):
        return self.base + self.mod

    @property
    def value(self):
        return rules.get_skill_name(self.name, self.parse_skill_value(self.actual))

    @staticmethod
    def parse_skill_value(value):
        if value > 200:
            return 201
        elif value > 180:
            return 200
        elif value > 160:
            return 180
        elif value > 140:
            return 160
        elif value > 120:
            return 140
        elif value > 100:
            return 120
        elif value > 80:
            return 100
        elif value > 60:
            return 80
        elif value > 40:
            return 60
        elif value > 20:
            return 40
        elif value > 0:
            return 20
        else:
            return 0
