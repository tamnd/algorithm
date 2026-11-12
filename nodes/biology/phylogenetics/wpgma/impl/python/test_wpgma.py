# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/wpgma/. The authors are listed in prov/76VTZ9.jsonl.

import random
from fractions import Fraction

import pytest

from wpgma import cophenetic, wpgma


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
    out = []
    for u, a, b, _ in merges:
        members[u] = members[a] | members[b]
        out.append(members[u])
    return out


def naive_wpgma(D):
    """Oracle: a leaf at depth t inside its cluster has weight 2^-t in every cluster distance."""
    n = len(D)
    clusters = [{i: Fraction(1)} for i in range(n)]
    out = []
    while len(clusters) > 1:
        best = None
        for x in range(len(clusters)):
            for y in range(x + 1, len(clusters)):
                v = sum(wa * wb * D[a][b] for a, wa in clusters[x].items() for b, wb in clusters[y].items())
                if best is None or v < best[0]:
                    best = (v, x, y)
        v, x, y = best
        merged = {a: w / 2 for a, w in clusters[x].items()}
        merged.update({b: w / 2 for b, w in clusters[y].items()})
        out.append((frozenset(merged), v / 2))
        clusters = [c for k, c in enumerate(clusters) if k not in (x, y)] + [merged]
    return out


def is_ultrametric(M):
    n = len(M)
    return all(M[x][z] <= max(M[x][y], M[y][z]) for x in range(n) for y in range(n) for z in range(n))


EXAMPLE = [[0, 9, 5, 3, 7], [9, 0, 7, 7, 8], [5, 7, 0, 2, 8], [3, 7, 2, 0, 9], [7, 8, 8, 9, 0]]


def test_example_from_page():
    m = wpgma(EXAMPLE)
    assert m == [(5, 2, 3, 1), (6, 0, 5, 2), (7, 4, 6, Fraction(31, 8)), (8, 1, 7, 4)]
    assert clusters_of(5, m)[2] == frozenset({0, 2, 3, 4})


def test_small_cases():
    assert wpgma([[0]]) == []
    assert wpgma([[0, 3], [3, 0]]) == [(2, 0, 1, Fraction(3, 2))]
    with pytest.raises(ValueError):
        wpgma([])


def test_random_ultrametric_recovered():
    rng = random.Random(61)
    for _ in range(500):
        n = rng.randint(1, 10)
        D, true = random_ultrametric(n, rng)
        m = wpgma(D)
        assert cophenetic(n, m) == D
        assert set(clusters_of(n, m)) == true


def test_ultrametric_with_equal_heights():
    rng = random.Random(67)
    for _ in range(300):
        n = rng.randint(2, 9)
        D, _ = random_ultrametric(n, rng, min_step=0)
        assert cophenetic(n, wpgma(D)) == D


def test_matches_dyadic_weight_oracle():
    rng = random.Random(71)
    for _ in range(300):
        n = rng.randint(2, 8)
        D = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                D[i][j] = D[j][i] = rng.randint(1, 10 ** 6)
        m = wpgma(D)
        assert list(zip(clusters_of(n, m), [h for _, _, _, h in m])) == naive_wpgma(D)


def test_output_is_always_ultrametric():
    rng = random.Random(73)
    for _ in range(300):
        n = rng.randint(2, 8)
        D = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                D[i][j] = D[j][i] = rng.randint(1, 20)
        m = wpgma(D)
        heights = [h for _, _, _, h in m]
        assert heights == sorted(heights)
        assert is_ultrametric(cophenetic(n, m))
