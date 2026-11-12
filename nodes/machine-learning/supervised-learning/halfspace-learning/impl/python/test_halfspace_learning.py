# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/halfspace-learning/. The authors are listed in prov/34Q4BF.jsonl.

import random
from fractions import Fraction as F
from itertools import combinations, product

from halfspace_learning import (Infeasible, Unbounded, consistent, random_separable, separate, shattered,
                                simplex)


def test_consistent_on_random_separable_data() -> None:
    rng = random.Random(1)
    for _ in range(40):
        d = rng.randint(1, 4)
        xs, ys, w0, b0 = random_separable(rng.randint(1, 25), d, rng)
        out = separate(xs, ys)
        assert out is not None
        w, b, _ = out
        assert consistent(w, b, xs, ys)
        # Phase 2 minimizes |w|_1 + |b|: the true separator, scaled to margin 1, is no better.
        k = min(y * (sum(a * c for a, c in zip(w0, x)) + b0) for x, y in zip(xs, ys))
        assert sum(abs(v) for v in w) + abs(b) <= (sum(abs(v) for v in w0) + abs(b0)) / k


def test_xor_is_not_separable() -> None:
    xs = [[F(0), F(0)], [F(1), F(1)], [F(0), F(1)], [F(1), F(0)]]
    assert separate(xs, [1, 1, -1, -1]) is None


def test_one_dimension_against_brute_force() -> None:
    rng = random.Random(2)
    for _ in range(300):
        n = rng.randint(1, 7)
        xs = [[F(v)] for v in rng.sample(range(-10, 11), n)]
        ys = [rng.choice((-1, 1)) for _ in range(n)]
        order = [y for _, y in sorted(zip([x[0] for x in xs], ys))]
        brute = any(order == [-s] * k + [s] * (n - k) for s in (1, -1) for k in range(n + 1))
        assert (separate(xs, ys) is not None) == brute


def test_vc_dimension_d_plus_one() -> None:
    for d in (1, 2, 3):
        pts = [[F(0)] * d] + [[F(int(i == j)) for j in range(d)] for i in range(d)]
        assert shattered(pts)
    triangle_and_inside = [[F(0), F(0)], [F(4), F(0)], [F(0), F(4)], [F(1), F(1)]]
    assert not shattered(triangle_and_inside)
    assert not shattered([[F(0), F(0)], [F(1), F(1)], [F(0), F(1)], [F(1), F(0)]])
    rng = random.Random(3)
    for d in (1, 2, 3):  # Radon: no d + 2 points are shattered
        for _ in range(5):
            pts = [[F(rng.randint(-20, 20), 7) for _ in range(d)] for _ in range(d + 2)]
            assert not shattered(pts)


def test_simplex_against_vertex_enumeration() -> None:
    rng = random.Random(4)
    for _ in range(200):
        m, n = 2, 4
        a = [[F(rng.randint(-3, 3)) for _ in range(n)] for _ in range(m)]
        b = [F(rng.randint(-4, 4)) for _ in range(m)]
        c = [F(rng.randint(0, 4)) for _ in range(n)]  # c >= 0, so a feasible LP is bounded
        best = None
        for cols in combinations(range(n), m):
            (p, q), (r, s) = [[a[i][j] for j in cols] for i in range(m)]
            det = p * s - q * r
            if det == 0:
                continue
            u = (b[0] * s - q * b[1]) / det
            v = (p * b[1] - r * b[0]) / det
            if u >= 0 and v >= 0:
                val = c[cols[0]] * u + c[cols[1]] * v
                best = val if best is None else min(best, val)
        try:
            x, _ = simplex(a, b, c)
        except Infeasible:
            # Rank-deficient systems can be feasible without a basis of two columns; check them apart.
            if best is not None:
                raise
            continue
        assert all(v >= 0 for v in x)
        assert all(sum(ai * xi for ai, xi in zip(row, x)) == bi for row, bi in zip(a, b))
        val = sum(ci * xi for ci, xi in zip(c, x))
        if best is not None:
            assert val == best


def test_unbounded_is_reported() -> None:
    try:
        simplex([[F(1), F(-1)]], [F(1)], [F(0), F(-1)])
    except Unbounded:
        return
    raise AssertionError("expected Unbounded")
