# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/boehm-knot-insertion/. The authors are listed in prov/A1WEXZ.jsonl.

import random
from fractions import Fraction

import pytest

from boehm_knot_insertion import boehm_insert, refine_by_insertion


def cox_de_boor_all(knots, p, u):
    """All N_(i,p)(u) by the Cox-de Boor recursion, one degree at a time, with 0/0 = 0."""
    m = len(knots) - 1
    big_n = [Fraction(1) if knots[i] <= u < knots[i + 1] else Fraction(0) for i in range(m)]
    for r in range(1, p + 1):
        nxt = []
        for i in range(m - r):
            v = Fraction(0)
            if knots[i + r] != knots[i]:
                v += (u - knots[i]) / Fraction(knots[i + r] - knots[i]) * big_n[i]
            if knots[i + r + 1] != knots[i + 1]:
                v += (knots[i + r + 1] - u) / Fraction(knots[i + r + 1] - knots[i + 1]) * big_n[i + 1]
            nxt.append(v)
        big_n = nxt
    return big_n


def curve(knots, p, ctrl, u):
    """The reference: sum_i N_(i,p)(u) P_i, for u in [t_p, t_(n+1))."""
    out = [Fraction(0)] * len(ctrl[0])
    basis = cox_de_boor_all(knots, p, u)
    for i, pt in enumerate(ctrl):
        b = basis[i]
        for k in range(len(out)):
            out[k] += b * pt[k]
    return tuple(out)


def test_params(knots, p, rng, extra=6):
    """p + 1 points in each nonempty span of the domain, which pin down each polynomial piece,
    and some random parameters."""
    n = len(knots) - p - 2
    params = []
    for mu in range(p, n + 1):
        a, b = knots[mu], knots[mu + 1]
        if a < b:
            params += [a + (b - a) * Fraction(k, p + 1) for k in range(p + 1)]
    lo, hi = knots[p], knots[n + 1]
    params += [lo + (hi - lo) * Fraction(rng.randint(0, 999), 1000) for _ in range(extra)]
    return params


test_params.__test__ = False


def random_case(rng):
    p = rng.randint(1, 4)
    n = rng.randint(p, p + 5)
    while True:
        knots = sorted(rng.randint(0, 6) for _ in range(n + p + 2))
        if max(knots.count(v) for v in knots) <= p + 1 and knots[p] < knots[n + 1]:
            break
    ctrl = [(Fraction(rng.randint(-9, 9)), Fraction(rng.randint(-9, 9), 2)) for _ in range(n + 1)]
    return p, n, knots, ctrl


def random_new_knot(rng, knots, p, n):
    while True:
        u = knots[p] + (knots[n + 1] - knots[p]) * Fraction(rng.randint(0, 11), 12)
        if knots.count(u) <= p:
            return u


def test_example_of_the_page():
    knots = [0, 0, 0, 1, 2, 3, 3, 3]
    ctrl = [(0, 0), (1, 2), (3, 3), (5, 1), (6, 0)]
    new_knots, new_ctrl = boehm_insert(knots, 2, ctrl, Fraction(3, 2))
    assert new_knots == [0, 0, 0, 1, Fraction(3, 2), 2, 3, 3, 3]
    half = Fraction(1, 2)
    assert new_ctrl == [(0, 0), (1, 2), (5 * half, Fraction(11, 4)), (7 * half, 5 * half), (5, 1), (6, 0)]


def test_curve_is_unchanged():
    rng = random.Random(21)
    for _ in range(500):
        p, n, knots, ctrl = random_case(rng)
        u = random_new_knot(rng, knots, p, n)
        new_knots, new_ctrl = boehm_insert(knots, p, ctrl, u)
        assert len(new_knots) == len(knots) + 1 and len(new_ctrl) == n + 2
        assert new_knots == sorted(knots + [u])
        for x in test_params(new_knots, p, rng):
            assert curve(new_knots, p, new_ctrl, x) == curve(knots, p, ctrl, x)


def test_new_points_cut_corners():
    # Each new point lies on a leg P_(i-1) P_i of the old control polygon.
    rng = random.Random(22)
    for _ in range(500):
        p, n, knots, ctrl = random_case(rng)
        u = random_new_knot(rng, knots, p, n)
        _, new_ctrl = boehm_insert(knots, p, ctrl, u)
        for i, q in enumerate(new_ctrl):
            ok = False
            for a, b in ((i - 1, i), (i - 1, i - 1), (i, i)):
                if 0 <= a <= n and 0 <= b <= n:
                    pa, pb = ctrl[a], ctrl[b]
                    cross = (pb[0] - pa[0]) * (q[1] - pa[1]) - (pb[1] - pa[1]) * (q[0] - pa[0])
                    dot = (q[0] - pa[0]) * (q[0] - pb[0]) + (q[1] - pa[1]) * (q[1] - pb[1])
                    ok = ok or (cross == 0 and dot <= 0)
            assert ok


def test_p_fold_knot_gives_a_point_of_the_curve():
    rng = random.Random(23)
    for _ in range(300):
        p = rng.randint(1, 4)
        n = rng.randint(p, p + 4)
        knots = [0] * (p + 1) + sorted(rng.sample(range(1, 10), n - p)) + [10] * (p + 1)
        ctrl = [(rng.randint(-9, 9), rng.randint(-9, 9)) for _ in range(n + 1)]
        u = Fraction(rng.randint(1, 99), 10)
        while u in knots:
            u += Fraction(1, 100)
        new_knots, new_ctrl = refine_by_insertion(knots, p, ctrl, [u] * p)
        k = new_knots.index(u)
        assert new_ctrl[k - 1] == curve(knots, p, ctrl, u)


def test_refinement_by_repeated_insertion():
    rng = random.Random(24)
    for _ in range(200):
        p, n, knots, ctrl = random_case(rng)
        new = []
        work = list(knots)
        for _ in range(rng.randint(1, 4)):
            u = random_new_knot(rng, work, p, len(work) - p - 2)
            new.append(u)
            work = sorted(work + [u])
        fine_knots, fine_ctrl = refine_by_insertion(knots, p, ctrl, new)
        assert fine_knots == work
        for x in test_params(fine_knots, p, rng, extra=5):
            assert curve(fine_knots, p, fine_ctrl, x) == curve(knots, p, ctrl, x)


def test_rejects_bad_input():
    knots = [0, 0, 0, 1, 1, 1]
    ctrl = [(0, 0), (1, 1), (2, 0)]
    with pytest.raises(ValueError):
        boehm_insert(knots, 2, ctrl, 1)
    with pytest.raises(ValueError):
        boehm_insert([0, 0, 0, 1, 1, 2, 2, 2], 2, ctrl + [(3, 3), (4, 4)], 2)
    with pytest.raises(ValueError):
        boehm_insert([0, 0, 0, 0, 1, 1, 1], 2, [(0, 0), (1, 1), (2, 0), (3, 1)], 0)
