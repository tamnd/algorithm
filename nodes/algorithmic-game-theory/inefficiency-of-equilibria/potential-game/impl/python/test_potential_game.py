# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/potential-game/. The authors are listed in prov/9E88DE.jsonl.

import itertools
import random
from fractions import Fraction

from potential_game import (
    deviations,
    exact_potential,
    four_cycle_sums,
    is_exact_potential,
    profiles,
    pure_nash,
)

C, D = 0, 1
PD = {(C, C): (1, 1), (C, D): (3, 0), (D, C): (0, 3), (D, D): (2, 2)}
MATCHING_PENNIES = {(0, 0): (0, 1), (1, 1): (0, 1), (0, 1): (1, 0), (1, 0): (1, 0)}
ORDINAL_ONLY = {(0, 0): (0, 0), (1, 0): (1, 0), (0, 1): (0, 1), (1, 1): (2, 1)}


def shifted(phi, s):
    return {t: v - phi[s] for t, v in phi.items()}


def test_prisoners_dilemma():
    phi = exact_potential((2, 2), PD)
    phi = {t: v + 2 for t, v in phi.items()}
    assert phi == {(C, C): 2, (C, D): 1, (D, C): 1, (D, D): 0}
    assert pure_nash((2, 2), PD) == [(D, D)]


def test_no_exact_potential():
    assert exact_potential((2, 2), MATCHING_PENNIES) is None
    assert pure_nash((2, 2), MATCHING_PENNIES) == []
    assert exact_potential((2, 2), ORDINAL_ONLY) is None
    assert four_cycle_sums((2, 2), ORDINAL_ONLY) == {1, -1}
    count_b = {s: sum(s) for s in ORDINAL_ONLY}
    for s in ORDINAL_ONLY:
        for i, t in deviations((2, 2), s):
            assert (ORDINAL_ONLY[t][i] < ORDINAL_ONLY[s][i]) == (count_b[t] < count_b[s])


def random_congestion_game(rng, n, r, k):
    """n players, r resources with cost tables, k strategies (nonempty resource sets) per player."""
    table = [[rng.randint(0, 6) for _ in range(n)] for _ in range(r)]
    subsets = [frozenset(c) for size in range(1, r + 1) for c in itertools.combinations(range(r), size)]
    strategies = [rng.sample(subsets, k) for _ in range(n)]
    sizes = tuple(k for _ in range(n))
    cost, rosenthal = {}, {}
    for s in profiles(sizes):
        load = [sum(1 for i in range(n) if e in strategies[i][s[i]]) for e in range(r)]
        cost[s] = tuple(sum(table[e][load[e] - 1] for e in strategies[i][s[i]]) for i in range(n))
        rosenthal[s] = Fraction(sum(table[e][j] for e in range(r) for j in range(load[e])))
    return sizes, cost, rosenthal


def test_congestion_games_have_the_rosenthal_potential():
    rng = random.Random(1973)
    for _ in range(40):
        n = rng.randint(2, 4)
        sizes, cost, rosenthal = random_congestion_game(rng, n, rng.randint(2, 4), rng.randint(2, 3))
        for s in profiles(sizes):
            for i, t in deviations(sizes, s):
                assert rosenthal[t] - rosenthal[s] == cost[t][i] - cost[s][i]
        phi = exact_potential(sizes, cost)
        assert phi is not None
        start = profiles(sizes)[0]
        assert shifted(phi, start) == shifted(rosenthal, start)
        low = min(phi.values())
        minimizers = [s for s in phi if phi[s] == low]
        assert set(minimizers) <= set(pure_nash(sizes, cost))


def test_coordination_plus_dummy():
    rng = random.Random(1996)
    for _ in range(40):
        sizes = tuple(rng.randint(2, 4) for _ in range(rng.randint(2, 3)))
        base = {s: rng.randint(-5, 5) for s in profiles(sizes)}
        dummy = [dict() for _ in sizes]
        cost = {}
        for s in profiles(sizes):
            parts = []
            for i in range(len(sizes)):
                key = s[:i] + s[i + 1 :]
                if key not in dummy[i]:
                    dummy[i][key] = rng.randint(-5, 5)
                parts.append(base[s] + dummy[i][key])
            cost[s] = tuple(parts)
        phi = exact_potential(sizes, cost)
        assert is_exact_potential(sizes, cost, phi)
        start = profiles(sizes)[0]
        assert shifted(phi, start) == shifted({s: Fraction(v) for s, v in base.items()}, start)


def test_four_cycle_characterization():
    rng = random.Random(44)
    seen = {True: 0, False: 0}
    for trial in range(150):
        sizes = tuple(rng.randint(2, 3) for _ in range(rng.randint(2, 3)))
        base = {s: rng.randint(0, 4) for s in profiles(sizes)}
        cost = {s: tuple(base[s] for _ in sizes) for s in base}
        if trial % 2:
            s = rng.choice(profiles(sizes))
            i = rng.randrange(len(sizes))
            cost[s] = cost[s][:i] + (cost[s][i] + rng.randint(1, 3),) + cost[s][i + 1 :]
        exists = exact_potential(sizes, cost) is not None
        assert exists == (four_cycle_sums(sizes, cost) <= {0})
        seen[exists] += 1
    assert seen[True] > 0 and seen[False] > 0
