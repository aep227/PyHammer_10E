import tkinter as tk
import tkinter.ttk as ttk
import data_manage as data_man

class AddWeaponWindow(tk.Toplevel):

    def __init__(self, attacker_list, weapon_listbox, root_x, root_y, selected_attacker):
        tk.Toplevel.__init__(self)
        self.title('Add Weapon')
        self.default_pad = 20
        self.default_font = ('Cascadia Code', '14')

        win_x = root_x + 542
        win_y = root_y + 50
        self.geometry(f'+{win_x}+{win_y}')

        self.name_label = ttk.Label(      self, text = 'Weapon Name', style = 'default.TLabel')
        self.name_entry = ttk.Entry(      self, width = 10, font = self.default_font, justify = 'center')
        self.count_label = ttk.Label(     self, text = 'Count', style = 'default.TLabel')
        self.count_entry = ttk.Entry(     self, width = 10, font = self.default_font, justify = 'center')
        self.attacks_label = ttk.Label(   self, text = 'Attacks', style = 'default.TLabel')
        self.attacks_entry = ttk.Entry(   self, width = 10, font = self.default_font, justify = 'center')
        self.skill_label = ttk.Label(     self, text = 'Skill', style = 'default.TLabel')
        self.skill_entry = ttk.Entry(     self, width = 10, font = self.default_font, justify = 'center')
        self.strength_label = ttk.Label(  self, text = 'Strength', style = 'default.TLabel')
        self.strength_entry = ttk.Entry(  self, width = 10, font = self.default_font, justify = 'center')
        self.AP_label = ttk.Label(        self, text = 'AP', style = 'default.TLabel')
        self.AP_entry = ttk.Entry(        self, width = 10, font = self.default_font, justify = 'center')
        self.damage_label = ttk.Label(    self, text = 'Damage', style = 'default.TLabel')
        self.damage_entry = ttk.Entry(    self, width = 10, font = self.default_font, justify = 'center')
        self.abilities_label = ttk.Label( self, text = 'Abilities', style = 'default.TLabel')
        self.abilities_entry = ttk.Entry( self, width = 10, font = self.default_font, justify = 'center')
        self.add_button = ttk.Button(     self, text = 'Add Weapon', style = 'default.TButton',
                                     command = lambda: data_man.add_weapon_to_attacker(attacker_list, weapon_listbox,
                                                                                       selected_attacker,
                                                                                       self.name_entry.get(),
                                                                                       self.count_entry.get(),
                                                                                       self.attacks_entry.get(),
                                                                                       self.skill_entry.get(),
                                                                                       self.strength_entry.get(),
                                                                                       self.AP_entry.get(),
                                                                                       self.damage_entry.get(),
                                                                                       self.abilities_entry.get()))
        self.exit_button = ttk.Button(    self, text = 'Exit', style = 'default.TButton', command = self.destroy)

        # Layout Window
        self.name_label.grid(       row = 0, column = 0, padx = self.default_pad, sticky = 'w')
        self.name_entry.grid(       row = 0, column = 1, padx = self.default_pad, pady = self.default_pad)
        self.count_label.grid(      row = 1, column = 0, padx = self.default_pad, sticky = 'w')
        self.count_entry.grid(      row = 1, column = 1, padx = self.default_pad, pady = self.default_pad)
        self.attacks_label.grid(    row = 2, column = 0, padx = self.default_pad, sticky = 'w')
        self.attacks_entry.grid(    row = 2, column = 1, padx = self.default_pad, pady = self.default_pad)
        self.skill_label.grid(      row = 3, column = 0, padx = self.default_pad, sticky = 'w')
        self.skill_entry.grid(      row = 3, column = 1, padx = self.default_pad, pady = self.default_pad)
        self.strength_label.grid(   row = 4, column = 0, padx = self.default_pad, sticky = 'w')
        self.strength_entry.grid(   row = 4, column = 1, padx = self.default_pad, pady = self.default_pad)
        self.AP_label.grid(         row = 5, column = 0, padx = self.default_pad, sticky = 'w')
        self.AP_entry.grid(         row = 5, column = 1, padx = self.default_pad, pady = self.default_pad)
        self.damage_label.grid(     row = 6, column = 0, padx = self.default_pad, sticky = 'w')
        self.damage_entry.grid(     row = 6, column = 1, padx = self.default_pad, pady = self.default_pad)
        self.abilities_label.grid(  row = 7, column = 0, padx = self.default_pad, sticky = 'w')
        self.abilities_entry.grid(  row = 7, column = 1, padx = self.default_pad, pady = self.default_pad)
        self.add_button.grid(       row = 8, column = 0, padx = self.default_pad, sticky = 'w')
        self.exit_button.grid(      row = 8, column = 1, padx = self.default_pad, pady = self.default_pad)

        self.focus()
        self.grab_set()
    # End init()

# End AddAttackerWindow