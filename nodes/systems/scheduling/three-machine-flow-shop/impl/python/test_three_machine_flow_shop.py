# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/three-machine-flow-shop/. The authors are listed in prov/F4DF7W.jsonl.

import random

from three_machine_flow_shop import (
    best_order_makespan,
    johnson_three_machine,
    makespan3,
    middle_is_dominated,
)


def test_example_dominated() -> None:
    a = [7, 2, 5, 3, 6]
    b = [4, 1, 3, 2, 4]
    c = [4, 6, 5, 7, 4]
    assert middle_is_dominated(a, b, c)
    order = johnson_three_machine(a, b, c)
    assert order == [1, 3, 2, 0, 4]
    assert makespan3(a, b, c, order) == 31
    assert best_order_makespan(a, b, c) == 31
    assert makespan3(a, b, c, [0, 1, 2, 3, 4]) == 37


def test_counterexample_outside_the_condition() -> None:
    a, b, c = [1, 1], [5, 4], [5, 2]
    assert not middle_is_dominated(a, b, c)
    order = johnson_three_machine(a, b, c)
    assert order == [1, 0]
    assert makespan3(a, b, c, order) == 15
    assert makespan3(a, b, c, [0, 1]) == 13 == best_order_makespan(a, b, c)


def test_edges() -> None:
    assert johnson_three_machine([], [], []) == []
    assert makespan3([], [], [], []) == 0
    assert makespan3([2], [3], [4], [0]) == 9


def test_dominated_middle_against_brute_force() -> None:
    rng = random.Random(1976)
    for _ in range(400):
        n = rng.randrange(1, 7)
        b = [rng.randrange(0, 6) for _ in range(n)]
        hi = max(b)
        big = [rng.randrange(hi, hi + 8) for _ in range(n)]
        other = [rng.randrange(0, 10) for _ in range(n)]
        a, c = (big, other) if rng.random() < 0.5 else (other, big)
        assert middle_is_dominated(a, b, c)
        order = johnson_three_machine(a, b, c)
        assert sorted(order) == list(range(n))
        assert makespan3(a, b, c, order) == best_order_makespan(a, b, c)


def test_reduction_is_a_heuristic_in_general() -> None:
    rng = random.Random(3)
    worse = 0
    for _ in range(300):
        n = rng.randrange(2, 6)
        a, b, c = ([rng.randrange(1, 7) for _ in range(n)] for _ in range(3))
        got = makespan3(a, b, c, johnson_three_machine(a, b, c))
        best = best_order_makespan(a, b, c)
        assert got >= best
        worse += got > best
    assert worse > 0
