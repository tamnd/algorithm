# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/doublet-detection/. The authors are listed in prov/WZKYKW.jsonl.

import math
import random

import pytest

from doublet_detection import (
    adjusted_k,
    bayes_score,
    call_doublets,
    doublet_scores,
    local_maxima,
    normalize_total,
    simulate_doublets,
    threshold_minimum,
)
from rq3lin import inverse, jacobi_eigh, knn, matmul, pca_fit, poisson_knuth, solve, sqdist


def cells(rng, n_per, n_types=3, d=30):
    """Cells of n_types types; type t has a mean of 8 on genes g with g mod n_types = t, and 1 elsewhere."""
    prof = [[8.0 if g % n_types == t else 1.0 for g in range(d)] for t in range(n_types)]
    X, lab = [], []
    for t in range(n_types):
        for _ in range(n_per):
            s = rng.uniform(0.6, 1.4)
            X.append([poisson_knuth(rng, s * m) for m in prof[t]])
            lab.append(t)
    return X, lab


def auc(pos, neg):
    w = sum(1.0 if p > q else 0.5 if p == q else 0.0 for p in pos for q in neg)
    return w / (len(pos) * len(neg))


# The group module rq3lin.

def test_knn_against_sorting_all_distances():
    rng = random.Random(1)
    pts = [[rng.randint(0, 3) for _ in range(2)] for _ in range(25)]
    for k in (0, 1, 4, 24):
        got = knn(pts, k)
        for i, nb in enumerate(got):
            order = sorted((j for j in range(25) if j != i), key=lambda j: (sqdist(pts[i], pts[j]), j))
            assert nb == order[:k]
    with pytest.raises(ValueError):
        knn(pts, 25)


def test_solve_and_inverse():
    rng = random.Random(2)
    for n in (1, 2, 5, 8):
        A = [[rng.uniform(-1, 1) for _ in range(n)] for _ in range(n)]
        x = [rng.uniform(-1, 1) for _ in range(n)]
        b = [sum(A[i][j] * x[j] for j in range(n)) for i in range(n)]
        assert all(math.isclose(u, v, abs_tol=1e-9) for u, v in zip(solve(A, b), x))
        P = matmul(A, inverse(A))
        assert all(abs(P[i][j] - (i == j)) < 1e-9 for i in range(n) for j in range(n))
    with pytest.raises(ValueError):
        solve([[1.0, 2.0], [2.0, 4.0]], [1.0, 2.0])


def test_jacobi_eigh():
    rng = random.Random(3)
    for n in (1, 3, 6, 10):
        B = [[rng.uniform(-1, 1) for _ in range(n)] for _ in range(n)]
        S = [[B[i][j] + B[j][i] for j in range(n)] for i in range(n)]
        vals, vecs = jacobi_eigh(S)
        assert vals == sorted(vals, reverse=True)
        for lam, v in zip(vals, vecs):
            Sv = [sum(S[i][j] * v[j] for j in range(n)) for i in range(n)]
            assert all(abs(a - lam * b) < 1e-9 for a, b in zip(Sv, v))
            assert math.isclose(sum(x * x for x in v), 1.0, rel_tol=1e-12)
        assert math.isclose(sum(vals), sum(S[i][i] for i in range(n)), abs_tol=1e-9)


def test_pca_of_points_on_a_line():
    pts = [[t, 2 * t, -t] for t in range(-3, 4)]
    mu, axes, var = pca_fit(pts, 1)
    s = math.sqrt(6)
    assert all(math.isclose(a, b, abs_tol=1e-12) for a, b in zip(axes[0], [1 / s, 2 / s, -1 / s]))
    assert math.isclose(var[0], 6 * sum(t * t for t in range(-3, 4)) / 6, rel_tol=1e-12)


def test_poisson_knuth_mean_and_variance():
    rng = random.Random(4)
    lam, n = 3.5, 4000
    xs = [poisson_knuth(rng, lam) for _ in range(n)]
    m = sum(xs) / n
    v = sum((x - m) ** 2 for x in xs) / (n - 1)
    assert abs(m - lam) <= 4 * math.sqrt(lam / n)
    assert abs(v - lam) <= 4 * math.sqrt(2 * lam * lam / n + lam / n)


# The doublet scores.

def test_simulated_doublets_are_sums_of_two_cells():
    rng = random.Random(5)
    X = [[rng.randint(0, 9) for _ in range(4)] for _ in range(6)]
    sims, pairs = simulate_doublets(X, 20, random.Random(6))
    again = random.Random(6)
    for s, (a, b) in zip(sims, pairs):
        assert (a, b) == (again.randrange(6), again.randrange(6))
        assert s == [x + y for x, y in zip(X[a], X[b])]


def test_normalize_total():
    out = normalize_total([[1, 3], [0, 0], [2, 2]], 8.0)
    assert out == [[2.0, 6.0], [0.0, 0.0], [4.0, 4.0]]


def test_adjusted_k():
    assert adjusted_k(5, 100, 200) == 15
    assert adjusted_k(6, 400, 800) == 18
    assert adjusted_k(7, 10, 5) == 10


def test_score_is_bayes_rule_with_neighbor_densities():
    """Treat the observed neighbors as singlets with density fs and the simulated ones as doublets."""
    for rho in (0.05, 0.1, 0.3):
        for r in (0.5, 1.0, 2.0):
            for k_adj in (3, 10, 31):
                for nd in range(k_adj + 1):
                    q = (nd + 1) / (k_adj + 2)
                    fd, fs = q / r, 1 - q          # sim density r fd, obs density fs
                    post = rho * fd / (rho * fd + (1 - rho) * fs)
                    assert math.isclose(bayes_score(nd, k_adj, rho, r), post, rel_tol=1e-12)


def test_score_is_increasing_in_simulated_neighbors_and_in_zero_one():
    for rho in (0.02, 0.1, 0.5):
        for r in (0.5, 2.0):
            k_adj = 20
            s = [bayes_score(nd, k_adj, rho, r) for nd in range(k_adj + 1)]
            assert all(a < b for a, b in zip(s, s[1:]))
            assert 0.0 < s[0] and s[-1] < 1.0


def test_score_is_rho_when_the_neighborhood_has_the_global_mix():
    # q = r / (1 + r) means f_d = f_s, so the posterior is the prior.
    for r, k_adj, nd in ((2.0, 13, 9), (1.0, 8, 4), (3.0, 6, 5)):
        assert math.isclose((nd + 1) / (k_adj + 2), r / (1 + r))
        for rho in (0.05, 0.2):
            assert math.isclose(bayes_score(nd, k_adj, rho, r), rho, rel_tol=1e-12)


def test_local_maxima_and_threshold():
    assert local_maxima([0, 2, 5, 3, 1, 4, 6, 2]) == [2, 6]
    assert local_maxima([1, 2, 3]) == []
    rng = random.Random(7)
    vals = [rng.gauss(0.1, 0.03) for _ in range(300)] + [rng.gauss(0.7, 0.05) for _ in range(150)]
    t = threshold_minimum(vals)
    assert 0.1 + 3 * 0.03 < t < 0.7 - 3 * 0.05   # inside the gap between the two modes
    with pytest.raises(ValueError):
        threshold_minimum([1.0, 1.0])
    assert call_doublets([0.1, 0.5, 0.3], 0.3) == [False, True, False]


def test_same_seed_same_scores():
    X, _ = cells(random.Random(8), 12)
    a = doublet_scores(X, random.Random(9))
    b = doublet_scores(X, random.Random(9))
    assert a == b


def test_errors():
    with pytest.raises(ValueError):
        doublet_scores([[1, 2], [3, 4]], random.Random(1))
    with pytest.raises(ValueError):
        doublet_scores([[1, 2]] * 5, random.Random(1), expected_rate=0.0)


def test_heterotypic_doublets_found_homotypic_missed_measured():
    """A measurement, not a theorem: 150 singlets of 3 types, 15 doublets of two types, 10 of one type."""
    rng = random.Random(1)
    X, lab = cells(rng, 50)
    n = len(X)
    het, homo = [], []
    for _ in range(15):
        a, b = rng.randrange(n), rng.randrange(n)
        while lab[b] == lab[a]:
            b = rng.randrange(n)
        het.append([x + y for x, y in zip(X[a], X[b])])
    for _ in range(10):
        a, b = rng.randrange(n), rng.randrange(n)
        while lab[b] != lab[a] or b == a:
            b = rng.randrange(n)
        homo.append([x + y for x, y in zip(X[a], X[b])])
    obs, sim = doublet_scores(X + het + homo, random.Random(101))
    single, s_het, s_homo = obs[:n], obs[n:n + 15], obs[n + 15:]
    assert auc(s_het, single) > 0.95
    assert auc(s_homo, single) < 0.8
    t = threshold_minimum(sim)
    calls = call_doublets(obs, t)
    assert sum(calls[n:n + 15]) >= 12
    assert sum(calls[:n]) <= 5
    assert sum(calls[n + 15:]) <= 3
