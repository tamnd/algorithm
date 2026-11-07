# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/reverse-cuthill-mckee/. The authors are listed in prov/36W80E.jsonl.

"""Reverse Cuthill-McKee ordering of a sparse symmetric matrix, with the
measures it is judged by: bandwidth, envelope, and the fill and flops of a
Cholesky factorization in the new order.

A graph is a list adj with adj[v] the list of neighbours of v (no self loops).
An ordering is a list order; vertex order[k] gets the new number k, and the
reordered matrix is P A P^T with (P A P^T)[k][l] = a[order[k]][order[l]].
"""

from collections import deque


def graph_from_dense(a) -> list[list[int]]:
    """Graph of the symmetric pattern of a (a_ij != 0 or a_ji != 0, i != j)."""
    n = len(a)
    return [[j for j in range(n) if j != i and (a[i][j] != 0 or a[j][i] != 0)] for i in range(n)]


def graph_from_edges(n: int, edges) -> list[list[int]]:
    adj = [set() for _ in range(n)]
    for v, w in edges:
        if v != w:
            adj[v].add(w)
            adj[w].add(v)
    return [sorted(s) for s in adj]


def _levels(adj, root):
    """Breadth-first level structure rooted at root."""
    seen = {root}
    out = [[root]]
    while True:
        nxt = []
        for v in out[-1]:
            for w in adj[v]:
                if w not in seen:
                    seen.add(w)
                    nxt.append(w)
        if not nxt:
            return out
        out.append(nxt)


def pseudo_peripheral(adj, start: int) -> int:
    """George and Liu (1979): move to a minimum-degree vertex of the last level
    while the eccentricity increases."""
    r, ls = start, _levels(adj, start)
    while True:
        x = min(ls[-1], key=lambda v: (len(adj[v]), v))
        lx = _levels(adj, x)
        if len(lx) <= len(ls):
            return r
        r, ls = x, lx


def reverse_cuthill_mckee(adj) -> list[int]:
    """The reverse Cuthill-McKee order of all vertices, component by component."""
    n = len(adj)
    deg = [len(nb) for nb in adj]
    numbered = [False] * n
    order: list[int] = []  # @line L1
    for s in sorted(range(n), key=lambda v: (deg[v], v)):  # @line L2
        if numbered[s]:  # @line L3
            continue
        r = pseudo_peripheral(adj, s)  # @line L4
        numbered[r] = True  # @line L5
        order.append(r)
        q = deque([r])
        while q:  # @line L6
            v = q.popleft()
            new = sorted((w for w in adj[v] if not numbered[w]), key=lambda w: (deg[w], w))  # @line L7
            for w in new:  # @line L8
                numbered[w] = True
                order.append(w)
                q.append(w)
    order.reverse()  # @line L9
    return order  # @line L10


def cuthill_mckee(adj) -> list[int]:
    """The Cuthill-McKee order, the reverse of reverse_cuthill_mckee."""
    return reverse_cuthill_mckee(adj)[::-1]


def _numbers(order):
    f = [0] * len(order)
    for k, v in enumerate(order):
        f[v] = k
    return f


def bandwidth(adj, order) -> int:
    f = _numbers(order)
    return max((abs(f[v] - f[w]) for v in range(len(adj)) for w in adj[v]), default=0)


def envelope(adj, order) -> int:
    """Number of entries strictly left of the diagonal and right of the first
    nonzero in each row of the lower triangle of P A P^T."""
    f = _numbers(order)
    return sum(f[v] - min([f[w] for w in adj[v]] + [f[v]]) for v in range(len(adj)))


def cholesky_pattern(adj, order) -> list[set[int]]:
    """Exact symbolic Cholesky: cols[k] = rows i > k with l_ik != 0 (new numbers),
    by eliminating vertices in order and joining their later neighbours into a clique."""
    f = _numbers(order)
    n = len(adj)
    later = [set(f[w] for w in adj[v]) for v in order]  # by new number
    cols = []
    for k in range(n):
        s = {i for i in later[k] if i > k}
        cols.append(s)
        for i in s:
            later[i] |= s - {i}
    return cols


def fill_and_flops(adj, order) -> tuple[int, int]:
    """(nnz of L below the diagonal, Cholesky flops sum_k c_k^2 + O(n)) for the order."""
    cols = cholesky_pattern(adj, order)
    nnz = sum(len(c) for c in cols)
    return nnz, sum(len(c) ** 2 for c in cols)


def permute(a, order):
    return [[a[i][j] for j in order] for i in order]
