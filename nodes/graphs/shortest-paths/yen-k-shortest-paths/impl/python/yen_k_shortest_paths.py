# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/yen-k-shortest-paths/. The authors are listed in prov/0RC5G2.jsonl.

import heapq


def _dijkstra_path(
    best: list[dict[int, float]], s: int, t: int, banned_vertices: set[int], banned_arcs: set[tuple[int, int]]
) -> tuple[float, list[int]] | None:
    """Shortest s-t path avoiding the banned vertices and arcs; weights must be nonnegative."""
    dist: dict[int, float] = {s: 0}
    parent: dict[int, int] = {}
    heap: list[tuple[float, int]] = [(0, s)]
    done: set[int] = set()
    while heap:
        d, u = heapq.heappop(heap)
        if u in done:
            continue
        done.add(u)
        if u == t:
            path = [t]
            while path[-1] != s:
                path.append(parent[path[-1]])
            path.reverse()
            return d, path
        for v, w in best[u].items():
            if v in banned_vertices or (u, v) in banned_arcs or v in done:
                continue
            nd = d + w
            if v not in dist or nd < dist[v]:
                dist[v] = nd
                parent[v] = u
                heapq.heappush(heap, (nd, v))
    return None


def yen_k_shortest_paths(
    n: int, edges: list[tuple[int, int, float]], s: int, t: int, k: int
) -> list[tuple[float, list[int]]]:
    """The k shortest simple s-t paths, as (weight, vertex list), in nondecreasing order of weight.

    Vertices are 0 .. n-1 and edges are (u, v, weight) with nonnegative weights. Parallel arcs are
    merged to the lightest one, since a path is given by its vertices; self-loops are ignored,
    because no simple path uses one. Fewer than k paths are returned when fewer exist.
    Time O(k n (m + n log n)) with a binary heap.
    """
    best: list[dict[int, float]] = [{} for _ in range(n)]
    for u, v, w in edges:
        if w < 0:
            raise ValueError("Yen's algorithm with Dijkstra needs nonnegative weights")
        if u != v and (v not in best[u] or w < best[u][v]):
            best[u][v] = w
    if k <= 0:
        return []
    first = _dijkstra_path(best, s, t, set(), set())  # @line L1
    if first is None:
        return []
    a = [first]
    candidates: list[tuple[float, list[int]]] = []  # @line L2: a min-heap of (weight, path)
    seen = {tuple(first[1])}
    while len(a) < k:  # @line L3
        _, prev = a[-1]
        for i in range(len(prev) - 1):  # @line L4
            spur = prev[i]  # @line L5
            root = prev[: i + 1]
            root_weight = sum(best[root[j]][root[j + 1]] for j in range(i))
            banned_arcs = {(spur, p[i + 1]) for _, p in a if len(p) > i + 1 and p[: i + 1] == root}  # @line L6
            banned_vertices = set(root[:-1])  # @line L7
            found = _dijkstra_path(best, spur, t, banned_vertices, banned_arcs)  # @line L8
            if found is not None:  # @line L9
                path = root[:-1] + found[1]
                if tuple(path) not in seen:
                    seen.add(tuple(path))
                    heapq.heappush(candidates, (root_weight + found[0], path))
            # @line L10: the banned sets are local, so nothing has to be restored
        if not candidates:  # @line L11
            break
        a.append(heapq.heappop(candidates))  # @line L12
    return a  # @line L13
