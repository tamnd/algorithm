# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/loop-nesting-forest/. The authors are listed in prov/EMNP01.jsonl.
import random
import time

import pytest

import toyir
from loop_nesting_forest import cfg_loops, depth, innermost, loop_forest


# ------------------------------------------------------------ brute force


def reach_in(allowed, succ, s):
    """The vertices of allowed that s reaches inside allowed (s included)."""
    seen = {s}
    stack = [s]
    while stack:
        v = stack.pop()
        for w in succ[v]:
            if w in allowed and w not in seen:
                seen.add(w)
                stack.append(w)
    return seen


def adjacency(n, edges):
    succ = [[] for _ in range(n)]
    for a, b in edges:
        succ[a].append(b)
    return succ


def by_definition(n, edges, root):
    """The forest from its recursive definition, with mutual reachability in
    place of a strongly connected components algorithm."""
    succ = adjacency(n, edges)
    reach = reach_in(set(range(n)), succ, root)
    pred = [[] for _ in range(n)]
    for a, b in edges:
        if a in reach:
            pred[b].append(a)
    out = set()

    def split(region):
        r = {v: reach_in(region, succ, v) for v in region}
        done = set()
        for v in sorted(region):
            if v in done:
                continue
            comp = {w for w in r[v] if v in r[w]}
            done |= comp
            if len(comp) == 1 and v not in succ[v]:
                continue
            heads = {x for x in comp if x == root or any(p not in comp for p in pred[x])}
            out.add((frozenset(comp), frozenset(heads)))
            split(comp - heads)

    split(reach)
    return out


def natural_loops(n, edges, root):
    """(reducible, loops) where loops are the natural loops, merged by
    header, with dominators from their definition: d dominates v when v
    cannot be reached from root once d is removed."""
    succ = adjacency(n, edges)
    reach = reach_in(set(range(n)), succ, root)

    def dominates(d, v):
        if d == v or d == root:
            return True
        return v not in reach_in(reach - {d}, succ, root)

    pred = [[] for _ in range(n)]
    for a, b in edges:
        if a in reach:
            pred[b].append(a)
    live = [(a, b) for a, b in edges if a in reach]
    back = [(a, b) for a, b in live if dominates(b, a)]
    forward = adjacency(n, [(a, b) for a, b in live if not dominates(b, a)])
    reducible = not has_cycle(reach, forward)
    loops = {}
    for a, h in back:
        body = loops.setdefault(h, {h})
        if a in body:
            continue
        body.add(a)
        stack = [a]
        while stack:
            v = stack.pop()
            for p in pred[v]:
                if p not in body:
                    body.add(p)
                    stack.append(p)
    return reducible, {(frozenset(b), frozenset([h])) for h, b in loops.items()}


def has_cycle(vertices, succ):
    indeg = {v: 0 for v in vertices}
    for v in vertices:
        for w in succ[v]:
            if w in indeg:
                indeg[w] += 1
    ready = [v for v in vertices if indeg[v] == 0]
    count = 0
    while ready:
        v = ready.pop()
        count += 1
        for w in succ[v]:
            if w in indeg:
                indeg[w] -= 1
                if indeg[w] == 0:
                    ready.append(w)
    return count != len(vertices)


def as_set(loops):
    return {(frozenset(x["nodes"]), frozenset(x["headers"])) for x in loops}


def random_graph(rng):
    n = rng.randint(1, 9)
    m = rng.randint(0, 3 * n)
    edges = [(rng.randrange(n), rng.randrange(n)) for _ in range(m)]
    return n, edges, rng.randrange(n)


# ------------------------------------------------------------------ tests


def test_nested_loops_example():
    # B0 -> B1 -> B2 -> B3 -> B4 -> B5 -> B6, with back edges B2 -> B1,
    # B4 -> B3 and B5 -> B1.
    edges = [(0, 1), (1, 2), (2, 1), (2, 3), (3, 4), (4, 3), (4, 5), (5, 1), (5, 6)]
    loops = loop_forest(7, edges, 0)
    assert loops == [
        {"nodes": [1, 2, 3, 4, 5], "headers": [1], "parent": -1},
        {"nodes": [3, 4], "headers": [3], "parent": 0},
    ]
    assert innermost(7, loops) == [-1, 0, 0, 1, 1, 0, -1]
    assert [depth(loops, i) for i in range(2)] == [1, 2]


def test_irreducible_loop_has_two_headers():
    # r -> A, r -> B, A <-> B, A -> C. The cycle can be entered at A or at B.
    loops = loop_forest(4, [(0, 1), (0, 2), (1, 2), (2, 1), (1, 3)], 0)
    assert loops == [{"nodes": [1, 2], "headers": [1, 2], "parent": -1}]


def test_small_cases():
    assert loop_forest(1, [], 0) == []
    assert loop_forest(1, [(0, 0)], 0) == [{"nodes": [0], "headers": [0], "parent": -1}]
    assert loop_forest(2, [(0, 1), (1, 1)], 0) == [{"nodes": [1], "headers": [1], "parent": -1}]
    # A loop through the root has the root as a header.
    assert loop_forest(2, [(0, 1), (1, 0)], 0) == [{"nodes": [0, 1], "headers": [0], "parent": -1}]
    assert loop_forest(3, [(0, 1), (1, 0), (1, 2), (2, 1)], 0) == [
        {"nodes": [0, 1, 2], "headers": [0], "parent": -1},
        {"nodes": [1, 2], "headers": [1], "parent": 0},
    ]
    # Repeated edges change nothing.
    assert loop_forest(2, [(0, 1), (1, 1), (1, 1), (0, 1)], 0) == [{"nodes": [1], "headers": [1], "parent": -1}]


def test_unreachable_part_is_ignored():
    # 2 <-> 3 is a cycle that 0 cannot reach, and 3 -> 1 is an edge from it
    # into the loop 1 <-> 4; that edge must not make 1 or 4 a header.
    edges = [(0, 1), (1, 4), (4, 1), (2, 3), (3, 2), (3, 4)]
    assert loop_forest(5, edges, 0) == [{"nodes": [1, 4], "headers": [1], "parent": -1}]


def test_bad_input():
    with pytest.raises(ValueError):
        loop_forest(0, [], 0)
    with pytest.raises(ValueError):
        loop_forest(2, [], 2)
    with pytest.raises(ValueError):
        loop_forest(2, [(0, 2)], 0)


def test_random_graphs_match_the_definition():
    rng = random.Random(97)
    multi = 0
    for _ in range(2000):
        n, edges, root = random_graph(rng)
        got = loop_forest(n, edges, root)
        assert as_set(got) == by_definition(n, edges, root), (n, edges, root)
        multi += sum(1 for x in got if len(x["headers"]) > 1)
    assert multi > 100


def test_reducible_graphs_give_merged_natural_loops():
    rng = random.Random(101)
    seen = [0, 0]
    for _ in range(2000):
        n, edges, root = random_graph(rng)
        reducible, nat = natural_loops(n, edges, root)
        seen[reducible] += 1
        if reducible:
            assert as_set(loop_forest(n, edges, root)) == nat, (n, edges, root)
    assert min(seen) > 100


def test_forest_properties():
    rng = random.Random(103)
    for _ in range(1500):
        n, edges, root = random_graph(rng)
        loops = loop_forest(n, edges, root)
        succ = adjacency(n, edges)
        reach = reach_in(set(range(n)), succ, root)
        sets = [set(x["nodes"]) for x in loops]
        for i, x in enumerate(loops):
            assert x["headers"] and set(x["headers"]) <= sets[i] <= reach
            p = x["parent"]
            assert p < i
            if p != -1:
                assert sets[i] <= sets[p] - set(loops[p]["headers"])
            for j in range(i):
                assert sets[i] <= sets[j] or not (sets[i] & sets[j])
                if sets[i] <= sets[j]:
                    # The parent is the smallest loop above.
                    assert p != -1 and sets[p] <= sets[j]
        inner = innermost(n, loops)
        for v in range(n):
            holding = [i for i in range(len(loops)) if v in sets[i]]
            assert inner[v] == (max(holding, key=lambda i: depth(loops, i)) if holding else -1)
        # Remove the edges from inside each loop to its headers: no cycle is left.
        cut = set()
        for x, s in zip(loops, sets):
            cut |= {(a, b) for a, b in edges if a in s and b in x["headers"]}
        rest = adjacency(n, [(a, b) for a, b in edges if (a, b) not in cut])
        assert not has_cycle(reach, rest)


def test_toy_programs():
    rng = random.Random(107)
    multi = 0
    for _ in range(300):
        prog = toyir.random_program(rng, 4, rng.randint(1, 14), rng.random() < 0.2)
        labels = list(prog.blocks)
        index = {lab: i for i, lab in enumerate(labels)}
        edges = [(index[a], index[b]) for a, b in toyir.edges(prog)]
        got = cfg_loops(prog)
        want = by_definition(len(labels), edges, 0)
        named = {(frozenset(index[v] for v in x["nodes"]), frozenset(index[v] for v in x["headers"])) for x in got}
        assert named == want
        multi += sum(1 for x in got if len(x["headers"]) > 1)
        if toyir.is_acyclic(prog):
            assert got == []
    assert multi > 0


def test_deep_nesting():
    # The path 0 .. 2k with the back edges 2k - i -> i gives k nested loops.
    k = 500
    n = 2 * k + 1
    edges = [(i, i + 1) for i in range(2 * k)] + [(2 * k - i, i) for i in range(k)]
    start = time.perf_counter()
    loops = loop_forest(n, edges, 0)
    assert time.perf_counter() - start < 5
    assert len(loops) == k
    for i, x in enumerate(loops):
        assert x["headers"] == [i] and x["nodes"] == list(range(i, 2 * k - i + 1))
        assert x["parent"] == i - 1
    assert depth(loops, k - 1) == k
    assert innermost(n, loops)[k] == k - 1
