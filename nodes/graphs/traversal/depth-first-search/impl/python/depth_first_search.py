# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/depth-first-search/. The authors are listed in prov/Q8B7W6.jsonl.

WHITE, GRAY, BLACK = 0, 1, 2


def depth_first_search(adj: list[list[int]]) -> tuple[list[int], list[int], list[int | None]]:
    """Run a full DFS on the graph with vertices 0 .. n-1 and adjacency lists adj.

    Returns (d, f, parent): the discovery time, the finish time and the DFS parent of
    each vertex. The times are 1 .. 2n. The roots are tried in the order 0 .. n-1 and
    each list in its given order, so the result is the one of the recursive procedure.
    The recursion is simulated with an explicit stack of (vertex, next index) pairs,
    so a long path does not overflow the Python stack. Time O(n + m), extra space O(n).
    """
    n = len(adj)
    color = [WHITE] * n  # @line L1
    parent: list[int | None] = [None] * n
    d = [0] * n
    f = [0] * n
    time = 0  # @line L2
    for root in range(n):  # @line L3
        if color[root] != WHITE:  # @line L4
            continue
        # DFS-VISIT(root), with the call stack made explicit.
        time += 1  # @line L5
        d[root] = time
        color[root] = GRAY
        stack = [(root, 0)]
        while stack:
            u, i = stack[-1]
            if i < len(adj[u]):  # @line L6
                stack[-1] = (u, i + 1)
                v = adj[u][i]
                if color[v] == WHITE:  # @line L7
                    parent[v] = u  # @line L8
                    time += 1  # @line L9: the call DFS-VISIT(v) starts with line L5
                    d[v] = time
                    color[v] = GRAY
                    stack.append((v, 0))
            else:
                stack.pop()
                time += 1  # @line L10
                f[u] = time
                color[u] = BLACK
    return d, f, parent
