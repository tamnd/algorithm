# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/levinson-durbin-algorithm/. The authors are listed in prov/44KZ70.jsonl.

import itertools
import random
from fractions import Fraction

import pytest

from levinson_durbin_algorithm import LeadingMinorZero, levinson_durbin, toeplitz_matrix


def leibniz(a, p=None):
    n = len(a)
    total = 0
    for s in itertools.permutations(range(n)):
        inv = sum(1 for i in range(n) for j in range(i + 1, n) if s[i] > s[j])
        term = -1 if inv % 2 else 1
        for i in range(n):
            term *= a[i][s[i]]
        total += term
    return total if p is None else total % p


def leading_minors_nonzero(a, p=None):
    return all(leibniz([r[:k] for r in a[:k]], p) != 0 for k in range(1, len(a) + 1))


def apply(a, x, p=None):
    out = [sum(Fraction(a[i][j]) * x[j] for j in range(len(x))) for i in range(len(a))]
    return out if p is None else [int(v) % p for v in out]


def random_toeplitz(rng, n, lo, hi):
    col = [rng.randrange(lo, hi) for _ in range(n)]
    row = [col[0]] + [rng.randrange(lo, hi) for _ in range(n - 1)] if n else []
    return col, row


def test_worked_example():
    col, row = [2, 1, 3], [2, -1, 1]
    t = toeplitz_matrix(col, row)
    assert t == [[2, -1, 1], [1, 2, -1], [3, 1, 2]]
    assert levinson_durbin(col, row, [5, -3, 6]) == [1, -1, 2]


def test_symmetric_example():
    col = row = [4, 2, 1]
    assert levinson_durbin(col, row, [7, 8, 7]) == [1, 1, 1]


def test_edges():
    assert levinson_durbin([], [], []) == []
    assert levinson_durbin([5], [5], [10]) == [2]
    assert levinson_durbin([3], [3], [1], p=7) == [5]
    with pytest.raises(LeadingMinorZero):
        levinson_durbin([0, 1], [0, 1], [1, 2])  # nonsingular, but t_0 = 0
    with pytest.raises(LeadingMinorZero):
        levinson_durbin([1, 1], [1, 1], [1, 2])  # singular
    with pytest.raises(LeadingMinorZero):
        levinson_durbin([1, 1, 0], [1, 1, 5], [1, 2, 3])  # the 2 by 2 minor is zero
    with pytest.raises(ValueError):
        levinson_durbin([1, 2], [3, 2], [1, 1])


def test_large_entries():
    rng = random.Random(11)
    for _ in range(30):
        n = rng.randrange(1, 9)
        col, row = random_toeplitz(rng, n, -2**64, 2**64)
        x_true = [rng.randrange(-2**30, 2**30) for _ in range(n)]
        t = toeplitz_matrix(col, row)
        c = [sum(t[i][j] * x_true[j] for j in range(n)) for i in range(n)]
        assert levinson_durbin(col, row, c) == x_true


def test_random_over_q():
    rng = random.Random(2025)
    for _ in range(600):
        n = rng.randrange(1, 6)
        col, row = random_toeplitz(rng, n, -3, 4)
        t = toeplitz_matrix(col, row)
        c = [rng.randrange(-9, 10) for _ in range(n)]
        if leading_minors_nonzero(t):
            x = levinson_durbin(col, row, c)
            assert apply(t, x) == c
        else:
            with pytest.raises(LeadingMinorZero):
                levinson_durbin(col, row, c)


@pytest.mark.parametrize("p", [2, 3, 5, 101])
def test_random_mod_p(p):
    rng = random.Random(p)
    for _ in range(300):
        n = rng.randrange(1, 6)
        col, row = random_toeplitz(rng, n, 0, p)
        t = toeplitz_matrix(col, row)
        c = [rng.randrange(p) for _ in range(n)]
        if leading_minors_nonzero(t, p):
            x = levinson_durbin(col, row, c, p)
            assert apply(t, x, p) == c
            assert all(0 <= v < p for v in x)
        else:
            with pytest.raises(LeadingMinorZero):
                levinson_durbin(col, row, c, p)


def test_symmetric_random():
    rng = random.Random(5)
    for _ in range(200):
        n = rng.randrange(1, 7)
        col = [rng.randrange(-5, 6) for _ in range(n)]
        col[0] = 30  # diagonally dominant, so positive definite and every leading minor is nonzero
        c = [rng.randrange(-9, 10) for _ in range(n)]
        x = levinson_durbin(col, col, c)
        assert apply(toeplitz_matrix(col, col), x) == c
