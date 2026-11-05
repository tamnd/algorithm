# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/nagamochi-ibaraki-certificate/. The authors are listed in prov/CXSCDF.jsonl.

"""Nagamochi-Ibaraki sparse certificate by one scan in maximum-label order.

The graph is undirected, on the vertices 0..n-1, given as a list of edges
(u, v). Parallel edges and self-loops are allowed. Each edge gets a label:
the index i >= 1 of the forest F_i that contains it, or 0 for a self-loop.
The certificate for k keeps the edges with label 1..k.
"""


def forest_labels(n: int, edges: list[tuple[int, int]]) -> list[int]:
    """Label every edge with the index of its forest, or 0 for a self-loop."""
    inc: list[list[tuple[int, int]]] = [[] for _ in range(n)]
    for e, (u, v) in enumerate(edges):
        if u != v:
            inc[u].append((v, e))
            inc[v].append((u, e))
    # Buckets of unscanned vertices by r, as doubly linked lists.
    r = [0] * n  # @line L1
    scanned = [False] * n
    head = [-1] * (len(edges) + 1)  # r[v] never exceeds the number of edges
    nxt = [-1] * n
    prv = [-1] * n

    def push(v: int) -> None:
        h = head[r[v]]
        nxt[v], prv[v] = h, -1
        if h != -1:
            prv[h] = v
        head[r[v]] = v

    def unlink(v: int) -> None:
        if prv[v] != -1:
            nxt[prv[v]] = nxt[v]
        else:
            head[r[v]] = nxt[v]
        if nxt[v] != -1:
            prv[nxt[v]] = prv[v]

    for v in range(n - 1, -1, -1):
        push(v)
    label = [0] * len(edges)  # @line L2
    top = 0
    for _ in range(n):  # @line L3
        while head[top] == -1:
            top -= 1
        x = head[top]  # @line L4
        unlink(x)
        scanned[x] = True  # @line L5
        for y, e in inc[x]:  # @line L6
            if not scanned[y]:
                unlink(y)
                r[y] += 1  # @line L7
                label[e] = r[y]  # @line L8
                push(y)  # @line L9
                if r[y] > top:
                    top = r[y]
    return label


def nagamochi_ibaraki_certificate(
    n: int, edges: list[tuple[int, int]], k: int
) -> list[int]:
    """Indices of the edges in F_1 + ... + F_k, in input order."""
    label = forest_labels(n, edges)
    return [e for e, i in enumerate(label) if 1 <= i <= k]  # @line L10
