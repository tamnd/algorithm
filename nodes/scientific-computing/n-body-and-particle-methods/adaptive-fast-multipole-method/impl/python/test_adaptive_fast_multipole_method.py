# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/adaptive-fast-multipole-method/. The authors are listed in prov/B4084E.jsonl.
"""Tests for the adaptive fast multipole method: the tree, the four lists and the accuracy against direct summation."""

import math
import random
import unittest

from adaptive_fast_multipole_method import (
    adaptive_fmm,
    adjacent,
    box_center,
    build_lists,
    build_tree,
    direct,
    eval_local,
    eval_multipole,
    p2l,
    p2m,
)


def clustered(n, seed):
    """Three tight Gaussian clusters and a thin uniform background."""
    rng = random.Random(seed)
    centers = [complex(0.2, 0.3), complex(0.7, 0.75), complex(0.8, 0.2)]
    z = []
    while len(z) < n:
        if rng.random() < 0.85:
            c = centers[rng.randrange(3)]
            w = c + complex(rng.gauss(0, 0.02), rng.gauss(0, 0.02))
        else:
            w = complex(rng.random(), rng.random())
        if 0 <= w.real < 1 and 0 <= w.imag < 1:
            z.append(w)
    q = [rng.uniform(-1, 1) for _ in range(n)]
    return q, z


def rel(a, b):
    num = math.sqrt(sum(abs(x - y) ** 2 for x, y in zip(a, b)))
    den = math.sqrt(sum(abs(y) ** 2 for y in b))
    return num / den


def ancestors(b):
    l, x, y = b
    return [(k, x >> (l - k), y >> (l - k)) for k in range(l + 1)]


class TestTree(unittest.TestCase):
    def setUp(self):
        self.q, self.z = clustered(400, 3)
        self.members, self.children = build_tree(self.z, 10)
        self.leaves = [b for b in self.children if not self.children[b]]

    def test_leaves_are_small_and_at_many_levels(self):
        for b in self.leaves:
            self.assertLessEqual(len(self.members[b]), 10)
            self.assertGreater(len(self.members[b]), 0)
        self.assertGreaterEqual(len({b[0] for b in self.leaves}), 4)

    def test_leaves_partition_the_charges(self):
        seen = sorted(i for b in self.leaves for i in self.members[b])
        self.assertEqual(seen, list(range(400)))
        for b in self.leaves:
            l, ix, iy = b
            h = 1.0 / (1 << l)
            for i in self.members[b]:
                self.assertTrue(ix * h <= self.z[i].real < (ix + 1) * h)
                self.assertTrue(iy * h <= self.z[i].imag < (iy + 1) * h)

    def test_each_leaf_pair_is_covered_once(self):
        U, V, W, X = build_lists(self.children)
        for t in self.leaves:
            at = ancestors(t)
            for c in self.leaves:
                ac = set(ancestors(c))
                routes = int(c in U[t])
                routes += sum(1 for a in at for v in V[a] if v in ac)
                routes += sum(1 for w in W[t] if w in ac)
                routes += sum(1 for a in at for x in X[a] if x == c)
                self.assertEqual(routes, 1, (t, c))
                self.assertEqual(c in U[t], adjacent(c, t))

    def test_lists_are_well_separated(self):
        U, V, W, X = build_lists(self.children)
        for b, vs in V.items():
            for c in vs:
                self.assertEqual(c[0], b[0])
                self.assertGreaterEqual(abs(box_center(c) - box_center(b)), 2.0 / (1 << b[0]) - 1e-12)
        for b, ws in W.items():
            for d in ws:
                self.assertGreater(d[0], b[0])
                self.assertFalse(adjacent(d, b))
                self.assertTrue(adjacent(ancestors(d)[-2], b))
                self.assertIn(b, X[d])


class TestTranslations(unittest.TestCase):
    def test_p2l_and_multipole_field(self):
        rng = random.Random(1)
        q = [rng.uniform(-1, 1) for _ in range(6)]
        z = [complex(0.75 + 0.2 * rng.random(), 0.1 + 0.2 * rng.random()) for _ in range(6)]
        idx = range(6)
        center = complex(0.2, 0.2)
        w = complex(0.25, 0.15)
        exact_u = sum(qi * math.log(abs(w - zi)) for qi, zi in zip(q, z))
        exact_f = sum(qi / (w - zi).conjugate() for qi, zi in zip(q, z))
        v, dv = eval_local(p2l(q, z, idx, center, 25), center, w)
        self.assertAlmostEqual(v.real, exact_u, places=10)
        self.assertLess(abs(dv.conjugate() - exact_f), 1e-9)
        src = complex(0.85, 0.2)
        mv, mdv = eval_multipole(p2m(q, z, idx, src, 25), src, w)
        self.assertAlmostEqual(mv.real, exact_u, places=10)
        self.assertLess(abs(mdv.conjugate() - exact_f), 1e-9)


class TestAdaptiveFMM(unittest.TestCase):
    def test_matches_direct_and_improves_with_p(self):
        q, z = clustered(400, 3)
        ud, fd = direct(q, z)
        errs = []
        for p in (3, 6, 12, 20):
            u, f, st = adaptive_fmm(q, z, p=p, s=10)
            errs.append((rel(u, ud), rel(f, fd)))
        for k in range(3):
            self.assertLess(errs[k + 1][0], errs[k][0] / 10)
            self.assertLess(errs[k + 1][1], errs[k][1] / 10)
        self.assertLess(errs[-1][0], 1e-10)
        self.assertLess(errs[-1][1], 1e-8)

    def test_near_field_is_small_for_clusters(self):
        q, z = clustered(400, 3)
        u, f, st = adaptive_fmm(q, z, p=4, s=10)
        self.assertLess(st["p2p"], 400 * 399 // 8)
        self.assertGreater(st["m2p"], 0)
        self.assertGreater(st["p2l"], 0)

    def test_uniform_points(self):
        rng = random.Random(8)
        z = [complex(rng.random(), rng.random()) for _ in range(300)]
        q = [rng.uniform(-1, 1) for _ in range(300)]
        ud, fd = direct(q, z)
        u, f, st = adaptive_fmm(q, z, p=16, s=8)
        self.assertLess(rel(u, ud), 1e-8)
        self.assertLess(rel(f, fd), 1e-7)

    def test_linear_in_the_charges(self):
        q, z = clustered(120, 4)
        rng = random.Random(9)
        r = [rng.uniform(-1, 1) for _ in range(120)]
        u1, f1, _ = adaptive_fmm(q, z, p=8, s=6)
        u2, f2, _ = adaptive_fmm(r, z, p=8, s=6)
        u3, f3, _ = adaptive_fmm([2 * a - b for a, b in zip(q, r)], z, p=8, s=6)
        for a, b, c in zip(u1, u2, u3):
            self.assertAlmostEqual(c, 2 * a - b, places=9)

    def test_small_inputs(self):
        self.assertEqual(adaptive_fmm([], [], p=4)[0], [])
        u, f, _ = adaptive_fmm([2.0], [complex(0.3, 0.3)], p=4)
        self.assertEqual(u, [0.0])
        self.assertEqual(f, [0j])
        q = [1.0, -1.0, 0.5]
        z = [complex(0.1, 0.1), complex(0.9, 0.9), complex(0.5, 0.2)]
        u, f, _ = adaptive_fmm(q, z, p=6, s=1)
        ud, fd = direct(q, z)
        for a, b in zip(u, ud):
            self.assertAlmostEqual(a, b, places=4)


if __name__ == "__main__":
    unittest.main()
