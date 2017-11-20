from random import randint
from world.skills import SKILL_VALUES


def roll_skill(character, skill):
    ###############################################################
    #  This needs to be rewritten to reflect new Skill handler    #
    #  and new combat/skill check methodology                     #
    ###############################################################

    # Get character's skill and endurance and combine them.
    skill = character.skills.get(skill)
    if not skill:
        skill = 0
    endurance = character.endurance.get()
    skill_value = skill + endurance

    #  Determine initial number of d100.  #
    bonus_chance = int(skill_value % 40)
    die_number = int(skill_value / 40)

    # determine if a bonus die is added
    if randint(1, 100) <= bonus_chance:
        die_number += 1

    # Generate list of rolls.  #
    results = []
    for x in range(0, die_number):
        results.append(randint(1, 100))

    # Sort the rolls from highest to lowest.  #
    if skill_value < 1:
        results.sort()
    else:
        results.sort(reverse=True)

    # Returns the highest of the dice rolls from the results list.  #
    if len(results) > 0:
        return results[0]
    else:
        return 0


def challenge_skill(challenger, defender, c_skill, d_skill):
    c_skill_value = roll_skill(challenger, c_skill)
    d_skill_value = roll_skill(defender, d_skill)

    success_rate = (c_skill - d_skill)
    combat_roll = c_skill_value - d_skill_value

    return combat_roll - success_rate / 20


def get_skill_name(skill, value):
    skill_base = SKILL_VALUES[skill]
    skill_desc = skill_base[value]
    return skill_desc


def parse_skill_check():
    pass


def price_haggle_check(character, cost):
    # Function for evaluating the business skill and applying a price reduction based on the success of the roll.
    haggle_score = roll_skill(character, "business")

    if haggle_score <= 60:
        return cost
    elif haggle_score <= 75:
        return cost * 0.9
    elif haggle_score <= 85:
        return cost * 0.85
    elif haggle_score <= 95:
        return cost * 0.8
    else:
        return cost * 0.75


def parse_accuracy(value):
    if value >= 40:
        return "Low"
    elif value >= 30:
        return "Low-Medium"
    elif value >= 25:
        return "Medium"
    elif value >= 20:
        return "Medium-High"
    elif value >= 15:
        return "High"
    elif value >= 10:
        return "Very High"
    else:
        return "Extremely High"


def parse_damage(value):
    if value >= 40:
        return "Extremely High"
    elif value >= 35:
        return "Very High"
    elif value >= 30:
        return "High"
    elif value >= 25:
        return "Medium-High"
    elif value >=20:
        return "Medium"
    elif value >= 15:
        return "Low-Medium"
    else:
        return "Low"

