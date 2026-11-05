# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/reingold-tilford-layout/. The authors are listed in prov/NB9NJR.jsonl.
import random
import unittest
from fractions import Fraction

from reingold_tilford_layout import children_from_parents, layout


def oracle(children, root, sep):
    """Slow layout by the same rule: whole subtrees, not contours, O(n^2)."""
    order = []
    stack = [root]
    while stack:
        v = stack.pop()
        order.append(v)
        stack.extend(reversed(children[v]))
    pos = {}  # v -> dict of (u -> (x relative to v, depth below v))
    for v in reversed(order):
        placed = {}
        offs = []
        for c in children[v]:
            sub = pos.pop(c)
            if not placed:
                d = Fraction(0)
            else:
                d = None
                for u, (xu, du) in placed.items():
                    for w, (xw, dw) in sub.items():
                        if du == dw and (d is None or xu - xw + sep > d):
                            d = xu - xw + sep
            offs.append(d)
            for w, (xw, dw) in sub.items():
                placed[w] = (xw + d, dw)
        m = (offs[0] + offs[-1]) / 2 if offs else Fraction(0)
        cur = {v: (Fraction(0), 0)}
        for u, (xu, du) in placed.items():
            cur[u] = (xu - m, du + 1)
        pos[v] = cur
    res = pos[root]
    n = len(children)
    return [res[v][0] for v in range(n)], [res[v][1] for v in range(n)]


def random_parents(n, rng):
    return [-1] + [rng.randrange(v) for v in range(1, n)]


class TestReingoldTilford(unittest.TestCase):
    def test_page_example(self):
        ch, r = children_from_parents([-1, 0, 0, 1, 1, 2, 4, 4])
        x, y = layout(ch, r, sep=2)
        h = Fraction(1, 2)
        self.assertEqual(x, [0, -3 * h, 3 * h, -5 * h, -h, 3 * h, -3 * h, h])
        self.assertEqual(y, [0, 1, 1, 2, 2, 2, 3, 3])

    def test_single_vertex(self):
        self.assertEqual(layout([[]]), ([0], [0]))

    def test_path(self):
        n = 100000
        ch = [[v + 1] for v in range(n - 1)] + [[]]
        x, y = layout(ch)
        self.assertTrue(all(v == 0 for v in x))
        self.assertEqual(y, list(range(n)))

    def test_star(self):
        n = 7
        ch = [list(range(1, n))] + [[] for _ in range(n - 1)]
        x, y = layout(ch, sep=1)
        self.assertEqual(x, [0] + [Fraction(k) - Fraction(n - 2, 2) for k in range(n - 1)])
        self.assertEqual(y, [0] + [1] * (n - 1))

    def test_random_against_oracle(self):
        rng = random.Random(20260412)
        for _ in range(600):
            n = rng.randint(1, 30)
            ch, r = children_from_parents(random_parents(n, rng))
            sep = rng.choice([1, 2, 3])
            got = layout(ch, r, sep)
            self.assertEqual(got, oracle(ch, r, sep))
            x, y = got
            # neighbours on a level keep the order and the separation
            levels = {}
            stack = [r]
            while stack:
                v = stack.pop()
                levels.setdefault(y[v], []).append(v)
                stack.extend(reversed(ch[v]))
            for row in levels.values():
                for a, b in zip(row, row[1:]):
                    self.assertGreaterEqual(x[b] - x[a], sep)
            for v in range(n):
                if ch[v]:
                    self.assertEqual(x[v], (x[ch[v][0]] + x[ch[v][-1]]) / 2)


if __name__ == "__main__":
    unittest.main()
