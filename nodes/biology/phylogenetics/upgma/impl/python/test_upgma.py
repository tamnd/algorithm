# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/upgma/. The authors are listed in prov/B7HW1Z.jsonl.

import random
from fractions import Fraction

import pytest

from upgma import cophenetic, upgma


def random_ultrametric(n, rng, min_step=1):
    """Random rooted binary tree with integer heights; returns (matrix 2 h(lca), clusters)."""
    clusters = [frozenset([i]) for i in range(n)]
    D = [[0] * n for _ in range(n)]
    h = 0
    out = set()
    while len(clusters) > 1:
        h += rng.randint(min_step, 4)
        a, b = rng.sample(range(len(clusters)), 2)
        A, B = clusters[a], clusters[b]
        for x in A:
            for y in B:
                D[x][y] = D[y][x] = 2 * h
        clusters = [c for k, c in enumerate(clusters) if k not in (a, b)] + [A | B]
        out.add(A | B)
    return D, out


def clusters_of(n, merges):
    members = {i: frozenset([i]) for i in range(n)}
    out = set()
    for u, a, b, _ in merges:
        members[u] = members[a] | members[b]
        out.add(members[u])
    return out


def naive_upgma(D):
    """Oracle: recompute every cluster distance as a plain average over the original matrix."""
    n = len(D)
    clusters = [frozenset([i]) for i in range(n)]
    out = []
    while len(clusters) > 1:
        best = None
        for x in range(len(clusters)):
            for y in range(x + 1, len(clusters)):
                A, B = clusters[x], clusters[y]
                avg = Fraction(sum(D[a][b] for a in A for b in B), len(A) * len(B))
                if best is None or avg < best[0]:
                    best = (avg, x, y)
        avg, x, y = best
        out.append((clusters[x] | clusters[y], avg / 2))
        clusters = [c for k, c in enumerate(clusters) if k not in (x, y)] + [clusters[x] | clusters[y]]
    return out


def is_ultrametric(M):
    n = len(M)
    return all(M[x][z] <= max(M[x][y], M[y][z]) for x in range(n) for y in range(n) for z in range(n))


ULTRA = [[0, 2, 10, 10, 10], [2, 0, 10, 10, 10], [10, 10, 0, 6, 6], [10, 10, 6, 0, 4], [10, 10, 6, 4, 0]]
NO_CLOCK = [[0, 6, 3, 6], [6, 0, 7, 10], [3, 7, 0, 5], [6, 10, 5, 0]]


def test_examples_from_page():
    assert upgma(ULTRA) == [(5, 0, 1, 1), (6, 3, 4, 2), (7, 2, 6, 3), (8, 5, 7, 5)]
    assert cophenetic(5, upgma(ULTRA)) == ULTRA
    m = upgma(NO_CLOCK)
    assert m == [(4, 0, 2, Fraction(3, 2)), (5, 3, 4, Fraction(11, 4)), (6, 1, 5, Fraction(23, 6))]
    assert frozenset({0, 1}) not in clusters_of(4, m)


def test_small_cases():
    assert upgma([[0]]) == []
    assert upgma([[0, 7], [7, 0]]) == [(2, 0, 1, Fraction(7, 2))]
    with pytest.raises(ValueError):
        upgma([])


def test_random_ultrametric_recovered():
    rng = random.Random(41)
    for _ in range(500):
        n = rng.randint(1, 10)
        D, true = random_ultrametric(n, rng)
        m = upgma(D)
        assert cophenetic(n, m) == D
        assert clusters_of(n, m) == true


def test_ultrametric_with_equal_heights():
    rng = random.Random(43)
    for _ in range(300):
        n = rng.randint(2, 9)
        D, _ = random_ultrametric(n, rng, min_step=0)
        assert cophenetic(n, upgma(D)) == D


def test_lance_williams_matches_plain_average():
    rng = random.Random(47)
    for _ in range(300):
        n = rng.randint(2, 8)
        D = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                D[i][j] = D[j][i] = rng.randint(1, 10 ** 6)
        got = [(c, h) for c, (_, _, _, h) in zip(clusters_in_order(n, upgma(D)), upgma(D))]
        assert got == naive_upgma(D)


def clusters_in_order(n, merges):
    members = {i: frozenset([i]) for i in range(n)}
    out = []
    for u, a, b, _ in merges:
        members[u] = members[a] | members[b]
        out.append(members[u])
    return out


def test_output_is_always_ultrametric():
    rng = random.Random(53)
    for _ in range(300):
        n = rng.randint(2, 8)
        D = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                D[i][j] = D[j][i] = rng.randint(1, 20)
        m = upgma(D)
        heights = [h for _, _, _, h in m]
        assert heights == sorted(heights)
        assert is_ultrametric(cophenetic(n, m))
