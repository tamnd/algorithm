# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/itai-rodeh-girth-algorithm/. The authors are listed in prov/SX075V.jsonl.

import random
from collections import deque

from itai_rodeh_girth_algorithm import itai_rodeh_girth_algorithm


def girth_oracle(n, edges):
    """Independent oracle: the shortest cycle through edge e = (u, v) has length
    1 + dist(u, v) in the graph without e; a loop is a cycle of length 1."""
    best = None
    for f, (u, v) in enumerate(edges):
        if u == v:
            c = 1
        else:
            dist = {u: 0}
            q = deque([u])
            while q:
                x = q.popleft()
                for g, (a, b) in enumerate(edges):
                    if g == f or x not in (a, b):
                        continue
                    y = b if x == a else a
                    if y not in dist:
                        dist[y] = dist[x] + 1
                        q.append(y)
            if v not in dist:
                continue
            c = dist[v] + 1
        best = c if best is None or c < best else best
    return best


def is_cycle(edges, res) -> bool:
    vs, es = res
    k = len(vs)
    if k == 0 or len(es) != k or len(set(vs)) != k or len(set(es)) != k:
        return False
    for i in range(k):
        a, b = vs[i], vs[(i + 1) % k]
        if edges[es[i]] not in ((a, b), (b, a)):
            return False
    return True


EXAMPLE = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0), (4, 5), (5, 6), (6, 3)]


def test_example() -> None:
    res = itai_rodeh_girth_algorithm(8, EXAMPLE)
    assert res is not None and is_cycle(EXAMPLE, res)
    assert len(res[0]) == 4 and sorted(res[0]) == [3, 4, 5, 6]


def test_small_cases() -> None:
    assert itai_rodeh_girth_algorithm(0, []) is None
    assert itai_rodeh_girth_algorithm(1, []) is None
    assert itai_rodeh_girth_algorithm(1, [(0, 0)]) == ([0], [0])
    assert itai_rodeh_girth_algorithm(2, [(0, 1), (1, 0)]) == ([0, 1], [1, 0])
    assert itai_rodeh_girth_algorithm(3, [(0, 1), (1, 2), (2, 0)]) is not None
    # trees and forests, with isolated vertices
    assert itai_rodeh_girth_algorithm(6, [(0, 1), (1, 2), (1, 3), (4, 5)]) is None
    # a loop away from a triangle wins
    edges = [(0, 1), (1, 2), (2, 0), (3, 3)]
    assert itai_rodeh_girth_algorithm(4, edges) == ([3], [3])


def test_petersen() -> None:
    outer = [(i, (i + 1) % 5) for i in range(5)]
    spokes = [(i, i + 5) for i in range(5)]
    inner = [(5 + i, 5 + (i + 2) % 5) for i in range(5)]
    edges = outer + spokes + inner
    res = itai_rodeh_girth_algorithm(10, edges)
    assert res is not None and is_cycle(edges, res) and len(res[0]) == 5


def test_long_cycle() -> None:
    n = 400
    edges = [(i, (i + 1) % n) for i in range(n)]
    res = itai_rodeh_girth_algorithm(n, edges)
    assert res is not None and len(res[0]) == n and is_cycle(edges, res)


def test_random_against_oracle() -> None:
    rng = random.Random(1978)
    for trial in range(700):
        n = rng.randint(1, 8)
        m = rng.randint(0, 11)
        edges = []
        for _ in range(m):
            u = rng.randrange(n)
            v = u if rng.random() < 0.05 else rng.randrange(n)
            edges.append((u, v))
        want = girth_oracle(n, edges)
        got = itai_rodeh_girth_algorithm(n, edges)
        if want is None:
            assert got is None
        else:
            assert got is not None and is_cycle(edges, got) and len(got[0]) == want
