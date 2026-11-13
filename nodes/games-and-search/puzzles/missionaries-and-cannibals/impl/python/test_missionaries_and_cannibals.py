# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/missionaries-and-cannibals/. The authors are listed in prov/YW0KDJ.jsonl.
import unittest

from missionaries_and_cannibals import (
    bfs,
    count_shortest,
    safe,
    shortest_crossings,
    shortest_plan,
)


def plan_is_valid(path, n, k):
    if path[0] != (n, n, 1) or path[-1] != (0, 0, 0):
        return False
    for (m, c, b), (m2, c2, b2) in zip(path, path[1:]):
        if b2 != 1 - b:
            return False
        i, j = abs(m - m2), abs(c - c2)
        moved_away = (m2 <= m and c2 <= c) if b == 1 else (m2 >= m and c2 >= c)
        if not moved_away or not 1 <= i + j <= k or not safe(m2, c2, n):
            return False
    return True


class TestClassic(unittest.TestCase):
    def test_eleven_crossings(self):
        self.assertEqual(shortest_crossings(3, 2), 11)
        path = shortest_plan(3, 2)
        self.assertEqual(len(path), 12)
        self.assertTrue(plan_is_valid(path, 3, 2))

    def test_four_shortest_solutions(self):
        self.assertEqual(count_shortest(3, 2), 4)

    def test_state_counts(self):
        dist, _ = bfs(3, 2)
        safe_states = [(m, c, b) for m in range(4) for c in range(4) for b in (0, 1) if safe(m, c, 3)]
        self.assertEqual(len(safe_states), 20)
        self.assertEqual(len(dist), 16)


class TestLimits(unittest.TestCase):
    def test_table(self):
        expected = {
            2: [1, 5, 11, None, None, None, None, None, None, None],
            3: [1, 3, 5, 9, 11, None, None, None, None, None],
            4: [1, 1, 3, 5, 7, 9, 11, 13, 15, 17],
        }
        for k, row in expected.items():
            self.assertEqual([shortest_crossings(n, k) for n in range(1, 11)], row)

    def test_largest_solvable(self):
        for k in (2, 3):
            for n in range(1, 16):
                self.assertEqual(shortest_crossings(n, k) is not None, n <= 2 * k - 1, (n, k))

    def test_boat_of_one(self):
        for n in range(1, 6):
            self.assertIsNone(shortest_crossings(n, 1))

    def test_boat_of_four(self):
        for n in range(3, 31):
            self.assertEqual(shortest_crossings(n, 4), 2 * n - 3)

    def test_boat_rule_changes_nothing_here(self):
        for k in range(2, 6):
            for n in range(1, 9):
                self.assertEqual(shortest_crossings(n, k, boat_safe=True), shortest_crossings(n, k))

    def test_plans_valid(self):
        for k in (2, 3, 4, 5):
            for n in range(1, 8):
                path = shortest_plan(n, k)
                if path is not None:
                    self.assertTrue(plan_is_valid(path, n, k))


if __name__ == "__main__":
    unittest.main()
