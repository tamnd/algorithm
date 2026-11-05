# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/slow-apsp-matrix-multiplication/. The authors are listed in prov/EK3RJN.jsonl.

import math
import random
import unittest

from slow_apsp_matrix_multiplication import extend, slow_apsp, weight_matrix

INF = math.inf
CLRS = [(0, 1, 3), (0, 2, 8), (0, 4, -4), (1, 3, 1), (1, 4, 7), (2, 1, 4), (3, 0, 2), (3, 2, -5), (4, 3, 6)]


def bellman_ford_all(n, edges):
    """Independent oracle: Bellman-Ford from every source, with a final pass for negative cycles."""
    rows = []
    for s in range(n):
        d = [INF] * n
        d[s] = 0
        for _ in range(n - 1):
            for u, v, w in edges:
                if d[u] + w < d[v]:
                    d[v] = d[u] + w
        for u, v, w in edges:
            if d[u] + w < d[v]:
                return None
        rows.append(d)
    return rows


class TestSlowAPSP(unittest.TestCase):
    def test_clrs_example(self):
        self.assertEqual(
            slow_apsp(5, CLRS),
            [[0, 1, -3, 2, -4], [3, 0, -4, 1, -1], [7, 4, 0, 5, 3], [2, -1, -5, 0, -2], [8, 5, 1, 6, 0]],
        )

    def test_intermediate_matrix(self):
        w = weight_matrix(5, CLRS)
        self.assertEqual(extend(w, w)[0], [0, 3, 8, 2, -4])
        self.assertEqual(extend(w, w)[4], [8, INF, 1, 6, 0])

    def test_negative_cycles(self):
        self.assertIsNone(slow_apsp(5, CLRS + [(2, 3, 4)]))
        self.assertIsNone(slow_apsp(1, [(0, 0, -1)]))
        # a negative cycle through all n vertices needs the n-th product
        self.assertIsNone(slow_apsp(3, [(0, 1, 1), (1, 2, 1), (2, 0, -3)]))
        # a negative cycle that most vertices cannot reach is still reported
        self.assertIsNone(slow_apsp(4, [(0, 1, 1), (2, 3, -1), (3, 2, -1)]))

    def test_unreachable_and_small(self):
        self.assertEqual(slow_apsp(0, []), [])
        self.assertEqual(slow_apsp(1, [(0, 0, 5)]), [[0]])
        self.assertEqual(slow_apsp(3, [(0, 1, -2), (0, 1, 4)]), [[0, -2, INF], [INF, 0, INF], [INF, INF, 0]])

    def test_zero_cycle(self):
        self.assertEqual(slow_apsp(2, [(0, 1, 3), (1, 0, -3)]), [[0, 3], [-3, 0]])

    def test_random_against_bellman_ford(self):
        rng = random.Random(1974)
        negative = 0
        for _ in range(600):
            n = rng.randint(0, 6)
            m = rng.randint(0, 3 * n)
            low = rng.choice([0, -2, -4])
            edges = [(rng.randrange(n), rng.randrange(n), rng.randint(low, 9)) for _ in range(m)] if n else []
            expected = bellman_ford_all(n, edges)
            got = slow_apsp(n, edges)
            if expected is None:
                negative += 1
            self.assertEqual(got, expected)
        self.assertGreater(negative, 50)


if __name__ == "__main__":
    unittest.main()
