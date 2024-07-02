#################################################
# Warhammer 40k 10th Edition combat calculator  #
#                                               #
# Engineer: Addison Powell                      #
# Start Date: 5/31/2024                         #
#################################################

import data_manage as data_man
import calc_functions as calc
import run_functions as run_func
import AddAttackerWindow as AddAttackerWindow
import tkinter as tk
import tkinter.ttk as ttk
import subprocess
import threading




###############################
#        GUI Functions        #
###############################

def attacker_select(event, G_SELECTED_ATTACKER, attacker_listbox, attacker_list, weapon_listbox):
    if attacker_listbox.curselection() != ():
        G_SELECTED_ATTACKER.set(attacker_listbox.curselection()[0])

        box_index = 0
        weapon_listbox.delete(0, tk.END)
        for weapon in attacker_list[G_SELECTED_ATTACKER.get()].weapons:
            weapon_listbox.insert(box_index, weapon.name)
            box_index += 1
# End attacker_select()

def weapon_select(event, G_SELECTED_ATTACKER, G_SELECTED_WEAPON, 
                  weapon_listbox, attacker_list, weapon_stats_listbox):
    if weapon_listbox.curselection() != ():
        G_SELECTED_WEAPON.set(weapon_listbox.curselection()[0])
        selected_weapon_name = weapon_listbox.get(G_SELECTED_WEAPON.get())

        attacker = attacker_list[G_SELECTED_ATTACKER]
        for weapon in attacker.weapons:
            if weapon.name == selected_weapon_name:
                weapon_stats_listbox.delete(0, tk.END)
                weapon_stats_listbox.insert('0', f'{weapon.count}x{weapon.attacks} attacks')
                weapon_stats_listbox.insert('1', f'Hitting on {weapon.skill}+')
                weapon_stats_listbox.insert('2', f'S{weapon.strength} AP{weapon.AP} {weapon.damage}D')
                weapon_stats_listbox.insert('3', f'Abilities:')
                sub_index = 4
                for ability in weapon.abilities:
                    weapon_stats_listbox.insert(f'{sub_index}', f'{ability}')
                    sub_index += 1
# End attacker_select()


def defender_select(event, G_SELECTED_DEFENDER, defender_listbox, defender_list, defender_stats_listbox):
    if defender_listbox.curselection() != ():
        G_SELECTED_DEFENDER = defender_listbox.curselection()[0]

        defender_stats_listbox.delete(0, tk.END)
        defender_stats_listbox.insert('0', f'Model Count: {defender_list[G_SELECTED_DEFENDER].model_count}')
        defender_stats_listbox.insert('1', f'T{defender_list[G_SELECTED_DEFENDER].toughness} {defender_list[G_SELECTED_DEFENDER].wounds}W')
        defender_stats_listbox.insert('2', f'{defender_list[G_SELECTED_DEFENDER].armor}+/{defender_list[G_SELECTED_DEFENDER].invul}++')
        defender_stats_listbox.insert('3', f'Keywords:')
        sub_index = 4
        for keyword in defender_list[G_SELECTED_DEFENDER].keywords:
            defender_stats_listbox.insert(f'{sub_index}', f'{keyword}')
            sub_index += 1
# End defender_select()


def thread_run_all(results_text, attacker_list, defender_list,
                   half_range, indirect, stationary, charged, cover):
    """ Creates the sub-thread to run all attackers against all defenders """

    t1 = threading.Thread(target = run_func.run_all, args = (results_text, attacker_list, defender_list,
                                                    half_range, indirect, stationary, charged, cover))
    t1.start()
# End thread_run_all()


def thread_run_attacker(results_text, attacker_list, defender_list, G_SELECTED_ATTACKER,
                        half_range, indirect, stationary, charged, cover):
    """ Creates the sub-thread to run the selected attacker against all defenders """

    t2 = threading.Thread(target = run_func.run_attacker, args = (results_text, attacker_list, defender_list, G_SELECTED_ATTACKER,
                                                         half_range, indirect, stationary, charged, cover))
    t2.start()
# End thread_run_attacker()


def thread_run_weapon(results_text, attacker_list, defender_list, weapon_listbox, G_SELECTED_ATTACKER, G_SELECTED_WEAPON,
                      half_range, indirect, stationary, charged, cover):
    """ Creates the sub-thread to run the selected weapon against all defenders """

    t3 = threading.Thread(target = run_func.run_weapon, args = (results_text, attacker_list, defender_list, weapon_listbox,
                                                       G_SELECTED_ATTACKER, G_SELECTED_WEAPON,
                                                       half_range, indirect, stationary, charged, cover))
    t3.start()
# End thread_run_weapon()

def populate_attacker_listbox(attacker_list, attacker_listbox):
    index = 0
    for attacker in attacker_list:
        attacker_listbox.insert(f'{index}', attacker.name)
        index += 1
# End populate_attacker_listbox()


def populate_defender_listbox(defender_list, defender_listbox):
    index = 0
    for defender in defender_list:
        defender_listbox.insert(f'{index}', defender.name)
        index += 1
# End populate_attacker_listbox()


def main():
    attacker_list, defender_list = data_man.initialize()
    # results_dict = run_all(attacker_list, defender_list)


    #############################
    #    User Interface setup   #
    #############################

    root = tk.Tk()
    root.title('PyHammer 10E')
    G_HALF_RANGE = tk.BooleanVar(root)
    G_INDIRECT = tk.BooleanVar(root)
    G_COVER = tk.BooleanVar(root)
    G_STATIONARY = tk.BooleanVar(root)
    G_CHARGED = tk.BooleanVar(root)
    G_SELECTED_ATTACKER = tk.IntVar(root)
    G_SELECTED_WEAPON = tk.IntVar(root)
    G_SELECTED_DEFENDER = tk.IntVar(root)
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
    

    # Defender frame
    defender_frame = ttk.Frame(root, style = 'default.TFrame')
    defender_label = ttk.Label(defender_frame, text = 'Defender Units', style = 'default.TLabel')
    defender_stats_label = ttk.Label(defender_frame, text = 'Defender Stats', style = 'default.TLabel')
    defender_listbox = tk.Listbox(defender_frame, height = 10, font = default_font)
    defender_stats_listbox = tk.Listbox(defender_frame, height = 10, font = default_font)


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
    add_attacker_unit_button = ttk.Button(db_function_frame, text = 'Add Attacker Unit', style = 'default.TButton',
                                          command = lambda: AddAttackerWindow.AddAttackerWindow())
    add_attacker_weapon_button = ttk.Button(db_function_frame, text = 'Add Attacker Weapon', style = 'default.TButton')
    remove_attacker_unit_button = ttk.Button(db_function_frame, text = 'Remove Attacker Unit', style = 'default.TButton')
    remove_attacker_weapon_button = ttk.Button(db_function_frame, text = 'Remove Attacker Weapon', style = 'default.TButton')
    add_defender_unit_button = ttk.Button(db_function_frame, text = 'Add Defender Unit', style = 'default.TButton')
    remove_defender_unit_button = ttk.Button(db_function_frame, text = 'Remove Defender Unit', style = 'default.TButton')


    # Calculation buttons
    calculate_frame = ttk.Frame(root, style = 'default.TFrame')
    calculate_all = ttk.Button(calculate_frame, text = 'Calculate All',
                               command = lambda: thread_run_all(results_text, attacker_list, defender_list,
                                                                G_HALF_RANGE.get(), G_INDIRECT.get(), G_STATIONARY.get(),
                                                                G_CHARGED.get(), G_COVER.get()),
                               style = 'default.TButton')
    calculate_attacker = ttk.Button(calculate_frame,
                                    text = 'Calculate Attacker',
                                    command = lambda: thread_run_attacker(results_text, attacker_list, defender_list,
                                                                          G_SELECTED_ATTACKER.get(), G_HALF_RANGE.get(),
                                                                          G_INDIRECT.get(), G_STATIONARY.get(), G_CHARGED.get(), G_COVER.get()),
                                    style = 'default.TButton')
    calculate_weapon = ttk.Button(calculate_frame,
                                  text = 'Calculate Weapon',
                                  command = lambda: thread_run_weapon(results_text, attacker_list, defender_list, weapon_listbox, G_SELECTED_ATTACKER.get(),
                                                                      G_SELECTED_WEAPON.get(), G_HALF_RANGE.get(), G_INDIRECT.get(), G_STATIONARY.get(),
                                                                      G_CHARGED.get(), G_COVER.get()),
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

    # Populate listboxes
    populate_attacker_listbox(attacker_list, attacker_listbox)
    populate_defender_listbox(defender_list, defender_listbox)


    # Event handling
    attacker_listbox.bind('<<ListboxSelect>>', lambda event: attacker_select(event, G_SELECTED_ATTACKER, attacker_listbox, attacker_list, weapon_listbox))
    weapon_listbox.bind('<<ListboxSelect>>', lambda event: weapon_select(event, G_SELECTED_ATTACKER.get(), G_SELECTED_WEAPON, weapon_listbox, attacker_list, weapon_stats_listbox))
    defender_listbox.bind('<<ListboxSelect>>', lambda event: defender_select(event, G_SELECTED_DEFENDER, defender_listbox, defender_list, defender_stats_listbox))
    root.mainloop()

if __name__ == '__main__':
    main()