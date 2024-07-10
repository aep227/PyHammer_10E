import calc_functions as calc
import tkinter as tk
import tkinter.ttk as ttk
from prettytable import PrettyTable
from prettytable import SINGLE_BORDER

###################################
#    Calculation Run Functions    #
###################################

def run_all(results_text, attacker_list, defender_list,
            half_range, indirect, stationary, charged, cover,
            calc_efficiency):
    results_dict = {}
    # Calculate average models slain
    for attacker in attacker_list:
        if attacker not in results_dict:
            results_dict[attacker.name] = {}

        for weapon in attacker.weapons:
            if weapon not in results_dict[attacker.name]:
                results_dict[attacker.name][weapon.name] = {}

            for defender in defender_list:
                if weapon not in results_dict[attacker.name][weapon.name]:
                    results_dict[attacker.name][weapon.name][defender.name] = {}

                avg_hits, avg_lethals = calc.calc_hits_avg(weapon, defender, 
                                                           half_range, indirect, stationary)
                results_dict[attacker.name][weapon.name][defender.name]['Avg Hits'] = avg_hits
    
                avg_wounds, avg_dev_wounds = calc.calc_wounds_avg(avg_hits, avg_lethals, weapon, defender,
                                                                  charged)
                results_dict[attacker.name][weapon.name][defender.name]['Avg Wounds'] = avg_wounds

                avg_unsaved = calc.calc_unsaved_avg(avg_wounds, avg_dev_wounds, weapon, defender,
                                                    cover)
                results_dict[attacker.name][weapon.name][defender.name]['Avg Unsaved'] = avg_unsaved

                avg_slain = calc.calc_slain_avg(avg_unsaved, weapon, defender)
                results_dict[attacker.name][weapon.name][defender.name]['Avg Slain'] = avg_slain

    table = PrettyTable()
    table.set_style(SINGLE_BORDER)

    if calc_efficiency:
        header_row = ['Weapon Points/Kill']
    else:
        header_row = ['Weapon']

    for defender in defender_list:
        header_row.append(defender.name)

    table.field_names = header_row

    attacker_index = 1
    for attacker in results_dict:
        # Attacker divider
        attacker_title = [f'{attacker}']
        for defender in defender_list:
            attacker_title.append('')
        table.add_row(attacker_title)

        for weapon in results_dict[f'{attacker}']:
            row = [f'{weapon}']

            if calc_efficiency:
                for defender in results_dict[f'{attacker}'][f'{weapon}']:
                    # Determine attacker object in list from attacker name
                    for unit in attacker_list:
                        if unit.name == attacker:
                            attacker_obj = unit

                    slain = results_dict[f'{attacker}'][f'{weapon}'][f'{defender}']['Avg Slain']

                    if slain != 0:
                        efficiency = attacker_obj.points / slain
                    else:
                        efficiency = 0
                    efficiency = float('{0:.2f}'.format(efficiency))
                    row.append(efficiency)
            else:
                for defender in results_dict[f'{attacker}'][f'{weapon}']:
                    row.append(results_dict[f'{attacker}'][f'{weapon}'][f'{defender}']['Avg Slain'])
                    
            table.add_row(row)

        
        # Blank row for next attacker
        if len(results_dict.keys()) > 1 and attacker_index != len(results_dict.keys()):
            blank_row = [f'']
            for defender in defender_list:
                blank_row.append('')
            table.add_row(blank_row)
            attacker_index += 1
        
    results_text.config(state = 'normal')
    results_text.delete('1.0', tk.END)
    results_text.insert('1.0', table)
    results_text.see(tk.END)
    results_text.config(state = 'disabled')
# End run_all()


def run_attacker(results_text, attacker_list, defender_list, G_SELECTED_ATTACKER,
                 half_range, indirect, stationary, charged, cover, calc_efficiency):
    attacker = attacker_list[G_SELECTED_ATTACKER]
    results_dict = {}
    results_dict[attacker.name] = {}
    table = PrettyTable()
    table.set_style(SINGLE_BORDER)
    
    if calc_efficiency:
        header_row = ['Weapon Points/Kill']
    else:
        header_row = ['Weapon']

    for defender in defender_list:
        header_row.append(defender.name)
    table.field_names = header_row

    for weapon in attacker.weapons:
        if weapon not in results_dict[attacker.name]:
            results_dict[attacker.name][weapon.name] = {}

        for defender in defender_list:
            if weapon not in results_dict[attacker.name][weapon.name]:
                results_dict[attacker.name][weapon.name][defender.name] = {}

            avg_hits, avg_lethals = calc.calc_hits_avg(weapon, defender, 
                                                        half_range, indirect, stationary)
            results_dict[attacker.name][weapon.name][defender.name]['Avg Hits'] = avg_hits

            avg_wounds, avg_dev_wounds = calc.calc_wounds_avg(avg_hits, avg_lethals, weapon, defender,
                                                                charged)
            results_dict[attacker.name][weapon.name][defender.name]['Avg Wounds'] = avg_wounds

            avg_unsaved = calc.calc_unsaved_avg(avg_wounds, avg_dev_wounds, weapon, defender,
                                                cover)
            results_dict[attacker.name][weapon.name][defender.name]['Avg Unsaved'] = avg_unsaved

            avg_slain = calc.calc_slain_avg(avg_unsaved, weapon, defender)
            results_dict[attacker.name][weapon.name][defender.name]['Avg Slain'] = avg_slain
    
    attacker_title = [f'{attacker.name}']
    for defender in defender_list:
        attacker_title.append('')
    table.add_row(attacker_title)

    for weapon in results_dict[f'{attacker.name}']:
        row = [f'{weapon}']

        if calc_efficiency:
            for defender in results_dict[f'{attacker.name}'][f'{weapon}']:

                slain = results_dict[f'{attacker.name}'][f'{weapon}'][f'{defender}']['Avg Slain']

                if slain != 0:
                    efficiency = attacker.points / slain
                else:
                    efficiency = 0
                efficiency = float('{0:.2f}'.format(efficiency))
                row.append(efficiency)
        else:
            for defender in results_dict[f'{attacker.name}'][f'{weapon}']:
                row.append(results_dict[f'{attacker.name}'][f'{weapon}'][f'{defender}']['Avg Slain'])

        table.add_row(row)

    results_text.config(state = 'normal')
    results_text.delete('1.0', tk.END)
    results_text.insert('1.0', table)
    results_text.see(tk.END)
    results_text.config(state = 'disabled')
# End run_attacker()


def run_weapon(results_text, attacker_list, defender_list, weapon_listbox, G_SELECTED_ATTACKER, G_SELECTED_WEAPON,
               half_range, indirect, stationary, charged, cover, calc_efficiency):
    attacker = attacker_list[G_SELECTED_ATTACKER]
    for weapon_check in attacker.weapons:
        w_listbox_check = weapon_listbox.get(G_SELECTED_WEAPON)
        if w_listbox_check == weapon_check.name:
            weapon = weapon_check
    results_dict = {}
    results_dict[attacker.name] = {}
    results_dict[attacker.name][weapon.name] = {}
    table = PrettyTable()
    table.set_style(SINGLE_BORDER)

    if calc_efficiency:
        header_row = ['Weapon Points/Kill']
    else:
        header_row = ['Weapon']

    for defender in defender_list:
        header_row.append(defender.name)
    table.field_names = header_row

    for defender in defender_list:
        if weapon not in results_dict[attacker.name][weapon.name]:
            results_dict[attacker.name][weapon.name][defender.name] = {}

        avg_hits, avg_lethals = calc.calc_hits_avg(weapon, defender, 
                                                    half_range, indirect, stationary)
        results_dict[attacker.name][weapon.name][defender.name]['Avg Hits'] = avg_hits

        avg_wounds, avg_dev_wounds = calc.calc_wounds_avg(avg_hits, avg_lethals, weapon, defender,
                                                            charged)
        results_dict[attacker.name][weapon.name][defender.name]['Avg Wounds'] = avg_wounds

        avg_unsaved = calc.calc_unsaved_avg(avg_wounds, avg_dev_wounds, weapon, defender,
                                            cover)
        results_dict[attacker.name][weapon.name][defender.name]['Avg Unsaved'] = avg_unsaved

        avg_slain = calc.calc_slain_avg(avg_unsaved, weapon, defender)
        results_dict[attacker.name][weapon.name][defender.name]['Avg Slain'] = avg_slain
    
    attacker_title = [f'{attacker.name}']
    for defender in defender_list:
        attacker_title.append('')
    table.add_row(attacker_title)

    for weapon in results_dict[f'{attacker.name}']:
        row = [f'{weapon}']

        if calc_efficiency:
            for defender in results_dict[f'{attacker.name}'][f'{weapon}']:

                slain = results_dict[f'{attacker.name}'][f'{weapon}'][f'{defender}']['Avg Slain']

                if slain != 0:
                    efficiency = attacker.points / slain
                else:
                    efficiency = 0
                efficiency = float('{0:.2f}'.format(efficiency))
                row.append(efficiency)
        else:
            for defender in results_dict[f'{attacker.name}'][f'{weapon}']:
                row.append(results_dict[f'{attacker.name}'][f'{weapon}'][f'{defender}']['Avg Slain'])

        table.add_row(row)

    results_text.config(state = 'normal')
    results_text.delete('1.0', tk.END)
    results_text.insert('1.0', table)
    results_text.see(tk.END)
    results_text.config(state = 'disabled')
# End run_weapon()