#################################################
# Warhammer 40k 10th Edition combat calculator  #
#                                               #
# Engineer: Addison Powell                      #
# Start Date: 5/31/2024                         #
#################################################

import Weapon
import Unit
import calc_functions as calc
import tkinter as tk
import tkinter.ttk as ttk
import subprocess
import threading
from prettytable import PrettyTable
from prettytable import SINGLE_BORDER


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
    
    bolterX10 = Weapon.Weapon(name = '10x Bolter',
                    count = 10,
                    attacks = 1,
                    skill = 3,
                    strength = 4,
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

    # Create units
    doms = Unit.Unit(name = '10x Dominions',
               model_count = 10,
               toughness = 3,
               wounds = 1,
               armor = 3,
               invul = None,
               keywords = {'INFANTRY'},
               weapons =  {bolterX5, storm_bolterX4, flamerX4, meltagunX4})
    
    bss = Unit.Unit(name = '10x BSS',
               model_count = 10,
               toughness = 3,
               wounds = 1,
               armor = 3,
               invul = None,
               keywords = {'INFANTRY'},
               weapons =  {bolterX10})
    

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

    attacker_list = [doms, bss]
    defender_list = [d_GEQ, d_MEQ, d_TEQ, d_VEQ, d_KEQ]

    return attacker_list, defender_list
# End initialize()


def create_unit():
    pass
# End create_unit()


def create_weapon():
    pass
# End create_weapon()


def run_all(results_text, attacker_list, defender_list,
            half_range, indirect, stationary, charged, cover):
    results_dict = {}
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
        
    # print(table)

    results_text.config(state = 'normal')
    results_text.delete('1.0', tk.END)
    results_text.insert('1.0', table)
    results_text.see(tk.END)
    results_text.config(state = 'disabled')
# End run_all()

# TO-DO: Change attacker_list to a single attacker
def run_attacker(results_text, attacker_list, defender_list,
                 half_range, indirect, stationary, charged, cover):
    results_text.config(state = 'normal')
    results_text.delete('1.0', tk.END)
    results_text.insert('1.0', 'In run_attacker()')
    results_text.see(tk.END)
    results_text.config(state = 'disabled')
# End run_attacker()

# TO-DO: Change attacker_list to a single weapon
def run_weapon(results_text, attacker_list, defender_list,
               half_range, indirect, stationary, charged, cover):
    results_text.config(state = 'normal')
    results_text.delete('1.0', tk.END)
    results_text.insert('1.0', 'In run_weapon()')
    results_text.see(tk.END)
    results_text.config(state = 'disabled')
# End run_weapon()




###############################
#        GUI Functions        #
###############################

def attacker_select(event, attacker_listbox, attacker_list, weapon_listbox):
    if attacker_listbox.curselection() != ():
        attacker_index = attacker_listbox.curselection()[0]

        box_index = 0
        weapon_listbox.delete(0, tk.END)
        for weapon in attacker_list[attacker_index].weapons:
            weapon_listbox.insert(box_index, weapon.name)
            box_index += 1
        # print('You selected item %d: "%s"', value, value)
# End attacker_select()

def weapon_select(event, weapon_listbox, attacker_list, weapon_stats_listbox):
    if weapon_listbox.curselection() != ():
        weapon_index = weapon_listbox.curselection()[0]

        # Determine which attacker has the selected weapon
        # Known issue: if multiple weapons share the same name, this can't determine which
        # of the multiple weapons is the 'correct' one
        index = 0
        for attacker in attacker_list:
            for weapon in attacker.weapons:
                if weapon_listbox.get(weapon_index) == weapon.name:
                    weapon_stats_listbox.delete(0, tk.END)
                    weapon_stats_listbox.insert('0', f'{weapon.count}x{weapon.attacks} attacks')
                    weapon_stats_listbox.insert('1', f'Hitting on {weapon.skill}+')
                    weapon_stats_listbox.insert('2', f'S{weapon.strength} AP{weapon.AP} {weapon.damage}D')
                    weapon_stats_listbox.insert('3', f'Abilities:')
                    sub_index = 4
                    for ability in weapon.abilities:
                        weapon_stats_listbox.insert(f'{sub_index}', f'{ability}')
                        sub_index += 1

            index += 1

        # print('You selected item %d: "%s"', value, value)
# End attacker_select()


def thread_run_all(results_text, attacker_list, defender_list,
                   half_range, indirect, stationary, charged, cover):
    """ Creates the sub-thread to run all attackers against all defenders """

    t1 = threading.Thread(target = run_all, args = (results_text, attacker_list, defender_list,
                                                    half_range, indirect, stationary, charged, cover))
    t1.start()
# End thread_run_all()


def thread_run_attacker(results_text, attacker_list, defender_list,
                        half_range, indirect, stationary, charged, cover):
    """ Creates the sub-thread to run the selected attacker against all defenders """

    t2 = threading.Thread(target = run_attacker, args = (results_text, attacker_list, defender_list,
                                                         half_range, indirect, stationary, charged, cover))
    t2.start()
# End thread_run_attacker()


def thread_run_weapon(results_text, attacker_list, defender_list,
                      half_range, indirect, stationary, charged, cover):
    """ Creates the sub-thread to run the selected weapon against all defenders """

    t3 = threading.Thread(target = run_weapon, args = (results_text, attacker_list, defender_list,
                                                       half_range, indirect, stationary, charged, cover))
    t3.start()
# End thread_run_weapon()


def main():
    attacker_list, defender_list = initialize()
    # results_dict = run_all(attacker_list, defender_list)


    #############################
    #    User Interface setup   #
    #############################

    root = tk.Tk()
    G_HALF_RANGE = tk.BooleanVar(root)
    G_INDIRECT = tk.BooleanVar(root)
    G_COVER = tk.BooleanVar(root)
    G_STATIONARY = tk.BooleanVar(root)
    G_CHARGED = tk.BooleanVar(root)
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
    # for weapon in attacker_list[0].weapons:
    #     weapon_listbox.insert(f'{index}', weapon.name)
    #     if index == 0:
    #         weapon_stats_listbox.insert('0', f'Attacks: {weapon.attacks}')
    #         weapon_stats_listbox.insert('1', f'Skill: {weapon.skill}')
    #         weapon_stats_listbox.insert('2', f'Strength: {weapon.strength}')
    #         weapon_stats_listbox.insert('3', f'AP: {weapon.AP}')
    #         weapon_stats_listbox.insert('4', f'Damage: {weapon.damage}')
    #         weapon_stats_listbox.insert('5', f'Abilities: {weapon.abilities}')
    #     index += 1


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
    results_text = tk.Text(results_frame, height = 24, width = 80, font = default_font, state = 'disabled')
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
    calculate_all = ttk.Button(calculate_frame, text = 'Calculate All',
                               command = lambda: thread_run_all(results_text, attacker_list, defender_list,
                                                 G_HALF_RANGE.get(), G_INDIRECT.get(), G_STATIONARY.get(), G_CHARGED.get(), G_COVER.get()),
                               style = 'default.TButton')
    calculate_attacker = ttk.Button(calculate_frame,
                                    text = 'Calculate Attacker',
                                    command = lambda: thread_run_attacker(results_text, attacker_list, defender_list,
                                                      G_HALF_RANGE.get(), G_INDIRECT.get(), G_STATIONARY.get(), G_CHARGED.get(), G_COVER.get()),
                                    style = 'default.TButton')
    calculate_weapon = ttk.Button(calculate_frame,
                                  text = 'Calculate Weapon',
                                  command = lambda: thread_run_weapon(results_text, attacker_list, defender_list,
                                                    G_HALF_RANGE.get(), G_INDIRECT.get(), G_STATIONARY.get(), G_CHARGED.get(), G_COVER.get()),
                                  style = 'default.TButton')


    # Settings frame
    settings_frame = ttk.Frame(root, style = 'default.TFrame')
    half_range_check = ttk.Checkbutton(settings_frame, text = 'Attacker Half Range', variable = G_HALF_RANGE, style = 'default.TCheckbutton', offvalue = False, onvalue = True)
    indirect_check = ttk.Checkbutton(settings_frame, text = 'Attacker Indirect', variable = G_INDIRECT, style = 'default.TCheckbutton', offvalue = False, onvalue = True)
    stationary_check = ttk.Checkbutton(settings_frame, text = 'Attacker Stationary', variable = G_STATIONARY, style = 'default.TCheckbutton', offvalue = False, onvalue = True)
    charged_check = ttk.Checkbutton(settings_frame, text = 'Attacker Charged', variable = G_CHARGED, style = 'default.TCheckbutton', offvalue = False, onvalue = True)
    cover_check = ttk.Checkbutton(settings_frame, text = 'Defender in Cover', variable = G_COVER, style = 'default.TCheckbutton', offvalue = False, onvalue = True)


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

    # Lay out root window
    attacker_frame.grid(    row = 0, column = 0, columnspan = 2)
    defender_frame.grid(    row = 1, column = 0)
    results_frame.grid(     row = 0, column = 2, rowspan = 2)
    db_function_frame.grid( row = 2, column = 0, rowspan = 2)
    settings_frame.grid(    row = 2, column = 2)
    calculate_frame.grid(   row = 3, column = 2)


    # Event handling
    selected_attacker = None
    attacker_listbox.bind('<<ListboxSelect>>', lambda event: attacker_select(event, attacker_listbox, attacker_list, weapon_listbox))
    weapon_listbox.bind('<<ListboxSelect>>', lambda event: weapon_select(event, weapon_listbox, attacker_list, weapon_stats_listbox))
    root.mainloop()

if __name__ == '__main__':
    main()