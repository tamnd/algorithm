# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/parallel-minimum-spanning-tree/. The authors are listed in prov/8WQPZV.jsonl.

import math
import random

from parallel_minimum_spanning_tree import Cost, parallel_boruvka


def kruskal(n: int, edges: list[tuple[int, int, float]]) -> list[int]:
    parent = list(range(n))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    out = []
    for i in sorted(range(len(edges)), key=lambda i: (edges[i][2], i)):
        u, v, _ = edges[i]
        a, b = find(u), find(v)
        if a != b:
            parent[a] = b
            out.append(i)
    return sorted(out)


EXAMPLE = [(0, 1, 4), (1, 2, 2), (2, 3, 6), (3, 4, 3), (4, 5, 1), (5, 0, 5), (1, 4, 7)]


def test_example() -> None:
    c = Cost()
    F = parallel_boruvka(6, EXAMPLE, c)
    assert F == [0, 1, 3, 4, 5]
    assert sum(EXAMPLE[i][2] for i in F) == 15
    assert c.rounds == 2
    assert c.active == [6, 2]


def family(rng: random.Random) -> list[tuple[int, list[tuple[int, int, float]]]]:
    out = []
    for n in (1, 2, 5, 16, 33):
        pairs = {
            "empty": [],
            "path": [(i, i + 1) for i in range(n - 1)],
            "star": [(0, i) for i in range(1, n)],
            "cycle": [(i, (i + 1) % n) for i in range(n)] if n >= 3 else [],
            "complete": [(i, j) for i in range(n) for j in range(i + 1, n)],
        }
        for es in pairs.values():
            out.append((n, [(u, v, rng.randint(1, 5)) for u, v in es]))  # many ties
            out.append((n, [(u, v, rng.random()) for u, v in es]))
            out.append((n, [(u, v, 1) for u, v in es]))  # all equal
    for _ in range(220):
        n = rng.randint(1, 50)
        p = rng.choice([0.02, 0.05, 0.1, 0.3, 0.7])
        es = [(i, j) for i in range(n) for j in range(i + 1, n) if rng.random() < p]
        if es and rng.random() < 0.3:
            es += rng.sample(es, max(1, len(es) // 4))  # parallel edges
        rng.shuffle(es)
        wmax = rng.choice([3, 1000])
        out.append((n, [(u, v, rng.randint(1, wmax)) for u, v in es]))
    return out


def test_against_kruskal() -> None:
    rng = random.Random(5)
    runs = 0
    for n, edges in family(rng):
        c = Cost()
        F = parallel_boruvka(n, edges, c)
        assert F == kruskal(n, edges)
        assert c.rounds <= math.ceil(math.log2(max(n, 1)))  # c = 1: at most ceil(log2 n) rounds
        for a, b in zip(c.active, c.active[1:]):
            assert b <= a // 2  # the supervertices with an edge at least halve in each round
        lg = math.log2(n + 2)
        assert c.span <= 6 * lg * lg + 6 * lg  # O(log^2 n) span
        runs += 1
    for _ in range(300):
        n = rng.randint(2, 40)
        es = [(i, j, rng.randint(1, 9)) for i in range(n) for j in range(i + 1, n) if rng.random() < 0.2]
        assert parallel_boruvka(n, es) == kruskal(n, es)
        runs += 1
    assert runs >= 500


def test_mean_rounds() -> None:
    # random sparse graphs: the mean number of rounds stays below 0.5 log2 n + 2
    rng = random.Random(3)
    for n in (64, 256):
        total = 0
        for _ in range(10):
            es = [(rng.randrange(n), rng.randrange(n), rng.random()) for _ in range(3 * n)]
            es = [(u, v, w) for u, v, w in es if u != v]
            c = Cost()
            parallel_boruvka(n, es, c)
            total += c.rounds
        assert total / 10 <= 0.5 * math.log2(n) + 2
