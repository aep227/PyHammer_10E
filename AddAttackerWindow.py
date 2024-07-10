import tkinter as tk
import tkinter.ttk as ttk
import data_manage as data_man

class AddAttackerWindow(tk.Toplevel):

    def __init__(self, attacker_list, attacker_listbox, root_x, root_y):
        tk.Toplevel.__init__(self)
        self.title('Add Attacker')
        self.default_pad = 20
        self.default_font = ('Cascadia Code', '14')

        win_x = root_x + 300
        win_y = root_y + 50
        self.geometry(f'+{win_x}+{win_y}')

        self.name_label = ttk.Label(        self, text = 'Attacker Name', style = 'default.TLabel')
        self.name_entry = ttk.Entry(        self, width = 10, font = self.default_font, justify = 'center')
        self.model_count_label = ttk.Label( self, text = 'Model Count', style = 'default.TLabel')
        self.model_count_entry = ttk.Entry( self, width = 10, font = self.default_font, justify = 'center')
        self.toughness_label = ttk.Label(   self, text = 'Toughness', style = 'default.TLabel')
        self.toughness_entry = ttk.Entry(   self, width = 10, font = self.default_font, justify = 'center')
        self.wounds_label = ttk.Label(      self, text = 'Wounds per Model', style = 'default.TLabel')
        self.wounds_entry = ttk.Entry(      self, width = 10, font = self.default_font, justify = 'center')
        self.armor_label = ttk.Label(       self, text = 'Armor Save', style = 'default.TLabel')
        self.armor_entry = ttk.Entry(       self, width = 10, font = self.default_font, justify = 'center')
        self.invul_label = ttk.Label(       self, text = 'Invulnerable Save', style = 'default.TLabel')
        self.invul_entry = ttk.Entry(       self, width = 10, font = self.default_font, justify = 'center')
        self.abilities_label = ttk.Label(   self, text = 'Abilities', style = 'default.TLabel')
        self.abilities_entry = ttk.Entry(   self, width = 10, font = self.default_font, justify = 'center')
        self.keywords_label = ttk.Label(    self, text = 'Keywords', style = 'default.TLabel')
        self.keywords_entry = ttk.Entry(    self, width = 10, font = self.default_font, justify = 'center')
        self.add_button = ttk.Button(       self, text = 'Add Attacker', style = 'default.TButton',
                                     command = lambda: data_man.add_attacker_to_list(attacker_list, attacker_listbox,
                                                                                    self.name_entry.get(),
                                                                                    self.model_count_entry.get(),
                                                                                    self.toughness_entry.get(),
                                                                                    self.wounds_entry.get(),
                                                                                    self.armor_entry.get(),
                                                                                    self.invul_entry.get(),
                                                                                    self.abilities_entry.get(),
                                                                                    self.keywords_entry.get()))
        self.exit_button = ttk.Button(    self, text = 'Exit', style = 'default.TButton', command = self.destroy)

        # Layout Window
        self.name_label.grid(        row = 0, column = 0, padx = self.default_pad, sticky = 'w')
        self.name_entry.grid(        row = 0, column = 1, padx = self.default_pad, pady = self.default_pad)
        self.model_count_label.grid( row = 1, column = 0, padx = self.default_pad, sticky = 'w')
        self.model_count_entry.grid( row = 1, column = 1, padx = self.default_pad, pady = self.default_pad)
        self.toughness_label.grid(   row = 2, column = 0, padx = self.default_pad, sticky = 'w')
        self.toughness_entry.grid(   row = 2, column = 1, padx = self.default_pad, pady = self.default_pad)
        self.wounds_label.grid(      row = 3, column = 0, padx = self.default_pad, sticky = 'w')
        self.wounds_entry.grid(      row = 3, column = 1, padx = self.default_pad, pady = self.default_pad)
        self.armor_label.grid(       row = 4, column = 0, padx = self.default_pad, sticky = 'w')
        self.armor_entry.grid(       row = 4, column = 1, padx = self.default_pad, pady = self.default_pad)
        self.invul_label.grid(       row = 5, column = 0, padx = self.default_pad, sticky = 'w')
        self.invul_entry.grid(       row = 5, column = 1, padx = self.default_pad, pady = self.default_pad)
        self.abilities_label.grid(   row = 6, column = 0, padx = self.default_pad, sticky = 'w')
        self.abilities_entry.grid(   row = 6, column = 1, padx = self.default_pad, pady = self.default_pad)
        self.keywords_label.grid(    row = 7, column = 0, padx = self.default_pad, sticky = 'w')
        self.keywords_entry.grid(    row = 7, column = 1, padx = self.default_pad, pady = self.default_pad)
        self.add_button.grid(        row = 9, column = 0, padx = self.default_pad, sticky = 'w')
        self.exit_button.grid(     row = 9, column = 1, padx = self.default_pad, pady = self.default_pad)

        self.focus()
        self.grab_set()
    # End init()

# End AddAttackerWindow