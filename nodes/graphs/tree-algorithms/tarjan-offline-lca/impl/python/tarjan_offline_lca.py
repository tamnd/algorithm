# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tarjan-offline-lca/. The authors are listed in prov/71EN86.jsonl.


def offline_lca(
    n: int,
    edges: list[tuple[int, int]],
    queries: list[tuple[int, int]],
    root: int = 0,
) -> list[int]:
    """Answer the LCA queries of a rooted tree offline, with Tarjan's method.

    The tree has the vertices 0 .. n-1, the n - 1 given edges, and the root
    `root`. It is not weighted. queries[i] = (u, v) asks for the lowest common
    ancestor of u and v; the result holds the answers in the same order.
    Time O((n + q) alpha(n)) with q = len(queries); no recursion.
    """
    adj: list[list[int]] = [[] for _ in range(n)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    uf = list(range(n))  # @line L1
    rank = [0] * n
    anc = list(range(n))
    done = [False] * n

    def find(x: int) -> int:
        r = x
        while uf[r] != r:
            r = uf[r]
        while uf[x] != r:  # path compression
            uf[x], x = r, uf[x]
        return r

    def union(x: int, y: int) -> None:
        x, y = find(x), find(y)
        if x == y:
            return
        if rank[x] < rank[y]:
            x, y = y, x
        uf[y] = x
        if rank[x] == rank[y]:
            rank[x] += 1

    qs: list[list[tuple[int, int]]] = [[] for _ in range(n)]
    for i, (u, v) in enumerate(queries):  # @line L2
        qs[u].append((v, i))
        qs[v].append((u, i))
    ans = [-1] * len(queries)
    nxt = [0] * n
    stack = [(root, -1)]  # @line L3
    while stack:  # @line L4
        v, p = stack[-1]  # @line L5
        a = adj[v]
        while nxt[v] < len(a) and a[nxt[v]] == p:
            nxt[v] += 1
        if nxt[v] < len(a):  # @line L6
            c = a[nxt[v]]
            nxt[v] += 1
            stack.append((c, v))
        else:  # @line L7
            stack.pop()  # @line L8
            done[v] = True
            for w, i in qs[v]:  # @line L9
                if done[w]:
                    ans[i] = anc[find(w)]
            if p != -1:  # @line L10
                union(p, v)
                anc[find(p)] = p
    return ans  # @line L11
