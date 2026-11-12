# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kernel-k-means/. The authors are listed in prov/8RTBTG.jsonl.

import itertools
import random
from fractions import Fraction as F

from kernel_k_means import kernel_k_means, kernel_matrix, objective


def dot(x, y):
    return sum(a * b for a, b in zip(x, y))


def poly2(x, y):
    return (dot(x, y) + 1) ** 2


def phi_poly2(x):
    """An explicit feature map of (x.y + 1)^2: all products u_i u_j with u = (x, 1)."""
    u = tuple(x) + (1,)
    return tuple(a * b for a in u for b in u)


def lloyd_from_labels(points, labels, k):
    """Plain Lloyd's algorithm on explicit vectors, started from labels, same tie rule."""
    a = list(labels)
    while True:
        cs = {}
        for c in range(k):
            m = [p for p, l in zip(points, a) if l == c]
            if m:
                cs[c] = tuple(sum(p[t] for p in m) / len(m) for t in range(len(points[0])))
        b = []
        for i, p in enumerate(points):
            dist = {c: sum((u - v) ** 2 for u, v in zip(p, cs[c])) for c in cs}
            best = min(dist.values())
            b.append(a[i] if dist[a[i]] == best else min(c for c in dist if dist[c] == best))
        if b == a:
            return a
        a = b


def test_ring_example() -> None:
    x = [(F(v),) for v in (-4, -3, -1, 0, 1, 3, 4)]
    K = kernel_matrix(x, lambda u, v: dot(u, v) ** 2)  # feature map x -> x^2
    start = [0, 0, 0, 1, 1, 1, 1]  # left and right, a fixed point of plain k-means
    labels, history = kernel_k_means(K, start, 2)
    assert labels == [0, 0, 1, 1, 1, 0, 0]  # outer {-4, -3, 3, 4} and inner {-1, 0, 1}
    assert history[-1] == F(2, 3) + 49


def test_matches_explicit_feature_map() -> None:
    rng = random.Random(10)
    for _ in range(60):
        n = rng.randrange(2, 9)
        k = rng.randrange(1, min(n, 3) + 1)
        x = [(F(rng.randrange(-3, 4)), F(rng.randrange(-3, 4))) for _ in range(n)]
        start = list(range(k)) + [rng.randrange(k) for _ in range(n - k)]
        rng.shuffle(start)
        K = kernel_matrix(x, poly2)
        feats = [phi_poly2(p) for p in x]
        for i in range(n):
            for j in range(n):
                assert K[i][j] == dot(feats[i], feats[j])
        got, history = kernel_k_means(K, start, k)
        assert got == lloyd_from_labels(feats, start, k)
        assert all(history[t + 1] < history[t] for t in range(len(history) - 1))
        assert all(h >= 0 for h in history)


def test_weighted_objective_is_normalized_cut_plus_constant() -> None:
    rng = random.Random(5)
    for _ in range(15):
        n = rng.randrange(3, 7)
        A = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                A[i][j] = A[j][i] = rng.randrange(0, 4)
            A[i][(i + 1) % n] = A[(i + 1) % n][i] = max(1, A[i][(i + 1) % n])  # no isolated vertex
        deg = [sum(r) for r in A]
        sigma = F(rng.randrange(0, 5))
        K = [[(sigma / deg[i] if i == j else 0) + F(A[i][j], deg[i] * deg[j]) for j in range(n)] for i in range(n)]
        for k in (2, 3):
            if k > n:
                continue
            const = None
            for lab in itertools.product(range(k), repeat=n):
                if len(set(lab)) < k:
                    continue
                ncut = sum(
                    F(sum(A[i][j] for i in range(n) if lab[i] == c for j in range(n) if lab[j] != c),
                      sum(deg[i] for i in range(n) if lab[i] == c))
                    for c in range(k)
                )
                diff = objective(K, lab, k, deg) - ncut
                const = diff if const is None else const
                assert diff == const
            assert const == n * sigma - k * sigma - k


def test_weighted_run_lowers_objective_with_psd_kernel() -> None:
    rng = random.Random(8)
    for _ in range(30):
        n = rng.randrange(2, 10)
        k = rng.randrange(1, min(n, 4) + 1)
        x = [(F(rng.randrange(-4, 5)), F(rng.randrange(-4, 5))) for _ in range(n)]
        w = [F(rng.randrange(1, 5)) for _ in range(n)]
        start = [rng.randrange(k) for _ in range(n)]
        K = kernel_matrix(x, poly2)
        labels, history = kernel_k_means(K, start, k, w)
        seq = [objective(K, start, k, w)] + history
        assert all(seq[t + 1] < seq[t] for t in range(len(seq) - 1))
