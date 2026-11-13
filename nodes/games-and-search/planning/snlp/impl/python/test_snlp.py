# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/snlp/. The authors are listed in prov/K3AVD8.jsonl.

import random
from collections import Counter, deque

from snlp import (SUSSMAN_GOAL, SUSSMAN_INIT, complete_plans, is_plan, make_action, move_actions, snlp, successor)


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


def sequences(plan):
    return {tuple(a.name for a in plan.actions(o)) for o in plan.linearizations()}


# The task of the page: A makes p, and R and S each need p.
A = make_action("A", [], ["p"], [])
R = make_action("R", ["p"], ["r"], [])
S = make_action("S", ["p"], ["s"], [])


def test_sussman_anomaly():
    plan = snlp(SUSSMAN_INIT, SUSSMAN_GOAL, move_actions("abc"))
    orders = list(plan.linearizations())
    assert [[a.name for a in plan.actions(o)] for o in orders] == [["move(c,a,table)", "move(b,table,c)", "move(a,table,b)"]]
    assert all_valid(plan, SUSSMAN_INIT, SUSSMAN_GOAL)


def test_existence_and_length_agree_with_bfs():
    rng = random.Random(21)
    solvable = unsolvable = 0
    for k in range(400):
        init, goal, acts = random_task(rng, 3 + k % 2, rng.randint(2, 6))
        best = bfs_length(init, goal, acts)
        plan = snlp(init, goal, acts)
        if best is None:
            assert plan is None
            unsolvable += 1
        else:
            assert len(plan.steps) - 2 == best
            assert all_valid(plan, init, goal)
            solvable += 1
    assert solvable > 100 and unsolvable > 100


def test_no_partial_plan_is_visited_twice():
    rng = random.Random(22)
    total = 0
    for _ in range(200):
        init, goal, acts = random_task(rng, 4, rng.randint(2, 5))
        seen = Counter()
        complete_plans(init, goal, acts, 4, visit=lambda p: seen.update([p.canonical()]))
        assert all(c == 1 for c in seen.values())
        total += len(seen)
    seen = Counter()
    complete_plans(SUSSMAN_INIT, SUSSMAN_GOAL, move_actions("abc"), 3, visit=lambda p: seen.update([p.canonical()]))
    assert all(c == 1 for c in seen.values())
    assert total > 1000


def test_complete_plans_have_disjoint_linearizations():
    rng = random.Random(23)
    pop_overlaps = 0
    for _ in range(200):
        init, goal, acts = random_task(rng, 4, rng.randint(2, 5))
        for systematic in (True, False):
            plans = complete_plans(init, goal, acts, 4, systematic)
            for p in plans:
                assert all_valid(p, init, goal)
            count = Counter()
            for p in plans:
                count.update(sequences(p))
            if systematic:
                assert all(c == 1 for c in count.values())
            elif any(c > 1 for c in count.values()):
                pop_overlaps += 1
    assert pop_overlaps > 10


def test_page_example():
    snlp_plans = complete_plans([], ["p", "r", "s"], [A, R, S], 4)
    pop_plans = complete_plans([], ["p", "r", "s"], [A, R, S], 4, systematic=False)
    assert len(snlp_plans) == len(pop_plans) == 4
    snlp_count, pop_count = Counter(), Counter()
    for p in snlp_plans:
        snlp_count.update(sequences(p))
    for p in pop_plans:
        pop_count.update(sequences(p))
    assert set(snlp_count) <= set(pop_count)
    assert max(snlp_count.values()) == 1 and sum(snlp_count.values()) == 6
    assert sum(pop_count.values()) == 16 and len(pop_count) == 8
    assert pop_count[("A", "A", "R", "S")] == 3


def test_adder_is_a_threat():
    plan = snlp([], ["p", "r", "s"], [A, R, S])
    assert len(plan.steps) - 2 == 3
    assert sequences(plan) == {("A", "R", "S"), ("A", "S", "R")}
