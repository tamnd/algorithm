# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/burnt-pancake-problem/. The authors are listed in prov/THR7VX.jsonl.
import unittest
from math import factorial

from burnt_pancake_problem import (
    all_stacks,
    apply_flips,
    burnt_pancake_number,
    distances,
    flip,
    simple_sort,
    unburnt_distances,
)

# OEIS A078941, n = 1 .. 17.
A078941 = [1, 4, 6, 8, 10, 12, 14, 15, 17, 18, 19, 21, 22, 23, 25, 26, 28]


def breakpoints(s):
    """Adjacent pairs (with n + 1 below the stack) that are not x, x + 1."""
    t = list(s) + [len(s) + 1]
    return sum(1 for x, y in zip(t, t[1:]) if y != x + 1)


class TestFlip(unittest.TestCase):
    def test_flip(self):
        self.assertEqual(flip((3, -1, 2), 2), (1, -3, 2))
        self.assertEqual(flip((3, -1, 2), 3), (-2, 1, -3))
        self.assertEqual(flip(flip((3, -1, 2), 3), 3), (3, -1, 2))

    def test_two_pancakes_upside_down(self):
        self.assertEqual(apply_flips((-1, -2), [2, 1, 2, 1]), (1, 2))


class TestExact(unittest.TestCase):
    def test_numbers_against_oeis(self):
        self.assertEqual([burnt_pancake_number(n) for n in range(1, 7)], A078941[:6])

    def test_state_count(self):
        for n in range(1, 7):
            self.assertEqual(len(distances(n)), 2 ** n * factorial(n))

    def test_all_upside_down_is_hardest(self):
        for n in range(1, 7):
            d = distances(n)
            self.assertEqual(d[tuple(-k for k in range(1, n + 1))], max(d.values()))

    def test_bounds_hold(self):
        self.assertEqual(burnt_pancake_number(1), 1)
        for n in range(2, 7):
            g = burnt_pancake_number(n)
            self.assertGreaterEqual(2 * g, 3 * n)
            self.assertEqual(g, 2 * n)

    def test_burnt_at_least_unburnt(self):
        for n in range(1, 7):
            d = distances(n)
            u = unburnt_distances(n)
            for perm, v in u.items():
                self.assertGreaterEqual(d[perm], v)

    def test_breakpoint_lower_bound(self):
        for n in range(1, 7):
            for s, v in distances(n).items():
                self.assertGreaterEqual(v, breakpoints(s))


class TestSimpleSort(unittest.TestCase):
    def test_sorts_every_stack(self):
        for n in range(1, 6):
            worst = 0
            for s in all_stacks(n):
                flips = simple_sort(s)
                self.assertEqual(apply_flips(s, flips), tuple(range(1, n + 1)))
                worst = max(worst, len(flips))
            self.assertEqual(worst, 3 * n - 2)


if __name__ == "__main__":
    unittest.main()
