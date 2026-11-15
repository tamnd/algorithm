# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/implicit-feedback-als/. The authors are listed in prov/84ZRE0.jsonl.

import random
from fractions import Fraction

import pytest

import implicit_feedback_als as ials

TOL = 1e-9


def random_counts(m: int, n: int, density: float, seed: int) -> dict[tuple[int, int], float]:
    rng = random.Random(seed)
    out = {}
    for u in range(m):
        for i in range(n):
            if rng.random() < density:
                out[(u, i)] = float(rng.randint(1, 9))
    return out


def exact_solve(a, b):
    """Gaussian elimination in exact rational arithmetic."""
    n = len(a)
    m = [[Fraction(x) for x in row] + [Fraction(y)] for row, y in zip(a, b)]
    for c in range(n):
        piv = next(k for k in range(c, n) if m[k][c] != 0)
        m[c], m[piv] = m[piv], m[c]
        for k in range(n):
            if k != c and m[k][c] != 0:
                f = m[k][c] / m[c][c]
                m[k] = [x - f * y for x, y in zip(m[k], m[c])]
    return [m[k][n] / m[k][k] for k in range(n)]


def test_fast_solve_equals_direct_solve():
    rng = random.Random(7)
    for trial in range(20):
        n, r = rng.randint(3, 12), rng.randint(1, 5)
        y = [[rng.uniform(-1.0, 1.0) for _ in range(r)] for _ in range(n)]
        rows = {i: float(rng.randint(1, 20)) for i in range(n) if rng.random() < 0.4}
        lam, alpha = rng.uniform(0.01, 2.0), rng.choice([0.0, 1.0, 10.0, 40.0])
        g = ials.gram(y, r)
        af, bf = ials.fast_system(rows, y, g, lam, alpha)
        ad, bd = ials.direct_system(rows, y, lam, alpha)
        for s in range(r):
            assert abs(bf[s] - bd[s]) <= TOL * (1 + abs(bd[s]))
            for t in range(r):
                assert abs(af[s][t] - ad[s][t]) <= TOL * (1 + abs(ad[s][t]))
        xf = ials.cholesky_solve(af, bf)
        xd = ials.cholesky_solve(ad, bd)
        xe = exact_solve(ad, bd)
        for s in range(r):
            assert abs(xf[s] - xd[s]) <= TOL
            assert abs(xd[s] - float(xe[s])) <= TOL


def test_half_step_minimizes_its_block():
    counts = random_counts(6, 5, 0.4, 3)
    lam, alpha, r = 0.5, 2.0, 2
    bu, _ = ials.group(counts)
    rng = random.Random(5)
    y = [[rng.gauss(0, 1) for _ in range(r)] for _ in range(5)]
    x = ials.half_step(bu, 6, y, lam, alpha)
    best = ials.objective(counts, x, y, lam, alpha)
    for _ in range(50):
        moved = [[a + rng.gauss(0, 0.05) for a in row] for row in x]
        assert ials.objective(counts, moved, y, lam, alpha) >= best - TOL


def test_objective_does_not_increase_after_each_half_step():
    for seed in range(5):
        counts = random_counts(9, 7, 0.3, seed)
        _, _, hist = ials.implicit_als(counts, 9, 7, 3, 0.1, 5.0, 8, seed=seed, track=True)
        assert len(hist) == 17
        for a, b in zip(hist, hist[1:]):
            assert b <= a + TOL * (1 + abs(a))


def test_page_example():
    counts = {(0, 0): 2.0, (0, 1): 1.0, (1, 1): 1.0, (1, 2): 3.0, (2, 0): 1.0}
    bu, bi = ials.group(counts)
    y = [[1.0], [1.0], [1.0]]
    x = ials.half_step(bu, 3, y, 1.0, 1.0)
    for got, want in zip(x, [5 / 7, 3 / 4, 2 / 5]):
        assert abs(got[0] - want) <= TOL
    assert abs(ials.objective(counts, [[0.0]] * 3, y, 1.0, 1.0) - 16.0) <= TOL
    assert abs(ials.objective(counts, x, y, 1.0, 1.0) - 499 / 70) <= TOL
    y2 = ials.half_step(bi, 3, x, 1.0, 1.0)
    for got, want in zip(y2, [0.8622210263539472, 0.8859938875683019, 0.7652662814305795]):
        assert abs(got[0] - want) <= TOL
    assert abs(ials.objective(counts, x, y2, 1.0, 1.0) - 6.804815546192129) <= TOL


def test_recommend_leaves_out_used_items():
    counts = random_counts(8, 10, 0.3, 11)
    x, y, _ = ials.implicit_als(counts, 8, 10, 2, 0.1, 10.0, 5)
    bu, _ = ials.group(counts)
    rows = bu.get(0, {})
    top = ials.recommend(rows, x[0], y, 3)
    assert len(top) == min(3, 10 - len(rows))
    assert not set(top) & set(rows)


def test_preconditions():
    with pytest.raises(ValueError):
        ials.implicit_als({(0, 0): 1.0}, 1, 1, 1, 0.0, 1.0, 1)
    with pytest.raises(ValueError):
        ials.implicit_als({(0, 0): 0.0}, 1, 1, 1, 1.0, 1.0, 1)
