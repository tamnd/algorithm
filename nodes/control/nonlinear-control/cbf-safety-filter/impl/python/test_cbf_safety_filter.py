# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cbf-safety-filter/. The authors are listed in prov/3VWCBR.jsonl.

"""Tests for cbf_safety_filter.py. Standard library only, fixed seeds."""

import itertools
import math
import random
import unittest
from fractions import Fraction as Fr

from cbf_safety_filter import INFEASIBLE, cbf_filter, cbf_qp, clip
from ctlsim import simulate


def dot(a, b):
    return sum((x * y for x, y in zip(a, b)), 0)


def brute_force(u_nom, a, b, lo, hi):
    """Solve the QP by trying every active set. Exact with Fractions.

    Each coordinate is at its lower bound, at its upper bound or free, and
    the barrier constraint is active or not. For each choice the stationary
    point is unique; the answer is the feasible one with the least cost.
    """
    m = len(u_nom)
    best = None
    states = []
    for j in range(m):
        s = ["free"]
        if lo[j] is not None:
            s.append("lo")
        if hi[j] is not None:
            s.append("hi")
        states.append(s)
    for choice in itertools.product(*states):
        fixed = {}
        for j, s in enumerate(choice):
            if s == "lo":
                fixed[j] = lo[j]
            elif s == "hi":
                fixed[j] = hi[j]
        free = [j for j in range(m) if j not in fixed]
        cands = []
        u = [fixed.get(j, u_nom[j]) for j in range(m)]
        cands.append(u)
        nf = sum((a[j] * a[j] for j in free), 0)
        if nf != 0:
            lam = -(dot(a, u) + b) / Fr(nf)
            cands.append([u[j] + lam * a[j] if j in free else u[j] for j in range(m)])
        for u in cands:
            ok = dot(a, u) + b >= 0 and all(
                (lo[j] is None or u[j] >= lo[j]) and (hi[j] is None or u[j] <= hi[j])
                for j in range(m))
            if ok:
                cost = sum(((x - y) ** 2 for x, y in zip(u, u_nom)), 0)
                if best is None or cost < best[0]:
                    best = (cost, u)
    return None if best is None else best[1]


def random_instance(rng, m):
    def r():
        return Fr(rng.randint(-8, 8), rng.randint(1, 3))
    u_nom = [r() for _ in range(m)]
    a = [r() if rng.random() < 0.85 else Fr(0) for _ in range(m)]
    b = r()
    lo, hi = [], []
    for _ in range(m):
        x, y = sorted([r(), r()])
        lo.append(x if rng.random() < 0.7 else None)
        hi.append(y if rng.random() < 0.7 else None)
    return u_nom, a, b, lo, hi


class TestQP(unittest.TestCase):
    def test_against_brute_force(self):
        rng = random.Random(3)
        n_inf = n_act = 0
        for m in (1, 2, 3, 4):
            for _ in range(150):
                u_nom, a, b, lo, hi = random_instance(rng, m)
                u, lam = cbf_qp(u_nom, a, b, lo, hi)
                ref = brute_force(u_nom, a, b, lo, hi)
                self.assertEqual(u, ref)
                if u is INFEASIBLE:
                    n_inf += 1
                    continue
                # KKT: lam >= 0, u = clip(u_nom + lam a), complementary slackness.
                self.assertGreaterEqual(lam, 0)
                self.assertEqual(u, clip([x + lam * y for x, y in zip(u_nom, a)], lo, hi))
                self.assertEqual(lam * (dot(a, u) + b), 0)
                if lam > 0:
                    n_act += 1
        self.assertGreater(n_inf, 10)
        self.assertGreater(n_act, 100)

    def test_no_box_closed_form(self):
        rng = random.Random(4)
        for _ in range(50):
            m = rng.randint(1, 4)
            u_nom = [Fr(rng.randint(-9, 9), 2) for _ in range(m)]
            a = [Fr(rng.randint(1, 9), rng.randint(1, 3)) * rng.choice((-1, 1)) for _ in range(m)]
            b = Fr(rng.randint(-20, 20), 3)
            u, _ = cbf_qp(u_nom, a, b)
            psi = dot(a, u_nom) + b
            want = list(u_nom) if psi >= 0 else [x - psi * y / dot(a, a) for x, y in zip(u_nom, a)]
            self.assertEqual(u, want)

    def test_integer_inputs_stay_exact(self):
        u, lam = cbf_qp([1, 1], [-1, -2], 0)
        # psi(0) = -3 and |a|^2 = 5, so lam = 3/5 and u = (1, 1) + lam a.
        self.assertEqual(u, [Fr(2, 5), Fr(-1, 5)])
        self.assertEqual(lam, Fr(3, 5))
        self.assertIsInstance(u[0], Fr)

    def test_infeasible_example(self):
        # x' = x + u, |u| <= 1, h = 2 - x, alpha(h) = h: a = -1, b = 2 - 2x.
        def solve(x):
            return cbf_qp([Fr(0)], [Fr(-1)], 2 - 2 * x, [Fr(-1)], [Fr(1)])[0]
        self.assertEqual(solve(Fr(3, 2)), [-1])
        self.assertIs(solve(Fr(8, 5)), INFEASIBLE)
        self.assertEqual(solve(Fr(1)), [0])


class TestClosedLoop(unittest.TestCase):
    def test_one_dimension(self):
        # x' = u, h = 1 - x, alpha(h) = h, u_nom = 1: the filter gives
        # u = 1 - x, so x(t) = 1 - e^(-t). RK4, dt = 0.01.
        ctl = cbf_filter(lambda x: [0.0], lambda x: [[1.0]], lambda x: 1 - x[0],
                         lambda x: [-1.0], lambda s: s, lambda t, x: [1.0])
        ts, xs, _ = simulate(lambda t, x, u: ctl(t, x), [0.0], 0.0, 5.0, 0.01)
        err = max(abs(x[0] - (1 - math.exp(-t))) for t, x in zip(ts, xs))
        self.assertLess(err, 1e-8)

    def test_obstacle(self):
        # Single integrator in the plane, disk of radius 1 at (2, 0),
        # h = |x - (2, 0)|^2 - 1, alpha(h) = h, u_nom = (4, 0) - x.
        h = lambda x: (x[0] - 2) ** 2 + x[1] ** 2 - 1  # noqa: E731
        ctl = cbf_filter(lambda x: [0.0, 0.0], lambda x: [[1.0, 0.0], [0.0, 1.0]], h,
                         lambda x: [2 * (x[0] - 2), 2 * x[1]], lambda s: s,
                         lambda t, x: [4 - x[0], -x[1]])
        ts, xs, _ = simulate(lambda t, x, u: ctl(t, x), [0.0, 0.2], 0.0, 12.0, 0.01)
        hs = [h(x) for x in xs]
        self.assertGreater(min(hs), 0.25)
        self.assertLess(min(hs), 0.2501)
        self.assertLess(math.hypot(xs[-1][0] - 4, xs[-1][1]), 1e-3)
        k = round(2.0 / 0.01)
        self.assertAlmostEqual(xs[k][0], 1.68245, places=4)
        self.assertAlmostEqual(xs[k][1], 1.14481, places=4)

    def test_sampled_data_violation(self):
        # With the input held for 0.15 and alpha(h) = 10 h, near the boundary
        # 1 - x_(k+1) = -0.5 (1 - x_k), so h changes sign (the pitfall).
        def run(gamma, hold):
            ctl = cbf_filter(lambda x: [0.0], lambda x: [[1.0]], lambda x: 1 - x[0],
                             lambda x: [-1.0], lambda s: gamma * s, lambda t, x: [1.0])
            self.assertEqual(round(hold / 0.01) * 0.01, hold)
            _, xs, _ = simulate(lambda t, x, u: [u[0]], [0.0], 0.0, 3.0, 0.01,
                                control=ctl, hold=hold)
            return min(1 - x[0] for x in xs)
        self.assertAlmostEqual(run(10.0, 0.15), -0.05, places=9)
        self.assertGreaterEqual(run(10.0, 0.05), 0.0)
        self.assertGreater(run(1.0, 0.15), 0.0)


if __name__ == "__main__":
    unittest.main()
