import Weapon

class Unit:
    """ Class defining a unit """
    def __init__(self, name=None, model_count=None, toughness=None,
                 wounds=None, armor=None, invul=None, abilities={},
                 keywords={}, weapons={}, points=1):
        self.name = name
        self.model_count = model_count
        self.toughness = toughness
        self.wounds = wounds
        self.armor = armor
        self.invul = invul
        self.abilities = abilities
        self.keywords = keywords
        self.weapons = weapons
        self.points = points

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
        if isinstance(weapon, Weapon.Weapon):
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
            'Weapons': f'{weapon_list}',
            'Points': f'{self.points}'
        }

        return report
# End Unit class