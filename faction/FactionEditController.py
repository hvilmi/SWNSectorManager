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
        star, planet = location.split(' - ')
        base_asset = self.asset_db.query(name=asset_name)
        self.cur_faction.add_new_asset(star, planet, base_asset[0])
        if not ignore_cost:
            pass

    def get_asset_world_list(self):
        """Returns list of planets on sector where current faction can acquire assets followed by rest of the worlds"""
        planets = self.faction_controller.get_alphabetical_planet_list()
        occupied_planets = list(self.cur_faction.get_occupied_planets())
        planets = sorted(list(set(occupied_planets) ^ set(planets)))
        return occupied_planets + [SEPARATOR] + planets
