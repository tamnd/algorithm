# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/nagamochi-ibaraki-certificate/. The authors are listed in prov/CXSCDF.jsonl.

import itertools
import random

from nagamochi_ibaraki_certificate import forest_labels, nagamochi_ibaraki_certificate


def connected_in(n, edges, removed=frozenset()):
    """Components of the graph on the vertices not in removed, as a label list."""
    comp = [-1] * n
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    c = 0
    for s in range(n):
        if s in removed or comp[s] != -1:
            continue
        comp[s] = c
        stack = [s]
        while stack:
            x = stack.pop()
            for y in adj[x]:
                if y not in removed and comp[y] == -1:
                    comp[y] = c
                    stack.append(y)
        c += 1
    return comp


def local_lambda(n, edges, u, v):
    """Least number of edges crossing a vertex set that holds u but not v."""
    best = len(edges)
    for mask in range(1 << n):
        if mask >> u & 1 and not mask >> v & 1:
            cut = sum(1 for a, b in edges if (mask >> a & 1) != (mask >> b & 1))
            best = min(best, cut)
    return best


def kappa(n, edges):
    """Vertex connectivity by brute force over removed sets."""
    for size in range(n):
        for s in itertools.combinations(range(n), size):
            rest = n - size
            if rest <= 1:
                return size
            comp = connected_in(n, edges, frozenset(s))
            if len({comp[x] for x in range(n) if x not in s}) > 1:
                return size
    return max(n - 1, 0)


def check(n, edges, kmax=4):
    label = forest_labels(n, edges)
    assert len(label) == len(edges)
    for e, (u, v) in enumerate(edges):
        assert (label[e] == 0) == (u == v)
    top = max(label, default=0)
    for i in range(1, top + 1):
        fi = [edges[e] for e in range(len(edges)) if label[e] == i]
        # F_i is a forest: no edge joins two vertices already joined.
        parent = list(range(n))

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        for a, b in fi:
            ra, rb = find(a), find(b)
            assert ra != rb
            parent[ra] = rb
        # Every edge of a later forest has its ends joined in F_i.
        for e, (a, b) in enumerate(edges):
            if label[e] > i:
                assert find(a) == find(b)
    kg = kappa(n, edges)
    for k in range(1, kmax + 1):
        keep = nagamochi_ibaraki_certificate(n, edges, k)
        h = [edges[e] for e in keep]
        assert len(h) <= k * max(n - 1, 0)
        for u, v in itertools.combinations(range(n), 2):
            lg = local_lambda(n, edges, u, v)
            lh = local_lambda(n, h, u, v)
            assert lh <= lg
            assert lh >= min(k, lg)
    # The vertex version holds for simple graphs, so drop loops and copies.
    simple = sorted({(min(u, v), max(u, v)) for u, v in edges if u != v})
    ks = kappa(n, simple)
    assert ks == kg
    for k in range(1, kmax + 1):
        h = [simple[e] for e in nagamochi_ibaraki_certificate(n, simple, k)]
        assert min(kappa(n, h), k) == min(ks, k)


def test_example():
    edges = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3), (3, 4), (3, 4), (4, 4)]
    assert forest_labels(5, edges) == [1, 1, 1, 3, 2, 2, 1, 2, 0]
    assert nagamochi_ibaraki_certificate(5, edges, 2) == [0, 1, 2, 4, 5, 6, 7]
    check(5, edges)


def test_edge_cases():
    assert forest_labels(0, []) == []
    assert nagamochi_ibaraki_certificate(1, [(0, 0), (0, 0)], 3) == []
    assert forest_labels(2, [(0, 1)] * 5) == [1, 2, 3, 4, 5]
    assert nagamochi_ibaraki_certificate(2, [(0, 1)] * 5, 3) == [0, 1, 2]
    assert nagamochi_ibaraki_certificate(4, [(0, 1), (2, 3)], 1) == [0, 1]
    check(4, [(0, 1), (2, 3)])
    check(3, [(0, 1), (1, 2), (2, 0), (0, 0), (1, 2)])


def test_parallel_edges_break_the_vertex_version():
    # A triangle with doubled edges 0-1 and 0-2: the copies fill F_1 and F_2,
    # the certificate for k = 2 loses the edge 1-2 and has a cut vertex 0.
    edges = [(1, 2), (2, 0), (0, 2), (0, 1), (1, 0)]
    h = [edges[e] for e in nagamochi_ibaraki_certificate(3, edges, 2)]
    assert kappa(3, edges) == 2
    assert kappa(3, h) == 1
    simple = [(1, 2), (0, 2), (0, 1)]
    assert kappa(3, [simple[e] for e in nagamochi_ibaraki_certificate(3, simple, 2)]) == 2


def test_complete_graph():
    n = 6
    edges = list(itertools.combinations(range(n), 2))
    label = forest_labels(n, edges)
    for k in range(1, n):
        keep = nagamochi_ibaraki_certificate(n, edges, k)
        assert len(keep) <= k * (n - 1)
        assert kappa(n, [edges[e] for e in keep]) >= k
    assert max(label) == n - 1


def test_large_path_and_star():
    n = 50000
    path = [(i, i + 1) for i in range(n - 1)]
    assert forest_labels(n, path) == [1] * (n - 1)
    star = [(0, i) for i in range(1, n)] * 2
    label = forest_labels(n, star)
    assert sorted(label) == [1] * (n - 1) + [2] * (n - 1)


def test_random_oracle():
    rng = random.Random(41)
    for _ in range(600):
        n = rng.randint(1, 6)
        m = rng.randint(0, 12)
        edges = [(rng.randrange(n), rng.randrange(n)) for _ in range(m)]
        check(n, edges, kmax=3)
