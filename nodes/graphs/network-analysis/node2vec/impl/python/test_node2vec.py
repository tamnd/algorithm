# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/node2vec/. The authors are listed in prov/3SC38Y.jsonl.

import math
import random
from collections import deque

from node2vec import build_graph, node2vec, node2vec_walk, transition_weights


def distance(adj: list[dict[int, float]], s: int, t: int) -> int:
    """Return the number of edges on a shortest path from s to t, or -1."""
    dist = {s: 0}
    queue = deque([s])
    while queue:
        u = queue.popleft()
        for v in adj[u]:
            if v not in dist:
                dist[v] = dist[u] + 1
                queue.append(v)
    return dist.get(t, -1)


def oracle(adj, t, v, p, q):
    """The definition of Grover and Leskovec: alpha = 1/p, 1, 1/q for d(t, x) = 0, 1, 2."""
    out = {}
    for x, w in adj[v].items():
        d = distance(adj, t, x)
        assert d in (0, 1, 2)
        alpha = {0: 1.0 / p, 1: 1.0, 2: 1.0 / q}[d]
        out[x] = w * alpha
    return out


def random_graph(rng: random.Random, n: int, prob: float, weighted: bool):
    edges = []
    for u in range(n):
        for v in range(u + 1, n):
            if rng.random() < prob:
                edges.append((u, v, rng.choice([0.5, 1.0, 2.0, 3.0])) if weighted else (u, v))
    return edges


def test_worked_example() -> None:
    adj = build_graph(6, [(0, 1), (0, 2), (1, 2), (1, 3), (3, 4), (3, 5), (4, 5)])
    for p, q, want in ((1.0, 2.0, {0: 0.4, 2: 0.4, 3: 0.2}), (4.0, 0.5, {0: 1 / 13, 2: 4 / 13, 3: 8 / 13})):
        w = dict(transition_weights(adj, 0, 1, p, q))
        total = sum(w.values())
        for x, pr in want.items():
            assert abs(w[x] / total - pr) < 1e-12


def test_edge_cases() -> None:
    rng = random.Random(1)
    adj = build_graph(3, [(0, 1)])
    assert node2vec_walk(adj, 2, 10, 1.0, 1.0, rng) == [2]
    assert node2vec_walk(adj, 0, 1, 1.0, 1.0, rng) == [0]
    assert node2vec_walk(adj, 0, 6, 0.3, 7.0, rng) == [0, 1, 0, 1, 0, 1]
    assert node2vec(0, [], dim=3) == []
    z = node2vec(3, [(0, 1)], dim=4, walks_per_vertex=2, length=5, seed=3)
    assert len(z) == 3 and all(len(row) == 4 for row in z)
    assert z == node2vec(3, [(0, 1)], dim=4, walks_per_vertex=2, length=5, seed=3)
    for bad in (dict(p=0.0), dict(q=-1.0), dict(dim=0), dict(length=0)):
        try:
            node2vec(2, [(0, 1)], **bad)
        except ValueError:
            pass
        else:
            raise AssertionError("expected ValueError")
    for edges in ([(0, 0)], [(0, 5)], [(0, 1, 0.0)]):
        try:
            build_graph(2, edges)
        except ValueError:
            pass
        else:
            raise AssertionError("expected ValueError")


def test_random_weights_against_definition() -> None:
    rng = random.Random(2016)
    for _ in range(500):
        n = rng.randint(2, 8)
        edges = random_graph(rng, n, rng.random(), rng.random() < 0.5)
        adj = build_graph(n, edges)
        p = rng.choice([0.25, 0.5, 1.0, 2.0, 4.0])
        q = rng.choice([0.25, 0.5, 1.0, 2.0, 4.0])
        for t in range(n):
            for v in adj[t]:
                got = dict(transition_weights(adj, t, v, p, q))
                want = oracle(adj, t, v, p, q)
                assert got.keys() == want.keys()
                for x in want:
                    assert abs(got[x] - want[x]) < 1e-12
                if p == q == 1.0:
                    assert all(abs(got[x] - adj[v][x]) < 1e-12 for x in got)


def test_random_walks_are_valid() -> None:
    rng = random.Random(55)
    for _ in range(500):
        n = rng.randint(1, 8)
        adj = build_graph(n, random_graph(rng, n, rng.random(), True))
        start = rng.randrange(n)
        length = rng.randint(1, 12)
        walk = node2vec_walk(adj, start, length, rng.choice([0.5, 1.0, 2.0]), rng.choice([0.5, 1.0, 2.0]), rng)
        assert walk[0] == start
        assert len(walk) == (length if adj[start] else 1)
        for a, b in zip(walk, walk[1:]):
            assert b in adj[a]


def test_step_frequencies() -> None:
    rng = random.Random(9)
    for _ in range(40):
        n = rng.randint(3, 7)
        adj = build_graph(n, random_graph(rng, n, 0.6, True))
        arcs = [(t, v) for t in range(n) for v in adj[t]]
        if not arcs:
            continue
        t, v = rng.choice(arcs)
        p, q = rng.choice([0.5, 2.0]), rng.choice([0.5, 2.0])
        want = oracle(adj, t, v, p, q)
        total = sum(want.values())
        trials = 6000
        seen = {x: 0 for x in want}
        for _ in range(trials):
            w = node2vec_walk_from(adj, t, v, p, q, rng)
            seen[w] += 1
        for x in want:
            pr = want[x] / total
            assert abs(seen[x] / trials - pr) < 5 * math.sqrt(pr * (1 - pr) / trials) + 1e-9


def node2vec_walk_from(adj, t, v, p, q, rng):
    """Sample the vertex after the step t -> v through node2vec_walk."""
    while True:
        walk = node2vec_walk(adj, t, 3, p, q, rng)
        if walk[1] == v:
            return walk[2]


def test_embedding_separates_cliques() -> None:
    edges = [(i, j) for i in range(5) for j in range(i + 1, 5)]
    edges += [(i, j) for i in range(5, 10) for j in range(i + 1, 10)] + [(4, 5)]
    z = node2vec(10, edges, dim=8, walks_per_vertex=10, length=20, window=3, seed=1)

    def cos(a, b):
        return sum(x * y for x, y in zip(a, b)) / math.sqrt(sum(x * x for x in a) * sum(y * y for y in b))

    within = [cos(z[i], z[j]) for i in range(10) for j in range(i + 1, 10) if (i < 5) == (j < 5)]
    between = [cos(z[i], z[j]) for i in range(5) for j in range(5, 10)]
    assert sum(within) / len(within) > sum(between) / len(between) + 0.3
