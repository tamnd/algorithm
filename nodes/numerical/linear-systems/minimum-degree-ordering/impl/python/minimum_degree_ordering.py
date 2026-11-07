# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/minimum-degree-ordering/. The authors are listed in prov/3FDE64.jsonl.

"""Minimum degree ordering of a sparse symmetric matrix.

A graph is a list adj with adj[v] the neighbours of v (no self loops), the
pattern of a symmetric matrix A. An ordering is a list order; vertex order[k]
is eliminated k-th, so P A P^T has (P A P^T)[k][l] = a[order[k]][order[l]].

minimum_degree works on the elimination graph (explicit fill edges).
minimum_degree_quotient works on the quotient graph of George and Liu, whose
storage never exceeds that of the original graph, with exact degrees or with
the approximate degree of Amestoy, Davis and Duff (AMD).
Ties are broken by the smallest vertex index, so all results are reproducible.
"""

import heapq


def graph_from_edges(n: int, edges) -> list[list[int]]:
    adj = [set() for _ in range(n)]
    for v, w in edges:
        if v != w:
            adj[v].add(w)
            adj[w].add(v)
    return [sorted(s) for s in adj]


def graph_from_dense(a) -> list[list[int]]:
    n = len(a)
    return [[j for j in range(n) if j != i and (a[i][j] != 0 or a[j][i] != 0)] for i in range(n)]


def minimum_degree(adj) -> list[int]:
    """Minimum degree on the elimination graph; ties by smallest index."""
    n = len(adj)
    g = [set(nb) for nb in adj]  # @line L1
    alive = [True] * n
    heap = [(len(g[v]), v) for v in range(n)]
    heapq.heapify(heap)
    order: list[int] = []
    while len(order) < n:  # @line L2
        d, v = heapq.heappop(heap)  # @line L3
        if not alive[v] or d != len(g[v]):
            continue  # stale heap entry
        order.append(v)  # @line L4
        alive[v] = False
        nb = g[v]  # @line L5
        for w in nb:  # @line L6
            g[w].discard(v)
            g[w] |= nb - {w}
        g[v] = set()
        for w in nb:  # @line L7
            heapq.heappush(heap, (len(g[w]), w))
    return order  # @line L8


def minimum_degree_quotient(adj, degree: str = "exact", stats=None) -> list[int]:
    """Minimum degree on the quotient graph.

    Variables i keep A[i] (variable neighbours) and E[i] (adjacent elements);
    an eliminated vertex p becomes an element with variable list L[p].
    degree = "exact" uses |reach(i)|; degree = "approximate" uses the AMD bound.
    If stats is a dict, stats["storage"] gets the largest value of
    sum |A_i| + sum |L_e| over the run, stats["checks"] a list of
    (approximate, exact, number of elements of i) for every degree update.
    """
    n = len(adj)
    a = [set(nb) for nb in adj]
    e = [set() for _ in range(n)]
    elems: dict[int, set[int]] = {}
    alive = [True] * n
    deg = [len(nb) for nb in adj]
    heap = [(deg[v], v) for v in range(n)]
    heapq.heapify(heap)
    order: list[int] = []
    storage = sum(deg)
    while len(order) < n:
        d, p = heapq.heappop(heap)
        if not alive[p] or d != deg[p]:
            continue
        order.append(p)
        alive[p] = False
        lp = set(a[p])
        for el in e[p]:
            lp |= elems.pop(el)  # absorb the elements adjacent to p
        lp.discard(p)
        absorbed = e[p]
        elems[p] = lp
        a[p] = set()
        e[p] = set()
        remaining = n - len(order)
        for i in lp:
            e[i] -= absorbed
            e[i].add(p)
            a[i] -= lp
            a[i].discard(p)
        for i in lp:
            reach = set(a[i])
            for el in e[i]:
                reach |= elems[el]
            reach.discard(i)
            exact = len(reach)
            if degree == "exact":
                deg[i] = exact
            else:
                ext = sum(len(elems[el] - lp) for el in e[i] if el != p)
                deg[i] = min(remaining - 1, deg[i] + len(lp) - 1, len(a[i]) + len(lp) - 1 + ext)
                if stats is not None:
                    stats.setdefault("checks", []).append((deg[i], exact, len(e[i])))
            heapq.heappush(heap, (deg[i], i))
        size = sum(len(a[v]) for v in range(n) if alive[v]) + sum(len(s) for s in elems.values())
        storage = max(storage, size)
    if stats is not None:
        stats["storage"] = storage
    return order


def _numbers(order):
    f = [0] * len(order)
    for k, v in enumerate(order):
        f[v] = k
    return f


def cholesky_pattern(adj, order) -> list[set[int]]:
    """Exact symbolic Cholesky: cols[k] = rows i > k with l_ik != 0 (new numbers)."""
    f = _numbers(order)
    n = len(adj)
    later = [set(f[w] for w in adj[v]) for v in order]
    cols = []
    for k in range(n):
        s = {i for i in later[k] if i > k}
        cols.append(s)
        for i in s:
            later[i] |= s - {i}
    return cols


def fill_and_flops(adj, order) -> tuple[int, int]:
    """(nonzeros of L below the diagonal, sum_k c_k^2) for the ordering."""
    cols = cholesky_pattern(adj, order)
    return sum(len(c) for c in cols), sum(len(c) ** 2 for c in cols)


def fill_edges(adj, order) -> int:
    """Number of fill entries: nonzeros of L below the diagonal minus edges of G."""
    return fill_and_flops(adj, order)[0] - sum(len(nb) for nb in adj) // 2


def ldlt_pattern_exact(a, order):
    """Exact LDL^T of P A P^T with Fractions; returns the set of (i, k), i > k, with l_ik != 0."""
    from fractions import Fraction
    n = len(a)
    b = [[Fraction(a[i][j]) for j in order] for i in order]
    nz = set()
    for k in range(n):
        piv = b[k][k]
        for i in range(k + 1, n):
            if b[i][k] != 0:
                nz.add((i, k))
                m = b[i][k] / piv
                for j in range(k + 1, i + 1):
                    if b[k][j] != 0:
                        b[i][j] -= m * b[k][j]
                        b[j][i] = b[i][j]
    return nz
