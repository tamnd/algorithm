# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/graph-structured-stack/. The authors are listed in prov/5TVZ6C.jsonl.

import itertools
import random

import pytest

from graph_structured_stack import GraphStructuredStack


def walks(nodes, edges, u, m, through):
    """Oracle: try every sequence of m + 1 nodes and keep the walks of the edge list."""
    out = []
    for seq in itertools.product(nodes, repeat=m):
        path = (u,) + seq
        steps = [(path[k], path[k + 1]) for k in range(m)]
        if all(s in edges for s in steps) and (through is None or through in steps):
            out.append((path[-1], tuple(edges[s] for s in reversed(steps))))
    return sorted(out)


def splice_closure(stacks):
    """Oracle: close a set of stacks (bottom first) under exchange of the parts
    below a shared cell."""
    stacks = set(stacks)
    changed = True
    while changed:
        changed = False
        for s1 in list(stacks):
            for s2 in list(stacks):
                for i, c in enumerate(s1):
                    for k, d in enumerate(s2):
                        if c == d:
                            new = s2[: k + 1] + s1[i + 1:]
                            if new not in stacks:
                                stacks.add(new)
                                changed = True
    return stacks


def test_example():
    # The stacks of the example on the page: three parses of the prefix "aa".
    g = GraphStructuredStack("q0")
    r = g.root
    a1, _ = g.node("q2", 1)
    g.add_edge(a1, r, "a")
    s1, _ = g.node("q1", 1)
    g.add_edge(s1, r, "S")
    a2, _ = g.node("q2", 2)
    g.add_edge(a2, s1, "a")
    s3, _ = g.node("q3", 2)
    g.add_edge(s3, s1, "S")
    s12, _ = g.node("q1", 2)
    g.add_edge(s12, r, "S")
    a3, created = g.node("q2", 3)
    assert created
    g.add_edge(a3, s3, "a")
    g.add_edge(a3, s12, "a")
    assert g.node("q2", 3) == (a3, False)
    assert sorted(g.pop(a3, 1)) == sorted([(s3, ("a",)), (s12, ("a",))])
    assert g.pop(s3, 2) == [(r, ("S", "S"))]
    assert g.stacks(a3, 10) == {(r, s1, s3, a3), (r, s12, a3)}
    assert g.tops(2) == [a2, s3, s12]
    g.check_invariant()


def test_no_upward_edge():
    g = GraphStructuredStack(0)
    v, _ = g.node(1, 2)
    with pytest.raises(ValueError):
        g.add_edge(g.root, v)
    with pytest.raises(ValueError):
        g.push(5, 1, v)
    w, created, new_edge = g.push(5, 2, v, "x")
    assert created and new_edge and g.out[w] == {v: "x"}
    assert g.push(5, 2, v, "y") == (w, False, False) and g.out[w] == {v: "x"}


def test_random_pop_against_walks():
    rng = random.Random(7)
    checked = 0
    for _ in range(300):
        g = GraphStructuredStack(0)
        nodes = [g.root]
        edges = {}
        for _ in range(rng.randint(1, 9)):
            s, j = rng.randint(0, 2), rng.randint(0, 3)
            v, created = g.node(s, j)
            if created:
                nodes.append(v)
        for _ in range(rng.randint(0, 12)):
            v, x = rng.choice(nodes), rng.choice(nodes)
            if g.level[x] <= g.level[v]:
                lab = (v, x)
                new = g.add_edge(v, x, lab)
                assert new == ((v, x) not in edges)
                edges.setdefault((v, x), lab)
        g.check_invariant()
        for _ in range(3):
            u = rng.choice(nodes)
            m = rng.randint(0, 3)
            through = rng.choice(list(edges)) if edges and rng.random() < 0.5 else None
            if through is not None and m == 0:
                through = None
            got = sorted(g.pop(u, m, through))
            assert got == walks(nodes, edges, u, m, through)
            checked += 1
    assert checked >= 500


def test_stack_set_is_splice_closure():
    rng = random.Random(11)
    for _ in range(300):
        g = GraphStructuredStack(0)
        explicit = {(g.root,)}
        for _ in range(rng.randint(1, 7)):
            x = rng.randrange(len(g.state))
            if rng.random() < 0.6:
                s, j = rng.randint(1, 3), g.level[x] + rng.randint(0, 1)
                if (s, j) in g.index and g.index[(s, j)] <= x:
                    continue
                had = x in g.out[g.index[(s, j)]] if (s, j) in g.index else False
                v, created, new_edge = g.push(s, j, x)
                assert created == (v == len(g.state) - 1 and len(g.out[v]) == 1 and not had)
                assert new_edge == (not had)
            else:
                v = rng.randrange(len(g.state))
                if v <= x or g.level[v] < g.level[x]:
                    continue
                g.add_edge(v, x)
            explicit = splice_closure(explicit | {s + (v,) for s in explicit if s[-1] == x})
        g.check_invariant()
        for u in range(len(g.state)):
            assert g.stacks(u, 50) == {s for s in explicit if s[-1] == u}


def test_long_chain_no_recursion():
    g = GraphStructuredStack(0)
    prev = g.root
    for j in range(1, 3001):
        v, _ = g.node(0, j)
        g.add_edge(v, prev, j)
        prev = v
    (end, labels), = g.pop(prev, 3000)
    assert end == g.root and labels == tuple(range(1, 3001))
