import tkinter as tk
import tkinter.ttk as ttk


class FactionTreeViewUI:
    def __init__(self, faction_controller, parent, x_coord, y_coord):
        self.parent = parent
        self.controller = faction_controller

        self.faction_frame = tk.Frame(self.parent)
        self.faction_frame.grid(column=x_coord, row=y_coord)
        self.faction_treeview = ttk.Treeview(self.faction_frame,
                                             columns=['Name', 'HP', 'Force', 'Cunning', 'Wealth', 'FacCreds',
                                                      'Homeworld', 'XP'])

        for id in ['Name', 'HP', 'Force', 'Cunning', 'Wealth', 'FacCreds', 'Homeworld', 'XP']:
            self.faction_treeview.column(id, width=75, anchor='center')
            self.faction_treeview.heading(id, text=id)
        self.faction_treeview.grid(row=0, column=0)

        self.faction_treeview['show'] = 'headings'
        self.faction_treeview.bind('<Double-1>', self.on_double_click)

        self.add_faction_button = tk.Button(self.faction_frame, text='Add Faction',
                                            command=self.open_new_faction_window)
        self.add_faction_button.grid(column=0, row=1)

        self.controller.register_faction_table(self)

    def show_faction(self, name='', hp='', force='', cunning='', wealth='', creds='', homeworld='', xp=''):
        self.faction_treeview.insert('', 'end', values=[name, hp, force, cunning, wealth, creds, homeworld, xp])

    def clear_factions(self):
        self.faction_treeview.delete(*self.faction_treeview.get_children())

    def open_new_faction_window(self):
        self.controller.add_new_faction()

    def on_double_click(self, event):
        cur_faction = self.faction_treeview.item(self.faction_treeview.focus())['values']
        print(cur_faction)
        try:
            self.controller.faction_chosen(cur_faction[0])
        except IndexError:
            # No factions exist yet, consider creating new one.
            pass
