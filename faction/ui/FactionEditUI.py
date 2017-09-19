import tkinter as tk
import tkinter.ttk as ttk
import sectorUI.treeviewsort as tvsort
import faction.assets.ui.asset_edit


class FactionEditUI:
    def __init__(self, controller, name='', hp='', force='', cunning='', wealth='', fcreds='', xp='', homeworld='\n'):
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

        tk.Label(main_frame, text='XP:').grid(column=6, row=0)
        self.xp_entry = tk.Entry(main_frame)
        self.xp_entry.grid(column=7, row=0)

        tk.Label(main_frame, text='Homeworld:').grid(column=8, row=0)
        self.homeworld_selection = tk.StringVar('')
        tk.OptionMenu(main_frame, self.homeworld_selection,
                      *self.controller.faction_controller.get_alphabetical_planet_list()).grid(column=9, row=0)

        self.set_fields(name, hp, fcreds, force, cunning, wealth, xp, homeworld)

        tk.Button(main_frame, text='Buy Assets', command=self.open_asset_window).grid(column=6, row=1)

        asset_columns = ('Name', 'Class', 'hp', 'cost', 'tl', 'type', 'attack', 'counterattack', 'special', 'Location')
        tk.Label(main_frame, text='Assets:').grid(column=0, row=6)
        self.asset_table = ttk.Treeview(main_frame, columns=asset_columns)
        tvsort.make_treeview_sortable(self.asset_table, asset_columns)
        for id in asset_columns:
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

        # Frame for handling changing asset health, location
        self.asset_edit_frame = tk.LabelFrame(main_frame)
        self.asset_edit_frame.grid(column=7, row=1, columnspan=3, rowspan=4)

        self.asset_edit_ui = faction.assets.ui.asset_edit.AssetEditUI(self.asset_edit_frame, self.controller,
                                                                      self.controller.get_asset_world_list())

        # Frame for faction actions
        action_frame = tk.LabelFrame(main_frame, text='Actions')
        action_frame.grid(column=7, row=5)
        tk.Button(action_frame, text='Add Base of Influence', command=self.add_boi).grid(column=0, row=0)
        tk.Button(action_frame, text='Asset action', command=self.action_clicked).grid(column=0, row=1)

    def set_asset_info(self, name, location, hp, refit_options, relocation_options):
        """Fills asset_edit_frame with information of chosen asset."""
        self.asset_edit_ui.set_asset_info(name, location, hp, refit_options, relocation_options)

    def set_fields(self, name='', hp='', fcreds='', force='', cunning='', wealth='', xp='', homeworld='\n'):
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
        self.xp_entry.delete(0, tk.END)
        self.xp_entry.insert(tk.END, xp)
        for i, planet_name in enumerate(self.controller.faction_controller.get_alphabetical_planet_list()):
            if homeworld in planet_name:
                self.homeworld_selection.set(self.controller.faction_controller.get_alphabetical_planet_list()[i])

    def save_faction(self):
        # new_name, new_hp, new_force, new_cunning, new_wealth, new_facreds
        # TODO: Add sending new coordinates
        self.controller.save_faction(self.name_entry.get(), self.hp_entry.get(), self.force_entry.get(),
                                     self.cunning_entry.get(), self.wealth_entry.get(), self.fcred_entry.get(),
                                     self.xp_entry.get(), self.homeworld_selection.get())

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
        return self.asset_table.get_children()[-1]

    def empty_table(self):
        self.asset_table.delete(*self.asset_table.get_children())

    def asset_clicked(self, event):
        """Passes index of currently chosen asset to FactionEditController with FactionEditController.asset_chosen(index)
         method"""
        self.controller.asset_chosen(self.asset_table.focus())

    ##############
    def insert_asset_location_choices(self, location, relocation_options):

        pass

    #######################

    def add_boi(self):
        self.controller.create_boi_adder()

    def action_clicked(self):
        self.controller.create_action_controller()
