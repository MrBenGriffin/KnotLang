# encoding: utf-8
# from .crs import Coords
# from .shape import Shape
# from .wall import Wall
# from knot.space.hexagonal import Com


class Cell:
    last = None

    def __init__(self, dim, walls):
        self.dim = dim
        self.tool = None
        self.opened = False
        self.opened_from = None
        self.walls = walls
        for com in self.walls:
            self.walls[com].set_cell(self, com.opposite)

    def name(self):
        pass

    def tuple(self):
        return tuple(self.dim)

    def back_fill(self):
        self.opened = False
        self.opened_from = None
        for compass, wall in self.walls.items():
            wall.make_solid(compass)
        self.tool = None

    def mined(self) -> bool:
        return self.opened

    def move(self, com):
        if com in self.walls and self.walls[com]:
            wall = self.walls[com]
            if not wall.is_wall():
                return wall.cells[com]
        return self

    def exits(self):
        list_of_exits = self.level_exits()
        return list_of_exits

    def level_exits(self):
        list_of_exits = []
        for compass, wall in self.walls.items():
            if not wall.is_wall():
                list_of_exits.append(compass)
        return list_of_exits

    def count_level_exits(self):
        count = 0
        for wall in list(self.walls.values()):
            if not wall.is_wall():
                count += 1
        return count

    def level_walls_to_be_dug(self, walls):
        for compass, wall in self.walls.items():
            if wall.can_be_dug(compass):
                walls.append(compass)
        return walls

    def neighbours(self):
        """
        :return: dict [Com: Neighbour] of neighbours
        """
        neighbours = {}
        for compass, wall in self.walls.items():
            neighbour = wall.cell(compass)
            if neighbour:
                neighbours[compass] = neighbour
        return neighbours

    def walls_that_can_be_doors(self):
        """
        :return: list [Com] that may be doors..
        """
        return [com for com, wall in self.walls.items() if wall.can_be_door(com)]

    def walls_that_can_be_dug(self):
        """
        :return: list [Com] that may be dug..
        """
        return self.level_walls_to_be_dug([])

    def is_a_passage(self):
        exits = self.walls_that_can_be_dug()
        if not exits:
            exits = self.level_exits()
            return len(exits) == 2 and exits[0] == exits[1].opposite
        return False

    def open(self, tool, com):
        # Open FROM direction comp.
        if not self.opened and not self.tool:
            self.opened = True
            self.opened_from = com
            self.tool = tool

    def wall(self, com):
        return None if com not in self.walls else self.walls[com]

    def __str__(self):
        return str(self.dim) + " " + self.code()

    def __repr__(self):
        return "Cell (" + str(self.dim) + " " + self.code() + ")"

    def code(self):
        if not self.mined():
            return "o" * len(self.walls)
        result = ''.join(["O" if c not in self.walls else self.walls[c].code(c) for c in self.dim.com()])
        return "  " if result == "OOOOOO" else result

    def __cmp__(self, other):
        return self.walls == other.walls
