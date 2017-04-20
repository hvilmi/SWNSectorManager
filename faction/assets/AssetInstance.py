from .Asset import Asset


class AssetInstance:
    def __init__(self, base_asset, cur_hp=None, star=None, planet=None):
        """

        :type base_asset: Asset
        """
        self.cur_hp = cur_hp
        self.base_asset = base_asset
        self.star = star
        self.planet = planet

    def get_name(self):
        return self.base_asset.get_name()

    def get_location(self):
        return self.star + " - " + self.planet
