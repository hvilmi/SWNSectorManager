import Planet


class StarSystem:
    """Container for Planets"""

    def __init__(self, name='', coord=(-1,-1), planets=None):
        if planets:
            self.planets = planets
        else:
            self.planets = []
        self.name = name
        self.coord = coord

    def set_name(self, name):
        self.name = name

    def set_coord(self, coord):
        self.coord = coord


    def add_planet(self, planet):
        self.planets.append(planet)
        print('added existing planet')

    def add_new_planet(self, name, pop, desc, tags, tl):
        new_planet = Planet.Planet(name, pop, desc, tags, tl)
        self.planets.append(new_planet)

    def get_planets(self):
        return self.planets

    def get_name(self):
        return self.name

    def get_coord(self):
        return self.coord


    def get_planet_by_name(self, name):
        for planet in self.planets:
            if planet.get_name() == name:
                return planet

