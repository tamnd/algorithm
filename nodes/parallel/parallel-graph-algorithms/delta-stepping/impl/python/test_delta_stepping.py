# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/delta-stepping/. The authors are listed in prov/CXP7SG.jsonl.

import heapq
import math
import random

from delta_stepping import Cost, delta_stepping

Edges = list[tuple[int, int, float]]


def dijkstra(n: int, edges: Edges, s: int) -> tuple[list[float], list[int]]:
    """Distances, and the fewest edges on a shortest path, for each vertex."""
    adj: list[list[tuple[int, float]]] = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    best: list[tuple[float, int]] = [(math.inf, 0)] * n
    best[s] = (0.0, 0)
    pq = [(0.0, 0, s)]
    while pq:
        d, h, u = heapq.heappop(pq)
        if (d, h) > best[u]:
            continue
        for v, w in adj[u]:
            if (d + w, h + 1) < best[v]:
                best[v] = (d + w, h + 1)
                heapq.heappush(pq, (d + w, h + 1, v))
    return [d for d, _ in best], [h for _, h in best]


def family(rng: random.Random) -> list[tuple[int, Edges]]:
    graphs: list[tuple[int, list[tuple[int, int]]]] = []
    for n in (1, 2, 7, 30):
        graphs.append((n, []))
        graphs.append((n, [(i, i + 1) for i in range(n - 1)] + [(i + 1, i) for i in range(n - 1)]))
        graphs.append((n, [(0, i) for i in range(1, n)] + [(i, 0) for i in range(1, n)]))
        graphs.append((n, [(i, (i + 1) % n) for i in range(n)]))
        graphs.append((n, [(i, j) for i in range(n) for j in range(n) if i != j]))
    for _ in range(100):
        n = rng.randint(1, 60)
        p = rng.choice([0.02, 0.05, 0.1, 0.3, 0.7])
        graphs.append((n, [(i, j) for i in range(n) for j in range(n) if i != j and rng.random() < p]))
    out = []
    for n, es in graphs:
        out.append((n, [(u, v, rng.randint(0, 10)) for u, v in es]))  # integer weights, with zeros
        out.append((n, [(u, v, rng.random()) for u, v in es]))
    return out


def test_example() -> None:
    edges: Edges = [(0, 1, 1), (0, 2, 4), (1, 2, 1), (1, 3, 5), (2, 3, 1), (3, 4, 3), (2, 4, 7)]
    c = Cost()
    d = delta_stepping(5, edges, 0, 2, c)
    assert d == [0, 1, 2, 3, 6]
    assert c.buckets == 3 and c.phases == 5


def test_against_dijkstra() -> None:
    rng = random.Random(15)
    runs = 0
    for n, edges in family(rng):
        s = rng.randrange(n)
        want, hops = dijkstra(n, edges, s)
        wmin = min((w for _, _, w in edges if w > 0), default=1)
        for delta in (wmin / 2, 0.3, 1, 3, 1e9):
            c = Cost()
            got = delta_stepping(n, edges, s, delta, c)
            assert all(math.isclose(a, b, abs_tol=1e-9) or a == b == math.inf for a, b in zip(got, want))
            if delta == 1e9:  # one bucket: the phases are at most the most edges on a shortest path, plus 1
                assert c.phases <= max((h for h, d in zip(hops, want) if d < math.inf), default=0) + 1
            runs += 1
        c = Cost()
        delta_stepping(n, [(u, v, w) for u, v, w in edges if w > 0], s, wmin / 2, c)
        assert c.phases == c.buckets  # every edge is heavy: one phase per bucket
    assert runs >= 500


def test_random_weights() -> None:
    # random digraphs with m = 4n arcs, weights uniform in [0, 1) and delta = 1/4 (1 over the
    # mean degree): the mean work stays below 2 (n + m), and the mean number of phases stays
    # below c log2 n with c = 5
    rng = random.Random(16)
    for n in (64, 256, 1024):
        work = phases = 0
        for _ in range(5):
            es = [(rng.randrange(n), rng.randrange(n), rng.random()) for _ in range(4 * n)]
            c = Cost()
            got = delta_stepping(n, es, 0, 0.25, c)
            want, _ = dijkstra(n, es, 0)
            assert all(math.isclose(a, b, abs_tol=1e-9) or a == b == math.inf for a, b in zip(got, want))
            work += c.work
            phases += c.phases
        assert work / 5 <= 2 * (n + 4 * n)
        assert phases / 5 <= 5 * math.log2(n)
