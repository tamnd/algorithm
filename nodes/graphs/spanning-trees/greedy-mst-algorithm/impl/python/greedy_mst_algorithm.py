# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/greedy-mst-algorithm/. The authors are listed in prov/701F07.jsonl.

import random
from collections import deque

UNCOLORED, BLUE, RED = 0, 1, 2


def greedy_mst(
    n: int, edges: list[tuple[int, int, float]], rng: random.Random | None = None
) -> tuple[list[int], list[tuple[str, int]]]:
    """Color the edges by the blue rule and the red rule; return (blue edges, log).

    The vertices are 0 .. n - 1 and edges[i] = (u, v, w) is an undirected
    edge. Weights may tie (the rules then pick by the edge index); the graph
    may be disconnected, and parallel edges and self-loops are allowed. The
    blue edges at the end form a minimum spanning forest. The log lists each
    step as ("blue", i) or ("red", i).

    With rng = None the choices are fixed: the uncolored edge with the
    smallest index, the cut around the blue tree of its first end, and the
    cycle through the blue path. With an rng, the edge, the cut (a random
    union of blue trees) and the cycle (a random path of non-red edges) are
    random, which exercises the free choices of the method.

    Cost: m steps of O(n + m) each, so O(m (n + m)) time; O(n + m) space.
    """
    m = len(edges)
    color = [UNCOLORED] * m  # @line L1
    log: list[tuple[str, int]] = []
    while UNCOLORED in color:  # @line L2
        todo = [i for i in range(m) if color[i] == UNCOLORED]
        e = todo[0] if rng is None else rng.choice(todo)
        u, v, _ = edges[e]
        comp = _labels(n, edges, color)
        if comp[u] != comp[v]:  # @line L3
            s = {comp[u]}  # @line L4
            if rng is not None:
                s |= {t for t in set(comp) if t != comp[v] and rng.random() < 0.5}
            crossing = [i for i in todo if (comp[edges[i][0]] in s) != (comp[edges[i][1]] in s)]
            pick = min(crossing, key=lambda i: (edges[i][2], i))  # @line L5
            color[pick] = BLUE
            log.append(("blue", pick))
        else:  # @line L6
            cycle = [e] + _path(n, edges, color, e, u, v, rng)  # @line L7
            pick = max((i for i in cycle if color[i] == UNCOLORED), key=lambda i: (edges[i][2], -i))  # @line L8
            color[pick] = RED
            log.append(("red", pick))
    return [i for i in range(m) if color[i] == BLUE], log  # @line L9


def _labels(n: int, edges: list[tuple[int, int, float]], color: list[int]) -> list[int]:
    """Label each vertex with the smallest vertex of its blue tree."""
    adj: list[list[int]] = [[] for _ in range(n)]
    for i, (a, b, _) in enumerate(edges):
        if color[i] == BLUE:
            adj[a].append(b)
            adj[b].append(a)
    comp = [-1] * n
    for s in range(n):
        if comp[s] < 0:
            comp[s] = s
            stack = [s]
            while stack:
                x = stack.pop()
                for y in adj[x]:
                    if comp[y] < 0:
                        comp[y] = s
                        stack.append(y)
    return comp


def _path(
    n: int, edges: list[tuple[int, int, float]], color: list[int], e: int, u: int, v: int, rng: random.Random | None
) -> list[int]:
    """Edge indices of a path from u to v that avoids e and red edges.

    Without an rng, only blue edges are used (such a path exists when u and v
    are in one blue tree). With an rng, any non-red edges, in random order.
    """
    adj: list[list[tuple[int, int]]] = [[] for _ in range(n)]
    for i, (a, b, _) in enumerate(edges):
        if i != e and (color[i] == BLUE or (rng is not None and color[i] == UNCOLORED)):
            adj[a].append((b, i))
            adj[b].append((a, i))
    if rng is not None:
        for lst in adj:
            rng.shuffle(lst)
    back: dict[int, tuple[int, int]] = {u: (-1, -1)}
    queue = deque([u])
    while queue and v not in back:
        x = queue.popleft()
        for y, i in adj[x]:
            if y not in back:
                back[y] = (x, i)
                queue.append(y)
    path: list[int] = []
    x = v
    while x != u:
        x, i = back[x]
        path.append(i)
    return path
