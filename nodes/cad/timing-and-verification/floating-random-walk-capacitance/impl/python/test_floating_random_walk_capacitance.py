# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/floating-random-walk-capacitance/. The authors are listed in prov/0AP7M8.jsonl.
"""Tests for the floating random walk. The brute force is a finite
difference solution of the Laplace equation on a grid, whose discrete
energy is an upper bound on the capacitance. Monte Carlo checks use a fixed
seed and a tolerance of 4 standard errors computed from the samples."""

import math
import random
import unittest

import floating_random_walk_capacitance as F

S = 1 << 24  # grid points per length unit
Z = 4.0  # tolerance in standard errors


def kernel(x, y, u, terms=80):
    """Poisson kernel of [0, pi]^2 at (x, y) for the point (u, 0) of the bottom side."""
    return (2 / math.pi) * sum(
        math.sin(n * u) * math.sin(n * x) * math.sinh(n * (math.pi - y)) / math.sinh(n * math.pi)
        for n in range(1, terms))


def fd_energy(box, rects, volts, cells):
    """Brute force: 5-point successive over-relaxation with `cells` cells per
    unit. Returns the sum of squared differences over grid edges, which is
    2 W / eps for the discrete field and is never below the exact value."""
    X0, Y0, X1, Y1 = box
    nx, ny = (X1 - X0) * cells, (Y1 - Y0) * cells
    phi = [[None] * (ny + 1) for _ in range(nx + 1)]
    for i in range(nx + 1):
        for j in range(ny + 1):
            if i in (0, nx) or j in (0, ny):
                phi[i][j] = float(volts[0])
    for k, (x0, y0, x1, y1) in enumerate(rects, 1):
        for i in range((x0 - X0) * cells, (x1 - X0) * cells + 1):
            for j in range((y0 - Y0) * cells, (y1 - Y0) * cells + 1):
                phi[i][j] = float(volts[k])
    free = [(i, j) for i in range(nx + 1) for j in range(ny + 1) if phi[i][j] is None]
    for i, j in free:
        phi[i][j] = 0.0
    w = 2 / (1 + math.sin(math.pi / max(nx, ny)))
    for _ in range(100000):
        delta = 0.0
        for i, j in free:
            d = w * (0.25 * (phi[i - 1][j] + phi[i + 1][j] + phi[i][j - 1] + phi[i][j + 1]) - phi[i][j])
            phi[i][j] += d
            delta = max(delta, abs(d))
        if delta < 1e-10:
            break
    e = 0.0
    for i in range(nx + 1):
        for j in range(ny + 1):
            if i < nx:
                e += (phi[i + 1][j] - phi[i][j]) ** 2
            if j < ny:
                e += (phi[i][j + 1] - phi[i][j]) ** 2
    return e


def scaled(box, rects):
    return F.Geometry(tuple(c * S for c in box), [tuple(c * S for c in r) for r in rects])


def simpson(f, a, b, n=400):
    h = (b - a) / n
    s = f(a) + f(b) + sum((4 if i % 2 else 2) * f(a + i * h) for i in range(1, n))
    return s * h / 3


class TestKernel(unittest.TestCase):
    def test_density_matches_full_kernel(self):
        c = math.pi / 2
        for u in (0.1, 0.7, 1.3, 2.2, 3.0):
            self.assertAlmostEqual(F.density(u), kernel(c, c, u), places=12)

    def test_derivatives_match_finite_differences(self):
        c, d = math.pi / 2, 1e-5
        for u in (0.2, 1.0, 1.9, 2.8):
            dx = (kernel(c + d, c, u) - kernel(c - d, c, u)) / (2 * d)
            dy = (kernel(c, c + d, u) - kernel(c, c - d, u)) / (2 * d)
            self.assertAlmostEqual(F.tangent_derivative(u), dx, places=8)
            self.assertAlmostEqual(F.normal_derivative(u), -dy, places=8)

    def test_each_side_has_mass_one_quarter(self):
        self.assertAlmostEqual(F.side_cdf(math.pi), 1.0, places=12)
        self.assertAlmostEqual(simpson(F.density, 0, math.pi), 0.25, places=9)

    def test_mean_value_for_harmonic_polynomials(self):
        # Integrate phi against the kernel over the four sides of the square
        # [-1, 1]^2; it must give phi(0, 0), and the gradient weights must
        # give grad phi(0, 0).
        polys = [
            (lambda x, y: 1.0, (0.0, 0.0)),
            (lambda x, y: x + 2 * y + 3, (1.0, 2.0)),
            (lambda x, y: x * x - y * y + 0.5, (0.0, 0.0)),
            (lambda x, y: x * y + x, (1.0, 0.0)),
            (lambda x, y: x ** 3 - 3 * x * y * y + y, (0.0, 1.0)),
        ]
        h = 1.0
        for phi, grad in polys:
            for normal in ((1, 0), (0, 1), (-1, 0), (0, -1)):
                val = gx = 0.0
                for side, ((sx, sy), (tx, ty), _) in enumerate(F._SIDES):
                    def point(u):
                        off = 2 * h * u / math.pi
                        return sx * h + tx * off, sy * h + ty * off
                    val += simpson(lambda u: F.density(u) * phi(*point(u)), 0, math.pi)
                    gx += simpson(lambda u: F.density(u) * F.gradient_weight(h, side, u, normal) * phi(*point(u)),
                                  1e-9, math.pi - 1e-9)
                self.assertAlmostEqual(val, phi(0, 0), places=7)
                self.assertAlmostEqual(gx, grad[0] * normal[0] + grad[1] * normal[1], places=5)

    def test_sampler_follows_the_cdf(self):
        rng = random.Random(5)
        n = 20000
        xs = sorted(F.sample_side_position(rng) for _ in range(n))
        ks = max(abs((i + 1) / n - F.side_cdf(x)) for i, x in enumerate(xs))
        self.assertLess(ks, 1.63 / math.sqrt(n))  # 1 percent level of Kolmogorov-Smirnov


class TestWalk(unittest.TestCase):
    def test_conductor_outside_box_is_rejected(self):
        with self.assertRaises(ValueError):
            F.Geometry((0, 0, 10, 10), [(0, 2, 3, 4)])

    def test_nearest_is_the_linf_distance(self):
        g = F.Geometry((0, 0, 100, 60), [(10, 10, 20, 20), (50, 30, 70, 40)])
        rng = random.Random(7)
        for _ in range(500):
            p = (rng.randrange(1, 100), rng.randrange(1, 60))
            d, k = g.nearest(p)
            cand = [(min(p[0], 100 - p[0], p[1], 60 - p[1]), 0)]
            for i, r in enumerate(g.rects, 1):
                cand.append((max(r[0] - p[0], p[0] - r[2], r[1] - p[1], p[1] - r[3], 0), i))
            self.assertEqual(d, min(c[0] for c in cand))
            self.assertIn((d, k), cand)

    def test_jumps_stay_in_the_empty_square_boundary(self):
        g = scaled((-3, -3, 3, 3), [(-1, -1, 1, 1)])
        rng = random.Random(11)
        for _ in range(2000):
            p = (rng.randrange(-3 * S + 1, 3 * S), rng.randrange(-3 * S + 1, 3 * S))
            h, _ = g.nearest(p)
            if h == 0:
                continue
            q, _, _ = F.jump(p, h, rng)
            self.assertEqual(max(abs(q[0] - p[0]), abs(q[1] - p[1])), h)
            self.assertGreaterEqual(g.nearest(q)[0], 0)

    def test_every_walk_ends_on_a_conductor(self):
        g = scaled((-4, -3, 4, 3), [(-3, -1, -1, 1), (1, -1, 3, 1)])
        for v, k, q in F.walks(g, 1, S // 2, 2000, random.Random(13)):
            self.assertEqual(g.nearest(q), (0, k))

    def test_same_seed_same_result(self):
        g = scaled((-3, -3, 3, 3), [(-1, -1, 1, 1)])
        a = F.capacitance_row(g, 1, S, 300, random.Random(17))
        b = F.capacitance_row(g, 1, S, 300, random.Random(17))
        self.assertEqual(a, b)


class TestEstimates(unittest.TestCase):
    def test_flux_of_log_r_is_two_pi(self):
        # phi = log r is harmonic outside the origin, which lies inside the
        # conductor, so -flux(grad phi) = -2 pi exactly.
        g = scaled((-3, -3, 3, 3), [(-1, -1, 1, 1)])
        mu, se = F.flux_estimate(g, 1, S, 12000, random.Random(1),
                                 lambda k, p: math.log(math.hypot(p[0], p[1]) / S))
        self.assertLess(abs(mu + 2 * math.pi), Z * se)

    def test_flux_of_linear_field_is_zero(self):
        g = scaled((-3, -3, 3, 3), [(-1, -1, 1, 1)])
        mu, se = F.flux_estimate(g, 1, S, 12000, random.Random(3), lambda k, p: (p[0] + 2 * p[1]) / S)
        self.assertLess(abs(mu), Z * se)

    def test_square_coax_matches_finite_differences(self):
        box, rects = (-3, -3, 3, 3), [(-1, -1, 1, 1)]
        c_fd = fd_energy(box, rects, [0, 1], 8)
        c_fd_fine_gap = c_fd - fd_energy(box, rects, [0, 1], 4)  # negative, about 3 times the bias
        row = F.capacitance_row(scaled(box, rects), 1, S // 2, 25000, random.Random(2))
        (c10, se0), (c11, se1) = row
        self.assertLess(abs(c11 - c_fd), Z * se1 + abs(c_fd_fine_gap))
        self.assertLess(abs(c10 + c_fd), Z * se0 + abs(c_fd_fine_gap))

    def test_two_conductors_reciprocity_and_brute_force(self):
        box, rects = (-4, -3, 4, 3), [(-3, -1, -1, 1), (1, -1, 3, 1)]
        e1 = fd_energy(box, rects, [0, 1, 0], 4)
        e2 = fd_energy(box, rects, [0, 0, 1], 4)
        e12 = fd_energy(box, rects, [0, 1, 1], 4)
        c12_fd = (e12 - e1 - e2) / 2
        g = scaled(box, rects)
        r1 = F.capacitance_row(g, 1, S // 2, 15000, random.Random(19))
        r2 = F.capacitance_row(g, 2, S // 2, 15000, random.Random(23))
        self.assertLess(r1[2][0], 0)  # coupling coefficients are negative
        self.assertLess(abs(r1[2][0] - r2[1][0]), Z * math.hypot(r1[2][1], r2[1][1]))
        self.assertLess(abs(r1[2][0] - c12_fd), Z * r1[2][1] + 0.05 * abs(c12_fd))
        self.assertLess(abs(r1[1][0] - e1), Z * r1[1][1] + 0.05 * e1)


if __name__ == "__main__":
    unittest.main()
