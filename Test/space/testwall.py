import unittest
from knot.space.hexagonal import Hexagon
from knot.tool import Cut, Cutter


class TestWall(unittest.TestCase):

    def setUp(self):
        self.shape = Hexagon()
        self.com = self.shape.com()
        self.lattice = self.shape.lattice((5, 5), set())
        self.paper = self.shape.paper()
        self.cutter = Cutter(self.paper.identity())

    def _first_open_wall(self):
        for cell in self.lattice.cells.values():
            for com in self.com:
                if com in cell.walls and cell.walls[com].can_be_door(com):
                    return cell.walls[com], com
        return None, None

    def test_wall_starts_solid(self):
        for cell in self.lattice.cells.values():
            for com in self.com:
                if com in cell.walls:
                    self.assertTrue(cell.walls[com].is_wall())
            break  # just check first cell

    def test_make_door(self):
        wall, com = self._first_open_wall()
        self.assertIsNotNone(wall)
        wall.make_door(com, self.cutter, Cut.I)
        self.assertFalse(wall.is_wall())

    def test_code_before_door(self):
        for cell in self.lattice.cells.values():
            for com in self.com:
                if com in cell.walls:
                    self.assertEqual(cell.walls[com].code(com), "O")
                    return

    def test_make_solid(self):
        wall, com = self._first_open_wall()
        self.assertIsNotNone(wall)
        wall.make_door(com, self.cutter, Cut.X)
        wall.make_solid()
        self.assertTrue(wall.is_wall())


if __name__ == '__main__':
    unittest.main()
