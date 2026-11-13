# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/relaxed-planning-graph/. The authors are listed in prov/ZT81NP.jsonl.

import math
import random
from collections import deque

from relaxed_planning_graph import Action, RelaxedPlanningGraph, h_ff, helpful_actions, relaxed_plan


def act(name, pre, add, dele=()):
    return Action(name, frozenset(pre), frozenset(add), frozenset(dele))


def random_task(rng, nf, na):
    facts = list(range(nf))
    acts = []
    for i in range(na):
        pre = rng.sample(facts, rng.randint(0, 2))
        add = rng.sample(facts, rng.randint(1, 2))
        dele = rng.sample([f for f in facts if f not in add], rng.randint(0, 2))
        acts.append(act(("a", i), pre, add, dele))
    return acts, frozenset(rng.sample(facts, rng.randint(1, nf // 2))), frozenset(rng.sample(facts, rng.randint(1, 3)))


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


def h_plus(actions, state, goal):
    """Optimal relaxed plan length, by breadth-first search over relaxed states."""
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


def h_max_unit(actions, state):
    """Fixed point of h(f) = 0 on the state, else 1 + min over achievers of the max over preconditions."""
    h = {f: 0 for f in state}
    changed = True
    while changed:
        changed = False
        for a in actions:
            if all(p in h for p in a.pre):
                c = 1 + max((h[p] for p in a.pre), default=0)
                for f in a.add:
                    if c < h.get(f, math.inf):
                        h[f] = c
                        changed = True
    return h


def is_relaxed_plan(state, goal, plan):
    s = state
    for a in plan:
        if not a.pre <= s:
            return False
        s = s | a.add
    return goal <= s


def figure2_extract(actions, state, goal):
    """The extraction with add effects marked true at times i - 1 and i, read literally."""
    g = RelaxedPlanningGraph(actions, state, goal)
    m = len(g.F) - 1
    goals = [set() for _ in range(m + 1)]
    for f in goal:
        goals[g.level[f]].add(f)
    true = set()
    chosen = []
    for i in range(m, 0, -1):
        for f in sorted(goals[i], key=repr):
            if (f, i) in true:
                continue
            o = min((j for j in g.layers[i - 1] if f in actions[j].add), key=lambda j: (g.difficulty(j), j))
            chosen.append(actions[o])
            for p in actions[o].pre:
                if g.level[p] != 0 and (p, i - 1) not in true:
                    goals[g.level[p]].add(p)
            for p in actions[o].add:
                true.add((p, i - 1))
                true.add((p, i))
    return chosen


def test_levels_are_unit_h_max():
    for seed in range(200):
        rng = random.Random(seed)
        acts, init, goal = random_task(rng, rng.randint(4, 8), rng.randint(4, 8))
        g = RelaxedPlanningGraph(acts, init, frozenset(range(100)))
        assert g.level == h_max_unit(acts, init)
        for i, layer in enumerate(g.layers):
            for j in layer:
                assert max((g.level[p] for p in acts[j].pre), default=0) == i


def test_extracted_plan_is_relaxed_plan_and_not_shorter_than_h_plus():
    for seed in range(150):
        rng = random.Random(seed)
        acts, init, goal = random_task(rng, rng.randint(4, 8), rng.randint(4, 8))
        for s in reachable(acts, init):
            hp = h_plus(acts, s, goal)
            plan = relaxed_plan(acts, s, goal)
            if hp == math.inf:
                assert plan is None and h_ff(acts, s, goal) == math.inf
                continue
            assert is_relaxed_plan(s, goal, plan)
            assert len(plan) >= hp
            assert len(set(plan)) == len(plan)
            assert (len(plan) == 0) == (goal <= s)
            hm = h_max_unit(acts, s)
            assert len(plan) >= max(hm[f] for f in goal)


def test_literal_figure2_marking_can_break_the_relaxed_plan():
    acts = [act("ap", ["r"], ["p"]), act("aq", ["r"], ["q"]),
            act("b", ["p"], ["g1", "q"]), act("c", ["q"], ["g2", "p"])]
    s, goal = frozenset(["r"]), frozenset(["g1", "g2"])
    literal = figure2_extract(acts, s, goal)
    assert len(literal) == 2 and not is_relaxed_plan(s, goal, literal)
    plan = relaxed_plan(acts, s, goal)
    assert len(plan) == 3 and is_relaxed_plan(s, goal, plan)
    assert h_plus(acts, s, goal) == 3


def test_helpful_actions_are_applicable_and_start_the_relaxed_plan():
    for seed in range(100):
        rng = random.Random(300 + seed)
        acts, init, goal = random_task(rng, rng.randint(4, 8), rng.randint(4, 8))
        plan = relaxed_plan(acts, init, goal)
        if not plan:
            continue
        helpful = helpful_actions(acts, init, goal)
        assert helpful and all(a.pre <= init for a in helpful)
        assert plan[0].pre <= init
        assert plan[0] in helpful


def test_two_blocks_layers():
    acts = [act(("pickup", "A"), [("clear", "A"), ("ontable", "A"), "he"], [("holding", "A")]),
            act(("stack", "A", "B"), [("holding", "A"), ("clear", "B")], [("on", "A", "B"), ("clear", "A"), "he"])]
    s = frozenset([("clear", "A"), ("clear", "B"), ("ontable", "A"), ("ontable", "B"), "he"])
    g = RelaxedPlanningGraph(acts, s, [("on", "A", "B")])
    assert [len(layer) for layer in g.layers] == [1, 1]
    assert [len(F) for F in g.F] == [5, 6, 7]
    assert h_ff(acts, s, [("on", "A", "B")]) == 2
