# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/eppstein-k-shortest-paths/. The authors are listed in prov/WNETNH.jsonl.

import heapq
import math

INF = math.inf


class _Node:
    """A node of a persistent leftist heap. It holds the best sidetrack out of one vertex."""

    __slots__ = ("key", "vertex", "left", "right", "rank")

    def __init__(self, key, vertex, left=None, right=None):
        self.key = key
        self.vertex = vertex
        self.left = left
        self.right = right
        self.rank = 1 + min(_rank(left), _rank(right))


def _rank(x) -> int:
    return x.rank if x else 0


def _insert(h, node):
    """Persistent insertion of a fresh one-node heap: h is left unchanged.

    Only the nodes on the right spine of h are copied, O(log size) of them.
    """
    if h is None:
        return node
    if node.key < h.key:
        return _Node(node.key, node.vertex, h, None)
    left, right = h.left, _insert(h.right, node)
    if _rank(left) < _rank(right):
        left, right = right, left
    return _Node(h.key, h.vertex, left, right)


def _relevant(adj, radj, s, t):
    """Vertices on some s-t walk: reachable from s and reaching t."""
    n = len(adj)

    def reach(g, r):
        seen = [False] * n
        seen[r] = True
        stack = [r]
        while stack:
            u = stack.pop()
            for v, *_ in g[u]:
                if not seen[v]:
                    seen[v] = True
                    stack.append(v)
        return seen

    a, b = reach(adj, s), reach(radj, t)
    return [a[v] and b[v] for v in range(n)]


def _distances_to_t(adj, radj, t, keep):
    """d[v] = dist(v, t) inside the kept vertices, and the tree edge out of each v.

    The tree edge of v is the edge (v, nxt[v]) with index tree_edge[v] in adj[v] that
    last lowered d[v]. Returns None if a negative cycle lies among the kept vertices.
    """
    n = len(adj)
    d = [INF] * n
    nxt = [-1] * n
    tree_edge = [-1] * n
    d[t] = 0
    if all(w >= 0 for u in range(n) if keep[u] for _, w in adj[u]):
        heap = [(0, t)]
        done = [False] * n
        while heap:
            dv, v = heapq.heappop(heap)
            if done[v]:
                continue
            done[v] = True
            for u, w, i in radj[v]:
                if keep[u] and dv + w < d[u]:
                    d[u], nxt[u], tree_edge[u] = dv + w, v, i
                    heapq.heappush(heap, (d[u], u))
        return d, nxt, tree_edge
    for _ in range(n):  # Bellman-Ford on the reversed graph
        changed = False
        for v in range(n):
            if not keep[v] or d[v] == INF:
                continue
            for u, w, i in radj[v]:
                if keep[u] and d[v] + w < d[u]:
                    d[u], nxt[u], tree_edge[u] = d[v] + w, v, i
                    changed = True
        if not changed:
            return d, nxt, tree_edge
    return None


def eppstein(
    adj: list[list[tuple[int, float]]], s: int, t: int, k: int
) -> list[tuple[float, list[int]]]:
    """Return the k shortest s-t walks as (weight, vertices), lightest first.

    The graph has the vertices 0 .. n-1; adj[u] lists the edges (v, w) out of u.
    Weights are real numbers, negative ones allowed. Walks may repeat vertices and
    edges. If a negative cycle lies on some s-t walk, there is no shortest walk and
    ValueError is raised; negative cycles elsewhere are ignored. If t is not
    reachable from s, the list is empty; if fewer than k walks exist, all are returned.
    """
    n = len(adj)
    radj: list[list[tuple[int, float, int]]] = [[] for _ in range(n)]
    for u in range(n):
        for i, (v, w) in enumerate(adj[u]):
            radj[v].append((u, w, i))
    keep = _relevant(adj, radj, s, t)
    if not keep[s] or k <= 0:
        return []
    found = _distances_to_t(adj, radj, t, keep)  # @line L1
    if found is None:
        raise ValueError("a negative cycle lies on an s-t walk")
    d, nxt, tree_edge = found
    # sidetracks out of each vertex, as a binary heap array; the best one is first
    side: list[list[tuple[float, int]]] = [[] for _ in range(n)]
    for u in range(n):
        if keep[u]:
            for i, (v, w) in enumerate(adj[u]):
                if keep[v] and i != tree_edge[u]:
                    side[u].append((w + d[v] - d[u], i))  # @line L2
            heapq.heapify(side[u])
    # H[v]: persistent heap of the best sidetracks of v and of its tree ancestors
    hg: list[_Node | None] = [None] * n
    kids: list[list[int]] = [[] for _ in range(n)]
    for v in range(n):
        if nxt[v] != -1:
            kids[nxt[v]].append(v)
    order = [t]  # tree order from t: the tree parent comes first
    for v in order:
        order.extend(kids[v])
    for v in order:
        h = hg[nxt[v]] if v != t else None
        if side[v]:
            h = _insert(h, _Node(side[v][0][0], v))  # @line L3
        hg[v] = h
    result = [(d[s], _walk(adj, nxt, s, t, []))]  # @line L4
    pq: list = []
    tick = 0
    if hg[s] is not None:
        pq.append((d[s] + hg[s].key, tick, ("T", hg[s]), ()))  # @line L5
    while pq and len(result) < k:  # @line L6
        cost, _, item, hist = heapq.heappop(pq)  # @line L7
        key, u, i, children = _expand(item, side)
        seq = hist + ((u, i),)
        result.append((cost, _walk(adj, nxt, s, t, list(seq))))  # @line L8
        for child in children:  # @line L9
            ckey = _expand(child, side)[0]
            tick += 1
            heapq.heappush(pq, (cost - key + ckey, tick, child, hist))
        head = hg[adj[u][i][0]]
        if head is not None:  # @line L10
            tick += 1
            heapq.heappush(pq, (cost + head.key, tick, ("T", head), seq))
    return result  # @line L11


def _expand(item, side):
    """Key, sidetrack (u, edge index) and path-graph heap children of a node."""
    if item[0] == "T":
        node = item[1]
        key, i = side[node.vertex][0]
        children = [("T", c) for c in (node.left, node.right) if c is not None]
        # the rest of the sidetracks of the vertex hang below the T node
        children += [("A", node.vertex, c) for c in (1, 2) if c < len(side[node.vertex])]
        return key, node.vertex, i, children
    _, u, j = item  # position j >= 1 of the heap array of the sidetracks of u
    key, i = side[u][j]
    kids = [("A", u, c) for c in (2 * j + 1, 2 * j + 2) if c < len(side[u])]
    return key, u, i, kids


def _walk(adj, nxt, s: int, t: int, sidetracks: list) -> list[int]:
    """Follow tree edges from s, taking the given sidetracks in order, to t."""
    walk = [s]
    v = s
    for u, i in sidetracks:
        while v != u:
            v = nxt[v]
            walk.append(v)
        v = adj[u][i][0]
        walk.append(v)
    while v != t:
        v = nxt[v]
        walk.append(v)
    return walk
