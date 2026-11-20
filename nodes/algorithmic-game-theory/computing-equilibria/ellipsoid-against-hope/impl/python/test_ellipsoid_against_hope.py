# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ellipsoid-against-hope/. The authors are listed in prov/WQZKXN.jsonl.
"""Tests of ellipsoid against hope: the stationary step, the separation oracle, and exact
correlated equilibria on games with known and unknown equilibria."""

import random
from fractions import Fraction

from agtgame import from_bimatrix, is_correlated, profiles, random_game
from ellipsoid_against_hope import (dual_index, ellipsoid_against_hope, gain_column, restricted_lp,
                                    separation_oracle, stationary_of_rates)

F = Fraction
CHICKEN = from_bimatrix([[0, 7], [2, 6]], [[0, 2], [7, 6]])
PENNIES = from_bimatrix([[1, -1], [-1, 1]], [[-1, 1], [1, -1]])
RPS = from_bimatrix([[0, -1, 1], [1, 0, -1], [-1, 1, 0]], [[0, 1, -1], [-1, 0, 1], [1, -1, 0]])
PD = from_bimatrix([[3, 0], [5, 1]], [[3, 5], [0, 1]])


def g_value(game, y, s, index):
    return sum(float(c) * v for c, v in zip(gain_column(game, s, index), y))


def test_stationary_of_rates_balances_the_flows():
    rng = random.Random(5)
    for _ in range(300):
        k = rng.randint(1, 5)
        rates = [[rng.choice([0.0, 0.0, rng.random() * 3]) if j != l else 0.0 for l in range(k)] for j in range(k)]
        x = stationary_of_rates(rates)
        assert all(v >= 0 for v in x) and abs(sum(x) - 1) < 1e-12
        for j in range(k):
            out_flow = x[j] * sum(rates[j][l] for l in range(k) if l != j)
            in_flow = sum(x[l] * rates[l][j] for l in range(k) if l != j)
            assert abs(out_flow - in_flow) < 1e-9


def test_oracle_returns_a_violated_constraint():
    rng = random.Random(8)
    for _ in range(60):
        sizes = tuple(rng.randint(2, 3) for _ in range(rng.choice([2, 3])))
        game = random_game(rng, sizes, -4, 4)
        index = dual_index(sizes)
        y = [rng.choice([0.0, rng.random() * 5]) for _ in index]
        s = separation_oracle(game, y, index)
        assert s in set(profiles(sizes))
        assert g_value(game, y, s, index) >= -1e-9  # so g(y, s) <= -1 fails


def test_known_equilibria():
    for game in (PENNIES, RPS):
        p, X, _ = ellipsoid_against_hope(game)
        k = game[0][0]
        assert p == {s: F(1, k * k) for s in profiles(game[0])}  # the unique correlated equilibrium
    p, _, _ = ellipsoid_against_hope(PD)
    assert p == {(1, 1): F(1)}
    p, X, steps = ellipsoid_against_hope(CHICKEN)
    assert is_correlated(CHICKEN, p) and set(p) <= X and len(X) <= steps


def test_random_games_give_exact_correlated_equilibria():
    rng = random.Random(2008)
    for _ in range(40):
        sizes = tuple(rng.randint(2, 3) for _ in range(rng.choice([2, 2, 3])))
        game = random_game(rng, sizes, -3, 3)
        p, X, steps = ellipsoid_against_hope(game)
        assert is_correlated(game, p)
        assert set(p) <= X and len(X) <= steps
        # The returned distribution is one that the restricted LP accepts.
        assert restricted_lp(game, X) is not None


def test_restricted_lp_can_be_infeasible():
    # In matching pennies no correlated equilibrium has support smaller than all four profiles.
    assert restricted_lp(PENNIES, {(0, 0), (0, 1), (1, 0)}) is None
    assert restricted_lp(PD, {(0, 0)}) is None
    assert restricted_lp(PD, {(1, 1)}) == {(1, 1): F(1)}


def test_trivial_games():
    solo = ((1, 1), {(0, 0): (F(2), F(3))})
    p, X, steps = ellipsoid_against_hope(solo)
    assert p == {(0, 0): F(1)} and steps == 0
    one = ((3,), {(0,): (F(1),), (1,): (F(4),), (2,): (F(4),)})
    p, _, _ = ellipsoid_against_hope(one)
    assert is_correlated(one, p) and set(p) <= {(1,), (2,)}
