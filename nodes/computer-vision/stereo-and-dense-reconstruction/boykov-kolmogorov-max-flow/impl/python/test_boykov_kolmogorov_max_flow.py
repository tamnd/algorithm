# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/boykov-kolmogorov-max-flow/. The authors are listed in prov/FXPM4P.jsonl.

import itertools
import random
from collections import deque

from boykov_kolmogorov_max_flow import bk_max_flow, cut_capacity, grid_graph


def brute_min_cut(n, edges, s, t):
    """The least cut capacity over all node sets with s and without t."""
    others = [v for v in range(n) if v not in (s, t)]
    best = None
    for bits in itertools.product((False, True), repeat=len(others)):
        side = [False] * n
        side[s] = True
        for v, b in zip(others, bits):
            side[v] = b
        c = cut_capacity(n, edges, side)
        if best is None or c < best:
            best = c
    return best


def edmonds_karp(n, edges, s, t):
    """Reference max flow by shortest augmenting paths."""
    cap = {}
    adj = [set() for _ in range(n)]
    for (u, v, c) in edges:
        cap[(u, v)] = cap.get((u, v), 0) + c
        cap.setdefault((v, u), 0)
        adj[u].add(v)
        adj[v].add(u)
    flow = 0
    while True:
        prev = {s: None}
        queue = deque([s])
        while queue and t not in prev:
            u = queue.popleft()
            for v in adj[u]:
                if v not in prev and cap[(u, v)] > 0:
                    prev[v] = u
                    queue.append(v)
        if t not in prev:
            return flow
        path = []
        v = t
        while prev[v] is not None:
            path.append((prev[v], v))
            v = prev[v]
        delta = min(cap[e] for e in path)
        for (u, v) in path:
            cap[(u, v)] -= delta
            cap[(v, u)] += delta
        flow += delta


def check_flow(n, edges, s, t, value, side, edge_flow):
    assert side[s] and not side[t]
    net = [0] * n
    for (u, v, c), f in zip(edges, edge_flow):
        assert 0 <= f <= c
        net[u] -= f
        net[v] += f
    for v in range(n):
        if v not in (s, t):
            assert net[v] == 0
    assert net[t] == value == -net[s]
    # The cut of the final S tree is saturated, so it is a minimum cut.
    assert cut_capacity(n, edges, side) == value


def random_graph(rng, n, m, cmax):
    edges = []
    for _ in range(m):
        u, v = rng.randrange(n), rng.randrange(n)
        if u != v:
            edges.append((u, v, rng.randint(0, cmax)))
    return edges


def test_small_example():
    # s = 0, a = 1, b = 2, t = 3.
    edges = [(0, 1, 3), (0, 2, 2), (1, 2, 1), (1, 3, 2), (2, 3, 3)]
    value, side, f = bk_max_flow(4, edges, 0, 3)
    assert value == 5
    assert side == [True, False, False, False]
    check_flow(4, edges, 0, 3, value, side, f)


def test_against_brute_force_cuts():
    rng = random.Random(1)
    for _ in range(300):
        n = rng.randint(2, 9)
        edges = random_graph(rng, n, rng.randint(0, 3 * n), 6)
        value, side, f = bk_max_flow(n, edges, 0, n - 1)
        assert value == brute_min_cut(n, edges, 0, n - 1)
        check_flow(n, edges, 0, n - 1, value, side, f)


def test_against_edmonds_karp_on_grids():
    rng = random.Random(2)
    for _ in range(20):
        w, h = rng.randint(2, 9), rng.randint(2, 9)
        tc = [[(rng.choice((0, 0, rng.randint(1, 20))),
                rng.choice((0, 0, rng.randint(1, 20)))) for _ in range(w)]
              for _ in range(h)]
        lam = rng.randint(1, 8)
        n, edges, s, t = grid_graph(w, h, tc, lambda *a: lam)
        value, side, f = bk_max_flow(n, edges, s, t)
        assert value == edmonds_karp(n, edges, s, t)
        check_flow(n, edges, s, t, value, side, f)


def test_parallel_and_antiparallel_edges():
    rng = random.Random(3)
    for _ in range(100):
        n = rng.randint(3, 7)
        edges = random_graph(rng, n, 4 * n, 4)
        edges += [(u, v, c) for (u, v, c) in edges[: n]]
        edges += [(v, u, c) for (u, v, c) in edges[: n]]
        value, side, f = bk_max_flow(n, edges, n - 1, 0)
        assert value == brute_min_cut(n, edges, n - 1, 0)
        check_flow(n, edges, n - 1, 0, value, side, f)


def test_no_path():
    value, side, f = bk_max_flow(3, [(1, 2, 5), (2, 0, 4)], 0, 2)
    assert value == 0 and side == [True, False, False]
