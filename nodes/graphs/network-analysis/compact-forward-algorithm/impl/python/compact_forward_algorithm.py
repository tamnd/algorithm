# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/compact-forward-algorithm/. The authors are listed in prov/R006RZ.jsonl.


def compact_forward_algorithm(adj: list[list[int]]) -> list[tuple[int, int, int]]:
    """List every triangle of a simple undirected graph exactly once.

    The vertices are 0 .. n-1 and adj[v] lists the neighbours of v; each edge is
    in both lists, with no self-loops and no repeated edges. Each triangle is
    returned as (a, v, u) with eta(a) < eta(v) < eta(u), where eta numbers the
    vertices by non-increasing degree, ties by vertex number. The number of
    triangles is the length of the list. Time O(m^(3/2)) after the O(n + m)
    preparation, extra space O(n + m).
    """
    n = len(adj)
    order = sorted(range(n), key=lambda v: (-len(adj[v]), v))  # @line L1
    eta = [0] * n
    for rank, v in enumerate(order):
        eta[v] = rank
    nbr: list[list[int]] = [[] for _ in range(n)]  # @line L2: lists sorted by eta
    for w in order:
        for x in adj[w]:
            nbr[x].append(w)
    triangles: list[tuple[int, int, int]] = []  # @line L3
    for v in order:  # @line L4
        ev = eta[v]
        lv = nbr[v]
        for u in lv:  # @line L5
            if eta[u] <= ev:
                continue
            lu = nbr[u]
            i = 0  # @line L6
            j = 0
            while i < len(lv) and j < len(lu) and eta[lv[i]] < ev and eta[lu[j]] < ev:  # @line L7
                a = lv[i]  # @line L8
                b = lu[j]
                if eta[a] < eta[b]:  # @line L9
                    i += 1
                elif eta[a] > eta[b]:  # @line L10
                    j += 1
                else:  # @line L11
                    triangles.append((a, v, u))
                    i += 1
                    j += 1
    return triangles  # @line L12
