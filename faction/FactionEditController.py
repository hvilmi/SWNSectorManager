import tkinter as tk

from faction.assets import AssetDatabase
from faction.assets.ui import AssetBuyingUI
from faction.ui import FactionEditUI
from faction import Faction
import faction.assets.boi.BoIAdder as BoIAdder
import faction.action.controller

SEPARATOR = '-------'


class FactionEditController:
    def __init__(self, faction_controller, faction: Faction):
        self.asset_window = None
        self.cur_asset = None
        self.faction_controller = faction_controller
        self.cur_faction = faction
        self.asset_db = AssetDatabase.AssetDatabase()
        self.faction_ui = FactionEditUI.FactionEditUI(self, faction.name, faction.hp, faction.force, faction.cunning,
                                                      faction.wealth, faction.fac_creds, faction.xp, faction.homeworld)

        self.asset_treeview_index = {}
        self.show_assets()

        self.boi_adder = None
        self.action_controller = None

    def save_faction(self, new_name, new_hp, new_force, new_cunning, new_wealth, new_fcreds, xp, homeworld):
        self.cur_faction.name = new_name
        self.cur_faction.hp = new_hp
        self.cur_faction.cunning = new_cunning
        self.cur_faction.force = new_force
        self.cur_faction.wealth = new_wealth
        self.cur_faction.fac_creds = new_fcreds
        self.cur_faction.xp = xp
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
                self.asset_window.filter_change()
        else:
            self.asset_window = AssetBuyingUI.AssetBuyingUI(self)
            self.asset_window.filter_change()

    def update_faction_ui(self):
        self.faction_ui.set_fields(self.cur_faction.name, self.cur_faction.hp,
                                   self.cur_faction.fac_creds,
                                   self.cur_faction.force, self.cur_faction.cunning,
                                   self.cur_faction.wealth,
                                   self.cur_faction.xp,
                                   self.cur_faction.homeworld)

    def acquire_asset(self, asset_name, location, ignore_cost):
        try:
            star, planet = location.split(' - ')
            base_asset = self.asset_db.query(name=asset_name)[0]
            x_coord, y_coord = self.faction_controller.sector.get_star_by_name(star).get_coord()
            if not ignore_cost:
                if base_asset.cost <= int(self.cur_faction.fac_creds):
                    if self.faction_controller.sector.get_planet_by_name(planet).get_tl() >= base_asset.tl:
                        self.cur_faction.add_new_asset(star, planet, base_asset, x_coord, y_coord)
                        self.cur_faction.fac_creds = int(self.cur_faction.fac_creds) - base_asset.cost
                        self.update_faction_ui()
                    else:
                        self.asset_window.raise_error(AssetBuyingUI.TL_ERROR)
                else:
                    self.asset_window.raise_error(AssetBuyingUI.COST_ERROR)
            else:
                self.cur_faction.add_new_asset(star, planet, base_asset, x_coord, y_coord)
            self.show_assets()
        except ValueError:
            self.asset_window.raise_error(AssetBuyingUI.PLANET_ERROR)

    def get_asset_world_list(self):
        """Returns list of planets on sector where current faction can acquire assets followed by rest of the worlds.
        Current implementation lists worlds in which faction has any assets."""
        planets = self.faction_controller.get_alphabetical_planet_list()
        occupied_planets = list(self.cur_faction.get_occupied_planets())
        planets = sorted(list(set(occupied_planets) ^ set(planets)))
        return occupied_planets + [SEPARATOR] + planets

    def show_assets(self):
        self.faction_ui.empty_table()
        self.asset_treeview_index = {}
        print('Faction assets', self.cur_faction.assets)
        if len(self.cur_faction.assets) == 0:
            # No assets to show
            return

        for asset_instance in self.cur_faction.assets:
            base_asset = asset_instance.base_asset
            treeview_id = self.faction_ui.show_asset(base_asset.name, base_asset.asset_class,
                                                     asset_instance.cur_hp,
                                                     base_asset.cost, base_asset.tl, base_asset.type,
                                                     base_asset.attack,
                                                     base_asset.counterattack, base_asset.special,
                                                     asset_instance.get_location())
            self.asset_treeview_index[treeview_id] = asset_instance.index
        self.asset_chosen(list(self.asset_treeview_index.keys())[0])

    def asset_chosen(self, index):
        if index not in self.asset_treeview_index.keys():
            print('No asset in list')
            return
        chosen_asset = self.cur_faction.get_asset_by_id(self.asset_treeview_index[index])
        refit_names = [asset.get_name() for asset in self.asset_db.query(type=chosen_asset.base_asset.get_type())]
        self.faction_ui.set_asset_info(chosen_asset.get_name(), chosen_asset.get_location(), chosen_asset.cur_hp,
                                       refit_names, chosen_asset.get_relocation_choices())
        self.cur_asset = chosen_asset

    def modify_asset(self, hp, location, refit_asset, refit_cost):

        if self.cur_asset is None:
            return

        self.cur_asset.cur_hp = hp
        print(location[0])
        self.cur_asset.set_location(location)
        self.show_assets()
        if self.asset_db.query(name=refit_asset)[0] != self.cur_asset.base_asset:
            # Refit is done
            if refit_cost <= self.cur_faction.fac_creds:
                self.cur_faction.fac_creds = int(self.cur_faction.fac_creds) - int(refit_cost)
                self.cur_asset.base_asset = self.asset_db.query(name=refit_asset)[0]
        self.update_faction_ui()
        self.show_assets()

    def refit_choice_changed(self, name, ui):
        if self.cur_asset is None:
            pass
        elif self.cur_asset.base_asset.cost == '*':
            ui.show_refit_cost('*')
        else:
            refit_asset = self.asset_db.query(name=name)[0]
            refit_cost = int(refit_asset.cost) - int(self.cur_asset.base_asset.cost)
            if refit_cost > 0:
                ui.show_refit_cost(refit_cost)
            else:
                ui.show_refit_cost(0)

    def delete_cur_asset(self):
        self.cur_faction.assets.remove(self.cur_asset)
        self.show_assets()

    def reload_assets(self, filter_bool: bool, world_name: str):
        if filter_bool:
            if world_name == SEPARATOR:
                self.asset_window.raise_error(AssetBuyingUI.PLANET_ERROR)
                return
            else:
                world_name = world_name.split(' - ')
                planet = self.faction_controller.sector.get_planet_by_name(world_name[1])

            self.asset_window.insert_to_table('force', self.asset_db.query(type='F', max_level=self.cur_faction.force,
                                                                           tl=planet.get_tl(),
                                                                           max_cost=int(self.cur_faction.fac_creds)))
            self.asset_window.insert_to_table('cunning', self.asset_db.query(type='C',
                                                                             max_level=self.cur_faction.cunning,
                                                                             tl=planet.get_tl(),
                                                                             max_cost=int(self.cur_faction.fac_creds)))
            self.asset_window.insert_to_table('wealth', self.asset_db.query(type='W',
                                                                            max_level=self.cur_faction.wealth,
                                                                            tl=planet.get_tl(),
                                                                            max_cost=int(self.cur_faction.fac_creds)))
        else:
            print('Query without filter')
            self.asset_window.insert_to_table('force', self.asset_db.query(type='F'))
            self.asset_window.insert_to_table('cunning', self.asset_db.query(type='C'))
            self.asset_window.insert_to_table('wealth', self.asset_db.query(type='W'))

    def change_asset_location_choices(self, filter):
        if not self.cur_asset:
            return

        if filter:
            relocation_choices = self.cur_asset.get_relocation_choices()
        else:
            star_list = self.faction_controller.sector.stars
            relocation_choices = []
            for star in star_list:
                for planet in star.planets:
                    relocation_choices.append(star.name + ' - ' + planet.name)

        self.faction_ui.insert_asset_location_choices(self.cur_asset.get_location(), relocation_choices)

    def create_boi_adder(self):
        self.boi_adder = BoIAdder.BoIAdder(self)

    def create_action_controller(self):
        self.action_controller = faction.action.controller.ActionController(self.cur_faction)
