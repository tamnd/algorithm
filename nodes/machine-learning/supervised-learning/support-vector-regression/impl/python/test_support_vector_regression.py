# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/support-vector-regression/. The authors are listed in prov/9APN7H.jsonl.

import math
import random

from support_vector_regression import SVR, eps_insensitive, gaussian_kernel, linear_kernel


def sine_data(seed, n, noise):
    rng = random.Random(seed)
    xs = [(rng.uniform(-3, 3),) for _ in range(n)]
    ys = [math.sin(x[0]) + rng.gauss(0, noise) for x in xs]
    return xs, ys


def test_page_example() -> None:
    xs, ys = [(0.0,), (1.0,), (2.0,)], [0.0, 1.0, 2.0]
    m = SVR(linear_kernel, 10.0, 0.5).fit(xs, ys)
    # One WSS3 step: the pair (a_3, a*_1) moves by d = 1/4.
    assert m.iterations == 1
    assert m.a == [0.0, 0.0, 0.25] and m.a_star == [0.25, 0.0, 0.0]
    assert m.b == 0.5 and m.fitted() == [0.5, 1.0, 1.5]  # f(x) = x/2 + 1/2
    assert abs(m.primal_objective() - 0.125) < 1e-15 and abs(m.dual_objective() - 0.125) < 1e-15
    # With C = 0.1 both multipliers hit C, the slope is 0.2, and b is any
    # value in [0.5, 1.1]; the solver takes the middle.
    m = SVR(linear_kernel, 0.1, 0.5).fit(xs, ys)
    assert m.theta == [-0.1, 0.0, 0.1]
    assert abs(m.b - 0.8) < 1e-12
    assert abs(m.primal_objective() - 0.08) < 1e-12 and abs(m.dual_objective() - 0.08) < 1e-12


def test_eps_insensitive_loss() -> None:
    assert eps_insensitive(0.3, 0.5) == 0.0
    assert eps_insensitive(-0.5, 0.5) == 0.0
    assert eps_insensitive(0.75, 0.5) == 0.25
    assert eps_insensitive(-2.0, 0.5) == 1.5


def test_kkt_conditions_and_zero_duality_gap() -> None:
    for seed in range(3):
        xs, ys = sine_data(seed, 30, 0.1)
        for k in (linear_kernel, gaussian_kernel(1.0)):
            for c in (0.1, 1.0, 10.0):
                for e in (0.05, 0.2):
                    m = SVR(k, c, e).fit(xs, ys)
                    assert all(0 <= v <= c for v in m.a + m.a_star)
                    assert all(a * s == 0 for a, s in zip(m.a, m.a_star))  # a_i a*_i = 0
                    assert abs(sum(m.theta)) < 1e-9
                    assert m.kkt_violation() < 1e-6
                    p, d = m.primal_objective(), m.dual_objective()
                    assert -1e-9 <= p - d < 1e-6 * (1 + abs(p))


def test_tube_and_support_vectors() -> None:
    xs, ys = sine_data(4, 40, 0.1)
    for e in (0.05, 0.1, 0.3):
        m = SVR(gaussian_kernel(1.0), 5.0, e).fit(xs, ys)
        for i, (y, f) in enumerate(zip(ys, m.fitted())):
            if abs(y - f) < e - 1e-6:
                assert m.theta[i] == 0.0  # strictly inside the tube: not a support vector
            if abs(y - f) > e + 1e-6:
                assert abs(abs(m.theta[i]) - m.c) < 1e-12  # outside the tube: at the bound C
    counts = [len(SVR(gaussian_kernel(1.0), 5.0, e).fit(xs, ys).sv) for e in (0.02, 0.1, 0.3, 0.6)]
    assert counts == sorted(counts, reverse=True) and counts[0] > counts[-1]


def test_against_a_direct_primal_minimization() -> None:
    # For a linear kernel in one dimension, the primal in (w, b) is convex in
    # two variables; nested ternary searches find its minimum.
    rng = random.Random(9)
    for _ in range(5):
        xs = [(rng.uniform(-2, 2),) for _ in range(10)]
        ys = [1.5 * x[0] + rng.gauss(0, 0.5) for x in xs]
        c, e = rng.choice([0.2, 1.0, 5.0]), rng.choice([0.1, 0.4])

        def primal(w, b):
            return 0.5 * w * w + c * sum(eps_insensitive(y - w * x[0] - b, e) for x, y in zip(xs, ys))

        def best_b(w):
            lo, hi = -20.0, 20.0
            for _ in range(100):
                m1, m2 = lo + (hi - lo) / 3, hi - (hi - lo) / 3
                lo, hi = (lo, m2) if primal(w, m1) <= primal(w, m2) else (m1, hi)
            return primal(w, (lo + hi) / 2)

        lo, hi = -20.0, 20.0
        for _ in range(100):
            m1, m2 = lo + (hi - lo) / 3, hi - (hi - lo) / 3
            lo, hi = (lo, m2) if best_b(m1) <= best_b(m2) else (m1, hi)
        exact = best_b((lo + hi) / 2)
        m = SVR(linear_kernel, c, e).fit(xs, ys)
        assert abs(m.primal_objective() - exact) < 1e-6 * (1 + exact)
