import Planet
import StarSystem
import sector.SectorPathfinder as pathfinder


class Sector:
    def __init__(self, name=''):
        self.stars = []
        self.name = name
        self.pathfinder = pathfinder.SectorPathfinder(8, 10)

    def get_star_by_coord(self, coord) -> StarSystem.StarSystem:
        for star in self.stars:
            if star.coord[0] == coord[0] and star.coord[1] == coord[1]:
                return star
        return None

    def get_star_by_name(self, name) -> StarSystem.StarSystem:
        for star in self.stars:
            if star.name == name:
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
                planet_list.append(star.get_name() + " - " + planet.get_name())
        if len(planet_list) == 0:
            planet_list = [""]
        return sorted(planet_list, key=str.lower)

    def get_planet_by_name(self, name):
        """Returns first planet found with a given name"""
        for star in self.stars:
            if star.get_planet_by_name(name):
                return star.get_planet_by_name(name)

    def delete_star(self, star):
        self.stars.remove(star)

    def get_star_vicinity(self, star):
        if type(star) is StarSystem.StarSystem:
            coord = star.coord
        elif type(star) is str:
            coord = self.get_star_by_name(star)
        else:
            coord = star

        neighbours = self.pathfinder.get_neighbours(*coord)
        neighbour_list = []

        if self.get_star_by_coord(coord):
            for planet in self.get_star_by_coord(coord).planets:
                neighbour_list.append(self.get_star_by_coord(coord).name + ' - ' + planet.name)

        for neighbour in neighbours:
            if self.get_star_by_coord(neighbour.coord):
                star = self.get_star_by_coord(neighbour.coord)
                for planet in star.planets:
                    neighbour_list.append(star.name + ' - ' + planet.name)
            else:
                neighbour_list.append('0' + str(neighbour.coord[0]) + '0' + str(neighbour.coord[1]))

        return neighbour_list
