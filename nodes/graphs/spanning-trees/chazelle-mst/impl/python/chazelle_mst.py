# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chazelle-mst/. The authors are listed in prov/T77RVB.jsonl.

"""A simplified form of Chazelle's soft-heap MST algorithm.

This module keeps the two ideas that make Chazelle's algorithm work: pieces
grown by Prim's rule with a soft heap, which may corrupt (raise) keys, and
the filter MSF(G) = MSF(MSF of each piece + MSF of the contracted graph
without the bad edges + the bad edges). It does not reproduce Chazelle's
hierarchy of pieces with Ackermann-sized targets, so it does not reach the
O(m alpha(m, n)) bound; see the page for the costs.
"""

from typing import Any


class _Node:
    __slots__ = ("ckey", "rank", "items", "left", "right")

    def __init__(self, ckey: Any, items: list) -> None:
        self.ckey = ckey
        self.rank = 0
        self.items = items
        self.left: "_Node | None" = None
        self.right: "_Node | None" = None

    def is_leaf(self) -> bool:
        return self.left is None and self.right is None


class SoftHeap:
    """Soft heap after Kaplan, Tarjan and Zwick, with rank threshold t.

    Items are pairs (key, payload). Every item in a node's list has the
    node's ckey as its current key, which is at least its own key and never
    decreases. delete_min returns an item of smallest current key. A node of
    rank at most t holds at most one item, so with t >= lg(inserts) nothing
    is corrupted, and a small t corrupts many items.
    """

    def __init__(self, t: int) -> None:
        self.t = t
        self.roots: dict[int, _Node] = {}

    def _size(self, rank: int) -> int:
        s = 1
        for _ in range(self.t, rank):
            s = (3 * s + 1) // 2
        return s

    def _sift(self, x: _Node) -> None:
        target = self._size(x.rank)
        while len(x.items) < target and not x.is_leaf():
            if x.left is None or (x.right is not None and x.right.ckey < x.left.ckey):
                x.left, x.right = x.right, x.left
            c = x.left
            x.items.extend(c.items)
            x.ckey = c.ckey
            c.items = []
            if not c.is_leaf():
                self._sift(c)
            if not c.items:
                x.left = None

    def insert(self, key: Any, payload: Any) -> None:
        x = _Node(key, [(key, payload)])
        while x.rank in self.roots:
            y = self.roots.pop(x.rank)
            z = _Node(None, [])
            z.rank = x.rank + 1
            z.left, z.right = x, y
            self._sift(z)
            x = z
        self.roots[x.rank] = x

    def __bool__(self) -> bool:
        return bool(self.roots)

    def delete_min(self) -> tuple[Any, Any, Any]:
        """Remove an item of smallest current key; return (key, payload, ckey)."""
        r = min(self.roots, key=lambda k: self.roots[k].ckey)
        x = self.roots[r]
        key, payload = x.items.pop()
        ckey = x.ckey
        if not x.items:
            self._sift(x)
            if not x.items:
                del self.roots[r]
        return key, payload, ckey

    def remaining(self) -> list[tuple[Any, Any, Any]]:
        """All items still in the heap, as (key, payload, ckey)."""
        out = []
        stack = list(self.roots.values())
        while stack:
            x = stack.pop()
            out.extend((k, p, x.ckey) for k, p in x.items)
            stack.extend(c for c in (x.left, x.right) if c is not None)
        return out


def _kruskal(n: int, edges: list[tuple[int, int, Any, int]]) -> list[int]:
    parent = list(range(n))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    out = []
    for u, v, key, i in sorted(edges, key=lambda e: e[2]):
        a, b = find(u), find(v)
        if a != b:
            parent[a] = b
            out.append(i)
    return out


def _msf(n: int, edges: list[tuple[int, int, Any, int]], piece_size: int, t: int, base: int,
         log: list | None) -> list[int]:
    """edges[j] = (u, v, key, id) with distinct keys and no self-loops; returns ids."""
    if len(edges) <= base:                                                  # @line L1
        return _kruskal(n, edges)
    adj: list[list[int]] = [[] for _ in range(n)]
    for j, (u, v, _, _) in enumerate(edges):
        adj[u].append(j)
        adj[v].append(j)
    piece = [-1] * n                                                        # @line L2
    label = list(range(n))           # union-find over piece ids, for merges
    bad: set[int] = set()

    def find(x: int) -> int:
        while label[x] != x:
            label[x] = label[label[x]]
            x = label[x]
        return x

    def far(j: int, x: int) -> int:
        u, v = edges[j][0], edges[j][1]
        return v if u == x else u

    for r in range(n):                                                      # @line L3
        if piece[r] != -1:
            continue
        piece[r] = r
        size = 1
        heap = SoftHeap(t)
        for j in adj[r]:
            heap.insert(edges[j][2], (j, far(j, r)))
        while heap and size < piece_size:                                   # @line L4
            key, (j, y), ckey = heap.delete_min()                           # @line L5
            if ckey != key:
                bad.add(j)
            if piece[y] == r:                                               # @line L6
                continue
            if piece[y] != -1:
                if j not in bad:
                    label[find(r)] = find(piece[y])
                break
            piece[y] = r                                                    # @line L7
            size += 1
            for i in adj[y]:
                z = far(i, y)
                if piece[z] != r:
                    heap.insert(edges[i][2], (i, z))
        for key, (j, _), ckey in heap.remaining():                          # @line L8
            if ckey != key:
                bad.add(j)
    comp = [find(piece[x]) for x in range(n)]
    ids = sorted(set(comp))
    index = {c: k for k, c in enumerate(ids)}
    inside: dict[int, list] = {}
    between = []
    for j, (u, v, key, i) in enumerate(edges):
        if comp[u] == comp[v]:
            inside.setdefault(comp[u], []).append((u, v, key, i))
        elif j not in bad:
            between.append((index[comp[u]], index[comp[v]], key, i))
    if log is not None:
        log.append((n, len(edges), len(ids), len(bad)))
    keep = []
    for group in inside.values():                                           # @line L9
        keep.extend(_kruskal(n, group))
    keep.extend(_msf(len(ids), between, piece_size, t, base, log))          # @line L10
    keep_set = set(keep) | {edges[j][3] for j in bad}                       # @line L11
    return _kruskal(n, [e for e in edges if e[3] in keep_set])              # @line L12


def chazelle_mst(n: int, edges: list[tuple[int, int, float]], piece_size: int = 8, t: int = 2,
                 base: int = 8, log: list | None = None) -> list[int]:
    """Return the indices of the minimum spanning forest, sorted.

    The vertices are 0 .. n - 1 and edges[i] = (u, v, w) is undirected.
    Weights may tie; ties are broken by the edge index, so the answer is the
    unique forest that Kruskal's algorithm gives under the order (w, i).
    Parallel edges and self-loops are allowed. The graph need not be
    connected: the result is a minimum spanning forest.

    piece_size bounds the size of a grown piece, t is the rank threshold of
    the soft heaps (small t means many corrupted edges), and graphs with at
    most base edges go straight to Kruskal. If log is a list, each level
    appends (vertices, edges, pieces, bad edges).
    """
    work = [(u, v, (w, i), i) for i, (u, v, w) in enumerate(edges) if u != v]
    return sorted(_msf(n, work, max(piece_size, 2), t, base, log))
