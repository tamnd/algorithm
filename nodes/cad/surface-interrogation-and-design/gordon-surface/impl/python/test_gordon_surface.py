# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gordon-surface/. The authors are listed in prov/8125BY.jsonl.

import random
import unittest
from fractions import Fraction as Fr

from gordon_surface import gordon_parts, gordon_surface
from si3spline import (add, curve_point, interpolate, iso_curve_u, iso_curve_v,
                       refine, sub, surface_point)

H = [0, 0, 0, Fr(1, 2), 1, 1, 1]


def example_network():
    """The network of the page: two leaning bumps that cross at the centre."""
    zero_u = [(Fr(0), Fr(0), Fr(0)), (Fr(1, 2), Fr(0), Fr(0)), (Fr(1), Fr(0), Fr(0))]
    bump_u = [(Fr(0), Fr(1, 2), Fr(0)), (Fr(1, 4), Fr(1, 2), Fr(2)),
              (Fr(3, 4), Fr(1, 2), Fr(0)), (Fr(1), Fr(1, 2), Fr(0))]
    top_u = [(x, Fr(1), z) for x, _, z in zero_u]
    u_curves = [([0, 0, 0, 1, 1, 1], zero_u), (H, bump_u), ([0, 0, 0, 1, 1, 1], top_u)]
    swap = lambda c: [(y, x, z) for x, y, z in c]
    v_curves = [(k, swap(c)) for k, c in u_curves]
    halves = [Fr(0), Fr(1, 2), Fr(1)]
    return u_curves, v_curves, halves, halves


def random_family(rng, cross, own, grid, deg, extra):
    """Curves through grid[i][j] at own[j], each with its own extra parameters.

    Curve i of the family passes through grid[i][j] at the parameter own[j].
    Its other interpolation points are random, so each curve gets its own
    averaging knots, and the family needs the knot merge.
    """
    curves = []
    for i in range(len(cross)):
        ts = set(own) | {Fr(0), Fr(1)}
        while len(ts) < len(own) + 2 + extra:
            ts.add(Fr(rng.randint(1, 99), 100))
        ts = sorted(ts)
        pts = [grid[i][own.index(t)] if t in own else
               tuple(Fr(rng.randint(-9, 9)) for _ in range(3)) for t in ts]
        curves.append(interpolate(ts, pts, deg))
    return curves


def random_network(rng, n, m, p, q):
    us = sorted(rng.sample([Fr(k, 20) for k in range(1, 20)], n - 2) + [Fr(0), Fr(1)])
    vs = sorted(rng.sample([Fr(k, 20) for k in range(1, 20)], m - 2) + [Fr(0), Fr(1)])
    grid = [[tuple(Fr(rng.randint(-9, 9)) for _ in range(3)) for _ in vs] for _ in us]
    v_curves = random_family(rng, us, vs, grid, q, rng.randint(0, 3))
    gridT = [[grid[i][j] for i in range(len(us))] for j in range(len(vs))]
    u_curves = random_family(rng, vs, us, gridT, p, rng.randint(0, 3))
    return u_curves, v_curves, us, vs


class TestGordonSurface(unittest.TestCase):
    def assert_interpolates(self, u_curves, v_curves, us, vs, S, rng):
        U, V, p, q, P = S
        for u, (kn, ctrl) in zip(us, v_curves):
            # the iso-curve at u and the input curve on the same knots: equal nets
            self.assertEqual(iso_curve_u(U, p, P, u), refine(kn, q, ctrl, V)[1])
            t = Fr(rng.randint(0, 1000), 1000)
            self.assertEqual(surface_point(U, V, p, q, P, u, t), curve_point(kn, q, ctrl, t))
        for v, (kn, ctrl) in zip(vs, u_curves):
            self.assertEqual(iso_curve_v(V, q, P, v), refine(kn, p, ctrl, U)[1])
            t = Fr(rng.randint(0, 1000), 1000)
            self.assertEqual(surface_point(U, V, p, q, P, t, v), curve_point(kn, p, ctrl, t))

    def test_example(self):
        net = example_network()
        S = gordon_surface(*net)
        U, V, p, q, P = S
        self.assertEqual((U, V, p, q), (H, H, 2, 2))
        heights = [[z for _, _, z in row] for row in P]
        self.assertEqual(heights, [[0, 0, 0, 0], [0, 3, 1, 0], [0, 1, -1, 0], [0, 0, 0, 0]])
        self.assertEqual(surface_point(*S, Fr(1, 2), Fr(1, 2)), (Fr(1, 2), Fr(1, 2), 1))
        self.assertEqual(surface_point(*S, Fr(1, 4), Fr(1, 4))[2], Fr(21, 16))
        S1, S2, T = gordon_parts(*net)
        z = [surface_point(*X, Fr(1, 4), Fr(1, 2))[2] for X in (S1, S2, T, S)]
        self.assertEqual(z, [Fr(3, 4), Fr(5, 4), Fr(3, 4), Fr(5, 4)])
        self.assert_interpolates(*net, S, random.Random(1))

    def test_random_networks_are_interpolated(self):
        rng = random.Random(7)
        for _ in range(12):
            p, q = rng.randint(1, 3), rng.randint(1, 3)
            n, m = p + rng.randint(0, 2), q + rng.randint(0, 2)
            net = random_network(rng, n + 1, m + 1, p, q)
            S = gordon_surface(*net)
            self.assert_interpolates(*net, S, rng)

    def test_net_sum_equals_boolean_sum(self):
        rng = random.Random(3)
        net = random_network(rng, 4, 3, 2, 2)
        S = gordon_surface(*net)
        S1, S2, T = gordon_parts(*net)
        for _ in range(10):
            u, v = Fr(rng.randint(0, 50), 50), Fr(rng.randint(0, 50), 50)
            boolean = sub(add(surface_point(*S1, u, v), surface_point(*S2, u, v)),
                          surface_point(*T, u, v))
            self.assertEqual(surface_point(*S, u, v), boolean)

    def test_lofts_alone_miss_the_other_family(self):
        u_curves, v_curves, us, vs = example_network()
        S1, _, _ = gordon_parts(u_curves, v_curves, us, vs)
        # S1 takes the v-curves, but at v = 1/2 it is not the bump u-curve
        kn, ctrl = u_curves[1]
        self.assertNotEqual(surface_point(*S1, Fr(1, 8), Fr(1, 2)),
                            curve_point(kn, 2, ctrl, Fr(1, 8)))

    def test_incompatible_network_is_rejected(self):
        u_curves, v_curves, us, vs = example_network()
        kn, ctrl = v_curves[1]
        moved = list(ctrl)
        moved[1] = (moved[1][0], moved[1][1], moved[1][2] + 1)
        bad = list(v_curves)
        bad[1] = (kn, moved)
        with self.assertRaises(ValueError):
            gordon_surface(u_curves, bad, us, vs)

    def test_too_few_curves_is_rejected(self):
        u_curves, v_curves, us, vs = example_network()
        with self.assertRaises(ValueError):
            gordon_surface(u_curves, v_curves[:2], us[:2], vs)


if __name__ == "__main__":
    unittest.main()
