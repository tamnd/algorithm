# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/negotiated-congestion-routing/. The authors are listed in prov/V8CQHN.jsonl.

import itertools
import random
from fractions import Fraction

from negotiated_congestion_routing import (
    adjacency,
    grid_edges,
    negotiated_congestion_routing,
    occupancy,
    overflow_of,
    route_net,
)


def is_route(width: int, height: int, pins: list[int], route: frozenset[int]) -> bool:
    """Checker: the edges form a tree that holds all pins, and every leaf is a pin."""
    edges = grid_edges(width, height)
    pins_set = set(pins)
    if len(pins_set) == 1:
        return not route
    deg: dict[int, int] = {}
    nbr: dict[int, list[int]] = {}
    for e in route:
        if not 0 <= e < len(edges):
            return False
        u, v = edges[e]
        for a, b in ((u, v), (v, u)):
            deg[a] = deg.get(a, 0) + 1
            nbr.setdefault(a, []).append(b)
    nodes = set(deg)
    if not pins_set <= nodes or len(route) != len(nodes) - 1:
        return False
    if any(d == 1 and v not in pins_set for v, d in deg.items()):
        return False
    start = next(iter(nodes))
    seen = {start}
    stack = [start]
    while stack:
        u = stack.pop()
        for v in nbr[u]:
            if v not in seen:
                seen.add(v)
                stack.append(v)
    return seen == nodes


_SUBTREES: dict[tuple[int, int], list[tuple[frozenset[int], frozenset[int], frozenset[int]]]] = {}


def subtrees(width: int, height: int) -> list[tuple[frozenset[int], frozenset[int], frozenset[int]]]:
    """Every nonempty edge subset of the grid that is a tree, with its nodes and its leaves."""
    if (width, height) not in _SUBTREES:
        edges = grid_edges(width, height)
        m = len(edges)
        out = []
        for mask in range(1, 1 << m):
            route = frozenset(e for e in range(m) if mask >> e & 1)
            nodes = frozenset(v for e in route for v in edges[e])
            if is_route(width, height, sorted(nodes), route):
                deg = {v: sum(v in edges[e] for e in route) for v in nodes}
                out.append((route, nodes, frozenset(v for v in nodes if deg[v] == 1)))
        _SUBTREES[(width, height)] = out
    return _SUBTREES[(width, height)]


def all_trees(width: int, height: int, pins: list[int]) -> list[frozenset[int]]:
    """Brute force: every edge subset of the grid that is a valid route of the net."""
    p = set(pins)
    return [r for r, nodes, leaves in subtrees(width, height) if p <= nodes and leaves <= p]


def brute_force(width: int, height: int, caps: list[int], nets: list[list[int]]) -> tuple[int, int]:
    """Least (total overflow, wirelength) over all combinations of routes."""
    m = len(grid_edges(width, height))
    cands = [all_trees(width, height, p) for p in nets]
    best = None
    for combo in itertools.product(*cands):
        key = (overflow_of(occupancy(combo, m), caps), sum(len(r) for r in combo))
        if best is None or key < best:
            best = key
    assert best is not None
    return best


def sequential(width: int, height: int, caps: list[int], nets: list[list[int]]) -> int:
    """Route the nets once, in order, each one on a shortest path that avoids full edges
    when it can. Return the total overflow."""
    edges = grid_edges(width, height)
    adj = adjacency(width * height, edges)
    occ = [0] * len(edges)
    big = Fraction(10**6)
    for pins in nets:
        cost = [Fraction(1) if occ[e] < caps[e] else big for e in range(len(edges))]
        for e in route_net(pins, adj, cost):
            occ[e] += 1
    return overflow_of(occ, caps)


def coords(width: int, route: frozenset[int], height: int = 3) -> list[tuple[tuple[int, int], tuple[int, int]]]:
    edges = grid_edges(width, height)
    return sorted(((u % width, u // width), (v % width, v // width)) for u, v in (edges[e] for e in route))


def test_example() -> None:
    # 3 x 3 grid, capacity 1. Net A joins (1,0) and (0,1). Net B joins (0,0) and (2,2).
    nets = [[1, 3], [0, 8]]
    assert sequential(3, 3, [1] * 12, nets) == 1
    assert sequential(3, 3, [1] * 12, nets[::-1]) == 0
    assert brute_force(3, 3, [1] * 12, nets) == (0, 6)
    r = negotiated_congestion_routing(3, 3, 1, nets)
    assert r["log"] == [(1, 6), (0, 6)]
    assert r["iterations"] == 2
    assert coords(3, r["routes"][0]) == [((0, 1), (1, 1)), ((1, 0), (1, 1))]
    assert coords(3, r["routes"][1]) == [((0, 0), (0, 1)), ((0, 1), (0, 2)), ((0, 2), (1, 2)), ((1, 2), (2, 2))]
    first = negotiated_congestion_routing(3, 3, 1, nets, max_iters=1)
    assert coords(3, first["routes"][0]) == [((0, 0), (0, 1)), ((0, 0), (1, 0))]


def test_single_net_is_shortest() -> None:
    rng = random.Random(3)
    for _ in range(50):
        w, h = rng.randrange(1, 7), rng.randrange(1, 7)
        if w * h < 2:
            continue
        s, t = rng.sample(range(w * h), 2)
        r = negotiated_congestion_routing(w, h, 1, [[s, t]])
        assert r["overflow"] == 0
        assert r["wirelength"] == abs(s % w - t % w) + abs(s // w - t // w)


def test_edges_cases() -> None:
    assert negotiated_congestion_routing(2, 2, 1, [])["routes"] == []
    r = negotiated_congestion_routing(2, 2, 1, [[3, 3]])
    assert r["routes"] == [frozenset()] and r["overflow"] == 0
    # Two nets on the only edge of a 2 x 1 grid with capacity 1 cannot both fit.
    r = negotiated_congestion_routing(2, 1, 1, [[0, 1], [1, 0]], max_iters=5)
    assert r["overflow"] == 1 and r["iterations"] == 5


def test_against_brute_force() -> None:
    rng = random.Random(1)
    legal = solved = 0
    for _ in range(80):
        caps = [rng.choice([0, 1, 1, 2]) for _ in range(12)]
        k = rng.choice([2, 3])
        nets = [rng.sample(range(9), rng.choice([2, 2, 3]) if k == 2 else 2) for _ in range(k)]
        best_ov, best_wl = brute_force(3, 3, caps, nets)
        r = negotiated_congestion_routing(3, 3, caps, nets, max_iters=30)
        for pins, route in zip(nets, r["routes"]):
            assert is_route(3, 3, pins, route)
        occ = occupancy(r["routes"], 12)
        assert r["overflow"] == overflow_of(occ, caps) >= best_ov
        assert r["wirelength"] == sum(len(x) for x in r["routes"])
        if r["overflow"] == 0:
            assert all(o <= c for o, c in zip(occ, caps))
            assert r["wirelength"] >= best_wl
        if best_ov == 0:
            legal += 1
            solved += r["overflow"] == 0
    # Measured on these seeds, not a theorem: every instance with a legal routing was solved.
    assert legal > 20 and solved == legal


def test_larger_grids_are_valid() -> None:
    rng = random.Random(7)
    for _ in range(4):
        w = h = 6
        m = len(grid_edges(w, h))
        caps = [rng.choice([1, 2]) for _ in range(m)]
        nets = [rng.sample(range(w * h), rng.choice([2, 3, 4])) for _ in range(12)]
        r = negotiated_congestion_routing(w, h, caps, nets, max_iters=20)
        for pins, route in zip(nets, r["routes"]):
            assert is_route(w, h, pins, route)
        assert r["overflow"] == min(ov for ov, _ in r["log"])
        again = negotiated_congestion_routing(w, h, caps, nets, max_iters=20)
        assert again == r
