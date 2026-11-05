# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bipartiteness-testing/. The authors are listed in prov/S82K2H.jsonl.

from collections import deque
from collections.abc import Sequence


def bipartiteness_testing(adj: Sequence[Sequence[int]]) -> tuple[bool, list[int]]:
    """Test whether the undirected graph with vertices 0 .. n-1 is bipartite.

    adj[v] lists the neighbours of v; an undirected edge is in both lists, and a
    self-loop {v, v} appears as v in adj[v]. Returns (True, color) with a proper
    2-coloring color[v] in {0, 1}, or (False, cycle) where cycle is a list of
    vertices of odd length that forms a closed walk (consecutive vertices and the
    last and first vertex are adjacent) and, for a simple graph, a simple odd cycle.
    Time O(n + m), extra space O(n).
    """
    n = len(adj)
    color: list[int | None] = [None] * n  # @line L1
    parent: list[int] = [-1] * n
    for s in range(n):  # @line L2
        if color[s] is not None:
            continue
        color[s] = 0  # @line L3
        q = deque([s])
        while q:  # @line L4
            u = q.popleft()  # @line L5
            for w in adj[u]:  # @line L6
                if color[w] is None:  # @line L7
                    color[w] = 1 - color[u]  # type: ignore[operator]
                    parent[w] = u
                    q.append(w)
                elif color[w] == color[u]:  # @line L8
                    return False, _odd_cycle(parent, u, w)
    return True, [c if c is not None else 0 for c in color]  # @line L9


def _odd_cycle(parent: list[int], u: int, w: int) -> list[int]:
    """The cycle u -> ... -> z <- ... <- w closed by the edge {w, u}.

    u and w are in the same BFS layer, so they reach their lowest common
    ancestor z after the same number of parent steps.
    """
    left = [u]  # @line L10
    right = [w]
    x, y = u, w
    while x != y:
        x, y = parent[x], parent[y]
        left.append(x)
        right.append(y)
    # left ends with z, right ends with z; drop the second copy of z
    return left + right[-2::-1]  # @line L11
