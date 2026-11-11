# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/synchronizer/. The authors are listed in prov/S5XWV5.jsonl.

import random

from synchronizer import run_alpha, run_beta, run_sync

KINDS = ["tree", "path", "grid", "gnp"]


# ------------------------------------------------ synchronous test algorithms


class SyncBFS:
    """Synchronous BFS from node 0: sparse messages, few rounds active."""

    def __init__(self, v, nbrs):
        self.v, self.nbrs = v, nbrs
        self.out = 0 if v == 0 else None
        self.fresh = v == 0

    def send(self, p):
        if not self.fresh:
            return []
        self.fresh = False
        return [(w, self.out) for w in self.nbrs]

    def receive(self, p, msgs):
        if self.out is None and msgs:
            self.out = min(d for _, d in msgs) + 1
            self.fresh = True


class MinFlood:
    """Every node sends its current minimum to all neighbours in every round."""

    def __init__(self, v, nbrs):
        self.nbrs = nbrs
        self.out = (v * 7919) % 1009

    def send(self, p):
        return [(w, self.out) for w in self.nbrs]

    def receive(self, p, msgs):
        for _, x in msgs:
            self.out = min(self.out, x)


class HashWalk:
    """Message pattern that depends on the state and the round number."""

    def __init__(self, v, nbrs):
        self.v, self.nbrs = v, nbrs
        self.out = v

    def send(self, p):
        return [(w, (self.out * 31 + p) % 997) for w in self.nbrs if (self.out + w + p) % 3 == 0]

    def receive(self, p, msgs):
        for u, x in msgs:
            self.out = (self.out * 17 + x + u) % 100003


ALGS = [SyncBFS, MinFlood, HashWalk]


# ------------------------------------------------------------------- graphs


def edges_to_adj(n, edges):
    adj = [[] for _ in range(n)]
    for u, v in sorted(edges):
        adj[u].append(v)
        adj[v].append(u)
    return adj


def make_graph(kind, n, seed):
    rng = random.Random(seed)
    tree = {(rng.randrange(v), v) for v in range(1, n)}
    if kind == "path":
        return edges_to_adj(n, {(v - 1, v) for v in range(1, n)})
    if kind == "tree":
        return edges_to_adj(n, tree)
    if kind == "grid":
        a = max(1, int(n**0.5))
        b = max(1, n // a)
        edges = set()
        for i in range(a):
            for j in range(b):
                v = i * b + j
                if j + 1 < b:
                    edges.add((v, v + 1))
                if i + 1 < a:
                    edges.add((v, v + b))
        return edges_to_adj(a * b, edges)
    p = rng.uniform(0.05, 0.4)
    edges = set(tree)
    for u in range(n):
        for v in range(u + 1, n):
            if rng.random() < p:
                edges.add((u, v))
    return edges_to_adj(n, edges)


def bfs_tree(adj, r):
    parent = [-1] * len(adj)
    parent[r] = r
    depth = [0] * len(adj)
    frontier = [r]
    while frontier:
        nxt = []
        for v in frontier:
            for w in adj[v]:
                if parent[w] < 0:
                    parent[w] = v
                    depth[w] = depth[v] + 1
                    nxt.append(w)
        frontier = nxt
    return parent, max(depth)


def cases(count, offset):
    for seed in range(count):
        adj = make_graph(KINDS[seed % 4], 1 + seed % 20, seed + offset)
        n = len(adj)
        m = sum(len(a) for a in adj) // 2
        yield seed, adj, n, m, ALGS[seed % 3], 1 + seed % 6


def test_alpha_matches_synchronous_run_and_overhead():
    for seed, adj, n, m, alg, P in cases(120, 0):
        ref = run_sync(adj, alg, P)
        res = run_alpha(adj, alg, P, seed)
        assert res["out"] == ref["out"]
        assert res["trace"] == ref["trace"]
        assert res["alg_messages"] == ref["alg_messages"]
        assert res["count"].get("ACK", 0) == ref["alg_messages"]
        assert res["count"].get("SAFE", 0) == 2 * m * P
        assert res["time"] <= 3 * P + 1e-9


def test_beta_matches_synchronous_run_and_overhead():
    for seed, adj, n, m, alg, P in cases(120, 500):
        parent, h = bfs_tree(adj, seed % n)
        ref = run_sync(adj, alg, P)
        res = run_beta(adj, parent, alg, P, seed)
        assert res["out"] == ref["out"]
        assert res["trace"] == ref["trace"]
        assert res["count"].get("ACK", 0) == ref["alg_messages"]
        assert res["count"].get("SUBTREE_SAFE", 0) == (n - 1) * P
        assert res["count"].get("PULSE", 0) == (n - 1) * P
        assert res["time"] <= P * (2 * h + 2) + 1e-9


def test_beta_on_a_deep_tree_is_slow_alpha_on_dense_graph_is_costly():
    # Complete graph on 12 nodes, P = 4 rounds of MinFlood.
    n, P = 12, 4
    adj = edges_to_adj(n, {(u, v) for u in range(n) for v in range(u + 1, n)})
    m = n * (n - 1) // 2
    a = run_alpha(adj, MinFlood, P, 1)
    path_tree = [max(0, v - 1) for v in range(n)]  # a Hamiltonian path, height n - 1
    star_tree = [0] * n  # height 1
    b_star = run_beta(adj, star_tree, MinFlood, P, 1)
    b_path = run_beta(adj, path_tree, MinFlood, P, 1)
    assert a["count"]["SAFE"] == 2 * m * P > b_star["count"]["PULSE"] * 2
    assert b_path["time"] > b_star["time"]
    assert a["out"] == b_star["out"] == b_path["out"] == run_sync(adj, MinFlood, P)["out"]
