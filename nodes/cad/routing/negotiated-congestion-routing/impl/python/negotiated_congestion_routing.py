# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/negotiated-congestion-routing/. The authors are listed in prov/V8CQHN.jsonl.

"""Negotiated congestion routing (PathFinder) on a global-routing grid.

The routing graph is a grid of width * height gcells. Node (x, y) has the
index y * width + x. Each edge between two neighbor gcells has an integer
capacity. A net is a list of distinct nodes. A route is a set of edge
indices that forms a tree in which every leaf is a pin of the net.

All costs are Fractions, and ties are broken by node index, so a run is
exact and gives the same result each time.
"""

import heapq
from fractions import Fraction
from typing import Sequence, Union

Edge = tuple[int, int]


def grid_edges(width: int, height: int) -> list[Edge]:
    """Edges (u, v) with u < v: first the horizontal edges, then the vertical edges."""
    edges = []
    for y in range(height):
        for x in range(width - 1):
            edges.append((y * width + x, y * width + x + 1))
    for y in range(height - 1):
        for x in range(width):
            edges.append((y * width + x, (y + 1) * width + x))
    return edges


def adjacency(n_nodes: int, edges: Sequence[Edge]) -> list[list[tuple[int, int]]]:
    """For each node, the list of (neighbor, edge index), sorted by neighbor."""
    adj: list[list[tuple[int, int]]] = [[] for _ in range(n_nodes)]
    for e, (u, v) in enumerate(edges):
        adj[u].append((v, e))
        adj[v].append((u, e))
    for lst in adj:
        lst.sort()
    return adj


def route_net(pins: Sequence[int], adj: list[list[tuple[int, int]]], cost: Sequence[Fraction]) -> frozenset[int]:
    """Grow a tree from the first pin. Each step runs Dijkstra from all tree nodes
    to the nearest pin that is not yet reached and adds that path to the tree."""
    tree_nodes = {pins[0]}
    tree_edges: set[int] = set()
    left = set(pins) - tree_nodes
    while left:
        dist = {v: Fraction(0) for v in tree_nodes}
        prev: dict[int, tuple[int, int]] = {}
        heap = [(Fraction(0), v) for v in sorted(tree_nodes)]
        heapq.heapify(heap)
        done: set[int] = set()
        target = -1
        while heap:
            d, u = heapq.heappop(heap)
            if u in done:
                continue
            done.add(u)
            if u in left:
                target = u
                break
            for v, e in adj[u]:
                nd = d + cost[e]
                if v not in dist or nd < dist[v]:
                    dist[v] = nd
                    prev[v] = (u, e)
                    heapq.heappush(heap, (nd, v))
        if target < 0:
            raise ValueError("a pin cannot be reached from the rest of the net")
        v = target
        while v not in tree_nodes:
            u, e = prev[v]
            tree_edges.add(e)
            tree_nodes.add(v)
            v = u
        left -= tree_nodes
    return frozenset(tree_edges)


def overflow_of(occ: Sequence[int], cap: Sequence[int]) -> int:
    """Total overflow: the sum over all edges of max(0, occupancy - capacity)."""
    return sum(max(0, o - c) for o, c in zip(occ, cap))


def occupancy(routes: Sequence[frozenset[int]], n_edges: int) -> list[int]:
    occ = [0] * n_edges
    for r in routes:
        for e in r:
            occ[e] += 1
    return occ


def negotiated_congestion_routing(
    width: int,
    height: int,
    cap: Union[int, Sequence[int]],
    nets: Sequence[Sequence[int]],
    max_iters: int = 50,
    pres_fac_first: Fraction = Fraction(0),
    pres_fac_init: Fraction = Fraction(1, 2),
    pres_fac_mult: Fraction = Fraction(3, 2),
    hist_fac: Fraction = Fraction(1),
    base: Fraction = Fraction(1),
) -> dict:
    """Route all nets with negotiated congestion.

    Returns a dict with the keys routes (one frozenset of edge indices per
    net), overflow, wirelength, iterations and log (a list of the pair
    (overflow, wirelength) after each iteration). The routes are those of the
    best iteration: least overflow, then least wirelength.
    """
    edges = grid_edges(width, height)
    m = len(edges)
    caps = [cap] * m if isinstance(cap, int) else list(cap)
    if len(caps) != m:
        raise ValueError("one capacity per edge is needed")
    adj = adjacency(width * height, edges)
    nets = [list(dict.fromkeys(p)) for p in nets]
    if not nets or max_iters < 1:
        return {"routes": [frozenset()] * len(nets), "overflow": 0, "wirelength": 0, "iterations": 0, "log": []}

    hist = [Fraction(0)] * m  # @line L1
    pres_fac = pres_fac_first
    occ = [0] * m
    routes: list[frozenset[int]] = [frozenset()] * len(nets)
    best = None
    log = []
    it = 0
    for it in range(1, max_iters + 1):  # @line L2
        for i, pins in enumerate(nets):  # @line L3
            for e in routes[i]:  # @line L4
                occ[e] -= 1
            cost = []
            for e in range(m):  # @line L5
                p = 1 + pres_fac * max(0, occ[e] + 1 - caps[e])
                cost.append((base + hist[e]) * p)
            routes[i] = route_net(pins, adj, cost) if len(pins) > 1 else frozenset()  # @line L6
            for e in routes[i]:  # @line L7
                occ[e] += 1
        ov = overflow_of(occ, caps)
        wl = sum(len(r) for r in routes)
        log.append((ov, wl))
        if best is None or (ov, wl) < best[0]:
            best = ((ov, wl), list(routes))
        if ov == 0:  # @line L8
            break
        for e in range(m):  # @line L9
            hist[e] += hist_fac * max(0, occ[e] - caps[e])
        pres_fac = pres_fac_init if pres_fac == 0 else pres_fac * pres_fac_mult  # @line L10
    assert best is not None
    (ov, wl), best_routes = best
    return {"routes": best_routes, "overflow": ov, "wirelength": wl, "iterations": it, "log": log}  # @line L11
