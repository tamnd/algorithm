# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/graphplan/. The authors are listed in prov/RD7TS9.jsonl.

import random
from collections import deque
from itertools import combinations

from graphplan import Action, graphplan, interfere, linearize


def act(name, pre, add, dele=()):
    return Action(name, frozenset(pre), frozenset(add), frozenset(dele))


def blocks(names):
    acts = []
    for x in names:
        acts.append(act(("pickup", x), [("clear", x), ("ontable", x), "handempty"], [("holding", x)],
                        [("clear", x), ("ontable", x), "handempty"]))
        acts.append(act(("putdown", x), [("holding", x)], [("clear", x), ("ontable", x), "handempty"], [("holding", x)]))
        for y in names:
            if x != y:
                acts.append(act(("stack", x, y), [("holding", x), ("clear", y)],
                                [("on", x, y), ("clear", x), "handempty"], [("holding", x), ("clear", y)]))
                acts.append(act(("unstack", x, y), [("on", x, y), ("clear", x), "handempty"],
                                [("holding", x), ("clear", y)], [("on", x, y), ("clear", x), "handempty"]))
    return acts


def table(names):
    return frozenset([("ontable", x) for x in names] + [("clear", x) for x in names] + ["handempty"])


def gripper(balls):
    acts = []
    for r, r2 in (("a", "b"), ("b", "a")):
        acts.append(act(("move", r, r2), [("robby", r)], [("robby", r2)], [("robby", r)]))
        for b in balls:
            for h in ("left", "right"):
                acts.append(act(("pick", b, r, h), [("at", b, r), ("robby", r), ("free", h)],
                                [("carry", b, h)], [("at", b, r), ("free", h)]))
                acts.append(act(("drop", b, r, h), [("carry", b, h), ("robby", r)],
                                [("at", b, r), ("free", h)], [("carry", b, h)]))
    init = frozenset([("robby", "a"), ("free", "left"), ("free", "right")] + [("at", b, "a") for b in balls])
    return acts, init, frozenset(("at", b, "b") for b in balls)


def logistics():
    acts = []
    for l, l2 in (("l1", "l2"), ("l2", "l1")):
        acts.append(act(("drive", l, l2), [("truck", l)], [("truck", l2)], [("truck", l)]))
        for p in ("p1", "p2"):
            acts.append(act(("load", p, l), [("at", p, l), ("truck", l)], [("in", p)], [("at", p, l)]))
            acts.append(act(("unload", p, l), [("in", p), ("truck", l)], [("at", p, l)], [("in", p)]))
    init = frozenset([("truck", "l1"), ("at", "p1", "l1"), ("at", "p2", "l1")])
    return acts, init, frozenset([("at", "p1", "l2"), ("at", "p2", "l2")])


def random_task(rng, nf, na):
    facts = list(range(nf))
    acts = []
    for i in range(na):
        pre = rng.sample(facts, rng.randint(0, 2))
        add = rng.sample(facts, rng.randint(1, 2))
        dele = rng.sample([f for f in facts if f not in add], rng.randint(0, 2))
        acts.append(act(("a", i), pre, add, dele))
    init = frozenset(rng.sample(facts, rng.randint(1, nf // 2)))
    goal = frozenset(rng.sample(facts, rng.randint(1, 3)))
    return acts, init, goal


def valid_parallel(actions, init, goal, plan):
    """Every step is applicable and pairwise non-interfering, and the goal holds at the end."""
    s = init
    for step in plan:
        assert all(a in actions for a in step)
        assert all(a.pre <= s for a in step)
        assert not any(interfere(a, b) for a, b in combinations(step, 2))
        s = (s - frozenset().union(*(a.dele for a in step))) | frozenset().union(*(a.add for a in step))
    return goal <= s


def valid_sequential(init, goal, seq):
    s = init
    for a in seq:
        if not a.pre <= s:
            return False
        s = (s - a.dele) | a.add
    return goal <= s


def min_parallel_steps(actions, init, goal):
    """Breadth-first search where one edge is a nonempty set of non-interfering applicable actions."""
    dist = {init: 0}
    q = deque([init])
    while q:
        s = q.popleft()
        if goal <= s:
            return dist[s]
        app = [a for a in actions if a.pre <= s]
        for r in range(1, len(app) + 1):
            for step in combinations(app, r):
                if any(interfere(a, b) for a, b in combinations(step, 2)):
                    continue
                t = (s - frozenset().union(*(a.dele for a in step))) | frozenset().union(*(a.add for a in step))
                if t not in dist:
                    dist[t] = dist[s] + 1
                    q.append(t)
    return None


def min_actions(actions, init, goal):
    dist = {init: 0}
    q = deque([init])
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
    return None


def check(actions, init, goal):
    plan = graphplan(actions, init, goal)
    best = min_parallel_steps(actions, init, goal)
    if best is None:
        assert plan is None
        return None
    assert plan is not None
    assert valid_parallel(actions, init, goal, plan)
    assert valid_sequential(init, goal, linearize(plan))
    assert len(plan) == best
    return plan


def test_random_tasks_match_brute_force():
    solved = unsolved = 0
    for seed in range(150):
        rng = random.Random(seed)
        acts, init, goal = random_task(rng, rng.randint(4, 8), rng.randint(4, 8))
        if check(acts, init, goal) is None:
            unsolved += 1
        else:
            solved += 1
    assert solved > 20 and unsolved > 20


def consuming_task(rng):
    """Actions that often use up their preconditions, so that goals compete for resources."""
    nf = rng.randint(4, 8)
    facts = list(range(nf))
    acts = []
    for i in range(rng.randint(4, 8)):
        pre = rng.sample(facts, rng.randint(1, 2))
        add = rng.sample([f for f in facts if f not in pre], 1)
        acts.append(act(("a", i), pre, add, pre if rng.random() < 0.7 else []))
    return acts, frozenset(rng.sample(facts, rng.randint(2, nf // 2 + 1))), frozenset(rng.sample(facts, 3))


def test_no_plan_exactly_when_bfs_finds_none():
    stopped_by_nogoods = 0
    for seed in range(450):
        rng = random.Random(seed)
        if seed < 150:
            acts, init, goal = random_task(rng, rng.randint(4, 8), rng.randint(4, 8))
        else:
            acts, init, goal = consuming_task(rng)
        stats = {}
        plan = graphplan(acts, init, goal, stats)
        assert (plan is None) == (min_actions(acts, init, goal) is None)
        if stats["reason"].startswith("nogoods"):
            stopped_by_nogoods += 1
    assert stopped_by_nogoods > 0


def test_tokens_goal_needs_the_termination_test():
    acts = [act(("put", t, x), [t], [x], [t]) for t in ["t1", "t2"] for x in ["x", "y", "z"]]
    acts += [act("make_u", ["x", "y"], ["u"]), act("make_v", ["z"], ["v"])]
    init = frozenset(["t1", "t2"])
    stats = {}
    assert graphplan(acts, init, {"u", "v"}, stats) is None
    assert stats["reason"].startswith("nogoods")
    assert min_actions(acts, init, frozenset({"u", "v"})) is None
    plan = check(acts, init, frozenset({"u"}))
    assert len(plan) == 2


def test_benchmark_tasks():
    names = ["A", "B", "C"]
    acts = blocks(names)
    for goal in ([("on", "A", "B"), ("on", "B", "C")], [("on", "C", "B"), ("on", "B", "A")],
                 [("on", "A", "B"), ("on", "C", "A")], [("holding", "A"), ("on", "B", "C")]):
        check(acts, table(names), frozenset(goal))
    acts, init, goal = gripper(["b1", "b2"])
    plan = check(acts, init, goal)
    assert len(plan) == 3 and len(linearize(plan)) == 5
    acts, init, goal = logistics()
    plan = check(acts, init, goal)
    assert len(plan) == 3 and len(linearize(plan)) == 5


def test_fewest_steps_is_not_fewest_actions():
    acts = [act("a1", [], ["p"]), act("a2", [], ["q"]), act("a3", [], ["r"]), act("b", ["p", "q", "r"], ["g"]),
            act("c1", [], ["s"]), act("c2", ["s"], ["t"]), act("c3", ["t"], ["g"])]
    plan = check(acts, frozenset(), frozenset(["g"]))
    assert len(plan) == 2 and len(linearize(plan)) == 4
    assert min_actions(acts, frozenset(), frozenset(["g"])) == 3
    assert min_parallel_steps(acts, frozenset(), frozenset(["g"])) == 2
