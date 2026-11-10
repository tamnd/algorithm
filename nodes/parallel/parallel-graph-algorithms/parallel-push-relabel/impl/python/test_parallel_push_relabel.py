# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/parallel-push-relabel/. The authors are listed in prov/R2Q1DA.jsonl.

import math
import random
from collections import deque

from parallel_push_relabel import Cost, parallel_push_relabel

Arcs = list[tuple[int, int, int]]


def edmonds_karp(n: int, arcs: Arcs, s: int, t: int) -> int:
    """Sequential reference: shortest augmenting paths found by BFS."""
    to: list[int] = []
    res: list[int] = []
    adj: list[list[int]] = [[] for _ in range(n)]
    for u, v, c in arcs:
        adj[u].append(len(to))
        to.append(v)
        res.append(c)
        adj[v].append(len(to))
        to.append(u)
        res.append(0)
    value = 0
    while True:
        prev = [-1] * n
        seen = [False] * n
        seen[s] = True
        q = deque([s])
        while q and not seen[t]:
            u = q.popleft()
            for a in adj[u]:
                if res[a] > 0 and not seen[to[a]]:
                    seen[to[a]] = True
                    prev[to[a]] = a
                    q.append(to[a])
        if not seen[t]:
            return value
        x = math.inf
        v = t
        while v != s:
            x = min(x, res[prev[v]])
            v = to[prev[v] ^ 1]
        v = t
        while v != s:
            res[prev[v]] -= x
            res[prev[v] ^ 1] += x
            v = to[prev[v] ^ 1]
        value += x


def check_flow(n: int, arcs: Arcs, s: int, t: int, value: int, flow: list[int]) -> None:
    """The flow is feasible, has the given value, and a cut of equal capacity exists."""
    bal = [0] * n
    for (u, v, c), f in zip(arcs, flow):
        assert 0 <= f <= c
        bal[u] -= f
        bal[v] += f
    assert all(bal[v] == 0 for v in range(n) if v != s and v != t)
    assert bal[t] == value
    adj: list[list[int]] = [[] for _ in range(n)]  # residual graph of the result
    for (u, v, c), f in zip(arcs, flow):
        if f < c:
            adj[u].append(v)
        if f > 0:
            adj[v].append(u)
    side = {s}
    stack = [s]
    while stack:
        u = stack.pop()
        for v in adj[u]:
            if v not in side:
                side.add(v)
                stack.append(v)
    assert t not in side
    assert sum(c for u, v, c in arcs if u in side and v not in side) == value


def family(rng: random.Random) -> list[tuple[int, list[tuple[int, int]]]]:
    out: list[tuple[int, list[tuple[int, int]]]] = []
    for n in (2, 3, 7, 25):
        out.append((n, []))
        out.append((n, [(i, i + 1) for i in range(n - 1)]))  # path
        out.append((n, [(0, i) for i in range(1, n)] + [(i, n - 1) for i in range(1, n - 1)]))  # star, then to t
        out.append((n, [(i, (i + 1) % n) for i in range(n)] + [((i + 1) % n, i) for i in range(n)]))  # cycle
        out.append((n, [(i, j) for i in range(n) for j in range(n) if i != j]))  # complete
    for _ in range(120):
        n = rng.randint(2, 30)
        p = rng.choice([0.05, 0.1, 0.2, 0.4, 0.8])
        out.append((n, [(i, j) for i in range(n) for j in range(n) if i != j and rng.random() < p]))
    return out


def test_example() -> None:
    arcs: Arcs = [(0, 1, 3), (0, 2, 2), (1, 2, 1), (1, 3, 1), (2, 3, 3)]
    c = Cost()
    value, flow = parallel_push_relabel(4, arcs, 0, 3, c)
    assert value == 4
    check_flow(4, arcs, 0, 3, value, flow)
    assert flow == [2, 2, 1, 1, 3]
    assert (c.pulses, c.relabels, c.pushes) == (4, 4, 5)


def test_against_edmonds_karp() -> None:
    rng = random.Random(17)
    runs = 0
    for n, es in family(rng):
        for _ in range(4):
            arcs = [(u, v, rng.choice([0, 1, 1, 2, 5, 10, 100])) for u, v in es]
            if rng.random() < 0.2:  # parallel arcs and loops
                arcs += [(u, v, rng.randint(0, 5)) for u, v, _ in arcs[:3]] + [(0, 0, 4)]
            s, t = rng.sample(range(n), 2)
            c = Cost()
            value, flow = parallel_push_relabel(n, arcs, s, t, c)
            assert value == edmonds_karp(n, arcs, s, t)
            check_flow(n, arcs, s, t, value, flow)
            assert c.pulses < 4 * n * n
            runs += 1
    assert runs >= 500


def test_pulses_on_random_graphs() -> None:
    # random digraphs with m = 4n arcs and capacities in 1..100: the mean number of pulses
    # stays below c n with c = 16, far below the proved bound 4 n^2 (it is not polylogarithmic:
    # without global relabeling, the excess that cannot reach t climbs above d(s) = n first)
    rng = random.Random(18)
    for n in (32, 128, 512):
        pulses = 0
        for _ in range(4):
            arcs = [(rng.randrange(n), rng.randrange(n), rng.randint(1, 100)) for _ in range(4 * n)]
            c = Cost()
            parallel_push_relabel(n, arcs, 0, n - 1, c)
            pulses += c.pulses
        assert pulses / 4 <= 16 * n
