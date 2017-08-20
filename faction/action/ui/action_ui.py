import tkinter as tk
import tkinter.ttk as ttk


class ActionUI(tk.Toplevel):
    def __init__(self, parent, actor_assets):
        tk.Toplevel.__init__(self)
        self.parent = parent
        main_frame = tk.Frame(self)
        main_frame.grid(column=0, row=0)

        self.actor_assets = actor_assets
        aasset_names = [asset.base_asset.get_name() + " at " + asset.get_location() for asset in actor_assets]
        actor_choice = tk.StringVar()
        self.actor_combobox = ttk.Combobox(main_frame, textvariable=actor_choice, values=aasset_names)
        self.actor_combobox.bind('<<ComboboxSelected>>', self.actor_selected)
        self.actor_combobox.grid(column=0, row=0)

        self.targets_table = ttk.Treeview(main_frame, columns=['hp'])
        self.targets_table.grid(column=0, row=1, columnspan=3)
        self.target_list = []

    def actor_selected(self, *args):
        self.parent.set_chosen_actor_asset(self.actor_combobox.current())

    def target_selected(self):
        print(self.targets_table.focus())

    def populate_target_table(self, assets):
        self.target_list = assets

        for asset in self.target_list:
            asset_iid = asset.parent.name + ' ' + asset.id
            self.targets_table.insert(asset.parent.name, tk.END, iid=asset_iid, values=[asset.cur_hp])
