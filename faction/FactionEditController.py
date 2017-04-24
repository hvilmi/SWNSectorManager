import tkinter as tk

from faction.assets import AssetDatabase
from faction.assets.ui import AssetBuyingUI
from faction.ui import FactionEditUI
from faction import Faction

SEPARATOR = '-------'


class FactionEditController:
    def __init__(self, faction_controller, faction: Faction):
        self.faction_controller = faction_controller
        self.cur_faction = faction
        self.asset_db = AssetDatabase.AssetDatabase()
        self.faction_ui = FactionEditUI.FactionEditUI(self, faction.name, faction.hp, faction.force, faction.cunning,
                                                      faction.wealth, faction.fac_creds, faction.homeworld)
        self.asset_window = None


        self.cur_asset = None
        self.asset_treeview_index = {}
        self.show_assets()

    def save_faction(self, new_name, new_hp, new_force, new_cunning, new_wealth, new_fcreds, homeworld):
        self.cur_faction.name = new_name
        self.cur_faction.hp = new_hp
        self.cur_faction.cunning = new_cunning
        self.cur_faction.force = new_force
        self.cur_faction.wealth = new_wealth
        self.cur_faction.fac_creds = new_fcreds
        if homeworld:
            self.cur_faction.homeworld = homeworld
        self.faction_controller.display_factions()

    def delete_current_faction(self):
        self.faction_controller.delete_faction(self.cur_faction)

    def create_asset_window(self):
        if self.asset_window:
            try:
                self.asset_window.bring_to_front()
            except tk.TclError:
                # Asset Window was closed
                self.asset_window = AssetBuyingUI.AssetBuyingUI(self)
                self.asset_window.insert_to_table('force',
                                                  self.asset_db.query(type='F', max_level=self.cur_faction.force))
        else:
            self.asset_window = AssetBuyingUI.AssetBuyingUI(self)
            self.asset_window.insert_to_table('force', self.asset_db.query(type='F', max_level=self.cur_faction.force))

    def acquire_asset(self, asset_name, location, ignore_cost):
        try:
            star, planet = location.split(' - ')
            base_asset = self.asset_db.query(name=asset_name)[0]
            if not ignore_cost:
                if base_asset.cost <= int(self.cur_faction.fac_creds):
                    if self.faction_controller.sector.get_planet_by_name(planet).get_tl() >= base_asset.tl:
                        self.cur_faction.add_new_asset(star, planet, base_asset)
                        self.cur_faction.fac_creds = int(self.cur_faction.fac_creds) - base_asset.cost
                        self.faction_ui.set_fields(self.cur_faction.name, self.cur_faction.hp, self.cur_faction.fac_creds,
                                                   self.cur_faction.force, self.cur_faction.cunning, self.cur_faction.wealth,
                                                   self.cur_faction.homeworld)
                    else:
                        self.asset_window.raise_error(AssetBuyingUI.TL_ERROR)
                else:
                    self.asset_window.raise_error(AssetBuyingUI.COST_ERROR)
            else:
                self.cur_faction.add_new_asset(star, planet, base_asset)
            self.show_assets()
        except ValueError:
            self.asset_window.raise_error(AssetBuyingUI.PLANET_ERROR)

    def get_asset_world_list(self):
        """Returns list of planets on sector where current faction can acquire assets followed by rest of the worlds"""
        planets = self.faction_controller.get_alphabetical_planet_list()
        occupied_planets = list(self.cur_faction.get_occupied_planets())
        planets = sorted(list(set(occupied_planets) ^ set(planets)))
        return occupied_planets + [SEPARATOR] + planets

    def show_assets(self):
        self.faction_ui.empty_table()
        for asset_instance in self.cur_faction.assets:
            base_asset = asset_instance.base_asset
            treeview_id = self.faction_ui.show_asset(base_asset.name, base_asset.asset_class,
                                                     asset_instance.cur_hp,
                                                     base_asset.cost, base_asset.tl, base_asset.type,
                                                     base_asset.attack,
                                                     base_asset.counterattack, base_asset.special,
                                                     asset_instance.get_location())
            self.asset_treeview_index[treeview_id] = asset_instance.index

    def asset_chosen(self, index):
        print(self.cur_faction.assets)
        chosen_asset = self.cur_faction.get_asset_by_id(self.asset_treeview_index[index])
        self.faction_ui.set_asset_info(chosen_asset.get_name(), chosen_asset.get_location(), chosen_asset.cur_hp)
        self.cur_asset = chosen_asset

    def modify_asset(self, hp, location):
        self.cur_asset.cur_hp = hp
        self.cur_asset.set_location(location)
        self.show_assets()
