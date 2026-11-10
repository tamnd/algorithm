# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/floodmax/. The authors are listed in prov/ZNV8N8.jsonl.

import random
from collections import deque

from floodmax import diameter, floodmax, random_connected_graph


def path(n: int) -> list[list[int]]:
    return [[w for w in (v - 1, v + 1) if 0 <= w < n] for v in range(n)]


def within(adj: list[list[int]], s: int, r: int) -> set[int]:
    dist = {s: 0}
    q = deque([s])
    while q:
        v = q.popleft()
        for w in adj[v]:
            if w not in dist:
                dist[w] = dist[v] + 1
                q.append(w)
    return {v for v, d in dist.items() if d <= r}


def check(adj: list[list[int]], ids: list[int]) -> None:
    n = len(adj)
    m = sum(len(a) for a in adj) // 2
    d = diameter(adj)
    res = floodmax(adj, ids, d)
    top = ids.index(max(ids))
    assert res["leaders"] == [top]
    assert res["known"] == [max(ids)] * n
    assert res["messages"] == 2 * m * d
    # the invariant: after round r, max is the largest id within distance r
    for r, row in enumerate(res["history"]):
        for v in range(n):
            assert row[v] == max(ids[w] for w in within(adj, v, r))
    opt = floodmax(adj, ids, d, opt=True)
    assert opt["leaders"] == [top] and opt["known"] == res["known"]
    assert opt["messages"] <= res["messages"]
    # a larger bound on the diameter also works
    assert floodmax(adj, ids, d + 2)["leaders"] == [top]


def test_page_example() -> None:
    adj = path(5)
    ids = [3, 1, 5, 2, 7]
    res = floodmax(adj, ids, 4)
    assert res["history"] == [
        [3, 1, 5, 2, 7],
        [3, 5, 5, 7, 7],
        [5, 5, 7, 7, 7],
        [5, 7, 7, 7, 7],
        [7, 7, 7, 7, 7],
    ]
    assert res["leaders"] == [4] and res["messages"] == 32
    assert floodmax(adj, ids, 4, opt=True)["messages"] == 17
    short = floodmax(adj, ids, 3)
    assert short["known"][0] == 5


def test_random_graphs() -> None:
    rng = random.Random(42)
    for t in range(60):
        n = rng.randrange(1, 40)
        adj = random_connected_graph(n, rng.randrange(0, 2 * n + 1), seed=t)
        ids = rng.sample(range(1000), n)
        check(adj, ids)


def test_too_few_rounds_can_break() -> None:
    for n in range(2, 12):
        ids = [n - 2] + list(range(n - 2)) + [n - 1]
        res = floodmax(path(n), ids, n - 2)
        assert res["leaders"] == [0, n - 1]
