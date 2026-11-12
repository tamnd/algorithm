# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/slink/. The authors are listed in prov/5KYFGE.jsonl.

import math
import random
from fractions import Fraction

from slink import pointer_to_merges, slink


def naive_single_linkage(D):
    """The O(n^3) greedy method: merge the two clusters with the least
    minimum member distance, recomputed from the members at each step."""
    clusters = [frozenset([i]) for i in range(len(D))]
    out = []
    while len(clusters) > 1:
        h, x, y = min(
            (min(D[i][j] for i in clusters[x] for j in clusters[y]), x, y)
            for x in range(len(clusters))
            for y in range(x + 1, len(clusters))
        )
        out.append(h)
        clusters = [c for t, c in enumerate(clusters) if t not in (x, y)] + [clusters[x] | clusters[y]]
    return out


def minimax(D):
    """Single-linkage cophenetic distances as minimax path lengths (Floyd-Warshall)."""
    n = len(D)
    U = [list(r) for r in D]
    for k in range(n):
        for i in range(n):
            for j in range(n):
                U[i][j] = min(U[i][j], max(U[i][k], U[k][j]))
    return U


def cophenetic(n, merges):
    sets = [[i] for i in range(n)]
    C = [[0] * n for _ in range(n)]
    for a, b, h, _ in merges:
        for i in sets[a]:
            for j in sets[b]:
                C[i][j] = C[j][i] = h
        sets.append(sets[a] + sets[b])
    return C


def check_pointer(D, pi, lam):
    """The definition of the pointer representation, checked from minimax distances."""
    n = len(D)
    U = minimax(D)
    for i in range(n - 1):
        assert lam[i] == min(U[i][j] for j in range(i + 1, n))
        assert pi[i] == max(j for j in range(n) if U[i][j] <= lam[i])
    if n:
        assert pi[n - 1] == n - 1 and lam[n - 1] == math.inf


def test_worked_example():
    xs = [0, 2, 3, 7, 13, 21]
    pi, lam = slink(6, lambda i, j: abs(xs[i] - xs[j]))
    assert pi == [2, 2, 3, 4, 5, 5]
    assert lam == [2, 1, 4, 6, 8, math.inf]
    assert [h for _, _, h, _ in pointer_to_merges(pi, lam)] == [1, 2, 4, 6, 8]


def test_edges():
    assert slink(0, lambda i, j: 0) == ([], [])
    assert slink(1, lambda i, j: 0) == ([0], [math.inf])
    assert pointer_to_merges(*slink(2, lambda i, j: 5)) == [(0, 1, 5, 2)]


def test_each_pair_read_once():
    calls = []
    slink(7, lambda i, j: calls.append((i, j)) or abs(i - j))
    assert sorted(calls) == sorted((i, j) for j in range(7) for i in range(j))


def test_against_naive_with_ties():
    rng = random.Random(13)
    for _ in range(600):
        n = rng.randrange(0, 9)
        D = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                D[i][j] = D[j][i] = rng.randrange(1, 6)
        pi, lam = slink(n, lambda i, j: D[i][j])
        check_pointer(D, pi, lam)
        merges = pointer_to_merges(pi, lam)
        assert [h for _, _, h, _ in merges] == naive_single_linkage(D)
        assert cophenetic(n, merges) == minimax(D)


def test_points_in_the_plane():
    rng = random.Random(5)
    for _ in range(200):
        n = rng.randrange(2, 12)
        P = [(Fraction(rng.randrange(-50, 51)), Fraction(rng.randrange(-50, 51))) for _ in range(n)]
        D = [[(p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2 for q in P] for p in P]
        pi, lam = slink(n, lambda i, j: D[i][j])
        assert [h for _, _, h, _ in pointer_to_merges(pi, lam)] == naive_single_linkage(D)
