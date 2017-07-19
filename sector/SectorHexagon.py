

class Hexagon:

    def __init__(self, x, y):
        self.coord = [x, y]
        self.neighbours = []

    def add_neigbour(self, neighbour, cost=1):
        self.neighbours.append([neighbour, cost])
