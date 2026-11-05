# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/edmonds-blossom/. The authors are listed in prov/6F205G.jsonl.

from collections import deque
from typing import Callable, NamedTuple, Optional


class Matching(NamedTuple):
    size: int
    mate: list[int]  # mate[v] is the partner of v, or -1 if v is free
    phases: int  # number of forest searches, the last one included


def edmonds_blossom(
    n: int,
    edges: list[tuple[int, int]],
    on_event: Optional[Callable[[str, tuple], None]] = None,
) -> Matching:
    """Maximum matching of a general graph by Edmonds' blossom algorithm.

    Vertices are 0 .. n - 1 and each pair (u, v) in edges is an undirected edge;
    the graph is unweighted and need not be bipartite. Self-loops are ignored and
    parallel edges are allowed. The optional callback gets ("blossom", (base,
    vertices)) for each contraction and ("augment", path) for each augmentation.
    At most n/2 + 1 phases of O(n^2 + m) time each, so O(n^3) time for a simple
    graph (O(n (n^2 + m)) in general); O(n + m) space.
    """
    adj: list[list[int]] = [[] for _ in range(n)]
    for u, v in edges:
        if not (0 <= u < n and 0 <= v < n):
            raise ValueError("edge end out of range")
        if u != v:
            adj[u].append(v)
            adj[v].append(u)
    mate = [-1] * n  # @line L1
    size = 0
    phases = 0
    while True:  # @line L2
        phases += 1
        path = _phase(n, adj, mate, on_event)
        if path is None:  # @line L12
            return Matching(size, mate, phases)
        size += 1


def _phase(n, adj, mate, on_event):
    """Grow an alternating forest from all free vertices; augment once or prove maximality."""
    base = list(range(n))  # @line L3
    parent = [-1] * n  # parent[y] of an inner vertex y, and links inside blossoms
    outer = [False] * n
    tree = [-1] * n
    queue: deque[int] = deque()
    for v in range(n):
        if mate[v] < 0:
            outer[v] = True
            tree[v] = v
            queue.append(v)
    while queue:  # @line L4
        v = queue.popleft()
        for w in adj[v]:  # @line L5
            if base[v] == base[w] or mate[v] == w:  # @line L6
                continue
            if outer[w] and tree[w] != tree[v]:  # @line L7
                path = _root_path(v, mate, parent)[::-1] + _root_path(w, mate, parent)
                _flip(v, mate, parent)  # @line L8
                _flip(w, mate, parent)
                mate[v], mate[w] = w, v
                if on_event is not None:
                    on_event("augment", tuple(path))
                return path
            if outer[w]:  # @line L9: an edge inside one tree closes a blossom
                b = _lca(v, w, base, mate, parent)
                in_blossom = [False] * n
                _mark_path(v, b, w, base, mate, parent, in_blossom)  # @line L10
                _mark_path(w, b, v, base, mate, parent, in_blossom)
                members = [b]
                for x in range(n):
                    if in_blossom[base[x]]:
                        if x != b:
                            members.append(x)
                        base[x] = b
                        if not outer[x]:
                            outer[x] = True
                            queue.append(x)
                if on_event is not None:
                    on_event("blossom", (b, tuple(sorted(members))))
            elif parent[w] < 0:  # @line L11: w is not in the forest yet, so it is matched
                parent[w] = v
                tree[w] = tree[v]
                u = mate[w]
                outer[u] = True
                tree[u] = tree[v]
                queue.append(u)
    return None


def _lca(a: int, b: int, base: list[int], mate: list[int], parent: list[int]) -> int:
    """Base of the blossom closed by an edge between two outer vertices of one tree."""
    seen = set()
    while True:
        a = base[a]
        seen.add(a)
        if mate[a] < 0:
            break
        a = parent[mate[a]]
    while True:
        b = base[b]
        if b in seen:
            return b
        b = parent[mate[b]]


def _mark_path(v, b, child, base, mate, parent, in_blossom):
    """Walk from v up to the base b, linking the outer vertices back towards child."""
    while base[v] != b:
        in_blossom[base[v]] = True
        in_blossom[base[mate[v]]] = True
        parent[v] = child
        child = mate[v]
        v = parent[mate[v]]


def _root_path(x: int, mate: list[int], parent: list[int]) -> list[int]:
    """The even alternating path from the outer vertex x to the root of its tree."""
    path = [x]
    y = mate[x]
    while y >= 0:
        z = parent[y]
        path += [y, z]
        y = mate[z]
    return path


def _flip(x: int, mate: list[int], parent: list[int]) -> None:
    """Flip the path from the outer vertex x to its root; x is left free."""
    y = mate[x]
    while y >= 0:
        z = parent[y]
        nxt = mate[z]
        mate[y], mate[z] = z, y
        y = nxt
