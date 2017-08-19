import faction.FactionEditController as FactionEditController
import faction.Faction as Faction
import faction.assets.AssetInstance


# name, hp, force, cunning, wealth, fac_creds, xp, homeworld

class FactionController:
    def __init__(self, factions, sector):
        self.factions = factions
        for faction in self.factions:
            faction.controller = self
        self.sector = sector
        self.faction_treeview = None

    def faction_chosen(self, faction_name):
        chosen_faction = self.get_faction_by_name(faction_name)
        faction_edit_ui = FactionEditController.FactionEditController(self, chosen_faction)

    def get_faction_by_name(self, name):
        for faction in self.factions:
            if faction.name == name:
                return faction
        print("No faction found")

    def add_new_faction(self):
        Faction.Faction('', 0, 0, 0, 0, 0, 0, "", self)
        faction_edit_ui = FactionEditController.FactionEditController(self, self.factions[-1])

    def register_faction_table(self, faction_treeview):
        self.faction_treeview = faction_treeview
        print(self.factions)
        self.display_factions()

    def display_factions(self):
        self.faction_treeview.clear_factions()
        print(self.factions)
        for faction in self.factions:
            self.faction_treeview.show_faction(name=faction.name, hp=faction.hp, force=faction.force,
                                               cunning=faction.cunning, wealth=faction.wealth, creds=faction.fac_creds,
                                               homeworld=faction.homeworld, xp=faction.xp)

    def get_alphabetical_planet_list(self):
        return self.sector.get_alphabetical_planet_list()

    def delete_faction(self, faction):
        """Takes Faction object or faction name as input and removes that faction."""
        if isinstance(faction, Faction.Faction):
            self.factions.remove(faction)
        elif isinstance(faction, str):
            self.factions.remove(self.get_faction_by_name(faction))
        self.display_factions()

    def clear(self):
        self.factions = []
        self.faction_treeview.clear_factions()

    def get_assets_in_location(self, location: [int, int], planet=None) -> [faction.assets.AssetInstance]:
        asset_list = []
        for faction_instance in self.factions:
            for asset_instance in faction_instance.assets:
                if asset_instance.x_coord == location[0] and asset_instance.y_coord == location[1]:
                    asset_list.append(asset_instance)

        if planet is not None:
            for asset_instance in asset_list:
                if asset_instance.planet != planet:
                    asset_list.remove(asset_instance)

        return asset_list
