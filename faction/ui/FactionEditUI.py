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

        tk.Button(main_frame, text='Buy Assets', command=self.open_asset_window).grid(column=6, row=1)

        tk.Label(main_frame, text='Assets:').grid(column=0, row=6)
        self.asset_table = ttk.Treeview(main_frame,
                                        columns=['Name', 'Class', 'hp', 'cost', 'tl', 'type', 'attack', 'counterattack',
                                                 'special', 'Location'])
        for id in ['Name', 'Class', 'hp', 'cost', 'tl', 'type', 'attack', 'counterattack', 'special', 'Location']:
            self.asset_table.column(id, width=75, anchor='center')
            self.asset_table.heading(id, text=id)
        self.asset_table['show'] = 'headings'
        self.asset_table.grid(column=0, row=3, columnspan=7, rowspan=5)
        self.asset_table.bind('<Double-1>', self.asset_clicked)

        table_scroll = tk.Scrollbar(self.asset_table)
        table_scroll.config(command=self.asset_table.yview)
        self.asset_table.config(yscrollcommand=table_scroll.set)

        # Buttons for accepting/cancelling edits and deleting faction
        tk.Button(main_frame, text="Save", command=self.save_faction).grid(column=0, row=8)
        tk.Button(main_frame, text="Cancel", command=self.close).grid(column=1, row=8)
        tk.Button(main_frame, text="Delete Faction", command=self.delete_faction).grid(column=2, row=8)

        # Frame for handling changing faction health, location
        self.asset_edit_frame = tk.LabelFrame(main_frame)
        self.asset_edit_frame.grid(column=7, row=1, columnspan=3, rowspan=4)

        tk.Label(self.asset_edit_frame, text="Location").grid(column=0, row=0)
        self.cur_asset_location = tk.StringVar()
        self.asset_location_option_menu = tk.OptionMenu(self.asset_edit_frame, self.cur_asset_location,
                                                        *self.controller.get_asset_world_list()).grid(row=0, column=1)
        tk.Label(self.asset_edit_frame, text="Current HP").grid(column=0, row=1)
        self.asset_hp_entry = tk.Entry(self.asset_edit_frame)
        self.asset_hp_entry.grid(column=1, row=1)

        # TODO: Implement changing asset to another of same type. Perhaps with simple tk.OptionMenu

        tk.Button(self.asset_edit_frame, text='Save Asset', command=self.asset_save).grid(column=0, row=2)

    def set_asset_info(self, name, location, hp):
        """Fills asset_edit_frame with information of chosen asset"""
        self.asset_edit_frame.config(text=name)
        self.cur_asset_location.set(location)
        self.asset_hp_entry.delete(0, tk.END)
        self.asset_hp_entry.insert(tk.END, hp)

    def set_fields(self, name='', hp='', fcreds='', force='', cunning='', wealth='', homeworld='\n'):
        """Sets values inserted in ui"""
        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(tk.END, name)
        self.hp_entry.delete(0, tk.END)
        self.hp_entry.insert(tk.END, hp)
        self.fcred_entry.delete(0, tk.END)
        self.fcred_entry.insert(tk.END, fcreds)
        self.force_entry.delete(0, tk.END)
        self.force_entry.insert(tk.END, force)
        self.cunning_entry.delete(0, tk.END)
        self.cunning_entry.insert(tk.END, cunning)
        self.wealth_entry.delete(0, tk.END)
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

    def show_asset(self, name, asset_class, hp, cost, tl, asset_type, attack, counterattack, special, location):
        self.asset_table.insert('', 'end',
                                values=[name, asset_class, hp, cost, tl, asset_type, attack, counterattack, special,
                                        location])

    def empty_table(self):
        self.asset_table.delete(*self.asset_table.get_children())

    def asset_clicked(self, event):
        """Passes index of currently chosen asset to FactionEditController with FactionEditController.asset_chosen(index)
         method"""
        assets = self.asset_table.get_children()
        self.controller.asset_chosen(assets.index(self.asset_table.focus()))

    def asset_save(self):
        self.controller.modify_asset(self.asset_hp_entry.get(), self.cur_asset_location.get())