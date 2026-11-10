# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/locally-dominant-matching/. The authors are listed in prov/EHBHSK.jsonl.

import math
import random
from functools import lru_cache

from locally_dominant_matching import Cost, locally_dominant_matching

Edges = list[tuple[int, int, float]]


def greedy(n: int, edges: Edges) -> list[int]:
    used = [False] * n
    out = []
    for i in sorted(range(len(edges)), key=lambda i: (edges[i][2], i), reverse=True):
        u, v, _ = edges[i]
        if u != v and not used[u] and not used[v]:
            used[u] = used[v] = True
            out.append(i)
    return sorted(out)


def max_weight(n: int, edges: Edges) -> float:
    inc: list[list[tuple[int, float]]] = [[] for _ in range(n)]
    for u, v, w in edges:
        if u != v:
            inc[u].append((v, w))
            inc[v].append((u, w))

    @lru_cache(maxsize=None)
    def best(free: int) -> float:
        if free == 0:
            return 0
        v = (free & -free).bit_length() - 1
        rest = free & ~(1 << v)
        out = best(rest)
        for u, w in inc[v]:
            if rest >> u & 1:
                out = max(out, w + best(rest & ~(1 << u)))
        return out

    return best((1 << n) - 1)


def longest_chain(edges: Edges) -> int:
    # the most edges on a path of the line graph along which the key decreases
    order = sorted(range(len(edges)), key=lambda i: (edges[i][2], i), reverse=True)
    at: dict[int, list[int]] = {}
    depth = {}
    for i in order:
        u, v, _ = edges[i]
        if u == v:
            continue
        depth[i] = 1 + max((depth[j] for x in (u, v) for j in at.get(x, [])), default=0)
        at.setdefault(u, []).append(i)
        at.setdefault(v, []).append(i)
    return max(depth.values(), default=0)


def family(rng: random.Random) -> list[tuple[int, Edges]]:
    graphs: list[tuple[int, list[tuple[int, int]]]] = []
    for n in (1, 2, 3, 8, 11):
        graphs.append((n, []))
        graphs.append((n, [(i, i + 1) for i in range(n - 1)]))
        graphs.append((n, [(0, i) for i in range(1, n)]))
        if n >= 3:
            graphs.append((n, [(i, (i + 1) % n) for i in range(n)]))
        graphs.append((n, [(i, j) for i in range(n) for j in range(i + 1, n)]))
    for _ in range(120):
        n = rng.randint(1, 12)
        p = rng.choice([0.1, 0.3, 0.6, 0.9])
        graphs.append((n, [(i, j) for i in range(n) for j in range(i + 1, n) if rng.random() < p]))
    out = []
    for n, es in graphs:
        out.append((n, [(u, v, rng.randint(1, 3)) for u, v in es]))  # many ties
        out.append((n, [(u, v, rng.random()) for u, v in es]))
    return out


def test_example() -> None:
    edges: Edges = [(0, 1, 5), (1, 2, 7), (2, 3, 6), (3, 4, 3), (0, 4, 4), (1, 3, 2)]
    c = Cost()
    m = locally_dominant_matching(5, edges, c)
    assert m == [1, 4]  # {1,2} in round 1, {0,4} in round 2
    assert c.rounds == 2


def test_against_greedy_and_brute_force() -> None:
    rng = random.Random(9)
    runs = 0
    for n, edges in family(rng):
        for _ in range(2):
            es = edges[:]
            rng.shuffle(es)
            c = Cost()
            m = locally_dominant_matching(n, es, c)
            assert m == greedy(n, es)
            used = [False] * n
            for i in m:
                u, v, _ = es[i]
                assert not used[u] and not used[v]
                used[u] = used[v] = True
            assert all(used[u] or used[v] for u, v, _ in es if u != v)  # maximal
            assert 2 * sum(es[i][2] for i in m) >= max_weight(n, es) - 1e-9  # 1/2-approximation
            assert c.rounds <= longest_chain(es)
            runs += 1
    assert runs >= 500


def test_increasing_path_is_slow() -> None:
    for n in (2, 3, 10, 51, 200):
        c = Cost()
        m = locally_dominant_matching(n, [(i, i + 1, i) for i in range(n - 1)], c)
        assert c.rounds == n // 2
        assert len(m) == n // 2


def test_mean_rounds_random_weights() -> None:
    # random graphs with 2n edges and random weights: c = 1, the mean number of rounds stays below log2 n
    rng = random.Random(10)
    for n in (64, 256, 1024):
        total = 0
        for _ in range(10):
            es = set()
            while len(es) < 2 * n:
                u, v = rng.randrange(n), rng.randrange(n)
                if u != v:
                    es.add((min(u, v), max(u, v)))
            c = Cost()
            locally_dominant_matching(n, [(u, v, rng.random()) for u, v in sorted(es)], c)
            total += c.rounds
            assert c.work <= 40 * (n + 2 * n) * math.ceil(math.log2(n))
        assert total / 10 <= math.log2(n)
