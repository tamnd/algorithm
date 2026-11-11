# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sparse-neighborhood-cover/. The authors are listed in prov/FFF7KM.jsonl.

"""Sparse neighbourhood cover by kernel growing, in the style of Awerbuch and Peleg (sequential).

The input is a graph, a radius r and an integer k >= 1. The output is a
list of clusters (sets of nodes), each with a start node, such that every
ball B(v, r) lies inside some cluster, every cluster has strong radius at
most (2k - 1) r around its start node, and every node lies in at most
k * n^(1/k) clusters.

The work runs in phases. R holds the centres whose balls are not yet
covered; at the start of a phase N = |R| and every centre of R is free.
While a free centre v exists, grow Y = {v}: let Z be the free centres whose
ball meets the union of the balls of Y; if |Z| > N^(1/k) |Y|, set Y = Z and
repeat. Then output the union of the balls of Y as a cluster, remove Y from
R, and make Z not free for the rest of the phase.

Precondition: adj is an undirected simple graph; r >= 0; k >= 1.
Cost: polynomial in n (this is a centralized reference, not a round-efficient algorithm).
"""

from collections import deque


def ball(adj: list[list[int]], v: int, r: int, alive: list[bool] | None = None) -> dict[int, int]:
    """Distances from v up to r, inside the alive nodes if given."""
    dist = {v: 0}
    q = deque([v])
    while q:
        x = q.popleft()
        if dist[x] == r:
            continue
        for y in adj[x]:
            if y not in dist and (alive is None or alive[y]):
                dist[y] = dist[x] + 1
                q.append(y)
    return dist


def av_cover(adj: list[list[int]], r: int, k: int) -> tuple[list[tuple[int, set[int]]], int]:
    """Return ([(start node, cluster)], phases)."""
    n = len(adj)
    balls = [set(ball(adj, v, r)) for v in range(n)]
    remaining = set(range(n))
    clusters: list[tuple[int, set[int]]] = []
    phases = 0
    while remaining:
        phases += 1
        threshold = len(remaining) ** (1.0 / k)
        free = set(remaining)
        while free:
            v = min(free)
            Y = {v}
            kernel = set(balls[v])
            while True:
                Z = {u for u in free if balls[u] & kernel}
                if len(Z) <= threshold * len(Y):
                    break
                Y = Z
                kernel = set().union(*(balls[u] for u in Y))
            clusters.append((v, kernel))
            remaining -= Y
            free -= Z
    return clusters, phases


def overlap(n: int, clusters: list[tuple[int, set[int]]]) -> int:
    count = [0] * n
    for _, c in clusters:
        for x in c:
            count[x] += 1
    return max(count, default=0)


def strong_radius(adj: list[list[int]], start: int, cluster: set[int]) -> int:
    """Largest distance from start to a cluster node inside the cluster; -1 if the cluster is not connected."""
    alive = [x in cluster for x in range(len(adj))]
    dist = ball(adj, start, len(adj), alive)
    if len(dist) != len(cluster):
        return -1
    return max(dist.values())
