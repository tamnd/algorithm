# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/metric-tsp-inapproximability/. The authors are listed in prov/XPTJYD.jsonl.
"""The (1,2)-TSP instance of a graph, and the identity OPT = n + pi(G) for non-Hamiltonian G.

A graph is (n, edges) with vertices 0 .. n-1. pi(G) is the least number of vertex-disjoint paths
that cover all vertices. For small instances only: the solvers use dynamic programs over subsets.
"""

from fractions import Fraction


def one_two_instance(n: int, edges: list[tuple[int, int]]) -> list[list[int]]:
    """Cost 1 for an edge of the graph and cost 2 for every other pair."""
    c = [[2] * n for _ in range(n)]
    for u, v in edges:
        c[u][v] = c[v][u] = 1
    for v in range(n):
        c[v][v] = 0
    return c


def tsp_opt(c: list[list[int]]) -> int:
    """Held and Karp dynamic program: the least cost of a tour through all n >= 2 cities."""
    n = len(c)
    full = (1 << n) - 1
    inf = float("inf")
    best = [[inf] * n for _ in range(1 << n)]
    best[1][0] = 0
    for s in range(1, 1 << n, 2):
        for v in range(n):
            if best[s][v] == inf:
                continue
            for w in range(n):
                if not s >> w & 1:
                    t = s | 1 << w
                    if best[s][v] + c[v][w] < best[t][w]:
                        best[t][w] = best[s][v] + c[v][w]
    return min(best[full][v] + c[v][0] for v in range(1, n))


def _path_sets(n: int, edges: list[tuple[int, int]]) -> list[bool]:
    """ok[s] is True if the graph has a path whose vertex set is exactly s."""
    adj = [0] * n
    for u, v in edges:
        adj[u] |= 1 << v
        adj[v] |= 1 << u
    end = [0] * (1 << n)
    for v in range(n):
        end[1 << v] = 1 << v
    for s in range(1, 1 << n):
        for v in range(n):
            if end[s] >> v & 1:
                nxt = adj[v] & ~s
                while nxt:
                    w = (nxt & -nxt).bit_length() - 1
                    end[s | 1 << w] |= 1 << w
                    nxt &= nxt - 1
    return [e != 0 for e in end]


def path_cover_number(n: int, edges: list[tuple[int, int]]) -> int:
    """The least number of vertex-disjoint paths that cover all n vertices."""
    ok = _path_sets(n, edges)
    full = (1 << n) - 1
    need = [0] + [n + 1] * full
    for s in range(1, full + 1):
        low = s & -s
        sub = s
        while sub:
            if sub & low and ok[sub]:
                need[s] = min(need[s], need[s ^ sub] + 1)
            sub = (sub - 1) & s
    return need[full]


def is_hamiltonian(n: int, edges: list[tuple[int, int]]) -> bool:
    return n >= 3 and tsp_opt(one_two_instance(n, edges)) == n


def tour_cost(c: list[list[int]], tour: list[int]) -> int:
    return sum(c[tour[i]][tour[(i + 1) % len(tour)]] for i in range(len(tour)))


def tour_to_paths(c: list[list[int]], tour: list[int]) -> list[list[int]]:
    """Cut the tour at its cost-2 edges. With j >= 1 such edges this gives j paths of the graph."""
    n = len(tour)
    cuts = [i for i in range(n) if c[tour[i]][tour[(i + 1) % n]] == 2]
    if not cuts:
        return [tour[:]]
    start = (cuts[0] + 1) % n
    seq = tour[start:] + tour[:start]
    paths, cur = [], [seq[0]]
    for a, b in zip(seq, seq[1:]):
        if c[a][b] == 2:
            paths.append(cur)
            cur = [b]
        else:
            cur.append(b)
    paths.append(cur)
    return paths


def paths_to_tour(paths: list[list[int]]) -> list[int]:
    """Join the paths end to start in the given order."""
    return [v for p in paths for v in p]


def gap_ratio(a: Fraction, b: Fraction) -> Fraction:
    """If pi <= a n against pi >= b n is NP-hard, no ratio below (1 + b) / (1 + a) is possible."""
    return (1 + b) / (1 + a)
