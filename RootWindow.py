import tkinter as tk
import tkinter.ttk as ttk
import AddAttackerWindow as AddAttackerWindowImport
import AddWeaponWindow as AddWeaponWindowImport
import AddDefenderWindow as AddDefenderWindowImport
import data_manage as data_man
import run_functions as run_func
import threading

class RootWindow(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        self.title('PyHammer 10E')
        self.G_HALF_RANGE = tk.BooleanVar(self)
        self.G_INDIRECT = tk.BooleanVar(self)
        self.G_COVER = tk.BooleanVar(self)
        self.G_STATIONARY = tk.BooleanVar(self)
        self.G_CHARGED = tk.BooleanVar(self)
        self.G_SELECTED_ATTACKER = tk.IntVar(self)
        self.G_SELECTED_WEAPON = tk.IntVar(self)
        self.G_SELECTED_DEFENDER = tk.IntVar(self)
        self.G_CALC_EFFICIENCY = tk.BooleanVar(self)
        self.std_font = ('Cascadia Code', '14')
        self.title_font = ('Cascadia Code', '18', 'bold')
        self.std_padding = 20

        self.s = ttk.Style()
        self.s.configure('default.TFrame', font = self.std_font)
        self.s.configure('title.TLabel', font = self.title_font)
        self.s.configure('default.TLabel', font = self.std_font)
        self.s.configure('default.TButton', font = self.std_font)
        self.s.configure('default.TCheckbutton', font = self.std_font)
        self.s.configure('spacer.TLabel', font = ('Cascadia Code', '16'))

        # Generate initial attacker and defender lists
        self.attacker_list, self.defender_list = data_man.initialize()

        # Attacker frame
        self.attacker_frame = ttk.Frame(self, style = 'default.TFrame')
        self.attacker_label = ttk.Label(self.attacker_frame, text = 'Attacker Units', style = 'default.TLabel')
        self.weapon_label = ttk.Label(self.attacker_frame, text = 'Attacker Weapons', style = 'default.TLabel')
        self.weapon_stats_label = ttk.Label(self.attacker_frame, text = 'Weapon Stats', style = 'default.TLabel')
        self.attacker_listbox = tk.Listbox(self.attacker_frame, height = 10, font = self.std_font)
        self.weapon_listbox = tk.Listbox(self.attacker_frame, height = 10, font = self.std_font)
        self.weapon_stats_listbox = tk.Listbox(self.attacker_frame, height = 10, font = self.std_font)
        

        # Defender frame
        self.defender_frame = ttk.Frame(self, style = 'default.TFrame')
        self.defender_label = ttk.Label(self.defender_frame, text = 'Defender Units', style = 'default.TLabel')
        self.defender_stats_label = ttk.Label(self.defender_frame, text = 'Defender Stats', style = 'default.TLabel')
        self.defender_listbox = tk.Listbox(self.defender_frame, height = 10, font = self.std_font)
        self.defender_stats_listbox = tk.Listbox(self.defender_frame, height = 10, font = self.std_font)


        # Results frame
        self.results_frame = ttk.Frame(self, style = 'default.TFrame')
        self.results_label = ttk.Label(self.results_frame, text = 'Results', style = 'default.TLabel')
        self.results_text = tk.Text(self.results_frame, height = 24, width = 80, font = self.std_font, state = 'disabled')
        self.results_scroll_y = ttk.Scrollbar(self.results_frame, orient = 'vertical', command = self.results_text.yview)
        self.results_scroll_x = ttk.Scrollbar(self.results_frame, orient = 'horizontal', command = self.results_text.xview)
        self.results_text.config(yscrollcommand=self.results_scroll_y.set)
        self.results_text.config(xscrollcommand=self.results_scroll_x.set)


        # Function buttons
        self.db_function_frame = ttk.Frame(self, style = 'default.TFrame')
        self.add_attacker_unit_button = ttk.Button(self.db_function_frame, text = 'Add Attacker Unit', style = 'default.TButton',
                                                   command = lambda: AddAttackerWindowImport.AddAttackerWindow(self.attacker_list, self.attacker_listbox,
                                                                                                               self.get_location_x(), self.get_location_y()))
        self.add_attacker_weapon_button = ttk.Button(self.db_function_frame, text = 'Add Attacker Weapon', style = 'default.TButton',
                                                     command = lambda: AddWeaponWindowImport.AddWeaponWindow(self.attacker_list, self.weapon_listbox,
                                                                                                               self.get_location_x(), self.get_location_y(),
                                                                                                               self.G_SELECTED_ATTACKER.get()))
        self.remove_attacker_unit_button = ttk.Button(self.db_function_frame, text = 'Remove Attacker Unit', style = 'default.TButton',
                                                      command = lambda: data_man.remove_attacker_from_list(self.attacker_list, self.attacker_listbox,
                                                                                                           self.weapon_listbox, self.weapon_stats_listbox,
                                                                                                           self.G_SELECTED_ATTACKER.get()))
        self.remove_attacker_weapon_button = ttk.Button(self.db_function_frame, text = 'Remove Attacker Weapon', style = 'default.TButton',
                                                        command = lambda: data_man.remove_weapon(self.attacker_list, self.weapon_listbox, 
                                                                                                 self.G_SELECTED_ATTACKER.get(), self.G_SELECTED_WEAPON.get(),
                                                                                                 self.weapon_stats_listbox))
        self.add_defender_unit_button = ttk.Button(self.db_function_frame, text = 'Add Defender Unit', style = 'default.TButton',
                                                   command = lambda: AddDefenderWindowImport.AddDefenderWindow(self.defender_list, self.defender_listbox,
                                                                                                               self.get_location_x(), self.get_location_y()))
        self.remove_defender_unit_button = ttk.Button(self.db_function_frame, text = 'Remove Defender Unit', style = 'default.TButton',
                                                      command = lambda: data_man.remove_defender_from_list(self.defender_list, self.defender_listbox,
                                                                                                           self.defender_stats_listbox, self.G_SELECTED_DEFENDER.get()))


        # Calculation buttons
        self.calculate_frame = ttk.Frame(self, style = 'default.TFrame')
        self.calculate_all = ttk.Button(self.calculate_frame, text = 'Calculate All',
                                command = lambda: self.thread_run_all(self.results_text, self.attacker_list, self.defender_list,
                                                                      self.G_HALF_RANGE.get(), self.G_INDIRECT.get(), self.G_STATIONARY.get(),
                                                                      self.G_CHARGED.get(), self.G_COVER.get(), self.G_CALC_EFFICIENCY.get()),
                                style = 'default.TButton')
        self.calculate_attacker = ttk.Button(self.calculate_frame,
                                        text = 'Calculate Attacker',
                                        command = lambda: self.thread_run_attacker(self.results_text, self.attacker_list, self.defender_list,
                                                                                   self.G_SELECTED_ATTACKER.get(), self.G_HALF_RANGE.get(),
                                                                                   self.G_INDIRECT.get(), self.G_STATIONARY.get(), self.G_CHARGED.get(),
                                                                                   self.G_COVER.get(), self.G_CALC_EFFICIENCY.get()),
                                        style = 'default.TButton')
        self.calculate_weapon = ttk.Button(self.calculate_frame,
                                    text = 'Calculate Weapon',
                                    command = lambda: self.thread_run_weapon(self.results_text, self.attacker_list, self.defender_list, self.weapon_listbox, self.G_SELECTED_ATTACKER.get(),
                                                                             self.G_SELECTED_WEAPON.get(), self.G_HALF_RANGE.get(), self.G_INDIRECT.get(), self.G_STATIONARY.get(),
                                                                             self.G_CHARGED.get(), self.G_COVER.get(), self.G_CALC_EFFICIENCY.get()),
                                    style = 'default.TButton')


        # Settings frame
        self.settings_frame = ttk.Frame(self, style = 'default.TFrame')
        self.half_range_check = ttk.Checkbutton(self.settings_frame, text = 'Attacker Half Range', variable = self.G_HALF_RANGE, style = 'default.TCheckbutton', offvalue = False, onvalue = True)
        self.indirect_check = ttk.Checkbutton(self.settings_frame, text = 'Attacker Indirect', variable = self.G_INDIRECT, style = 'default.TCheckbutton', offvalue = False, onvalue = True)
        self.stationary_check = ttk.Checkbutton(self.settings_frame, text = 'Attacker Stationary', variable = self.G_STATIONARY, style = 'default.TCheckbutton', offvalue = False, onvalue = True)
        self.charged_check = ttk.Checkbutton(self.settings_frame, text = 'Attacker Charged', variable = self.G_CHARGED, style = 'default.TCheckbutton', offvalue = False, onvalue = True)
        self.cover_check = ttk.Checkbutton(self.settings_frame, text = 'Defender in Cover', variable = self.G_COVER, style = 'default.TCheckbutton', offvalue = False, onvalue = True)
        self.efficiency_check = ttk.Checkbutton(self.settings_frame, text = 'Calculate Efficiency', variable = self.G_CALC_EFFICIENCY, style = 'default.TCheckbutton', offvalue = False, onvalue = True)


        # Lay out attacker frame
        self.attacker_label.grid(       row = 0, column = 0)
        self.weapon_label.grid(         row = 0, column = 1)
        self.weapon_stats_label.grid(   row = 0, column = 2)
        self.attacker_listbox.grid(     row = 1, column = 0, padx = self.std_padding, pady = self.std_padding)
        self.weapon_listbox.grid(       row = 1, column = 1)
        self.weapon_stats_listbox.grid( row = 1, column = 2, padx = self.std_padding, pady = self.std_padding)

        # Lay out defender frame
        self.defender_label.grid(         row = 0, column = 0)
        self.defender_stats_label.grid(   row = 0, column = 1)
        self.defender_listbox.grid(       row = 1, column = 0, padx = self.std_padding, pady = self.std_padding)
        self.defender_stats_listbox.grid( row = 1, column = 1)

        # Lay out settings frame
        self.half_range_check.grid(  row = 0, column = 0, padx = self.std_padding, sticky = 'w')
        self.indirect_check.grid(    row = 1, column = 0, padx = self.std_padding, sticky = 'w')
        self.stationary_check.grid(  row = 0, column = 1, padx = self.std_padding, sticky = 'w')
        self.charged_check.grid(     row = 1, column = 1, padx = self.std_padding, sticky = 'w')
        self.cover_check.grid(       row = 0, column = 2, padx = self.std_padding, sticky = 'w')
        self.efficiency_check.grid(  row = 1, column = 2, padx = self.std_padding, sticky = 'w')

        # Lay out results frame
        self.results_label.grid(    row = 0, column = 0)
        self.results_text.grid(     row = 1, column = 0)
        self.results_scroll_y.grid( row = 1, column = 1, sticky = 'nsw')
        self.results_scroll_x.grid( row = 2, column = 0, sticky = 'nwe')

        # Lay out function frame
        self.add_attacker_unit_button.grid(      row = 0, column = 0, padx = self.std_padding, pady = self.std_padding)
        self.add_attacker_weapon_button.grid(    row = 0, column = 1, padx = self.std_padding, pady = self.std_padding)
        self.add_defender_unit_button.grid(      row = 0, column = 2, padx = self.std_padding, pady = self.std_padding)
        self.remove_attacker_unit_button.grid(   row = 1, column = 0, padx = self.std_padding, pady = self.std_padding)
        self.remove_attacker_weapon_button.grid( row = 1, column = 1, padx = self.std_padding, pady = self.std_padding)
        self.remove_defender_unit_button.grid(   row = 1, column = 2, padx = self.std_padding, pady = self.std_padding)

        # Lay out calculation frame
        self.calculate_all.grid(      row = 0, column = 0, padx = self.std_padding, pady = self.std_padding)
        self.calculate_attacker.grid( row = 0, column = 1, padx = self.std_padding, pady = self.std_padding)
        self.calculate_weapon.grid(   row = 0, column = 2, padx = self.std_padding, pady = self.std_padding)

        # Lay out root window
        self.attacker_frame.grid(    row = 0, column = 0, columnspan = 2)
        self.defender_frame.grid(    row = 1, column = 0)
        self.results_frame.grid(     row = 0, column = 2, rowspan = 2)
        self.db_function_frame.grid( row = 2, column = 0, rowspan = 2)
        self.settings_frame.grid(    row = 2, column = 2)
        self.calculate_frame.grid(   row = 3, column = 2)

        # Event handling
        self.attacker_listbox.bind('<<ListboxSelect>>', lambda event: self.attacker_select(event, self.G_SELECTED_ATTACKER, self.attacker_listbox,
                                                                                           self.attacker_list, self.weapon_listbox, self.weapon_stats_listbox))
        
        self.weapon_listbox.bind('<<ListboxSelect>>', lambda event: self.weapon_select(event, self.G_SELECTED_ATTACKER.get(), self.G_SELECTED_WEAPON,
                                                                                       self.weapon_listbox, self.attacker_list, self.weapon_stats_listbox))
        
        self.defender_listbox.bind('<<ListboxSelect>>', lambda event: self.defender_select(event, self.G_SELECTED_DEFENDER, self.defender_listbox,
                                                                                           self.defender_list, self.defender_stats_listbox))

        # Populate listboxes with initial values
        self.populate_attacker_listbox(self.attacker_list, self.attacker_listbox)
        self.populate_defender_listbox(self.defender_list, self.defender_listbox)
    # End init()



    ###############################
    #     Threading Functions     #
    ###############################

    def thread_run_all(self, results_text, attacker_list, defender_list,
                half_range, indirect, stationary, charged, cover, calc_efficiency):
        """ Creates the sub-thread to run all attackers against all defenders """

        t1 = threading.Thread(target = run_func.run_all, args = (results_text, attacker_list, defender_list,
                                                half_range, indirect, stationary, charged, cover, calc_efficiency))
        t1.start()
    # End thread_run_all()


    def thread_run_attacker(self, results_text, attacker_list, defender_list, G_SELECTED_ATTACKER,
                            half_range, indirect, stationary, charged, cover, calc_efficiency):
        """ Creates the sub-thread to run the selected attacker against all defenders """

        t2 = threading.Thread(target = run_func.run_attacker, args = (results_text, attacker_list, defender_list, G_SELECTED_ATTACKER,
                                                            half_range, indirect, stationary, charged, cover, calc_efficiency))
        t2.start()
    # End thread_run_attacker()


    def thread_run_weapon(self, results_text, attacker_list, defender_list, weapon_listbox, G_SELECTED_ATTACKER, G_SELECTED_WEAPON,
                        half_range, indirect, stationary, charged, cover, calc_efficiency):
        """ Creates the sub-thread to run the selected weapon against all defenders """

        t3 = threading.Thread(target = run_func.run_weapon, args = (results_text, attacker_list, defender_list, weapon_listbox,
                                                        G_SELECTED_ATTACKER, G_SELECTED_WEAPON,
                                                        half_range, indirect, stationary, charged, cover, calc_efficiency))
        t3.start()
    # End thread_run_weapon()



    ###############################
    #        GUI Functions        #
    ###############################

    def attacker_select(self, event, G_SELECTED_ATTACKER, attacker_listbox, attacker_list, weapon_listbox, weapon_stats_listbox):
        if attacker_listbox.curselection() != ():
            G_SELECTED_ATTACKER.set(attacker_listbox.curselection()[0])

            box_index = 0
            weapon_listbox.delete(0, tk.END)
            for weapon in attacker_list[G_SELECTED_ATTACKER.get()].weapons:
                weapon_listbox.insert(box_index, weapon.name)
                box_index += 1

            weapon_stats_listbox.delete(0, tk.END)
    # End attacker_select()


    def weapon_select(self, event, G_SELECTED_ATTACKER, G_SELECTED_WEAPON, 
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


    def defender_select(self, event, G_SELECTED_DEFENDER, defender_listbox, defender_list, defender_stats_listbox):
        if defender_listbox.curselection() != ():
            G_SELECTED_DEFENDER.set(defender_listbox.curselection()[0])

            defender_stats_listbox.delete(0, tk.END)
            defender_stats_listbox.insert('0', f'Model Count: {defender_list[G_SELECTED_DEFENDER.get()].model_count}')
            defender_stats_listbox.insert('1', f'T{defender_list[G_SELECTED_DEFENDER.get()].toughness} {defender_list[G_SELECTED_DEFENDER.get()].wounds}W')
            defender_stats_listbox.insert('2', f'{defender_list[G_SELECTED_DEFENDER.get()].armor}+/{defender_list[G_SELECTED_DEFENDER.get()].invul}++')
            defender_stats_listbox.insert('3', f'Keywords:')
            sub_index = 4
            for keyword in defender_list[G_SELECTED_DEFENDER.get()].keywords:
                defender_stats_listbox.insert(f'{sub_index}', f'{keyword}')
                sub_index += 1
    # End defender_select()


    def populate_attacker_listbox(self, attacker_list, attacker_listbox):
        index = 0
        for attacker in attacker_list:
            attacker_listbox.insert(f'{index}', attacker.name)
            index += 1
    # End populate_attacker_listbox()


    def populate_defender_listbox(self, defender_list, defender_listbox):
        index = 0
        for defender in defender_list:
            defender_listbox.insert(f'{index}', defender.name)
            index += 1
    # End populate_attacker_listbox()


    def get_location_x(self):
        return self.winfo_rootx()
    

    def get_location_y(self):
        return self.winfo_rooty()


# End RootWindow
