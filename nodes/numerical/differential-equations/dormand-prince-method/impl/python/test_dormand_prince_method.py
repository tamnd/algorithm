# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dormand-prince-method/. The authors are listed in prov/Q8KN04.jsonl.

import math
import random
from fractions import Fraction as Fr

import pytest

from dormand_prince_method import A, B, B_HAT, C, dormand_prince_method, fixed_step

S = 7
AM = [[A[i][j] if j < len(A[i]) else Fr(0) for j in range(S)] for i in range(S)]


def trees(max_order):
    """Rooted trees as sorted tuples of subtrees, grouped by order (no recursion depth issue)."""
    by_order = {1: [()]}
    for n in range(2, max_order + 1):
        found = set()
        # children multisets: partitions of n - 1 into orders of subtrees
        def build(rest, min_key, acc):
            if rest == 0:
                found.add(tuple(sorted(acc)))
                return
            for m in range(1, rest + 1):
                for t in by_order[m]:
                    key = (m, t)
                    if key >= min_key:
                        build(rest - m, key, acc + [t])
        build(n - 1, (0, ()), [])
        by_order[n] = sorted(found)
    return by_order


def order_of(t):
    return 1 + sum(order_of(u) for u in t)


def gamma(t):
    g = order_of(t)
    for u in t:
        g *= gamma(u)
    return g


def stage_vector(t):
    v = [Fr(1)] * S
    for u in t:
        w = stage_vector(u)
        aw = [sum(AM[i][j] * w[j] for j in range(S)) for i in range(S)]
        v = [a * b for a, b in zip(v, aw)]
    return v


def satisfies(b, t):
    return sum(bi * vi for bi, vi in zip(b, stage_vector(t))) == Fr(1, gamma(t))


def test_tree_counts_and_order_conditions():
    ts = trees(6)
    assert [len(ts[n]) for n in range(1, 7)] == [1, 1, 2, 4, 9, 20]
    assert all(sum(AM[i]) == C[i] for i in range(S))
    for n in range(1, 6):
        assert all(satisfies(B, t) for t in ts[n])  # order 5: 17 conditions
    assert not all(satisfies(B, t) for t in ts[6])  # order exactly 5
    for n in range(1, 5):
        assert all(satisfies(B_HAT, t) for t in ts[n])  # order 4: 8 conditions
    assert not all(satisfies(B_HAT, t) for t in ts[5])


def test_fsal_and_stability_polynomial():
    assert A[6] == B[:6] and B[6] == 0 and C[6] == 1
    v, coeff = [Fr(1)] * S, [Fr(1)]
    for _ in range(S):
        coeff.append(sum(bi * vi for bi, vi in zip(B, v)))
        v = [sum(AM[i][j] * v[j] for j in range(S)) for i in range(S)]
    assert coeff == [Fr(1), Fr(1), Fr(1, 2), Fr(1, 6), Fr(1, 24), Fr(1, 120), Fr(1, 600), Fr(0)]


def f_quad(t, y):
    return [-2 * t * y[0] ** 2]


def test_worked_example_trace():
    r = dormand_prince_method(f_quad, 0.0, [1.0], 1.0, atol=1e-6, rtol=1e-6, h=0.1,
                              keep_path=True)
    assert (r.accepted, r.rejected, r.f_evals) == (6, 2, 49)
    ts = [round(t, 6) for t, _ in r.path]
    assert ts == [0.0, 0.1, 0.315901, 0.490436, 0.668019, 0.857716, 1.0]
    assert abs(r.y[0] - 0.5) < 2e-8


def test_observed_orders_with_fixed_steps():
    e5 = [abs(fixed_step(f_quad, 0.0, [1.0], 0.2 / 2 ** k, 5 * 2 ** k)[0] - 0.5) for k in range(4)]
    e4 = [abs(fixed_step(f_quad, 0.0, [1.0], 0.2 / 2 ** k, 5 * 2 ** k, B_HAT)[0] - 0.5)
          for k in range(4)]
    p5 = [math.log2(e5[i] / e5[i + 1]) for i in range(3)]
    p4 = [math.log2(e4[i] / e4[i + 1]) for i in range(3)]
    assert all(4.9 < p < 5.4 for p in p5)
    assert all(4.0 < p < 4.8 for p in p4)


def test_random_test_equations_against_exponential():
    rng = random.Random(1980)
    for _ in range(500):
        lam = rng.uniform(-3, 1)
        y0 = rng.uniform(-2, 2)
        t_end = rng.uniform(0, 2)
        r = dormand_prince_method(lambda t, y: [lam * y[0]], 0.0, [y0], t_end, 1e-8, 1e-8)
        assert r.t == t_end
        assert abs(r.y[0] - y0 * math.exp(lam * t_end)) <= 1e-6 * (1 + abs(y0) * math.exp(lam * t_end))
        assert r.f_evals == 2 + 6 * (r.accepted + r.rejected)


def test_harmonic_oscillator_and_logistic_vector():
    f = lambda t, y: [y[1], -y[0], y[2] * (1 - y[2])]
    r = dormand_prince_method(f, 0.0, [1.0, 0.0, 0.5], 10.0, 1e-9, 1e-9)
    assert abs(r.y[0] - math.cos(10)) < 1e-7 and abs(r.y[1] + math.sin(10)) < 1e-7
    assert abs(r.y[2] - 1 / (1 + math.exp(-10))) < 1e-8
    assert abs(r.y[0] ** 2 + r.y[1] ** 2 - 1) < 1e-7


def test_tolerance_reduces_error():
    errs = [abs(dormand_prince_method(f_quad, 0.0, [1.0], 1.0, tol, tol).y[0] - 0.5)
            for tol in (1e-4, 1e-7, 1e-10)]
    assert errs[0] > errs[1] > errs[2] and errs[2] < 1e-9


def test_edges():
    r = dormand_prince_method(f_quad, 0.0, [1.0], 0.0)
    assert (r.accepted, r.f_evals, r.y) == (0, 0, [1.0])
    r = dormand_prince_method(lambda t, y: [1.0], 0.0, [0.0], 0.3, h=5.0)
    assert r.accepted == 1 and r.t == 0.3 and abs(r.y[0] - 0.3) < 1e-15
    with pytest.raises(ValueError):
        dormand_prince_method(f_quad, 1.0, [1.0], 0.0)


def test_stiff_problem_step_limited_by_stability():
    lam = -1000.0
    f = lambda t, y: [lam * (y[0] - math.cos(t)) - math.sin(t)]  # solution cos t
    r = dormand_prince_method(f, 0.0, [1.0], 1.0, 1e-3, 1e-3)
    assert abs(r.y[0] - math.cos(1.0)) < 1e-2
    # stability interval about [-3.31, 0]: at least 1000/3.31 accepted steps are needed
    assert r.accepted + r.rejected > 300
