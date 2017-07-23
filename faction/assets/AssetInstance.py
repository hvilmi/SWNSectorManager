from .Asset import Asset
from .. import Faction
import Sector


class AssetInstance:
    cur_index = 0

    def __init__(self, parent: Faction, base_asset, cur_hp, star, planet, index, x_coord=None, y_coord=None):
        """

        :type base_asset: Asset
        """
        self.parent = parent
        self.cur_hp = cur_hp
        self.base_asset = base_asset
        self.star = star
        self.planet = planet
        self.index = index
        if x_coord is not None and y_coord is not None:
            self.y_coord = y_coord
            self.x_coord = x_coord
        else:
            star = self.get_sector().get_star_by_name(self.star)
            self.x_coord = star.coord[0]
            self.y_coord = star.coord[1]
        print('Created AssetInstance with coords ', self.x_coord, self.y_coord)

    def get_name(self):
        return self.base_asset.get_name()

    def get_location(self):
        if self.planet == '':
            if self.star == '':
                return '0' + str(self.x_coord) + '0' + str(self.y_coord)
            else:
                return self.star
        return self.star + " - " + self.planet

    def set_location(self, location, coordinates=None):
        """location is a string in format '<Star> - <Planet>', '<Star>' or '0X0Y'."""
        print('set_location with ', location)
        self.planet = ''
        self.star = ''
        if ' - ' not in location:
            if coordinates is not None:
                self.x_coord = coordinates[0]
                self.y_coord = coordinates[1]
                star = self.get_sector().get_star_by_coord((coordinates[0], coordinates[1]))
                if star:
                    # Set star name if system happens to have one
                    self.star = star

            else:
                self.star = ''
                self.planet = ''
                self.x_coord = int(location[1])
                self.y_coord = int(location[3])
                star = self.get_sector().get_star_by_coord((self.x_coord, self.y_coord))
                if star:
                    self.star = star

        else:
            star, planet = location.split(' - ')
            self.star = star
            self.planet = planet
            if coordinates is not None:
                self.x_coord = coordinates[0]
                self.y_coord = coordinates[1]
            else:
                star_coord = self.get_sector().get_star_by_name(star).coord
                self.x_coord = star_coord[0]
                self.y_coord = star_coord[1]

    def get_coord(self):
        """ Returns coordinates of asset as list [x,y]"""
        return [self.x_coord, self.y_coord]

    def get_relocation_choices(self):
        """Returns list of hexagons on sector map which are next to current location of asset.
        First row of elements of list are in format 0x0y' when hexagon is empty and 'Star - planet' when hexagon
        contains a star.
        Second row is x and y coordinates of the option"""

        return self.get_sector().get_star_vicinity([self.x_coord, self.y_coord])

    def get_sector(self) -> Sector.Sector:
        return self.parent.controller.sector
