# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/symmetric-network-congestion-min-cost-flow/. The authors are listed in prov/KZRBES.jsonl.

"""A pure Nash equilibrium of a symmetric network congestion game, by min-cost flow.

The network is directed. Vertices are hashable labels. An edge is a triple (u, v, costs),
where costs[j - 1] is c_e(j), the cost that each of the j players on the edge pays.
The costs of an edge must be nonnegative and nondecreasing in j. All n players go from
s to t, and a strategy is a simple s-t path, given as a list of edge indices.

The algorithm minimizes Rosenthal's potential Phi = sum_e sum_{j <= x_e} c_e(j) over all
integral flows of value n by successive shortest paths with the marginal costs
c_e(x_e + 1) forward and -c_e(x_e) backward, and then splits the flow into n paths.
A profile that minimizes Phi is a pure Nash equilibrium.
"""

from fractions import Fraction
from typing import Hashable, Sequence

Edge = tuple[Hashable, Hashable, Sequence]


def _check(edges: Sequence[Edge], n: int) -> None:
    if n < 1:
        raise ValueError("there must be at least one player")
    for u, v, costs in edges:
        if len(costs) < n:
            raise ValueError("each edge needs the costs c_e(1), ..., c_e(n)")
        if any(c < 0 for c in costs[:n]):
            raise ValueError("costs must be nonnegative")
        if any(costs[j] > costs[j + 1] for j in range(n - 1)):
            raise ValueError("costs must be nondecreasing in the number of users")


def _cheapest_path(vertices, edges, x, s, t, n):
    """Bellman-Ford on the residual graph. Return a list of (edge index, +1 or -1), or None."""
    dist = {v: None for v in vertices}
    pred = {}
    dist[s] = Fraction(0)
    for _ in range(len(vertices) - 1):
        changed = False
        for e, (u, v, costs) in enumerate(edges):
            if x[e] < n and dist[u] is not None:  # forward arc u -> v
                d = dist[u] + costs[x[e]]  # c_e(x_e + 1)
                if dist[v] is None or d < dist[v]:
                    dist[v], pred[v], changed = d, (e, 1), True
            if x[e] > 0 and dist[v] is not None:  # backward arc v -> u
                d = dist[v] - costs[x[e] - 1]  # -c_e(x_e)
                if dist[u] is None or d < dist[u]:
                    dist[u], pred[u], changed = d, (e, -1), True
        if not changed:
            break
    if dist[t] is None:
        return None
    path, w = [], t
    while w != s:
        e, d = pred[w]
        path.append((e, d))
        u, v, _ = edges[e]
        w = u if d == 1 else v
    path.reverse()
    return path


def min_potential_flow(vertices, edges: Sequence[Edge], s, t, n: int) -> list[int]:
    """Return integral edge loads x of an s-t flow of value n that minimize Rosenthal's potential."""
    _check(edges, n)
    vertices = list(vertices)
    x = [0] * len(edges)  # @line L1
    for _ in range(n):  # @line L2
        path = _cheapest_path(vertices, edges, x, s, t, n)  # @line L3
        if path is None:
            raise ValueError("t is not reachable from s")
        for e, d in path:  # @line L4
            x[e] += d
    return x


def split_into_paths(edges: Sequence[Edge], x: list[int], s, t, n: int) -> list[list[int]]:
    """Split the flow x of value n into n simple s-t paths. Cycles met on the way are removed."""
    x = list(x)
    out = {}
    for e, (u, v, _) in enumerate(edges):
        out.setdefault(u, []).append(e)
    ptr = {u: 0 for u in out}  # x only goes down here, so an edge with x = 0 is never needed again
    paths = []
    for _ in range(n):  # @line L5
        walk, where = [], {s: 0}  # walk is a list of edges; where maps a vertex to its place
        w = s
        while w != t:  # @line L6
            lst = out[w]
            while x[lst[ptr[w]]] == 0:
                ptr[w] += 1
            e = lst[ptr[w]]
            v = edges[e][1]
            if v in where:  # @line L7: the walk closes a cycle, so remove it
                i = where[v]
                for f in walk[i:] + [e]:
                    x[f] -= 1
                for f in walk[i:]:
                    del where[edges[f][1]]
                walk = walk[:i]
                w = v
            else:
                walk.append(e)
                where[v] = len(walk)
                w = v
        for f in walk:  # @line L8
            x[f] -= 1
        paths.append(walk)
    return paths  # @line L9


def symmetric_congestion_equilibrium(vertices, edges: Sequence[Edge], s, t, n: int) -> list[list[int]]:
    """Return a pure Nash equilibrium: one simple s-t path (a list of edge indices) per player."""
    x = min_potential_flow(vertices, edges, s, t, n)
    return split_into_paths(edges, x, s, t, n)


def loads(edges: Sequence[Edge], paths: list[list[int]]) -> list[int]:
    """Return the number of players on each edge."""
    x = [0] * len(edges)
    for p in paths:
        for e in p:
            x[e] += 1
    return x


def rosenthal_potential(edges: Sequence[Edge], paths: list[list[int]]) -> Fraction:
    """Return Phi = sum over edges of c_e(1) + ... + c_e(x_e)."""
    x = loads(edges, paths)
    return sum((Fraction(c) for e, (_, _, costs) in enumerate(edges) for c in costs[: x[e]]), Fraction(0))


def player_costs(edges: Sequence[Edge], paths: list[list[int]]) -> list[Fraction]:
    """Return the cost of each player: the sum of c_e(x_e) over the edges of its path."""
    x = loads(edges, paths)
    return [sum((Fraction(edges[e][2][x[e] - 1]) for e in p), Fraction(0)) for p in paths]
