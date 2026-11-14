# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rectilinear-minimum-spanning-tree/. The authors are listed in prov/53V9N5.jsonl.

from bisect import bisect_left
from typing import Sequence

Point = tuple[int, int]
Edge = tuple[int, int, int]  # (length, i, j)


def l1(p: Point, q: Point) -> int:
    return abs(p[0] - q[0]) + abs(p[1] - q[1])


def region_neighbors(pts: Sequence[Point], strict_x: bool, strict_k: bool) -> list[int]:
    """For each point i, the point j that minimizes x_j + y_j among the points with

    x_j >= x_i (or > if strict_x) and y_j - x_j >= y_i - x_i (or > if strict_k).
    In that region the L1 distance from i is (x_j + y_j) - (x_i + y_i).
    Returns -1 where the region is empty. Uses a sweep in decreasing x and a
    Fenwick tree for suffix minima over the ranks of y - x. The points must be distinct.
    """
    n = len(pts)
    keys = sorted({y - x for x, y in pts})
    m = len(keys)
    inf = (float("inf"), -1)
    tree = [inf] * (m + 1)  # Fenwick tree over reversed ranks, holding minima

    def update(rank: int, val: tuple) -> None:
        i = m - rank
        while i <= m:
            if val < tree[i]:
                tree[i] = val
            i += i & -i

    def query(rank: int) -> tuple:  # minimum over ranks >= rank
        i = m - rank
        best = inf
        while i > 0:
            if tree[i] < best:
                best = tree[i]
            i -= i & -i
        return best

    order = sorted(range(n), key=lambda i: (-pts[i][0], -pts[i][1]))  # @line L4
    out = [-1] * n
    g = 0
    while g < n:
        h = g
        while h < n and pts[order[h]][0] == pts[order[g]][0]:
            h += 1
        group = order[g:h]  # equal x, in decreasing y
        for i in group:
            x, y = pts[i]
            r = bisect_left(keys, y - x)
            best = query(r + 1 if strict_k else r)  # @line L5
            out[i] = best[1]
            if not strict_x:
                update(r, (x + y, i))  # @line L7
        if strict_x:
            for i in group:
                x, y = pts[i]
                update(bisect_left(keys, y - x), (x + y, i))  # @line L7
        g = h
    return out


# The four half-open octants [0, 45), [45, 90), [90, 135), [135, 180) degrees,
# each mapped onto a region of region_neighbors by an L1 isometry.
OCTANTS = (
    (lambda x, y: (y, x), False, True),
    (lambda x, y: (x, y), True, False),
    (lambda x, y: (-x, y), False, True),
    (lambda x, y: (y, -x), True, False),
)


def octant_graph(pts: Sequence[Point]) -> list[Edge]:
    """Edges from each distinct point to a nearest point in each of four half-open octants."""
    edges = []
    for f, sx, sk in OCTANTS:  # @line L2
        moved = [f(x, y) for x, y in pts]  # @line L3
        nb = region_neighbors(moved, sx, sk)
        for i, j in enumerate(nb):
            if j >= 0:  # @line L6
                edges.append((l1(pts[i], pts[j]), i, j))
    return edges


def find(parent: list[int], a: int) -> int:
    while parent[a] != a:
        parent[a] = parent[parent[a]]
        a = parent[a]
    return a


def rectilinear_minimum_spanning_tree(points: Sequence[Point]) -> list[Edge]:
    """Return the edges (length, i, j) of a minimum spanning tree of points under the L1 metric.

    Indices refer to the input list. Repeated points are joined by edges of length 0.
    Runs in O(n log n) time.
    """
    n = len(points)
    first: dict[Point, int] = {}
    edges: list[Edge] = []
    uniq: list[int] = []
    for i, p in enumerate(points):  # @line L1
        if p in first:
            edges.append((0, first[p], i))
        else:
            first[p] = i
            uniq.append(i)
    sub = [points[i] for i in uniq]
    for d, a, b in octant_graph(sub):
        edges.append((d, uniq[a], uniq[b]))
    edges.sort()  # @line L8
    parent = list(range(n))
    tree = []
    for d, a, b in edges:
        ra, rb = find(parent, a), find(parent, b)
        if ra != rb:
            parent[ra] = rb
            tree.append((d, a, b))
    return tree  # @line L9
