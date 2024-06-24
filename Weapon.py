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