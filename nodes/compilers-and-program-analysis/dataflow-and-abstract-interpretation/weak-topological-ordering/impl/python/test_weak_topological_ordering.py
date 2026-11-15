# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/weak-topological-ordering/. The authors are listed in prov/X5B201.jsonl.

import math
import random
from collections import deque

from weak_topological_ordering import (
    Component,
    flatten,
    heads_of,
    iterate,
    show,
    weak_topological_ordering,
)

INF = math.inf

# The control flow graph of the nested loop on the page.
EXAMPLE = {
    "entry": ["outer"],
    "outer": ["init", "exit"],
    "init": ["inner"],
    "inner": ["body", "next"],
    "body": ["inner"],
    "next": ["outer"],
    "exit": [],
}


def wto_of(graph, root):
    return weak_topological_ordering(lambda v: graph[v], root)


# ---- brute force oracles, independent of the code under test ----


def reach(graph, start, allowed):
    """Vertices of allowed reachable from start by paths inside allowed (start included)."""
    seen = {start}
    todo = [start]
    while todo:
        u = todo.pop()
        for w in graph[u]:
            if w in allowed and w not in seen:
                seen.add(w)
                todo.append(w)
    return seen


def sccs(graph, allowed):
    """The strongly connected components of the subgraph induced by allowed, from reachability sets."""
    r = {u: reach(graph, u, allowed) for u in allowed}
    out = []
    done = set()
    for u in sorted(allowed, key=repr):
        if u in done:
            continue
        comp = frozenset(w for w in r[u] if u in r[w])
        done |= comp
        out.append(comp)
    return out


def has_cycle(graph, allowed):
    indeg = {u: 0 for u in allowed}
    for u in allowed:
        for w in graph[u]:
            if w in allowed:
                indeg[w] += 1
    q = deque(u for u in allowed if indeg[u] == 0)
    seen = 0
    while q:
        u = q.popleft()
        seen += 1
        for w in graph[u]:
            if w in allowed:
                indeg[w] -= 1
                if indeg[w] == 0:
                    q.append(w)
    return seen < len(allowed)


def vertices(e):
    if isinstance(e, Component):
        out = {e.head}
        for b in e.body:
            out |= vertices(b)
        return out
    return {e}


def check_level(graph, part, allowed, root_like):
    """The elements of part are the SCCs of graph[allowed], in topological order, recursively."""
    sets = [frozenset(vertices(e)) for e in part]
    assert sorted(sets, key=sorted_key) == sorted(sccs(graph, allowed), key=sorted_key)
    pos = {}
    for k, s in enumerate(sets):
        for u in s:
            pos[u] = k
    for u in allowed:
        for w in graph[u]:
            if w in allowed:
                assert pos[u] <= pos[w]  # no edge goes back to an earlier element
    for e, s in zip(part, sets):
        cyclic = len(s) > 1 or any(u in graph[u] for u in s)
        assert isinstance(e, Component) == cyclic
        if isinstance(e, Component):
            h = e.head
            assert h in reach(graph, h, s) and any(h in graph[u] for u in s)  # h is on a cycle in s
            outside = [u for u in graph if h in graph[u] and u not in s]
            assert h in root_like or outside  # h is entered from outside or is a start vertex
            check_level(graph, e.body, s - {h}, set(graph[h]))


def sorted_key(s):
    return sorted(map(repr, s))


def check_wto(graph, root):
    w = wto_of(graph, root)
    order = flatten(w)
    reachable = reach(graph, root, set(graph))
    assert len(order) == len(set(order)) and set(order) == reachable
    check_level(graph, w, reachable, {root})
    rank = {v: k for k, v in enumerate(order)}
    omega = heads_of(w)
    heads = {v for v in order if omega[v] and omega[v][-1] == v}
    for u in reachable:
        for v in graph[u]:
            forward = rank[u] < rank[v] and v not in omega[u]
            backward = rank[v] <= rank[u] and v in omega[u]
            assert forward or backward, (u, v)
    assert not has_cycle(graph, reachable - heads)
    return w


def random_graph(rng, n):
    graph = {u: [] for u in range(n)}
    p = rng.choice((0.15, 0.25, 0.4))
    for u in range(n):
        for v in range(n):
            if rng.random() < p:
                graph[u].append(v)
        rng.shuffle(graph[u])
    return graph


# ---- the tests ----


def test_example() -> None:
    w = check_wto(EXAMPLE, "entry")
    assert show(w) == "entry (outer init (inner body) next) exit"
    assert flatten(w) == ["entry", "outer", "init", "inner", "body", "next", "exit"]
    assert heads_of(w)["body"] == ["outer", "inner"]


def test_edges() -> None:
    assert wto_of({0: []}, 0) == [0]
    assert wto_of({0: [0]}, 0) == [Component(0, [])]
    assert show(wto_of({0: [1], 1: [0]}, 0)) == "(0 1)"
    assert show(wto_of({0: [1], 1: [1, 2], 2: []}, 0)) == "0 (1) 2"
    # vertex 3 is not reachable from the root and is left out
    assert flatten(wto_of({0: [1], 1: [], 3: [0]}, 0)) == [0, 1]
    # an irreducible loop: the cycle 1 <-> 2 is entered at 1 and at 2
    g = {0: [1, 2], 1: [2], 2: [1]}
    assert show(check_wto(g, 0)) == "0 (1 2)"


def test_nested_chain_is_quadratic() -> None:
    n = 40
    g = {i: [] for i in range(n)}
    for i in range(n - 1):
        g[i].append(i + 1)
        g[i + 1].append(i)
    calls = {v: 0 for v in g}

    def succ(v):
        calls[v] += 1
        return g[v]

    w = weak_topological_ordering(succ, 0)
    omega = heads_of(w)
    assert show(w).startswith("(0 (1 (2 ") and len(omega[n - 1]) == n - 1  # nesting depth n - 1
    for v in g:
        assert calls[v] == 1 + len(omega[v])
    assert sum(calls.values()) == sum(1 + len(omega[v]) for v in g) >= n * (n - 1) // 2


def test_random_wto() -> None:
    rng = random.Random(20241115)
    for _ in range(700):
        n = rng.randint(1, 8)
        g = random_graph(rng, n)
        root = rng.randrange(n)
        calls = {v: 0 for v in g}

        def succ(v, g=g, calls=calls):
            calls[v] += 1
            return g[v]

        weak_topological_ordering(succ, root)
        w = check_wto(g, root)
        omega = heads_of(w)
        for v in flatten(w):
            assert calls[v] == 1 + len(omega[v])


def random_equations(rng, g, root, size):
    """Random monotone edge functions S -> {(a + c) mod size : a in S and a in guard}."""
    edges = {}
    for u in g:
        for v in g[u]:
            guard = frozenset(a for a in range(size) if rng.random() < 0.7)
            edges[(u, v)] = (rng.randint(0, size - 1), guard)
    init = frozenset(rng.sample(range(size), rng.randint(1, 2)))
    preds = {v: [u for u in g if v in g[u]] for v in g}

    def f(v, x):
        out = set(init) if v == root else set()
        for u in preds[v]:
            c, guard = edges[(u, v)]
            out |= {(a + c) % size for a in x[u] if a in guard}
        return frozenset(out)

    return f


def test_iterate_finite_gives_least_fixed_point() -> None:
    rng = random.Random(7)
    for _ in range(500):
        n = rng.randint(1, 7)
        g = random_graph(rng, n)
        root = rng.randrange(n)
        f = random_equations(rng, g, root, 6)
        w = weak_topological_ordering(lambda v: g[v], root)
        got = iterate(w, f, lambda a, b: a <= b, lambda a, b: a | b, frozenset())
        # Kleene iteration from bottom, over the reachable vertices
        order = flatten(w)
        x = {v: frozenset() for v in g}
        while True:
            y = {v: (f(v, x) if v in order else frozenset()) for v in g}
            if y == x:
                break
            x = y
        assert {v: got.get(v, frozenset()) for v in order} == {v: x[v] for v in order}


def iv_leq(a, b):
    return a is None or (b is not None and b[0] <= a[0] and a[1] <= b[1])


def iv_join(a, b):
    if a is None:
        return b
    if b is None:
        return a
    return (min(a[0], b[0]), max(a[1], b[1]))


def iv_widen(a, b):
    if a is None:
        return b
    if b is None:
        return a
    return (-INF if b[0] < a[0] else a[0], INF if b[1] > a[1] else a[1])


def test_iterate_intervals_is_sound_and_stops() -> None:
    rng = random.Random(99)
    for _ in range(500):
        n = rng.randint(1, 7)
        g = random_graph(rng, n)
        root = rng.randrange(n)
        preds = {v: [u for u in g if v in g[u]] for v in g}
        edges = {}
        for u in g:
            for v in g[u]:
                lo, hi = sorted(rng.sample(range(-6, 7), 2))
                guard = rng.choice(((-INF, INF), (lo, INF), (-INF, hi), (lo, hi)))
                edges[(u, v)] = (rng.randint(-2, 3), guard)
        start = rng.randint(-3, 3)
        calls = [0]

        def f(v, x):
            calls[0] += 1
            assert calls[0] < 20000
            out = (start, start) if v == root else None
            for u in preds[v]:
                a = x[u]
                if a is None:
                    continue
                c, (gl, gu) = edges[(u, v)]
                lo, hi = max(a[0], gl), min(a[1], gu)
                if lo <= hi:
                    out = iv_join(out, (lo + c, hi + c))
            return out

        w = weak_topological_ordering(lambda v: g[v], root)
        x = iterate(w, f, iv_leq, iv_widen, None)
        full = {v: x.get(v) for v in g}
        for v in flatten(w):  # the result is a post-fixed point
            assert iv_leq(f(v, full), full[v])
        # every concrete state found by a bounded search is covered
        seen = {(root, start)}
        todo = [(root, start)]
        while todo and len(seen) < 3000:
            u, a = todo.pop()
            for v in g[u]:
                c, (gl, gu) = edges[(u, v)]
                if gl <= a <= gu and abs(a + c) <= 40 and (v, a + c) not in seen:
                    seen.add((v, a + c))
                    todo.append((v, a + c))
        for v, a in seen:
            box = x.get(v)
            assert box is not None and box[0] <= a <= box[1]
