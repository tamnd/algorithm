# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/saturation-algorithm/. The authors are listed in prov/WW2T0H.jsonl.

import random

from saturation_algorithm import Saturation, reachable_states, successors

# Three processes in a ring pass one token. Level k holds process k:
# 0 = idle, 1 = has the token, 2 = working. Event w_k: 1 -> 2 on level k.
# Event p_k: process k is working (2), goes idle, and gives the token to the
# next process (0 -> 1 on the level below, with level 1 passing to level 3).
RING = [
    {3: {1: [2]}},
    {2: {1: [2]}},
    {1: {1: [2]}},
    {3: {2: [0]}, 2: {0: [1]}},
    {2: {2: [0]}, 1: {0: [1]}},
    {3: {0: [1]}, 1: {2: [0]}},
]


def bfs(sizes, events, init):
    seen = set(init)
    stack = list(init)
    while stack:
        s = stack.pop()
        for e in events:
            for t in successors(sizes, e, s):
                if t not in seen:
                    seen.add(t)
                    stack.append(t)
    return seen


def rand_model(rng):
    K = rng.randint(2, 4)
    sizes = [rng.randint(2, 3) for _ in range(K)]
    events = []
    for _ in range(rng.randint(1, 6)):
        top = rng.randint(1, K)
        bot = rng.randint(1, top)
        ev = {}
        for k in range(bot, top + 1):
            if k in (top, bot) or rng.random() < 0.5:
                n = sizes[k - 1]
                ev[k] = {i: rng.sample(range(n), rng.randint(1, 2)) for i in range(n) if rng.random() < 0.6}
        events.append(ev)
    init = {tuple(rng.randrange(n) for n in sizes) for _ in range(rng.randint(1, 2))}
    return sizes, events, init


def test_ring():
    init = {(0, 0, 1)}
    got, sat, root = reachable_states([3, 3, 3], RING, init)
    assert got == bfs([3, 3, 3], RING, init)
    assert sorted(got) == [(0, 0, 1), (0, 0, 2), (0, 1, 0), (0, 2, 0), (1, 0, 0), (2, 0, 0)]
    assert len(sat.unique) == 6
    assert sat.kids[root] == (6, 3, 3) and sat.firings == 5


def test_random_against_bfs():
    rng = random.Random(2001)
    for _ in range(300):
        sizes, events, init = rand_model(rng)
        got, sat, root = reachable_states(sizes, events, init)
        assert got == bfs(sizes, events, init)
        assert sat.saturate(root) == root


def test_saturated_nodes_are_closed():
    """Each node built is closed under the events whose Top is at most its level."""
    rng = random.Random(77)
    for _ in range(100):
        sizes, events, init = rand_model(rng)
        _, sat, _ = reachable_states(sizes, events, init)
        for p in set(sat.sat_cache.values()):
            if p <= 1:
                continue
            k = sat.level[p]
            low = [{l: m for l, m in e.items()} for e, t in zip(events, sat.top) if t <= k]
            sub = Saturation(sizes[:k], [])
            sub.level, sub.kids, sub.K = sat.level, sat.kids, k
            part = sub.states(p)
            for s in part:
                for e in low:
                    assert set(successors(sizes[:k], e, s)) <= part
