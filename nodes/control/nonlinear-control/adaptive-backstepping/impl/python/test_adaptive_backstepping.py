# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/adaptive-backstepping/. The authors are listed in prov/5JZM0E.jsonl.

"""Tests for adaptive_backstepping.py. Standard library only, fixed seeds."""

import random
import unittest
from fractions import Fraction as Fr

from adaptive_backstepping import (
    Dual,
    adaptive_backstepping,
    closed_loop,
    eps_part,
    new_tag,
    real_part,
    stages,
)
from ctlsim import simulate

# The page example: x1' = x2 + theta x1^2, x2' = u, theta = 1 unknown.
PHI = [lambda x: [x[0] ** 2], lambda x: [0]]
BETA = lambda x: 1  # noqa: E731
C = [1, 1]
GAMMA = [[1]]


def example_u(x1, x2, th, c1=1, c2=1, g=1):
    """The controller of the example, written out by hand."""
    z1 = x1
    z2 = x2 + c1 * x1 + th * x1 ** 2
    w2 = (c1 + 2 * th * x1) * x1 ** 2
    tau2 = x1 ** 3 + w2 * z2
    u = -z1 - c2 * z2 - w2 * th + (-c1 - 2 * th * x1) * x2 - x1 ** 2 * g * tau2
    return u, g * tau2


def vdot_check(phi, beta, c, G, Ginv, theta, x, th):
    """Return (V', -sum c_i z_i^2) at (x, th) along the closed loop.

    V' is computed from one extra dual direction along the vector field,
    so it uses the chain rule only, not the error equations of the proof.
    """
    n, p = len(phi), len(th)
    F = closed_loop(phi, beta, c, G, theta)
    d = F(0, list(x) + list(th))
    t = new_tag()
    xd = [Dual(t, x[i], d[i]) for i in range(n)]
    thd = [Dual(t, th[l], d[n + l]) for l in range(p)]
    _, Z, _, _ = stages(phi, c, G, n, xd, thd)
    zs = [real_part(z, t) for z in Z]
    zd = [eps_part(z, t) for z in Z]
    err = [theta[l] - th[l] for l in range(p)]
    th_dot = d[n:]
    # V = |z|^2 / 2 + err^T Ginv err / 2, and err' = -th_dot.
    vd = sum(a * b for a, b in zip(zs, zd))
    vd -= sum(err[r] * Ginv[r][s] * th_dot[s] for r in range(p) for s in range(p))
    return vd, -sum(ci * z * z for ci, z in zip(c, zs))


def random_poly(rng, k):
    """A random polynomial in x_1..x_k of degree at most 2, integer terms."""
    terms = [(rng.randint(-2, 2), rng.randrange(k), rng.randrange(k + 1)) for _ in range(2)]

    def h(x):
        s = 0
        for a, i, j in terms:
            s = s + a * x[i] * (x[j] if j < k else 1)
        return s
    return h


class TestExample(unittest.TestCase):
    def test_initial_values(self):
        u, th_dot, z = adaptive_backstepping(PHI, BETA, C, GAMMA, [Fr(1), Fr(0)], [Fr(0)])
        self.assertEqual(u, -4)
        self.assertEqual(th_dot, [2])
        self.assertEqual(z, [1, 1])

    def test_closed_form(self):
        rng = random.Random(1)
        for _ in range(20):
            x1, x2, th = (Fr(rng.randint(-9, 9), rng.randint(1, 5)) for _ in range(3))
            c1, c2, g = (Fr(rng.randint(1, 6), rng.randint(1, 3)) for _ in range(3))
            u, th_dot, _ = adaptive_backstepping(PHI, BETA, [c1, c2], [[g]], [x1, x2], [th])
            self.assertEqual((u, th_dot[0]), example_u(x1, x2, th, c1, c2, g))

    def test_scalar_case(self):
        # n = 1: x' = beta u + phi^T theta gives u = (-c z - phi^T th) / beta
        # and th' = Gamma phi z.
        phi = [lambda x: [x[0] ** 2, x[0]]]
        beta = lambda x: 2 + x[0] ** 2  # noqa: E731
        x, th = [Fr(3, 2)], [Fr(1, 3), Fr(-2)]
        G = [[2, 1], [1, 1]]
        u, th_dot, z = adaptive_backstepping(phi, beta, [Fr(5)], G, x, th)
        ph = [Fr(9, 4), Fr(3, 2)]
        self.assertEqual(z, [Fr(3, 2)])
        self.assertEqual(u, (-5 * x[0] - ph[0] * th[0] - ph[1] * th[1]) / beta(x))
        self.assertEqual(th_dot, [(2 * ph[0] + ph[1]) * x[0], (ph[0] + ph[1]) * x[0]])


class TestLyapunovIdentity(unittest.TestCase):
    def test_example(self):
        vd, rhs = vdot_check(PHI, BETA, C, GAMMA, [[1]], [1], [Fr(1), Fr(0)], [Fr(0)])
        self.assertEqual(vd, rhs)
        self.assertEqual(vd, -2)

    def test_random_systems(self):
        # Exact V' = -sum c_i z_i^2 on random systems with n = 1..3 and
        # p = 1..2, a non-diagonal Gamma and a state-dependent beta.
        rng = random.Random(7)
        G = [[2, 1], [1, 1]]
        Ginv = [[1, -1], [-1, 2]]
        count = 0
        for n in (1, 2, 3):
            for p in (1, 2):
                for _ in range(4):
                    phi = []
                    for i in range(n):
                        polys = [random_poly(rng, i + 1) for _ in range(p)]
                        phi.append(lambda x, polys=polys: [h(x) for h in polys])
                    beta = lambda x: 1 + x[0] ** 2  # noqa: E731
                    c = [Fr(rng.randint(1, 4), rng.randint(1, 2)) for _ in range(n)]
                    Gp = [row[:p] for row in G[:p]]
                    Gi = Ginv if p == 2 else [[Fr(1, 2)]]
                    theta = [Fr(rng.randint(-3, 3), 2) for _ in range(p)]
                    x = [Fr(rng.randint(-6, 6), rng.randint(1, 3)) for _ in range(n)]
                    th = [Fr(rng.randint(-6, 6), 3) for _ in range(p)]
                    vd, rhs = vdot_check(phi, beta, c, Gp, Gi, theta, x, th)
                    self.assertEqual(vd, rhs)
                    count += 1
        self.assertEqual(count, 24)


class TestSimulation(unittest.TestCase):
    def test_example_run(self):
        # RK4, dt = 0.01, T = 10. Theorem: V is nonincreasing and z -> 0.
        # The estimate need not reach theta = 1.
        F = closed_loop(PHI, BETA, C, GAMMA, [1])
        ts, xs, _ = simulate(F, [1.0, 0.0, 0.0], 0.0, 10.0, 0.01)
        V = []
        for s in xs:
            _, _, z = adaptive_backstepping(PHI, BETA, C, GAMMA, s[:2], s[2:])
            V.append((z[0] ** 2 + z[1] ** 2 + (1 - s[2]) ** 2) / 2)
        self.assertAlmostEqual(V[0], 1.5)
        for k in range(len(V) - 1):
            self.assertLessEqual(V[k + 1], V[k] + 1e-9)
        x1, x2, th = xs[-1]
        self.assertLess(abs(x1) + abs(x2), 1e-3)
        self.assertAlmostEqual(th, 1.63173, places=4)
        self.assertGreater(abs(th - 1), 0.5)
        self.assertAlmostEqual(V[-1], (1 - th) ** 2 / 2, places=6)
        # The page table, t = 1.
        k = round(1.0 / 0.01)
        self.assertAlmostEqual(xs[k][0], 0.32603, places=4)
        self.assertAlmostEqual(xs[k][1], -0.98258, places=4)
        self.assertAlmostEqual(xs[k][2], 1.64337, places=4)


if __name__ == "__main__":
    unittest.main()
