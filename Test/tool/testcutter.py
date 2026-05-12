import unittest
from knot.tool.cut import Cut
from knot.tool import Setting


class TestCut(unittest.TestCase):

    def test_opposite(self):
        self.assertEqual(Cut.O.opposite, Cut.O)
        self.assertEqual(Cut.I.opposite, Cut.I)
        self.assertEqual(Cut.X.opposite, Cut.X)
        self.assertEqual(Cut.H.opposite, Cut.B)
        self.assertEqual(Cut.B.opposite, Cut.H)

    def test_hex_bins(self):
        self.assertEqual(Cut.O.hex(), 0)
        self.assertEqual(Cut.I.hex(), 1)
        self.assertEqual(Cut.X.hex(), 2)
        self.assertEqual(Cut.H.hex(), 2)
        self.assertEqual(Cut.B.hex(), 2)

    def test_str(self):
        self.assertEqual(str(Cut.O), "O")
        self.assertEqual(str(Cut.I), "I")
        self.assertEqual(str(Cut.X), "X")
        self.assertEqual(str(Cut.H), "H")
        self.assertEqual(str(Cut.B), "B")


class TestSetting(unittest.TestCase):

    def test_all_twists(self):
        # straights_balance=0.0 → random() always >= 0.0 → always Cut.X
        s = Setting(straights_balance=0.0)
        for _ in range(20):
            self.assertEqual(s.choose(), Cut.X)

    def test_all_straights(self):
        # straights_balance=1.0 → random() never >= 1.0 → always Cut.I
        s = Setting(straights_balance=1.0)
        for _ in range(20):
            self.assertEqual(s.choose(), Cut.I)


if __name__ == '__main__':
    unittest.main()
