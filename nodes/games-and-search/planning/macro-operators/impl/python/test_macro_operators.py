# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/macro-operators/. The authors are listed in prov/8C2C7V.jsonl.

import random
from collections import deque
from itertools import product

from macro_operators import (Action, breadth_first_plan, expand, is_macro, macro, macro_table, neighbours,
                             plan_with_macros, slide, solve_with_table)


def fs(*xs):
    return frozenset(xs)


def run(seq, s):
    """Apply the actions one by one; None if one of them is not applicable."""
    for a in seq:
        if not a.pre <= s:
            return None
        s = (s - a.dele) | a.add
    return s


def all_states(facts):
    for bits in product((0, 1), repeat=len(facts)):
        yield frozenset(f for f, b in zip(facts, bits) if b)


def reachable(ops, init):
    seen, queue = {init}, deque([init])
    while queue:
        s = queue.popleft()
        for a in ops:
            if a.pre <= s:
                t = (s - a.dele) | a.add
                if t not in seen:
                    seen.add(t)
                    queue.append(t)
    return seen


def depth(ops, init, goal):
    """The fewest operators to a goal state, by breadth-first search written here."""
    layer, seen, d = {init}, {init}, 0
    while layer:
        if any(goal <= s for s in layer):
            return d
        layer = {(s - a.dele) | a.add for s in layer for a in ops if a.pre <= s} - seen
        seen |= layer
        d += 1
    return None


def random_task(rng):
    facts = list(range(rng.randint(2, 5)))
    actions = []
    for j in range(rng.randint(2, 6)):
        pre = fs(*rng.sample(facts, rng.randint(0, min(2, len(facts)))))
        changed = rng.sample(facts, rng.randint(1, min(3, len(facts))))
        cut = rng.randint(0, len(changed))
        actions.append(Action(("a", j), pre, fs(*changed[:cut]), fs(*changed[cut:])))
    init = fs(*(f for f in facts if rng.random() < 0.4))
    goal = fs(*rng.sample(facts, rng.randint(1, len(facts))))
    return facts, actions, init, goal


def random_sequences(rng, actions, count):
    return [[rng.choice(actions) for _ in range(rng.randint(2, 3))] for _ in range(count)]


def logistics(packages):
    at = lambda p, l: ("at", p, l)
    actions = [Action(("drive", a, b), fs(("truck", a)), fs(("truck", b)), fs(("truck", a)))
               for a, b in (("l1", "l2"), ("l2", "l1"))]
    names = ["p%d" % i for i in range(1, packages + 1)]
    for p in names:
        for l in ("l1", "l2"):
            actions.append(Action(("load", p, l), fs(at(p, l), ("truck", l)), fs(("in", p)), fs(at(p, l))))
            actions.append(Action(("unload", p, l), fs(("in", p), ("truck", l)), fs(at(p, l)), fs(("in", p))))
    by_name = {a.name: a for a in actions}
    carry = [[by_name[("load", p, a)], by_name[("drive", a, b)], by_name[("unload", p, b)]]
             for p in names for a, b in (("l1", "l2"), ("l2", "l1"))]
    init = fs(*(at(p, "l1") for p in names), ("truck", "l1"))
    goal = fs(*(at(p, "l2") for p in names))
    return actions, carry, init, goal


def tree_search_nodes(ops, init, goal):
    """Iterative deepening without duplicate detection: the depth found and the nodes generated."""
    total = 0
    for limit in range(20):
        count = 0

        def dfs(s, d):
            nonlocal count
            count += 1
            if goal <= s:
                return True
            return d < limit and any(dfs((s - a.dele) | a.add, d + 1) for a in ops if a.pre <= s)

        found = dfs(init, 0)
        total += count
        if found:
            return limit, total
    return None


def test_a_macro_acts_like_its_sequence_in_every_state():
    never = 0
    for seed in range(600):
        rng = random.Random(seed)
        facts, actions, _, _ = random_task(rng)
        for seq in random_sequences(rng, actions, 3):
            m = macro(seq)
            results = {s: run(seq, s) for s in all_states(facts)}
            if m is None:
                never += 1
                assert all(r is None for r in results.values())
                continue
            assert not m.add & m.dele and expand([m]) == seq
            for s, r in results.items():
                assert (m.pre <= s) == (r is not None)
                if r is not None:
                    assert (s - m.dele) | m.add == r
    assert never > 0


def test_plans_with_macros_expand_to_valid_plans():
    shorter = longer = 0
    for seed in range(600):
        rng = random.Random(1000 + seed)
        facts, actions, init, goal = random_task(rng)
        seqs = random_sequences(rng, actions, rng.randint(1, 4))
        macros = [m for m in map(macro, seqs) if m is not None]
        best = depth(actions, init, goal)
        plan = plan_with_macros(actions, seqs, init, goal)
        assert (plan is None) == (best is None)
        if plan is None:
            continue
        assert all(not is_macro(a) and a in actions for a in plan)
        assert run(plan, init) is not None and goal <= run(plan, init)
        assert len(plan) >= best
        macro_depth = depth(actions + macros, init, goal)
        assert macro_depth <= best and len(breadth_first_plan(actions + macros, init, goal)) == macro_depth
        shorter += macro_depth < best
        longer += len(plan) > best
    assert shorter > 0 and longer > 0


def test_macros_raise_the_branching_factor_and_keep_the_reachable_states():
    base_total = macro_total = 0
    for seed in range(600):
        rng = random.Random(2000 + seed)
        facts, actions, init, goal = random_task(rng)
        macros = [m for m in map(macro, random_sequences(rng, actions, 3)) if m is not None]
        states = reachable(actions, init)
        assert reachable(actions + macros, init) == states
        for s in states:
            base = sum(a.pre <= s for a in actions)
            extra = sum(m.pre <= s for m in macros)
            base_total += base
            macro_total += base + extra
            assert extra == sum(run(m.name[1], s) is not None for m in macros)
    assert macro_total > base_total


def test_logistics_carry_macros():
    actions, carry, init, goal = logistics(2)
    macros = [macro(seq) for seq in carry]
    m = macros[0]
    assert m.pre == fs(("at", "p1", "l1"), ("truck", "l1"))
    assert m.add == fs(("at", "p1", "l2"), ("truck", "l2"))
    assert m.dele == fs(("at", "p1", "l1"), ("in", "p1"), ("truck", "l1"))
    states = reachable(actions, init)
    assert len(states) == 18
    assert sum(sum(a.pre <= s for a in actions) for s in states) * 3 == 7 * len(states)
    assert sum(sum(a.pre <= s for a in actions + macros) for s in states) == 3 * len(states)
    assert depth(actions, init, goal) == 5 and depth(actions + macros, init, goal) == 3
    assert len(plan_with_macros(actions, carry, init, goal)) == 5
    assert tree_search_nodes(actions, init, goal) == (5, 218)
    assert tree_search_nodes(actions + macros, init, goal) == (3, 53)
    actions, carry, init, goal = logistics(3)
    macros = [macro(seq) for seq in carry]
    assert tree_search_nodes(actions, init, goal) == (7, 6434)
    assert tree_search_nodes(actions + macros, init, goal) == (5, 1449)


def test_macro_table_solves_every_state_of_the_2_by_3_puzzle():
    rows, cols = 2, 3
    goal = (1, 2, 3, 4, 5, 0)
    dist, queue = {goal: 0}, deque([goal])
    while queue:
        s = queue.popleft()
        for x in neighbours(rows, cols, s.index(0)):
            t = slide(s, x)
            if t not in dist:
                dist[t] = dist[s] + 1
                queue.append(t)
    assert len(dist) == 360 and max(dist.values()) == 21
    table = macro_table(rows, cols)
    sizes = {}
    for (i, j), moves in table.items():
        if moves:
            sizes.setdefault(i, []).append(len(moves))
    assert {i: (len(v), max(v)) for i, v in sizes.items()} == {0: (5, 3), 1: (4, 10), 2: (3, 14), 3: (2, 12)}
    bound = sum(max(v) for v in sizes.values())
    lengths = []
    for s in dist:
        moves = solve_with_table(table, rows, cols, s)
        t = s
        for x in moves:
            assert x in neighbours(rows, cols, t.index(0))
            t = slide(t, x)
        assert t == goal and dist[s] <= len(moves) <= bound
        lengths.append(len(moves))
    assert max(lengths) == 39 == bound and sum(lengths) == 21 * 360 and sum(dist.values()) == 4544
