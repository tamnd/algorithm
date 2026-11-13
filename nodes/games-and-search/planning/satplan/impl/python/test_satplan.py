# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/satplan/. The authors are listed in prov/WT1M0J.jsonl.

import random
from itertools import combinations

from satplan import Action, Encoding, dpll, satplan


def fs(*xs):
    return frozenset(xs)


def clash(a, b):
    return bool(a.dele & (b.pre | b.add) or b.dele & (a.pre | a.add))


def steps_from(actions, s):
    """Every set of applicable actions of which no two clash, the empty set included."""
    app = [a for a in actions if a.pre <= s]
    out = []
    for r in range(len(app) + 1):
        for step in combinations(app, r):
            if all(not clash(a, b) for a, b in combinations(step, 2)):
                out.append(step)
    return out


def apply_step(s, step):
    dele = frozenset().union(*(a.dele for a in step))
    add = frozenset().union(*(a.add for a in step))
    return (s - dele) | add


def count_plans(actions, init, goal, k):
    """The number of sequences of k steps from init that end in a goal state."""
    counts = {frozenset(init): 1}
    for _ in range(k):
        nxt = {}
        for s, c in counts.items():
            for step in steps_from(actions, s):
                t = apply_step(s, step)
                nxt[t] = nxt.get(t, 0) + c
        counts = nxt
    return sum(c for s, c in counts.items() if goal <= s)


def fewest_steps(actions, init, goal, bound):
    """Breadth-first search over parallel steps: the fewest steps to a goal state, or None above bound."""
    layer, seen = {frozenset(init)}, {frozenset(init)}
    for k in range(bound + 1):
        if any(goal <= s for s in layer):
            return k
        nxt = set()
        for s in layer:
            for step in steps_from(actions, s):
                t = apply_step(s, step)
                if t not in seen:
                    seen.add(t)
                    nxt.add(t)
        layer = nxt
    return None


def fewest_actions(actions, init, goal):
    layer, seen, d = {frozenset(init)}, {frozenset(init)}, 0
    while layer:
        if any(goal <= s for s in layer):
            return d
        layer = {(s - a.dele) | a.add for s in layer for a in actions if a.pre <= s} - seen
        seen |= layer
        d += 1
    return None


def is_valid(actions, init, goal, plan):
    s = frozenset(init)
    for step in plan:
        if any(a not in actions or not a.pre <= s for a in step):
            return False
        if any(clash(a, b) for a, b in combinations(step, 2)):
            return False
        s = apply_step(s, step)
    return goal <= s


def count_models(clauses, n):
    """Brute force over all 2^n assignments, with each clause as a pair of bit masks."""
    masks = []
    for c in sorted(clauses, key=len):
        pos = sum(1 << (x - 1) for x in c if x > 0)
        neg = sum(1 << (-x - 1) for x in c if x < 0)
        masks.append((pos, neg))
    full = (1 << n) - 1
    return sum(1 for x in range(1 << n) if all((x & p) or (full & ~x & q) for p, q in masks))


def random_task(rng, n_facts, n_actions):
    facts = list(range(n_facts))
    actions = []
    for j in range(n_actions):
        pre = fs(*rng.sample(facts, rng.randint(0, min(2, n_facts))))
        changed = rng.sample(facts, rng.randint(1, min(3, n_facts)))
        cut = rng.randint(0, len(changed))
        actions.append(Action(("a", j), pre, fs(*changed[:cut]), fs(*changed[cut:])))
    init = fs(*(f for f in facts if rng.random() < 0.4))
    goal = fs(*rng.sample(facts, rng.randint(1, n_facts)))
    return actions, init, goal


def test_models_are_exactly_the_parallel_plans():
    """The number of models at horizon k equals the number of k-step parallel plans, by brute force on both sides."""
    cases = sat = 0
    for seed in range(2000):
        rng = random.Random(seed)
        actions, init, goal = random_task(rng, rng.randint(1, 3), rng.randint(1, 3))
        k = rng.randint(0, 2)
        enc = Encoding(actions, init, goal, k)
        n = len(enc.var)
        if n > 13:
            continue
        cases += 1
        models = count_models(enc.clauses, n)
        assert models == count_plans(actions, init, goal, k)
        model = dpll(enc.clauses, n)
        assert (model is not None) == (models > 0)
        if model is not None:
            sat += 1
            assert all(any((x > 0) == model[abs(x)] for x in c) for c in enc.clauses)
            assert is_valid(actions, init, goal, enc.decode(model))
    assert cases >= 500 and 0 < sat < cases


def test_satplan_finds_the_fewest_parallel_steps():
    unsolved = 0
    for seed in range(600):
        rng = random.Random(10000 + seed)
        actions, init, goal = random_task(rng, rng.randint(2, 5), rng.randint(2, 6))
        best = fewest_steps(actions, init, goal, 4)
        plan = satplan(actions, init, goal, max_steps=4)
        if best is None:
            unsolved += 1
            assert plan is None
        else:
            assert len(plan) == best and is_valid(actions, init, goal, plan)
            assert all(plan) or best == 0
    assert 0 < unsolved < 600


def test_default_bound_decides_plan_existence():
    for seed in range(300):
        rng = random.Random(20000 + seed)
        actions, init, goal = random_task(rng, rng.randint(1, 3), rng.randint(1, 3))
        plan = satplan(actions, init, goal)
        assert (plan is None) == (fewest_actions(actions, init, goal) is None)
        if plan is not None:
            assert is_valid(actions, init, goal, plan)


def test_logistics_needs_three_steps():
    at = lambda p, l: ("at", p, l)
    actions = [Action(("drive", a, b), fs(("truck", a)), fs(("truck", b)), fs(("truck", a)))
               for a, b in (("l1", "l2"), ("l2", "l1"))]
    for p in ("p1", "p2"):
        for l in ("l1", "l2"):
            actions.append(Action(("load", p, l), fs(at(p, l), ("truck", l)), fs(("in", p)), fs(at(p, l))))
            actions.append(Action(("unload", p, l), fs(("in", p), ("truck", l)), fs(at(p, l)), fs(("in", p))))
    init = fs(at("p1", "l1"), at("p2", "l1"), ("truck", "l1"))
    goal = fs(at("p1", "l2"), at("p2", "l2"))
    for k in (0, 1, 2):
        assert dpll(Encoding(actions, init, goal, k).clauses, len(Encoding(actions, init, goal, k).var)) is None
    plan = satplan(actions, init, goal)
    assert [sorted(a.name for a in step) for step in plan] == [
        [("load", "p1", "l1"), ("load", "p2", "l1")], [("drive", "l1", "l2")],
        [("unload", "p1", "l2"), ("unload", "p2", "l2")]]
    assert fewest_actions(actions, init, goal) == 5
    sizes = [(len(e.var), len(e.clauses)) for e in (Encoding(actions, init, goal, k) for k in range(5))]
    assert sizes == [(8, 10), (26, 83), (44, 156), (62, 229), (80, 302)]
    assert [count_plans(actions, init, goal, k) for k in range(5)] == [0, 0, 0, 1, 9]


def test_interference_clauses_are_needed():
    """Without them, a model can put an action that deletes a precondition next to the action that needs it."""
    a = Action("a", fs("p"), fs("q"), fs("p"))
    b = Action("b", fs("p"), fs("r"), fs())
    actions, init, goal = [a, b], fs("p"), fs("q", "r")
    assert [[x.name for x in step] for step in satplan(actions, init, goal)] == [["b"], ["a"]]
    enc = Encoding(actions, init, goal, 1)
    assert dpll(enc.clauses, len(enc.var)) is None
    loose = [c for c in enc.clauses if not (len(c) == 2 and c[0] < 0 and c[1] < 0
                                             and {-c[0], -c[1]} == {enc.action(0, 1), enc.action(1, 1)})]
    assert len(loose) == len(enc.clauses) - 1 and dpll(loose, len(enc.var)) is not None
