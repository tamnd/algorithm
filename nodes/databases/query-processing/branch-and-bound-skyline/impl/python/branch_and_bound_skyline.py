# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/branch-and-bound-skyline/. The authors are listed in prov/G5JMTR.jsonl.

"""Branch-and-bound skyline (BBS) over a static R-tree, smaller values are better.

A point p dominates q when p[i] <= q[i] in every dimension and p[i] < q[i] in
at least one. The skyline is the set of points that no point dominates; equal
points do not dominate each other, so duplicates of a skyline point are all in
the skyline.

The R-tree is built by Sort-Tile-Recursive (STR) packing with a fixed node
capacity. BBS keeps a min-heap of entries keyed by mindist, the L1 distance
from the origin to the lower corner of the entry (for a point, the sum of its
coordinates). It pops the entry with the smallest key; an entry whose lower
corner is dominated by a skyline point found so far is discarded, a node is
expanded (one node read), and a point is a new skyline point. Children are
also checked before they are pushed.
"""

import heapq
import itertools
import math
from collections.abc import Sequence


def dominates(p: Sequence, q: Sequence) -> bool:
    """p dominates q: no worse in every dimension and better in at least one."""
    better = False
    for a, b in zip(p, q):
        if a > b:
            return False
        if a < b:
            better = True
    return better


class Node:
    """An R-tree node: lo and hi are the corners of its MBR; children are Nodes or point ids."""

    __slots__ = ("lo", "hi", "children", "leaf")

    def __init__(self, lo: tuple, hi: tuple, children: list, leaf: bool) -> None:
        self.lo, self.hi, self.children, self.leaf = lo, hi, children, leaf


def _tile(items: list, center, dim: int, dims: int, cap: int) -> list:
    """STR: split items (sorted by center[dim]) into slabs, recursively, into groups of at most cap."""
    if dim == dims - 1 or len(items) <= cap:
        items = sorted(items, key=lambda it: center(it)[dim])
        return [items[i:i + cap] for i in range(0, len(items), cap)]
    pages = math.ceil(len(items) / cap)
    slabs = math.ceil(pages ** (1 / (dims - dim)))
    per = cap * math.ceil(pages / slabs)
    items = sorted(items, key=lambda it: center(it)[dim])
    out = []
    for i in range(0, len(items), per):
        out += _tile(items[i:i + per], center, dim + 1, dims, cap)
    return out


def build_rtree(points: Sequence[tuple], cap: int = 4) -> Node | None:
    """A static R-tree over the point ids 0..n-1, packed bottom-up by STR."""
    if not points:
        return None
    dims = len(points[0])
    groups = _tile(list(range(len(points))), lambda i: points[i], 0, dims, cap)
    level = []
    for g in groups:
        lo = tuple(min(points[i][k] for i in g) for k in range(dims))
        hi = tuple(max(points[i][k] for i in g) for k in range(dims))
        level.append(Node(lo, hi, g, True))
    while len(level) > 1:
        groups = _tile(level, lambda nd: tuple((a + b) / 2 for a, b in zip(nd.lo, nd.hi)), 0, dims, cap)
        level = [Node(tuple(min(c.lo[k] for c in g) for k in range(dims)),
                      tuple(max(c.hi[k] for c in g) for k in range(dims)), g, False) for g in groups]
    return level[0]


def all_nodes(root: Node | None) -> list:
    out, stack = [], [root] if root else []
    while stack:
        nd = stack.pop()
        out.append(nd)
        if not nd.leaf:
            stack.extend(nd.children)
    return out


def bbs(points: Sequence[tuple], root: Node | None):
    """Return (skyline ids in output order, stats) with stats nodes_read and max_heap."""
    stats = {"nodes_read": 0, "max_heap": 0}
    if root is None:
        return [], stats
    sky: list = []
    tie = itertools.count()
    heap = [(sum(root.lo), next(tie), root)]  # @line L1
    while heap:  # @line L2
        stats["max_heap"] = max(stats["max_heap"], len(heap))
        _, _, e = heapq.heappop(heap)  # @line L3
        corner = e.lo if isinstance(e, Node) else points[e]
        if any(dominates(points[s], corner) for s in sky):
            continue  # @line L4
        if isinstance(e, Node):  # @line L5
            stats["nodes_read"] += 1
            for c in e.children:
                cc = c.lo if isinstance(c, Node) else points[c]
                if not any(dominates(points[s], cc) for s in sky):
                    heapq.heappush(heap, (sum(cc), next(tie), c))  # @line L6
        else:
            sky.append(e)  # @line L7
    return sky, stats  # @line L8


def skyline_bruteforce(points: Sequence[tuple]) -> list:
    return [i for i, p in enumerate(points) if not any(dominates(q, p) for q in points)]
