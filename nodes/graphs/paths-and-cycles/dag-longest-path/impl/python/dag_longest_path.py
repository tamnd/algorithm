# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dag-longest-path/. The authors are listed in prov/K16C2B.jsonl.

from collections import deque

NEG_INF = float("-inf")


def topological_order(n: int, edges: list[tuple[int, int, float]]) -> list[int]:
    """Kahn's algorithm. Raise ValueError if the directed graph has a cycle."""
    out: list[list[int]] = [[] for _ in range(n)]
    indeg = [0] * n
    for u, v, _ in edges:
        out[u].append(v)
        indeg[v] += 1
    queue = deque(u for u in range(n) if indeg[u] == 0)
    order: list[int] = []
    while queue:
        u = queue.popleft()
        order.append(u)
        for v in out[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                queue.append(v)
    if len(order) < n:
        raise ValueError("the graph has a cycle, so longest paths are not defined")
    return order


def dag_longest_path(
    n: int, edges: list[tuple[int, int, float]], s: int
) -> tuple[list[float], list[int | None]]:
    """Longest path weights from s in a directed acyclic multigraph.

    edges[i] = (u, v, w) is an arc u -> v of weight w; weights may be negative and
    parallel arcs are allowed. Returns (dist, parent): dist[v] is the largest weight of
    a path from s to v, or -inf if v is not reachable from s, and the parent pointers
    give such a path. Raises ValueError if the graph has a cycle (a self-loop is one).
    Time O(n + m), extra space O(n + m).
    """
    order = topological_order(n, edges)  # @line L1
    out: list[list[tuple[int, float]]] = [[] for _ in range(n)]
    for u, v, w in edges:
        out[u].append((v, w))
    dist: list[float] = [NEG_INF] * n  # @line L2
    parent: list[int | None] = [None] * n
    dist[s] = 0  # @line L3
    for u in order:  # @line L4
        if dist[u] == NEG_INF:  # @line L5
            continue
        for v, w in out[u]:  # @line L6
            if dist[u] + w > dist[v]:  # @line L7
                dist[v] = dist[u] + w  # @line L8
                parent[v] = u
    return dist, parent  # @line L9


def path_to(parent: list[int | None], s: int, t: int) -> list[int]:
    """The vertices of the path from s to t given by the parent pointers."""
    path = [t]
    while path[-1] != s:
        p = parent[path[-1]]
        if p is None:
            raise ValueError("t is not reachable from s")
        path.append(p)
    path.reverse()
    return path


def longest_path_anywhere(n: int, edges: list[tuple[int, int, float]]) -> tuple[float, list[int]]:
    """The heaviest path of the whole DAG, from any vertex to any vertex.

    A path of one vertex has weight 0, so the answer is at least 0 when n >= 1.
    Same as dag_longest_path with every dist starting at 0 instead of -inf.
    """
    if n == 0:
        return 0, []
    order = topological_order(n, edges)
    out: list[list[tuple[int, float]]] = [[] for _ in range(n)]
    for u, v, w in edges:
        out[u].append((v, w))
    dist: list[float] = [0] * n
    parent: list[int | None] = [None] * n
    for u in order:
        for v, w in out[u]:
            if dist[u] + w > dist[v]:
                dist[v] = dist[u] + w
                parent[v] = u
    t = max(range(n), key=lambda v: dist[v])
    path = [t]
    while parent[path[-1]] is not None:
        path.append(parent[path[-1]])  # type: ignore[arg-type]
    path.reverse()
    return dist[t], path
