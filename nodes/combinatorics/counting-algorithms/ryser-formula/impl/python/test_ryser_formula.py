# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ryser-formula/. The authors are listed in prov/11ZBTR.jsonl.

import itertools
import math
import random
from fractions import Fraction

import pytest

from ryser_formula import ryser_permanent


def per_definition(a):
    """Reference: the sum over all permutations."""
    n = len(a)
    return sum(
        math.prod(a[i][p[i]] for i in range(n)) for p in itertools.permutations(range(n))
    )


def per_expansion(a):
    """Reference: row expansion with memoization over column subsets."""
    n = len(a)
    f = {0: 1}
    for mask in range(1, 1 << n):
        row = bin(mask).count("1") - 1
        f[mask] = sum(a[row][j] * f[mask ^ (1 << j)] for j in range(n) if mask >> j & 1)
    return f[(1 << n) - 1]


def test_worked_example():
    assert ryser_permanent([[1, 2, 3], [4, 5, 6], [7, 8, 9]]) == 450


def test_edges():
    assert ryser_permanent([]) == 1
    assert ryser_permanent([[7]]) == 7
    assert ryser_permanent([[0]]) == 0
    assert ryser_permanent([[1, 2], [3, 4]]) == 10
    with pytest.raises(ValueError):
        ryser_permanent([[1, 2], [3]])
    with pytest.raises(ValueError):
        ryser_permanent([[1, 2]])


def test_named_matrices():
    for n in range(0, 9):
        ones = [[1] * n for _ in range(n)]
        assert ryser_permanent(ones) == math.factorial(n)
        ident = [[int(i == j) for j in range(n)] for i in range(n)]
        assert ryser_permanent(ident) == 1
    derangements = [1, 0, 1, 2, 9, 44, 265, 1854, 14833, 133496, 1334961]
    for n, d in enumerate(derangements):
        assert ryser_permanent([[int(i != j) for j in range(n)] for i in range(n)]) == d
    menage = [1, 2, 13, 80, 579, 4738, 43387]
    for n, m in zip(range(3, 10), menage):
        a = [[0 if j in (i, (i + 1) % n) else 1 for j in range(n)] for i in range(n)]
        assert ryser_permanent(a) == m


def test_fractions():
    a = [[Fraction(1, 2), Fraction(1, 3)], [Fraction(1, 5), Fraction(1, 7)]]
    assert ryser_permanent(a) == Fraction(1, 14) + Fraction(1, 15)


def test_random_against_definition():
    rng = random.Random(20260611)
    for _ in range(600):
        n = rng.randint(0, 6)
        lo = rng.choice([0, -5])
        a = [[rng.randint(lo, 5) for _ in range(n)] for _ in range(n)]
        assert ryser_permanent(a) == per_definition(a)


def test_random_zero_one_against_expansion():
    rng = random.Random(7)
    for _ in range(200):
        n = rng.randint(1, 9)
        p = rng.random()
        a = [[int(rng.random() < p) for _ in range(n)] for _ in range(n)]
        assert ryser_permanent(a) == per_expansion(a)


def test_invariance():
    rng = random.Random(11)
    for _ in range(100):
        n = rng.randint(1, 7)
        a = [[rng.randint(-3, 3) for _ in range(n)] for _ in range(n)]
        rows = list(range(n))
        cols = list(range(n))
        rng.shuffle(rows)
        rng.shuffle(cols)
        b = [[a[rows[i]][cols[j]] for j in range(n)] for i in range(n)]
        t = [list(col) for col in zip(*a)]
        assert ryser_permanent(a) == ryser_permanent(b) == ryser_permanent(t)
