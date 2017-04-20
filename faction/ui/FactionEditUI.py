import tkinter as tk
import tkinter.ttk as ttk


class FactionEditUI:
    def __init__(self, controller, name='', hp='', force='', cunning='', wealth='', fcreds='', homeworld='\n'):
        self.controller = controller

        self.main_window = tk.Toplevel()

        main_frame = tk.Frame(self.main_window)
        main_frame.grid(row=0, column=0)

        tk.Label(main_frame, text='Name:').grid(column=0, row=0)
        self.name_entry = tk.Entry(main_frame)
        self.name_entry.grid(column=1, row=0)

        tk.Label(main_frame, text='HP:').grid(column=2, row=0)
        self.hp_entry = tk.Entry(main_frame)
        self.hp_entry.grid(column=3, row=0)

        tk.Label(main_frame, text='FacCreds:').grid(column=4, row=0)
        self.fcred_entry = tk.Entry(main_frame)
        self.fcred_entry.grid(column=5, row=0)

        tk.Label(main_frame, text='Force:').grid(column=0, row=1)
        self.force_entry = tk.Entry(main_frame)
        self.force_entry.grid(column=1, row=1)

        tk.Label(main_frame, text='Cunning:').grid(column=2, row=1)
        self.cunning_entry = tk.Entry(main_frame)
        self.cunning_entry.grid(column=3, row=1)

        tk.Label(main_frame, text='Wealth:').grid(column=4, row=1)
        self.wealth_entry = tk.Entry(main_frame)
        self.wealth_entry.grid(column=5, row=1)

        tk.Label(main_frame, text='Homeworld:').grid(column=6, row=0)
        self.homeworld_selection = tk.StringVar('')
        tk.OptionMenu(main_frame, self.homeworld_selection,
                      *self.controller.faction_controller.get_alphabetical_planet_list()).grid(column=7, row=0)

        self.set_fields(name, hp, fcreds, force, cunning, wealth, homeworld)

        # TODO: Implement faction assets
        tk.Button(main_frame, text='Buy Assets', command=self.open_asset_window).grid(column=6, row=1)

        tk.Label(main_frame, text='Assets:').grid(column=0, row=6)
        self.asset_table = ttk.Treeview(main_frame,
                                        columns=['Name', 'Class', 'hp', 'cost', 'tl', 'type', 'attack', 'counterattack',
                                                 'special'])
        for id in ['Name', 'Class', 'hp', 'cost', 'tl', 'type', 'attack', 'counterattack', 'special']:
            self.asset_table.column(id, width=75, anchor='center')
            self.asset_table.heading(id, text=id)
        self.asset_table['show'] = 'headings'
        self.asset_table.grid(column=0, row=7, columnspan=7)

        table_scroll = tk.Scrollbar(self.asset_table)
        table_scroll.config(command=self.asset_table.yview)
        self.asset_table.config(yscrollcommand=table_scroll.set)

        # GUI for buying assets


        # Buttons for accepting/cancelling edits and deleting faction
        tk.Button(main_frame, text="Save", command=self.save_faction).grid(column=0, row=8)
        tk.Button(main_frame, text="Cancel", command=self.close).grid(column=1, row=8)
        tk.Button(main_frame, text="Delete Faction", command=self.delete_faction).grid(column=2, row=8)

    def set_fields(self, name='', hp='', fcreds='', force='', cunning='', wealth='', homeworld='\n'):
        '''Sets values inserted in ui'''
        self.name_entry.insert(tk.END, name)
        self.hp_entry.insert(tk.END, hp)
        self.fcred_entry.insert(tk.END, fcreds)
        self.force_entry.insert(tk.END, force)
        self.cunning_entry.insert(tk.END, cunning)
        self.wealth_entry.insert(tk.END, wealth)
        print(homeworld)
        for i, planet_name in enumerate(self.controller.faction_controller.get_alphabetical_planet_list()):
            print(planet_name)
            if homeworld in planet_name:
                self.homeworld_selection.set(self.controller.faction_controller.get_alphabetical_planet_list()[i])

    def save_faction(self):
        # new_name, new_hp, new_force, new_cunning, new_wealth, new_facreds
        self.controller.save_faction(self.name_entry.get(), self.hp_entry.get(), self.force_entry.get(),
                                     self.cunning_entry.get(), self.wealth_entry.get(), self.fcred_entry.get(),
                                     self.homeworld_selection.get())

    def close(self):
        self.main_window.destroy()

    def delete_faction(self):
        self.controller.delete_current_faction()
        self.close()

    def open_asset_window(self):
        self.controller.create_asset_window()
