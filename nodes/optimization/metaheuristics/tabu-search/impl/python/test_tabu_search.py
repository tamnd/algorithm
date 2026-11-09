# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tabu-search/. The authors are listed in prov/4KBPCC.jsonl.

import itertools
import random

import pytest

from tabu_search import knapsack_moves, knapsack_objective, tabu_search

V6 = [9, 9, 12, 7, 2, 8]
W6 = [4, 3, 5, 4, 3, 4]
C6 = 15


def bits(s: str) -> tuple[int, ...]:
    return tuple(int(c) for c in s)


def brute_force(values, weights, capacity) -> int:
    n = len(values)
    f = knapsack_objective(values)
    return min(f(x) for x in itertools.product((0, 1), repeat=n) if sum(w for w, b in zip(weights, x) if b) <= capacity)


def test_example_of_the_page() -> None:
    f = knapsack_objective(V6)
    best, fb, log = tabu_search((0,) * 6, f, knapsack_moves(W6, C6), 3, 10)
    assert [(s.attribute, s.x, -s.fx, s.aspirated, s.tabu_list) for s in log] == [
        (2, bits("001000"), 12, False, [2]),
        (0, bits("101000"), 21, False, [2, 0]),
        (1, bits("111000"), 30, False, [2, 0, 1]),
        (4, bits("111010"), 32, False, [0, 1, 4]),
        (2, bits("110010"), 20, False, [1, 4, 2]),
        (5, bits("110011"), 28, False, [4, 2, 5]),
        (0, bits("010011"), 19, False, [2, 5, 0]),
        (3, bits("010111"), 26, False, [5, 0, 3]),
        (4, bits("010101"), 24, False, [0, 3, 4]),
        (0, bits("110101"), 33, True, [3, 4, 0]),
    ]
    assert (best, fb) == (bits("110101"), -33)
    assert fb == brute_force(V6, W6, C6)


def test_tenure_zero_and_edges() -> None:
    f = knapsack_objective(V6)
    # with an empty tabu list the search can cycle between two solutions
    _, _, log = tabu_search((0,) * 6, f, knapsack_moves(W6, C6), 0, 8)
    assert all(s.tabu_list == [] for s in log)
    assert log[4].x == log[6].x
    # zero iterations return the start
    assert tabu_search((0,) * 6, f, knapsack_moves(W6, C6), 3, 0) == ((0,) * 6, 0, [])
    # no allowed move: stop early
    best, fb, log = tabu_search((0,), lambda x: 0, lambda x: iter(()), 2, 5)
    assert (best, fb, log) == ((0,), 0, [])
    with pytest.raises(ValueError):
        tabu_search((0,), lambda x: 0, lambda x: iter(()), -1, 5)


def check_run(values, weights, capacity, x0, tenure, iterations) -> None:
    f = knapsack_objective(values)
    moves = knapsack_moves(weights, capacity)
    best, fb, log = tabu_search(x0, f, moves, tenure, iterations)
    x, f_best, tabu = x0, f(x0), []
    for s in log:
        # recompute the admissible moves of the current solution and the best of them
        admissible = []
        for a, y in moves(x):
            if a not in tabu or f(y) < f_best:
                admissible.append((f(y), a, y))
        assert admissible, "a move was made although none was admissible"
        least = min(c for c, _, _ in admissible)
        first = next((a, y) for c, a, y in admissible if c == least)
        assert (s.attribute, s.x) == first
        # a tabu move is made only through the aspiration criterion
        assert s.aspirated == (s.attribute in tabu)
        if s.aspirated:
            assert s.fx < f_best
        # the tabu list holds the last min(k, tenure) attributes, oldest first
        tabu = (tabu + [s.attribute])[max(0, len(tabu) + 1 - tenure) :] if tenure else []
        assert s.tabu_list == tabu and len(tabu) <= tenure
        # feasibility and the best value
        assert sum(w for w, b in zip(weights, s.x) if b) <= capacity
        assert s.fx == f(s.x)
        assert s.f_best == min(f_best, s.fx) <= f_best
        x, f_best = s.x, s.f_best
    assert fb == f(best) == f_best == min([f(x0)] + [s.fx for s in log])
    if len(log) < iterations:
        assert all(a in tabu and f(y) >= f_best for a, y in moves(x))


def test_invariants_on_random_instances() -> None:
    rng = random.Random(4242)
    for _ in range(500):
        n = rng.randint(1, 8)
        values = [rng.randint(1, 15) for _ in range(n)]
        weights = [rng.randint(1, 8) for _ in range(n)]
        capacity = rng.randint(0, sum(weights))
        tenure = rng.randint(0, n + 1)
        check_run(values, weights, capacity, (0,) * n, tenure, rng.randint(0, 25))


def descent_path(x, f, moves) -> list:
    """Best-improvement hill climbing: the path of solutions after the start."""
    path = []
    while True:
        cand = [(f(y), y) for _, y in moves(x)]
        least = min((c for c, _ in cand), default=None)
        if least is None or least >= f(x):
            return path
        x = next(y for c, y in cand if c == least)
        path.append(x)


def test_starts_with_the_hill_climbing_descent() -> None:
    rng = random.Random(77)
    for _ in range(300):
        n = rng.randint(1, 8)
        values = [rng.randint(1, 15) for _ in range(n)]
        weights = [rng.randint(1, 8) for _ in range(n)]
        capacity = rng.randint(0, sum(weights))
        f, moves = knapsack_objective(values), knapsack_moves(weights, capacity)
        path = descent_path((0,) * n, f, moves)
        _, fb, log = tabu_search((0,) * n, f, moves, rng.randint(0, n), len(path) + 5)
        assert [s.x for s in log[: len(path)]] == path
        assert fb <= (f(path[-1]) if path else 0)


def test_fixed_seed_reaches_the_optimum() -> None:
    rng = random.Random(10)
    values = [rng.randint(5, 40) for _ in range(10)]
    weights = [rng.randint(3, 20) for _ in range(10)]
    capacity = sum(weights) // 2
    opt = brute_force(values, weights, capacity)
    best, fb, _ = tabu_search((0,) * 10, knapsack_objective(values), knapsack_moves(weights, capacity), 3, 50)
    assert fb == opt
    assert sum(w for w, b in zip(weights, best) if b) <= capacity
