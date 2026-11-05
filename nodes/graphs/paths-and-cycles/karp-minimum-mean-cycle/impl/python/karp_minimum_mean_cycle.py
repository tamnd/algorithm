# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/karp-minimum-mean-cycle/. The authors are listed in prov/CDP661.jsonl.

from fractions import Fraction


def karp_minimum_mean_cycle(
    n: int, arcs: list[tuple[int, int, int | Fraction]]
) -> tuple[Fraction, list[int]] | None:
    """Return (the minimum cycle mean, a cycle with that mean), or None if acyclic.

    The directed graph has the vertices 0 .. n-1 and the arcs arcs[i] = (u, v, w), from
    u to v with weight w (an int or a Fraction, of any sign); parallel arcs and
    self-loops are allowed. The cycle is the list of its arc numbers in order.
    D[k][v] is the least weight of a walk with exactly k arcs that ends at v and starts
    anywhere. Time O(n (n + m)), extra space O(n^2).
    """
    INF = None
    dist: list[list[int | Fraction | None]] = [[0] * n]  # @line L1
    par: list[list[int]] = [[-1] * n]
    for k in range(1, n + 1):  # @line L2
        cur: list[int | Fraction | None] = [INF] * n  # @line L3
        pk = [-1] * n
        prev = dist[k - 1]
        for a, (u, v, w) in enumerate(arcs):  # @line L4
            if prev[u] is not None:
                d = prev[u] + w
                if cur[v] is None or d < cur[v]:  # @line L5
                    cur[v] = d
                    pk[v] = a
        dist.append(cur)
        par.append(pk)
    best: Fraction | None = None  # @line L6
    best_v = -1
    for v in range(n):  # @line L7
        dn = dist[n][v]
        if dn is None:
            continue
        mu = max(  # @line L8
            Fraction(dn - dist[k][v], n - k) for k in range(n) if dist[k][v] is not None
        )
        if best is None or mu < best:  # @line L9
            best, best_v = mu, v
    if best is None:  # @line L10
        return None
    # L11: walk back from (n, best_v) and cut out the first repeated vertex
    seen: dict[int, int] = {}  # @line L11
    walk_arcs: list[int] = []
    v, k = best_v, n
    while v not in seen:
        seen[v] = len(walk_arcs)
        a = par[k][v]
        walk_arcs.append(a)
        v, k = arcs[a][0], k - 1
    cycle = walk_arcs[seen[v] :]  # arcs in reverse order, from the repeat back
    cycle.reverse()
    return best, cycle  # @line L12
