import sector.SectorHexagon as shexagon


class SectorPathfinder:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.hexagons = []
        self.generate_hexagrid()

    def generate_hexagrid(self):
        """Generates a grid of hexagons with correct neighbours and sets i as self.hexagons"""
        # x_range = range(self.width)
        # y_range = range(self.height)
        # self.hexagons = [shexagon.Hexagon(x, y) for x in x_range for y in y_range]

        for x in range(self.width):
            self.hexagons.append([])
            for y in range(self.height):
                self.hexagons[x].append(shexagon.Hexagon(x, y))

        for column in self.hexagons:
            for hexagon in column:
                if hexagon.y > 0:
                    hexagon.add_neigbour(self.hexagons[hexagon.x][hexagon.y - 1])
                if hexagon.y < self.height - 1:
                    hexagon.add_neigbour(self.hexagons[hexagon.x][hexagon.y + 1])

                if hexagon.x % 2 == 0:
                    if hexagon.x < self.width - 1:
                        if hexagon.y > 0:
                            hexagon.add_neigbour(self.hexagons[hexagon.x + 1][hexagon.y - 1])
                        hexagon.add_neigbour(self.hexagons[hexagon.x + 1][hexagon.y])
                    if hexagon.x > 0:
                        if hexagon.y > 0:
                            hexagon.add_neigbour(self.hexagons[hexagon.x - 1][hexagon.y - 1])
                        hexagon.add_neigbour(self.hexagons[hexagon.x - 1][hexagon.y])

                else:
                    hexagon.add_neigbour(self.hexagons[hexagon.x - 1][hexagon.y])
                    if hexagon.x < self.width - 1:
                        hexagon.add_neigbour(self.hexagons[hexagon.x + 1][hexagon.y])
                        if hexagon.y < self.height - 1:
                            hexagon.add_neigbour(self.hexagons[hexagon.x + 1][hexagon.y + 1])
                    if hexagon.y < self.height - 1:
                        hexagon.add_neigbour(self.hexagons[hexagon.x - 1][hexagon.y + 1])

    def find_path(self, start_coord, end_coord):
        star_hexagon = self.hexagons[start_coord[0]][start_coord[1]]
        goal_hexagon = self.hexagons[end_coord[0]][end_coord[1]]
        # TODO: Implement suitable path finding algorithm

    def get_neighbours(self, x, y):
        neighbour_list = self.hexagons[x][y].neighbours
        final_list = []
        for neighbour in neighbour_list:
            final_list.append(neighbour[0])
        return final_list

