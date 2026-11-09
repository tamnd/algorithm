# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/late-acceptance-hill-climbing/. The authors are listed in prov/ZRSAWH.jsonl.

import itertools
import random

import pytest

from late_acceptance_hill_climbing import distance_matrix, late_acceptance_hill_climbing, random_two_opt, tour_length

P8 = [(0, 0), (4, 0), (8, 1), (9, 5), (6, 8), (2, 9), (-1, 6), (3, 4)]
D8 = distance_matrix(P8)
X0 = (0, 3, 6, 1, 4, 7, 2, 5)


def f8(t: tuple[int, ...]) -> int:
    return tour_length(D8, t)


def brute_force(d: list[list[int]]) -> int:
    n = len(d)
    return min(tour_length(d, (0,) + p) for p in itertools.permutations(range(1, n)))


def test_example_of_the_page() -> None:
    best, fb, log = late_acceptance_hill_climbing(X0, f8, random_two_opt, 3, 12, random.Random(5))
    assert f8(X0) == 66
    assert [(s.v, s.f_candidate, s.c_before, s.accepted, s.fx) for s in log] == [
        (0, 60, 66, True, 60),
        (1, 61, 66, True, 61),
        (2, 56, 66, True, 56),
        (0, 61, 60, False, 56),
        (1, 57, 61, True, 57),
        (2, 50, 56, True, 50),
        (0, 53, 56, True, 53),
        (1, 49, 57, True, 49),
        (2, 49, 50, True, 49),
        (0, 52, 53, True, 52),
        (1, 44, 49, True, 44),
        (2, 50, 49, False, 44),
    ]
    assert fb == 44 and f8(best) == 44
    assert brute_force(D8) == 33
    best, fb, _ = late_acceptance_hill_climbing(X0, f8, random_two_opt, 3, 400, random.Random(5))
    assert fb == 33


def check_run(x0, f, length, log) -> None:
    costs = [f(x0)] + [s.fx for s in log]  # costs[i + 1] is the cost after iteration i
    for i, s in enumerate(log):
        assert s.v == i % length
        # the history slot holds the cost from `length` iterations earlier
        assert s.c_before == (costs[i + 1 - length] if i >= length else costs[0])
        # the acceptance rule as stated
        assert s.accepted == (s.f_candidate <= s.c_before or s.f_candidate <= costs[i])
        assert s.fx == (s.f_candidate if s.accepted else costs[i]) == f(s.x)
        # the cost never exceeds the largest of the last `length` costs before it
        assert s.fx <= max(costs[max(0, i + 1 - length) : i + 1])
        assert s.fx <= costs[0]
        if length == 1:
            assert s.fx <= costs[i]


def test_invariants_on_random_instances() -> None:
    rng = random.Random(909)
    for _ in range(300):
        n = rng.randint(4, 9)
        d = distance_matrix([(rng.randint(0, 50), rng.randint(0, 50)) for _ in range(n)])
        f = lambda t: tour_length(d, t)  # noqa: E731
        x0 = (0,) + tuple(rng.sample(range(1, n), n - 1))
        length = rng.randint(1, 30)
        best, fb, log = late_acceptance_hill_climbing(x0, f, random_two_opt, length, rng.randint(0, 300), random.Random(rng.random()))
        check_run(x0, f, length, log)
        for s in log:
            assert sorted(s.x) == list(range(n)) and s.x[0] == 0
        assert fb == f(best) == min([f(x0)] + [s.fx for s in log])


def test_edges() -> None:
    with pytest.raises(ValueError):
        late_acceptance_hill_climbing(X0, f8, random_two_opt, 0, 5, random.Random(1))
    assert late_acceptance_hill_climbing(X0, f8, random_two_opt, 4, 0, random.Random(1)) == (X0, 66, [])


def test_fixed_seed_reaches_the_optimum() -> None:
    rng = random.Random(2024)
    d = distance_matrix([(rng.randint(0, 100), rng.randint(0, 100)) for _ in range(10)])
    f = lambda t: tour_length(d, t)  # noqa: E731
    opt = brute_force(d)
    assert opt == 231
    best, fb, _ = late_acceptance_hill_climbing(tuple(range(10)), f, random_two_opt, 50, 2000, random.Random(0))
    assert fb == opt and f(best) == opt
