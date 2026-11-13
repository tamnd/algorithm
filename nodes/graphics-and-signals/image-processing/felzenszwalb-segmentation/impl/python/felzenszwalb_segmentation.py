# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/felzenszwalb-segmentation/. The authors are listed in prov/SE60TX.jsonl.

"""Felzenszwalb-Huttenlocher graph-based segmentation.

The input is an undirected graph with n nodes 0..n-1 and weighted edges
(w, u, v). The algorithm sorts the edges by weight and runs over them like
Kruskal's algorithm. Two components C1 and C2 joined by the edge are merged
when w <= MInt(C1, C2) = min(Int(C1) + k/|C1|, Int(C2) + k/|C2|), where
Int(C) is the largest edge weight of a minimum spanning tree of C. Because
the edges come in sorted order, the weight of the merging edge is the new
Int of the merged component.

The threshold k/|C| is kept as a Fraction, so integer weights give exact
decisions. For an image, grid_edges builds the 4- or 8-connected pixel graph
with the absolute gray difference (or the Euclidean color distance) as the
weight.
"""

import math
from fractions import Fraction
from typing import Dict, List, Sequence, Tuple

Edge = Tuple[object, int, int]


class Forest:
    """Disjoint-set forest with union by size, path halving, and Int per root."""

    def __init__(self, n: int) -> None:
        self.parent = list(range(n))
        self.size = [1] * n
        self.internal: List[object] = [0] * n

    def find(self, x: int) -> int:
        p = self.parent
        while p[x] != x:
            p[x] = p[p[x]]
            x = p[x]
        return x

    def union(self, a: int, b: int) -> int:
        """Link the roots a and b and return the new root."""
        if self.size[a] < self.size[b]:
            a, b = b, a
        self.parent[b] = a
        self.size[a] += self.size[b]
        return a


def threshold(size: int, k) -> Fraction:
    """The function tau(C) = k / |C|."""
    return Fraction(k) / size


def segment_graph(n: int, edges: Sequence[Edge], k, min_size: int = 0) -> List[int]:
    """Return a list comp with comp[v] = the root of the component of v.

    Ties in weight are broken by the position in the input list (a stable
    sort); the resulting partition does not depend on that order.
    """
    order = sorted(edges, key=lambda e: e[0])  # @line L1
    f = Forest(n)  # @line L2
    for w, u, v in order:  # @line L3
        a, b = f.find(u), f.find(v)  # @line L4
        if a == b:  # @line L5
            continue
        m_int = min(f.internal[a] + threshold(f.size[a], k), f.internal[b] + threshold(f.size[b], k))
        if w <= m_int:  # @line L6
            c = f.union(a, b)  # @line L7
            f.internal[c] = w  # @line L8
    if min_size > 1:
        # Postprocessing from the paper's code: join small components along
        # the edges in sorted order. This step ignores the predicate.
        for w, u, v in order:
            a, b = f.find(u), f.find(v)
            if a != b and (f.size[a] < min_size or f.size[b] < min_size):
                c = f.union(a, b)
                f.internal[c] = max(f.internal[a], f.internal[b], w)
    return [f.find(v) for v in range(n)]  # @line L9


def relabel(comp: Sequence[int]) -> List[int]:
    """Renumber components 0, 1, 2, ... in the order of their first node."""
    names: Dict[int, int] = {}
    return [names.setdefault(c, len(names)) for c in comp]


def pixel_distance(a, b):
    """Absolute difference of gray values, or Euclidean distance of color tuples."""
    if isinstance(a, (tuple, list)):
        return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))
    return abs(a - b)


def grid_edges(img: Sequence[Sequence[object]], connectivity: int = 8) -> List[Edge]:
    """Edges of the pixel grid; node id of pixel (x, y) is y * W + x."""
    if connectivity not in (4, 8):
        raise ValueError("connectivity must be 4 or 8")
    h = len(img)
    w = len(img[0]) if h else 0
    steps = [(1, 0), (0, 1)] + ([(1, 1), (-1, 1)] if connectivity == 8 else [])
    edges: List[Edge] = []
    for y in range(h):
        for x in range(w):
            for dx, dy in steps:
                nx, ny = x + dx, y + dy
                if 0 <= nx < w and ny < h:
                    edges.append((pixel_distance(img[y][x], img[ny][nx]), y * w + x, ny * w + nx))
    return edges


def segment_image(img: Sequence[Sequence[object]], k, connectivity: int = 8, min_size: int = 0) -> List[List[int]]:
    """Label image with components numbered 0, 1, ... in raster order."""
    h = len(img)
    w = len(img[0]) if h else 0
    comp = relabel(segment_graph(w * h, grid_edges(img, connectivity), k, min_size))
    return [comp[y * w:(y + 1) * w] for y in range(h)]
