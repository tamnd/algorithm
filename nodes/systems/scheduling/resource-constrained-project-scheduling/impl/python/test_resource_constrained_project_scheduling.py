# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/resource-constrained-project-scheduling/. The authors are listed in prov/NND7DR.jsonl.

import itertools
import random

from resource_constrained_project_scheduling import (
    is_feasible,
    latest_finish_times,
    makespan,
    serial_sgs,
    serial_sgs_lft,
)


def exact_optimum(p, arcs, r, cap):
    """The least makespan, by a search over integer start times for T = 0, 1, 2, ...

    Integer data admit an optimal schedule with integer start times, so the search
    is exact. It does not use the schedule generation scheme."""
    n = len(p)
    pred = [[] for _ in range(n)]
    for i, j in arcs:
        pred[j].append(i)
    order = []
    while len(order) < n:  # any topological order
        order.append(next(j for j in range(n) if j not in order and all(i in order for i in pred[j])))
    horizon = sum(p)
    for T in range(horizon + 1):
        use = [[0] * len(cap) for _ in range(T + 1)]
        start = [0] * n

        def place(idx):
            if idx == n:
                return True
            j = order[idx]
            lo = max((start[i] + p[i] for i in pred[j]), default=0)
            for s in range(lo, T - p[j] + 1):
                if all(use[t][k] + r[j][k] <= cap[k] for t in range(s, s + p[j]) for k in range(len(cap))):
                    for t in range(s, s + p[j]):
                        for k in range(len(cap)):
                            use[t][k] += r[j][k]
                    start[j] = s
                    if place(idx + 1):
                        return True
                    for t in range(s, s + p[j]):
                        for k in range(len(cap)):
                            use[t][k] -= r[j][k]
            return False

        if place(0):
            return T
    raise AssertionError("no schedule within the horizon")


def all_lists(n, arcs):
    for perm in itertools.permutations(range(n)):
        pos = {j: x for x, j in enumerate(perm)}
        if all(pos[i] < pos[j] for i, j in arcs):
            yield perm


def random_instance(rng, n, kinds=1):
    p = [rng.randrange(1, 5) for _ in range(n)]
    arcs = [(i, j) for i in range(n) for j in range(i + 1, n) if rng.random() < 0.3]
    cap = [rng.randrange(2, 5) for _ in range(kinds)]
    r = [[rng.randrange(0, c + 1) for c in cap] for _ in range(n)]
    return p, arcs, r, cap


# the example of the page: activities A, B, C, D = 0, 1, 2, 3, one resource of 4 units
P = [4, 3, 4, 1]
ARCS = [(1, 2), (2, 3)]
R = [[3], [1], [2], [0]]
CAP = [4]


def test_example() -> None:
    assert latest_finish_times(P, ARCS) == [8, 3, 7, 8]
    start = serial_sgs_lft(P, ARCS, R, CAP)
    assert is_feasible(P, ARCS, R, CAP, start) is None
    assert start == [7, 0, 3, 7]
    assert makespan(P, start) == 11
    assert exact_optimum(P, ARCS, R, CAP) == 9
    best = serial_sgs(P, ARCS, R, CAP, [0, 1, 2, 3])
    assert best == [0, 0, 4, 8] and makespan(P, best) == 9


def test_lft_is_optimal_on_a_second_instance() -> None:
    p = [3, 2, 4, 2, 3, 2, 1]
    arcs = [(0, 3), (1, 4), (2, 5), (3, 6), (4, 6), (5, 6)]
    r = [[2], [3], [2], [2], [1], [3], [1]]
    start = serial_sgs_lft(p, arcs, r, [4])
    assert is_feasible(p, arcs, r, [4], start) is None
    assert makespan(p, start) == exact_optimum(p, arcs, r, [4]) == 10


def test_edges() -> None:
    assert serial_sgs_lft([], [], [], [1]) == []
    assert serial_sgs_lft([3], [], [[1]], [1]) == [0]
    # two activities that do not fit together run one after the other
    assert serial_sgs_lft([2, 3], [], [[2], [2]], [3]) == [0, 2]
    # a zero-length activity needs no free capacity
    assert serial_sgs_lft([2, 0], [], [[1], [1]], [1]) == [0, 0]
    assert serial_sgs_lft([2, 0, 1], [(0, 1), (1, 2)], [[1], [1], [1]], [1]) == [0, 2, 2]


def test_every_schedule_is_feasible() -> None:
    rng = random.Random(1996)
    for _ in range(200):
        n = rng.randrange(1, 9)
        p, arcs, r, cap = random_instance(rng, n, kinds=rng.randrange(1, 3))
        start = serial_sgs_lft(p, arcs, r, cap)
        assert is_feasible(p, arcs, r, cap, start) is None
        for lst in itertools.islice(all_lists(n, arcs), 20):
            assert is_feasible(p, arcs, r, cap, serial_sgs(p, arcs, r, cap, lst)) is None


def test_some_list_is_optimal() -> None:
    # the serial SGS makes active schedules, and some active schedule is optimal
    rng = random.Random(42)
    hits = 0
    for _ in range(60):
        n = rng.randrange(1, 6)
        p, arcs, r, cap = random_instance(rng, n)
        best = exact_optimum(p, arcs, r, cap)
        assert min(makespan(p, serial_sgs(p, arcs, r, cap, lst)) for lst in all_lists(n, arcs)) == best
        got = makespan(p, serial_sgs_lft(p, arcs, r, cap))
        assert got >= best
        hits += got == best
    assert hits > 0
