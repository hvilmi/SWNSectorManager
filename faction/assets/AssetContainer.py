class FacAssetContainer:
    def __init__(self, assets=None):
        """Class for storing and retrieving asset templates for factions"""
        if not (assets is None):
            self.assets = assets
        else:
            self.assets = [{}]

    def query(self, name='', tl=0, type='', max_level=8):
        temp_assets = [asset for asset in self.assets if
                       name in asset['name'] and tl <= asset['tl'] and type in asset['type'] and max_level >= asset
                       ['level']]
        return temp_assets
