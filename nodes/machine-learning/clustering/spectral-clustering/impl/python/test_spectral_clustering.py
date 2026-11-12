# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/spectral-clustering/. The authors are listed in prov/FGDG1R.jsonl.

import math
import random
from fractions import Fraction

from spectral_clustering import (
    as_partition,
    degrees,
    epsilon_graph,
    gaussian_graph,
    jacobi_eigh,
    knn_graph,
    laplacian,
    spectral_clustering,
    spectral_embedding,
)

METHODS = ("unnormalized", "shi-malik", "njw")


def planted_graph(sizes, rng, integer=False):
    """A graph whose connected components are the given blocks: a random spanning
    path inside each block plus random extra edges, and no edge between blocks."""
    n = sum(sizes)
    perm = list(range(n))
    rng.shuffle(perm)
    blocks, start = [], 0
    for s in sizes:
        blocks.append(perm[start:start + s])
        start += s
    W = [[0] * n for _ in range(n)]

    def weight():
        return rng.randint(1, 5) if integer else rng.uniform(0.5, 2.0)

    for b in blocks:
        for u, v in zip(b, b[1:]):
            W[u][v] = W[v][u] = weight()
        for u in b:
            for v in b:
                if u < v and W[u][v] == 0 and rng.random() < 0.4:
                    W[u][v] = W[v][u] = weight()
    return W, {frozenset(b) for b in blocks}


def exact_rank(M):
    A = [[Fraction(x) for x in row] for row in M]
    rows, cols, r = len(A), len(A[0]), 0
    for c in range(cols):
        piv = next((i for i in range(r, rows) if A[i][c] != 0), None)
        if piv is None:
            continue
        A[r], A[piv] = A[piv], A[r]
        for i in range(rows):
            if i != r and A[i][c] != 0:
                f = A[i][c] / A[r][c]
                A[i] = [a - f * b for a, b in zip(A[i], A[r])]
        r += 1
    return r


def test_jacobi_against_definition():
    rng = random.Random(3)
    for n in (1, 2, 5, 8):
        A = [[0.0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i, n):
                A[i][j] = A[j][i] = rng.uniform(-3, 3)
        vals, V = jacobi_eigh(A)
        assert vals == sorted(vals)
        for j in range(n):
            for i in range(n):
                av = sum(A[i][t] * V[t][j] for t in range(n))
                assert abs(av - vals[j] * V[i][j]) < 1e-9
            for jj in range(n):
                dot = sum(V[t][j] * V[t][jj] for t in range(n))
                assert abs(dot - (1.0 if j == jj else 0.0)) < 1e-9


def test_zero_multiplicity_is_component_count_exactly():
    rng = random.Random(1)
    for sizes in ([4], [3, 3], [1, 2, 4], [2, 2, 2, 3], [5, 1, 1]):
        W, comps = planted_graph(sizes, rng, integer=True)
        n = len(W)
        L = laplacian(W)
        assert exact_rank(L) == n - len(comps)
        d = degrees(W)
        for comp in comps:
            ind = [1 if i in comp else 0 for i in range(n)]
            assert all(sum(Fraction(L[i][j]) * ind[j] for j in range(n)) == 0 for i in range(n))
            if all(x > 0 for x in d):  # L_rw 1_A = D^(-1) L 1_A = 0
                assert all(sum(Fraction(L[i][j], d[i]) * ind[j] for j in range(n)) == 0
                           for i in range(n))


def test_null_space_is_spanned_by_indicators():
    rng = random.Random(2)
    for sizes in ([3, 4], [2, 3, 4], [5, 2, 2, 2]):
        W, comps = planted_graph(sizes, rng)
        n, c = len(W), len(comps)
        d = degrees(W)
        for kind in ("unnormalized", "sym"):
            vals, V = jacobi_eigh(laplacian(W, kind))
            assert sum(1 for x in vals if abs(x) < 1e-9) == c
            assert vals[c] > 1e-6
            for j in range(c):
                v = [V[i][j] for i in range(n)]
                # v = D^(1/2) f for L_sym, v = f for L; f must be constant on each component
                f = [v[i] / math.sqrt(d[i]) if kind == "sym" else v[i] for i in range(n)]
                for comp in comps:
                    vals_on = [f[i] for i in comp]
                    assert max(vals_on) - min(vals_on) < 1e-8


def test_recovers_planted_components():
    rng = random.Random(4)
    for sizes in ([3, 4], [2, 3, 4], [4, 4, 2], [3, 3, 3, 3]):
        W, comps = planted_graph(sizes, rng)
        for m in METHODS:
            labels = spectral_clustering(W, len(sizes), m, random.Random(7))
            assert as_partition(labels) == comps, (sizes, m)
    # an isolated vertex: only the unnormalized Laplacian is defined
    W, comps = planted_graph([4, 4, 1], rng)
    assert as_partition(spectral_clustering(W, 3, "unnormalized", random.Random(7))) == comps
    try:
        spectral_clustering(W, 3, "njw")
        assert False
    except ValueError:
        pass


def test_three_blobs_with_each_similarity_graph():
    rng = random.Random(5)
    centers = [(0.0, 0.0), (6.0, 0.0), (0.0, 6.0)]
    pts, truth = [], {}
    for c, (cx, cy) in enumerate(centers):
        for _ in range(6):
            truth.setdefault(c, []).append(len(pts))
            pts.append((cx + rng.uniform(-1, 1), cy + rng.uniform(-1, 1)))
    want = {frozenset(v) for v in truth.values()}
    for W in (gaussian_graph(pts, 1.0), knn_graph(pts, 3), epsilon_graph(pts, 3.0)):
        for m in METHODS:
            assert as_partition(spectral_clustering(W, 3, m, random.Random(11))) == want


def test_graph_builders():
    rng = random.Random(6)
    pts = [(rng.random(), rng.random()) for _ in range(12)]
    a, b = knn_graph(pts, 3), knn_graph(pts, 3, mutual=True)
    for W in (a, b, epsilon_graph(pts, 0.3), gaussian_graph(pts, 0.5)):
        assert all(W[i][j] == W[j][i] for i in range(12) for j in range(12))
        assert all(W[i][i] == 0 for i in range(12))
    assert all(b[i][j] <= a[i][j] for i in range(12) for j in range(12))
    assert all(sum(row) >= 3 for row in a)


def test_njw_rows_have_unit_norm_and_shi_malik_solves_generalized_problem():
    rng = random.Random(8)
    W, _ = planted_graph([4, 5], rng)
    n = len(W)
    for row in spectral_embedding(W, 2, "njw"):
        assert abs(math.sqrt(sum(x * x for x in row)) - 1) < 1e-9
    L, d = laplacian(W), degrees(W)
    vals, _ = jacobi_eigh(laplacian(W, "sym"))
    U = spectral_embedding(W, 3, "shi-malik")
    for j in range(3):
        for i in range(n):
            lu = sum(L[i][t] * U[t][j] for t in range(n))
            assert abs(lu - vals[j] * d[i] * U[i][j]) < 1e-9
