# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ho-kalman-algorithm/. The authors are listed in prov/A1602S.jsonl.

import random
from fractions import Fraction

from ctlmat import charpoly, mat_power, mul
from ho_kalman_algorithm import hankel, ho_kalman, independent_columns, markov_parameters


def _rank(a):
    return len(independent_columns(a))


def _ctrb(A, B):
    n = len(A)
    blocks = [mul(mat_power(A, k), B) for k in range(n)]
    return [sum((blk[i] for blk in blocks), []) for i in range(n)]


def _obsv(A, C):
    n = len(A)
    out = []
    for k in range(n):
        out.extend(mul(C, mat_power(A, k)))
    return out


def test_worked_example():
    q = Fraction
    h = [[[1]], [[2]], [[0]], [[q(1, 2)]], [[0]], [[q(1, 8)]]]
    assert hankel(h, 2, 2) == [[2, 0], [0, q(1, 2)]]
    A, B, C, D = ho_kalman(h, 2)
    assert A == [[0, q(1, 4)], [1, 0]]
    assert B == [[1], [0]]
    assert C == [[2, 0]]
    assert D == [[1]]
    assert charpoly(A) == [1, 0, q(-1, 4)]
    # h_k = (1/2)^(k-1) + (-1/2)^(k-1) holds beyond the data
    hk = markov_parameters(A, B, C, D, 10)
    for k in range(1, 11):
        assert hk[k] == [[q(1, 2) ** (k - 1) + q(-1, 2) ** (k - 1)]]


def _random_system(rng, n, m, p):
    A = [[Fraction(rng.randint(-4, 4), 4) for _ in range(n)] for _ in range(n)]
    B = [[rng.randint(-2, 2) for _ in range(m)] for _ in range(n)]
    C = [[rng.randint(-2, 2) for _ in range(n)] for _ in range(p)]
    D = [[rng.randint(-1, 1) for _ in range(m)] for _ in range(p)]
    return A, B, C, D


def test_random_mimo_exact():
    rng = random.Random(4)
    done = 0
    for _ in range(40):
        n, m, p = rng.randint(1, 4), rng.randint(1, 2), rng.randint(1, 2)
        A0, B0, C0, D0 = _random_system(rng, n, m, p)
        N = n
        h = markov_parameters(A0, B0, C0, D0, 2 * N)
        A, B, C, D = ho_kalman(h, N)
        # the order is the rank of the Hankel matrix, at most n
        n_min = _rank(hankel(h, N, N))
        assert len(A) == n_min <= n
        # all Markov parameters agree, also far beyond the 2N that were used
        assert markov_parameters(A, B, C, D, 3 * N + 4) == markov_parameters(A0, B0, C0, D0, 3 * N + 4)
        # a controllable and observable system gives the same order and the same poles
        if _rank(_ctrb(A0, B0)) == n and _rank(_obsv(A0, C0)) == n:
            assert len(A) == n
            assert charpoly(A) == charpoly(A0)
            done += 1
    assert done >= 10


def test_non_minimal_system_is_reduced():
    # the second state is not controllable, the third is not observable
    A = [[Fraction(1, 2), 0, 0], [0, Fraction(1, 3), 0], [0, 0, Fraction(-1, 5)]]
    B = [[1], [0], [1]]
    C = [[1, 1, 0]]
    D = [[0]]
    h = markov_parameters(A, B, C, D, 6)
    Ar, Br, Cr, Dr = ho_kalman(h, 3)
    assert Ar == [[Fraction(1, 2)]]
    assert markov_parameters(Ar, Br, Cr, Dr, 12) == markov_parameters(A, B, C, D, 12)


def test_too_few_block_rows_fails():
    # order 2, but N = 1: the result reproduces h_1 and h_2 only
    q = Fraction
    A0 = [[q(1, 2), 0], [0, q(-1, 2)]]
    B0 = [[1], [1]]
    C0 = [[1, 1]]
    D0 = [[0]]
    h = markov_parameters(A0, B0, C0, D0, 2)
    A, B, C, D = ho_kalman(h, 1)
    assert len(A) == 1
    assert A == [[0]]
    assert markov_parameters(A, B, C, D, 2) == h
    assert markov_parameters(A, B, C, D, 3)[3] == [[0]]
    assert markov_parameters(A0, B0, C0, D0, 3)[3] == [[Fraction(1, 2)]]


def test_independent_columns_against_brute_force():
    rng = random.Random(9)
    from itertools import combinations
    from ctlmat import det
    for _ in range(30):
        r, c = rng.randint(1, 4), rng.randint(1, 4)
        a = [[rng.randint(-1, 1) for _ in range(c)] for _ in range(r)]
        rank = 0
        for k in range(1, min(r, c) + 1):
            if any(det([[a[i][j] for j in cs] for i in rs]) != 0
                   for rs in combinations(range(r), k) for cs in combinations(range(c), k)):
                rank = k
        assert len(independent_columns(a)) == rank
