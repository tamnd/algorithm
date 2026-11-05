# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hub-labeling/. The authors are listed in prov/AFFE5D.jsonl.

import heapq
import math
import random

import pytest

from hub_labeling import hub_labeling, query

C, D, E, F, G, H = range(6)
EXAMPLE = [(C, D, 3), (C, E, 2), (D, F, 4), (E, D, 1), (E, F, 2), (E, G, 3), (F, G, 2), (F, H, 1), (G, H, 2)]


def build(n, arcs):
    adj = [[] for _ in range(n)]
    for u, v, w in arcs:
        adj[u].append((v, w))
    return adj


def dijkstra(adj, s):
    """Independent oracle: plain Dijkstra with a binary heap."""
    dist = [math.inf] * len(adj)
    dist[s] = 0
    heap = [(0, s)]
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue
        for v, w in adj[u]:
            if d + w < dist[v]:
                dist[v] = d + w
                heapq.heappush(heap, (dist[v], v))
    return dist


def check_all_pairs(adj, order=None):
    lout, lin = hub_labeling(adj, order)
    n = len(adj)
    for u in range(n):
        want = dijkstra(adj, u)
        for v in range(n):
            assert query(lout, lin, u, v) == want[v], (u, v)
    for lab in lout + lin:
        ranks = [r for r, _ in lab]
        assert ranks == sorted(ranks) and len(set(ranks)) == len(ranks)
    return lout, lin


def test_example_labels_and_queries():
    adj = build(6, EXAMPLE)
    order = [F, E, D, G, C, H]
    lout, lin = check_all_pairs(adj, order)
    assert lout[C] == [(0, 4), (1, 2), (4, 0)]
    assert lin[H] == [(0, 1), (3, 2), (5, 0)]
    assert sum(map(len, lout)) + sum(map(len, lin)) == 21
    assert query(lout, lin, C, H) == 5
    assert query(lout, lin, D, G) == 6


def test_unreachable_is_inf():
    adj = build(6, EXAMPLE)
    lout, lin = hub_labeling(adj)
    assert query(lout, lin, H, C) == math.inf
    adj = build(3, [(0, 1, 1)])
    lout, lin = check_all_pairs(adj)
    assert query(lout, lin, 0, 2) == math.inf
    assert query(lout, lin, 2, 2) == 0


def test_negative_weight_and_negative_cycle_rejected():
    with pytest.raises(ValueError):
        hub_labeling(build(2, [(0, 1, -1)]))
    with pytest.raises(ValueError):
        hub_labeling(build(3, [(0, 1, 2), (1, 2, -3), (2, 1, 1)]))


def test_bad_order_rejected():
    with pytest.raises(ValueError):
        hub_labeling(build(3, [(0, 1, 1)]), [0, 0, 1])


def test_zero_weights_and_cycles():
    adj = build(4, [(0, 1, 0), (1, 0, 0), (1, 2, 0), (2, 3, 5), (3, 1, 0)])
    for order in ([0, 1, 2, 3], [3, 2, 1, 0], [2, 0, 3, 1]):
        check_all_pairs(adj, order)


def test_empty_and_single_vertex():
    assert hub_labeling([]) == ([], [])
    lout, lin = hub_labeling([[]])
    assert query(lout, lin, 0, 0) == 0


def test_random_against_dijkstra():
    rng = random.Random(20261105)
    for case in range(600):
        n = rng.randint(1, 9)
        m = rng.randint(0, 3 * n)
        arcs = [(rng.randrange(n), rng.randrange(n), rng.choice([0, 1, 2, 3, 5, 8, 2.5])) for _ in range(m)]
        adj = build(n, arcs)
        order = list(range(n))
        rng.shuffle(order)
        check_all_pairs(adj, order if case % 2 else None)
