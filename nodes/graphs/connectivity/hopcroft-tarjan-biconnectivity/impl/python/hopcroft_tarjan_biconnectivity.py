# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hopcroft-tarjan-biconnectivity/. The authors are listed in prov/B1ZMBY.jsonl.


def biconnectivity(
    n: int, edges: list[tuple[int, int]]
) -> tuple[list[int], list[int], list[list[int]]]:
    """Find the articulation points, the bridges and the blocks of an undirected graph.

    Precondition: the vertices are 0 .. n-1 and edges[i] = (u, v) is the edge with id i.
    Parallel edges and loops are allowed, and the graph need not be connected.
    Returns (aps, bridges, blocks): the sorted articulation points, the sorted ids of
    the bridges, and the blocks as sorted lists of edge ids, in the order of output
    (loops first, then the order in which the search closes the blocks).
    Time O(n + m), extra space O(n + m). The depth-first search uses an explicit stack
    of (vertex, id of the tree edge into it, next index) frames, not recursion.
    """
    adj: list[list[tuple[int, int]]] = [[] for _ in range(n)]
    blocks: list[list[int]] = []
    for i, (u, v) in enumerate(edges):
        if u == v:
            blocks.append([i])  # @line L2
        else:
            adj[u].append((v, i))
            adj[v].append((u, i))
    d = [0] * n  # @line L1
    low = [0] * n
    t = 0
    estack: list[int] = []
    is_ap = [False] * n
    bridges: list[int] = []
    for r in range(n):  # @line L3
        if d[r]:
            continue
        children = 0
        t += 1  # @line L5: VISIT(r, nil) starts
        d[r] = low[r] = t
        frames = [(r, -1, 0)]
        while frames:
            u, p, k = frames[-1]
            if k < len(adj[u]):  # @line L6
                frames[-1] = (u, p, k + 1)
                v, e = adj[u][k]
                if e == p:  # the tree edge into u, by id
                    continue
                if d[v] == 0:  # @line L7
                    estack.append(e)  # @line L8
                    if u == r:
                        children += 1
                    t += 1  # @line L5: VISIT(v, e) starts
                    d[v] = low[v] = t
                    frames.append((v, e, 0))
                elif d[v] < d[u]:  # @line L14
                    estack.append(e)  # @line L15
                    low[u] = min(low[u], d[v])
                continue
            frames.pop()  # VISIT(u, p) returns to its caller
            if not frames:
                break
            w = frames[-1][0]  # the parent of u; p is the tree edge {w, u}
            low[w] = min(low[w], low[u])  # @line L9
            if low[u] >= d[w]:  # @line L10
                block = []  # @line L11
                while True:
                    x = estack.pop()
                    block.append(x)
                    if x == p:
                        break
                blocks.append(sorted(block))
                if w != r:  # @line L12
                    is_ap[w] = True
                if low[u] > d[w]:  # @line L13
                    bridges.append(p)
        if children >= 2:  # @line L4
            is_ap[r] = True
    aps = [v for v in range(n) if is_ap[v]]
    return aps, sorted(bridges), blocks
