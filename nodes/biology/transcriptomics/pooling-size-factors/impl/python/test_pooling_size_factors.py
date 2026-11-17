# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pooling-size-factors/. The authors are listed in prov/EQZ9B0.jsonl.

import math
import random
from fractions import Fraction

import pytest

from pooling_size_factors import (
    build_system,
    median_ratio,
    pooled_size_factors,
    ring_order,
    ring_pools,
    solve_pools,
)
from rq3lin import poisson_knuth

# The answers below are exact in exact arithmetic. In floating point the normal
# matrix can be nearly singular (see the circulant test), with a condition number
# up to about (total pool size) / weak, so rounding errors of about 1e-16 grow to
# about 1e-7. The tolerance leaves a factor of 100 on that.
TOL = 1e-5


def exact_data(rng, G, n, de_frac, clusters=None):
    """counts[g][j] = theta_j lam_g for non-DE genes; DE genes get a cell-specific factor."""
    theta = [rng.uniform(0.3, 3.0) for _ in range(n)]
    lam = [rng.uniform(1.0, 50.0) for _ in range(G)]
    n_de = int(de_frac * G)
    counts = []
    for g in range(G):
        row = []
        for j in range(n):
            f = 1.0
            if g < n_de:
                f = rng.choice([0.1, 1.0, 8.0]) if clusters is None else (6.0 if clusters[j] == 1 else 1.0)
            row.append(theta[j] * lam[g] * f)
        counts.append(row)
    return counts, theta


def centered(v):
    m = sum(v) / len(v)
    return [x / m for x in v]


def frac_solve(A, b):
    n = len(A)
    M = [A[i][:] + [b[i]] for i in range(n)]
    for c in range(n):
        p = next(r for r in range(c, n) if M[r][c] != 0)
        M[c], M[p] = M[p], M[c]
        for r in range(n):
            if r != c and M[r][c] != 0:
                f = M[r][c] / M[c][c]
                M[r] = [x - f * y for x, y in zip(M[r], M[c])]
    return [M[i][n] / M[i][i] for i in range(n)]


def test_page_example():
    Y = [[10, 20, 10, 40], [6, 12, 6, 24], [4, 8, 4, 96]]
    pools, f, single, t = build_system(Y, sizes=(2, 3))
    assert t == [20, 40, 20, 160]
    assert pools == [[0, 1], [1, 3], [3, 2], [2, 0], [0, 1, 3], [1, 3, 2], [3, 2, 0], [2, 0, 1]]
    want = [16, 12, 12, 16, 20, 20, 20, 24]
    assert all(math.isclose(a, b / 7, rel_tol=1e-12) for a, b in zip(f, want))
    assert all(math.isclose(a, b / 7, rel_tol=1e-12) for a, b in zip(single, [8, 8, 8, 4]))
    got = pooled_size_factors(Y, sizes=(2, 3))
    assert all(math.isclose(a, b, rel_tol=TOL) for a, b in zip(got, [0.5, 1.0, 0.5, 2.0]))
    # Pools of size 2 alone are singular on a ring of 4: x + (1, -1, 1, -1) fits them too.
    alt = [1, -1, 1, -1]
    assert all(alt[p[0]] + alt[p[1]] == 0 for p in ring_pools(4, [2]))


def test_ring_order():
    lib = [50, 10, 40, 20, 30, 60]
    # Sorted: cells 1 (10), 3 (20), 4 (30), 2 (40), 0 (50), 5 (60).
    assert ring_order(lib) == [1, 4, 0, 5, 2, 3]


def test_ring_pools_wrap_and_count():
    pools = ring_pools(5, [2, 5])
    assert len(pools) == 10
    assert pools[4] == [4, 0]
    assert all(sorted(p) == [0, 1, 2, 3, 4] for p in pools[5:])
    with pytest.raises(ValueError):
        ring_pools(5, [6])


def test_each_cell_is_in_the_sum_of_the_sizes_pools():
    pools = ring_pools(120, [20, 40, 60, 80, 100])
    for j in range(120):
        assert sum(p.count(j) for p in pools) == 300


def test_median_ratio():
    assert median_ratio([2, 4, 9, 0], [1, 2, 3, 0]) == 2
    with pytest.raises(ValueError):
        median_ratio([1, 2], [0, 0])


def test_exact_recovery_with_a_minority_of_de_genes():
    rng = random.Random(1)
    for de in (0.0, 0.2, 0.45):
        counts, theta = exact_data(rng, 40, 50, de)
        got = pooled_size_factors(counts, sizes=(10, 20, 30, 40))
        assert all(math.isclose(a, b, rel_tol=TOL) for a, b in zip(got, centered(theta)))


def test_library_size_is_wrong_under_composition_but_pooling_is_right():
    rng = random.Random(2)
    counts, theta = exact_data(rng, 40, 50, 0.3)
    lib = centered([sum(counts[g][j] for g in range(40)) for j in range(50)])
    truth = centered(theta)
    assert max(abs(a / b - 1) for a, b in zip(lib, truth)) > 0.2
    got = pooled_size_factors(counts, sizes=(10, 20, 30, 40))
    assert max(abs(a / b - 1) for a, b in zip(got, truth)) < TOL


def test_float_solution_matches_exact_rational_solution():
    rng = random.Random(3)
    n, G = 8, 6
    counts = [[rng.randint(0, 9) + (1 if g == 0 else 0) for _ in range(n)] for g in range(G)]
    pools, factors, single, t = build_system(counts, sizes=(2, 4))
    x = solve_pools(n, pools, factors, single, weak=1e-6)
    w = Fraction(1, 10 ** 6)
    N = [[Fraction(0)] * n for _ in range(n)]
    rhs = [Fraction(0)] * n
    for S, f in zip(pools, factors):
        for a in S:
            rhs[a] += Fraction(f)
            for b in S:
                N[a][b] += 1
    for j in range(n):
        N[j][j] += w
        rhs[j] += w * Fraction(single[j])
    exact = frac_solve(N, rhs)
    assert all(math.isclose(a, float(b), rel_tol=1e-7, abs_tol=1e-9) for a, b in zip(x, exact))


def test_pool_equations_alone_can_be_singular():
    """n = 100 with all sizes multiples of 20: the ring vector cos(2 pi 5 p / 100) has zero sum on every pool."""
    n, sizes = 100, (20, 40, 60, 80, 100)
    v = [math.cos(2 * math.pi * 5 * p / n) for p in range(n)]
    for pool in ring_pools(n, sizes):
        assert abs(sum(v[p] for p in pool)) < 1e-9
    # The condition of the proof: some k, not a multiple of n, with n | k w for every w.
    assert any(all(k * w % n == 0 for w in sizes) for k in range(1, n))
    assert not any(all(k * w % 101 == 0 for w in sizes) for k in range(1, 101))


def test_weak_equations_make_the_answer_unique_and_barely_move_it():
    rng = random.Random(4)
    counts, theta = exact_data(rng, 30, 100, 0.2)
    got = pooled_size_factors(counts)
    assert all(math.isclose(a, b, rel_tol=TOL) for a, b in zip(got, centered(theta)))


def test_clusters_exact():
    rng = random.Random(5)
    n = 60
    clusters = [0] * 35 + [1] * 25
    counts, theta = exact_data(rng, 40, n, 0.4, clusters)
    got = pooled_size_factors(counts, sizes=(5, 10, 15, 20), clusters=clusters)
    assert all(math.isclose(a, b, rel_tol=TOL) for a, b in zip(got, centered(theta)))


def test_errors():
    with pytest.raises(ValueError):
        pooled_size_factors([[0, 1], [0, 2]], sizes=(1,))


def test_poisson_counts_with_many_zeros_measured():
    """A measurement, not a theorem: 120 cells, 200 genes, mean count about 0.6, 20 percent DE genes."""
    rng = random.Random(2016)
    n, G = 120, 200
    theta = [math.exp(rng.gauss(0.0, 0.4)) for _ in range(n)]
    lam = [math.exp(rng.gauss(-1.0, 1.0)) for _ in range(G)]
    group = [j % 2 for j in range(n)]
    counts = []
    for g in range(G):
        up = g < 40
        counts.append([poisson_knuth(rng, theta[j] * lam[g] * (5.0 if up and group[j] else 1.0)) for j in range(n)])
    zeros = sum(c == 0 for row in counts for c in row) / (n * G)
    assert zeros > 0.5
    truth = centered(theta)
    pooled = pooled_size_factors(counts)
    lib = centered([sum(counts[g][j] for g in range(G)) for j in range(n)])

    def log_err(est):
        return sum((math.log(a / b)) ** 2 for a, b in zip(est, truth)) / n

    def group_bias(est):
        d = [math.log(a / b) for a, b in zip(est, truth)]
        return sum(d[j] for j in range(n) if group[j]) / 60 - sum(d[j] for j in range(n) if not group[j]) / 60

    assert all(v > 0 for v in pooled)
    assert log_err(pooled) < log_err(lib)
    # The library size inflates the factors of the group with the up genes (composition bias).
    assert abs(group_bias(pooled)) < 0.6 * abs(group_bias(lib))
    # The single-cell medians are mostly 0, so they cannot be used directly.
    _, _, single, _ = build_system(counts)
    assert sum(s == 0 for s in single) > n / 2
