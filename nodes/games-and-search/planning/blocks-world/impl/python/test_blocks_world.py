# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/blocks-world/. The authors are listed in prov/KD4S9R.jsonl.

import math
import random

from blocks_world import (
    arrangements,
    bfs_plan,
    blocks_world_actions,
    blocks_world_state,
    in_position,
    is_plan,
    move_actions,
    move_state,
    random_stacks,
    reachable,
    table_then_build,
)


def full_goal(stacks):
    return frozenset(f for f in move_state(stacks) if f[0] in ("on", "ontable"))


def lah_sum(n):
    # Lah numbers L(n, k) = C(n - 1, k - 1) n! / k! count arrangements into exactly k stacks.
    if n == 0:
        return 1
    return sum(math.comb(n - 1, k - 1) * math.factorial(n) // math.factorial(k) for k in range(1, n + 1))


def test_arrangement_counts():
    assert [arrangements(n) for n in range(7)] == [1, 1, 3, 13, 73, 501, 4051]
    assert all(arrangements(n) == lah_sum(n) for n in range(12))


def test_reachable_state_counts():
    for n in range(1, 6):
        blocks = "abcde"[:n]
        start = [list(blocks)]
        assert len(reachable(move_state(start), move_actions(blocks))) == arrangements(n)
        assert len(reachable(blocks_world_state(start), blocks_world_actions(blocks))) == arrangements(n) + n * arrangements(n - 1)


def test_two_encodings_agree_on_full_goals():
    rng = random.Random(11)
    blocks = "abcd"
    m, h = move_actions(blocks), blocks_world_actions(blocks)
    for _ in range(20):
        start, target = random_stacks(blocks, rng), random_stacks(blocks, rng)
        goal = full_goal(target)
        moves = bfs_plan(move_state(start), goal, m)
        hand = bfs_plan(blocks_world_state(start), goal, h)
        assert len(hand) == 2 * len(moves)


def test_table_then_build_is_within_factor_two():
    rng = random.Random(3)
    worst = 0.0
    for n in (3, 4, 5):
        blocks = "abcde"[:n]
        acts = move_actions(blocks)
        for _ in range(25):
            start, target = random_stacks(blocks, rng), random_stacks(blocks, rng)
            goal = full_goal(target)
            init = move_state(start)
            plan = table_then_build(start, target, blocks)
            assert is_plan(init, goal, plan)
            opt = len(bfs_plan(init, goal, acts))
            misplaced = n - len(in_position(start, target))
            assert misplaced <= opt <= len(plan) <= 2 * misplaced
            if opt:
                worst = max(worst, len(plan) / opt)
    assert worst <= 2


def test_sussman_instance():
    start, target = [["a", "c"], ["b"]], [["c", "b", "a"]]
    plan = table_then_build(start, target, "abc")
    assert [a.name for a in plan] == ["move(c,a,table)", "move(b,table,c)", "move(a,table,b)"]
