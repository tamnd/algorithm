# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kosaraju-sharir/. The authors are listed in prov/TA3TXZ.jsonl.


def kosaraju_sharir(adj: list[list[int]]) -> list[int]:
    """Return comp, where comp[v] is the number of the strongly connected component of v.

    The graph is directed, with vertices 0 .. n-1 and adjacency lists adj. Parallel
    arcs (repeated entries) and self-loops (v in adj[v]) are allowed. The components
    are numbered 0, 1, ... in the order the second pass finds them, which is a
    topological order of the condensation: for each arc (u, v), comp[u] <= comp[v].
    Both passes use explicit stacks, so long paths do not overflow the Python stack.
    Time O(n + m), extra space O(n + m) for the transpose.
    """
    n = len(adj)
    # L1: a DFS of G that lists the vertices in order of finish time.
    order: list[int] = []
    seen = [False] * n
    for root in range(n):  # @line L1
        if seen[root]:
            continue
        seen[root] = True
        stack = [(root, 0)]
        while stack:
            u, i = stack[-1]
            if i < len(adj[u]):
                stack[-1] = (u, i + 1)
                v = adj[u][i]
                if not seen[v]:
                    seen[v] = True
                    stack.append((v, 0))
            else:
                stack.pop()
                order.append(u)  # u finishes
    adj_t: list[list[int]] = [[] for _ in range(n)]  # @line L2
    for u in range(n):
        for v in adj[u]:
            adj_t[v].append(u)
    comp: list[int] = [-1] * n  # @line L3
    k = -1
    for u in reversed(order):  # @line L4
        if comp[u] != -1:  # @line L5
            continue
        k += 1  # @line L6
        # L7: ASSIGN(G^T, u, k), with an explicit stack.
        todo = [u]  # @line L7
        comp[u] = k  # @line L9
        while todo:
            x = todo.pop()
            for y in adj_t[x]:  # @line L10
                if comp[y] == -1:  # @line L11
                    comp[y] = k
                    todo.append(y)
    return comp  # @line L8
