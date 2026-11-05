# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/louvain-method/. The authors are listed in prov/GC71E9.jsonl.

import random
from fractions import Fraction
from itertools import combinations

from louvain_method import louvain_method


def modularity(n, edges, groups):
    """Weighted modularity from the definition, over ordered pairs of vertices."""
    a = [[Fraction(0)] * n for _ in range(n)]
    for u, v, w in edges:
        if u == v:
            a[u][u] += 2 * w
        else:
            a[u][v] += w
            a[v][u] += w
    k = [sum(row) for row in a]
    two_w = sum(k)
    label = {}
    for i, g in enumerate(groups):
        for v in g:
            label[v] = i
    q = Fraction(0)
    for i in range(n):
        for j in range(n):
            if label[i] == label[j]:
                q += a[i][j] - k[i] * k[j] / two_w
    return q / two_w


def reference(n, edges):
    """Louvain with blocks of original vertices, each move scored by a full modularity computation."""
    if sum(w for _, _, w in edges) == 0:
        return [[v] for v in range(n)], []
    blocks = [[v] for v in range(n)]
    linked = set()
    for u, v, _ in edges:
        linked.add((u, v))
        linked.add((v, u))
    levels = []
    while True:
        k = len(blocks)
        comm = list(range(k))
        moved = False
        improved = True
        while improved:
            improved = False
            for b in range(k):
                old = comm[b]
                near = {
                    comm[c]
                    for c in range(k)
                    if c != b and any((x, y) in linked for x in blocks[b] for y in blocks[c])
                }
                def score(target):
                    trial = comm[:]
                    trial[b] = target
                    groups = {}
                    for c in range(k):
                        groups.setdefault(trial[c], []).extend(blocks[c])
                    return modularity(n, edges, list(groups.values()))
                best, best_q = old, score(old)
                for c in sorted(near):
                    q = score(c)
                    if q > best_q:
                        best, best_q = c, q
                comm[b] = best
                if best != old:
                    improved = moved = True
        if not moved:
            return sorted(sorted(p) for p in blocks), levels
        order = []
        for b in range(k):
            if comm[b] not in order:
                order.append(comm[b])
        blocks = [sum((blocks[b] for b in range(k) if comm[b] == c), []) for c in order]
        levels.append(sorted(sorted(p) for p in blocks))


def all_partitions(items):
    if not items:
        yield []
        return
    first, rest = items[0], items[1:]
    for p in all_partitions(rest):
        for i in range(len(p)):
            yield p[:i] + [[first] + p[i]] + p[i + 1 :]
        yield [[first]] + p


def random_weighted(rng, n, p):
    edges = [(u, v, rng.choice([1, 1, 1, 2, 3])) for u, v in combinations(range(n), 2) if rng.random() < p]
    if n and rng.random() < 0.2:
        v = rng.randrange(n)
        edges.append((v, v, rng.choice([1, 2])))
    return edges


def test_example():
    edges = [(u, v, 1) for u, v in [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3), (3, 4), (4, 5), (4, 6), (5, 6)]]
    comms, levels = louvain_method(7, edges)
    assert comms == [[0, 1, 2, 3], [4, 5, 6]]
    assert levels == [[[0, 1, 2, 3], [4, 5, 6]]]
    assert modularity(7, edges, comms) == Fraction(59, 162)


def test_edge_cases():
    assert louvain_method(0, []) == ([], [])
    assert louvain_method(3, []) == ([[0], [1], [2]], [])
    assert louvain_method(2, [(0, 1, 1)])[0] == [[0, 1]]
    assert louvain_method(4, [(0, 1, 1), (2, 3, 1)])[0] == [[0, 1], [2, 3]]


def test_random_against_reference():
    rng = random.Random(20081001)
    for _ in range(500):
        n = rng.randint(0, 8)
        edges = random_weighted(rng, n, rng.choice([0.2, 0.4, 0.6]))
        assert louvain_method(n, edges) == reference(n, edges)


def test_never_above_optimum():
    rng = random.Random(10008)
    for _ in range(150):
        n = rng.randint(1, 7)
        edges = random_weighted(rng, n, 0.45)
        if not edges:
            continue
        comms, levels = louvain_method(n, edges)
        q = modularity(n, edges, comms)
        best = max(modularity(n, edges, p) for p in all_partitions(list(range(n))))
        assert q <= best
        qs = [modularity(n, edges, [[v] for v in range(n)])] + [modularity(n, edges, p) for p in levels]
        assert all(x < y for x, y in zip(qs, qs[1:]))


if __name__ == "__main__":
    test_example()
    test_edge_cases()
    test_random_against_reference()
    test_never_above_optimum()
    print("ok")
