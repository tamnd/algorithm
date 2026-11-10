# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bottleneck-tsp-approximation/. The authors are listed in prov/PT0SHC.jsonl.

from typing import Sequence


def threshold_graph(cost: Sequence[Sequence[float]], t: float) -> list[list[int]]:
    """Adjacency lists of G_t: the pairs u != v with cost at most t."""
    n = len(cost)
    return [[v for v in range(n) if v != u and cost[u][v] <= t] for u in range(n)]


def is_connected_without(adj: list[list[int]], removed: int) -> bool:
    """True if the graph minus the vertex `removed` (or minus nothing, for -1) is connected."""
    n = len(adj)
    start = 0 if removed != 0 else 1
    seen = [False] * n
    if removed >= 0:
        seen[removed] = True
    seen[start] = True
    stack = [start]
    count = 1
    while stack:
        u = stack.pop()
        for v in adj[u]:
            if not seen[v]:
                seen[v] = True
                count += 1
                stack.append(v)
    return count == n - (1 if removed >= 0 else 0)


def is_biconnected(adj: list[list[int]]) -> bool:
    """For n >= 3: connected, and connected after the removal of any one vertex. Time O(n^3)."""
    n = len(adj)
    return is_connected_without(adj, -1) and all(is_connected_without(adj, v) for v in range(n))


def square(adj: list[list[int]]) -> list[list[int]]:
    """The square of the graph: u and v are adjacent when their distance is 1 or 2."""
    n = len(adj)
    out = []
    for u in range(n):
        near = set(adj[u])
        for w in adj[u]:
            near.update(adj[w])
        near.discard(u)
        out.append(sorted(near))
    return out


def hamiltonian_cycle(adj: list[list[int]]) -> list[int] | None:
    """A Hamiltonian cycle that starts at 0, by a dynamic program over subsets.

    Time O(2^n n^2) and space O(2^n n): for small n only. For the square of a biconnected graph,
    the algorithms of Lau and of Alstrup et al. find such a cycle in polynomial time.
    """
    n = len(adj)
    full = (1 << n) - 1
    # pred[mask][v] = the vertex before v on a path from 0 through mask that ends at v, or -1.
    pred = [[-2] * n for _ in range(1 << n)]
    pred[1][0] = -1
    for mask in range(1, 1 << n, 2):
        row = pred[mask]
        for v in range(n):
            if row[v] == -2:
                continue
            for w in adj[v]:
                if not mask >> w & 1 and pred[mask | 1 << w][w] == -2:
                    pred[mask | 1 << w][w] = v
    for last in range(1, n):
        if pred[full][last] != -2 and 0 in adj[last]:
            cycle, mask, v = [], full, last
            while v != -1:
                cycle.append(v)
                u = pred[mask][v]
                mask &= ~(1 << v)
                v = u
            cycle.reverse()
            return cycle
    return None


def bottleneck(cost: Sequence[Sequence[float]], tour: list[int]) -> float:
    """The largest cost of an edge of the closed tour."""
    k = len(tour)
    return max((cost[tour[i]][tour[(i + 1) % k]] for i in range(k)), default=0) if k > 1 else 0


def bottleneck_tsp_2approx(cost: Sequence[Sequence[float]]) -> tuple[list[int], float]:
    """Return (tour, t): a tour whose largest edge costs at most 2 t, where t <= OPT.

    Precondition: cost is a symmetric n x n matrix of non-negative numbers with the triangle
    inequality. The threshold search takes O(n^3 log n) time; the Hamiltonian cycle step here is
    exact but exponential, O(2^n n^2), so this code is for small n.
    """
    n = len(cost)
    if n <= 2:
        return list(range(n)), bottleneck(cost, list(range(n)))
    values = sorted({cost[u][v] for u in range(n) for v in range(u + 1, n)})  # @line L1
    lo, hi = 0, len(values) - 1  # @line L2
    while lo < hi:  # @line L3
        mid = (lo + hi) // 2
        if is_biconnected(threshold_graph(cost, values[mid])):  # @line L4
            hi = mid
        else:
            lo = mid + 1
    t = values[lo]  # @line L5
    s = square(threshold_graph(cost, t))  # @line L6
    tour = hamiltonian_cycle(s)  # @line L7
    if tour is None:
        raise AssertionError("Fleischner's theorem says this cannot happen")
    return tour, t  # @line L8
