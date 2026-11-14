# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/multicommodity-flow-global-routing/. The authors are listed in prov/6WN748.jsonl.

"""Global routing as a fractional multicommodity flow, then randomized rounding.

The routing graph has nodes 0 .. n_nodes - 1 and undirected edges (u, v),
each with a positive capacity. A net has one route out of a set of routes:
all paths between its two pins (the Dijkstra oracle), or an explicit list
of candidate routes. The fractional problem is the linear program

    minimize lam  subject to  sum_P x[i][P] = 1 for each net i,
                              x >= 0,
                              load_e(x) <= lam * c_e for each edge e.

The solver is the averaged multiplicative weights method with a shortest
route oracle, in the style of Garg and Koenemann. All arithmetic is exact.
"""

import heapq
import random
from fractions import Fraction
from typing import Optional, Sequence

Edge = tuple[int, int]
Route = frozenset[int]


def grid_graph(width: int, height: int) -> tuple[int, list[Edge]]:
    """Grid of width * height gcells. Node (x, y) has the index y * width + x."""
    edges = []
    for y in range(height):
        for x in range(width - 1):
            edges.append((y * width + x, y * width + x + 1))
    for y in range(height - 1):
        for x in range(width):
            edges.append((y * width + x, (y + 1) * width + x))
    return width * height, edges


def shortest_route(n_nodes: int, edges: Sequence[Edge], length: Sequence[Fraction], s: int, t: int) -> Route:
    """Dijkstra from s to t. Ties go to the smaller node index. Returns the edge set of the path."""
    adj: list[list[tuple[int, int]]] = [[] for _ in range(n_nodes)]
    for e, (u, v) in enumerate(edges):
        adj[u].append((v, e))
        adj[v].append((u, e))
    dist = {s: Fraction(0)}
    prev: dict[int, tuple[int, int]] = {}
    heap = [(Fraction(0), s)]
    done = set()
    while heap:
        d, u = heapq.heappop(heap)
        if u in done:
            continue
        done.add(u)
        if u == t:
            break
        for v, e in sorted(adj[u]):
            nd = d + length[e]
            if v not in dist or nd < dist[v]:
                dist[v] = nd
                prev[v] = (u, e)
                heapq.heappush(heap, (nd, v))
    if t not in done:
        raise ValueError("the pins of a net are not connected")
    route = set()
    v = t
    while v != s:
        u, e = prev[v]
        route.add(e)
        v = u
    return frozenset(route)


def congestion(routes: Sequence[Route], caps: Sequence[int]) -> Fraction:
    """Largest ratio load / capacity over all edges for one route per net."""
    load = [0] * len(caps)
    for r in routes:
        for e in r:
            load[e] += 1
    return max((Fraction(l, c) for l, c in zip(load, caps)), default=Fraction(0))


def multicommodity_flow_global_routing(
    n_nodes: int,
    edges: Sequence[Edge],
    caps: Sequence[int],
    nets: Sequence[tuple[int, int]],
    eps: Fraction = Fraction(1, 4),
    rounds: int = 200,
    candidates: Optional[Sequence[Sequence[Route]]] = None,
    seed: int = 0,
) -> dict:
    """Return a dict with the keys
    x: for each net, a dict that maps a route to its weight (the weights add up to 1),
    lam_frac: the congestion of x, lower_bound: a proven lower bound on the fractional
    optimum, rho: the width, routes: one route per net after randomized rounding, and
    lam_int: the congestion of the rounded routes.
    With candidates, net i chooses from candidates[i] and nets is not used for routing.
    """
    m = len(edges)
    if any(c <= 0 for c in caps) or len(caps) != m:
        raise ValueError("one positive capacity per edge is needed")
    k = len(candidates) if candidates is not None else len(nets)
    if k == 0 or rounds < 1:
        raise ValueError("at least one net and one round are needed")

    def oracle(i: int, length: list[Fraction]) -> Route:
        if candidates is None:
            s, t = nets[i]
            return shortest_route(n_nodes, edges, length, s, t)
        best = None
        for r in candidates[i]:
            key = sum((length[e] for e in r), Fraction(0))
            if best is None or key < best[0]:
                best = (key, r)
        assert best is not None
        return best[1]

    w = [Fraction(1)] * m  # @line L1
    rho = Fraction(k, min(caps))
    counts: list[dict[Route, int]] = [{} for _ in range(k)]
    lower_bound = Fraction(0)
    for _ in range(rounds):  # @line L2
        total = sum(w)
        length = [w[e] / (total * caps[e]) for e in range(m)]  # @line L3
        load = [0] * m
        for i in range(k):
            r = oracle(i, length)  # @line L4
            counts[i][r] = counts[i].get(r, 0) + 1  # @line L5
            for e in r:
                load[e] += 1
        lower_bound = max(lower_bound, sum((length[e] * load[e] for e in range(m)), Fraction(0)))  # @line L6
        w = [w[e] * (1 + eps * load[e] / (rho * caps[e])) for e in range(m)]  # @line L7

    x = [{r: Fraction(c, rounds) for r, c in cnt.items()} for cnt in counts]  # @line L8
    avg = [Fraction(0)] * m
    for xi in x:
        for r, f in xi.items():
            for e in r:
                avg[e] += f
    lam_frac = max(avg[e] / caps[e] for e in range(m))

    rng = random.Random(seed)
    routes = []
    for cnt in counts:  # @line L9
        pick = rng.randrange(rounds)
        for r, c in cnt.items():
            if pick < c:
                routes.append(r)
                break
            pick -= c
    return {  # @line L10
        "x": x,
        "lam_frac": lam_frac,
        "lower_bound": lower_bound,
        "rho": rho,
        "routes": routes,
        "lam_int": congestion(routes, caps),
    }
