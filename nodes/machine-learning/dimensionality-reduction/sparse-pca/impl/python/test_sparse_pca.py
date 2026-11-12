# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sparse-pca/. The authors are listed in prov/JKAB4E.jsonl.

import math
import random
from itertools import combinations

from sparse_pca import best_of_starts, brute_force, covariance, default_start, deflate, jacobi_eigen, matvec, quad, sparse_pca, tpower

EXAMPLE = [(13, 11, 9), (9, 15, 7), (5, 7, 17), (1, 11, 15), (7, -1, -3), (3, 3, -5), (-1, -5, 5), (-5, -1, 3)]


def spiked(rng, d, k, beta, m):
    """beta v v^T + W W^T / m with a k-sparse unit spike v and Gaussian noise W (d x m)."""
    support = rng.sample(range(d), k)
    v = [0.0] * d
    for i in support:
        v[i] = rng.choice((-1.0, 1.0)) / math.sqrt(k)
    w = [[rng.gauss(0, 1) for _ in range(m)] for _ in range(d)]
    return [[beta * v[i] * v[j] + sum(a * b for a, b in zip(w[i], w[j])) / m for j in range(d)] for i in range(d)]


def test_worked_example():
    a = covariance(EXAMPLE)
    assert a == [[29, 22, 4], [22, 44, 26], [4, 26, 53]]
    x, val, _ = tpower(a, 2, default_start(a, 2))
    assert abs(val - (97 + math.sqrt(2785)) / 2) < 1e-9
    assert x[0] == 0.0
    # from e_1 the method stops at the local optimum on the support {1, 2}
    x, val, _ = tpower(a, 2, [1, 0, 0])
    assert x[2] == 0.0 and abs(val - (73 + math.sqrt(2161)) / 2) < 1e-9


def test_value_never_decreases():
    rng = random.Random(1)
    for _ in range(20):
        a = spiked(rng, 8, 3, 2.0, 6)
        for k in (1, 2, 3, 5):
            start = [rng.gauss(0, 1) for _ in range(8)]
            x, val, hist = tpower(a, k, start)
            assert all(h2 >= h1 - 1e-12 for h1, h2 in zip(hist, hist[1:]))
            assert sum(1 for t in x if t != 0.0) <= k
            assert abs(sum(t * t for t in x) - 1) < 1e-12


def test_full_cardinality_is_power_iteration():
    rng = random.Random(2)
    a = spiked(rng, 6, 2, 5.0, 10)
    vals, _ = jacobi_eigen(a)
    _, val, _ = tpower(a, 6, [1.0] * 6)
    assert abs(val - max(vals)) < 1e-9


def test_matches_brute_force_on_spiked_instances():
    rng = random.Random(3)
    for trial in range(15):
        d, k = 8, rng.choice((2, 3, 4))
        a = spiked(rng, d, k, 4.0, 20)
        _, exact = brute_force(a, k)
        x, val = best_of_starts(a, k)
        assert val <= exact + 1e-9
        assert abs(val - exact) < 1e-9, trial
        assert abs(quad(a, x) - val) < 1e-9


def test_never_beats_brute_force_on_random_psd():
    rng = random.Random(4)
    for _ in range(15):
        d = 7
        w = [[rng.gauss(0, 1) for _ in range(3)] for _ in range(d)]
        a = [[sum(p * q for p, q in zip(w[i], w[j])) for j in range(d)] for i in range(d)]
        for k in (2, 3):
            _, exact = brute_force(a, k)
            _, val, _ = tpower(a, k, [rng.gauss(0, 1) for _ in range(d)])
            assert val <= exact + 1e-9


def test_clique_reduction():
    # max over k-sparse unit x of x^T (Adj + c I) x equals k - 1 + c exactly when a k-clique exists
    rng = random.Random(5)
    n, k = 8, 4
    for planted in (True, False):
        while True:
            edges = {(i, j) for i, j in combinations(range(n), 2) if rng.random() < 0.4}
            if planted:
                edges |= set(combinations(sorted(rng.sample(range(n), k)), 2))
            has = any(all(e in edges for e in combinations(s, 2)) for s in combinations(range(n), k))
            if has == planted:
                break
        adj = [[1.0 if (min(i, j), max(i, j)) in edges else 0.0 for j in range(n)] for i in range(n)]
        c = max(sum(row) for row in adj)
        m = [[adj[i][j] + (c if i == j else 0.0) for j in range(n)] for i in range(n)]
        _, exact = brute_force(m, k)
        assert (abs(exact - (k - 1 + c)) < 1e-9) == planted
        assert exact <= k - 1 + c + 1e-9


def test_projection_deflation():
    a = covariance(EXAMPLE)
    comps, values = sparse_pca(a, 2, 2)
    a2 = deflate(a, comps[0])
    assert all(abs(t) < 1e-9 for t in matvec(a2, comps[0]))
    assert abs(quad(a2, comps[1]) - values[1]) < 1e-9
    assert values[0] >= values[1]
    assert all(sum(1 for t in c if abs(t) > 1e-12) <= 2 for c in comps)
    # sparse components need not be orthogonal: here the inner product is about 0.29
    assert abs(sum(p * q for p, q in zip(*comps))) > 0.1
