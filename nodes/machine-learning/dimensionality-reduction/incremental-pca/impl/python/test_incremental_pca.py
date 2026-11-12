# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/incremental-pca/. The authors are listed in prov/0NPZBY.jsonl.

import math
import random

import pytest

from incremental_pca import IncrementalPCA, one_sided_jacobi, orth

EXAMPLE = [(13, 11, 9), (9, 15, 7), (5, 7, 17), (1, 11, 15), (7, -1, -3), (3, 3, -5), (-1, -5, 5), (-5, -1, 3)]


def batch_pca(x):
    """Oracle: eigenpairs of the covariance (divisor n) by the cyclic Jacobi eigenvalue method."""
    n, d = len(x), len(x[0])
    mu = [sum(r[j] for r in x) / n for j in range(d)]
    m = [[sum((r[a] - mu[a]) * (r[b] - mu[b]) for r in x) / n for b in range(d)] for a in range(d)]
    v = [[float(i == j) for j in range(d)] for i in range(d)]
    for _ in range(50):
        for p in range(d - 1):
            for q in range(p + 1, d):
                if abs(m[p][q]) < 1e-300:
                    continue
                th = (m[q][q] - m[p][p]) / (2 * m[p][q])
                t = math.copysign(1.0, th) / (abs(th) + math.sqrt(th * th + 1))
                c = 1 / math.sqrt(t * t + 1)
                s = t * c
                for r in range(d):
                    m[r][p], m[r][q] = c * m[r][p] - s * m[r][q], s * m[r][p] + c * m[r][q]
                    v[r][p], v[r][q] = c * v[r][p] - s * v[r][q], s * v[r][p] + c * v[r][q]
                for r in range(d):
                    m[p][r], m[q][r] = c * m[p][r] - s * m[q][r], s * m[p][r] + c * m[q][r]
    order = sorted(range(d), key=lambda j: -m[j][j])
    return mu, [m[j][j] for j in order], [[v[r][j] for r in range(d)] for j in order]


def same_up_to_sign(a, b, tol):
    dot = sum(x * y for x, y in zip(a, b))
    return abs(abs(dot) - 1.0) < tol


def random_data(rng, n, d, scales):
    mix = [[rng.gauss(0, 1) for _ in range(d)] for _ in range(d)]
    rows = []
    for _ in range(n):
        g = [scales[j] * rng.gauss(0, 1) for j in range(d)]
        rows.append([sum(mix[i][j] * g[j] for j in range(d)) + 5.0 * i for i in range(d)])
    return rows


def feed(ipca, x, sizes):
    start = 0
    for m in sizes:
        if start >= len(x):
            break
        ipca.update(x[start:start + m])
        start += m
    if start < len(x):
        ipca.update(x[start:])
    return ipca


def test_worked_example():
    for k in (3, 2):
        ipca = feed(IncrementalPCA(3, k), EXAMPLE, [3, 3, 2])
        assert ipca.n == 8
        assert all(abs(a - b) < 1e-12 for a, b in zip(ipca.mean, [4, 5, 6]))
        assert all(abs(a - b) < 1e-9 for a, b in zip(ipca.eigenvalues(), [81, 36, 9][:k]))
        for u, want in zip(ipca.components(), [(1, 2, 2), (2, 1, -2), (2, -2, 1)]):
            assert same_up_to_sign(u, [t / 3 for t in want], 1e-9)


@pytest.mark.parametrize("seed", [1, 2, 3])
def test_full_rank_equals_batch_pca(seed):
    rng = random.Random(seed)
    x = random_data(rng, 41, 5, [4.0, 2.5, 1.5, 1.0, 0.5])
    sizes = [rng.randint(1, 7) for _ in range(20)]
    ipca = feed(IncrementalPCA(5, 5), x, sizes)
    mu, values, vectors = batch_pca(x)
    assert ipca.n == 41
    assert all(abs(a - b) < 1e-9 for a, b in zip(ipca.mean, mu))
    assert all(abs(a - b) < 1e-8 * values[0] for a, b in zip(ipca.eigenvalues(), values))
    for u, v in zip(ipca.components(), vectors):
        assert same_up_to_sign(u, v, 1e-8)


def test_truncation_is_exact_for_low_rank_data():
    rng = random.Random(4)
    # rank 2 data plus a mean: k = 2 loses nothing at any step
    x = random_data(rng, 30, 6, [3.0, 1.0, 0, 0, 0, 0])
    ipca = feed(IncrementalPCA(6, 2), x, [1, 4, 2, 9, 5])
    mu, values, vectors = batch_pca(x)
    assert all(abs(a - b) < 1e-8 * values[0] for a, b in zip(ipca.eigenvalues(), values[:2]))
    for u, v in zip(ipca.components(), vectors[:2]):
        assert same_up_to_sign(u, v, 1e-8)
    z = ipca.transform(x[:3])
    rec = [[ipca.mean[i] + sum(zz[j] * ipca.u[j][i] for j in range(2)) for i in range(6)] for zz in z]
    assert all(abs(a - b) < 1e-8 for r, s in zip(rec, x[:3]) for a, b in zip(r, s))


def test_truncation_on_decaying_spectrum_is_close():
    rng = random.Random(5)
    x = random_data(rng, 200, 6, [10.0, 6.0, 0.3, 0.2, 0.1, 0.05])
    ipca = feed(IncrementalPCA(6, 2), x, [10] * 20)
    mu, values, vectors = batch_pca(x)
    for got, want in zip(ipca.eigenvalues(), values[:2]):
        assert abs(got - want) < 0.01 * want
    for u, v in zip(ipca.components(), vectors[:2]):
        assert same_up_to_sign(u, v, 1e-3)


def test_forgetting_factor_follows_recent_data():
    ipca = IncrementalPCA(2, 1, forget=0.5)
    ipca.update([(t, 0.0) for t in (-3, -1, 1, 3)])
    for _ in range(10):
        ipca.update([(0.0, t) for t in (-1, 1)])
    u = ipca.components()[0]
    assert abs(u[1]) > 0.99
    assert abs(ipca.n - 4.0) < 0.01  # n tends to m / (1 - f) = 4


def test_helpers():
    a = [[3.0, 1.0], [1.0, 3.0], [0.0, 2.0]]
    v, s = one_sided_jacobi(a)
    av = [[sum(a[i][t] * v[j][t] for t in range(2)) for j in range(2)] for i in range(3)]
    assert abs(sum(av[i][0] * av[i][1] for i in range(3))) < 1e-12
    assert abs(sum(t * t for t in s) - sum(x * x for r in a for x in r)) < 1e-12
    basis = orth([[1.0, 0.0, 0.0], [2.0, 0.0, 0.0], [1.0, 1.0, 0.0]], 1.0)
    assert len(basis) == 2
