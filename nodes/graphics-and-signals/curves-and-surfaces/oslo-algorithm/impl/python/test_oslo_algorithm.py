# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/oslo-algorithm/. The authors are listed in prov/MGGW0D.jsonl.

import random
from bisect import bisect_right
from fractions import Fraction

import pytest

from oslo_algorithm import oslo_matrix, oslo_refine


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
    for b, pt in zip(cox_de_boor_all(knots, p, u), ctrl):
        for k in range(len(out)):
            out[k] += b * pt[k]
    return tuple(out)


def boehm_insert(knots, p, ctrl, u):
    """Reference: Boehm's single knot insertion."""
    mu = bisect_right(knots, u) - 1
    new = list(ctrl[: mu - p + 1])
    for i in range(mu - p + 1, mu + 1):
        a = Fraction(u - knots[i]) / (knots[i + p] - knots[i])
        new.append(tuple((1 - a) * x + a * y for x, y in zip(ctrl[i - 1], ctrl[i])))
    new += list(ctrl[mu:])
    return sorted(list(knots) + [u]), new


def random_case(rng):
    p = rng.randint(1, 4)
    n = rng.randint(p, p + 4)
    while True:
        tau = sorted(rng.randint(0, 6) for _ in range(n + p + 2))
        ok = max(tau.count(v) for v in tau) <= p + 1
        if ok and tau[p] < tau[p + 1] and tau[n] < tau[n + 1]:
            break
    ctrl = [(Fraction(rng.randint(-9, 9)), Fraction(rng.randint(-9, 9), 3)) for _ in range(n + 1)]
    lo, hi = tau[p], tau[n + 1]
    t = list(tau)
    for _ in range(rng.randint(1, 5)):
        x = lo + (hi - lo) * Fraction(rng.randint(1, 11), 12)
        if t.count(x) <= p:
            t = sorted(t + [x])
    return p, n, tau, t, ctrl


def test_example_of_the_page():
    tau = [0, 0, 0, 1, 2, 3, 3, 3]
    t = [0, 0, 0, Fraction(1, 2), 1, Fraction(3, 2), 2, Fraction(5, 2), 3, 3, 3]
    ctrl = [(0, 0), (1, 2), (3, 3), (5, 1), (6, 0)]
    h = Fraction(1, 2)
    q = Fraction(1, 4)
    assert oslo_refine(tau, t, 2, ctrl) == [
        (0, 0),
        (h, 1),
        (3 * h, 9 * q),
        (5 * h, 11 * q),
        (7 * h, 5 * h),
        (9 * h, 3 * h),
        (11 * h, h),
        (6, 0),
    ]
    rows = oslo_matrix(tau, t, 2)
    assert rows[2] == {1: 3 * q, 2: q} and rows[3] == {1: q, 2: 3 * q}


def test_matches_repeated_boehm_insertion():
    rng = random.Random(31)
    for _ in range(500):
        p, n, tau, t, ctrl = random_case(rng)
        work_knots, work_ctrl = list(tau), list(ctrl)
        extra = list(t)
        for x in tau:
            extra.remove(x)
        for x in extra:
            work_knots, work_ctrl = boehm_insert(work_knots, p, work_ctrl, x)
        assert work_knots == t
        assert oslo_refine(tau, t, p, ctrl) == [tuple(Fraction(c) for c in pt) for pt in work_ctrl]


def test_curve_is_unchanged():
    rng = random.Random(32)
    for _ in range(300):
        p, n, tau, t, ctrl = random_case(rng)
        fine = oslo_refine(tau, t, p, ctrl)
        big_n = len(t) - p - 2
        params = []
        for mu in range(p, big_n + 1):
            if t[mu] < t[mu + 1]:
                params += [t[mu] + (t[mu + 1] - t[mu]) * Fraction(k, p + 1) for k in range(p + 1)]
        params += [tau[p] + (tau[n + 1] - tau[p]) * Fraction(rng.randint(0, 99), 100) for _ in range(4)]
        for x in params:
            assert curve(t, p, fine, x) == curve(tau, p, ctrl, x)


def test_rows_are_convex_weights():
    rng = random.Random(33)
    for _ in range(500):
        p, n, tau, t, ctrl = random_case(rng)
        for row in oslo_matrix(tau, t, p):
            assert sum(row.values()) == 1
            assert all(a > 0 for a in row.values())


def test_no_new_knot_gives_the_identity():
    tau = [0, 0, 0, 0, 1, 3, 4, 4, 4, 4]
    rows = oslo_matrix(tau, tau, 3)
    assert rows == [{i: 1} for i in range(6)]


def test_rejects_bad_input():
    tau = [0, 0, 0, 1, 2, 2, 2]
    ctrl = [(0, 0), (1, 1), (2, 0), (3, 1)]
    with pytest.raises(ValueError):
        oslo_refine(tau, [0, 0, 0, 2, 2, 2], 2, ctrl)
    with pytest.raises(ValueError):
        oslo_refine(tau, [0, 0, 0, 0, 1, 2, 2, 2], 2, ctrl)
    with pytest.raises(ValueError):
        oslo_refine(tau, [0, 0, 0, 1, 1, 1, 1, 2, 2, 2], 2, ctrl)
