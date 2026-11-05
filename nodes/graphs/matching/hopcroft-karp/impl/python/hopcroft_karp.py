# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hopcroft-karp/. The authors are listed in prov/V8H9RQ.jsonl.

from collections import deque
from typing import Callable, NamedTuple, Optional

INF = float("inf")


class Matching(NamedTuple):
    size: int
    mate_left: list[int]  # mate_left[x] is the right vertex matched to x, or -1
    mate_right: list[int]  # mate_right[y] is the left vertex matched to y, or -1
    phases: int  # number of breadth-first searches, the last one included


def hopcroft_karp(
    n_left: int,
    n_right: int,
    edges: list[tuple[int, int]],
    on_phase: Optional[Callable[[int, int, list[list[int]]], None]] = None,
) -> Matching:
    """Maximum matching of a bipartite graph by the Hopcroft-Karp algorithm.

    The left side is 0 .. n_left - 1, the right side is 0 .. n_right - 1, and each
    pair (x, y) in edges joins left vertex x to right vertex y. Parallel edges are
    allowed. The graph is unweighted. The optional callback gets, after each phase
    that augments, the phase number, the length D (in left layers) of the shortest
    augmenting paths, and the paths found, each as [x0, y1, x1, ..., yD].
    O(sqrt(n)) phases of O(n + m) time each, so O((n + m) sqrt(n)) time; O(n + m) space.
    """
    adj: list[list[int]] = [[] for _ in range(n_left)]
    for x, y in edges:
        if not (0 <= x < n_left and 0 <= y < n_right):
            raise ValueError("edge end out of range")
        adj[x].append(y)
    mate_l = [-1] * n_left  # @line L1
    mate_r = [-1] * n_right
    dist: list[float] = [INF] * n_left
    phases = 0
    size = 0
    while True:  # @line L2
        phases += 1
        for x in range(n_left):  # @line L3
            dist[x] = 0 if mate_l[x] < 0 else INF
        queue = deque(x for x in range(n_left) if mate_l[x] < 0)  # @line L4
        big_d: float = INF
        while queue:  # @line L5
            x = queue.popleft()
            if dist[x] < big_d:  # @line L6
                for y in adj[x]:
                    x2 = mate_r[y]
                    if x2 < 0:  # @line L7
                        big_d = min(big_d, dist[x] + 1)
                    elif dist[x2] == INF:  # @line L8
                        dist[x2] = dist[x] + 1
                        queue.append(x2)
        if big_d == INF:  # @line L9
            return Matching(size, mate_l, mate_r, phases)
        found: list[list[int]] = []
        for x in range(n_left):  # @line L10
            if mate_l[x] < 0 and dist[x] == 0:  # @line L11
                path = _dfs(x, adj, mate_l, mate_r, dist, big_d)
                if path is not None:
                    size += 1
                    found.append(path)
        if on_phase is not None:
            on_phase(phases, int(big_d), found)


def _dfs(
    root: int,
    adj: list[list[int]],
    mate_l: list[int],
    mate_r: list[int],
    dist: list[float],
    big_d: float,
) -> Optional[list[int]]:
    """DFS(root) of the pseudocode, with an explicit stack instead of recursion.

    Returns the augmenting path [x0, y1, ..., yD] after flipping it, or None.
    """
    stack = [root]
    entry_d = {root: dist[root]}  # @line L12: d <- dist[x]
    dist[root] = INF  # @line L12: dist[x] <- infinity, so x is entered once per phase
    ptr = {root: 0}
    chosen: dict[int, int] = {}
    while stack:
        x = stack[-1]
        d = entry_d[x]
        if ptr[x] < len(adj[x]):  # @line L13
            y = adj[x][ptr[x]]
            ptr[x] += 1
            x2 = mate_r[y]
            if x2 < 0:
                if d + 1 == big_d:  # @line L14: a free vertex at the last layer
                    chosen[x] = y
                    path: list[int] = []
                    for v in stack:  # @line L15: flip the path
                        mate_l[v] = chosen[v]
                        mate_r[chosen[v]] = v
                        path += [v, chosen[v]]
                    return path
            elif dist[x2] == d + 1:  # @line L14: go one layer down
                chosen[x] = y
                entry_d[x2] = dist[x2]
                dist[x2] = INF
                ptr[x2] = 0
                stack.append(x2)
        else:
            stack.pop()  # @line L16: DFS(x) returns false
    return None
