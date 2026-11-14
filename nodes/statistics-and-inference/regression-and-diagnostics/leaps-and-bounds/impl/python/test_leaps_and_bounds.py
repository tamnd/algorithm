# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/leaps-and-bounds/. The authors are listed in prov/EKM5SR.jsonl.

import itertools
import math
import random
from fractions import Fraction

import pytest

from leaps_and_bounds import centered_sscp, leaps_and_bounds, sweep


def solve(a, b):
    """Gaussian elimination with partial pivoting; works for floats and Fractions."""
    k = len(a)
    m = [list(row) + [b[i]] for i, row in enumerate(a)]
    for c in range(k):
        piv = max(range(c, k), key=lambda r: abs(m[r][c]))
        m[c], m[piv] = m[piv], m[c]
        for r in range(c + 1, k):
            f = m[r][c] / m[c][c]
            m[r] = [u - f * v for u, v in zip(m[r], m[c])]
    out = [0] * k
    for i in reversed(range(k)):
        out[i] = (m[i][k] - sum(m[i][j] * out[j] for j in range(i + 1, k))) / m[i][i]
    return out


def rss_direct(x, y, s):
    """RSS of the fit with an intercept and the columns s, from the normal equations on raw data."""
    one = Fraction(1) if isinstance(y[0], Fraction) else 1.0
    rows = [[one] + [r[j] for j in s] for r in x]
    k = len(rows[0])
    xtx = [[sum(r[i] * r[j] for r in rows) for j in range(k)] for i in range(k)]
    xty = [sum(r[i] * v for r, v in zip(rows, y)) for i in range(k)]
    b = solve(xtx, xty)
    return sum((v - sum(bi * ri for bi, ri in zip(b, r))) ** 2 for r, v in zip(rows, y))


def exhaustive(x, y, nbest):
    p = len(x[0])
    out = []
    for size in range(p + 1):
        vals = sorted(rss_direct(x, y, s) for s in itertools.combinations(range(p), size))
        out.append(vals[:nbest])
    return out


def correlated_data(rng, n, p, rho=0.6):
    x = []
    for _ in range(n):
        z0 = rng.gauss(0, 1)
        x.append([math.sqrt(1 - rho) * rng.gauss(0, 1) + math.sqrt(rho) * z0 for _ in range(p)])
    beta = [rng.choice([0.0, 0.0, 0.5, 1.0, -1.0]) for _ in range(p)]
    y = [sum(b * v for b, v in zip(beta, r)) + rng.gauss(0, 1) for r in x]
    return x, y


def test_matches_all_subsets_for_p_up_to_10():
    rng = random.Random(20261114)
    for p in range(1, 11):
        for nbest in (1, 3):
            x, y = correlated_data(rng, 3 * p + 5, p)
            got = leaps_and_bounds(x, y, nbest)
            want = exhaustive(x, y, nbest)
            for size in range(p + 1):
                vals = [r for r, _ in got.best[size]]
                assert len(vals) == len(want[size])
                for g, w in zip(vals, want[size]):
                    assert math.isclose(g, w, rel_tol=1e-9, abs_tol=1e-9)
                for r, s in got.best[size]:
                    assert len(s) == size
                    assert math.isclose(r, rss_direct(x, y, s), rel_tol=1e-9, abs_tol=1e-9)


def test_exact_in_fractions():
    rng = random.Random(5)
    for _ in range(3):
        p, n = 6, 12
        x = [[Fraction(rng.randint(-5, 5)) for _ in range(p)] for _ in range(n)]
        y = [Fraction(x[i][0] - 2 * x[i][3] + rng.randint(-4, 4)) for i in range(n)]
        got = leaps_and_bounds(x, y, 2)
        want = exhaustive(x, y, 2)
        for size in range(p + 1):
            assert [r for r, _ in got.best[size]] == want[size]


def test_bounding_rule_a_superset_never_has_a_larger_rss():
    rng = random.Random(11)
    p, n = 5, 10
    x = [[Fraction(rng.randint(-3, 3)) for _ in range(p)] for _ in range(n)]
    y = [Fraction(rng.randint(-6, 6)) for _ in range(n)]
    rss = {s: rss_direct(x, y, s) for r in range(p + 1) for s in itertools.combinations(range(p), r)}
    for t in rss:
        for s in rss:
            if set(t) <= set(s):
                assert rss[s] <= rss[t]


def test_sweep_out_of_full_model_gives_the_subset_rss():
    rng = random.Random(3)
    x = [[Fraction(rng.randint(-3, 3)) for _ in range(4)] for _ in range(9)]
    y = [Fraction(rng.randint(-6, 6)) for _ in range(9)]
    a = centered_sscp(x, y)
    for j in range(4):
        sweep(a, j)
    for j in (3, 1):
        sweep(a, j, reverse=True)
    assert a[4][4] == rss_direct(x, y, (0, 2))


def test_pruning_visits_far_fewer_nodes_than_the_full_tree():
    rng = random.Random(42)
    p = 14
    x, y = correlated_data(rng, 60, p, rho=0.3)
    res = leaps_and_bounds(x, y)
    assert res.nodes < 2 ** (p + 1) // 20
    assert res.sweeps == p + res.nodes - 1  # one sweep for each child node


def test_collinear_columns_are_rejected():
    x = [[1.0, 2.0], [2.0, 4.0], [3.0, 6.0], [4.0, 8.0]]
    with pytest.raises(ValueError):
        leaps_and_bounds(x, [1.0, 2.0, 2.0, 5.0])
    with pytest.raises(ValueError):
        leaps_and_bounds([[1.0], [2.0]], [1.0, 2.0], 0)
