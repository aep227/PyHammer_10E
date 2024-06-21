#################################################
# Warhammer 40k 10th Edition combat calculator  #
#                                               #
# Engineer: Addison Powell                      #
# Start Date: 5/31/2024                         #
#################################################

import json
import math
import tkinter as tk
import tkinter.ttk as ttk
import subprocess
import threading
from prettytable import PrettyTable

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

class Weapon:
    """ Class for defining a Weapon """
    def __init__(self, name=None, count=None, attacks=None, skill=None,
                strength=None, AP=None, damage=None, abilities={}):
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
        if ability not in self.abilities:
            self.abilities.add(ability)
        else:
            print(f'Alert: {self.name} already has the {ability} ability')

    def remove_ability(self, ability):
        if ability in self.abilities:
            self.abilities.remove(ability)
        else:
            print(f'Alert: {self.name} does not have the {ability} ability')
    
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
    def __init__(self, name=None, model_count=None, toughness=None,
                 wounds=None, armor=None, invul=None, abilities={},
                 keywords={}, weapons={}):
        self.name = name
        self.model_count = model_count
        self.toughness = toughness
        self.wounds = wounds
        self.armor = armor
        self.invul = invul
        self.abilities = abilities
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


    # Ability add/remove/clear
    def add_ability(self, ability):
        if ability not in self.abilities:
            self.abilities.add(ability)
        else:
            print(f'Alert: {self.name} already has the {ability} ability')

    def remove_ability(self, ability):
        if ability in self.abilities:
            self.abilities.remove(ability)
        else:
            print(f'Alert: {self.name} does not have the {ability} ability')
    
    def clear_abilities(self):
        self.abilities.clear()


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

    def add_ability(self, ability):
            self.abilities.add(ability)

    def remove_ability(self, ability):
            self.abilities.remove(ability)


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
                    damage = 'D6',
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
    
    d_VEQ = Unit(name = '1x VEQ',
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
    skill_mod = 0
    if STATIONARY == True and 'HEAVY' in weapon.abilities:
        skill_mod -= 1
    if 'STEALTH' in defender.abilities:
        skill_mod += 1
    if INDIRECT == True and 'INDIRECT FIRE' in weapon.abilities:
        skill_mod += 1

    # Cap skill modification to +/- 1
    if skill_mod > 1:
        skill_mod = 1
    elif skill_mod < -1:
        skill_mod = -1
    
    mod_skill = weapon.skill + skill_mod

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

    return float('{0:.3f}'.format(hits+sustained)), float('{0:.3f}'.format(lethals))
# End calc_hits_avg()


def calc_wounds_avg(hits, lethals, weapon, defender):
    """ Calculate the average number of wounds 
    
    Arguments:
    hits - number of hits from weapon
    lethals - number of lethal hits from weapon
    weapon - the attacking weapon
    defender - the defending unit

    Returns:
    wounds - the average wounds inflicted by the weapon on the defender
    dev_wounds - the average devastating wounds inflicted by the weapon on the defender
    """

    # Determine number of devastating wounds
    if 'DEVASTATING WOUNDS' in weapon.abilities:
        dev_wounds = hits * P6
    else:
        dev_wounds = 0

    # Determine base wound target
    if weapon.strength >= defender.toughness*2:
        target = 2
    elif weapon.strength > defender.toughness and weapon.strength < (defender.toughness*2):
        target = 3
    elif weapon.strength == defender.toughness:
        target = 4
    elif weapon.strength < defender.toughness and (weapon.strength*2) > defender.toughness:
        target = 5
    elif (weapon.strength*2) <= defender.toughness:
        target = 6

    # Check LANCE
    if 'LANCE' in weapon.abilities and CHARGED == True:
        target -= 1

    # Cap wound target
    if target > 6:
        target = 6
    elif target < 2:
        target = 2

    # Calculate wounds
    if 'TWIN-LINKED' in weapon.abilities:
        match target:
            case 2:
                wounds = hits * P2_RRA
            case 3:
                wounds = hits * P3_RRA
            case 4:
                wounds = hits * P4_RRA
            case 5:
                wounds = hits * P5_RRA
            case 6:
                wounds = hits * P6_RRA
    else:
        match target:
            case 2:
                wounds = hits * P2
            case 3:
                wounds = hits * P3
            case 4:
                wounds = hits * P4
            case 5:
                wounds = hits * P5
            case 6:
                wounds = hits * P6

    # Add lethals
    wounds += lethals

    return float('{0:.3f}'.format(wounds)), float('{0:.3f}'.format(dev_wounds))
# End calc_wounds_avg()


def calc_unsaved_avg(wounds, dev_wounds, weapon, defender):
    """ Calculate the average number of unsaved wounds
    
    Arguments:
    wounds - number of wounds from weapon
    dev_wounds - number of devastating wounds from weapon
    weapon - the attacking weapon
    defender - the defending unit

    Returns:
    unsaved - the average number of unsaved wounds inflicted by the weapon on the defender
    """

    # Calculate AP-modified armor save
    # AP is negative, subtract to add to armor number, making it worse
    mod_armor = defender.armor - weapon.AP

    # Check for cover
    if COVER and 'IGNORES COVER' not in weapon.abilities:
        mod_armor -= 1

    # Prevent 3+ armor going to a 2+ armor in cover vs AP0
    if defender.armor == 3 and mod_armor == 2:
        mod_armor = 3

    # Determine if AP-modified armor save is better than invulnerable save
    if defender.invul != None and mod_armor > defender.invul:
        save = defender.invul
    else:
        save = mod_armor
    
    # Cap save
    if save > 7:
        save = 7

    # Determine number of unsaved wounds        
    match save:
        case 2:
            unsaved = wounds * P6
        case 3:
            unsaved = wounds * P5
        case 4:
            unsaved = wounds * P4
        case 5:
            unsaved = wounds * P3
        case 6:
            unsaved = wounds * P2
        case 7:
            unsaved = wounds

    unsaved += dev_wounds

    return float('{0:.3f}'.format(unsaved))
# End calc_unsaved_avg()


def calc_slain_avg(unsaved, weapon, defender):
    """ Calculate the average number of defending models slain
     
    Arguments:
    unsaved - number of unsaved wounds from weapon
    weapon - the attacking weapon
    defender - the defending unit

    Returns:
    slain - the average number of slain models
    """

    # Convert random damage to average
    if weapon.damage in RANDOM_VALUE_AVGS:
        damage = RANDOM_VALUE_AVGS[weapon.damage]
    else:
        damage = weapon.damage

    unsaved_to_kill = math.ceil(defender.wounds / damage)
    slain = unsaved / unsaved_to_kill

    return float('{0:.3f}'.format(slain))
# End calc_slain_avg()


def create_unit():
    pass
# End create_unit()


def create_weapon():
    pass
# End create_weapon()


def run_one():
    pass
# End run_one()

def run_all(attacker_list, defender_list):
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
    
                avg_wounds, avg_dev_wounds = calc_wounds_avg(avg_hits, avg_lethals, weapon, defender)
                results_dict[attacker.name][weapon.name][defender.name]['Avg Wounds'] = avg_wounds

                avg_unsaved = calc_unsaved_avg(avg_wounds, avg_dev_wounds, weapon, defender)
                results_dict[attacker.name][weapon.name][defender.name]['Avg Unsaved'] = avg_unsaved

                avg_slain = calc_slain_avg(avg_unsaved, weapon, defender)
                results_dict[attacker.name][weapon.name][defender.name]['Avg Slain'] = avg_slain

    return results_dict
# End run_all()


###############################
#        GUI Functions        #
###############################

def weapon_select(evt):
    w = evt.widget
    index = int(w.curselection()[0])
    value = w.get(index)
    print('You selected item %d: "%s"' % (index, value))




def main():
    attacker_list, defender_list = initialize()
    # results_dict = run_all(attacker_list, defender_list)


    #############################
    #    User Interface setup   #
    #############################

    root = tk.Tk()
    default_font = ('Cascadia Code', '14')
    title_font = ('Cascadia Code', '18', 'bold')
    default_padding = 20

    s = ttk.Style()
    s.configure('default.TFrame', font = default_font)
    s.configure('title.TLabel', font = title_font)
    s.configure('default.TLabel', font = default_font)
    s.configure('default.TButton', font = default_font)
    s.configure('default.TCheckbutton', font = default_font)
    s.configure('spacer.TLabel', font = ('Cascadia Code', '16'))

    # Attacker frame
    attacker_frame = ttk.Frame(root, style = 'default.TFrame')
    attacker_label = ttk.Label(attacker_frame, text = 'Attacker Units', style = 'default.TLabel')
    weapon_label = ttk.Label(attacker_frame, text = 'Attacker Weapons', style = 'default.TLabel')
    weapon_stats_label = ttk.Label(attacker_frame, text = 'Weapon Stats', style = 'default.TLabel')
    attacker_listbox = tk.Listbox(attacker_frame, height = 10, font = default_font)
    weapon_listbox = tk.Listbox(attacker_frame, height = 10, font = default_font)
    weapon_stats_listbox = tk.Listbox(attacker_frame, height = 10, font = default_font)

    index = 0
    for attacker in attacker_list:
        attacker_listbox.insert(f'{index}', attacker.name)
        index += 1
    index = 0
    for weapon in attacker_list[0].weapons:
        weapon_listbox.insert(f'{index}', weapon.name)
        if index == 0:
            weapon_stats_listbox.insert('0', f'Attacks: {weapon.attacks}')
            weapon_stats_listbox.insert('1', f'Skill: {weapon.skill}')
            weapon_stats_listbox.insert('2', f'Strength: {weapon.strength}')
            weapon_stats_listbox.insert('3', f'AP: {weapon.AP}')
            weapon_stats_listbox.insert('4', f'Damage: {weapon.damage}')
            weapon_stats_listbox.insert('5', f'Abilities: {weapon.abilities}')
        index += 1


    # Defender frame
    defender_frame = ttk.Frame(root, style = 'default.TFrame')
    defender_label = ttk.Label(defender_frame, text = 'Defender Units', style = 'default.TLabel')
    defender_stats_label = ttk.Label(defender_frame, text = 'Defender Stats', style = 'default.TLabel')
    defender_listbox = tk.Listbox(defender_frame, height = 10, font = default_font)
    defender_stats_listbox = tk.Listbox(defender_frame, height = 10, font = default_font)

    index = 0
    for defender in defender_list:
        defender_listbox.insert(f'{index}', defender.name)
        index += 1
    index = 0
    defender_stats_listbox.insert('0', f'Model Count: {defender_list[0].model_count}')
    defender_stats_listbox.insert('1', f'Toughness: {defender_list[0].toughness}')
    defender_stats_listbox.insert('2', f'Wounds: {defender_list[0].wounds}')
    defender_stats_listbox.insert('3', f'Armor: {defender_list[0].armor}')
    defender_stats_listbox.insert('4', f'Invul: {defender_list[0].invul}')
    defender_stats_listbox.insert('5', f'Keywords: {defender_list[0].keywords}')




    # Results frame
    results_frame = ttk.Frame(root, style = 'default.TFrame')
    results_label = ttk.Label(results_frame, text = 'Results', style = 'default.TLabel')
    results_text = tk.Text(results_frame, height = 24, width = 80, font = default_font)
    results_scroll_y = ttk.Scrollbar(results_frame, orient = 'vertical', command = results_text.yview)
    results_scroll_x = ttk.Scrollbar(results_frame, orient = 'horizontal', command = results_text.xview)
    results_text.config(yscrollcommand=results_scroll_y.set)
    results_text.config(xscrollcommand=results_scroll_x.set)


    # Function buttons
    db_function_frame = ttk.Frame(root, style = 'default.TFrame')
    add_attacker_unit_button = ttk.Button(db_function_frame, text = 'Add Attacker Unit', style = 'default.TButton')
    add_attacker_weapon_button = ttk.Button(db_function_frame, text = 'Add Attacker Weapon', style = 'default.TButton')
    remove_attacker_unit_button = ttk.Button(db_function_frame, text = 'Remove Attacker Unit', style = 'default.TButton')
    remove_attacker_weapon_button = ttk.Button(db_function_frame, text = 'Remove Attacker Weapon', style = 'default.TButton')
    add_defender_unit_button = ttk.Button(db_function_frame, text = 'Add Defender Unit', style = 'default.TButton')
    remove_defender_unit_button = ttk.Button(db_function_frame, text = 'Remove Defender Unit', style = 'default.TButton')


    # Calculation buttons
    calculate_frame = ttk.Frame(root, style = 'default.TFrame')
    calculate_all = ttk.Button(calculate_frame, text = 'Calculate All', style = 'default.TButton')
    calculate_attacker = ttk.Button(calculate_frame, text = 'Calculate Attacker', style = 'default.TButton')
    calculate_weapon = ttk.Button(calculate_frame, text = 'Calculate Weapon', style = 'default.TButton')
    calculate_selected = ttk.Button(calculate_frame, text = 'Calculate Selected', style = 'default.TButton')


    # Settings frame
    HALF_RANGE = tk.BooleanVar()
    HALF_RANGE.set(False)
    INDIRECT = tk.BooleanVar()
    INDIRECT.set(False)
    COVER = tk.BooleanVar()
    COVER.set(False)
    STATIONARY = tk.BooleanVar()
    STATIONARY.set(False)
    CHARGED = tk.BooleanVar()
    CHARGED.set(False)
    settings_frame = ttk.Frame(root, style = 'default.TFrame')
    half_range_check = ttk.Checkbutton(settings_frame, text = 'Attacker Half Range', variable = HALF_RANGE, style = 'default.TCheckbutton', offvalue = False, onvalue = True)
    indirect_check = ttk.Checkbutton(settings_frame, text = 'Attacker Indirect', variable = INDIRECT, style = 'default.TCheckbutton', offvalue = False, onvalue = True)
    stationary_check = ttk.Checkbutton(settings_frame, text = 'Attacker Stationary', variable = STATIONARY, style = 'default.TCheckbutton', offvalue = False, onvalue = True)
    charged_check = ttk.Checkbutton(settings_frame, text = 'Attacker Charged', variable = CHARGED, style = 'default.TCheckbutton', offvalue = False, onvalue = True)
    cover_check = ttk.Checkbutton(settings_frame, text = 'Defender in Cover', variable = COVER, style = 'default.TCheckbutton', offvalue = False, onvalue = True)


    # Lay out attacker frame
    attacker_label.grid(       row = 0, column = 0)
    weapon_label.grid(         row = 0, column = 1)
    weapon_stats_label.grid(   row = 0, column = 2)
    attacker_listbox.grid(     row = 1, column = 0, padx = default_padding, pady = default_padding)
    weapon_listbox.grid(       row = 1, column = 1)
    weapon_stats_listbox.grid( row = 1, column = 2, padx = default_padding, pady = default_padding)

    # Lay out defender frame
    defender_label.grid(         row = 0, column = 0)
    defender_stats_label.grid(   row = 0, column = 1)
    defender_listbox.grid(       row = 1, column = 0, padx = default_padding, pady = default_padding)
    defender_stats_listbox.grid( row = 1, column = 1)

    # Lay out settings frame
    half_range_check.grid(  row = 0, column = 0, padx = default_padding, sticky = 'w')
    indirect_check.grid(    row = 1, column = 0, padx = default_padding, sticky = 'w')
    stationary_check.grid(  row = 0, column = 1, padx = default_padding, sticky = 'w')
    charged_check.grid(     row = 1, column = 1, padx = default_padding, sticky = 'w')
    cover_check.grid(       row = 0, column = 2, padx = default_padding, sticky = 'w')

    # Lay out results frame
    results_label.grid(    row = 0, column = 0)
    results_text.grid(     row = 1, column = 0)
    results_scroll_y.grid( row = 1, column = 1, sticky = 'nsw')
    results_scroll_x.grid( row = 2, column = 0, sticky = 'nwe')

    # Lay out function frame
    add_attacker_unit_button.grid(      row = 0, column = 0, padx = default_padding, pady = default_padding)
    add_attacker_weapon_button.grid(    row = 0, column = 1, padx = default_padding, pady = default_padding)
    add_defender_unit_button.grid(      row = 0, column = 2, padx = default_padding, pady = default_padding)
    remove_attacker_unit_button.grid(   row = 1, column = 0, padx = default_padding, pady = default_padding)
    remove_attacker_weapon_button.grid( row = 1, column = 1, padx = default_padding, pady = default_padding)
    remove_defender_unit_button.grid(   row = 1, column = 2, padx = default_padding, pady = default_padding)

    # Lay out calculation frame
    calculate_all.grid(      row = 0, column = 0, padx = default_padding, pady = default_padding)
    calculate_attacker.grid( row = 0, column = 1, padx = default_padding, pady = default_padding)
    calculate_weapon.grid(   row = 0, column = 2, padx = default_padding, pady = default_padding)
    calculate_selected.grid( row = 0, column = 3, padx = default_padding, pady = default_padding)

    # Lay out root window
    attacker_frame.grid(    row = 0, column = 0, columnspan = 2)
    defender_frame.grid(    row = 1, column = 0)
    results_frame.grid(     row = 0, column = 2, rowspan = 2)
    db_function_frame.grid( row = 2, column = 0, rowspan = 2)
    settings_frame.grid(    row = 2, column = 2)
    calculate_frame.grid(   row = 3, column = 2)


    # Event handling
    weapon_listbox.bind('<<ListboxSelect>>', weapon_select)
    root.mainloop()

if __name__ == '__main__':
    main()