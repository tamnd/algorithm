# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/markov-clustering/. The authors are listed in prov/5FFE0B.jsonl.

import random
from itertools import combinations

from markov_clustering import markov_clustering


def reference(n, edges, inflation=2.0, prune=1e-6, tol=1e-9, max_iter=1000):
    """MCL with sparse columns held in dicts, and a search for the components of the limit graph."""
    if n == 0:
        return [], 0
    cols = [{v: 1.0} for v in range(n)]
    for u, v, w in edges:
        cols[v][u] = cols[v].get(u, 0.0) + w
        if u != v:
            cols[u][v] = cols[u].get(v, 0.0) + w

    def scaled(col, cut):
        s = sum(col.values())
        col = {i: x / s for i, x in col.items()}
        col = {i: x for i, x in col.items() if x >= cut}
        s = sum(col.values())
        return {i: x / s for i, x in col.items()}

    cols = [scaled(c, 0.0) for c in cols]
    t = 0
    while True:
        new = []
        for j in range(n):
            out = {}
            for k, y in cols[j].items():
                for i, x in cols[k].items():
                    out[i] = out.get(i, 0.0) + x * y
            new.append(scaled({i: x**inflation for i, x in out.items()}, prune))
        t += 1
        change = max(
            abs(new[j].get(i, 0.0) - cols[j].get(i, 0.0)) for j in range(n) for i in range(n)
        )
        cols = new
        if change <= tol or t >= max_iter:
            break
    near = [set() for _ in range(n)]
    for j in range(n):
        for i in cols[j]:
            near[i].add(j)
            near[j].add(i)
    seen, out = set(), []
    for s in range(n):
        if s in seen:
            continue
        seen.add(s)
        stack, comp = [s], []
        while stack:
            x = stack.pop()
            comp.append(x)
            for y in near[x]:
                if y not in seen:
                    seen.add(y)
                    stack.append(y)
        out.append(sorted(comp))
    return sorted(out), t


def components(n, edges):
    label = list(range(n))

    def find(x):
        while label[x] != x:
            x = label[x]
        return x

    for u, v, _ in edges:
        a, b = find(u), find(v)
        if a != b:
            label[max(a, b)] = min(a, b)
    return {v: find(v) for v in range(n)}


def random_graph(rng, n, p):
    return [(u, v, rng.choice([1, 1, 2])) for u, v in combinations(range(n), 2) if rng.random() < p]


def test_example():
    edges = [(0, 1, 1), (0, 2, 1), (1, 2, 1), (3, 4, 1), (3, 5, 1), (4, 5, 1), (2, 3, 1)]
    assert markov_clustering(6, edges) == ([[0, 1, 2], [3, 4, 5]], 9)


def test_two_cliques_joined_by_an_edge():
    edges = [(u, v, 1) for g in ([0, 1, 2, 3], [4, 5, 6, 7]) for u, v in combinations(g, 2)]
    edges.append((3, 4, 1))
    assert markov_clustering(8, edges)[0] == [[0, 1, 2, 3], [4, 5, 6, 7]]


def test_inflation_controls_granularity():
    edges = [(0, 1, 1), (0, 2, 1), (1, 2, 1), (3, 4, 1), (3, 5, 1), (4, 5, 1), (2, 3, 1)]
    assert markov_clustering(6, edges, inflation=1.4)[0] == [[0, 1, 2, 3, 4, 5]]
    assert markov_clustering(6, edges, inflation=4.0)[0] == [[0, 1, 2], [3, 4, 5]]


def test_overlap_merges_in_the_read_out():
    # The middle vertex of a path of 7 vertices is split evenly between two attractors.
    assert markov_clustering(7, [(i, i + 1, 1) for i in range(6)])[0] == [list(range(7))]


def test_edge_cases():
    assert markov_clustering(0, []) == ([], 0)
    assert markov_clustering(1, []) == ([[0]], 1)
    assert markov_clustering(4, []) == ([[0], [1], [2], [3]], 1)
    assert markov_clustering(2, [(0, 1, 1)])[0] == [[0, 1]]
    assert markov_clustering(4, [(0, 1, 1), (2, 3, 1)])[0] == [[0, 1], [2, 3]]
    assert markov_clustering(3, [(0, 1, 1), (0, 1, 2), (2, 2, 5)])[0] == [[0, 1], [2]]


def test_random_against_reference():
    rng = random.Random(20000501)
    for _ in range(300):
        n = rng.randint(0, 12)
        edges = random_graph(rng, n, rng.choice([0.15, 0.3, 0.5]))
        assert markov_clustering(n, edges) == reference(n, edges)


def test_clusters_partition_and_refine_components():
    rng = random.Random(7)
    for _ in range(200):
        n = rng.randint(1, 15)
        edges = random_graph(rng, n, rng.choice([0.1, 0.25, 0.4]))
        clusters, _ = markov_clustering(n, edges)
        assert sorted(v for c in clusters for v in c) == list(range(n))
        comp = components(n, edges)
        for c in clusters:
            assert len({comp[v] for v in c}) == 1


if __name__ == "__main__":
    test_example()
    test_two_cliques_joined_by_an_edge()
    test_inflation_controls_granularity()
    test_overlap_merges_in_the_read_out()
    test_edge_cases()
    test_random_against_reference()
    test_clusters_partition_and_refine_components()
    print("ok")
