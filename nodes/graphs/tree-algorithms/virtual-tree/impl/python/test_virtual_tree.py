# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/virtual-tree/. The authors are listed in prov/Q53SNA.jsonl.

import random
import sys

sys.dont_write_bytecode = True

from virtual_tree import VirtualTree  # noqa: E402

EXAMPLE = [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (4, 6), (4, 7)]


def naive(n, edges, root, keys):
    """Close the keys under pairwise LCA by climbing, then link each vertex
    to its nearest proper ancestor in the closed set."""
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

    def lca(u, v):
        while depth[u] > depth[v]:
            u = par[u]
        while depth[v] > depth[u]:
            v = par[v]
        while u != v:
            u, v = par[u], par[v]
        return u

    ks = set(keys)
    closed = {lca(x, y) for x in ks for y in ks}
    link = {}
    for v in closed:
        u = par[v]
        while u != -1 and u not in closed:
            u = par[u]
        link[v] = u
    return closed, link


def as_links(nodes, par):
    return {v: (nodes[par[i]] if par[i] >= 0 else -1) for i, v in enumerate(nodes)}


def test_example():
    vt = VirtualTree(8, EXAMPLE, 0)
    nodes, par = vt.build([5, 3, 6])
    assert nodes == [0, 1, 3, 6, 5]
    assert as_links(nodes, par) == {0: -1, 1: 0, 3: 1, 6: 1, 5: 0}
    total = sum(vt.depth[v] - vt.depth[nodes[par[i]]] for i, v in enumerate(nodes) if par[i] >= 0)
    assert total == 6
    nodes, par = vt.build([6, 7])
    assert nodes == [4, 6, 7] and par == [-1, 0, 0]


def test_single_vertex():
    vt = VirtualTree(1, [], 0)
    assert vt.build([0]) == ([0], [-1])
    assert vt.build([0, 0]) == ([0], [-1])


def test_star():
    n = 30
    vt = VirtualTree(n, [(0, i) for i in range(1, n)], 0)
    nodes, par = vt.build([5, 9, 2])
    assert nodes == [0, 2, 5, 9] and par == [-1, 0, 0, 0]
    assert vt.build([7]) == ([7], [-1])


def test_long_path():
    n = 100_000
    vt = VirtualTree(n, [(i, i + 1) for i in range(n - 1)], 0)
    rng = random.Random(3)
    keys = rng.sample(range(n), 2000)
    nodes, par = vt.build(keys)
    assert nodes == sorted(keys)
    assert par == list(range(-1, len(nodes) - 1))


def test_random_against_naive():
    rng = random.Random(20240612)
    for _ in range(600):
        n = rng.randint(1, 40)
        perm = list(range(n))
        rng.shuffle(perm)
        edges = [(perm[i], perm[rng.randrange(i)]) for i in range(1, n)]
        root = rng.randrange(n)
        vt = VirtualTree(n, edges, root)
        keys = [rng.randrange(n) for _ in range(rng.randint(1, 8))]
        nodes, par = vt.build(keys)
        closed, link = naive(n, edges, root, keys)
        assert set(nodes) == closed and len(nodes) == len(closed)
        assert len(nodes) <= 2 * len(set(keys)) - 1
        assert as_links(nodes, par) == link


if __name__ == "__main__":
    test_example()
    test_single_vertex()
    test_star()
    test_long_path()
    test_random_against_naive()
    print("ok")
