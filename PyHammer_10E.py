#################################################
# Warhammer 40k 10th Edition combat calculator  #
#                                               #
# Engineer: Addison Powell                      #
# Start Date: 5/31/2024                         #
#################################################

### Set up constants ###
# Probabilites, no rerolls
P2 = 0.833
P3 = 0.667
P4 = 0.500
P5 = 0.333
P6 = 0.167
# Probabilties, rerolling 1s
P2_RR1 = 0.833
P3_RR1 = 0.667
P4_RR1 = 0.500
P5_RR1 = 0.333
P6_RR1 = 0.167
# Probabilities, rerolling all
P2_RRA = 0.833
P3_RRA = 0.667
P4_RRA = 0.500
P5_RRA = 0.333
P6_RRA = 0.167

# Random value averages
RANDOM_VALUE_AVGS = {
    'D3': 2,
    '2D3': 4,
    'D6': 3.5,
    '2D6': 7,
    'D3_PLUS_3': 5,
    'D6_PLUS_3': 6.5,
    'D6_PLUS_6': 9.5,
}

class Weapon:
    def __init__(self, name=None, attacks=None, skill=None, strength=None, AP=None, damage=None, abilities={}):
        self.name = name
        self.attacks = attacks
        self.skill = skill
        self.strength = strength
        self.AP = AP
        self.damage = damage
        self.abilities = abilities

    # Update functions
    def update_name(self, name):
        self.name = name
    
    def update_attacks(self, attacks):
        if attacks in RANDOM_VALUE_AVGS.keys():
            self.attacks = RANDOM_VALUE_AVGS[attacks]
        elif attacks > 0:
            self.attacks = attacks
        else:
            print('Error: Invalid attacks value')

    def update_skill(self, skill):
        if 2 <= skill <= 6:
            self.skill = skill
        else:
            print('Error: skill must be between 2 and 6')

    def update_strength(self, strength):
        if self.strength > 0:
            self.strength = strength
        else:
            print('Error: strength must be greater than zero')

    def update_AP(self, AP):
        if self.AP >= 0:
            self.attacks = AP
        else:
            print('Error: AP must be positive')

    def update_damage(self, damage):
        if damage in RANDOM_VALUE_AVGS.keys():
            self.damage = RANDOM_VALUE_AVGS[damage]
        elif damage > 0:
            self.attacks = damage
        else:
            print('Error: Invalid attacks value')


    # Ability add/remove/clear
    def add_ability(self, ability):
        self.abilities.add(ability)

    def remove_ability(self, ability):
        if ability in self.abilities:
            self.abilities.remove(ability)
        else:
            print(f'Alert: {self.name} does not have the {ability} keyword')
    
    def clear_abilities(self):
        self.abilities.clear()
# End Weapon class


class Unit:
    def __init__(self, toughness=None, wounds=None, armor=None, invul=None, keywords={}, weapons={}):
        self.toughness = toughness
        self.wounds = wounds
        self.armor = armor
        self.invul = invul
        self.keywords = keywords
        self.weapons = weapons

    # Update functions
    def update_toughness(self, toughness):
        if toughness > 0:
            self.toughness = toughness
        else:
            print('Error: Toughness must be above zero')

    def update_wounds(self, wounds):
        if wounds > 0:
            self.wounds = wounds
        else:
            print('Error: Wounds must be above zero')

    def update_armor(self, armor):
        if 2 <= armor <= 6:
            self.armor = armor
        else:
            print('Error: Armor save must be between 2 and 6')

    def update_invul(self, invul):
        if 2 <= invul <= 6:
            self.invul = invul
        else:
            print('Error: Invulnerable save must be between 2 and 6')


    # Keyword add/remove/clear
    def add_keyword(self, keyword):
        self.keywords.add(keyword)

    def remove_keyword(self, keyword):
        if keyword in self.keywords:
            self.keywords.remove(keyword)
        else:
            print(f'Alert: {self.name} does not have {keyword} keyword')

    def clear_keywords(self):
        self.keywords.clear()


    # Weapon add/remove/clear
    def add_weapon(self, weapon):
        if isinstance(weapon, Weapon):
            self.weapons.add(weapon)
        else:
            print(f'Error: {weapon} is not a Weapon object')

    def remove_weapon(self, weapon):
        if weapon in self.weapons:
            self.weapons.remove(weapon)
        else:
            print(f'Alert: {self.name} is not equipped with {weapon}')
    
    def clear_weapons(self):
        self.weapons.clear()
# End Unit class


def initialize():
    """ Set up Unit and Weapon instances """
    pass
# End initialize()


def calc_hits():
    """ Calculate the average number of hits """
    pass
# End calc_hits()


def calc_wounds():
    """ Calculate the average number of wounds """
    pass
# End calc_wounds()


def calc_slain():
    """ Calculate the average number of defending models slain """
    pass
# End calc_slain()


def report():
    """ Print results to terminal """
    pass
# End report()

def main():
    initialize()

    calc_hits()

    calc_wounds()

    calc_slain()

    report()


if __name__ == '__main__':
    main()