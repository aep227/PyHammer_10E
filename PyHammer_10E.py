#################################################
# Warhammer 40k 10th Edition combat calculator  #
#                                               #
# Engineer: Addison Powell                      #
# Start Date: 5/31/2024                         #
#################################################

import json
import math

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

'''
Available weapon keywords:
- Rapid Fire X
- Ignores Cover
- Twin-linked
- Torrent
- Lethal Hits
- Lance
- Indirect Fire
- Blast
- Melta X
- Heavy
- Devastating Wounds
- Sustained Hits
- Anti-Keyword X+ (Infantry, Monster, Vehicle, Titanic)

Available unit keywords:
- Feel No Pain
- Stealth

'''

# Global settings
HALF_RANGE = False
INDIRECT_PENALTY = False
COVER = False
STATIONARY = False


class Weapon:
    """ Class for defining a Weapon """
    def __init__(self, name=None, count=None, attacks=None, skill=None, strength=None, AP=None, damage=None, abilities={}):
        self.name = name
        self.count = count
        self.attacks = attacks
        self.skill = skill
        self.strength = strength
        self.AP = AP
        self.damage = damage
        self.abilities = abilities

    # Update functions
    def update_name(self, name):
        self.name = name
    
    def update_count(self, count):
        self.count = count

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
            self.damage = damage
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

    def report(self):
        report = {
            'Name': f'{self.name}',
            'Attacks:': f'{self.attacks}',
            'Skill:': f'{self.skill}',
            'Strength:': f'{self.strength}',
            'AP:': f'{self.AP}',
            'Damage:': f'{self.damage}',
            'Abilities:': f'{self.abilities}'
        }
        return report

# End Weapon class


class Unit:
    """ Class defining a unit """
    def __init__(self, name=None, model_count=None, toughness=None, wounds=None, armor=None, invul=None, keywords={}, weapons={}):
        self.name = name
        self.model_count = model_count
        self.toughness = toughness
        self.wounds = wounds
        self.armor = armor
        self.invul = invul
        self.keywords = keywords
        self.weapons = weapons

    # Update functions
    def update_model_count(self, model_count):
        if model_count > 0:
            self.model_count = model_count
        else:
            print('Error: Model count must be above zero')

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

    def report(self):
        weapon_list = ''
        for weapon in self.weapons:
            weapon_list += f'{weapon.name}, '
        weapon_list = weapon_list[:-2]

        report = {
            'Name': f'{self.name}',
            'Model count': f'{self.model_count}',
            'Toughness': f'{self.toughness}',
            'Wounds': f'{self.wounds}',
            'Armor': f'{self.armor}',
            'Invul': f'{self.invul}',
            'Keywords': f'{self.keywords}',
            'Weapons': f'{weapon_list}'
        }

        return report
# End Unit class


def initialize():
    """ 
    Set up Unit and Weapon instances
     
    returns - list of units
    """

    # Create weapons first
    bolter = Weapon(name = '10x Bolter',
                    count = 10,
                    attacks = 1,
                    skill = 3,
                    strength = 4,
                    AP = 0,
                    damage = 1,
                    abilities = {'RAPID FIRE 1'})
    
    flamer = Weapon(name = '2x Flamer',
                    count = 2,
                    attacks = 'D6',
                    skill = 3,
                    strength = 5,
                    AP = 0,
                    damage = 1,
                    abilities = {'TORRENT'})
    
    meltagun = Weapon(name = '2x Meltagun',
                    count = 2,
                    attacks = 1,
                    skill = 3,
                    strength = 9,
                    AP = -4,
                    damage = 'd6',
                    abilities = {'MELTA 2'})
    
    bolt_pistol = Weapon(name = '10x Bolt Pistol',
                    count = 10,
                    attacks = 1,
                    skill = 3,
                    strength = 4,
                    AP = 0,
                    damage = 1,
                    abilities = {'PISTOL'})

    # Create units
    bss = Unit(name = '10xBSS',
               model_count = 10,
               toughness = 3,
               wounds = 1,
               armor = 3,
               invul = None,
               keywords = {'INFANTRY'},
               weapons =  {bolter, bolt_pistol, flamer, meltagun})
    

    # Defender defaults
    d_GEQ = Unit(name = '10x GEQ',
               model_count = 10,
               toughness = 3,
               wounds = 1,
               armor = 5,
               invul = None,
               keywords = {'INFANTRY'},
               weapons =  {})
    
    d_MEQ = Unit(name = '5x MEQ',
               model_count = 5,
               toughness = 4,
               wounds = 2,
               armor = 3,
               invul = None,
               keywords = {'INFANTRY'},
               weapons =  {})
    
    d_TEQ = Unit(name = '5x TEQ',
               model_count = 5,
               toughness = 5,
               wounds = 3,
               armor = 2,
               invul = 4,
               keywords = {'INFANTRY'},
               weapons =  {})
    
    d_VEQ = Unit(name = 'VEQ',
               model_count = 1,
               toughness = 10,
               wounds = 12,
               armor = 3,
               invul = None,
               keywords = {'VEHICLE'},
               weapons =  {})

    # pretty_bolter = json.dumps(bolter.report(), indent=4)
    # print(pretty_bolter)
    # pretty_bss = json.dumps(bss.report(), indent=4)
    # print(pretty_bss)

    attacker_list = [bss]
    defender_list = [d_GEQ, d_MEQ, d_TEQ, d_VEQ]

    return attacker_list, defender_list
# End initialize()


def calc_hits_avg(weapon, defender):
    """ Calculate the average number of hits

    Arguments:
    weapon - the attacking weapon
    defender - the defending unit

    Returns:
    hits - the average hits on the defender
    lethals - the average number of lethal hits on the defender
    """

    # Convert random attacks to average
    if weapon.attacks in RANDOM_VALUE_AVGS:
        attacks = RANDOM_VALUE_AVGS[weapon.attacks]
    else:
        attacks = weapon.attacks

    # Multiple attacks by number of weapons
    attacks *= weapon.count


    # Calculate weapon abilities
    for ability in weapon.abilities:
        # Attack modifiers first
        if 'RAPID FIRE' in ability and HALF_RANGE == True:
            value = ability[:-2].strip()
            if value == 'D3':
                value = 2
            attacks += int(value) * weapon.count

        if 'BLAST' in ability:
            blast_attacks = math.floor(defender.model_count / 5)
            attacks += blast_attacks * weapon.count

        if 'LETHAL HITS' in ability:
            lethals = attacks * P6
        else:
            lethals = 0
        
        if 'SUSTAINED HITS' in ability:
            value = ability[:-2].strip()
            if value == 'D3':
                value = 2
            sustained = (attacks * P6) * int(value)
        else:
            sustained = 0
    
    # Determine target number
    mod_skill = weapon.skill
    if STATIONARY == True and 'HEAVY' in weapon.abilities:
        mod_skill -= 1
    if 'STEALTH' in defender.abilities:
        mod_skill += 1

    # Cap target number
    if mod_skill < 2:
        mod_skill = 2
    elif mod_skill > 6:
        mod_skill = 6

    # Determine rerolls
    if 'REROLL ONES HITS' in weapon.abilities:
        rerolls = 'ONES'
    elif 'REROLL ALL HITS' in weapon.abilities:
        rerolls = 'ALL'
    else:
        rerolls = 'NONE'

    if 'TORRENT' in weapon.abilities:
        hits = attacks
        lethals = 0
        sustained = 0
    else:
        match rerolls:
            case 'NONE':
                match mod_skill:
                    case 2:
                        hits = attacks * P2
                    case 3:
                        hits = attacks * P3
                    case 4:
                        hits = attacks * P4
                    case 5:
                        hits = attacks * P5
                    case 6:
                        hits = attacks * P6
            case 'ONES':
                match mod_skill:
                    case 2:
                        hits = attacks * P2_RR1
                    case 3:
                        hits = attacks * P3_RR1
                    case 4:
                        hits = attacks * P4_RR1
                    case 5:
                        hits = attacks * P5_RR1
                    case 6:
                        hits = attacks * P6_RR1
            case 'ALL':
                match mod_skill:
                    case 2:
                        hits = attacks * P2_RRA
                    case 3:
                        hits = attacks * P3_RRA
                    case 4:
                        hits = attacks * P4_RRA
                    case 5:
                        hits = attacks * P5_RRA
                    case 6:
                        hits = attacks * P6_RRA

    return '{0:.3f}'.format(hits+sustained), '{0:.3f}'.format(lethals)
# End calc_hits_avg()


def calc_wounds_avg(hits, lethals, weapon, defender):
    """ Calculate the average number of wounds 
    
    Arguments:
    hits - number of hits from weapon
    lethals - number of lethal hits from weapon
    weapon - the attacking weapon
    defender - the defending unit

    Returns - wounds; the average wounds inflicted by the weapon on the defender
    """

# End calc_wounds_avg()


def calc_unsaved_avg():
    """ Calculate the average number of unsaved wounds """
    pass
# End calc_unsaved_avg()


def calc_slain_avg():
    """ Calculate the average number of defending models slain """
    pass
# End calc_slain_avg()


def report_avg():
    """ Print average results to terminal """
    pass
# End report_avg()


def main():
    attacker_list, defender_list = initialize()
    results_dict = {}

    for attacker in attacker_list:
        # print(attacker.name)
        if attacker not in results_dict:
            results_dict[attacker.name] = {}

        for weapon in attacker.weapons:
            # print(f'\t{weapon.name}')
            if weapon not in results_dict[attacker.name]:
                results_dict[attacker.name][weapon.name] = {}

            for defender in defender_list:
                # print(f'\t\t{defender.name}')
                if weapon not in results_dict[attacker.name][weapon.name]:
                    results_dict[attacker.name][weapon.name][defender.name] = {}

                avg_hits, avg_lethals = calc_hits_avg(weapon, defender)
                results_dict[attacker.name][weapon.name][defender.name]['Avg Hits'] = avg_hits
    
                avg_wounds = calc_wounds_avg(avg_hits, avg_lethals, weapon, defender, )
                # results_dict[attacker.name][weapon.name][defender.name]['Avg Wounds'] = avg_wounds

                # avg_slain = calc_slain_avg()
                # results_dict[attacker.name][weapon.name][defender.name]['Avg Slain'] = avg_slain

    # report_avg()
    print(json.dumps(results_dict, indent=4))


if __name__ == '__main__':
    main()