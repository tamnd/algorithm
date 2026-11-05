# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kuhn-algorithm/. The authors are listed in prov/H8SH4G.jsonl.


def kuhn_algorithm(n_left: int, n_right: int, adj: list[list[int]]) -> list[int | None]:
    """Maximum matching of a bipartite graph, unweighted, by Kuhn's algorithm.

    The left side is 0 .. n_left-1 and the right side is 0 .. n_right-1;
    adj[u] lists the right neighbours of the left vertex u (repeats are allowed).
    Returns mate_left: mate_left[u] is the right mate of u, or None if u is exposed.
    The number of edges of the matching is the count of entries that are not None.
    One depth-first search per left vertex: O(n_left * (n + m)) time, O(n + m) space.
    The search uses an explicit stack, so deep paths do not hit the recursion limit.
    """
    if len(adj) != n_left:
        raise ValueError("adj must have one list per left vertex")
    mate_left: list[int | None] = [None] * n_left  # @line L1
    mate_right: list[int | None] = [None] * n_right
    for u in range(n_left):  # @line L2
        visited = [False] * n_right  # @line L3
        _try(u, adj, mate_left, mate_right, visited)  # @line L4
    return mate_left  # @line L5


def _try(
    root: int,
    adj: list[list[int]],
    mate_left: list[int | None],
    mate_right: list[int | None],
    visited: list[bool],
) -> bool:
    """TRY(root) without recursion. A frame is [x, next index into adj[x], v that x waits on]."""
    stack: list[list[int]] = [[root, 0, -1]]
    while stack:
        frame = stack[-1]
        x, i = frame[0], frame[1]
        if i == len(adj[x]):  # @line L12: every neighbour failed, TRY(x) returns false
            stack.pop()
            continue
        v = adj[x][i]  # @line L6
        frame[1] = i + 1
        if visited[v]:  # @line L7
            continue
        visited[v] = True  # @line L8
        w = mate_right[v]
        if w is not None:  # @line L9: call TRY(mate_right[v])
            frame[2] = v
            stack.append([w, 0, -1])
            continue
        # v is exposed: the path root .. x v is augmenting. Flip it along the stack.
        for j in range(len(stack) - 1, -1, -1):  # @line L10
            y = stack[j][0]
            target = v if j == len(stack) - 1 else stack[j][2]
            mate_right[target] = y
            mate_left[y] = target
        return True  # @line L11
    return False
