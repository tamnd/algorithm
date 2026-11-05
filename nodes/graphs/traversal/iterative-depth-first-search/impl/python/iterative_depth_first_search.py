# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/iterative-depth-first-search/. The authors are listed in prov/FP6REQ.jsonl.

WHITE, GRAY, BLACK = 0, 1, 2


def iterative_depth_first_search(
    adj: list[list[int]],
) -> tuple[list[int], list[int], list[int | None]]:
    """Run a full depth-first search without recursion and return (d, f, parent).

    The graph has the vertices 0 .. n-1 and the adjacency lists adj (directed, or
    undirected with each edge in both lists). Roots are tried in the order 0 .. n-1 and
    each list is scanned in its given order, so the discovery times d, the finish times
    f (both in 1 .. 2n) and the parents are the same as those of the recursive DFS.
    Time O(n + m), extra space O(n).
    """
    n = len(adj)
    color = [WHITE] * n  # @line L1
    parent: list[int | None] = [None] * n
    nxt = [0] * n
    d = [0] * n
    f = [0] * n
    time = 0  # @line L2
    stack: list[int] = []
    for u in range(n):  # @line L3
        if color[u] != WHITE:  # @line L4
            continue
        color[u] = GRAY  # @line L5
        time += 1
        d[u] = time
        stack.append(u)
        while stack:  # @line L6
            x = stack[-1]  # @line L7
            if nxt[x] < len(adj[x]):  # @line L8
                v = adj[x][nxt[x]]  # @line L9
                nxt[x] += 1
                if color[v] == WHITE:  # @line L10
                    parent[v] = x  # @line L11
                    color[v] = GRAY
                    time += 1
                    d[v] = time
                    stack.append(v)
            else:
                stack.pop()  # @line L12
                color[x] = BLACK
                time += 1
                f[x] = time
    return d, f, parent  # @line L13
