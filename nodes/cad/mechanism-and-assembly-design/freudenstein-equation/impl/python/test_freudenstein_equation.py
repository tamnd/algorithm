# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/freudenstein-equation/. The authors are listed in prov/Z9SNZM.jsonl.

import math
import random
import unittest
from fractions import Fraction

from freudenstein_equation import (
    function_generator,
    rational_unit,
    solve_linear,
    three_point_synthesis,
    unit_point,
)


def det3(m):
    return (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
            - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
            + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))


def cramer3(m, r):
    """Oracle: Cramer's rule for a 3 x 3 system."""
    dm = det3(m)
    if dm == 0:
        return None
    out = []
    for k in range(3):
        mk = [row[:k] + [r[i]] + row[k + 1:] for i, row in enumerate(m)]
        out.append(det3(mk) / dm)
    return out


def circle_points(a, b, c, d, phi):
    """Oracle for positions: the points B at distance |b| from A and |c| from O4 = (d, 0)."""
    ax, ay = a * math.cos(phi), a * math.sin(phi)
    dx, dy = d - ax, -ay
    dist = math.hypot(dx, dy)
    rb, rc = abs(b), abs(c)
    if dist == 0 or dist > rb + rc or dist < abs(rb - rc):
        return []
    along = (rb * rb - rc * rc + dist * dist) / (2 * dist)
    h = math.sqrt(max(rb * rb - along * along, 0.0))
    mx, my = ax + along * dx / dist, ay + along * dy / dist
    return [(mx - h * dy / dist, my + h * dx / dist), (mx + h * dy / dist, my - h * dx / dist)]


def random_rational(rng, lo=-3, hi=3):
    return Fraction(rng.randint(lo * 6, hi * 6), rng.randint(1, 6))


class TestLinearSolver(unittest.TestCase):
    def test_against_cramer(self):
        rng = random.Random(1955)
        singular = 0
        for _ in range(600):
            m = [[Fraction(rng.randint(-3, 3)) for _ in range(3)] for _ in range(3)]
            r = [Fraction(rng.randint(-5, 5)) for _ in range(3)]
            want = cramer3(m, r)
            got = solve_linear(m, r)
            self.assertEqual(got, want)
            singular += want is None
        self.assertGreater(singular, 10)


class TestThreePointExact(unittest.TestCase):
    def test_worked_example(self):
        # phi: t = 1/3, 1/2, 1 (36.87, 53.13, 90 degrees); psi: t = 1/2, 2/3, 3/2 (53.13, 67.38, 112.62 degrees)
        pts = [rational_unit(p) + rational_unit(q)
               for p, q in zip((Fraction(1, 3), Fraction(1, 2), 1), (Fraction(1, 2), Fraction(2, 3), Fraction(3, 2)))]
        a, b2, c, k = three_point_synthesis(pts, Fraction(9))
        self.assertEqual(k, (Fraction(3, 5), Fraction(9, 13), Fraction(15, 13)))
        self.assertEqual((a, b2, c), (15, 25, 13))
        pins = []
        for cphi, sphi, cpsi, spsi in pts:
            pa = (a * cphi, a * sphi)
            pb = (9 + c * cpsi, c * spsi)
            self.assertEqual((pb[0] - pa[0]) ** 2 + (pb[1] - pa[1]) ** 2, 25)
            pins.append((pa, pb))
        self.assertEqual(pins[0], ((12, 9), (Fraction(84, 5), Fraction(52, 5))))
        self.assertEqual(pins[1], ((9, 12), (14, 12)))
        self.assertEqual(pins[2], ((0, 15), (4, 12)))

    def test_random_exact_points(self):
        rng = random.Random(1878)
        checked = 0
        for _ in range(700):
            ts = [random_rational(rng) for _ in range(6)]
            pts = [rational_unit(ts[j]) + rational_unit(ts[j + 3]) for j in range(3)]
            d = Fraction(rng.randint(1, 20), rng.randint(1, 5))
            res = three_point_synthesis(pts, d)
            if res is None:
                continue
            a, b2, c, (k1, k2, k3) = res
            for cphi, sphi, cpsi, spsi in pts:
                # the equation holds exactly
                self.assertEqual(k1 * cpsi - k2 * cphi + k3, cphi * cpsi + sphi * spsi)
                # and the loop closes exactly: |B - A|^2 = b^2 with signed lengths a and c
                pa = (a * cphi, a * sphi)
                pb = (d + c * cpsi, c * spsi)
                self.assertEqual((pb[0] - pa[0]) ** 2 + (pb[1] - pa[1]) ** 2, b2)
            checked += 1
        self.assertGreater(checked, 500)

    def test_repeated_point_is_singular(self):
        p = rational_unit(Fraction(1, 2)) + rational_unit(Fraction(1, 3))
        q = rational_unit(1) + rational_unit(2)
        self.assertIsNone(three_point_synthesis([p, p, q], Fraction(1)))


class TestThreePointFloat(unittest.TestCase):
    def test_linkage_passes_the_points(self):
        rng = random.Random(77)
        checked = 0
        for _ in range(800):
            phis = [rng.uniform(0, 2 * math.pi) for _ in range(3)]
            psis = [rng.uniform(0, 2 * math.pi) for _ in range(3)]
            d = rng.uniform(0.5, 5.0)
            res = three_point_synthesis([unit_point(p, q) for p, q in zip(phis, psis)], d)
            if res is None:
                continue
            a, b2, c, _ = res
            if b2 <= 0 or max(abs(a), abs(c), b2) > 1e4:
                continue
            b = math.sqrt(b2)
            scale = abs(a) + b + abs(c) + d
            for phi, psi in zip(phis, psis):
                want = (d + c * math.cos(psi), c * math.sin(psi))
                pts = circle_points(a, b, c, d, phi)
                self.assertTrue(pts, (a, b, c, d, phi))
                gap = min(math.hypot(x - want[0], y - want[1]) for x, y in pts)
                self.assertLess(gap, 1e-6 * scale)
            checked += 1
        self.assertGreater(checked, 500)

    def test_log_function_generator(self):
        f, x0, x1 = math.log10, 1.0, 2.0
        phi0, dphi, psi0, dpsi = map(math.radians, (90, 60, 15, 60))
        cheb = [1.5 - 0.5 * math.cos((2 * j - 1) * math.pi / 6) for j in (1, 2, 3)]
        errors = {}
        for name, xs in (("chebyshev", cheb), ("equal", [1.25, 1.5, 1.75])):
            a, b2, c, _ = function_generator(f, x0, x1, xs, phi0, dphi, psi0, dpsi, 1.0)
            b = math.sqrt(b2)
            if name == "chebyshev":
                self.assertAlmostEqual(a, 0.97149, places=4)
                self.assertAlmostEqual(b, 2.25042, places=4)
                self.assertAlmostEqual(c, 1.19026, places=4)
            # follow the output pin B continuously from the first precision point
            x_start = xs[0]
            phi = phi0 + dphi * (x_start - x0)
            psi = psi0 + dpsi * (f(x_start) - f(x0)) / (f(x1) - f(x0))
            last = (1.0 + c * math.cos(psi), c * math.sin(psi))
            worst = 0.0
            grid = sorted(set([x0 + i * (x1 - x0) / 2000 for i in range(2001)] + xs))
            k0 = grid.index(x_start)
            for path in (grid[k0:], grid[k0::-1]):
                pin = last
                for x in path:
                    phi = phi0 + dphi * (x - x0)
                    pts = circle_points(a, b, c, 1.0, phi)
                    self.assertTrue(pts)
                    pin = min(pts, key=lambda p: math.hypot(p[0] - pin[0], p[1] - pin[1]))
                    got = math.atan2(pin[1], pin[0] - 1.0)
                    ideal = psi0 + dpsi * (f(x) - f(x0)) / (f(x1) - f(x0))
                    err = abs(math.remainder(got - ideal, 2 * math.pi))
                    if any(abs(x - p) < 1e-12 for p in xs):
                        self.assertLess(err, 1e-9)
                    worst = max(worst, err)
            errors[name] = math.degrees(worst)
        self.assertAlmostEqual(errors["chebyshev"], 0.0608, places=3)
        self.assertAlmostEqual(errors["equal"], 0.1670, places=3)


if __name__ == "__main__":
    unittest.main()
