# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lr-b-spline/. The authors are listed in prov/G8C6QC.jsonl.

import random
from fractions import Fraction as F

from lr_b_spline import LRSpline, local_bspline, split_knots


def open_knots(n, p):
    return [F(0)] * (p + 1) + [F(a) for a in range(1, n)] + [F(n)] * (p + 1)


def boehm(knots, coeffs, u, p):
    """Reference: whole-vector knot insertion in one direction."""
    k = max(i for i in range(len(knots) - 1) if knots[i] <= u < knots[i + 1])
    new = []
    for i in range(len(coeffs) + 1):
        if i <= k - p:
            new.append(coeffs[i])
        elif i > k:
            new.append(coeffs[i - 1])
        else:
            a = (u - knots[i]) / (knots[i + p] - knots[i])
            new.append(a * coeffs[i] + (1 - a) * coeffs[i - 1])
    return sorted(knots + [u]), new


def pts(rng, k, n=4):
    return [(F(rng.randint(0, 100 * n), 100), F(rng.randint(0, 100 * n), 100)) for _ in range(k)]


def refine_random(S, rng):
    """Split a random B-spline at the middle of its longest knot interval, with a segment over its support."""
    xk, yk = rng.choice(sorted(S.funcs))
    if rng.random() < 0.5:
        a, b = max(zip(xk, xk[1:]), key=lambda ab: ab[1] - ab[0])
        return S.insert(("v", (a + b) / 2, yk[0], yk[-1]))
    a, b = max(zip(yk, yk[1:]), key=lambda ab: ab[1] - ab[0])
    return S.insert(("h", (a + b) / 2, xk[0], xk[-1]))


def test_one_knot_split_is_an_identity():
    rng = random.Random(1)
    for p in (1, 2, 3):
        for _ in range(20):
            t = tuple(sorted(F(rng.randint(0, 6)) for _ in range(p + 2)))
            if t[0] == t[-1]:
                continue
            a = F(rng.randint(1, 59), 10)
            if not t[0] < a < t[-1] or a in t:
                continue
            (t1, a1), (t2, a2) = split_knots(t, a)
            assert 0 < a1 <= 1 and 0 < a2 <= 1
            for _ in range(5):
                x = F(rng.randint(0, 600), 100)
                assert local_bspline(t, x, F(6)) == a1 * local_bspline(t1, x, F(6)) + a2 * local_bspline(t2, x, F(6))


def test_full_lines_give_the_tensor_product_refinement():
    rng = random.Random(2)
    p, q = 2, 3
    xk, yk = open_knots(4, p), open_knots(3, q)
    C = [[F(rng.randint(-9, 9)) for _ in range(len(yk) - q - 1)] for _ in range(len(xk) - p - 1)]
    S = LRSpline(xk, yk, p, q, C)
    S.insert(("v", F(5, 2), F(0), F(3)))
    S.insert(("h", F(1, 2), F(0), F(4)))
    # reference: Boehm on the rows, then on the columns
    xr, rows = xk, C
    cols = [list(c) for c in zip(*rows)]
    new_cols = []
    for col in cols:
        xr, c = boehm(xk, col, F(5, 2), p)
        new_cols.append(c)
    rows = [list(r) for r in zip(*new_cols)]
    yr = yk
    new_rows = []
    for row in rows:
        yr, r = boehm(yk, row, F(1, 2), q)
        new_rows.append(r)
    assert len(S.funcs) == len(new_rows) * len(new_rows[0])
    for i, row in enumerate(new_rows):
        for j, c in enumerate(row):
            key = (tuple(xr[i : i + p + 2]), tuple(yr[j : j + q + 2]))
            assert S.funcs[key] == [1, c]


def test_example_counts_and_weight():
    kn = open_knots(4, 2)
    S = LRSpline(kn, kn, 2, 2)
    assert S.insert(("v", F(3, 2), F(0), F(3))) == 9
    assert len(S.funcs) == 39
    assert all(g == 1 for g, _ in S.funcs.values())
    assert S.insert(("h", F(3, 2), F(0), F(3))) == 13
    assert len(S.funcs) == 43
    t = (F(1), F(3, 2), F(2), F(3))
    assert {k: g for k, (g, _) in S.funcs.items() if g != 1} == {(t, t): F(15, 16)}


def test_weighted_partition_of_unity():
    rng = random.Random(3)
    for p, q in ((2, 2), (3, 2), (1, 3)):
        S = LRSpline(open_knots(4, p), open_knots(4, q), p, q)
        for _ in range(12):
            refine_random(S, rng)
        assert all(g > 0 for g, _ in S.funcs.values())
        for x, y in pts(rng, 8) + [(F(4), F(4)), (F(0), F(4))]:
            assert S.evaluate(x, y, weights_only=True) == 1


def test_refinement_leaves_the_surface_unchanged():
    rng = random.Random(4)
    for p, q in ((2, 2), (3, 3)):
        xk, yk = open_knots(4, p), open_knots(4, q)
        C = [[F(rng.randint(-9, 9)) for _ in range(len(yk) - q - 1)] for _ in range(len(xk) - p - 1)]
        S = LRSpline(xk, yk, p, q, C)
        probe = pts(rng, 10)
        before = [S.evaluate(x, y) for x, y in probe]
        for _ in range(10):
            refine_random(S, rng)
            assert [S.evaluate(x, y) for x, y in probe] == before


def test_no_b_spline_is_left_traversed():
    rng = random.Random(5)
    S = LRSpline(open_knots(4, 2), open_knots(4, 2), 2, 2)
    for _ in range(15):
        refine_random(S, rng)
        assert all(S.traversing(k) is None for k in S.funcs)


def test_a_segment_that_splits_nothing_is_refused():
    kn = open_knots(4, 2)
    S = LRSpline(kn, kn, 2, 2)
    funcs, lines = dict(S.funcs), dict(S.lines)
    try:
        S.insert(("v", F(3, 2), F(0), F(1, 2)))
        refused = False
    except ValueError:
        refused = True
    assert refused
    assert S.funcs == funcs and S.lines == lines
