from .assets import AssetInstance
from .assets import Asset


class Faction:
    def __init__(self, name, hp, force, cunning, wealth, fac_creds, xp, homeworld):
        self.name = name
        self.hp = hp
        self.force = force
        self.cunning = cunning
        self.wealth = wealth
        self.fac_creds = fac_creds
        self.assets = []
        self.xp = xp
        self.homeworld = homeworld

    def get_level_with_string(self, string):
        levels = {'cunning': self.cunning, 'force': self.force, 'wealth': self.wealth}
        return levels[string]

    def add_new_asset(self, star, planet, base_asset: Asset.Asset):
        new_asset = AssetInstance.AssetInstance(base_asset, base_asset.max_hp, star, planet)
        self.assets.append(new_asset)

    def add_asset(self, star, planet, cur_hp, base_asset):
        new_asset = AssetInstance.AssetInstance(base_asset, cur_hp, star, planet)
        self.assets.append(new_asset)

    def get_occupied_planets(self):
        locations = []
        for asset_instance in self.assets:
            locations.append(asset_instance.get_location())
        # Convert list of asset locations to a set and back to list to remove duplicates
        return list(set(locations))
