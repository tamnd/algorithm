# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/distributed-minimum-vertex-cover/. The authors are listed in prov/511N17.jsonl.

"""2-approximate vertex cover in the LOCAL model: the ends of a maximal matching.

matching_cover computes a maximal matching by Luby's algorithm on the line
graph (three rounds per phase, as on the distributed maximal matching page)
and returns its matched nodes, which every node knows after the last round.
min_vertex_cover_size is an exact brute force for small graphs, used to
check the ratio.

Precondition: adj is an undirected simple graph given by adjacency lists;
the brute force needs n <= 20.
Cost: O(log n) rounds with high probability; the brute force takes O(2^n n)
time.
"""

import random


def is_vertex_cover(adj: list[list[int]], cover: set[int]) -> bool:
    return all(v in cover or u in cover for v in range(len(adj)) for u in adj[v])


def matching_cover(adj: list[list[int]], rng: random.Random) -> tuple[set[int], int, int]:
    """Return (cover, matching size, rounds)."""
    n = len(adj)
    mate = [-1] * n
    rounds = 0
    while True:
        live = [(u, v) for u in range(n) if mate[u] < 0 for v in adj[u] if u < v and mate[v] < 0]
        if not live:
            break
        prio = {e: (rng.random(), e) for e in live}  # round 1
        least: dict[int, tuple[float, tuple[int, int]]] = {}
        for e, p in prio.items():  # round 2
            for x in e:
                if x not in least or p < least[x]:
                    least[x] = p
        for (u, v), p in prio.items():  # round 3: matched nodes announce
            if least[u] == p and least[v] == p:
                mate[u], mate[v] = v, u
        rounds += 3
    cover = {v for v in range(n) if mate[v] >= 0}
    return cover, len(cover) // 2, rounds


def min_vertex_cover_size(adj: list[list[int]]) -> int:
    """Exact minimum vertex cover size by trying all subsets (n <= 20)."""
    n = len(adj)
    assert n <= 20
    edges = [(u, v) for u in range(n) for v in adj[u] if u < v]
    best = n
    for mask in range(1 << n):
        size = bin(mask).count("1")
        if size < best and all((mask >> u) & 1 or (mask >> v) & 1 for u, v in edges):
            best = size
    return best
