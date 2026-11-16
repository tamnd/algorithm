# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hybrid-a-star/. The authors are listed in prov/C6X95N.jsonl.

import heapq
import math
import random

from hybrid_a_star import (
    Grid,
    dubins_segments,
    endpoint,
    hybrid_a_star,
    move,
    path_cost,
    path_free,
    wrap,
)

RHO, STEP = 2.0, 1.5


def pose_error(a, b):
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]), abs(wrap(a[2] - b[2])))


def random_map(rng, n=20, density=0.15):
    blocked = {(i, j) for i in range(n) for j in range(n) if rng.random() < density}
    return Grid(n, n, 1.0, blocked)


def random_free_pose(rng, grid):
    while True:
        x, y = rng.uniform(0, grid.nx), rng.uniform(0, grid.ny)
        if grid.free(x, y):
            return x, y, rng.uniform(-math.pi, math.pi)


def best_sequence_cost(start, goal, moves, bound, pos_tol, ang_tol, reverse_cost, switch_cost):
    """Uniform-cost search over exact poses and the last direction: the least cost of any
    sequence of the motion primitives that ends in the goal region (empty map)."""
    def at_goal(q):
        return math.hypot(q[0] - goal[0], q[1] - goal[1]) <= pos_tol and abs(wrap(q[2] - goal[2])) <= ang_tol

    def key(q, d):
        return round(q[0], 9), round(q[1], 9), round(q[2] % (2 * math.pi), 9), d

    heap = [(0.0, 0, tuple(start), 0.0)]
    seen = {}
    c = 1
    while heap:
        g, _, q, d = heapq.heappop(heap)
        if at_goal(q):
            return g
        k = key(q, d)
        if k in seen:
            continue
        seen[k] = g
        for kappa, dd in moves:
            g2 = g + STEP * (reverse_cost if dd < 0 else 1.0) + (switch_cost if d and dd != d else 0.0)
            if g2 <= bound + 1e-9:
                heapq.heappush(heap, (g2, c, move(q, kappa, dd * STEP), dd))
                c += 1
    return math.inf


def test_dubins_shot_ends_at_the_goal():
    rng = random.Random(1)
    for _ in range(2000):
        q0 = (rng.uniform(-9, 9), rng.uniform(-9, 9), rng.uniform(-math.pi, math.pi))
        q1 = (rng.uniform(-9, 9), rng.uniform(-9, 9), rng.uniform(-math.pi, math.pi))
        segs = dubins_segments(q0, q1, RHO)
        assert all(abs(k) <= 1.0 / RHO + 1e-15 and s > 0 for k, s in segs)
        assert pose_error(endpoint(q0, segs), q1) < 1e-9


def test_paths_are_free_and_drivable():
    rng = random.Random(2)
    found = 0
    for trial in range(20):
        grid = random_map(rng)
        start, goal = random_free_pose(rng, grid), random_free_pose(rng, grid)
        res = hybrid_a_star(grid, start, goal, RHO, STEP, shot_every=5, use_grid_heuristic=True, max_expansions=4000)
        if res is None:
            continue
        found += 1
        cost, segs, _ = res
        assert path_free(grid, start, segs)
        assert all(abs(k) <= 1.0 / RHO + 1e-15 for k, _ in segs)
        assert abs(path_cost(segs) - cost) < 1e-9
        end = endpoint(start, segs)
        assert math.hypot(end[0] - goal[0], end[1] - goal[1]) <= 0.5 + 1e-9
        assert abs(wrap(end[2] - goal[2])) <= 0.1 + 1e-9
    assert found >= 12


def test_cost_is_at_least_the_best_primitive_sequence():
    # Without the shot, the result is a sequence of primitives, so it cannot beat the best one.
    # With fine bins nothing is pruned that matters, and the two are equal.
    rng = random.Random(3)
    grid = Grid(40, 40, 1.0)
    moves = [(k, d) for d in (1.0, -1.0) for k in (-1.0 / RHO, 0.0, 1.0 / RHO)]
    gaps = []
    for _ in range(12):
        start = (20.0, 20.0, rng.uniform(-math.pi, math.pi))
        seq = [rng.choice(moves) for _ in range(rng.randint(2, 4))]
        goal = endpoint(start, [(k, d * STEP) for k, d in seq])
        bound = path_cost([(k, d * STEP) for k, d in seq], 2.0, 0.0)
        opt = best_sequence_cost(start, goal, moves, bound, 0.3, 0.05, 2.0, 0.0)
        assert opt <= bound + 1e-9
        fine = hybrid_a_star(grid, start, goal, RHO, STEP, n_heading=100000, bin_res=1e-3,
                             switch_cost=0.0, pos_tol=0.3, ang_tol=0.05)
        assert abs(fine[0] - opt) < 1e-9
        coarse = hybrid_a_star(grid, start, goal, RHO, STEP, n_heading=36, switch_cost=0.0,
                               pos_tol=0.3, ang_tol=0.05)
        if coarse is not None:
            assert coarse[0] >= opt - 1e-9
            gaps.append(coarse[0] - opt)
    assert gaps


def test_forward_path_is_not_shorter_than_dubins():
    # With reverse motion off, any path is a forward path of curvature at most 1 / rho, so its
    # length is at least the Dubins length between its end poses.
    rng = random.Random(4)
    for _ in range(10):
        grid = random_map(rng, density=0.08)
        start, goal = random_free_pose(rng, grid), random_free_pose(rng, grid)
        res = hybrid_a_star(grid, start, goal, RHO, STEP, reverse=False, shot_every=3,
                            use_grid_heuristic=True, max_expansions=3000)
        if res is None:
            continue
        cost, segs, _ = res
        length = sum(abs(s) for _, s in segs)
        dub = sum(s for _, s in dubins_segments(start, endpoint(start, segs), RHO))
        assert length >= dub - 1e-7


def test_shot_on_an_empty_map_is_the_dubins_path():
    grid = Grid(30, 30, 1.0)
    start, goal = (5.0, 5.0, 0.0), (20.0, 22.0, 1.0)
    cost, segs, expansions = hybrid_a_star(grid, start, goal, RHO, STEP, shot_every=1)
    assert expansions == 1
    assert pose_error(endpoint(start, segs), goal) < 1e-9
    assert abs(cost - sum(s for _, s in dubins_segments(start, goal, RHO))) < 1e-12


def test_walled_off_goal_returns_none():
    # The search runs out of cells and returns None.
    blocked = {(6, j) for j in range(12)}
    grid = Grid(12, 12, 1.0, blocked)
    assert hybrid_a_star(grid, (2.0, 6.0, 0.0), (10.0, 6.0, 0.0), RHO, STEP, n_heading=36, shot_every=4) is None
