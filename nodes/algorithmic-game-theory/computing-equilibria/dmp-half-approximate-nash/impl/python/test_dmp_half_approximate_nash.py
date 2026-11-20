# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dmp-half-approximate-nash/. The authors are listed in prov/F0ZSX8.jsonl.

import random
from fractions import Fraction

from agtgame import from_bimatrix, is_epsilon_nash, is_nash, max_gain
from dmp_half_approximate_nash import dmp, gains

F = Fraction
HALF = F(1, 2)


def random_unit_matrix(rng, m, n, den):
    return [[F(rng.randint(0, den), den) for _ in range(n)] for _ in range(m)]


class CountingMatrix:
    """A matrix that counts how many entries are read."""

    def __init__(self, rows):
        self.rows = rows
        self.reads = 0

    def __len__(self):
        return len(self.rows)

    def __getitem__(self, r):
        return CountingRow(self, self.rows[r])


class CountingRow:
    def __init__(self, owner, row):
        self.owner = owner
        self.row = row

    def __len__(self):
        return len(self.row)

    def __getitem__(self, c):
        self.owner.reads += 1
        return self.row[c]


def test_tight_example_gains_are_exactly_half():
    for a, b in [(0, 0), (1, 1), (F(1, 3), F(2, 3))]:
        A = [[0, a], [1, b]]
        B = [[1, 1], [0, 1]]
        x, y = dmp(A, B, 0)
        assert x == [HALF, HALF] and y == [1, 0]
        assert gains(A, B, x, y) == (HALF, HALF)
        assert max_gain(from_bimatrix(A, B), [x, y]) == HALF


def test_pure_equilibrium_when_k_equals_i():
    # Prisoner's dilemma scaled to [0, 1]: defect (row 1, column 1) is dominant.
    A = [[F(3, 5), 0], [1, F(1, 5)]]
    B = [[F(3, 5), 1], [0, F(1, 5)]]
    x, y = dmp(A, B, 1)
    assert x == [0, 1] and y == [0, 1]
    assert is_nash(from_bimatrix(A, B), [x, y])


def test_check_games():
    # Battle of the sexes and matching pennies, scaled to [0, 1].
    bos = ([[1, 0], [0, HALF]], [[HALF, 0], [0, 1]])
    mp = ([[1, 0], [0, 1]], [[0, 1], [1, 0]])
    chicken = ([[0, 1], [F(2, 7), F(6, 7)]], [[0, F(2, 7)], [1, F(6, 7)]])
    for A, B in (bos, mp, chicken):
        g = from_bimatrix(A, B)
        for i in range(len(A)):
            x, y = dmp(A, B, i)
            assert is_epsilon_nash(g, [x, y], HALF)
    # In matching pennies the bound 1/2 is reached from row 0.
    x, y = dmp(*mp, 0)
    assert x == [HALF, HALF] and y == [0, 1]
    assert gains(*mp, x, y) == (HALF, 0)


def test_random_games_every_start_row():
    rng = random.Random(20261120)
    for _ in range(300):
        m, n = rng.randint(1, 6), rng.randint(1, 6)
        A = random_unit_matrix(rng, m, n, rng.choice([1, 2, 5, 12]))
        B = random_unit_matrix(rng, m, n, rng.choice([1, 2, 5, 12]))
        g = from_bimatrix(A, B)
        for i in range(m):
            x, y = dmp(A, B, i)
            assert sum(x) == 1 and sum(y) == 1 and min(x) >= 0
            assert sum(1 for p in x if p) <= 2 and sum(1 for p in y if p) == 1
            gr, gc = gains(A, B, x, y)
            assert gr <= HALF and gc <= HALF
            assert max_gain(g, [x, y]) == max(gr, gc)
            assert is_epsilon_nash(g, [x, y], HALF)


def test_gain_scales_with_the_payoff_range():
    rng = random.Random(7)
    for _ in range(200):
        m, n = rng.randint(1, 5), rng.randint(1, 5)
        lo, hi = rng.randint(-9, 0), rng.randint(1, 9)
        A = [[rng.randint(lo, hi) for _ in range(n)] for _ in range(m)]
        B = [[rng.randint(lo, hi) for _ in range(n)] for _ in range(m)]
        x, y = dmp(A, B, rng.randrange(m))
        gr, gc = gains(A, B, x, y)
        assert gr <= F(hi - lo, 2) and gc <= F(hi - lo, 2)


def test_reads_m_plus_n_entries():
    rng = random.Random(3)
    for m, n in [(1, 1), (3, 5), (8, 2), (10, 10)]:
        A = CountingMatrix(random_unit_matrix(rng, m, n, 4))
        B = CountingMatrix(random_unit_matrix(rng, m, n, 4))
        dmp(A, B, m - 1)
        assert B.reads == n and A.reads == m
