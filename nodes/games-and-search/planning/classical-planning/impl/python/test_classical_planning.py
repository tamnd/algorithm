# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/classical-planning/. The authors are listed in prov/M1BM1K.jsonl.

import random

from classical_planning import (
    bfs_plan,
    blocks_world_actions,
    blocks_world_state,
    brute_force_shortest,
    is_plan,
    move_actions,
    move_state,
    random_stacks,
    reachable,
)


def goal_of(stacks):
    """The goal of a full arrangement: every on and ontable fact of it."""
    return frozenset(f for f in move_state(stacks) if f[0] in ("on", "ontable"))


def test_sussman_lengths():
    init = move_state([["a", "c"], ["b"]])
    goal = frozenset({("on", "a", "b"), ("on", "b", "c")})
    plan = bfs_plan(init, goal, move_actions("abc"))
    assert [a.name for a in plan] == ["move(c,a,table)", "move(b,table,c)", "move(a,table,b)"]
    init4 = blocks_world_state([["a", "c"], ["b"]])
    plan4 = bfs_plan(init4, goal, blocks_world_actions("abc"))
    assert len(plan4) == 6
    assert brute_force_shortest(init4, goal, blocks_world_actions("abc"), 6) == 6


def test_bfs_is_shortest_against_brute_force():
    rng = random.Random(2024)
    for _ in range(40):
        blocks = "abc"
        start, target = random_stacks(blocks, rng), random_stacks(blocks, rng)
        goal = goal_of(target)
        for acts, init in ((move_actions(blocks), move_state(start)), (blocks_world_actions(blocks), blocks_world_state(start))):
            plan = bfs_plan(init, goal, acts)
            assert plan is not None
            assert is_plan(init, goal, plan)
            assert brute_force_shortest(init, goal, acts, len(plan)) == len(plan)


def test_partial_goals_four_blocks():
    rng = random.Random(5)
    blocks = "abcd"
    acts = move_actions(blocks)
    checked = 0
    while checked < 15:
        start, target = random_stacks(blocks, rng), random_stacks(blocks, rng)
        facts = sorted(goal_of(target))
        goal = frozenset(rng.sample(facts, 2))
        init = move_state(start)
        plan = bfs_plan(init, goal, acts)
        if plan is None or len(plan) > 4:
            continue
        assert is_plan(init, goal, plan)
        assert brute_force_shortest(init, goal, acts, len(plan)) == len(plan)
        checked += 1


def test_unsolvable_goal():
    init = move_state([["a"], ["b"]])
    goal = frozenset({("on", "a", "b"), ("on", "b", "a")})
    acts = move_actions("ab")
    assert bfs_plan(init, goal, acts) is None
    assert all(not goal <= s for s in reachable(init, acts))
    assert brute_force_shortest(init, goal, acts, 4) is None


def test_empty_plan_when_goal_holds():
    init = move_state([["a", "b"]])
    assert bfs_plan(init, frozenset({("on", "b", "a")}), move_actions("ab")) == []
