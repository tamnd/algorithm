# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/yen-k-shortest-paths/. The authors are listed in prov/0RC5G2.jsonl.

import random
import unittest

from yen_k_shortest_paths import yen_k_shortest_paths

NAMES = "CDEFGH"
EXAMPLE = [
    ("C", "D", 3), ("C", "E", 2), ("D", "F", 4), ("E", "D", 1), ("E", "F", 2),
    ("E", "G", 3), ("F", "G", 2), ("F", "H", 1), ("G", "H", 2),
]


def named(edges):
    return [(NAMES.index(a), NAMES.index(b), w) for a, b, w in edges]


def all_simple_paths(n, edges, s, t):
    """Independent oracle: every simple s-t path by depth-first search, with its least weight."""
    best = {}
    for u, v, w in edges:
        if u != v and ((u, v) not in best or w < best[(u, v)]):
            best[(u, v)] = w
    out = [[] for _ in range(n)]
    for (u, v), w in best.items():
        out[u].append((v, w))
    found = []

    def go(u, path, weight):
        if u == t:
            found.append((weight, tuple(path)))
            return
        for v, w in out[u]:
            if v not in path:
                path.append(v)
                go(v, path, weight + w)
                path.pop()

    go(s, [s], 0)
    return sorted(found), best


class TestYen(unittest.TestCase):
    def test_example(self):
        got = yen_k_shortest_paths(6, named(EXAMPLE), 0, 5, 3)
        self.assertEqual([(w, "".join(NAMES[x] for x in p)) for w, p in got], [(5, "CEFH"), (7, "CEGH"), (8, "CDFH")])

    def test_all_paths_of_example(self):
        got = yen_k_shortest_paths(6, named(EXAMPLE), 0, 5, 100)
        self.assertEqual([w for w, _ in got], [5, 7, 8, 8, 8, 11, 11])

    def test_unreachable_and_trivial(self):
        self.assertEqual(yen_k_shortest_paths(3, [(0, 1, 1)], 0, 2, 4), [])
        self.assertEqual(yen_k_shortest_paths(2, [(0, 1, 1)], 0, 0, 3), [(0, [0])])
        self.assertEqual(yen_k_shortest_paths(2, [(0, 1, 1)], 0, 1, 0), [])

    def test_negative_weights_and_cycles_rejected(self):
        with self.assertRaises(ValueError):
            yen_k_shortest_paths(2, [(0, 1, -1)], 0, 1, 2)
        with self.assertRaises(ValueError):
            yen_k_shortest_paths(3, [(0, 1, 1), (1, 2, 1), (2, 1, -5)], 0, 2, 2)

    def test_cycles_and_parallel_arcs(self):
        edges = [(0, 1, 1), (1, 0, 1), (1, 2, 1), (0, 2, 5), (0, 2, 3), (2, 2, 0)]
        self.assertEqual(yen_k_shortest_paths(3, edges, 0, 2, 5), [(2, [0, 1, 2]), (3, [0, 2])])

    def test_random_against_enumeration(self):
        rng = random.Random(1971)
        for _ in range(600):
            n = rng.randint(1, 7)
            m = rng.randint(0, 3 * n)
            edges = [(rng.randrange(n), rng.randrange(n), rng.randint(0, 6)) for _ in range(m)]
            s, t = rng.randrange(n), rng.randrange(n)
            k = rng.randint(1, 12)
            expected, best = all_simple_paths(n, edges, s, t)
            got = yen_k_shortest_paths(n, edges, s, t, k)
            self.assertEqual([w for w, _ in got], [w for w, _ in expected[:k]])
            paths = [tuple(p) for _, p in got]
            self.assertEqual(len(set(paths)), len(paths))
            for w, p in got:
                self.assertEqual((p[0], p[-1]), (s, t))
                self.assertEqual(len(set(p)), len(p))
                self.assertEqual(sum(best[(p[i], p[i + 1])] for i in range(len(p) - 1)), w)


if __name__ == "__main__":
    unittest.main()
