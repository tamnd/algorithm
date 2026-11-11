# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/low-diameter-decomposition/. The authors are listed in prov/FW9GHE.jsonl.

"""Low-diameter decomposition by exponential shifts (Miller, Peng and Xu), as a synchronous distributed algorithm.

Every node u draws a shift delta_u from the exponential distribution with
rate beta. Node v joins the cluster of the centre u that maximizes
delta_u - dist(u, v), with ties broken by the larger index. Each node keeps
the best (value, centre) pair it has heard; in each round it sends that
pair, and a neighbour that receives (x, u) compares x - 1 with its own pair.
After R rounds with R > max delta, every node holds its true best pair.

Precondition: adj is an undirected simple graph; beta > 0.
Cost: R rounds with messages of one value and one identifier, and
R = O(log n / beta) suffices w.h.p. Each edge is cut with probability at
most 1 - exp(-beta) <= beta, and every cluster is connected with strong
radius at most max delta.
"""

import math
import random
from collections import deque


def mpx(adj: list[list[int]], beta: float, rng: random.Random, R: int | None = None) -> tuple[list[int], list[float], int]:
    """Return (centre of each node, shifts, rounds)."""
    n = len(adj)
    delta = [rng.expovariate(beta) for _ in range(n)]  # @line L1
    best = [(delta[v], v) for v in range(n)]  # @line L2
    if R is None:
        R = math.floor(max(delta, default=0.0)) + 1
    for _ in range(R):  # @line L3
        sent = list(best)  # @line L4
        for v in range(n):  # @line L5
            for u in adj[v]:
                cand = (sent[u][0] - 1, sent[u][1])
                if cand > best[v]:
                    best[v] = cand
    centre = [best[v][1] for v in range(n)]  # @line L6
    return centre, delta, R


def shifted_values(adj: list[list[int]], delta: list[float]) -> list[list[tuple[float, int]]]:
    """Centralized check: for each node v, the pairs (delta_u - dist(u, v), u) with value >= 0, best first."""
    n = len(adj)
    vals: list[list[tuple[float, int]]] = [[] for _ in range(n)]
    for u in range(n):
        dist = {u: 0}
        q = deque([u])
        while q:
            x = q.popleft()
            vals[x].append((delta[u] - dist[x], u))
            if dist[x] + 1 <= delta[u]:
                for y in adj[x]:
                    if y not in dist:
                        dist[y] = dist[x] + 1
                        q.append(y)
    for v in range(n):
        vals[v].sort(reverse=True)
    return vals


def exact_centres(adj: list[list[int]], delta: list[float]) -> list[int]:
    return [vals[0][1] for vals in shifted_values(adj, delta)]


def kept_nodes(adj: list[list[int]], delta: list[float]) -> list[bool]:
    """Nodes whose best value beats the second best by more than 1 (the Elkin-Neiman rule)."""
    out = []
    for vals in shifted_values(adj, delta):
        second = vals[1][0] if len(vals) > 1 else -math.inf
        out.append(vals[0][0] - second > 1)
    return out


def cut_fraction(adj: list[list[int]], centre: list[int]) -> float:
    edges = [(u, v) for u in range(len(adj)) for v in adj[u] if u < v]
    return sum(1 for u, v in edges if centre[u] != centre[v]) / max(1, len(edges))


def strong_radius(adj: list[list[int]], centre: list[int]) -> int:
    """Largest distance from a centre to a member, inside the cluster; -1 if some cluster is not connected to its centre."""
    worst = 0
    for c in set(centre):
        dist = {c: 0}
        q = deque([c])
        while q:
            x = q.popleft()
            for y in adj[x]:
                if centre[y] == c and y not in dist:
                    dist[y] = dist[x] + 1
                    q.append(y)
        members = [v for v in range(len(adj)) if centre[v] == c]
        if len(dist) != len(members):
            return -1
        worst = max(worst, max(dist.values()))
    return worst
