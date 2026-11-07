# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cuthill-mckee/. The authors are listed in prov/9BQFTQ.jsonl.

"""The Cuthill-McKee ordering of a sparse symmetric pattern.

The pattern is given as adjacency lists adj[v] (neighbours of v, no self
loops), built from a dense matrix or from CSR arrays by the helpers below.
The result is a list order with order[k] = the old index of the vertex that
gets the new number k. Standard library only.
"""

from collections import deque


def graph_from_dense(a):
    """Adjacency lists of the symmetrized off-diagonal pattern of a."""
    n = len(a)
    nb = [set() for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j and (a[i][j] != 0 or a[j][i] != 0):
                nb[i].add(j)
    return [sorted(s) for s in nb]


def graph_from_csr(n, ptr, ind):
    """Adjacency lists from CSR row pointers and column indices."""
    nb = [set() for _ in range(n)]
    for i in range(n):
        for p in range(ptr[i], ptr[i + 1]):
            j = ind[p]
            if j != i:
                nb[i].add(j)
                nb[j].add(i)
    return [sorted(s) for s in nb]


def levels(adj, root):
    """Breadth-first level structure from root, as a list of levels."""
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


def pseudo_peripheral(adj, start):
    """George and Liu (1979): move to a min-degree vertex of the last level
    while the eccentricity grows."""
    r = start
    ls = levels(adj, r)
    while True:
        x = min(ls[-1], key=lambda v: (len(adj[v]), v))
        lx = levels(adj, x)
        if len(lx) <= len(ls):
            return r
        r, ls = x, lx


def cuthill_mckee(adj, start=None, peripheral=True):
    """Return the Cuthill-McKee order of all vertices.

    start: root for the component of start (default: a vertex of minimum
    degree). peripheral: replace each root by a pseudo-peripheral vertex.
    Components are processed in order of their minimum degree vertex.
    """
    n = len(adj)
    deg = [len(adj[v]) for v in range(n)]
    seen = [False] * n  # @line L1
    order = []
    cand = sorted(range(n), key=lambda v: (deg[v], v))
    if start is not None:
        cand = [start] + [v for v in cand if v != start]
    for s in cand:  # @line L2
        if seen[s]:
            continue
        r = pseudo_peripheral(adj, s) if peripheral else s  # @line L3
        seen[r] = True  # @line L4
        order.append(r)
        head = len(order) - 1  # @line L5
        while head < len(order):  # @line L6
            v = order[head]  # @line L7
            head += 1
            new = [w for w in adj[v] if not seen[w]]
            new.sort(key=lambda w: (deg[w], w))  # @line L8
            for w in new:
                seen[w] = True  # @line L9
                order.append(w)
    return order  # @line L10


def reverse_cuthill_mckee(adj, **kw):
    """George (1971): the Cuthill-McKee order reversed."""
    return cuthill_mckee(adj, **kw)[::-1]


def bandwidth(adj, order):
    """max |f(i) - f(j)| over edges, with f the new numbers."""
    f = {v: k for k, v in enumerate(order)}
    return max((abs(f[v] - f[w]) for v in range(len(adj)) for w in adj[v]), default=0)


def profile(adj, order):
    """Envelope size: sum over rows of (row index - first column index) in
    the lower triangle of the permuted matrix."""
    f = {v: k for k, v in enumerate(order)}
    tot = 0
    for v in range(len(adj)):
        i = f[v]
        first = min([f[w] for w in adj[v]] + [i])
        tot += i - first
    return tot


def permute(a, order):
    """The dense matrix P A P^T with (P A P^T)[k][l] = a[order[k]][order[l]]."""
    return [[a[i][j] for j in order] for i in order]
