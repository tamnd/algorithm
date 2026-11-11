# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/linial-algorithm/. The authors are listed in prov/RAK95W.jsonl.

import itertools
import math
import random

from linial_algorithm import choose, linial_coloring, linial_step, point_set, schedule


def cover_free(sets: list[set[int]], delta: int) -> bool:
    """Brute force: no set is inside the union of delta other sets."""
    for i, s in enumerate(sets):
        others = [t for j, t in enumerate(sets) if j != i]
        for group in itertools.combinations(others, min(delta, len(others))):
            if s <= set().union(*group):
                return False
    return True


def test_polynomial_family_is_cover_free() -> None:
    for q, d, delta in ((3, 1, 2), (5, 1, 4), (5, 2, 2), (7, 1, 3)):
        assert q > delta * d
        sets = [point_set(x, q, d) for x in range(min(q ** (d + 1), 30))]
        assert all(len(s) == q for s in sets)
        assert cover_free(sets, delta)


def test_family_fails_without_the_condition() -> None:
    # q = delta * d: some set is covered by delta others.
    sets = [point_set(x, 3, 1) for x in range(9)]
    assert not cover_free(sets, 3)


def test_random_family_of_the_existence_proof() -> None:
    m, delta = 8, 2
    k = math.floor(math.e * (delta + 1) ** 2 * math.log(m)) + 1
    found = False
    for seed in range(20):
        rng = random.Random(seed)
        sets = [{j for j in range(k) if rng.random() < 1 / (delta + 1)} for _ in range(m)]
        if cover_free(sets, delta):
            found = True
            break
    assert found


def test_choose_meets_its_conditions() -> None:
    for delta in (1, 2, 3, 5, 10):
        for m in (10, 1000, 10**6, 2**64):
            q, d = choose(m, delta)
            assert q > delta * d and q ** (d + 1) >= m
            assert all(q % p for p in range(2, q))


def ring(n: int) -> list[list[int]]:
    return [[(v - 1) % n, (v + 1) % n] for v in range(n)]


def grid(a: int, b: int) -> list[list[int]]:
    adj: list[list[int]] = [[] for _ in range(a * b)]
    for i in range(a):
        for j in range(b):
            v = i * b + j
            if i + 1 < a:
                adj[v].append(v + b)
                adj[v + b].append(v)
            if j + 1 < b:
                adj[v].append(v + 1)
                adj[v + 1].append(v)
    return adj


def bounded_degree(n: int, delta: int, rng: random.Random) -> list[list[int]]:
    adj: list[list[int]] = [[] for _ in range(n)]
    for _ in range(n * delta):
        u, v = rng.randrange(n), rng.randrange(n)
        if u != v and v not in adj[u] and len(adj[u]) < delta and len(adj[v]) < delta:
            adj[u].append(v)
            adj[v].append(u)
    return adj


def proper(adj: list[list[int]], c: list[int]) -> bool:
    return all(c[u] != c[v] for v in range(len(adj)) for u in adj[v])


def test_colouring_on_graph_families() -> None:
    rng = random.Random(4)
    graphs = [ring(30), grid(8, 9), bounded_degree(300, 3, rng), bounded_degree(300, 6, rng)]
    for adj in graphs:
        n = len(adj)
        delta = max(len(a) for a in adj)
        for N in (n, 10**6, 2**40):
            ids = rng.sample(range(N), n)
            history: list[list[int]] = []
            c, rounds = linial_coloring(adj, ids, N, delta, history)
            assert proper(adj, c)
            assert set(c) <= set(range(delta + 1))
            sched = schedule(N, delta)
            m_end = sched[-1][1] ** 2 if sched else N
            assert rounds == len(sched) + max(0, m_end - delta - 1)
            for h, (_, q, _) in zip(history, sched):
                assert proper(adj, h)
                assert max(h) < q * q


def test_step_example() -> None:
    adj = [[1, 2, 3], [0], [0], [0]]
    assert linial_step([100, 5, 77, 288], adj, 7, 2)[0] == 2


def test_schedule_reaches_order_delta_squared() -> None:
    for delta in (2, 3, 5, 10, 30):
        for N in (10**6, 2**64, 2**256):
            sched = schedule(N, delta)
            m_end = sched[-1][1] ** 2
            assert m_end <= (4 * delta + 1) ** 2
            assert len(sched) <= 4
