# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/correlated-equilibrium-linear-program/. The authors are listed in prov/V535CJ.jsonl.
"""Tests of the correlated equilibrium LP against check values and vertex enumeration."""

import random
from fractions import Fraction
from itertools import combinations

from agtgame import from_bimatrix, is_coarse_correlated, is_correlated, profiles, pure_nash_brute, random_game
from correlated_equilibrium_linear_program import ce_constraints, correlated_equilibrium_lp

F = Fraction
CHICKEN = from_bimatrix([[0, 7], [2, 6]], [[0, 2], [7, 6]])  # strategy 0 is D, 1 is C


def welfare(game, p):
    return sum((q * sum(game[1][s], F(0)) for s, q in p.items()), F(0))


def solve_unique(M, b):
    """Return the unique solution of the square system M z = b, or None."""
    r = len(M)
    rows = [list(M[k]) + [b[k]] for k in range(r)]
    for col in range(r):
        p = next((k for k in range(col, r) if rows[k][col] != 0), None)
        if p is None:
            return None
        rows[col], rows[p] = rows[p], rows[col]
        pv = rows[col][col]
        rows[col] = [v / pv for v in rows[col]]
        for k in range(r):
            f = rows[k][col]
            if k != col and f != 0:
                rows[k] = [a - f * c for a, c in zip(rows[k], rows[col])]
    return [rows[k][-1] for k in range(r)]


def best_vertex(game, weight):
    """Maximize sum_s weight(s) p(s) over the CE polytope by enumerating all its vertices."""
    S, rows, _ = ce_constraints(game)
    N = len(S)
    ineq = rows + [[F(-1) if a == b else F(0) for a in range(N)] for b in range(N)]
    best = None
    for tight in combinations(range(len(ineq)), N - 1):
        z = solve_unique([[F(1)] * N] + [ineq[t] for t in tight], [F(1)] + [F(0)] * (N - 1))
        if z is None or any(sum((a * v for a, v in zip(row, z)), F(0)) > 0 for row in ineq):
            continue
        val = sum((F(weight(s)) * v for s, v in zip(S, z)), F(0))
        best = val if best is None or val > best else best
    return best


def test_chicken_check_values():
    p, value = correlated_equilibrium_lp(CHICKEN)
    assert p == {(0, 1): F(1, 4), (1, 0): F(1, 4), (1, 1): F(1, 2)}
    assert value == F(21, 2)
    assert all(sum(q * CHICKEN[1][s][i] for s, q in p.items()) == F(21, 4) for i in range(2))
    assert is_correlated(CHICKEN, p)
    third = {(0, 1): F(1, 3), (1, 0): F(1, 3), (1, 1): F(1, 3)}
    assert is_correlated(CHICKEN, third) and welfare(CHICKEN, third) == 10
    mixed = {(a, b): F([1, 2][a], 3) * F([1, 2][b], 3) for a in range(2) for b in range(2)}
    assert is_correlated(CHICKEN, mixed) and welfare(CHICKEN, mixed) == F(28, 3)
    low, low_value = correlated_equilibrium_lp(CHICKEN, weight=lambda s: -sum(CHICKEN[1][s]))
    assert is_correlated(CHICKEN, low) and low_value == best_vertex(CHICKEN, lambda s: -sum(CHICKEN[1][s]))
    assert welfare(CHICKEN, low) == -low_value == F(36, 5)
    assert low == {(0, 0): F(1, 5), (0, 1): F(2, 5), (1, 0): F(2, 5)}


def test_unique_correlated_equilibria():
    pennies = from_bimatrix([[1, -1], [-1, 1]], [[-1, 1], [1, -1]])
    rps = from_bimatrix([[0, -1, 1], [1, 0, -1], [-1, 1, 0]], [[0, 1, -1], [-1, 0, 1], [1, -1, 0]])
    pd = from_bimatrix([[3, 0], [5, 1]], [[3, 5], [0, 1]])
    rng = random.Random(5)
    for _ in range(5):
        w = {s: rng.randint(-5, 5) for s in profiles((3, 3))}
        p, _ = correlated_equilibrium_lp(rps, weight=lambda s: w[s])
        assert p == {s: F(1, 9) for s in profiles((3, 3))}
        p, _ = correlated_equilibrium_lp(pennies, weight=lambda s: w[s] if s in w else 0)
        assert p == {s: F(1, 4) for s in profiles((2, 2))}
    assert correlated_equilibrium_lp(pd)[0] == {(1, 1): F(1)}


def test_feasibility_mode_and_one_player():
    p, value = correlated_equilibrium_lp(CHICKEN, weight=lambda s: 0)
    assert value == 0 and is_correlated(CHICKEN, p)
    solo = ((3,), {(0,): (F(2),), (1,): (F(5),), (2,): (F(5),)})
    p, value = correlated_equilibrium_lp(solo)
    assert value == 5 and is_correlated(solo, p) and set(p) <= {(1,), (2,)}


def test_constraint_count_and_meaning():
    game = random_game(random.Random(3), (2, 3, 2), -3, 3)
    S, rows, labels = ce_constraints(game)
    assert len(S) == 12 and len(rows) == 2 + 6 + 2
    for (i, j, l), row in zip(labels, rows):
        assert all(row[t] == 0 for t, s in enumerate(S) if s[i] != j)


def test_random_two_player_games_against_vertex_enumeration():
    rng = random.Random(1234)
    for _ in range(80):
        sizes = rng.choice([(2, 2), (2, 2), (2, 3), (3, 2)])
        game = random_game(rng, sizes, -4, 4)
        if sizes == (2, 2) or rng.random() < 0.08:
            p, value = correlated_equilibrium_lp(game)
            assert is_correlated(game, p) and is_coarse_correlated(game, p)
            assert welfare(game, p) == value
            assert value == best_vertex(game, lambda s: sum(game[1][s]))
            for s in pure_nash_brute(game):
                assert sum(game[1][s]) <= value


def test_random_multiplayer_games():
    rng = random.Random(77)
    for _ in range(40):
        sizes = tuple(rng.randint(2, 3) for _ in range(rng.choice([2, 3])))
        game = random_game(rng, sizes, -3, 3)
        w = {s: rng.randint(-3, 3) for s in profiles(sizes)}
        p, value = correlated_equilibrium_lp(game, weight=lambda s: w[s])
        assert is_correlated(game, p)
        assert sum((q * w[s] for s, q in p.items()), F(0)) == value
        # Every pure Nash equilibrium is a feasible point, so it cannot do better.
        for s in pure_nash_brute(game):
            assert w[s] <= value
