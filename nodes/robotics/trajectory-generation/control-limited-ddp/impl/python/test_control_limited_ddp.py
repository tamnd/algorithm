# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/control-limited-ddp/. The authors are listed in prov/DH08X0.jsonl.
import itertools
import math
import random
import unittest

from control_limited_ddp import (
    Problem,
    backward,
    box_qp,
    control_limited_ddp,
    double_integrator,
    matvec,
    pendulum,
    qp_value,
    transpose,
    vadd,
)


def gradient(prob, us):
    """dJ/du_k for every k, by the adjoint recursion."""
    xs = prob.rollout(us)
    lam = matvec(prob.qf, vadd(xs[-1], prob.goal, -1.0))
    grads = [None] * len(us)
    for k in reversed(range(len(us))):
        _, a, b = prob.dyn(xs[k], us[k])
        grads[k] = vadd(matvec(prob.r, us[k]), matvec(transpose(b), lam))
        lam = vadd(matvec(prob.q, vadd(xs[k], prob.goal, -1.0)), matvec(transpose(a), lam))
    return grads


def flat(us):
    return [v for u in us for v in u]


def unflat(v, m):
    return [v[i:i + m] for i in range(0, len(v), m)]


def solve(a, b):
    """Gaussian elimination with partial pivoting."""
    n = len(b)
    m = [row[:] + [b[i]] for i, row in enumerate(a)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(m[r][c]))
        m[c], m[p] = m[p], m[c]
        for r in range(c + 1, n):
            f = m[r][c] / m[c][c]
            for j in range(c, n + 1):
                m[r][j] -= f * m[c][j]
    x = [0.0] * n
    for i in reversed(range(n)):
        x[i] = (m[i][n] - sum(m[i][j] * x[j] for j in range(i + 1, n))) / m[i][i]
    return x


def hessian_and_gradient(prob, n_steps, m):
    """For linear dynamics J is quadratic in U; columns of the Hessian are gradient differences."""
    zero = [[0.0] * m for _ in range(n_steps)]
    g0 = flat(gradient(prob, zero))
    h = []
    for j in range(n_steps * m):
        e = [0.0] * (n_steps * m)
        e[j] = 1.0
        h.append(vadd(flat(gradient(prob, unflat(e, m))), g0, -1.0))
    return transpose(h), g0


def kkt_residual(prob, us):
    """Largest violation of the first-order conditions of min J subject to the box."""
    worst = 0.0
    for u, g in zip(us, gradient(prob, us)):
        for i in range(len(u)):
            if u[i] <= prob.lo[i]:
                worst = max(worst, -g[i])
            elif u[i] >= prob.hi[i]:
                worst = max(worst, g[i])
            else:
                worst = max(worst, abs(g[i]))
    return worst


def random_linear(rng, n, m):
    a = [[(1.0 if i == j else 0.0) + rng.uniform(-0.2, 0.2) for j in range(n)] for i in range(n)]
    b = [[rng.uniform(-0.5, 0.5) for _ in range(m)] for _ in range(n)]

    def dyn(x, u):
        return vadd(matvec(a, x), matvec(b, u)), a, b
    return dyn


def diag(vals):
    return [[v if i == j else 0.0 for j in range(len(vals))] for i, v in enumerate(vals)]


class TestWorkedExample(unittest.TestCase):
    def test_pendulum_swing_up(self):
        dt, umax = 0.05, 3.0
        prob = Problem(pendulum(dt), [0.0, 0.0], [math.pi, 0.0], diag([0.0, 0.0]), [[0.1 * dt]],
                       diag([100.0, 10.0]), [-umax], [umax])
        xs, us, info = control_limited_ddp(prob, [[0.0]] * 80, iters=300)
        costs = info["costs"]
        self.assertAlmostEqual(costs[0], 493.4802, places=3)
        self.assertAlmostEqual(costs[1], 142.2482, places=3)
        self.assertAlmostEqual(costs[-1], 0.854863, places=5)
        self.assertEqual(info["iterations"], 60)
        self.assertTrue(all(costs[i + 1] < costs[i] for i in range(len(costs) - 1)))
        self.assertTrue(all(-umax <= u[0] <= umax for u in us))
        self.assertEqual(sum(1 for u in us if abs(u[0]) == umax), 19)
        self.assertLess(abs(xs[-1][0] - math.pi), 0.01)
        self.assertLess(abs(xs[-1][1]), 0.02)
        self.assertLess(kkt_residual(prob, us), 1e-4)


class TestExactCases(unittest.TestCase):
    def test_unconstrained_linear_quadratic_in_one_iteration(self):
        rng = random.Random(2014)
        n, m, steps = 3, 2, 10
        prob = Problem(random_linear(rng, n, m), [1.0, -0.5, 0.3], [0.0] * n, diag([1.0, 0.5, 0.2]),
                       diag([0.3, 0.1]), diag([5.0, 5.0, 5.0]), [-1e6] * m, [1e6] * m)
        h, g = hessian_and_gradient(prob, steps, m)
        best = unflat(solve(h, [-v for v in g]), m)
        _, us, info = control_limited_ddp(prob, [[0.0] * m] * steps, iters=1)
        self.assertEqual(info["iterations"], 1)
        for u, v in zip(us, best):
            for a, b in zip(u, v):
                self.assertAlmostEqual(a, b, places=8)
        # A second backward pass finds nothing left to do.
        _, _, dv1, dv2 = backward(prob, prob.rollout(us), us, 0.0)
        self.assertLess(abs(dv1 + dv2), 1e-12)

    def test_box_qp_against_all_active_sets(self):
        rng = random.Random(11)
        for _ in range(200):
            m = rng.randint(1, 3)
            p = [[rng.uniform(-1, 1) for _ in range(m)] for _ in range(m)]
            h = [[sum(p[k][i] * p[k][j] for k in range(m)) + (0.1 if i == j else 0.0) for j in range(m)] for i in range(m)]
            g = [rng.uniform(-3, 3) for _ in range(m)]
            lo = [rng.uniform(-2, 0) for _ in range(m)]
            hi = [rng.uniform(0, 2) for _ in range(m)]
            best = math.inf
            for pattern in itertools.product((0, 1, 2), repeat=m):
                x = [lo[i] if pattern[i] == 0 else hi[i] if pattern[i] == 2 else 0.0 for i in range(m)]
                free = [i for i in range(m) if pattern[i] == 1]
                if free:
                    rhs = [-(g[i] + sum(h[i][j] * x[j] for j in range(m) if j not in free)) for i in free]
                    sol = solve([[h[i][j] for j in free] for i in free], rhs)
                    for a, i in enumerate(free):
                        x[i] = sol[a]
                if all(lo[i] - 1e-12 <= x[i] <= hi[i] + 1e-12 for i in range(m)):
                    best = min(best, qp_value(h, g, x))
            x, _ = box_qp(h, g, lo, hi)
            self.assertTrue(all(lo[i] <= x[i] <= hi[i] for i in range(m)))
            self.assertAlmostEqual(qp_value(h, g, x), best, places=9)


class TestConstrainedLinear(unittest.TestCase):
    def check(self, prob, steps, m):
        h, g = hessian_and_gradient(prob, steps, m)
        # Accelerated projected gradient on the same convex problem, as an independent reference.
        lip = max(sum(abs(v) for v in row) for row in h)
        lo, hi = prob.lo * steps, prob.hi * steps
        x = [0.0] * (steps * m)
        y, t = x[:], 1.0
        for _ in range(1200):
            grad = vadd(matvec(h, y), g)
            xn = [min(max(y[i] - grad[i] / lip, lo[i]), hi[i]) for i in range(len(y))]
            tn = (1 + math.sqrt(1 + 4 * t * t)) / 2
            y = [xn[i] + (t - 1) / tn * (xn[i] - x[i]) for i in range(len(y))]
            x, t = xn, tn
        _, us, info = control_limited_ddp(prob, [[0.0] * m] * steps, iters=100)
        self.assertLess(kkt_residual(prob, us), 1e-6)
        costs = info["costs"]
        self.assertTrue(all(costs[i + 1] < costs[i] for i in range(len(costs) - 1)))
        self.assertAlmostEqual(costs[-1], qp_value(h, g, x) + costs[0], places=6)
        return us

    def test_double_integrator_with_a_small_box(self):
        prob = Problem(double_integrator(0.1), [1.0, 0.0], [0.0, 0.0], diag([0.1, 0.01]), [[0.01]],
                       diag([10.0, 10.0]), [-0.5], [0.5])
        us = self.check(prob, 30, 1)
        self.assertGreater(sum(1 for u in us if abs(u[0]) == 0.5), 5)

    def test_random_linear_systems(self):
        rng = random.Random(1966)
        for _ in range(2):
            n, m, steps = 2, 2, 10
            prob = Problem(random_linear(rng, n, m), [rng.uniform(-2, 2) for _ in range(n)], [0.0] * n,
                           diag([1.0, 1.0]), diag([0.1, 0.1]), diag([10.0, 10.0]), [-0.4, -0.4], [0.4, 0.4])
            self.check(prob, steps, m)


if __name__ == "__main__":
    unittest.main()
