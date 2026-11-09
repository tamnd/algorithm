# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/clarke-wright-savings/. The authors are listed in prov/BGTTNH.jsonl.

import random

from clarke_wright_savings import clarke_wright_savings, routes_cost, savings_list


def manhattan(points: list[tuple[int, int]]) -> list[list[int]]:
    return [[abs(a - c) + abs(b - d) for (c, d) in points] for (a, b) in points]


def cvrp_optimum(dist: list[list[int]], demand: list[int], capacity: int) -> int:
    """Exact optimum by dynamic programming over subsets of customers."""
    n = len(dist) - 1
    full = 1 << n
    inf = float("inf")
    path = [[inf] * n for _ in range(full)]
    for j in range(n):
        path[1 << j][j] = dist[0][j + 1]
    for s in range(1, full):
        for j in range(n):
            v = path[s][j]
            if v == inf:
                continue
            for k in range(n):
                if not (s >> k) & 1:
                    t = s | (1 << k)
                    path[t][k] = min(path[t][k], v + dist[j + 1][k + 1])
    route = [0] * full
    load = [0] * full
    for s in range(1, full):
        route[s] = min(path[s][j] + dist[j + 1][0] for j in range(n) if (s >> j) & 1)
        load[s] = sum(demand[i + 1] for i in range(n) if (s >> i) & 1)
    best = [0] * full
    for s in range(1, full):
        low = s & -s
        rest = s ^ low
        b = inf
        sub = rest
        while True:
            block = sub | low
            if load[block] <= capacity:
                b = min(b, route[block] + best[s ^ block])
            if sub == 0:
                break
            sub = (sub - 1) & rest
        best[s] = b
    return best[full - 1]


def check(dist: list[list[int]], demand: list[int], capacity: int) -> list[list[int]]:
    n = len(dist) - 1
    merges: list[tuple[int, int, int]] = []
    routes = clarke_wright_savings(dist, demand, capacity, merges)
    # Every customer is served exactly once.
    assert sorted(c for r in routes for c in r) == list(range(1, n + 1))
    # Every route respects the capacity.
    assert all(sum(demand[c] for c in r) <= capacity for r in routes)
    # Each merge removes one route, and the cost equals the star cost minus
    # the applied savings, recomputed from scratch.
    assert len(routes) == n - len(merges)
    star = sum(2 * dist[0][i] for i in range(1, n + 1))
    for s, i, j in merges:
        assert s == dist[0][i] + dist[0][j] - dist[i][j] > 0
    assert routes_cost(dist, routes) == star - sum(s for s, _, _ in merges)
    # Each applied merge joins two customers that are adjacent in a route.
    for _, i, j in merges:
        assert any(
            {r[t], r[t + 1]} == {i, j} for r in routes for t in range(len(r) - 1)
        )
    # No positive-saving merge of two route ends is still feasible.
    route_of = {c: k for k, r in enumerate(routes) for c in r}
    ends = {c for r in routes for c in (r[0], r[-1])}
    loads = [sum(demand[c] for c in r) for r in routes]
    for s, i, j in savings_list(dist):
        if s > 0 and i in ends and j in ends and route_of[i] != route_of[j]:
            assert loads[route_of[i]] + loads[route_of[j]] > capacity
    return routes


def test_example() -> None:
    pts = [(0, 0), (2, 4), (-5, 1), (-2, -2), (-4, 3), (-5, 5)]
    demand = [0, 2, 3, 2, 6, 4]
    dist = manhattan(pts)
    merges: list[tuple[int, int, int]] = []
    routes = clarke_wright_savings(dist, demand, 10, merges)
    assert routes == [[1, 2, 3], [4, 5]]
    assert merges == [(14, 4, 5), (4, 2, 3), (2, 1, 2)]
    assert routes_cost(dist, routes) == 46
    assert cvrp_optimum(dist, demand, 10) == 42
    assert routes_cost(dist, [[3, 4], [1, 5, 2]]) == 42
    check(dist, demand, 10)


def test_reversal_and_large_capacity() -> None:
    # Customers on a line to the right of the depot: one route, in order.
    xs = [0, 1, 2, 3, 4]
    dist = [[abs(a - b) for b in xs] for a in xs]
    routes = check(dist, [0, 1, 1, 1, 1], 100)
    assert len(routes) == 1
    assert routes[0] in ([1, 2, 3, 4], [4, 3, 2, 1])
    assert routes_cost(dist, routes) == 8


def test_small_cases() -> None:
    assert clarke_wright_savings([[0]], [0], 5) == []
    assert clarke_wright_savings([[0, 3], [3, 0]], [0, 2], 5) == [[1]]
    try:
        clarke_wright_savings([[0, 3], [3, 0]], [0, 6], 5)
    except ValueError:
        pass
    else:
        raise AssertionError("a demand above the capacity must be rejected")


def test_random_invariants_and_optimum() -> None:
    rng = random.Random(5311)
    for _ in range(600):
        n = rng.randint(1, 7)
        pts = [(rng.randint(-8, 8), rng.randint(-8, 8)) for _ in range(n + 1)]
        dist = manhattan(pts)
        capacity = rng.randint(4, 15)
        demand = [0] + [rng.randint(1, capacity) for _ in range(n)]
        routes = check(dist, demand, capacity)
        cost = routes_cost(dist, routes)
        assert cvrp_optimum(dist, demand, capacity) <= cost <= sum(2 * dist[0][i] for i in range(1, n + 1))
