# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dfs-cycle-detection/. The authors are listed in prov/YS8QZ8.jsonl.

WHITE, GRAY, BLACK = 0, 1, 2


def dfs_cycle_detection(
    n: int, edges: list[tuple[int, int]], directed: bool = True
) -> list[int] | None:
    """Return the ids of the edges of one cycle, in order, or None if there is no cycle.

    The vertices are 0 .. n-1 and edge i is edges[i] = (u, v). With directed=True it is
    the arc u -> v; with directed=False it is the undirected edge {u, v}. Parallel edges
    and self-loops are allowed. The returned list [e_1, ..., e_k] is a cycle: the edges
    are distinct, each one starts where the one before it ends, the last one ends where
    the first one starts, and no vertex is passed twice. The recursion is simulated with
    an explicit stack, so a long path does not overflow the Python stack.
    Time O(n + m), extra space O(n + m).
    """
    out: list[list[tuple[int, int]]] = [[] for _ in range(n)]
    for i, (u, v) in enumerate(edges):
        out[u].append((i, v))
        if not directed and u != v:
            out[v].append((i, u))
    color = [WHITE] * n  # @line L1
    pe: list[int] = [-1] * n  # the edge by which each vertex was discovered
    tail: list[int] = [-1] * n  # the vertex at the other end of pe

    def cycle(e: int, u: int, v: int) -> list[int]:
        c = [e]  # @line L11
        x = u
        while x != v:  # @line L12
            c.append(pe[x])
            x = tail[x]
        c.reverse()
        return c  # @line L13

    for root in range(n):  # @line L2
        if color[root] != WHITE:  # @line L3
            continue
        # VISIT(root), with the call stack made explicit.  @line L4
        color[root] = GRAY  # @line L6
        stack = [(root, 0)]
        while stack:
            u, i = stack[-1]
            if i < len(out[u]):  # @line L7
                stack[-1] = (u, i + 1)
                e, v = out[u][i]
                if not directed and e == pe[u]:
                    continue  # the tree edge back to the parent is not a cycle
                if color[v] == GRAY:  # @line L8
                    return cycle(e, u, v)
                if color[v] == WHITE:  # @line L9
                    pe[v] = e
                    tail[v] = u
                    color[v] = GRAY  # the call VISIT(v) starts with line L6
                    stack.append((v, 0))
            else:
                stack.pop()
                color[u] = BLACK  # @line L10
    return None  # @line L5
