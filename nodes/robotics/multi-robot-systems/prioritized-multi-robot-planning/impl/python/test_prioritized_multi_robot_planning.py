# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/prioritized-multi-robot-planning/. The authors are listed in prov/9VT1PP.jsonl.

import itertools
import random
from collections import deque

from prioritized_multi_robot_planning import (
    check_plan,
    free_cells,
    neighbors,
    prioritized_planning,
)


def coupled_makespan(grid, starts, goals):
    """Brute force: BFS over the joint states of all robots (complete and optimal)."""
    starts, goals = tuple(starts), tuple(goals)
    dist = {starts: 0}
    queue = deque([starts])
    while queue:
        state = queue.popleft()
        if state == goals:
            return dist[state]
        for nxt in itertools.product(*[neighbors(grid, c) for c in state]):
            if len(set(nxt)) < len(nxt):
                continue
            swap = any(
                nxt[i] == state[k] and nxt[k] == state[i] and nxt[i] != state[i]
                for i in range(len(state))
                for k in range(i + 1, len(state))
            )
            if not swap and nxt not in dist:
                dist[nxt] = dist[state] + 1
                queue.append(nxt)
    return None


def bfs_length(grid, start, goal):
    dist = {start: 0}
    queue = deque([start])
    while queue:
        cell = queue.popleft()
        for nxt in neighbors(grid, cell):
            if nxt not in dist:
                dist[nxt] = dist[cell] + 1
                queue.append(nxt)
    return dist.get(goal)


POCKET = ["#.##", "...."]
POCKET_STARTS = [(1, 0), (1, 3)]
POCKET_GOALS = [(1, 3), (1, 0)]

SIDING = ["....", "..##"]
SIDING_STARTS = [(0, 2), (0, 0)]
SIDING_GOALS = [(0, 1), (0, 3)]


def test_order_matters_in_the_pocket():
    assert prioritized_planning(POCKET, POCKET_STARTS, POCKET_GOALS, [0, 1]) is None
    paths = prioritized_planning(POCKET, POCKET_STARTS, POCKET_GOALS, [1, 0])
    assert paths is not None
    assert check_plan(POCKET, POCKET_STARTS, POCKET_GOALS, paths)
    assert paths[1] == [(1, 3), (1, 2), (1, 1), (1, 0)]
    assert paths[0] == [(1, 0), (1, 1), (0, 1), (1, 1), (1, 2), (1, 3)]
    assert coupled_makespan(POCKET, POCKET_STARTS, POCKET_GOALS) == 5


def test_every_order_has_no_plan_but_a_plan_exists():
    for order in ([0, 1], [1, 0]):
        assert prioritized_planning(SIDING, SIDING_STARTS, SIDING_GOALS, order) is None
    assert coupled_makespan(SIDING, SIDING_STARTS, SIDING_GOALS) == 4


def test_one_robot_is_a_shortest_path():
    rng = random.Random(8)
    for _ in range(100):
        rows, cols = rng.randint(1, 6), rng.randint(1, 6)
        grid = ["".join("#" if rng.random() < 0.25 else "." for _ in range(cols)) for _ in range(rows)]
        cells = free_cells(grid)
        if len(cells) < 2:
            continue
        s, g = rng.sample(cells, 2)
        paths = prioritized_planning(grid, [s], [g])
        length = bfs_length(grid, s, g)
        if length is None:
            assert paths is None
        else:
            assert len(paths[0]) - 1 == length


def test_against_coupled_search():
    rng = random.Random(21)
    solved = unsolved = 0
    for _ in range(250):
        rows, cols = rng.randint(1, 3), rng.randint(2, 4)
        grid = ["".join("#" if rng.random() < 0.25 else "." for _ in range(cols)) for _ in range(rows)]
        cells = free_cells(grid)
        r = rng.randint(2, 3)
        if len(cells) < 2 * r:
            continue
        pick = rng.sample(cells, 2 * r)
        starts, goals = pick[:r], pick[r:]
        best = coupled_makespan(grid, starts, goals)
        paths = prioritized_planning(grid, starts, goals)
        if paths is None:
            unsolved += 1
            continue
        solved += 1
        assert check_plan(grid, starts, goals, paths)
        assert best is not None
        assert max(len(p) for p in paths) - 1 >= best
    assert solved > 50 and unsolved > 0


def test_conflict_checker_rejects_swaps_and_collisions():
    grid = ["..."]
    starts, goals = [(0, 0), (0, 1)], [(0, 1), (0, 0)]
    assert not check_plan(grid, starts, goals, [[(0, 0), (0, 1)], [(0, 1), (0, 0)]])
    assert not check_plan(grid, [(0, 0), (0, 2)], [(0, 1), (0, 1)], [[(0, 0), (0, 1)], [(0, 2), (0, 1)]])
