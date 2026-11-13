# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/causal-graph-heuristic/. The authors are listed in prov/WC1PNH.jsonl.

import itertools
import math
import random
from collections import deque

from causal_graph_heuristic import (CausalGraphHeuristic, Operator, Task, causal_graph, domain_transition_graph,
                                    pruned_order, pruned_transitions)


def key(s):
    return tuple(sorted(s.items(), key=repr))


def applicable(o, s):
    return all(s[u] == e for u, e in o.pre.items())


def successors(task, s):
    for o in task.operators:
        if applicable(o, s):
            t = dict(s)
            t.update(o.eff)
            yield o, t


def is_goal(task, s):
    return all(s[v] == g for v, g in task.goal.items())


def reachable(task, init):
    seen, q = {key(init): init}, deque([init])
    while q:
        s = q.popleft()
        for _, t in successors(task, s):
            if key(t) not in seen:
                seen[key(t)] = t
                q.append(t)
    return list(seen.values())


def goal_distance(task, s):
    seen, q = {key(s)}, deque([(s, 0)])
    while q:
        x, d = q.popleft()
        if is_goal(task, x):
            return d
        for _, t in successors(task, x):
            if key(t) not in seen:
                seen.add(key(t))
                q.append((t, d + 1))
    return math.inf


def relaxed_distance(task, s):
    """h+ for SAS+: a relaxed state is a set of variable-value pairs, and values are never lost."""
    start, goal = frozenset(s.items()), frozenset(task.goal.items())
    seen, q = {start}, deque([(start, 0)])
    while q:
        x, d = q.popleft()
        if goal <= x:
            return d
        for o in task.operators:
            if frozenset(o.pre.items()) <= x:
                t = x | frozenset(o.eff.items())
                if t not in seen:
                    seen.add(t)
                    q.append((t, d + 1))
    return math.inf


def all_states(task):
    names = sorted(task.domains, key=repr)
    for values in itertools.product(*(range(task.domains[v]) for v in names)):
        yield dict(zip(names, values))


def random_task(rng):
    n = rng.randint(2, 4)
    dom = {i: rng.randint(2, 3) for i in range(n)}
    ops = []
    for j in range(rng.randint(3, 7)):
        pre = {u: rng.randrange(dom[u]) for u in rng.sample(range(n), rng.randint(0, min(2, n)))}
        eff = {v: rng.choice([x for x in range(dom[v]) if x != pre.get(v)])
               for v in rng.sample(range(n), rng.randint(1, min(2, n)))}
        ops.append(Operator(("o", j), pre, eff))
    goal = {v: rng.randrange(dom[v]) for v in rng.sample(range(n), rng.randint(1, n))}
    return Task(dom, ops, {v: rng.randrange(dom[v]) for v in dom}, goal)


def unary_acyclic_task(rng):
    """Unary operators with conditions only on lower variables, and a cycle through each domain."""
    n = rng.randint(1, 3)
    dom = {i: rng.randint(2, 3) for i in range(n)}
    ops = []
    for v in range(n):
        for d in range(dom[v]):
            pre = {u: rng.randrange(dom[u]) for u in range(v) if rng.random() < 0.5}
            pre[v] = d
            ops.append(Operator(("cycle", v, d), pre, {v: (d + 1) % dom[v]}))
        for j in range(rng.randint(0, 2)):
            d, d2 = rng.sample(range(dom[v]), 2)
            pre = {u: rng.randrange(dom[u]) for u in range(v) if rng.random() < 0.5}
            pre[v] = d
            ops.append(Operator(("extra", v, j), pre, {v: d2}))
    goal = {v: rng.randrange(dom[v]) for v in rng.sample(range(n), rng.randint(1, n))}
    return Task(dom, ops, {v: rng.randrange(dom[v]) for v in dom}, goal)


def transport(packages, cells=4, truck=3, start=0, dest=2):
    """A truck on a line of cells; each package variable has one value per cell and one for "in the truck"."""
    dom, ops = {"t": cells}, []
    for x in range(cells - 1):
        ops.append(Operator(("drive", x, x + 1), {"t": x}, {"t": x + 1}))
        ops.append(Operator(("drive", x + 1, x), {"t": x + 1}, {"t": x}))
    init, goal = {"t": truck}, {}
    for p in range(packages):
        v = ("p", p)
        dom[v] = cells + 1
        for x in range(cells):
            ops.append(Operator(("load", p, x), {v: x, "t": x}, {v: cells}))
            ops.append(Operator(("unload", p, x), {v: cells, "t": x}, {v: x}))
        init[v], goal[v] = start, dest
    return Task(dom, ops, init, goal)


def test_domain_transition_graphs_match_definition_5():
    """An arc d -> d2 with label c exists exactly when some operator, applicable in some state s with s(v) = d,
    sets v to d2 and has the preconditions c on the other variables (with d != d2 when v has no precondition)."""
    for seed in range(600):
        task = random_task(random.Random(seed))
        for v in task.domains:
            expected = set()
            for s in all_states(task):
                for o in task.operators:
                    if v in o.eff and applicable(o, s) and (v in o.pre or s[v] != o.eff[v]):
                        label = frozenset((u, e) for u, e in o.pre.items() if u != v)
                        expected.add((s[v], o.eff[v], label, o.name))
            arcs = domain_transition_graph(task, v)
            assert len(arcs) == len(set(arcs)) and set(arcs) == expected


def test_causal_graph_matches_definition_6():
    for seed in range(600):
        task = random_task(random.Random(seed))
        expected = set()
        for v in task.domains:
            for _, _, label, _ in domain_transition_graph(task, v):
                expected.update((u, v) for u, _ in label if u != v)
        for o in task.operators:
            expected.update((u, v) for u in o.eff for v in o.eff if u != v)
        weight = causal_graph(task)
        assert set(weight) == expected
        for (u, v), w in weight.items():
            assert w == sum(1 for o in task.operators if v in o.eff and (u in o.pre or u in o.eff))


def test_pruned_graph_is_acyclic_and_keeps_acyclic_graphs():
    cyclic = 0
    for seed in range(600):
        task = random_task(random.Random(seed))
        level = pruned_order(task)
        assert sorted(level.values()) == list(range(len(task.domains)))
        arcs = set(causal_graph(task))
        kept = {(u, v) for (u, v) in arcs if level[u] < level[v]}
        is_cyclic = any((v, u) in arcs for (u, v) in arcs) or len(kept) < len(arcs)
        cyclic += is_cyclic
        if not is_cyclic:
            assert kept == arcs
        for v, trans in pruned_transitions(task, level).items():
            for d, d2, cond, _ in trans:
                assert d != d2 and all(level[u] < level[v] for u, _ in cond)
    assert cyclic > 0


def test_zero_exactly_at_goal_states():
    states = over = under = 0
    for seed in range(600):
        task = random_task(random.Random(seed))
        h = CausalGraphHeuristic(task)
        for s in reachable(task, task.init):
            states += 1
            value = h(s)
            assert (value == 0) == is_goal(task, s)
            assert value >= sum(s[v] != g for v, g in task.goal.items())
            d = goal_distance(task, s)
            if value < math.inf and d < math.inf:
                over += value > d
                under += value < d
    assert states > 2000 and over > 0 and under > 0


def test_one_variable_gives_the_true_distance():
    for seed in range(300):
        rng = random.Random(seed)
        k = rng.randint(2, 6)
        ops = [Operator(("o", j), {0: a} if rng.random() < 0.8 else {}, {0: b})
               for j, (a, b) in enumerate(rng.sample([(a, b) for a in range(k) for b in range(k) if a != b],
                                                    rng.randint(1, k)))]
        task = Task({0: k}, ops, {0: 0}, {0: rng.randrange(k)})
        h = CausalGraphHeuristic(task)
        for d in range(k):
            assert h({0: d}) == goal_distance(task, {0: d})


def test_acyclic_graphs_with_strongly_connected_transition_graphs_are_solvable():
    """Observation 7 of Helmert (2006), checked by breadth-first search from every state."""
    for seed in range(300):
        task = unary_acyclic_task(random.Random(seed))
        level = pruned_order(task)
        assert all(level[u] < level[v] for (u, v) in causal_graph(task))
        h = CausalGraphHeuristic(task)
        for s in all_states(task):
            assert goal_distance(task, s) < math.inf
            assert h(s) < math.inf


def test_transport_follows_the_truck():
    task = transport(1)
    h = CausalGraphHeuristic(task)
    assert h.level == {"t": 0, ("p", 0): 1}
    assert h(task.init) == goal_distance(task, task.init) == 7
    assert relaxed_distance(task, task.init) == 5
    task = transport(2)
    h = CausalGraphHeuristic(task)
    assert h(task.init) == 14 and goal_distance(task, task.init) == 9 and relaxed_distance(task, task.init) == 7


def test_greedy_commitment_gives_infinity_on_a_solvable_state():
    ops = [Operator("u01", {"u": 0}, {"u": 1}), Operator("u03", {"u": 0}, {"u": 3}),
           Operator("u32", {"u": 3}, {"u": 2}),
           Operator("a", {"v": 0, "u": 1}, {"v": 1}), Operator("b", {"v": 0, "u": 2}, {"v": 1}),
           Operator("c", {"v": 1, "u": 2}, {"v": 2})]
    task = Task({"u": 4, "v": 3}, ops, {"u": 0, "v": 0}, {"v": 2})
    h = CausalGraphHeuristic(task)
    assert h(task.init) == math.inf
    assert goal_distance(task, task.init) == 4
