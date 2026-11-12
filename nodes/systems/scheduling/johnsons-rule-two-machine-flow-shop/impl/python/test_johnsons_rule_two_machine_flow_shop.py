# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/johnsons-rule-two-machine-flow-shop/. The authors are listed in prov/8HDKEZ.jsonl.

import itertools
import random

from johnsons_rule_two_machine_flow_shop import (
    best_permutation_makespan,
    best_schedule_makespan,
    johnson_smallest_time,
    makespan_of_orders,
)


def f2(a, b, order):
    return makespan_of_orders([a, b], [order, order])


def johnson_relation_holds(a, b, order):
    """For each pair with i before j: min(a_i, b_j) <= min(a_j, b_i)."""
    for x in range(len(order)):
        for y in range(x + 1, len(order)):
            i, j = order[x], order[y]
            if min(a[i], b[j]) > min(a[j], b[i]):
                return False
    return True


def test_example() -> None:
    a = [7, 3, 9, 4, 6]
    b = [5, 8, 2, 4, 7]
    order = johnson_smallest_time(a, b)
    assert order == [1, 3, 4, 0, 2]
    assert f2(a, b, order) == 31
    assert best_schedule_makespan([a, b]) == 31
    assert f2(a, b, [0, 1, 2, 3, 4]) == 36


def test_edges() -> None:
    assert johnson_smallest_time([], []) == []
    assert johnson_smallest_time([2], [9]) == [0]
    assert johnson_smallest_time([3, 3], [3, 3]) == [0, 1]


def test_optimal_over_all_orders() -> None:
    rng = random.Random(1954)
    for _ in range(300):
        n = rng.randrange(1, 8)
        a = [rng.randrange(0, 10) for _ in range(n)]
        b = [rng.randrange(0, 10) for _ in range(n)]
        order = johnson_smallest_time(a, b)
        assert sorted(order) == list(range(n))
        assert johnson_relation_holds(a, b, order)
        assert f2(a, b, order) == min(f2(a, b, o) for o in itertools.permutations(range(n)))


def test_optimal_over_all_schedules_two_machines() -> None:
    # independent orders on the two machines do not help
    rng = random.Random(21)
    for _ in range(40):
        n = rng.randrange(1, 6)
        a = [rng.randrange(1, 10) for _ in range(n)]
        b = [rng.randrange(1, 10) for _ in range(n)]
        assert f2(a, b, johnson_smallest_time(a, b)) == best_schedule_makespan([a, b])


def test_permutation_schedules_suffice_for_three_machines() -> None:
    rng = random.Random(31)
    for _ in range(40):
        n = rng.randrange(1, 5)
        p = [[rng.randrange(1, 8) for _ in range(n)] for _ in range(3)]
        assert best_permutation_makespan(p) == best_schedule_makespan(p)


def test_permutation_schedules_fail_for_four_machines() -> None:
    p = [[1, 4], [4, 1], [4, 1], [1, 4]]
    assert best_permutation_makespan(p) == 14
    assert best_schedule_makespan(p) == 12
    assert makespan_of_orders(p, [(0, 1), (0, 1), (1, 0), (1, 0)]) == 12


def test_relation_is_not_transitive_with_ties() -> None:
    # each adjacent pair of 0, 1, 2 satisfies the relation, the pair (0, 2) does not,
    # and the order is not optimal
    a, b = [5, 2, 3], [2, 2, 3]
    assert min(a[0], b[1]) <= min(a[1], b[0]) and min(a[1], b[2]) <= min(a[2], b[1])
    assert not johnson_relation_holds(a, b, [0, 1, 2])
    assert f2(a, b, [0, 1, 2]) == 13
    assert f2(a, b, johnson_smallest_time(a, b)) == 12
