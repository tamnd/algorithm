# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/grasp/. The authors are listed in prov/FPPN86.jsonl.

import itertools
import random
from fractions import Fraction

import pytest

from grasp import cover_cost, covers, drop_and_swap_descent, grasp, greedy_randomized_construction

U8 = set(range(8))
S8 = [{0, 2, 4, 5, 7}, {4, 6, 7}, {0, 1, 5, 6}, {0, 4}, {2, 3, 6}, {3, 6}, {0, 6, 7}]
C8 = [9, 5, 9, 2, 9, 9, 4]


def brute_force(universe, sets, costs) -> int:
    return min(
        cover_cost(costs, frozenset(x))
        for r in range(1, len(sets) + 1)
        for x in itertools.combinations(range(len(sets)), r)
        if covers(universe, sets, frozenset(x))
    )


def is_local_min(universe, sets, costs, x) -> bool:
    c = cover_cost(costs, x)
    for j in x:
        for y in [x - {j}] + [(x - {j}) | {k} for k in range(len(sets)) if k not in x]:
            if covers(universe, sets, y) and cover_cost(costs, y) < c:
                return False
    return True


def test_example_of_the_page() -> None:
    assert brute_force(U8, S8, C8) == 23
    g, steps = greedy_randomized_construction(U8, S8, C8, Fraction(0), random.Random(0))
    assert [j for _, j in steps] == [3, 6, 0, 4, 2] and cover_cost(C8, g) == 33
    assert drop_and_swap_descent(U8, S8, C8, g) == frozenset({2, 3, 4, 6})
    best, cost, log = grasp(U8, S8, C8, Fraction(1, 2), 3, random.Random(0))
    assert [(sorted(x), cx, sorted(z), cz) for x, cx, z, cz in log] == [
        ([0, 2, 3, 4], 29, [2, 3, 4, 6], 24),
        ([2, 3, 4, 6], 24, [2, 3, 4, 6], 24),
        ([1, 2, 3, 4], 25, [1, 2, 4], 23),
    ]
    assert (best, cost) == (frozenset({1, 2, 4}), 23)


def random_instance(rng):
    m = rng.randint(1, 8)
    universe = set(range(m))
    sets = [set(e for e in range(m) if rng.random() < 0.4) for _ in range(rng.randint(1, 7))]
    sets = [s for s in sets if s] or [set(universe)]
    missing = universe - set().union(*sets)
    if missing:
        sets.append(missing)
    costs = [rng.randint(1, 9) for _ in sets]
    return universe, sets, costs


def test_construction_follows_the_candidate_list() -> None:
    rng = random.Random(31)
    for _ in range(400):
        universe, sets, costs = random_instance(rng)
        alpha = Fraction(rng.randint(0, 4), 4)
        x, steps = greedy_randomized_construction(universe, sets, costs, alpha, random.Random(rng.random()))
        assert covers(universe, sets, x)
        uncovered = set(universe)
        for rcl, j in steps:
            ratio = {k: Fraction(costs[k], len(s & uncovered)) for k, s in enumerate(sets) if s & uncovered}
            lo, hi = min(ratio.values()), max(ratio.values())
            assert rcl == sorted(k for k, r in ratio.items() if r <= lo + alpha * (hi - lo))
            assert j in rcl and sets[j] & uncovered
            uncovered -= sets[j]
        assert not uncovered and x == frozenset(j for _, j in steps)


def test_greedy_construction_meets_the_harmonic_bound() -> None:
    rng = random.Random(77)
    for _ in range(300):
        universe, sets, costs = random_instance(rng)
        d = max(len(s) for s in sets)
        harmonic = sum(Fraction(1, i) for i in range(1, d + 1))
        x, _ = greedy_randomized_construction(universe, sets, costs, Fraction(0), random.Random(rng.random()))
        assert cover_cost(costs, x) <= harmonic * brute_force(universe, sets, costs)


def test_invariants_on_random_instances() -> None:
    rng = random.Random(4040)
    for _ in range(200):
        universe, sets, costs = random_instance(rng)
        best, cost, log = grasp(universe, sets, costs, Fraction(rng.randint(0, 4), 4), rng.randint(1, 5), random.Random(rng.random()))
        for x, cx, z, cz in log:
            assert covers(universe, sets, x) and covers(universe, sets, z)
            assert cz == cover_cost(costs, z) <= cx == cover_cost(costs, x)
            assert is_local_min(universe, sets, costs, z)
        assert cost == cover_cost(costs, best) == min(cz for *_, cz in log)
        assert cost >= brute_force(universe, sets, costs)


def test_edges() -> None:
    with pytest.raises(ValueError):
        grasp(U8, S8, C8, Fraction(1, 2), 0, random.Random(1))
    with pytest.raises(ValueError):
        greedy_randomized_construction({0, 1}, [{0}], [1], Fraction(0), random.Random(1))
    assert grasp(set(), [{0}], [3], Fraction(1), 2, random.Random(1))[:2] == (frozenset(), 0)


def test_fixed_seed_reaches_the_optimum() -> None:
    rng = random.Random(2024)
    universe = set(range(12))
    sets = [set(e for e in range(12) if rng.random() < 0.3) for _ in range(12)]
    sets.append(universe - set().union(*sets))
    sets = [s for s in sets if s]
    costs = [rng.randint(1, 20) for _ in sets]
    opt = brute_force(universe, sets, costs)
    best, cost, _ = grasp(universe, sets, costs, Fraction(1, 2), 10, random.Random(5))
    assert cost == opt and covers(universe, sets, best)
