import Weapon
import Unit

#########################
#    Data Management    #
#########################

def initialize():
    """ 
    Set up Unit and Weapon instances
     
    returns - list of units
    """

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
    
    paragon_MM = Weapon.Weapon(name = '3x Multimeltas',
                    count = 3,
                    attacks = 2,
                    skill = 2,
                    strength = 10,
                    AP = -4,
                    damage = 'D6',
                    abilities = {'MELTA 2', 'LANCE'})
    
    paragon_krak = Weapon.Weapon(name = '3x Krak Grenades',
                    count = 3,
                    attacks = 1,
                    skill = 2,
                    strength = 10,
                    AP = -2,
                    damage = 'D3',
                    abilities = {'TWIN-LINKED', 'LANCE'})
    
    exorcist_missiles = Weapon.Weapon(name = 'Exorcist Missiles',
                    count = 1,
                    attacks = 'D6_PLUS_2',
                    skill = 3,
                    strength = 11,
                    AP = -3,
                    damage = 'D6',
                    abilities = {'INDIRECT FIRE'})
    
    sac_mace = Weapon.Weapon(name = 'Sacresant Maces',
                    count = 5,
                    attacks = 3,
                    skill = 3,
                    strength = 4,
                    AP = -1,
                    damage = 2,
                    abilities = {'LETHAL HITS'})
    
    sac_halberd = Weapon.Weapon(name = 'Sacresant Halberds',
                    count = 5,
                    attacks = 3,
                    skill = 3,
                    strength = 5,
                    AP = -2,
                    damage = 1,
                    abilities = {'SUSTAINED HITS 1'})

    # Create units
    doms = Unit.Unit(name = '10x Dominions',
               model_count = 10,
               toughness = 3,
               wounds = 1,
               armor = 3,
               invul = 6,
               keywords = {'INFANTRY'},
               weapons =  {bolterX5, storm_bolterX4, flamerX4, meltagunX4})
    
    rets = Unit.Unit(name = '5x Rets',
               model_count = 5,
               toughness = 3,
               wounds = 1,
               armor = 3,
               invul = 6,
               keywords = {'INFANTRY'},
               weapons =  {heavy_bolterX4, multi_meltaX4, heavy_flamerX4})
    
    paragons = Unit.Unit(name = '3x Paragons',
               model_count = 3,
               toughness = 7,
               wounds = 4,
               armor = 2,
               invul = 4,
               keywords = {'VEHICLE', 'WALKER'},
               weapons =  {paragon_MM, paragon_krak})
    
    exorcist = Unit.Unit(name = 'Exorcist',
               model_count = 1,
               toughness = 10,
               wounds = 11,
               armor = 3,
               invul = 6,
               keywords = {'VEHICLE'},
               weapons =  {exorcist_missiles})
    
    sacsX5 = Unit.Unit(name = '5x Sacresants',
               model_count = 5,
               toughness = 3,
               wounds = 1,
               armor = 3,
               invul = 4,
               keywords = {'INFANTRY'},
               weapons =  {sac_mace, sac_halberd})
    

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

    attacker_list = [doms, rets, paragons, exorcist, sacsX5]
    defender_list = [d_GEQ, d_MEQ, d_TEQ, d_VEQ, d_KEQ]

    return attacker_list, defender_list
# End initialize()


def create_unit():
    pass
# End create_unit()


def remove_unit():
    pass
# End remove_unit()


def create_weapon():
    pass
# End create_weapon()


def remove_weapon():
    pass
# End remove_weapon()


def create_defender():
    pass
# End create_defender()


def remove_defender():
    pass
# End remove_defender()