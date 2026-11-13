# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hashiwokakero-problem/. The authors are listed in prov/BYSQMT.jsonl.

import random

from hashiwokakero_problem import brute_force, connected, crossings, is_solution, slots, solve


def random_instance(rng, h, w, n):
    """Numbers taken from a random valid bridge plan, so a solution exists."""
    cells = [(r, c) for r in range(h) for c in range(w)]
    while True:
        pos = rng.sample(cells, n)
        isl = {p: 0 for p in pos}
        sl = slots(isl)
        cr = crossings(sl)
        counts = [rng.choice((0, 1, 1, 2)) for _ in sl]
        if any(counts[i] and counts[j] for i, j in cr) or not connected(isl, sl, counts):
            continue
        for (a, b), k in zip(sl, counts):
            isl[a] += k
            isl[b] += k
        if all(isl.values()):
            return isl, counts


def test_known_puzzle() -> None:
    islands = {(0, 0): 1, (0, 2): 3, (0, 4): 4, (0, 6): 4, (2, 0): 2, (2, 4): 1,
               (4, 6): 2, (6, 0): 3, (6, 2): 2}
    sl = slots(islands)
    sols = solve(islands)
    assert len(sols) == 1
    plan = dict(zip(sl, sols[0]))
    assert plan[((0, 4), (0, 6))] == 2 and plan[((0, 6), (4, 6))] == 2
    assert plan[((2, 0), (6, 0))] == 2 and plan[((0, 2), (6, 2))] == 1
    assert plan[((2, 0), (2, 4))] == 0
    assert sorted(map(tuple, sols)) == sorted(map(tuple, brute_force(islands)))


def test_connectivity_rule() -> None:
    # Four 2s on a square: without the connectivity rule there are three plans.
    square = {(0, 0): 2, (0, 2): 2, (2, 0): 2, (2, 2): 2}
    sl = slots(square)
    plans = [[1, 1, 1, 1], [2, 0, 0, 2], [0, 2, 2, 0]]
    assert sl == [((0, 0), (0, 2)), ((0, 0), (2, 0)), ((0, 2), (2, 2)), ((2, 0), (2, 2))]
    assert [is_solution(square, sl, p) for p in plans] == [True, False, False]
    assert solve(square) == [[1, 1, 1, 1]]


def test_crossing_rule() -> None:
    plus = {(0, 1): 1, (2, 1): 1, (1, 0): 1, (1, 2): 1}
    sl = slots(plus)
    assert len(crossings(sl)) == 1
    # Both bridges are needed and they cross, so there is no solution.
    assert solve(plus) == [] and brute_force(plus) == []


def test_solver_against_brute_force() -> None:
    rng = random.Random(31)
    checked = 0
    while checked < 60:
        h, w = rng.randint(2, 5), rng.randint(2, 5)
        n = rng.randint(2, min(7, h * w))
        isl, _ = random_instance(rng, h, w, n)
        if len(slots(isl)) > 9:
            continue
        if rng.random() < 0.3:
            v = rng.choice(list(isl))
            isl[v] = rng.randint(1, 8)
        assert sorted(map(tuple, solve(isl))) == sorted(map(tuple, brute_force(isl)))
        checked += 1
