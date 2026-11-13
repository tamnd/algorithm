# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/relaxed-plan-heuristic/. The authors are listed in prov/KSWASX.jsonl.

import math
import random
from collections import deque

from relaxed_plan_heuristic import Action, h_ff, helpful_actions, relaxed_plan


def act(name, pre, add, dele=()):
    return Action(name, frozenset(pre), frozenset(add), frozenset(dele))


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


def reachable(actions, init):
    seen = {init}
    q = deque([init])
    while q:
        s = q.popleft()
        for a in actions:
            if a.pre <= s:
                t = (s - a.dele) | a.add
                if t not in seen:
                    seen.add(t)
                    q.append(t)
    return seen


def goal_distances(actions, states, goal):
    """h* for every state, by backward breadth-first search over the explicit state graph."""
    pred = {s: [] for s in states}
    for s in states:
        for a in actions:
            if a.pre <= s:
                pred[(s - a.dele) | a.add].append(s)
    d = {s: 0 for s in states if goal <= s}
    q = deque(d)
    while q:
        t = q.popleft()
        for s in pred[t]:
            if s not in d:
                d[s] = d[t] + 1
                q.append(s)
    return {s: d.get(s, math.inf) for s in states}


def h_plus(actions, state, goal):
    dist = {state: 0}
    q = deque([state])
    while q:
        s = q.popleft()
        if goal <= s:
            return dist[s]
        for a in actions:
            if a.pre <= s and not a.add <= s:
                t = s | a.add
                if t not in dist:
                    dist[t] = dist[s] + 1
                    q.append(t)
    return math.inf


def is_relaxed_plan(state, goal, plan):
    s = state
    for a in plan:
        if not a.pre <= s:
            return False
        s = s | a.add
    return goal <= s


def test_example_where_h_ff_exceeds_h_star():
    acts = [act("pP", [], ["P"]), act("pQ", [], ["Q"]), act("a1", ["P"], ["g1"]), act("b", ["Q"], ["g2"]),
            act("x", ["P", "Q"], ["g1", "g2"])]
    s, goal = frozenset(), frozenset(["g1", "g2"])
    plan, _ = relaxed_plan(acts, s, goal)
    assert [a.name for a in plan] == ["pP", "pQ", "a1", "b"]
    assert h_ff(acts, s, goal) == 4
    assert h_plus(acts, s, goal) == 3
    assert goal_distances(acts, reachable(acts, s), goal)[s] == 3


def test_hoffmann_nebel_shared_precondition():
    acts = [act("opG1", ["P"], ["G1"]), act("opG2", ["P"], ["G2"]), act("opP", [], ["P"])]
    assert h_ff(acts, frozenset(), {"G1", "G2"}) == 3


def test_random_states_against_brute_force():
    checked = over_h_star = 0
    for seed in range(400):
        rng = random.Random(seed)
        acts, init, goal = random_task(rng)
        states = reachable(acts, init)
        hstar = goal_distances(acts, states, goal)
        for s in states:
            h = h_ff(acts, s, goal)
            hp = h_plus(acts, s, goal)
            checked += 1
            assert (h == math.inf) == (hp == math.inf)
            assert h >= hp
            assert (h == 0) == (goal <= s)
            if hstar[s] == math.inf:
                continue
            assert hp <= hstar[s]
            if h > hstar[s]:
                over_h_star += 1
            plan, _ = relaxed_plan(acts, s, goal)
            assert is_relaxed_plan(s, goal, plan)
    assert checked > 500 and over_h_star > 0


def test_blocks_world():
    acts, init = blocks(["A", "B", "C"])
    goal = frozenset([("on", "A", "B"), ("on", "B", "C")])
    states = reachable(acts, init)
    hstar = goal_distances(acts, states, goal)
    assert len(states) == 22
    assert h_ff(acts, init, goal) == 4 == hstar[init]
    values = [(h_ff(acts, s, goal), hstar[s]) for s in states]
    assert sum(h > d for h, d in values) == 1
    assert all((h == 0) == (d == 0) for h, d in values)


def test_helpful_actions():
    acts, init = blocks(["A", "B", "C"])
    goal = frozenset([("on", "A", "B"), ("on", "B", "C")])
    helpful = helpful_actions(acts, init, goal)
    assert helpful and all(a.pre <= init for a in helpful)
    assert ("pickup", "B") in [a.name for a in helpful]
    for seed in range(100):
        rng = random.Random(1000 + seed)
        acts, init, goal = random_task(rng)
        plan, _ = relaxed_plan(acts, init, goal)
        if plan:
            assert plan[0] in helpful_actions(acts, init, goal)


def test_unreachable_goal_is_infinite():
    acts = [act("a", ["p"], ["q"])]
    assert h_ff(acts, frozenset(["r"]), {"q"}) == math.inf
    assert h_ff(acts, frozenset(["p"]), {"q"}) == 1
    assert h_ff(acts, frozenset(["q"]), {"q"}) == 0
