# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/best-response-dynamics/. The authors are listed in prov/0D2G4K.jsonl.
"""Tests of best-response dynamics: potential games, matching pennies and random games."""

import random
from fractions import Fraction
from itertools import product

import pytest

from agtgame import from_bimatrix, profiles, pure_nash_brute, random_game
from best_response_dynamics import best_response_dynamics, best_responses

F = Fraction


def congestion_game(strategies, costs):
    """Return (game, potential) of an atomic congestion game, with utilities u = -c.

    strategies[i] is the list of the strategies of player i, each a tuple of resources.
    costs[e][j - 1] is the cost of resource e to each of its j users.
    """
    sizes = tuple(len(st) for st in strategies)

    def loads(s):
        load = [0] * len(costs)
        for i, a in enumerate(s):
            for e in strategies[i][a]:
                load[e] += 1
        return load

    pay = {}
    for s in profiles(sizes):
        load = loads(s)
        pay[s] = tuple(F(-sum(costs[e][load[e] - 1] for e in strategies[i][a])) for i, a in enumerate(s))

    def potential(s):
        load = loads(s)
        return sum(sum(costs[e][:load[e]]) for e in range(len(costs)))

    return (sizes, pay), potential


def naive_run(game, start, limit):
    """Apply the step rule from its definition, and stop at the first repeat or equilibrium."""
    sizes, pay = game
    s = tuple(start)
    path = [s]
    for _ in range(limit):
        movers = []
        for i in range(len(sizes)):
            here = pay[s][i]
            if any(pay[s[:i] + (b,) + s[i + 1:]][i] > here for b in range(sizes[i])):
                movers.append(i)
        if not movers:
            return s, "equilibrium", path
        if s in path[:-1]:
            return s, "cycle", path
        i = movers[0]
        top = max(pay[s[:i] + (b,) + s[i + 1:]][i] for b in range(sizes[i]))
        b = min(b for b in range(sizes[i]) if pay[s[:i] + (b,) + s[i + 1:]][i] == top)
        s = s[:i] + (b,) + s[i + 1:]
        path.append(s)
    raise AssertionError("the step limit is too small")


def test_page_example_two_links():
    game, phi = congestion_game([[(0,), (1,)]] * 4, [[1, 2, 3, 4], [1, 2, 3, 4]])
    s, status, path = best_response_dynamics(game, (0, 0, 0, 0))
    assert status == "equilibrium"
    assert path == [(0, 0, 0, 0), (1, 0, 0, 0), (1, 1, 0, 0)]
    assert [phi(p) for p in path] == [10, 7, 6]
    assert s in pure_nash_brute(game)


def test_matching_pennies_cycles():
    game = from_bimatrix([[1, -1], [-1, 1]], [[-1, 1], [1, -1]])
    assert pure_nash_brute(game) == []
    s, status, path = best_response_dynamics(game, (0, 0))
    assert status == "cycle"
    assert path == [(0, 0), (0, 1), (1, 1), (1, 0), (0, 0)]
    for start in profiles(game[0]):
        assert best_response_dynamics(game, start)[1] == "cycle"


def test_edge_cases():
    one = ((3,), {(0,): (F(1),), (1,): (F(5),), (2,): (F(5),)})
    assert best_response_dynamics(one, (0,)) == ((1,), "equilibrium", [(0,), (1,)])
    assert best_response_dynamics(one, (2,)) == ((2,), "equilibrium", [(2,)])
    flat = random_game(random.Random(1), (2, 3), 0, 0)
    assert best_response_dynamics(flat, (1, 2)) == ((1, 2), "equilibrium", [(1, 2)])
    assert best_responses(flat, (1, 2), 1) == [0, 1, 2]
    with pytest.raises(ValueError):
        best_response_dynamics(flat, (2, 0))
    with pytest.raises(ValueError):
        best_response_dynamics(flat, (0,))


def test_random_congestion_games_potential_strictly_falls():
    rng = random.Random(20240)
    for _ in range(250):
        n = rng.randint(2, 4)
        r = rng.randint(2, 4)
        subsets = [t for size in (1, 2) for t in product(range(r), repeat=size) if len(set(t)) == size and list(t) == sorted(t)]
        strategies = [rng.sample(subsets, rng.randint(2, min(4, len(subsets)))) for _ in range(n)]
        costs = []
        for _ in range(r):
            c, row = 0, []
            for _ in range(n):
                c += rng.randint(0, 4)
                row.append(c)
            costs.append(row)
        game, phi = congestion_game(strategies, costs)
        start = tuple(rng.randrange(k) for k in game[0])
        s, status, path = best_response_dynamics(game, start)
        assert status == "equilibrium"
        assert s in pure_nash_brute(game)
        for a, b in zip(path, path[1:]):
            mover = [i for i in range(n) if a[i] != b[i]]
            assert len(mover) == 1
            i = mover[0]
            gain = game[1][b][i] - game[1][a][i]
            assert gain > 0
            assert phi(a) - phi(b) == gain  # Rosenthal's potential is exact


def test_random_exact_potential_games():
    rng = random.Random(77)
    for _ in range(200):
        sizes = tuple(rng.randint(2, 3) for _ in range(rng.randint(2, 3)))
        phi = {s: F(rng.randint(-9, 9)) for s in profiles(sizes)}
        dummy = [{s[:i] + s[i + 1:]: F(rng.randint(-9, 9)) for s in profiles(sizes)} for i in range(len(sizes))]
        pay = {s: tuple(phi[s] + dummy[i][s[:i] + s[i + 1:]] for i in range(len(sizes))) for s in profiles(sizes)}
        game = (sizes, pay)
        start = tuple(rng.randrange(k) for k in sizes)
        s, status, path = best_response_dynamics(game, start)
        assert status == "equilibrium" and s in pure_nash_brute(game)
        assert all(phi[b] > phi[a] for a, b in zip(path, path[1:]))
        assert len(path) <= len(phi)


def test_random_games_against_naive_run():
    rng = random.Random(4242)
    cycles = 0
    for _ in range(500):
        sizes = tuple(rng.randint(2, 3) for _ in range(rng.randint(2, 3)))
        game = random_game(rng, sizes, -3, 3)
        start = tuple(rng.randrange(k) for k in sizes)
        got = best_response_dynamics(game, start)
        assert got == naive_run(game, start, len(game[1]) + 1)
        s, status, path = got
        nash = pure_nash_brute(game)
        if status == "equilibrium":
            assert s in nash
        else:
            cycles += 1
            assert s in path[:-1] and len(path) <= len(game[1]) + 1
        if not nash:
            assert status == "cycle"
    assert cycles > 0
