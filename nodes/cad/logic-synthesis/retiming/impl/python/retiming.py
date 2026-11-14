# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/retiming/. The authors are listed in prov/9JAVQE.jsonl.

"""Leiserson-Saxe retiming for the least clock period.

A circuit is a graph with vertices 0 .. n-1. Vertex v is a gate with an
integer delay d[v] >= 0. An edge (u, v, w) is a wire from u to v that
passes through w >= 0 registers. Vertex 0 is the host: it stands for the
outside world, has delay 0 and keeps r(0) = 0. Every cycle must hold at
least one register.

A retiming is an integer map r. The retimed edge weight is
w_r(e) = w(e) + r(v) - r(u). The retiming is legal when every w_r(e) >= 0.
"""

from typing import Optional

Edge = tuple[int, int, int]


def retimed(edges: list[Edge], r: list[int]) -> list[Edge]:
    """The edges after the retiming r."""
    return [(u, v, w + r[v] - r[u]) for (u, v, w) in edges]


def is_legal(edges: list[Edge], r: list[int]) -> bool:
    return all(w + r[v] - r[u] >= 0 for (u, v, w) in edges)


def clock_period(n: int, d: list[int], edges: list[Edge]) -> int:
    """The largest delay of a path with no register, the period of the circuit.

    Raises ValueError if some cycle has no register."""
    succ: list[list[int]] = [[] for _ in range(n)]
    indeg = [0] * n
    for (u, v, w) in edges:
        if w == 0:
            succ[u].append(v)
            indeg[v] += 1
    arrive = list(d)  # arrive[v]: the largest delay of a zero-register path ending at v
    queue = [v for v in range(n) if indeg[v] == 0]
    seen = 0
    while queue:
        u = queue.pop()
        seen += 1
        for v in succ[u]:
            arrive[v] = max(arrive[v], arrive[u] + d[v])
            indeg[v] -= 1
            if indeg[v] == 0:
                queue.append(v)
    if seen < n:
        raise ValueError("a cycle has no register")
    return max(arrive) if n else 0


def wd_matrices(n: int, d: list[int], edges: list[Edge]) -> tuple[list[list[Optional[int]]], list[list[Optional[int]]]]:
    """W[u][v] is the fewest registers on a path from u to v. D[u][v] is the
    largest delay of such a path, counting d[u] and d[v]. None if v is not
    reachable from u.

    Floyd-Warshall on the pairs (w(e), -d(u)), compared in lexicographic
    order. The empty path gives W[v][v] = 0 and D[v][v] = d[v]."""
    inf = None
    best: list[list[Optional[tuple[int, int]]]] = [[inf] * n for _ in range(n)]  # @line L1
    for v in range(n):
        best[v][v] = (0, 0)
    for (u, v, w) in edges:
        cand = (w, -d[u])
        if u != v and (best[u][v] is None or cand < best[u][v]):
            best[u][v] = cand
    for k in range(n):
        bk = best[k]
        for i in range(n):
            bik = best[i][k]
            if bik is None:
                continue
            bi = best[i]
            for j in range(n):
                bkj = bk[j]
                if bkj is None:
                    continue
                cand = (bik[0] + bkj[0], bik[1] + bkj[1])
                if bi[j] is None or cand < bi[j]:
                    bi[j] = cand
    W: list[list[Optional[int]]] = [[None] * n for _ in range(n)]  # @line L2
    D: list[list[Optional[int]]] = [[None] * n for _ in range(n)]
    for u in range(n):
        for v in range(n):
            if best[u][v] is not None:
                W[u][v] = best[u][v][0]
                D[u][v] = d[v] - best[u][v][1]
    return W, D


def solve_difference_constraints(n: int, cons: list[tuple[int, int, int]]) -> Optional[list[int]]:
    """Bellman-Ford for r(u) - r(v) <= b, each given as (u, v, b).

    Returns an integer solution with r[0] = 0, or None if a negative cycle
    makes the system infeasible."""
    dist = [0] * n  # a virtual source with an edge of weight 0 to each vertex
    for _ in range(n):
        changed = False
        for (u, v, b) in cons:  # the constraint is the edge v -> u of weight b
            if dist[v] + b < dist[u]:
                dist[u] = dist[v] + b
                changed = True
        if not changed:
            return [x - dist[0] for x in dist]
    return None


def period_constraints(n: int, edges: list[Edge], W, D, c: int) -> list[tuple[int, int, int]]:
    """The constraints of Leiserson and Saxe for a period of at most c."""
    cons = [(u, v, w) for (u, v, w) in edges]  # @line L7
    for u in range(n):
        for v in range(n):
            if D[u][v] is not None and D[u][v] > c:
                cons.append((u, v, W[u][v] - 1))  # @line L8
    return cons


def min_period_retiming(n: int, d: list[int], edges: list[Edge]) -> tuple[int, list[int]]:
    """OPT1: the least clock period over all legal retimings, and a retiming
    that reaches it. Binary search over the sorted values of D, with one
    Bellman-Ford test per probe."""
    clock_period(n, d, edges)  # checks that every cycle has a register
    W, D = wd_matrices(n, d, edges)
    values = sorted({D[u][v] for u in range(n) for v in range(n) if D[u][v] is not None})  # @line L3
    lo, hi = 0, len(values) - 1  # @line L4: the largest value is met by r = 0
    best = [0] * n
    while lo < hi:  # @line L5
        mid = (lo + hi) // 2  # @line L6
        r = solve_difference_constraints(n, period_constraints(n, edges, W, D, values[mid]))  # @line L9
        if r is None:
            lo = mid + 1  # @line L10
        else:
            hi, best = mid, r  # @line L11
    return values[lo], best  # @line L12


def feas(n: int, d: list[int], edges: list[Edge], c: int) -> Optional[list[int]]:
    """FEAS: a legal retiming with period at most c, or None.

    Repeat n - 1 times: compute the arrival time of each vertex in the
    retimed circuit, and add 1 to r(v) for each v whose arrival time is more
    than c. If the result still has a period above c, no legal retiming
    reaches c, and the function returns None."""
    r = [0] * n
    for _ in range(n - 1):
        arrive = _arrivals(n, d, retimed(edges, r))
        for v in range(n):
            if arrive[v] > c:
                r[v] += 1
    shifted = [x - r[0] for x in r]
    er = retimed(edges, shifted)
    if all(w >= 0 for (_, _, w) in er) and clock_period(n, d, er) <= c:
        return shifted
    return None


def _arrivals(n: int, d: list[int], edges: list[Edge]) -> list[int]:
    succ: list[list[int]] = [[] for _ in range(n)]
    indeg = [0] * n
    for (u, v, w) in edges:
        if w == 0:
            succ[u].append(v)
            indeg[v] += 1
    arrive = list(d)
    queue = [v for v in range(n) if indeg[v] == 0]
    while queue:
        u = queue.pop()
        for v in succ[u]:
            arrive[v] = max(arrive[v], arrive[u] + d[v])
            indeg[v] -= 1
            if indeg[v] == 0:
                queue.append(v)
    return arrive
