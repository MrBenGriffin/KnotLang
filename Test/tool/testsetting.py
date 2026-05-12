import unittest
from knot.tool import Setting, Cut, DummyRng


class TestSetting(unittest.TestCase):

    def test_all_twists(self):
        # straights_balance=0.0 → random() always >= 0.0 → always Cut.X
        s = Setting(straights_balance=0.0, rng=DummyRng(0))
        for _ in range(10):
            self.assertEqual(s.choose(), Cut.X)

    def test_all_straights(self):
        # straights_balance=1.0 → random() never >= 1.0 → always Cut.I
        s = Setting(straights_balance=1.0, rng=DummyRng(0))
        for _ in range(10):
            self.assertEqual(s.choose(), Cut.I)

    def test_mixed(self):
        # DummyRng: 0.0, 0.25, 0.5, 0.75, 0.999, repeat
        # straights_balance=0.5: values < 0.5 → I, >= 0.5 → X
        s = Setting(straights_balance=0.5, rng=DummyRng(0))
        expected = [Cut.I, Cut.I, Cut.X, Cut.X, Cut.X,
                    Cut.I, Cut.I, Cut.X, Cut.X, Cut.X]
        for i, want in enumerate(expected):
            self.assertEqual(s.choose(), want, f"Step {i}")


if __name__ == '__main__':
    unittest.main()
