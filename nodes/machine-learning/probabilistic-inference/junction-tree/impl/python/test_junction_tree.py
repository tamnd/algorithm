# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/junction-tree/. The authors are listed in prov/1CEHTH.jsonl.

import random
from itertools import combinations

import pytest

from junction_tree import JunctionTree


def filled_graph(n, edges, order):
    adj = {v: set() for v in range(n)}
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    full = {frozenset(e) for e in edges}
    pos = {v: i for i, v in enumerate(order)}
    for v in order:
        later = [u for u in adj[v] if pos[u] > pos[v]]
        for a, b in combinations(later, 2):
            if b not in adj[a]:
                adj[a].add(b)
                adj[b].add(a)
                full.add(frozenset((a, b)))
    return full


def maximal_cliques(n, es):
    cl = [frozenset(s) for k in range(1, n + 1) for s in combinations(range(n), k)
          if all(frozenset(p) in es for p in combinations(s, 2))]
    return {c for c in cl if not any(c < d for d in cl)}


def has_rip(cliques, tree):
    """Each vertex: the cliques that hold it induce a connected subgraph of the tree."""
    verts = set().union(*cliques) if cliques else set()
    for x in verts:
        hold = {i for i, c in enumerate(cliques) if x in c}
        start = next(iter(hold))
        seen, stack = {start}, [start]
        while stack:
            a = stack.pop()
            for i, j in tree:
                for p, q in ((i, j), (j, i)):
                    if p == a and q in hold and q not in seen:
                        seen.add(q)
                        stack.append(q)
        if seen != hold:
            return False
    return True


def spanning_trees(k):
    pairs = list(combinations(range(k), 2))
    for sub in combinations(pairs, k - 1):
        parent = list(range(k))

        def find(x):
            while parent[x] != x:
                x = parent[x]
            return x
        ok = True
        for i, j in sub:
            a, b = find(i), find(j)
            if a == b:
                ok = False
                break
            parent[a] = b
        if ok:
            yield list(sub)


def random_graph(rng, n, p):
    return [e for e in combinations(range(n), 2) if rng.random() < p]


def test_sprinkler_moral_graph():
    # C=0, S=1, R=2, W=3; moral edges CS, CR, SR, SW, RW.
    jt = JunctionTree.build(4, [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3)], [3, 0, 1, 2])
    assert set(jt.cliques) == {frozenset({1, 2, 3}), frozenset({0, 1, 2})}
    assert jt.separators() == [frozenset({1, 2})]
    assert jt.width() == 2


def test_cycle_of_length_five():
    edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0)]
    jt = JunctionTree.build(5, edges, [0, 1, 2, 3, 4])
    assert jt.cliques == [frozenset({0, 1, 4}), frozenset({1, 2, 4}), frozenset({2, 3, 4})]
    assert jt.tree_edges == [(0, 1), (1, 2)]
    assert jt.separators() == [frozenset({1, 4}), frozenset({2, 4})]
    jt.check_invariant(edges)


def test_edge_cases():
    jt = JunctionTree.build(0, [], [])
    jt.check_invariant()
    jt = JunctionTree.build(3, [], [2, 0, 1])
    assert len(jt.cliques) == 3 and len(jt.tree_edges) == 2
    jt.check_invariant()
    with pytest.raises(ValueError):
        JunctionTree.build(3, [], [0, 1])
    jt = JunctionTree.build(4, list(combinations(range(4), 2)), [0, 1, 2, 3])
    assert jt.cliques == [frozenset(range(4))] and jt.tree_edges == []


def test_random_graphs_are_junction_trees():
    rng = random.Random(42)
    for _ in range(500):
        n = rng.randint(1, 8)
        edges = random_graph(rng, n, rng.choice([0.2, 0.4, 0.6]))
        order = list(range(n))
        rng.shuffle(order)
        jt = JunctionTree.build(n, edges, order)
        full = filled_graph(n, edges, order)
        jt.check_invariant(edges)
        jt.check_invariant([tuple(e) for e in full if len(e) == 2])
        assert set(jt.cliques) == maximal_cliques(n, full)
        assert len(jt.cliques) == len(set(jt.cliques)) <= max(n, 1)
        assert has_rip(jt.cliques, jt.tree_edges)
        for s in jt.cliques:
            i = jt.find_clique(s)
            assert s <= jt.cliques[i]


def test_maximum_weight_spanning_trees_are_exactly_the_junction_trees():
    rng = random.Random(3)
    checked = 0
    while checked < 120:
        n = rng.randint(5, 8)
        edges = random_graph(rng, n, 0.35)
        order = list(range(n))
        rng.shuffle(order)
        cl = JunctionTree.build(n, edges, order).cliques
        k = len(cl)
        if k > 6 or k < 3:
            continue
        checked += 1
        trees = list(spanning_trees(k))
        weight = {tuple(t): sum(len(cl[i] & cl[j]) for i, j in t) for t in map(tuple, trees)}
        best = max(weight.values())
        for t in trees:
            assert has_rip(cl, t) == (weight[tuple(t)] == best)
