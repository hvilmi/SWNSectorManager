from .Asset import Asset


class AssetInstance:
    cur_index = 0

    def __init__(self, base_asset, cur_hp, star, planet, index):
        """

        :type base_asset: Asset
        """
        self.cur_hp = cur_hp
        self.base_asset = base_asset
        self.star = star
        self.planet = planet
        self.index = index

    def get_name(self):
        return self.base_asset.get_name()

    def get_location(self):
        return self.star + " - " + self.planet

    def set_location(self, location):
        """location is a string in format '<Star> - <Planet>'"""
        star, planet = location.split(' - ')
        self.star = star
        self.planet = planet
