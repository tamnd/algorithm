# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/atomic-congestion-game/. The authors are listed in prov/AE0S3S.jsonl.

import itertools
import random

from atomic_congestion_game import (
    all_profiles,
    best_response_dynamics,
    loads,
    player_cost,
    pure_nash,
    rosenthal_potential,
    social_cost,
)

# Atomic Pigou: link 0 costs 2 for any load, link 1 costs its load.
PIGOU = ([[2, 2], [1, 2]], [[{0}, {1}], [{0}, {1}]])


def test_atomic_pigou():
    table = {p: (social_cost(PIGOU, p), rosenthal_potential(PIGOU, p)) for p in all_profiles(PIGOU)}
    assert table == {(0, 0): (4, 4), (0, 1): (3, 3), (1, 0): (3, 3), (1, 1): (4, 3)}
    assert pure_nash(PIGOU) == [(0, 1), (1, 0), (1, 1)]
    profile, steps = best_response_dynamics(PIGOU, (0, 0))
    assert profile == (1, 0)
    assert steps == [(0, 1, 1)]


def random_game(rng, n, r, k, affine):
    if affine:
        costs = []
        for _ in range(r):
            a, b = rng.randint(0, 3), rng.randint(0, 3)
            costs.append([a * j + b for j in range(1, n + 1)])
    else:
        costs = [sorted(rng.randint(0, 8) for _ in range(n)) for _ in range(r)]
    subsets = [set(c) for size in range(1, r + 1) for c in itertools.combinations(range(r), size)]
    strategies = [rng.sample(subsets, k) for _ in range(n)]
    return costs, strategies


def test_potential_changes_by_the_deviators_gain():
    rng = random.Random(1973)
    for _ in range(50):
        n = rng.randint(2, 4)
        game = random_game(rng, n, rng.randint(2, 4), rng.randint(2, 3), rng.random() < 0.5)
        for p in all_profiles(game):
            for i in range(n):
                for k in range(len(game[1][i])):
                    q = p[:i] + (k,) + p[i + 1 :]
                    assert rosenthal_potential(game, q) - rosenthal_potential(game, p) == player_cost(game, q, i) - player_cost(game, p, i)


def test_equilibria_are_the_local_minima_of_the_potential():
    rng = random.Random(7)
    for _ in range(50):
        n = rng.randint(2, 4)
        game = random_game(rng, n, rng.randint(2, 4), rng.randint(2, 3), False)
        local = []
        for p in all_profiles(game):
            phi = rosenthal_potential(game, p)
            if all(
                rosenthal_potential(game, p[:i] + (k,) + p[i + 1 :]) >= phi
                for i in range(n)
                for k in range(len(game[1][i]))
            ):
                local.append(p)
        assert local == pure_nash(game)
        assert local


def test_best_response_dynamics():
    rng = random.Random(2016)
    for _ in range(60):
        n = rng.randint(2, 4)
        game = random_game(rng, n, rng.randint(2, 4), rng.randint(2, 3), rng.random() < 0.5)
        start = tuple(rng.randrange(len(s)) for s in game[1])
        profile, steps = best_response_dynamics(game, start)
        assert profile in pure_nash(game)
        for _, gain, drop in steps:
            assert gain > 0 and gain == drop
        assert sum(d for _, _, d in steps) == rosenthal_potential(game, start) - rosenthal_potential(game, profile)


def test_potential_and_social_cost():
    rng = random.Random(3)
    for _ in range(40):
        n = rng.randint(2, 4)
        affine = rng.random() < 0.5
        game = random_game(rng, n, rng.randint(2, 4), rng.randint(2, 3), affine)
        for p in all_profiles(game):
            phi, cost = rosenthal_potential(game, p), social_cost(game, p)
            assert phi <= cost <= max(loads(game, p)) * phi
            if affine:
                assert cost <= 2 * phi
            assert cost == sum(player_cost(game, p, i) for i in range(n))
