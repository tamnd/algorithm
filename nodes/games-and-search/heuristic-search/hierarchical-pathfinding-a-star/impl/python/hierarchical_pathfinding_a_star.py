# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hierarchical-pathfinding-a-star/. The authors are listed in prov/XNV0WK.jsonl.

"""HPA* (Botea, Mueller and Schaeffer) with one level of abstraction, on a 4-connected unit-cost grid.

Preprocessing splits the grid into square clusters, finds the entrances on
the borders between clusters, puts transition nodes on each entrance, and
links the nodes of each cluster by their exact distances inside the cluster.
A query inserts the start and the goal, runs A* on the small abstract graph,
and refines each abstract edge into a grid path. The result is a valid path,
but it is not always a shortest one.
"""

import heapq
from collections import deque

MOVES = ((1, 0), (-1, 0), (0, 1), (0, -1))
SINGLE_LIMIT = 6  # entrances shorter than this get one transition, the others two


class HPAStar:
    def __init__(self, rows: list[str], c: int):
        """rows[y][x] is '#' for a wall. c is the side of a cluster."""
        if c < 1:
            raise ValueError("the cluster size must be positive")
        self.rows, self.c = rows, c
        self.h, self.w = len(rows), len(rows[0]) if rows else 0
        self.graph: dict = {}  # abstract node (a cell) -> {node: cost}
        self.entrances: list = []  # lists of (cell in one cluster, cell in the other) along a border
        self._build()

    def free(self, x: int, y: int) -> bool:
        return 0 <= x < self.w and 0 <= y < self.h and self.rows[y][x] != "#"

    def cluster(self, cell: tuple[int, int]) -> tuple[int, int]:
        return cell[0] // self.c, cell[1] // self.c

    def _add_edge(self, a, b, cost):
        self.graph.setdefault(a, {})
        self.graph.setdefault(b, {})
        if cost < self.graph[a].get(b, float("inf")):
            self.graph[a][b] = self.graph[b][a] = cost

    def _build(self):
        c = self.c
        borders = []  # @line L1
        for x in range(c, self.w, c):  # vertical borders between columns x - 1 and x
            for y0 in range(0, self.h, c):
                borders.append([((x - 1, y), (x, y)) for y in range(y0, min(y0 + c, self.h))])
        for y in range(c, self.h, c):  # horizontal borders between rows y - 1 and y
            for x0 in range(0, self.w, c):
                borders.append([((x, y - 1), (x, y)) for x in range(x0, min(x0 + c, self.w))])
        for border in borders:  # @line L2
            run = []
            for a, b in border + [(None, None)]:  # @line L3
                if a is not None and self.free(*a) and self.free(*b):
                    run.append((a, b))
                    continue
                if run:
                    self.entrances.append(run)
                    if len(run) < SINGLE_LIMIT:  # @line L4
                        chosen = [run[len(run) // 2]]
                    else:
                        chosen = [run[0], run[-1]]
                    for p, q in chosen:  # @line L5
                        self._add_edge(p, q, 1)
                run = []
        by_cluster: dict = {}
        for node in self.graph:
            by_cluster.setdefault(self.cluster(node), []).append(node)
        for cl, nodes in by_cluster.items():  # @line L6
            for i, a in enumerate(nodes):
                dist, _ = self.search_in_cluster(a, cl)
                for b in nodes[i + 1 :]:
                    if b in dist:
                        self._add_edge(a, b, dist[b])  # @line L7

    def search_in_cluster(self, src, cl):
        """Breadth-first search from src that stays inside the cluster cl. Return distances and parents."""
        dist, parent = {src: 0}, {src: None}
        queue = deque([src])
        while queue:
            u = queue.popleft()
            for dx, dy in MOVES:
                v = (u[0] + dx, u[1] + dy)
                if v not in dist and self.free(*v) and self.cluster(v) == cl:
                    dist[v] = dist[u] + 1
                    parent[v] = u
                    queue.append(v)
        return dist, parent

    def find_path(self, s: tuple[int, int], t: tuple[int, int]):
        """Return (a grid path from s to t, its cost, the number of abstract nodes expanded), or (None, None, n)."""
        if not (self.free(*s) and self.free(*t)):
            raise ValueError("start and goal must be free cells")
        extra: dict = {s: {}, t: {}}  # @line L8
        for x in (s, t):
            cl = self.cluster(x)
            dist, _ = self.search_in_cluster(x, cl)
            for node in self.graph:
                if self.cluster(node) == cl and node in dist and node != x:
                    extra[x][node] = dist[node]
            if x == s and t in dist:
                extra[s][t] = dist[t]

        def neighbours(u):
            for v, w in self.graph.get(u, {}).items():
                yield v, w
            for v, w in extra.get(u, {}).items():
                yield v, w
            for x in (s, t):  # the reverse edges from the inserted nodes
                if u in extra[x] and u != x:
                    yield x, extra[x][u]

        def hman(u):
            return abs(u[0] - t[0]) + abs(u[1] - t[1])

        g, parent = {s: 0}, {s: None}
        heap = [(hman(s), 0, s)]
        closed = set()
        expanded = 0
        tie = 0
        while heap:  # @line L9
            _, _, u = heapq.heappop(heap)
            if u in closed:
                continue
            closed.add(u)
            expanded += 1
            if u == t:
                break
            for v, w in neighbours(u):
                if g[u] + w < g.get(v, float("inf")):
                    g[v] = g[u] + w
                    parent[v] = u
                    tie += 1
                    heapq.heappush(heap, (g[v] + hman(v), tie, v))
        if t not in closed:
            return None, None, expanded  # @line L10
        abstract = [t]
        while parent[abstract[-1]] is not None:
            abstract.append(parent[abstract[-1]])
        abstract.reverse()
        path = [s]
        for a, b in zip(abstract, abstract[1:]):  # @line L11
            if self.cluster(a) != self.cluster(b):  # an inter-edge between two neighbouring cells
                path.append(b)
                continue
            _, par = self.search_in_cluster(a, self.cluster(a))
            piece = [b]
            while piece[-1] != a:
                piece.append(par[piece[-1]])
            path.extend(reversed(piece[:-1]))
        return path, g[t], expanded
