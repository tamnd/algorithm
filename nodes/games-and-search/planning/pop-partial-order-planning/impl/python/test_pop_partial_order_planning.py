# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pop-partial-order-planning/. The authors are listed in prov/7EP2KY.jsonl.

import random
from collections import deque

from pop_partial_order_planning import (SUSSMAN_GOAL, SUSSMAN_INIT, PartialPlan, is_plan, make_action, move_actions, pop,
                                        refine, successor, useful_actions)


def bfs_length(init, goal, actions):
    """Reference: the length of a shortest plan by breadth-first search over all reachable states."""
    init, goal = frozenset(init), frozenset(goal)
    dist = {init: 0}
    queue = deque([init])
    while queue:
        s = queue.popleft()
        if goal <= s:
            return dist[s]
        for a in actions:
            if a.pre <= s:
                t = successor(s, a)
                if t not in dist:
                    dist[t] = dist[s] + 1
                    queue.append(t)
    return None


def random_task(rng, n_facts, n_actions):
    facts = list(range(n_facts))
    acts = []
    for k in range(n_actions):
        pre = rng.sample(facts, rng.randint(0, 2))
        add = rng.sample(facts, rng.randint(1, 2))
        delete = [f for f in rng.sample(facts, rng.randint(0, 2)) if f not in add]
        acts.append(make_action(f"a{k}", pre, add, delete))
    init = frozenset(f for f in facts if rng.random() < 0.4)
    goal = frozenset(rng.sample(facts, rng.randint(1, 3)))
    return init, goal, acts


def all_valid(plan, init, goal):
    orders = list(plan.linearizations())
    return bool(orders) and all(is_plan(init, goal, plan.actions(o)) for o in orders)


def gripper(balls):
    acts = []
    for room, other in (("A", "B"), ("B", "A")):
        acts.append(make_action(f"move({room},{other})", [("at-robby", room)], [("at-robby", other)], [("at-robby", room)]))
        for b in balls:
            for g in ("left", "right"):
                acts.append(make_action(f"pick({b},{room},{g})", [("at", b, room), ("at-robby", room), ("free", g)],
                                        [("carry", b, g)], [("at", b, room), ("free", g)]))
                acts.append(make_action(f"drop({b},{room},{g})", [("carry", b, g), ("at-robby", room)],
                                        [("at", b, room), ("free", g)], [("carry", b, g)]))
    init = frozenset([("at-robby", "A"), ("free", "left"), ("free", "right")] + [("at", b, "A") for b in balls])
    goal = frozenset(("at", b, "B") for b in balls)
    return init, goal, acts


def test_sussman_anomaly():
    plan = pop(SUSSMAN_INIT, SUSSMAN_GOAL, move_actions("abc"))
    assert plan is not None and len(plan.steps) == 5
    orders = list(plan.linearizations())
    assert len(orders) == 1
    assert [a.name for a in plan.actions(orders[0])] == ["move(c,a,table)", "move(b,table,c)", "move(a,table,b)"]
    assert all_valid(plan, SUSSMAN_INIT, SUSSMAN_GOAL)


def test_four_blocks():
    acts = move_actions("abcd")
    init = frozenset({("on", "a", "b"), ("on", "b", "c"), ("ontable", "c"), ("ontable", "d"), ("clear", "a"), ("clear", "d")})
    goal = frozenset({("on", "d", "c"), ("on", "c", "b")})
    plan = pop(init, goal, acts, max_steps=6)
    assert plan is not None
    assert len(plan.steps) - 2 == bfs_length(init, goal, acts)
    assert all_valid(plan, init, goal)


def test_gripper_is_a_true_partial_order():
    init, goal, acts = gripper(["b1"])
    plan = pop(init, goal, acts, max_steps=4)
    assert len(plan.steps) - 2 == bfs_length(init, goal, acts) == 3
    assert all_valid(plan, init, goal)
    init, goal, acts = gripper(["b1", "b2"])
    plan = pop(init, goal, acts, max_steps=6)
    assert len(plan.steps) - 2 == bfs_length(init, goal, acts) == 5
    assert all_valid(plan, init, goal)
    assert len(list(plan.linearizations())) > 1


def test_existence_and_length_agree_with_bfs():
    rng = random.Random(11)
    solvable = unsolvable = 0
    for k in range(400):
        init, goal, acts = random_task(rng, 3 + k % 2, rng.randint(2, 6))
        best = bfs_length(init, goal, acts)
        plan = pop(init, goal, acts)
        if best is None:
            assert plan is None
            unsolvable += 1
        else:
            assert plan is not None
            assert len(plan.steps) - 2 == best
            assert all_valid(plan, init, goal)
            solvable += 1
    assert solvable > 100 and unsolvable > 100


def test_useless_actions_are_dropped():
    keep = make_action("keep", [1], [0], [1])
    idle = make_action("idle", [0, 1], [0], [1])
    blocked = make_action("blocked", [2], [3], [])
    assert [a.name for a in useful_actions(frozenset([1]), [keep, idle, blocked])] == ["keep"]


def test_every_plan_in_the_search_is_a_solution():
    rng = random.Random(12)
    for _ in range(60):
        init, goal, acts = random_task(rng, 4, 4)
        for plan in refine(PartialPlan(init, goal), acts, 3):
            assert all_valid(plan, init, goal)


def test_a_threat_needs_promotion():
    # a1 makes q but destroys p; the goal needs both, so a1 must come before a2.
    a1 = make_action("a1", [], ["q"], ["p"])
    a2 = make_action("a2", [], ["p"], [])
    plan = pop(["p"], ["p", "q"], [a1, a2])
    assert [a.name for a in plan.one_linearization()] == ["a1", "a2"]
    assert pop(["p"], ["p", "q"], [a1]) is None
