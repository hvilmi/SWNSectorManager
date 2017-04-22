import Planet
import StarSystem

class Sector:

    def __init__(self, name=''):
        self.stars = []
        self.name = name

    def get_star_by_coord(self, coord):
        for star in self.stars:
            if star.coord[0] == coord[0] and star.coord[1] == coord[1]:
                return star
        return None

    def add_star(self, star):
        self.stars.append(star)

    def get_stars(self):
        return self.stars

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def clear(self):
        self.stars = []
        self.name = ''

    def get_alphabetical_planet_list(self):
        """Returns list of all current planets in alphabetical order. Every entry is in format "<Star> - <Planet>" """
        planet_list = []
        for star in self.stars:
            for planet in star.get_planets():
                planet_list.append(star.get_name() +" - "+ planet.get_name())
        if len(planet_list) == 0:
            planet_list = [""]
        return sorted(planet_list, key=str.lower)

    def get_planet_by_name(self, name):
        '''Returns first planet found with a given name'''
        for star in self.stars:
            return star.get_planet_by_name(name)
