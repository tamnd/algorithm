# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/girvan-newman-algorithm/. The authors are listed in prov/G0RYGC.jsonl.

import random
from fractions import Fraction
from itertools import combinations

from girvan_newman_algorithm import edge_betweenness, girvan_newman_algorithm


def all_shortest_paths(n, edge_set, s, t):
    """Every shortest s-t path, by growing all simple paths level by level."""
    if s == t:
        return [[s]]
    paths = [[s]]
    for _ in range(n):
        longer = []
        for p in paths:
            for w in range(n):
                if w not in p and (min(p[-1], w), max(p[-1], w)) in edge_set:
                    longer.append(p + [w])
        done = [p for p in longer if p[-1] == t]
        if done:
            return done
        paths = longer
    return []


def brute_betweenness(n, edges):
    edge_set = set(edges)
    b = {e: Fraction(0) for e in edges}
    for s, t in combinations(range(n), 2):
        paths = all_shortest_paths(n, edge_set, s, t)
        for p in paths:
            for x, y in zip(p, p[1:]):
                b[(min(x, y), max(x, y))] += Fraction(1, len(paths))
    return b


def brute_components(n, edges):
    label = list(range(n))
    changed = True
    while changed:
        changed = False
        for u, v in edges:
            low = min(label[u], label[v])
            if label[u] != low or label[v] != low:
                label[u] = label[v] = low
                changed = True
    groups = {}
    for v in range(n):
        groups.setdefault(label[v], []).append(v)
    return sorted(sorted(g) for g in groups.values())


def brute_q(n, edges, part):
    m = len(edges)
    if m == 0:
        return Fraction(0)
    deg = [0] * n
    for u, v in edges:
        deg[u] += 1
        deg[v] += 1
    q = Fraction(0)
    for c in part:
        cs = set(c)
        inside = sum(1 for u, v in edges if u in cs and v in cs)
        q += Fraction(inside, m) - Fraction(sum(deg[v] for v in c), 2 * m) ** 2
    return q


def reference(n, edges):
    """Girvan-Newman from the definitions: path enumeration, label components."""
    current = sorted(edges)
    part = brute_components(n, current)
    levels = [part]
    while current:
        b = brute_betweenness(n, current)
        top = max(b.values())
        e = min(x for x in current if b[x] == top)
        current.remove(e)
        comps = brute_components(n, current)
        if len(comps) > len(part):
            part = comps
            levels.append(part)
    qs = [brute_q(n, edges, p) for p in levels]
    return levels[qs.index(max(qs))], levels


def random_graph(rng, n, p):
    return [(u, v) for u, v in combinations(range(n), 2) if rng.random() < p]


def test_example():
    edges = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3), (3, 4), (4, 5), (4, 6), (5, 6)]
    adj = [set() for _ in range(7)]
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    b = edge_betweenness(7, adj)
    assert b[(3, 4)] == 12 and b[(1, 3)] == 6 and b[(4, 5)] == 5 and b[(0, 1)] == 3 and b[(1, 2)] == 1
    best, levels = girvan_newman_algorithm(7, edges)
    assert best == [[0, 1, 2, 3], [4, 5, 6]]
    assert len(levels) == 7
    assert levels[2] == [[0], [1, 2, 3], [4, 5, 6]]
    assert brute_q(7, edges, best) == Fraction(59, 162)


def test_small_cases():
    assert girvan_newman_algorithm(0, []) == ([], [[]])
    assert girvan_newman_algorithm(1, []) == ([[0]], [[[0]]])
    assert girvan_newman_algorithm(3, []) == ([[0], [1], [2]], [[[0], [1], [2]]])
    best, levels = girvan_newman_algorithm(2, [(0, 1)])
    assert levels == [[[0, 1]], [[0], [1]]] and best == [[0, 1]]


def test_random_against_reference():
    rng = random.Random(20020611)
    for _ in range(600):
        n = rng.randint(1, 7)
        edges = random_graph(rng, n, rng.choice([0.2, 0.4, 0.6, 0.9]))
        adj = [set() for _ in range(n)]
        for u, v in edges:
            adj[u].add(v)
            adj[v].add(u)
        assert edge_betweenness(n, adj) == brute_betweenness(n, edges)
        assert girvan_newman_algorithm(n, edges) == reference(n, edges)


def test_levels_are_nested():
    rng = random.Random(7821)
    for _ in range(200):
        n = rng.randint(2, 12)
        edges = random_graph(rng, n, 0.35)
        best, levels = girvan_newman_algorithm(n, edges)
        assert levels[-1] == [[v] for v in range(n)]
        assert best in levels
        for coarse, fine in zip(levels, levels[1:]):
            assert len(fine) == len(coarse) + 1
            for c in fine:
                assert any(set(c) <= set(d) for d in coarse)


if __name__ == "__main__":
    test_example()
    test_small_cases()
    test_random_against_reference()
    test_levels_are_nested()
    print("ok")
