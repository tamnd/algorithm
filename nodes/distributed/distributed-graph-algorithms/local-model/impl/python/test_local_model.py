# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/local-model/. The authors are listed in prov/Y75PP5.jsonl.

import random

import pytest

from local_model import (
    CongestViolation,
    FullInfo,
    Gather,
    SyncBFS,
    all_done,
    ball_view,
    bits,
    distances,
    greedy_colouring,
    run,
    view_from_ball,
)

KINDS = ["path", "cycle", "tree", "grid", "gnp"]


def edges_to_adj(n, edges):
    adj = [[] for _ in range(n)]
    for u, v in sorted(edges):
        adj[u].append(v)
        adj[v].append(u)
    return adj


def make_graph(kind, n, seed):
    rng = random.Random(seed)
    if kind == "path":
        edges = {(v - 1, v) for v in range(1, n)}
    elif kind == "cycle":
        edges = {(v - 1, v) for v in range(1, n)} | ({(0, n - 1)} if n > 2 else set())
    elif kind == "tree":
        edges = {(rng.randrange(v), v) for v in range(1, n)}
    elif kind == "grid":
        a = max(1, int(n**0.5))
        b = max(1, n // a)
        n = a * b
        edges = set()
        for i in range(a):
            for j in range(b):
                v = i * b + j
                if j + 1 < b:
                    edges.add((v, v + 1))
                if i + 1 < a:
                    edges.add((v, v + b))
    else:
        edges = {(rng.randrange(v), v) for v in range(1, n)}
        for u in range(n):
            for v in range(u + 1, n):
                if rng.random() < 0.15:
                    edges.add((u, v))
    adj = edges_to_adj(n, edges)
    for nbrs in adj:  # random port numbers
        rng.shuffle(nbrs)
    return adj


def labels(n, rng):
    ids = rng.sample(range(1, n * n + 2), n)
    inputs = [rng.randrange(2) for _ in range(n)]
    return ids, inputs


def cases():
    for seed in range(40):
        kind = KINDS[seed % len(KINDS)]
        n = 2 + seed % 11
        yield seed, make_graph(kind, n, seed)


def test_bits_encoding():
    assert bits(0) == 3 and bits(1) == 5 and bits(-1) == 5
    assert bits(True) == 3
    assert bits((1, 2)) == 2 + 3 + bits(1) + bits(2)
    assert bits(frozenset({1, 2})) == bits((1, 2))
    assert all(bits(k) <= bits(k + 1) for k in range(0, 300))


def test_r_round_state_is_the_ball_view():
    for seed, adj in cases():
        rng = random.Random(seed)
        ids, inputs = labels(len(adj), rng)
        for r in range(4):
            states, _ = run(adj, ids, inputs, FullInfo(), r)
            for v in range(len(adj)):
                assert states[v] == view_from_ball(ball_view(adj, ids, inputs, v, r))


def outside_change(adj, ids, inputs, v, r, rng):
    """A new network that agrees with the old one on the radius-r ball of v."""
    n = len(adj)
    dist = distances(adj, v)
    far = [u for u in range(n) if dist[u] > r]
    extra = rng.randrange(0, 4) if far else 0
    far_all = far + list(range(n, n + extra))
    new = set()  # all edges between far nodes are replaced by random ones
    for i, a in enumerate(far_all):
        for b in far_all[i + 1 :]:
            if rng.random() < 0.3:
                new.add((a, b))
    for x in range(n, n + extra):  # keep the new nodes connected to the far part
        new.add((rng.choice(far), x))
    m = n + extra
    adj2 = [[] for _ in range(m)]
    for u in range(n):
        if dist[u] <= r:
            adj2[u] = list(adj[u])  # same ports, same degree
    for u in range(n):
        if dist[u] > r:
            adj2[u] = [w for w in adj[u] if dist[w] <= r]  # edges to the ball stay
    for a, b in sorted(new):
        adj2[a].append(b)
        adj2[b].append(a)
    used = {ids[u] for u in range(n) if dist[u] <= r}
    pool = [x for x in range(1, 4 * m * m) if x not in used]
    rng.shuffle(pool)
    ids2 = [ids[u] if u < n and dist[u] <= r else pool.pop() for u in range(m)]
    inputs2 = [inputs[u] if u < n and dist[u] <= r else rng.randrange(2) for u in range(m)]
    return adj2, ids2, inputs2


def test_changes_outside_the_ball_are_invisible():
    for seed, adj in cases():
        rng = random.Random(1000 + seed)
        ids, inputs = labels(len(adj), rng)
        for r in range(3):
            states, _ = run(adj, ids, inputs, FullInfo(), r)
            for v in range(len(adj)):
                adj2, ids2, inputs2 = outside_change(adj, ids, inputs, v, r, rng)
                states2, _ = run(adj2, ids2, inputs2, FullInfo(), r)
                assert states2[v] == states[v]


def test_a_change_at_distance_r_is_visible():
    adj = make_graph("path", 8, 0)
    ids = list(range(1, 9))
    for r in range(1, 6):
        a, _ = run(adj, ids, [0] * 8, FullInfo(), r)
        b, _ = run(adj, ids, [0] * r + [1] + [0] * (7 - r), FullInfo(), r)
        assert a[0] != b[0]  # node r is at distance r from node 0
        c, _ = run(adj, ids, [0] * (r + 1) + [1] + [0] * (6 - r), FullInfo(), r)
        assert a[0] == c[0]  # node r + 1 is not


def test_gather_detects_the_whole_graph_at_ecc_plus_one():
    for seed, adj in cases():
        rng = random.Random(seed)
        n = len(adj)
        ids, inputs = labels(n, rng)
        states, stats = run(adj, ids, inputs, Gather(), 4 * n, stop=all_done)
        ecc = [max(distances(adj, v).values()) for v in range(n)]
        assert [s[5] for s in states] == [e + 1 for e in ecc]
        assert stats["rounds"] == max(ecc) + 1  # D + 1
        truth = {ids[u]: (inputs[u], tuple(ids[w] for w in adj[u])) for u in range(n)}
        for s in states:
            assert s[4] == truth
        colours = [greedy_colouring(s[4]) for s in states]
        assert all(c == colours[0] for c in colours)
        col = colours[0]
        assert all(col[ids[u]] != col[ids[w]] for u in range(n) for w in adj[u])
        assert max(col.values()) <= max(len(x) for x in adj)  # at most Delta + 1 colours


def test_congest_mode_accepts_bfs_and_rejects_gathering():
    for seed, adj in cases():
        n = len(adj)
        rng = random.Random(seed)
        ids, _ = labels(n, rng)
        inputs = [1] + [0] * (n - 1)
        states, stats = run(adj, ids, inputs, SyncBFS(), n, mode="CONGEST", c=4)
        assert [s[1] for s in states] == [distances(adj, 0)[v] for v in range(n)]
        assert stats["messages"] == sum(len(x) for x in adj)  # every node sends once on every port
    star = edges_to_adj(30, {(0, v) for v in range(1, 30)})
    ids = list(range(1, 31))
    _, stats = run(star, ids, [0] * 30, Gather(), 3)  # LOCAL: fine
    assert stats["max_bits"] > 8 * 5
    with pytest.raises(CongestViolation):
        run(star, ids, [0] * 30, Gather(), 3, mode="CONGEST", c=8)
