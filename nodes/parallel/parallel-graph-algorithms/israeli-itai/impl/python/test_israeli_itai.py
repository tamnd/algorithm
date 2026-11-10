# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/israeli-itai/. The authors are listed in prov/NSTYXT.jsonl.

import math
import random
from functools import lru_cache

from israeli_itai import Cost, israeli_itai


def family(rng: random.Random) -> list[tuple[int, list[tuple[int, int]]]]:
    out = []
    for n in (1, 2, 3, 8, 9, 30):
        out.append((n, []))
        out.append((n, [(i, i + 1) for i in range(n - 1)]))
        out.append((n, [(0, i) for i in range(1, n)]))
        if n >= 3:
            out.append((n, [(i, (i + 1) % n) for i in range(n)]))
        out.append((n, [(i, j) for i in range(n) for j in range(i + 1, n)]))
    for _ in range(200):
        n = rng.randint(1, 60)
        p = rng.choice([0.02, 0.05, 0.1, 0.3, 0.8])
        out.append((n, [(i, j) for i in range(n) for j in range(i + 1, n) if rng.random() < p]))
    return out


def maximum_matching_size(n: int, edges: list[tuple[int, int]]) -> int:
    nb = [0] * n
    for u, v in edges:
        nb[u] |= 1 << v
        nb[v] |= 1 << u

    @lru_cache(maxsize=None)
    def best(free: int) -> int:
        if free == 0:
            return 0
        v = (free & -free).bit_length() - 1
        rest = free & ~(1 << v)
        out = best(rest)
        cand = nb[v] & rest
        while cand:
            u = (cand & -cand).bit_length() - 1
            cand &= cand - 1
            out = max(out, 1 + best(rest & ~(1 << u)))
        return out

    return best((1 << n) - 1)


def check_maximal_matching(n: int, edges: list[tuple[int, int]], m: list[tuple[int, int]]) -> None:
    es = {(min(u, v), max(u, v)) for u, v in edges if u != v}
    used = [False] * n
    for u, v in m:
        assert (u, v) in es
        assert not used[u] and not used[v]
        used[u] = used[v] = True
    assert all(used[u] or used[v] for u, v in es)  # maximal


def test_example() -> None:
    edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (1, 4)]
    script = [
        ({0: 1, 1: 2, 2: 1, 3: 4, 4: 1, 5: 4}, {1: 0, 2: 1, 4: 5}, {0: 1, 1: 0, 2: 1, 4: 5, 5: 4}),
        ({2: 3, 3: 2}, {2: 3, 3: 2}, {2: 3, 3: 2}),
    ]
    c = Cost()
    m = israeli_itai(6, edges, cost=c, script=script)
    assert m == [(0, 1), (2, 3), (4, 5)]
    assert c.rounds == 2 and c.edges == [6, 1]


def test_against_brute_force() -> None:
    rng = random.Random(6)
    runs = 0
    for n, edges in family(rng):
        for _ in range(3):
            m = israeli_itai(n, edges, random.Random(rng.random()))
            check_maximal_matching(n, edges, m)
            if n <= 12:
                assert 2 * len(m) >= maximum_matching_size(n, edges)  # a maximal matching is a 1/2-approximation
            runs += 1
    assert runs >= 500


def test_good_vertices_cover_half_the_edges() -> None:
    rng = random.Random(7)
    for _ in range(300):
        n = rng.randint(2, 40)
        p = rng.choice([0.05, 0.2, 0.6])
        edges = [(i, j) for i in range(n) for j in range(i + 1, n) if rng.random() < p]
        adj: list[list[int]] = [[] for _ in range(n)]
        for u, v in edges:
            adj[u].append(v)
            adj[v].append(u)
        d = [len(a) for a in adj]
        good = [3 * sum(1 for u in adj[v] if d[u] <= d[v]) >= d[v] for v in range(n)]
        assert 2 * sum(1 for u, v in edges if good[u] or good[v]) >= len(edges)


def test_edges_shrink_and_rounds() -> None:
    # the proof gives E[m_(t+1)] <= q m_t with q = 1 - (1 - e^(-1/3)) / 4 < 0.93;
    # on random graphs with 2n edges the mean number of rounds stays below 0.5 log2 n + 1 (c = 0.5)
    rng = random.Random(8)
    before = after = 0
    for n in (64, 256, 1024):
        total = 0
        for _ in range(10):
            edges = set()
            while len(edges) < 2 * n:
                u, v = rng.randrange(n), rng.randrange(n)
                if u != v:
                    edges.add((min(u, v), max(u, v)))
            c = Cost()
            israeli_itai(n, sorted(edges), random.Random(rng.random()), c)
            total += c.rounds
            before += sum(c.edges)
            after += sum(c.edges[1:])
            assert c.span <= 4 * math.ceil(math.log2(n + 1)) * (c.rounds + 1)
        assert total / 10 <= 0.5 * math.log2(n) + 1
    assert after <= 0.93 * before
