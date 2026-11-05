# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/eppstein-k-shortest-paths/. The authors are listed in prov/WNETNH.jsonl.

import math
import random

import pytest

from eppstein_k_shortest_paths import eppstein

INF = math.inf
# s=0, a=1, b=2, t=3
EXAMPLE = [(0, 1, 1), (0, 2, 2), (1, 2, 0), (1, 3, 3), (2, 3, 1), (3, 0, 4)]


def build(n, edges):
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    return adj


def dist_to(adj, t):
    """Independent oracle: Bellman-Ford distances to t, or None on a negative cycle
    that reaches t."""
    n = len(adj)
    d = [INF] * n
    d[t] = 0
    for _ in range(n):
        changed = False
        for u in range(n):
            for v, w in adj[u]:
                if d[v] + w < d[u]:
                    d[u] = d[v] + w
                    changed = True
        if not changed:
            return d
    return None


def brute(adj, s, t, k):
    """Independent oracle: the k smallest s-t walk weights, by counting walks.

    With h = dist(., t), every edge has reduced weight r = w + h[v] - h[u] >= 0, and a
    walk weighs h[s] plus its reduced weight. N_c(v), the number of v-t walks of
    reduced weight c (capped at k), satisfies N_c(v) = [v = t, c = 0] + sum over
    edges (v, x) of N_{c - r}(x); iterating it level by level reaches the fixed point.
    """
    n = len(adj)
    h = dist_to(adj, t)
    if h[s] == INF:
        return []
    live = [h[v] < INF for v in range(n)]
    red = [[(x, w + h[x] - h[v]) for x, w in adj[v] if live[x]] if live[v] else [] for v in range(n)]
    # if the walks from s are finite in number, all are simple paths of reduced weight <= limit
    limit = (n - 1) * max([r for v in range(n) for _, r in red[v]] + [0])
    reach = {s}
    stack = [s]
    while stack:
        u = stack.pop()
        for x, _ in red[u]:
            if x not in reach:
                reach.add(x)
                stack.append(x)
    cyclic = _has_cycle(red, reach)
    levels = []
    out = []
    c = 0
    while len(out) < k and (cyclic or c <= limit):
        base = [1 if (v == t and c == 0) else 0 for v in range(n)]
        for v in range(n):
            for x, r in red[v]:
                if 0 < r <= c:
                    base[v] = min(k, base[v] + levels[c - r][x])
        cur = base
        while True:  # zero reduced-weight edges stay within the level
            nxt = base[:]
            for v in range(n):
                for x, r in red[v]:
                    if r == 0:
                        nxt[v] = min(k, nxt[v] + cur[x])
            if nxt == cur:
                break
            cur = nxt
        levels.append(cur)
        out += [h[s] + c] * cur[s]
        c += 1
    return out[:k]


def _has_cycle(g, verts):
    color = dict.fromkeys(verts, 0)
    for r in verts:
        if color[r]:
            continue
        stack = [(r, iter(g[r]))]
        color[r] = 1
        while stack:
            u, it = stack[-1]
            for x, _ in it:
                if color.get(x) == 1:
                    return True
                if color.get(x) == 0:
                    color[x] = 1
                    stack.append((x, iter(g[x])))
                    break
            else:
                color[u] = 2
                stack.pop()
    return False


def weight(adj, walk):
    total = 0
    for u, v in zip(walk, walk[1:]):
        total += min(w for x, w in adj[u] if x == v)
    return total


def test_example() -> None:
    got = eppstein(build(4, EXAMPLE), 0, 3, 6)
    assert got == [
        (2, [0, 1, 2, 3]),
        (3, [0, 2, 3]),
        (4, [0, 1, 3]),
        (8, [0, 1, 2, 3, 0, 1, 2, 3]),
        (9, [0, 2, 3, 0, 1, 2, 3]),
        (9, [0, 1, 2, 3, 0, 2, 3]),
    ]


def test_k_zero_and_one() -> None:
    adj = build(4, EXAMPLE)
    assert eppstein(adj, 0, 3, 0) == []
    assert eppstein(adj, 0, 3, 1) == [(2, [0, 1, 2, 3])]


def test_unreachable_target() -> None:
    adj = build(4, [(0, 1, 1), (2, 3, 1), (3, 2, -5)])
    assert eppstein(adj, 0, 3, 5) == []


def test_fewer_than_k_walks() -> None:
    adj = build(3, [(0, 1, 2), (1, 2, 2), (0, 2, 5)])
    assert eppstein(adj, 0, 2, 10) == [(4, [0, 1, 2]), (5, [0, 2])]


def test_source_equals_target() -> None:
    adj = build(2, [(0, 1, 1), (1, 0, 2)])
    assert eppstein(adj, 0, 0, 3) == [(0, [0]), (3, [0, 1, 0]), (6, [0, 1, 0, 1, 0])]


def test_negative_cycle_on_a_walk_is_rejected() -> None:
    adj = build(3, [(0, 1, 1), (1, 1, -1), (1, 2, 1)])
    with pytest.raises(ValueError):
        eppstein(adj, 0, 2, 3)


def test_negative_cycle_off_every_walk_is_ignored() -> None:
    # 2 <-> 3 is a negative cycle reachable from s, but it cannot reach t = 1
    adj = build(4, [(0, 1, 3), (0, 2, 1), (2, 3, -2), (3, 2, 1)])
    assert eppstein(adj, 0, 1, 2) == [(3, [0, 1])]


def test_negative_edges_without_negative_cycles() -> None:
    adj = build(3, [(0, 1, 4), (1, 2, -3), (0, 2, 2), (2, 0, 1)])
    got = eppstein(adj, 0, 2, 4)
    assert [c for c, _ in got] == [1, 2, 3, 4]


def test_parallel_edges_give_distinct_walks() -> None:
    adj = build(2, [(0, 1, 1), (0, 1, 1), (0, 1, 2)])
    assert [c for c, _ in eppstein(adj, 0, 1, 5)] == [1, 1, 2]


def test_zero_weight_cycle() -> None:
    adj = build(3, [(0, 1, 1), (1, 0, 0), (1, 2, 1)])
    got = eppstein(adj, 0, 2, 4)
    assert [c for c, _ in got] == [2, 3, 4, 5]


def test_random_against_brute_force() -> None:
    rng = random.Random(1998)
    cases = 0
    while cases < 600:
        n = rng.randint(1, 6)
        edges = set()
        for _ in range(rng.randint(0, 12)):
            u, v = rng.randrange(n), rng.randrange(n)
            edges.add((u, v, rng.randint(-2, 6)))
        best = {}
        for u, v, w in edges:  # no parallel edges, so vertex lists name walks
            best[(u, v)] = min(w, best.get((u, v), w))
        adj = build(n, [(u, v, w) for (u, v), w in best.items()])
        s, t, k = rng.randrange(n), rng.randrange(n), rng.randint(1, 12)
        if dist_to(adj, t) is None:
            continue  # a negative cycle reaches t; rejection is tested above
        try:
            got = eppstein(adj, s, t, k)
        except ValueError:
            continue
        cases += 1
        want = brute(adj, s, t, k)
        assert [c for c, _ in got] == want
        walks = [tuple(w) for _, w in got]
        assert len(set(walks)) == len(walks)
        for c, w in got:
            assert w[0] == s and w[-1] == t and weight(adj, w) == c
