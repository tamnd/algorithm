# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/apsp-negative-triangle-equivalence/. The authors are listed in prov/ZT8VGE.jsonl.

import random
from math import ceil, log2

from apsp_negative_triangle_equivalence import (
    all_pairs_negative_triangle,
    apsp_via_min_plus,
    find_negative_triangle,
    min_plus_via_apsp,
    min_plus_via_negative_triangle,
    negative_triangle_via_min_plus,
    search_rounds,
    tripartite_copy,
)

SEED = 20261116


class Detector:
    """Brute-force negative triangle detection that counts its calls."""

    def __init__(self):
        self.calls = 0

    def __call__(self, A, B, D, I, J, K):
        self.calls += 1
        for i in I:
            for j in J:
                a = A[i][j]
                if a is None:
                    continue
                for k in K:
                    b, d = B[j][k], D[i][k]
                    if b is not None and d is not None and a + b + d < 0:
                        return True
        return False


def brute_pairs(A, B, D):
    return {
        (i, k)
        for i in range(len(A))
        for k in range(len(D[0]) if D else 0)
        for j in range(len(B))
        if A[i][j] is not None and B[j][k] is not None and D[i][k] is not None
        and A[i][j] + B[j][k] + D[i][k] < 0
    }


def brute_min_plus(A, B):
    nK = len(B[0]) if B else 0
    out = []
    for row in A:
        cells = []
        for k in range(nK):
            vals = [a + B[j][k] for j, a in enumerate(row) if a is not None and B[j][k] is not None]
            cells.append(min(vals) if vals else None)
        out.append(cells)
    return out


def floyd_warshall(W):
    n = len(W)
    d = [[0 if i == j else W[i][j] for j in range(n)] for i in range(n)]
    for m in range(n):
        for i in range(n):
            if d[i][m] is None:
                continue
            for j in range(n):
                if d[m][j] is not None and (d[i][j] is None or d[i][m] + d[m][j] < d[i][j]):
                    d[i][j] = d[i][m] + d[m][j]
    return d


def rand_matrix(rng, rows, cols, lo, hi, p_missing):
    return [[None if rng.random() < p_missing else rng.randint(lo, hi) for _ in range(cols)] for _ in range(rows)]


def test_find_returns_a_negative_triangle():
    rng = random.Random(SEED)
    found = 0
    for _ in range(300):
        nI, nJ, nK = rng.randint(1, 7), rng.randint(1, 7), rng.randint(1, 7)
        A = rand_matrix(rng, nI, nJ, -6, 6, 0.2)
        B = rand_matrix(rng, nJ, nK, -6, 6, 0.2)
        D = rand_matrix(rng, nI, nK, -6, 6, 0.2)
        det = Detector()
        I, J, K = list(range(nI)), list(range(nJ)), list(range(nK))
        if not det(A, B, D, I, J, K):
            continue
        found += 1
        i, j, k = find_negative_triangle(A, B, D, I, J, K, det)
        assert A[i][j] + B[j][k] + D[i][k] < 0
        rounds = ceil(log2(max(nI, nJ, nK)))
        assert det.calls <= 1 + 8 * rounds
    assert found > 100


def test_all_pairs_against_brute_force():
    rng = random.Random(SEED + 1)
    for _ in range(250):
        nI, nJ, nK = rng.randint(1, 9), rng.randint(1, 9), rng.randint(1, 9)
        A = rand_matrix(rng, nI, nJ, -8, 8, 0.15)
        B = rand_matrix(rng, nJ, nK, -8, 8, 0.15)
        D = rand_matrix(rng, nI, nK, -8, 8, 0.15)
        before = [row[:] for row in D]
        assert all_pairs_negative_triangle(A, B, D, Detector()) == brute_pairs(A, B, D)
        assert D == before


def test_call_count_bound():
    # Every call at line L10 ends a triple or comes before one deletion, and
    # each search for a triangle makes at most 8 calls per round.
    rng = random.Random(SEED + 2)
    for n in (8, 27, 30):
        A = rand_matrix(rng, n, n, -10, 10, 0.0)
        B = rand_matrix(rng, n, n, -10, 10, 0.0)
        D = rand_matrix(rng, n, n, -10, 10, 0.0)
        det = Detector()
        Y = all_pairs_negative_triangle(A, B, D, det)
        assert Y == brute_pairs(A, B, D)
        s = 1
        while s ** 3 < n:
            s += 1
        g = ceil(n / s)
        assert det.calls <= g ** 3 + len(Y) * (1 + 8 * ceil(log2(s)))


def test_min_plus_against_brute_force():
    rng = random.Random(SEED + 3)
    for _ in range(80):
        nI, nJ, nK = rng.randint(1, 5), rng.randint(1, 5), rng.randint(1, 5)
        A = rand_matrix(rng, nI, nJ, -9, 9, 0.2)
        B = rand_matrix(rng, nJ, nK, -9, 9, 0.2)
        assert min_plus_via_negative_triangle(A, B, Detector()) == brute_min_plus(A, B)


def test_negative_triangle_via_min_plus():
    rng = random.Random(SEED + 4)
    for _ in range(300):
        n = rng.randint(1, 6)
        A = rand_matrix(rng, n, n, -5, 5, 0.2)
        B = rand_matrix(rng, n, n, -5, 5, 0.2)
        D = rand_matrix(rng, n, n, -5, 5, 0.2)
        expect = bool(brute_pairs(A, B, D))
        assert negative_triangle_via_min_plus(A, B, D, brute_min_plus) == expect


def test_apsp_round_trip():
    # Graphs with potentials have negative edges but no negative cycle.
    rng = random.Random(SEED + 5)
    for _ in range(40):
        n = rng.randint(1, 6)
        p = [rng.randint(-5, 5) for _ in range(n)]
        W = [[None if i == j or rng.random() < 0.4 else rng.randint(0, 6) + p[i] - p[j]
              for j in range(n)] for i in range(n)]
        expect = floyd_warshall(W)
        det = Detector()
        assert apsp_via_min_plus(W, lambda X, Y: min_plus_via_negative_triangle(X, Y, det)) == expect
        A = rand_matrix(rng, n, n, -7, 7, 0.2)
        B = rand_matrix(rng, n, n, -7, 7, 0.2)
        assert min_plus_via_apsp(A, B, floyd_warshall) == brute_min_plus(A, B)


def test_tripartite_copy_of_a_directed_graph():
    rng = random.Random(SEED + 6)
    for _ in range(300):
        n = rng.randint(1, 6)
        W = rand_matrix(rng, n, n, -4, 6, 0.4)
        expect = any(
            len({i, j, k}) == 3 and None not in (W[i][j], W[j][k], W[k][i])
            and W[i][j] + W[j][k] + W[k][i] < 0
            for i in range(n) for j in range(n) for k in range(n)
        )
        A, B, D = tripartite_copy(W)
        assert Detector()(A, B, D, list(range(n)), list(range(n)), list(range(n))) == expect


def test_page_example():
    W = [
        [None, 2, 4, None],
        [None, None, -3, 1],
        [-1, None, None, 2],
        [-2, None, None, None],
    ]
    A, B, D = tripartite_copy(W)
    assert brute_pairs(A, B, D) == {(0, 2), (1, 0), (2, 1)}
    assert brute_min_plus(A, B)[0][2] == -1
    assert negative_triangle_via_min_plus(A, B, D, brute_min_plus)
    A = [[3, -2, 0], [1, 4, -5], [-1, 2, 2]]
    B = [[0, 5, -3], [2, -4, 1], [4, 0, 3]]
    det = Detector()
    assert min_plus_via_negative_triangle(A, B, det) == [[0, -6, -1], [-1, -5, -2], [-1, -2, -4]]
    assert search_rounds(5) == 5
