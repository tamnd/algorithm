# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dulmage-mendelsohn-decomposition/. The authors are listed in prov/7KYG8D.jsonl.

from collections import deque
from typing import NamedTuple

INF = float("inf")


class Part(NamedTuple):
    left: list[int]  # sorted left vertices of the part
    right: list[int]  # sorted right vertices of the part


class DMDecomposition(NamedTuple):
    size: int  # the matching number
    mate_left: list[int]  # a maximum matching: mate_left[x] is y or -1
    mate_right: list[int]  # mate_right[y] is x or -1
    x_surplus: Part  # reachable from free left vertices; more left than right
    blocks: list[Part]  # the square part, in topological order
    y_surplus: Part  # reachable from free right vertices; more right than left


def dulmage_mendelsohn(
    n_left: int, n_right: int, edges: list[tuple[int, int]]
) -> DMDecomposition:
    """Dulmage-Mendelsohn decomposition of a bipartite graph.

    The left side is 0 .. n_left - 1, the right side 0 .. n_right - 1, and each
    pair (x, y) joins left x to right y; the graph is unweighted. Returns a
    maximum matching, the part reachable by alternating paths from free left
    vertices, the part reachable from free right vertices, and the blocks of the
    rest, ordered so that every edge from block i to block j has its left end in
    block i, its right end in block j, and i < j.
    O((n + m) sqrt(n)) time for the matching, then O(n + m); O(n + m) space.
    """
    adj_l: list[list[int]] = [[] for _ in range(n_left)]
    adj_r: list[list[int]] = [[] for _ in range(n_right)]
    for x, y in edges:
        if not (0 <= x < n_left and 0 <= y < n_right):
            raise ValueError("edge end out of range")
        adj_l[x].append(y)
        adj_r[y].append(x)
    mate_l, mate_r, size = _hopcroft_karp(n_left, n_right, adj_l)  # @line L1

    # Alternating search from the free left vertices: non-matching edges from
    # left to right, matching edges from right to left.
    in_xl = [mate_l[x] < 0 for x in range(n_left)]  # @line L2
    in_xr = [False] * n_right
    queue = deque(x for x in range(n_left) if in_xl[x])
    while queue:  # @line L3
        x = queue.popleft()
        for y in adj_l[x]:  # @line L4
            if not in_xr[y]:
                in_xr[y] = True
                x2 = mate_r[y]  # @line L5: y is matched, else an augmenting path
                if not in_xl[x2]:
                    in_xl[x2] = True
                    queue.append(x2)

    # The same search from the free right vertices, sides swapped.
    in_yr = [mate_r[y] < 0 for y in range(n_right)]  # @line L6
    in_yl = [False] * n_left
    queue = deque(y for y in range(n_right) if in_yr[y])
    while queue:
        y = queue.popleft()
        for x in adj_r[y]:
            if not in_yl[x]:
                in_yl[x] = True
                y2 = mate_l[x]
                if not in_yr[y2]:
                    in_yr[y2] = True
                    queue.append(y2)

    square = [  # @line L7
        x for x in range(n_left) if not in_xl[x] and not in_yl[x]
    ]
    # Digraph H on the square left vertices: x -> mate_r[y] for an edge xy.
    arcs: dict[int, list[int]] = {x: [] for x in square}  # @line L8
    for x in square:
        for y in adj_l[x]:
            x2 = mate_r[y]
            if x2 != x and x2 in arcs:
                arcs[x].append(x2)
    comps = _tarjan_scc(square, arcs)  # @line L9
    comps.reverse()  # Tarjan emits sink components first
    blocks = [  # @line L10
        Part(sorted(c), sorted(mate_l[x] for x in c)) for c in comps
    ]
    x_surplus = Part(
        [x for x in range(n_left) if in_xl[x]],
        [y for y in range(n_right) if in_xr[y]],
    )
    y_surplus = Part(
        [x for x in range(n_left) if in_yl[x]],
        [y for y in range(n_right) if in_yr[y]],
    )
    return DMDecomposition(  # @line L11
        size, mate_l, mate_r, x_surplus, blocks, y_surplus
    )


def _hopcroft_karp(
    n_left: int, n_right: int, adj: list[list[int]]
) -> tuple[list[int], list[int], int]:
    """Maximum bipartite matching in O((n + m) sqrt(n)) time, iterative."""
    mate_l = [-1] * n_left
    mate_r = [-1] * n_right
    size = 0
    while True:
        dist: list[float] = [0 if mate_l[x] < 0 else INF for x in range(n_left)]
        queue = deque(x for x in range(n_left) if mate_l[x] < 0)
        big_d: float = INF
        while queue:
            x = queue.popleft()
            if dist[x] < big_d:
                for y in adj[x]:
                    x2 = mate_r[y]
                    if x2 < 0:
                        big_d = min(big_d, dist[x] + 1)
                    elif dist[x2] == INF:
                        dist[x2] = dist[x] + 1
                        queue.append(x2)
        if big_d == INF:
            return mate_l, mate_r, size
        ptr = [0] * n_left
        for root in range(n_left):
            if mate_l[root] >= 0 or dist[root] != 0:
                continue
            stack = [root]
            level = {root: 0.0}
            dist[root] = INF
            chosen: dict[int, int] = {}
            while stack:
                x = stack[-1]
                if ptr[x] == len(adj[x]):
                    stack.pop()
                    continue
                y = adj[x][ptr[x]]
                ptr[x] += 1
                x2 = mate_r[y]
                if x2 < 0:
                    if level[x] + 1 == big_d:
                        chosen[x] = y
                        for v in stack:
                            mate_l[v] = chosen[v]
                            mate_r[chosen[v]] = v
                        size += 1
                        break
                elif dist[x2] == level[x] + 1:
                    chosen[x] = y
                    level[x2] = dist[x2]
                    dist[x2] = INF
                    stack.append(x2)


def _tarjan_scc(nodes: list[int], arcs: dict[int, list[int]]) -> list[list[int]]:
    """Strongly connected components by Tarjan's algorithm with an explicit stack.

    Components come out in reverse topological order. O(nodes + arcs) time.
    """
    index: dict[int, int] = {}
    low: dict[int, int] = {}
    on_stack: dict[int, bool] = {}
    stack: list[int] = []
    comps: list[list[int]] = []
    counter = 0
    for start in nodes:
        if start in index:
            continue
        work = [(start, 0)]
        index[start] = low[start] = counter
        counter += 1
        stack.append(start)
        on_stack[start] = True
        while work:
            v, i = work[-1]
            if i < len(arcs[v]):
                work[-1] = (v, i + 1)
                w = arcs[v][i]
                if w not in index:
                    index[w] = low[w] = counter
                    counter += 1
                    stack.append(w)
                    on_stack[w] = True
                    work.append((w, 0))
                elif on_stack.get(w, False):
                    low[v] = min(low[v], index[w])
            else:
                work.pop()
                if work:
                    u = work[-1][0]
                    low[u] = min(low[u], low[v])
                if low[v] == index[v]:
                    comp = []
                    while True:
                        w = stack.pop()
                        on_stack[w] = False
                        comp.append(w)
                        if w == v:
                            break
                    comps.append(comp)
    return comps
