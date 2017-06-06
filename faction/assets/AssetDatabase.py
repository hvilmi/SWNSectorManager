import json
from . import Asset


class AssetDatabase:
    def __init__(self):
        self.asset_dict = {}
        self.load_assets('cunning.assets')
        self.load_assets('force.assets')
        self.load_assets('wealth.assets')

    def load_assets(self, file_name):
        """Loads a file containing assets in json format and outputs them as objects."""

        with open(file_name, 'r') as f:
            temp_dict = json.load(f)

        assets = {}
        for asset in temp_dict:
            new_asset = Asset.Asset(asset['name'], asset['type'], asset['hp'], asset['cost'], asset['tl'],
                                    asset['asset_class'], asset['attack'], asset['counterattack'], asset['special'])
            self.asset_dict[asset['name']] = new_asset

    def query(self, name='', type='', tl=10, asset_class='', max_cost=999, min_cost=0, max_level=8):
        """Queries loaded assets for those matching given criteria. If name argument is given, only queries for it."""
        if name != '':
            return [self.asset_dict[name]]
        else:
            temp_assets = []
            for key, asset in self.asset_dict.items():
                if type in asset.type and asset.tl <= tl and asset_class in asset.asset_class and int(max_level) >= int(asset.type[1:]) and max_cost >= asset.cost >= min_cost:
                    temp_assets.append(asset)
            return temp_assets
