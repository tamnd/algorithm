# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dixon-p-adic-lifting/. The authors are listed in prov/YG36BM.jsonl.

import random
from fractions import Fraction
from itertools import permutations

from dixon_p_adic_lifting import dixon_solve, inverse_mod_p, rational_reconstruction

SMALL_PRIMES = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]


def det_leibniz(a):
    n = len(a)
    total = 0
    for p in permutations(range(n)):
        inv = sum(1 for i in range(n) for j in range(i + 1, n) if p[i] > p[j])
        t = 1
        for i in range(n):
            t *= a[p[i]][i]
        total += -t if inv % 2 else t
    return total


def check(a, b, x):
    n = len(a)
    assert all(sum(a[i][j] * x[j] for j in range(n)) == b[i] for i in range(n))
    d = det_leibniz(a)
    assert all((x[j] * d).denominator == 1 for j in range(n))  # Cramer: det(A) x is integral


def test_example() -> None:
    m = [[2, 1, 0], [1, 3, 1], [0, 1, 4]]
    assert dixon_solve(m, [1, 0, 7]) == [1, -1, 2]
    assert dixon_solve(m, [1, 2, 3], primes=[7]) == [Fraction(1, 3), Fraction(1, 3), Fraction(2, 3)]


def test_edges() -> None:
    assert dixon_solve([], []) == []
    assert dixon_solve([[3]], [2]) == [Fraction(2, 3)]
    assert dixon_solve([[0]], [1]) is None
    assert dixon_solve([[1, 2], [2, 4]], [1, 2]) is None
    assert dixon_solve([[0, 1], [1, 0]], [5, 7]) == [7, 5]  # needs a swap modulo p
    assert dixon_solve([[1, 0], [0, 0]], [0, 0], primes=SMALL_PRIMES) is None
    assert dixon_solve([[2, 0], [0, 3]], [0, 0]) == [0, 0]


def test_unlucky_primes() -> None:
    # det = 3 * 5 * 7 = 105, so the first three primes divide the determinant
    a = [[3, 0, 0], [1, 5, 0], [2, 4, 7]]
    for _ in range(3):
        assert inverse_mod_p(a, 3) is None
    x = dixon_solve(a, [1, 1, 1], primes=SMALL_PRIMES)
    check(a, [1, 1, 1], x)


def test_rational_reconstruction() -> None:
    m = 10007
    for s in range(-30, 31):
        for t in range(1, 31):
            if Fraction(s, t).denominator != t:
                continue
            u = s * pow(t, -1, m) % m
            assert rational_reconstruction(u, m, 30, 30) == Fraction(s, t)


def test_random() -> None:
    rng = random.Random(1982)
    for trial in range(600):
        n = rng.randint(1, 5)
        a = [[rng.randint(-6, 6) for _ in range(n)] for _ in range(n)]
        if rng.random() < 0.15:
            a[rng.randrange(n)] = [0] * n
        if rng.random() < 0.15 and n > 1:
            i, j = rng.sample(range(n), 2)
            a[i] = [2 * x for x in a[j]]
        b = [rng.randint(-9, 9) for _ in range(n)]
        primes = SMALL_PRIMES if trial % 2 else None
        x = dixon_solve(a, b, primes=primes)
        if det_leibniz(a) == 0:
            assert x is None
        else:
            check(a, b, x)


def test_large_entries() -> None:
    rng = random.Random(7)
    for _ in range(20):
        n = 6
        a = [[rng.randint(-10**30, 10**30) for _ in range(n)] for _ in range(n)]
        b = [rng.randint(-10**30, 10**30) for _ in range(n)]
        x = dixon_solve(a, b)
        assert all(sum(a[i][j] * x[j] for j in range(n)) == b[i] for i in range(n))
