# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/normalized-cut/. The authors are listed in prov/HDGW2G.jsonl.

import random
from fractions import Fraction

from normalized_cut import (
    bipartitions,
    brute_force_min,
    fiedler_generalized,
    ncut,
    normalized_cut_bipartition,
    ratio_cut,
    recursive_ncut,
    sweep_cut,
    volume,
    cut_value,
)


def graph(n, edges):
    W = [[0] * n for _ in range(n)]
    for u, v, w in edges:
        W[u][v] = W[v][u] = w
    return W


G1 = graph(6, [(0, 4, 1), (1, 2, 3), (1, 3, 3), (2, 4, 3), (4, 5, 2)])
G2 = graph(6, [(0, 1, 1), (0, 3, 2), (1, 5, 2), (2, 4, 3), (2, 5, 3), (3, 4, 2), (3, 5, 2), (4, 5, 3)])


def random_connected(n, rng):
    W = [[0] * n for _ in range(n)]
    perm = list(range(n))
    rng.shuffle(perm)
    for u, v in zip(perm, perm[1:]):
        W[u][v] = W[v][u] = rng.randint(1, 4)
    for i in range(n):
        for j in range(i + 1, n):
            if W[i][j] == 0 and rng.random() < 0.3:
                W[i][j] = W[j][i] = rng.randint(1, 4)
    return W


def laplacian_forms(W, y):
    n = len(W)
    d = [sum(r) for r in W]
    yLy = sum(W[i][j] * (y[i] - y[j]) ** 2 for i in range(n) for j in range(i + 1, n))
    yDy = sum(d[i] * y[i] * y[i] for i in range(n))
    return yLy, yDy, sum(d[i] * y[i] for i in range(n))


def test_rayleigh_quotient_identities_exactly():
    rng = random.Random(1)
    for _ in range(30):
        n = rng.randint(3, 7)
        W = random_connected(n, rng)
        for A, B in bipartitions(n):
            sA = set(A)
            b = Fraction(volume(W, A), volume(W, B))
            y = [Fraction(1) if i in sA else -b for i in range(n)]
            yLy, yDy, yD1 = laplacian_forms(W, y)
            assert yD1 == 0
            assert yLy / yDy == ncut([[Fraction(x) for x in r] for r in W], A, B)
            f = [Fraction(len(B)) if i in sA else Fraction(-len(A)) for i in range(n)]
            fLf = sum(W[i][j] * (f[i] - f[j]) ** 2 for i in range(n) for j in range(i + 1, n))
            assert sum(f) == 0
            WF = [[Fraction(x) for x in r] for r in W]
            assert fLf / sum(x * x for x in f) == ratio_cut(WF, A, B)


def test_relaxation_is_a_lower_bound_and_sweep_is_feasible():
    rng = random.Random(2)
    for _ in range(60):
        n = rng.randint(3, 8)
        W = random_connected(n, rng)
        best, _, _ = brute_force_min(W, ncut)
        lam2, y = fiedler_generalized(W)
        A, B = sweep_cut(W, y)
        assert lam2 <= best + 1e-9
        assert ncut(W, A, B) >= best - 1e-9
        # Cheeger sweep bound: conductance <= sqrt(2 lam2), and Ncut <= 2 conductance
        assert ncut(W, A, B) <= 2 * (2 * lam2) ** 0.5 + 1e-9
        assert ncut(W, A, B) <= 2 * (2 * best) ** 0.5 + 1e-9
        assert sorted(A + B) == list(range(n)) and A and B


def test_generalized_eigenvector():
    lam, y = fiedler_generalized(G1)
    d = [sum(r) for r in G1]
    for i in range(6):
        Ly = d[i] * y[i] - sum(G1[i][j] * y[j] for j in range(6))
        assert abs(Ly - lam * d[i] * y[i]) < 1e-9
    assert abs(lam - (1 - 2 ** -0.5)) < 1e-9
    assert abs(sum(d[i] * y[i] for i in range(6))) < 1e-9


def test_worked_examples():
    F = [[Fraction(x) for x in r] for r in G1]
    assert brute_force_min(F, ncut)[0] == Fraction(8, 15)
    v, A, B = brute_force_min(F, ratio_cut)
    assert (v, A) == (Fraction(6, 5), [0])
    assert ncut(F, A, B) == Fraction(24, 23)
    A, B = normalized_cut_bipartition(G1)
    assert ncut(F, A, B) == Fraction(8, 15)
    # on G2 the sweep cut misses the optimum
    F2 = [[Fraction(x) for x in r] for r in G2]
    assert brute_force_min(F2, ncut)[:2] == (Fraction(20, 27), [0, 3])
    A, B = normalized_cut_bipartition(G2)
    assert (A, B) == ([0, 1, 3], [2, 4, 5])
    assert ncut(F2, A, B) == Fraction(3, 4)


def test_two_cliques_with_a_bridge_are_found():
    for a, b in ((3, 3), (3, 5), (4, 6)):
        n = a + b
        W = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if i != j and (i < a) == (j < a):
                    W[i][j] = 1
        W[a - 1][a] = W[a][a - 1] = 1
        A, B = normalized_cut_bipartition(W)
        assert {tuple(A), tuple(B)} == {tuple(range(a)), tuple(range(a, n))}
        assert ncut(W, A, B) == brute_force_min(W, ncut)[0]


def test_recursive_ncut():
    rng = random.Random(3)
    blocks = [list(range(0, 4)), list(range(4, 9)), list(range(9, 13))]
    n = 13
    W = [[0.0] * n for _ in range(n)]
    for bl in blocks:
        for i in bl:
            for j in bl:
                if i < j:
                    W[i][j] = W[j][i] = rng.uniform(2, 3)
    for u, v in ((3, 4), (8, 9), (0, 12)):
        W[u][v] = W[v][u] = 0.1
    assert recursive_ncut(W, 0.2) == blocks
    assert recursive_ncut(W, 0.0) == [list(range(n))]
    # disconnected parts are split first
    W2 = graph(5, [(0, 1, 1), (2, 3, 1), (3, 4, 1)])
    assert recursive_ncut(W2, 0.0) == [[0, 1], [2, 3, 4]]


def test_cut_counts():
    assert sum(1 for _ in bipartitions(6)) == 31
    assert cut_value(G1, [0, 4, 5], [1, 2, 3]) == 3
