# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pregel-model/. The authors are listed in prov/VS4KBS.jsonl.

import heapq
import random
from fractions import Fraction

from pregel_model import INF, max_value, pagerank, sssp


def random_graph(rng, n, m, wmax=9):
    out = [[] for _ in range(n)]
    seen = set()
    for _ in range(m):
        u, v = rng.randrange(n), rng.randrange(n)
        if u != v and (u, v) not in seen:
            seen.add((u, v))
            out[u].append((v, rng.randint(1, wmax)))
    return out


def dijkstra(n, out, s):
    dist = [INF] * n
    dist[s] = 0
    pq = [(0, s)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for v, w in out[u]:
            if d + w < dist[v]:
                dist[v] = d + w
                heapq.heappush(pq, (d + w, v))
    return dist


def last_change(n, out, s):
    """Synchronous Bellman-Ford: the last round in which each vertex improved."""
    d = [INF] * n
    d[s] = 0
    last = {s: 0}
    k = 0
    while True:
        k += 1
        nd = list(d)
        for u in range(n):
            for v, w in out[u]:
                nd[v] = min(nd[v], d[u] + w)
        changed = [v for v in range(n) if nd[v] < d[v]]
        if not changed:
            return last
        for v in changed:
            last[v] = k
        d = nd


def test_sssp_matches_dijkstra_and_superstep_count():
    rng = random.Random(1)
    for trial in range(60):
        n = rng.randint(1, 30)
        out = random_graph(rng, n, rng.randint(0, 4 * n))
        s = rng.randrange(n)
        p = rng.randint(1, 5)
        dist, g = sssp(n, out, s, p=p)
        assert dist == dijkstra(n, out, s)
        last = last_change(n, out, s)
        senders = [last[v] for v in last if out[v]]
        expected = 2 + max(senders) if senders else 1
        assert len(g.log) == expected
        dist2, g2 = sssp(n, out, s, p=p, combine=False)
        assert dist2 == dist
        assert sum(x.messages for x in g.log) <= sum(x.messages for x in g2.log)


def test_sssp_on_a_path():
    n = 6
    out = [[(i + 1, 1)] for i in range(n - 1)] + [[]]
    dist, g = sssp(n, out, 0, p=2)
    assert dist == list(range(n))
    assert len(g.log) == n  # the last vertex has no out-edges
    assert all(x.h <= 1 for x in g.log)


def power_iteration(n, out, k, alpha):
    x = [Fraction(1, n)] * n
    for _ in range(k):
        dangling = sum(x[u] for u in range(n) if not out[u])
        y = [(1 - alpha) / n + alpha * dangling / n] * n
        for u in range(n):
            for v, _ in out[u]:
                y[v] += alpha * x[u] / len(out[u])
        x = y
    return x


def test_pagerank_matches_power_iteration_exactly():
    rng = random.Random(2)
    alpha = Fraction(85, 100)
    for trial in range(25):
        n = rng.randint(1, 12)
        out = random_graph(rng, n, rng.randint(0, 3 * n))
        k = rng.randint(0, 8)
        ranks, g = pagerank(n, out, k, alpha, p=rng.randint(1, 4))
        assert ranks == power_iteration(n, out, k, alpha)
        assert sum(ranks) == 1
        assert len(g.log) == k + 1


def test_max_value():
    rng = random.Random(3)
    for trial in range(40):
        n = rng.randint(1, 25)
        und = random_graph(rng, n, 2 * n)
        out = [list(e) for e in und]
        for u in range(n):
            for v, w in und[u]:
                out[v].append((u, w))
        vals = [rng.randint(0, 100) for _ in range(n)]
        res, g = max_value(n, out, vals)
        # Each vertex ends with the largest value in its connected component.
        comp = list(range(n))

        def find(x):
            while comp[x] != x:
                comp[x] = comp[comp[x]]
                x = comp[x]
            return x
        for u in range(n):
            for v, _ in out[u]:
                comp[find(u)] = find(v)
        best = {}
        for v in range(n):
            best[find(v)] = max(best.get(find(v), -1), vals[v])
        assert res == [best[find(v)] for v in range(n)]
