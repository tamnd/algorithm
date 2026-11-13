# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gods-number/. The authors are listed in prov/YQFNF0.jsonl.
import unittest

from gods_number import (
    CUBE_POSITIONS,
    POCKET_POSITIONS,
    canonical_counts_htm,
    canonical_counts_qtm,
    counting_lower_bound,
    cube_layers,
    parity_lower_bound_qtm,
    pocket_distances,
)


class TestCounting(unittest.TestCase):
    def test_positions(self):
        self.assertEqual(CUBE_POSITIONS, 43252003274489856000)
        self.assertEqual(POCKET_POSITIONS, 3674160)

    def test_counts_bound_the_layers(self):
        h = canonical_counts_htm(4)
        q = canonical_counts_qtm(4)
        bh = cube_layers(4, "htm")
        bq = cube_layers(4, "qtm")
        self.assertEqual(bh, [1, 18, 243, 3240, 43239])
        self.assertEqual(bq, [1, 12, 114, 1068, 10011])
        self.assertEqual(h[:4], bh[:4])
        for a, b in zip(h + q, bh + bq):
            self.assertGreaterEqual(a, b)

    def test_htm_bound(self):
        h = canonical_counts_htm(20)
        self.assertEqual(h[:4], [1, 18, 243, 3240])
        self.assertEqual(counting_lower_bound(h, CUBE_POSITIONS), 18)
        self.assertLess(sum(h[:18]), CUBE_POSITIONS)

    def test_qtm_bounds(self):
        q = canonical_counts_qtm(24)
        self.assertEqual(counting_lower_bound(q, CUBE_POSITIONS), 20)
        self.assertEqual(parity_lower_bound_qtm(q, CUBE_POSITIONS), 21)


class TestPocketCube(unittest.TestCase):
    def test_half_turn_metric(self):
        c = pocket_distances("htm")
        self.assertEqual(sum(c), POCKET_POSITIONS)
        self.assertEqual(len(c) - 1, 11)
        self.assertEqual(c[-1], 2644)

    def test_quarter_turn_metric(self):
        c = pocket_distances("qtm")
        self.assertEqual(sum(c), POCKET_POSITIONS)
        self.assertEqual(len(c) - 1, 14)
        self.assertEqual(c[-1], 276)
        # every quarter turn is an odd corner permutation, so even and odd
        # layers each hold half of the positions
        self.assertEqual(sum(c[0::2]), POCKET_POSITIONS // 2)


if __name__ == "__main__":
    unittest.main()
