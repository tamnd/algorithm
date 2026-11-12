# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/parity-check-matrix/. The authors are listed in prov/TTGQBS.jsonl.

import random
from itertools import product

from parity_check_matrix import (
    min_dependent_columns,
    parity_check_from_systematic,
    parity_check_matrix,
    rank,
    syndrome,
)

G74 = [[1, 0, 0, 0, 1, 1, 0], [0, 1, 0, 0, 0, 1, 1], [0, 0, 1, 0, 1, 1, 1], [0, 0, 0, 1, 1, 0, 1]]
H74 = [[1, 0, 1, 1, 1, 0, 0], [1, 1, 1, 0, 0, 1, 0], [0, 1, 1, 1, 0, 0, 1]]


def span(g, q):
    k, n = len(g), len(g[0])
    return {tuple(sum(m[i] * g[i][j] for i in range(k)) % q for j in range(n)) for m in product(range(q), repeat=k)}


def min_weight(g, q):
    return min(sum(1 for x in c if x) for c in span(g, q) if any(c))


def test_hamming_example():
    assert parity_check_from_systematic(G74) == H74
    assert min_dependent_columns(H74) == 3
    assert syndrome(H74, [1, 0, 1, 1, 1, 0, 0]) == (0, 0, 0)
    assert syndrome(H74, [1, 0, 1, 1, 0, 0, 0]) == (1, 0, 0)


def test_ternary_minus_sign():
    g = [[1, 0, 1, 1], [0, 1, 1, 2]]
    h = parity_check_from_systematic(g, 3)
    assert h == [[2, 2, 1, 0], [2, 1, 0, 1]]
    for row in g:
        assert syndrome(h, row, 3) == (0, 0)
    # Without the minus sign the matrix is wrong over GF(3).
    bad = [[1, 1, 1, 0], [1, 2, 0, 1]]
    assert syndrome(bad, g[0], 3) != (0, 0)
    assert min_dependent_columns(h, 3) == 3


def test_repeated_column_gives_d2():
    h = [[1, 1, 0, 1], [0, 0, 1, 1]]
    assert min_dependent_columns(h) == 2
    g = [list(v) for v in product(range(2), repeat=4) if syndrome(h, v) == (0, 0) and any(v)]
    assert min(sum(v) for v in g) == 2


def test_zero_column_gives_d1():
    assert min_dependent_columns([[1, 0, 1], [0, 0, 1]]) == 1


def test_random_codes():
    rng = random.Random(21)
    done = 0
    while done < 200:
        q = rng.choice([2, 2, 3, 5])
        n = rng.randint(2, 9 if q == 2 else 6)
        k = rng.randint(1, n - 1)
        if q == 5:
            n, k = min(n, 5), min(k, 3)
            if k >= n:
                continue
        g = [[rng.randrange(q) for _ in range(n)] for _ in range(k)]
        if rank(g, q) < k:
            continue
        h = parity_check_matrix(g, q)
        assert len(h) == n - k and rank(h, q) == n - k
        for row in g:
            assert syndrome(h, row, q) == (0,) * (n - k)
        code = span(g, q)
        for v in product(range(q), repeat=n):
            assert (syndrome(h, v, q) == (0,) * (n - k)) == (v in code)
        assert min_dependent_columns(h, q) == min_weight(g, q)
        done += 1
