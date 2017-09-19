import tkinter as tk
import tkinter.ttk as ttk
import faction.FactionEditController


class AssetEditUI:
    def __init__(self, asset_frame: tk.Frame or tk.LabelFrame,
                 controller, asset_world_list: [str]):
        self.asset_edit_frame = asset_frame
        self.controller = controller

        tk.Label(self.asset_edit_frame, text="Location").grid(column=0, row=0)
        self.cur_asset_location = tk.StringVar()
        self.asset_location_option_menu = tk.OptionMenu(self.asset_edit_frame, self.cur_asset_location,
                                                        *asset_world_list)
        self.asset_location_option_menu.grid(row=0, column=1)
        tk.Label(self.asset_edit_frame, text="Current HP").grid(column=0, row=1)

        self.asset_location_filter_var = tk.BooleanVar()
        self.asset_location_filter_var.set(True)
        self.asset_location_filter_var.trace('w', self.location_filter_changed)
        tk.Checkbutton(self.asset_edit_frame, text="Normal movement",
                       var=self.asset_location_filter_var).grid(row=0, column=2)

        self.asset_hp_entry = tk.Entry(self.asset_edit_frame)
        self.asset_hp_entry.grid(column=1, row=1)

        self.asset_refit_var = tk.StringVar()
        self.asset_refit_var.trace("w", self.refit_change)
        self.asset_refit_menu = ttk.OptionMenu(self.asset_edit_frame, self.asset_refit_var)
        self.asset_refit_menu.grid(column=0, row=2)

        self.refit_price = tk.StringVar()
        self.refit_price.set('0')
        tk.Label(self.asset_edit_frame, textvariable=self.refit_price).grid(column=1, row=2)

        tk.Button(self.asset_edit_frame, text='Save Asset', command=self.asset_save).grid(column=0, row=3)
        tk.Button(self.asset_edit_frame, text='Delete Asset', command=self.asset_delete).grid(column=1, row=3)

    def get_asset(self):
        return [self.asset_hp_entry.get(), self.cur_asset_location.get(),
                self.asset_refit_var.get(), self.refit_price.get()]

    def refit_change(self, *args):
        print("Refit debug", self.asset_refit_var.get())
        self.controller.refit_choice_changed(self.asset_refit_var.get(), self)

    def show_refit_cost(self, cost):
        self.refit_price.set(cost)

    def location_filter_changed(self, *args):
        self.controller.change_asset_location_choices(self.asset_location_filter_var.get(), self)

    def insert_asset_location_choices(self, location, relocation_options):
        self.asset_location_option_menu['menu'].delete(0, tk.END)
        for loc in relocation_options:
            self.asset_location_option_menu['menu'].add_command(label=loc, command=lambda _location=loc:
            self.asset_location_option_menu.setvar(
                self.asset_location_option_menu.cget("textvariable")
                , value=_location))
        self.cur_asset_location.set(location)

    def set_asset_info(self, name, location, hp, refit_options, relocation_options):
        """Fills asset_edit_frame with information of chosen asset."""
        self.asset_edit_frame.config(text=name)
        self.cur_asset_location.set(location)
        self.asset_hp_entry.delete(0, tk.END)
        self.asset_hp_entry.insert(tk.END, hp)

        self.asset_refit_menu['menu'].delete(0, tk.END)
        for asset in refit_options:
            self.asset_refit_menu['menu'].add_command(label=asset,
                                                      command=lambda _asset=asset:
                                                      self.asset_refit_menu.setvar(
                                                          self.asset_refit_menu.cget("textvariable"),
                                                          value=_asset))
        self.asset_refit_var.set(name)

        print(self.asset_location_option_menu)
        self.insert_asset_location_choices(location, relocation_options)

    def get_current_values(self):
        return [self.asset_hp_entry.get(), self.cur_asset_location.get(), self.asset_refit_var.get(),
                self.refit_price.get()]

    def asset_save(self):
        self.controller.modify_asset(self.asset_hp_entry.get(), self.cur_asset_location.get(),
                                     self.asset_refit_var.get(), self.refit_price.get())

    # def show_refit_cost(self, cost):
    #    self.refit_price.set(cost)

    def asset_delete(self):
        self.controller.delete_cur_asset()

    # def location_filter_changed(self, *args):
    #    self.controller.change_asset_location_choices(self.asset_location_filter_var.get())
