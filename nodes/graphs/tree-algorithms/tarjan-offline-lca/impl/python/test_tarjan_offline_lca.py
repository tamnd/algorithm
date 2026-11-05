# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tarjan-offline-lca/. The authors are listed in prov/71EN86.jsonl.

import random
import sys

sys.dont_write_bytecode = True

from tarjan_offline_lca import offline_lca  # noqa: E402

EXAMPLE = [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (4, 6), (4, 7)]


def naive_lca(n, edges, queries, root):
    adj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    par = [-1] * n
    depth = [0] * n
    seen = [False] * n
    seen[root] = True
    order = [root]
    for v in order:
        for u in adj[v]:
            if not seen[u]:
                seen[u] = True
                par[u] = v
                depth[u] = depth[v] + 1
                order.append(u)
    out = []
    for u, v in queries:
        while depth[u] > depth[v]:
            u = par[u]
        while depth[v] > depth[u]:
            v = par[v]
        while u != v:
            u, v = par[u], par[v]
        out.append(u)
    return out


def random_tree(n, rng):
    perm = list(range(n))
    rng.shuffle(perm)
    return [(perm[i], perm[rng.randrange(i)]) for i in range(1, n)]


def test_example():
    q = [(6, 3), (7, 5), (6, 7), (4, 6), (2, 2), (3, 0)]
    assert offline_lca(8, EXAMPLE, q, 0) == [1, 0, 4, 4, 2, 0]
    assert offline_lca(8, EXAMPLE, [(6, 3), (7, 5)], 4) == [4, 4]


def test_single_vertex():
    assert offline_lca(1, [], [(0, 0)], 0) == [0]
    assert offline_lca(1, [], [], 0) == []


def test_star():
    n = 50
    edges = [(0, i) for i in range(1, n)]
    q = [(i, j) for i in range(n) for j in range(n)]
    assert offline_lca(n, edges, q, 0) == [i if i == j else 0 for i, j in q]
    # rooted at the leaf 1: the centre 0 is the LCA of two other leaves
    assert offline_lca(n, edges, [(2, 3), (1, 5), (0, 7)], 1) == [0, 1, 0]


def test_long_path():
    n = 100_000
    edges = [(i, i + 1) for i in range(n - 1)]
    rng = random.Random(7)
    q = [(rng.randrange(n), rng.randrange(n)) for _ in range(1000)]
    assert offline_lca(n, edges, q, 0) == [min(u, v) for u, v in q]
    assert offline_lca(n, edges, q, n - 1) == [max(u, v) for u, v in q]


def test_random_against_naive():
    rng = random.Random(20240611)
    for _ in range(600):
        n = rng.randint(1, 40)
        edges = random_tree(n, rng)
        root = rng.randrange(n)
        q = [(rng.randrange(n), rng.randrange(n)) for _ in range(rng.randint(0, 30))]
        assert offline_lca(n, edges, q, root) == naive_lca(n, edges, q, root)


if __name__ == "__main__":
    test_example()
    test_single_vertex()
    test_star()
    test_long_path()
    test_random_against_naive()
    print("ok")
