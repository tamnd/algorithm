# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fast-forward-planner/. The authors are listed in prov/RWBN9P.jsonl.

import math
import random
from collections import deque

from fast_forward_planner import Action, Task, enforced_hill_climbing, ff, greedy_best_first


def act(name, pre, add, dele=()):
    return Action(name, frozenset(pre), frozenset(add), frozenset(dele))


def valid(actions, init, goal, plan):
    s = frozenset(init)
    for a in plan:
        if a not in actions or not a.pre <= s:
            return False
        s = (s - a.dele) | a.add
    return frozenset(goal) <= s


def shortest_plan_length(actions, init, goal):
    """Breadth-first search over all reachable states; math.inf when there is no plan."""
    init, goal = frozenset(init), frozenset(goal)
    dist, q = {init: 0}, deque([init])
    while q:
        s = q.popleft()
        if goal <= s:
            return dist[s]
        for a in actions:
            if a.pre <= s:
                t = (s - a.dele) | a.add
                if t not in dist:
                    dist[t] = dist[s] + 1
                    q.append(t)
    return math.inf


def random_task(rng):
    nf = rng.randint(4, 8)
    facts = list(range(nf))
    acts = []
    for i in range(rng.randint(4, 8)):
        pre = rng.sample(facts, rng.randint(0, 2))
        add = rng.sample(facts, rng.randint(1, 2))
        dele = rng.sample([f for f in facts if f not in add], rng.randint(0, 2))
        acts.append(act(("a", i), pre, add, dele))
    return acts, frozenset(rng.sample(facts, rng.randint(1, nf // 2))), frozenset(rng.sample(facts, rng.randint(1, 3)))


def blocks(names):
    acts = []
    for x in names:
        acts.append(act(("pickup", x), [("clear", x), ("ontable", x), "he"], [("holding", x)],
                        [("clear", x), ("ontable", x), "he"]))
        acts.append(act(("putdown", x), [("holding", x)], [("clear", x), ("ontable", x), "he"], [("holding", x)]))
        for y in names:
            if x != y:
                acts.append(act(("stack", x, y), [("holding", x), ("clear", y)],
                                [("on", x, y), ("clear", x), "he"], [("holding", x), ("clear", y)]))
                acts.append(act(("unstack", x, y), [("on", x, y), ("clear", x), "he"],
                                [("holding", x), ("clear", y)], [("on", x, y), ("clear", x), "he"]))
    init = frozenset([("ontable", x) for x in names] + [("clear", x) for x in names] + ["he"])
    return acts, init


def gripper(balls):
    rooms, hands = ["A", "B"], ["left", "right"]
    acts = [act(("move", r, q), [("robby", r)], [("robby", q)], [("robby", r)]) for r in rooms for q in rooms if r != q]
    for b in balls:
        for r in rooms:
            for g in hands:
                acts.append(act(("pick", b, r, g), [("at", b, r), ("robby", r), ("free", g)], [("carry", b, g)],
                                [("at", b, r), ("free", g)]))
                acts.append(act(("drop", b, r, g), [("carry", b, g), ("robby", r)], [("at", b, r), ("free", g)],
                                [("carry", b, g)]))
    init = frozenset([("robby", "A"), ("free", "left"), ("free", "right")] + [("at", b, "A") for b in balls])
    return acts, init, frozenset(("at", b, "B") for b in balls)


def trap_task():
    acts = [act(("r", i), [("r", i)], [("r", i + 1)], [("r", i)]) for i in range(4)]
    acts.append(act("finish_route", [("r", 4)], ["g"], [("r", 4)]))
    acts.append(act("to_trap", [("r", 0)], ["u"], [("r", 0)]))
    acts.append(act("ap", ["u"], ["p"], ["u"]))
    acts.append(act("aq", ["u"], ["q"], ["u"]))
    acts.append(act("finish", ["p", "q"], ["g"]))
    return acts, frozenset([("r", 0)]), frozenset(["g"])


def test_random_tasks_against_breadth_first_search():
    fallbacks = solvable = 0
    for seed in range(600):
        rng = random.Random(seed)
        acts, init, goal = random_task(rng)
        stats = {}
        plan = ff(acts, init, goal, stats)
        best = shortest_plan_length(acts, init, goal)
        assert (plan is None) == (best == math.inf)
        if plan is not None:
            solvable += 1
            assert valid(acts, init, goal, plan) and len(plan) >= best
            fallbacks += stats["phase"] == "best-first search"
    assert solvable > 300 and fallbacks > 0


def test_dead_end_task_needs_the_fallback():
    acts, init, goal = trap_task()
    task = Task(acts, init, goal)
    assert enforced_hill_climbing(task) is None
    stats = {}
    plan = ff(acts, init, goal, stats)
    assert stats["phase"] == "best-first search"
    assert valid(acts, init, goal, plan) and len(plan) == 5


def test_helpful_actions_can_cut_every_plan():
    # Hoffmann and Nebel (2001), Section 6.1.1. The task has no dead ends.
    acts = [act("opA1", [], ["A"], ["B"]), act("opA2", ["PA"], ["A"]), act("opPA", [], ["PA"]),
            act("opB1", [], ["B"], ["A"]), act("opB2", ["PB"], ["B"]), act("opPB", [], ["PB"])]
    init, goal = frozenset(["B"]), frozenset(["A", "B"])
    task = Task(acts, init, goal, added_goal_deletion=False)
    assert [a.name for a in task.helpful_actions(init)] == ["opA1"]
    assert [a.name for a in task.helpful_actions(frozenset(["A"]))] == ["opB1"]
    assert enforced_hill_climbing(task) is None
    assert enforced_hill_climbing(Task(acts, init, goal)) is None
    stats = {}
    plan = ff(acts, init, goal, stats)
    assert stats["phase"] == "best-first search" and valid(acts, init, goal, plan)


def test_added_goal_deletion_can_cut_every_plan():
    # Hoffmann and Nebel (2001), Section 6.2.1: the goal A must be deleted and achieved again.
    acts = [act("opA", [], ["A"]), act("opB", ["A"], ["B"], ["A"])]
    init, goal = frozenset(), frozenset(["A", "B"])
    assert enforced_hill_climbing(Task(acts, init, goal)) is None
    without = enforced_hill_climbing(Task(acts, init, goal, added_goal_deletion=False))
    assert [a.name for a in without] == ["opA", "opB", "opA"]
    stats = {}
    plan = ff(acts, init, goal, stats)
    assert stats["phase"] == "best-first search"
    assert [a.name for a in plan] == ["opA", "opB", "opA"]


def test_added_goal_deletion_fixes_the_blocks_world_goal_order():
    acts, init = blocks(["A", "B", "C"])
    goal = frozenset([("on", "A", "B"), ("on", "B", "C")])
    stats = {}
    plan = ff(acts, init, goal, stats)
    assert stats["phase"] == "enforced hill climbing"
    assert [a.name for a in plan] == [("pickup", "B"), ("stack", "B", "C"), ("pickup", "A"), ("stack", "A", "B")]
    assert len(enforced_hill_climbing(Task(acts, init, goal, added_goal_deletion=False))) == 8
    acts, init = blocks(["A", "B", "C", "D"])
    goal = frozenset([("on", "A", "B"), ("on", "B", "C"), ("on", "C", "D")])
    plan = ff(acts, init, goal)
    assert valid(acts, init, goal, plan) and len(plan) == shortest_plan_length(acts, init, goal) == 6


def test_gripper_helpful_actions():
    acts, init, goal = gripper(["b1", "b2"])
    task = Task(acts, init, goal)
    holding = frozenset([("robby", "A"), ("carry", "b1", "left"), ("carry", "b2", "right")])
    assert len(list(task.successors(holding))) == 3
    assert [a.name for a in task.helpful_actions(holding)] == [("move", "A", "B")]
    assert [a.name for a, _ in task.pruned_successors(holding)] == [("move", "A", "B")]
    plan = ff(acts, init, goal)
    assert valid(acts, init, goal, plan) and len(plan) == shortest_plan_length(acts, init, goal) == 5


def test_best_first_search_alone_is_complete():
    for seed in range(200):
        rng = random.Random(5000 + seed)
        acts, init, goal = random_task(rng)
        plan = greedy_best_first(Task(acts, init, goal))
        assert (plan is None) == (shortest_plan_length(acts, init, goal) == math.inf)
        assert plan is None or valid(acts, init, goal, plan)
