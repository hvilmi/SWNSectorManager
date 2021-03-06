import tkinter as tk
import tkinter.ttk as ttk
import sectorUI.treeviewsort as tvsort

NO_ERROR = "Asset Acquired."
COST_ERROR = "Not enough facCreds."
TL_ERROR = "Planet is not advanced enough."
PLANET_ERROR = "No planet chosen."
PERMISSION_ERROR = "No permission from planetary authority."  # Not currently used.


class AssetBuyingUI:
    def __init__(self, parent):
        self.parent = parent

        self.top_level = tk.Toplevel(parent.faction_ui.main_window)

        main_frame = tk.Frame(self.top_level)
        main_frame.pack()

        self.asset_nb = ttk.Notebook(main_frame)
        self.asset_nb.grid(column=0, row=0, columnspan=5, rowspan=10)

        self.cunning_assets_table = self.create_asset_table(self.asset_nb, "Cunning")
        self.force_assets_table = self.create_asset_table(self.asset_nb, "Force")
        self.wealth_assets_table = self.create_asset_table(self.asset_nb, "Wealth")

        self.filter_bool = tk.BooleanVar()
        ttk.Checkbutton(main_frame, text="Filter Assets", var=self.filter_bool).grid(row=10, column=0)
        self.filter_bool.set(True)
        self.filter_bool.trace('w', self.filter_change)

        self.cost_bool = tk.BooleanVar()
        ttk.Checkbutton(main_frame, text="Ignore Cost", var=self.cost_bool).grid(row=11, column=0)
        self.cost_bool.set(False)

        tk.Button(main_frame, text='Acquire Asset', command=self.acquire_button_pressed).grid(row=12, column=0)

        self.world_selection = tk.StringVar()
        tk.OptionMenu(main_frame, self.world_selection, *self.parent.get_asset_world_list()).grid(row=10, column=1)
        self.world_selection.set(self.parent.get_asset_world_list()[0])
        self.world_selection.trace('w', self.filter_change)

        self.error_text = tk.StringVar()
        tk.Label(main_frame, textvariable=self.error_text).grid(row=12, column=1, columnspan=2)

    @staticmethod
    def create_asset_table(parent_nb, asset_type):

        new_frame = tk.Frame(parent_nb)
        parent_nb.add(new_frame, text=asset_type)

        asset_columns = ['Name', 'Level', 'hp', 'cost', 'tl', 'type', 'attack', 'counterattack', 'special']
        asset_table = ttk.Treeview(new_frame, columns=asset_columns)
        tvsort.make_treeview_sortable(asset_table, asset_columns)

        column_widths = [125, 50, 30, 30, 30, 50, 75, 75, 75]
        for id, col_width in zip(asset_columns, column_widths):
            asset_table.column(id, width=col_width, anchor='center')
            asset_table.heading(id, text=id)
        asset_table['show'] = 'headings'
        asset_table.grid(column=0, row=0)

        return asset_table

    def insert_to_table(self, table_id, assets):
        self.clear_error()
        """table id = 'cunning', 'force' or 'wealth' """
        table_dict = {'cunning': self.cunning_assets_table, 'force': self.force_assets_table,
                      'wealth': self.wealth_assets_table}
        cur_table = table_dict[table_id]
        cur_table.delete(*cur_table.get_children())

        for asset in assets:
            # Asset has special cost, hp or tech level
            cur_table.insert('', 'end', values=[asset.name, asset.type[1], asset.max_hp, asset.cost,
                                                asset.tl, asset.type[0], asset.attack, asset.counterattack,
                                                asset.special])

    def bring_to_front(self):
        self.top_level.lift()

    def acquire_button_pressed(self):
        tmp_list = self.asset_nb.tabs()
        table_list = [self.cunning_assets_table, self.force_assets_table, self.wealth_assets_table]
        active_table = table_list[tmp_list.index(self.asset_nb.select())]
        chosen_asset_name = active_table.item(active_table.focus())['values'][0]
        self.parent.acquire_asset(chosen_asset_name, self.world_selection.get(), self.cost_bool.get())

    def raise_error(self, error):
        self.error_text.set(error)

    def clear_error(self):
        self.error_text.set('')

    def filter_change(self, *args):
        self.parent.reload_assets(self.filter_bool.get(), self.world_selection.get())
