# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/five-color-algorithm/. The authors are listed in prov/AFEY7W.jsonl.

"""Five-color a simple planar graph with Kempe chain interchanges.

The graph is given by adjacency lists; no embedding is needed. The proof that
some Kempe interchange always works uses a plane embedding, but the algorithm
only tries all pairs of colors.
"""

from collections import deque


def five_color(adj: list[list[int]], stats: dict | None = None) -> list[int]:
    """Return colors 0 to 4, one for each vertex, with adjacent vertices colored differently.

    Precondition: adj describes a simple undirected graph (no loops, no parallel
    edges, u in adj[v] exactly when v in adj[u]). If the graph is planar, the
    call succeeds. If it is not planar, the call may raise ValueError.

    Cost: O(n + m) for the order, plus O(n + m) for each vertex that needs a
    Kempe interchange, so O(n^2) in the worst case for a planar graph.
    If stats is a dict, stats["swaps"] counts the interchanges.
    """
    n = len(adj)
    deg = [len(a) for a in adj]
    removed = [False] * n
    order: list[int] = []
    queue = [v for v in range(n) if deg[v] <= 5]  # @line L1
    while queue:  # @line L2
        v = queue.pop()
        removed[v] = True  # @line L3
        order.append(v)
        for u in adj[v]:  # @line L4
            if not removed[u]:
                deg[u] -= 1
                if deg[u] == 5:
                    queue.append(u)
    if len(order) < n:  # @line L5
        raise ValueError("not planar: every remaining vertex has degree at least 6")

    color = [-1] * n
    for v in reversed(order):  # @line L6
        owner = {}
        for u in adj[v]:  # @line L7
            if color[u] >= 0:
                owner[color[u]] = u
        if len(owner) < 5:  # @line L8
            color[v] = min(c for c in range(5) if c not in owner)
            continue
        done = False
        for i in range(5):  # @line L9
            for j in range(i + 1, 5):
                x, y = owner[i], owner[j]  # @line L10
                chain = {x}  # @line L11
                todo = deque([x])
                while todo:
                    w = todo.popleft()
                    for z in adj[w]:
                        if z not in chain and color[z] in (i, j):
                            chain.add(z)
                            todo.append(z)
                if y not in chain:  # @line L12
                    for w in chain:
                        color[w] = j if color[w] == i else i
                    color[v] = i
                    if stats is not None:
                        stats["swaps"] = stats.get("swaps", 0) + 1
                    done = True
                    break
            if done:
                break
        if not done:
            raise ValueError("not planar: no Kempe interchange frees a color")  # @line L13
    return color  # @line L14
