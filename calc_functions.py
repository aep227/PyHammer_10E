import math

# Probabilites, no rerolls
P2 = 0.833
P3 = 0.667
P4 = 0.500
P5 = 0.333
P6 = 0.167
# Probabilties, rerolling 1s
P2_RR1 = 0.972
P3_RR1 = 0.778
P4_RR1 = 0.583
P5_RR1 = 0.389
P6_RR1 = 0.195
# Probabilities, rerolling all
P2_RRA = 0.972
P3_RRA = 0.889
P4_RRA = 0.750
P5_RRA = 0.556
P6_RRA = 0.306

# Random value averages
RANDOM_VALUE_AVGS = {
    'D3': 2,
    '2D3': 4,
    'D6': 3.5,
    '2D6': 7,
    'D3_PLUS_3': 5,
    'D6_PLUS_1': 4.5,
    'D6_PLUS_2': 5.5,
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


def calc_hits_avg(weapon, defender, half_range, indirect, stationary):
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
        if 'RAPID FIRE' in ability and half_range == True:
            value = ability[-2:].strip()
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
            value = ability[-2:].strip()
            if value == 'D3':
                value = 2
            sustained = (attacks * P6) * int(value)
        else:
            sustained = 0
    
    # Determine target number
    skill_mod = 0
    if stationary == True and 'HEAVY' in weapon.abilities:
        skill_mod -= 1
    if 'STEALTH' in defender.abilities:
        skill_mod += 1
    if indirect == True and 'INDIRECT FIRE' in weapon.abilities:
        skill_mod += 1

    # Cap skill modification to +/- 1
    if skill_mod > 1:
        skill_mod = 1
    elif skill_mod < -1:
        skill_mod = -1
    
    mod_skill = weapon.skill + skill_mod

    # Cap target number. Indirect capped at 4+ to hit at best now
    if indirect == True and 'INDIRECT FIRE' in weapon.abilities:
        if mod_skill < 4:
            mod_skill = 4
        elif mod_skill > 6:
            mod_skill = 6
    else:
        if mod_skill < 2:
            mod_skill = 2
        elif mod_skill > 6:
            mod_skill = 6

    # Removes the 6s that already wounded
    if 'LETHAL HITS' in weapon.abilities:
        mod_skill += 1

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

    return float('{0:.2f}'.format(hits+sustained)), float('{0:.2f}'.format(lethals))
# End calc_hits_avg()


def calc_wounds_avg(hits, lethals, weapon, defender, charged):
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
    if 'LANCE' in weapon.abilities and charged == True:
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

    return float('{0:.2f}'.format(wounds)), float('{0:.2f}'.format(dev_wounds))
# End calc_wounds_avg()


def calc_unsaved_avg(wounds, dev_wounds, weapon, defender, cover):
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
    if cover and 'IGNORES COVER' not in weapon.abilities:
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
    elif save < 2:
        save = 2

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

    return float('{0:.2f}'.format(unsaved))
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

    return float('{0:.2f}'.format(slain))
# End calc_slain_avg()