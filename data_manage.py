import Weapon
import Unit

#########################
#    Data Management    #
#########################

def initialize():
    """ 
    Set up initial Unit and Weapon instances
     
    returns - list of attacker units, list of defender units
    """

    # Select between generic defenders for testing weapons
    # or generic weapons for testing durability

    # Create weapons first
    bolterX5 = Weapon.Weapon(name = '5x Bolter',
                    count = 5,
                    attacks = 1,
                    skill = 3,
                    strength = 5,
                    AP = 0,
                    damage = 1,
                    abilities = {'RAPID FIRE 1'})
    
    flamerX4 = Weapon.Weapon(name = '4x Flamer',
                    count = 4,
                    attacks = 'D6',
                    skill = 3,
                    strength = 6,
                    AP = 0,
                    damage = 1,
                    abilities = {'TORRENT', 'IGNORES COVER'})
    
    meltagunX4 = Weapon.Weapon(name = '4x Meltagun',
                    count = 4,
                    attacks = 1,
                    skill = 3,
                    strength = 10,
                    AP = -4,
                    damage = 'D6',
                    abilities = {'MELTA 2'})
    
    storm_bolterX4 = Weapon.Weapon(name = '4x Storm Bolter',
                    count = 4,
                    attacks = 2,
                    skill = 3,
                    strength = 5,
                    AP = 0,
                    damage = 2,
                    abilities = {'RAPID FIRE 2'})
    
    heavy_bolterX4 = Weapon.Weapon(name = '4x Heavy Bolters',
                    count = 4,
                    attacks = 3,
                    skill = 4,
                    strength = 6,
                    AP = -1,
                    damage = 2,
                    abilities = {'HEAVY', 'SUSTAINED HITS 1'})
    
    multi_meltaX4 = Weapon.Weapon(name = '4x Multimeltas',
                    count = 4,
                    attacks = 2,
                    skill = 4,
                    strength = 10,
                    AP = -4,
                    damage = 'D6',
                    abilities = {'HEAVY', 'MELTA 2'})
    
    heavy_flamerX4 = Weapon.Weapon(name = '4x Heavy Flamers',
                    count = 4,
                    attacks = 'D6',
                    skill = 3,
                    strength = 7,
                    AP = -1,
                    damage = 1,
                    abilities = {'TORRENT', 'IGNORES COVER'})
    
    paragon_MM = Weapon.Weapon(name = '3x MMs vs Mon/Veh',
                    count = 3,
                    attacks = 2,
                    skill = 2,
                    strength = 10,
                    AP = -4,
                    damage = 'D6',
                    abilities = {'MELTA 2', 'LANCE'})
    
    paragon_krak = Weapon.Weapon(name = '3x Grenades vs Mon/Veh',
                    count = 3,
                    attacks = 1,
                    skill = 2,
                    strength = 10,
                    AP = -2,
                    damage = 'D3',
                    abilities = {'TWIN-LINKED', 'LANCE'})
    
    paragon_sword = Weapon.Weapon(name = '3x Swords',
                    count = 3,
                    attacks = 4,
                    skill = 3,
                    strength = 8,
                    AP = -2,
                    damage = 2,
                    abilities = {})
    
    paragon_sword_vs_big = Weapon.Weapon(name = '3x Swords vs Mon/Veh',
                    count = 3,
                    attacks = 4,
                    skill = 2,
                    strength = 8,
                    AP = -2,
                    damage = 2,
                    abilities = {'LANCE'})
    
    paragon_mace = Weapon.Weapon(name = '3x Maces',
                    count = 3,
                    attacks = 3,
                    skill = 3,
                    strength = 12,
                    AP = -1,
                    damage = 3,
                    abilities = {})
    
    paragon_mace_vs_big = Weapon.Weapon(name = '3x Maces vs Mon/Veh',
                    count = 3,
                    attacks = 3,
                    skill = 2,
                    strength = 12,
                    AP = -1,
                    damage = 3,
                    abilities = {'LANCE'})
    
    exorcist_missiles = Weapon.Weapon(name = 'Exorcist Missiles',
                    count = 1,
                    attacks = 'D6_PLUS_2',
                    skill = 3,
                    strength = 11,
                    AP = -3,
                    damage = 'D6',
                    abilities = {'INDIRECT FIRE'})
    
    AP1_mace = Weapon.Weapon(name = 'AP-1 Maces',
                    count = 10,
                    attacks = 3,
                    skill = 3,
                    strength = 4,
                    AP = -1,
                    damage = 2,
                    abilities = {'LETHAL HITS'})
    
    AP2_mace = Weapon.Weapon(name = 'AP-2 Maces',
                    count = 10,
                    attacks = 3,
                    skill = 3,
                    strength = 4,
                    AP = -2,
                    damage = 2,
                    abilities = {'LETHAL HITS'})
    
    AP2_halberd = Weapon.Weapon(name = 'AP-2 Halberds',
                    count = 10,
                    attacks = 3,
                    skill = 3,
                    strength = 5,
                    AP = -2,
                    damage = 1,
                    abilities = {'SUSTAINED HITS 1'})
    
    AP3_halberd = Weapon.Weapon(name = 'AP-3 Halberds',
                    count = 10,
                    attacks = 3,
                    skill = 3,
                    strength = 5,
                    AP = -3,
                    damage = 1,
                    abilities = {'SUSTAINED HITS 1'})
    
    arco_flails = Weapon.Weapon(name = '10x Arco Flails',
                    count = 10,
                    attacks = 4,
                    skill = 4,
                    strength = 5,
                    AP = 0,
                    damage = 1,
                    abilities = {'SUSTAINED HITS 1'})
    
    twin_buzz_blades = Weapon.Weapon(name = 'Twin Buzz Blades',
                    count = 1,
                    attacks = 4,
                    skill = 3,
                    strength = 10,
                    AP = -3,
                    damage = 2,
                    abilities = {'SUSTAINED HITS 1', 'TWIN-LINKED'})

    # Create units
    doms = Unit.Unit(name = '10x Dominions',
               model_count = 10,
               toughness = 3,
               wounds = 1,
               armor = 3,
               invul = 6,
               keywords = {'INFANTRY'},
               weapons =  {bolterX5, storm_bolterX4, flamerX4, meltagunX4},
               points = 115)
    
    rets = Unit.Unit(name = '5x Rets',
               model_count = 5,
               toughness = 3,
               wounds = 1,
               armor = 3,
               invul = 6,
               keywords = {'INFANTRY'},
               weapons =  {heavy_bolterX4, multi_meltaX4, heavy_flamerX4},
               points = 125)
    
    paragons = Unit.Unit(name = '3x Paragons',
               model_count = 3,
               toughness = 7,
               wounds = 4,
               armor = 2,
               invul = 4,
               keywords = {'VEHICLE', 'WALKER'},
               weapons =  {paragon_MM, paragon_krak, paragon_sword, paragon_sword_vs_big, paragon_mace, paragon_mace_vs_big},
               points = 210)
    
    exorcist = Unit.Unit(name = 'Exorcist',
               model_count = 1,
               toughness = 10,
               wounds = 11,
               armor = 3,
               invul = 6,
               keywords = {'VEHICLE'},
               weapons =  {exorcist_missiles},
               points = 190)
    
    sacsX10 = Unit.Unit(name = '10x Sacresants',
               model_count = 5,
               toughness = 3,
               wounds = 1,
               armor = 3,
               invul = 4,
               keywords = {'INFANTRY'},
               weapons =  {AP1_mace, AP2_mace, AP2_halberd, AP3_halberd},
               points = 150)
    
    arcosX10 = Unit.Unit(name = '10x Arcos',
               model_count = 10,
               toughness = 3,
               wounds = 2,
               armor = 7,
               invul = 6,
               keywords = {'INFANTRY'},
               weapons =  {arco_flails},
               points = 150)
    
    mortifierX1 = Unit.Unit(name = '1x Mortifier',
               model_count = 1,
               toughness = 6,
               wounds = 5,
               armor = 3,
               invul = 6,
               keywords = {'INFANTRY'},
               weapons =  {twin_buzz_blades},
               points = 70)
    

    # Defender defaults
    d_GEQ = Unit.Unit(name = '10x GEQ',
               model_count = 10,
               toughness = 3,
               wounds = 1,
               armor = 5,
               invul = None,
               keywords = {'INFANTRY'},
               weapons =  {})
    
    d_MEQ = Unit.Unit(name = '5x MEQ',
               model_count = 5,
               toughness = 4,
               wounds = 2,
               armor = 3,
               invul = None,
               keywords = {'INFANTRY'},
               weapons =  {})
    
    d_TEQ = Unit.Unit(name = '5x TEQ',
               model_count = 5,
               toughness = 5,
               wounds = 3,
               armor = 2,
               invul = 4,
               keywords = {'INFANTRY'},
               weapons =  {})
    
    d_VEQ = Unit.Unit(name = '1x VEQ',
               model_count = 1,
               toughness = 10,
               wounds = 12,
               armor = 3,
               invul = None,
               keywords = {'VEHICLE'},
               weapons =  {})
    
    d_KEQ = Unit.Unit(name = '1x KEQ',
               model_count = 1,
               toughness = 12,
               wounds = 22,
               armor = 2,
               invul = 5,
               keywords = {'VEHICLE', 'TITANIC'},
               weapons =  {})

    attacker_list = [doms, rets, paragons, exorcist, sacsX10, arcosX10, mortifierX1]
    defender_list = [d_GEQ, d_MEQ, d_TEQ, d_VEQ, d_KEQ]

    return attacker_list, defender_list
# End initialize()


def update_attacker_listbox(attacker_list, attacker_listbox):
    attacker_listbox.delete('0', 'end')
    index = 0
    for attacker in attacker_list:
        attacker_listbox.insert(f'{index}', attacker.name)
        index += 1
# End update_attacker_listbox()


def update_weapon_listbox(attacker_list, weapon_listbox, selected_attacker):
    weapon_listbox.delete('0', 'end')
    index = 0
    for weapon in attacker_list[selected_attacker].weapons:
        weapon_listbox.insert(f'{index}', weapon.name)
        index += 1
# End update_weapon_listbox()


def update_defender_listbox(defender_list, defender_listbox):
    defender_listbox.delete('0', 'end')
    index = 0
    for defender in defender_list:
        defender_listbox.insert(f'{index}', defender.name)
        index += 1
# End update_defender_listbox()


def add_attacker_to_list(attacker_list, attacker_listbox, name, model_count, toughness,
                         wounds, armor, invul, abilities, keywords):
    attacker = Unit.Unit(name, model_count, toughness, wounds, armor, invul, abilities, keywords, weapons={})

    attacker_list.append(attacker)
    update_attacker_listbox(attacker_list, attacker_listbox)
# End add_attacker_to_list()


def remove_attacker_from_list(attacker_list, attacker_listbox, weapon_listbox, weapon_stats_listbox, selected_attacker):
    del attacker_list[selected_attacker]
    weapon_listbox.delete('0', 'end')
    weapon_stats_listbox.delete('0', 'end')
    update_attacker_listbox(attacker_list, attacker_listbox)
# End remove_attacker_from_list()


def add_weapon_to_attacker(attacker_list, weapon_listbox, selected_attacker, name,
                           count, attacks, skill, strength, AP, damage, abilities):
    new_weapon = Weapon.Weapon(name, int(count), attacks, int(skill), int(strength), int(AP), damage, abilities)
    attacker_list[selected_attacker].add_weapon(new_weapon)

    update_weapon_listbox(attacker_list, weapon_listbox, selected_attacker)
# End add_weapon_to_attacker()


def remove_weapon(attacker_list, weapon_listbox, selected_attacker, selected_weapon, weapon_stats_listbox):
    weapon_to_remove = weapon_listbox.get(selected_weapon)
    attacker_list[selected_attacker].remove_weapon(weapon_to_remove)
    weapon_stats_listbox.delete('0', 'end')
    update_weapon_listbox(attacker_list, weapon_listbox, selected_attacker)
# End remove_weapon()


def add_defender_to_list(defender_list, defender_listbox, name, model_count, toughness,
                         wounds, armor, invul, abilities, keywords):
    # TO-DO: Make a more robust type checking thing here
    if invul == '':
        invul = None
    else:
        invul = int(invul)
    defender = Unit.Unit(name, int(model_count), int(toughness), int(wounds), int(armor), invul, abilities, keywords, weapons={})

    defender_list.append(defender)
    update_defender_listbox(defender_list, defender_listbox)
# End add_attacker_to_list()


def remove_defender_from_list(defender_list, defender_listbox, defender_stats_listbox, selected_defender):
    del defender_list[selected_defender]
    defender_stats_listbox.delete('0', 'end')
    update_defender_listbox(defender_list, defender_listbox)
# End remove_defender_from_list()