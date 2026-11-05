# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/batagelj-zaversnik-algorithm/. The authors are listed in prov/HTAYEM.jsonl.


def batagelj_zaversnik_algorithm(adj: list[list[int]]) -> list[int]:
    """Return the core number of each vertex of a simple undirected graph.

    The vertices are 0 .. n-1 and adj[v] lists the neighbours of v; each edge
    {u, v} is in both lists, with no self-loops and no repeated edges. The core
    number of v is the largest k such that v lies in a subgraph in which every
    vertex has degree at least k. Vertices are kept in an array sorted by their
    current degree, with one bucket per degree, so the time is O(n + m) and the
    extra space is O(n).
    """
    n = len(adj)
    deg = [len(adj[v]) for v in range(n)]  # @line L1
    md = max(deg, default=0)  # @line L2
    bucket = [0] * (md + 1)  # @line L3: bucket[d] counts the vertices of degree d
    for v in range(n):
        bucket[deg[v]] += 1
    start = 0  # @line L4: bucket[d] becomes the first index of degree d
    for d in range(md + 1):
        num = bucket[d]
        bucket[d] = start
        start += num
    pos = [0] * n  # @line L5: place the vertices in vert, sorted by degree
    vert = [0] * n
    for v in range(n):
        pos[v] = bucket[deg[v]]
        vert[pos[v]] = v
        bucket[deg[v]] += 1
    for d in range(md, 0, -1):  # @line L6: restore the bucket starts
        bucket[d] = bucket[d - 1]
    bucket[0] = 0
    for i in range(n):  # @line L7
        v = vert[i]  # @line L8: v has the least current degree among vert[i:]
        for u in adj[v]:  # @line L9
            if deg[u] > deg[v]:  # @line L10
                du = deg[u]  # @line L11: w is the first vertex of the bucket of u
                pu = pos[u]
                pw = bucket[du]
                w = vert[pw]
                if u != w:  # @line L12: swap u and w
                    pos[u] = pw
                    vert[pu] = w
                    pos[w] = pu
                    vert[pw] = u
                bucket[du] += 1  # @line L13: u moves to the bucket of degree du - 1
                deg[u] -= 1
    return deg  # @line L14
