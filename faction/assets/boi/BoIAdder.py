import faction.assets.boi.BoIUI as boiUI
import faction.Faction as Faction


class BoIAdder:
    def __init__(self, fedit_controller):
        self.controller = fedit_controller
        self.boi_ui = boiUI.BoIAdderUI(self, fedit_controller.get_asset_world_list())

    def acquire_boi(self, cost, location, ignore_cost=False):
        try:
            star, planet = location.split(' - ')
            base_asset = self.controller.asset_db.query(name="Base of Influence")[0]
            if not ignore_cost:
                if cost <= int(self.controller.cur_faction.fac_creds):
                        self.controller.cur_faction.add_asset(star, planet, cost, base_asset)
                        self.controller.cur_faction.fac_creds = int(self.controller.cur_faction.fac_creds) - cost
                else:
                    self.boi_ui.raise_error(boiUI.COST_ERROR)
            else:
                self.controller.cur_faction.add_asset(star, planet, cost, base_asset)
            self.controller.show_assets()
        except ValueError:
            self.boi_ui.raise_error(boiUI.PLANET_ERROR)
