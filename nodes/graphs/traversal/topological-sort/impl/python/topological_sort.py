# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/topological-sort/. The authors are listed in prov/KDXVF9.jsonl.

WHITE, GRAY, BLACK = 0, 1, 2


def topological_sort(adj: list[list[int]]) -> list[int] | None:
    """Return a topological ordering of the directed graph, or None if it has a cycle.

    The graph has the vertices 0 .. n-1 and the adjacency lists adj. The order is the
    reverse postorder of a DFS that tries the roots in the order 0 .. n-1 and each list
    in its given order, so it is the vertices by decreasing DFS finish time. The
    recursion is simulated with an explicit stack of (vertex, next index) pairs.
    Time O(n + m), extra space O(n).
    """
    n = len(adj)
    color = [WHITE] * n  # @line L1
    post: list[int] = []  # @line L2: the list L, built from the back and reversed at the end
    for root in range(n):  # @line L3
        if color[root] != WHITE:  # @line L4
            continue
        color[root] = GRAY  # @line L6
        stack = [(root, 0)]
        while stack:
            u, i = stack[-1]
            if i < len(adj[u]):  # @line L7
                stack[-1] = (u, i + 1)
                v = adj[u][i]
                if color[v] == GRAY:  # @line L8
                    return None
                if color[v] == WHITE:  # @line L9
                    color[v] = GRAY  # the call VISIT(v) starts with line L6
                    stack.append((v, 0))
            else:
                stack.pop()
                color[u] = BLACK  # @line L10
                post.append(u)  # @line L11
    post.reverse()
    return post  # @line L5
