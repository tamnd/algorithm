# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/iterated-one-steiner/. The authors are listed in prov/S1Z8DM.jsonl.

from typing import Sequence

Point = tuple[int, int]
Edge = tuple[int, int, int]  # (length, i, j), indices into the point list


def l1(p: Point, q: Point) -> int:
    return abs(p[0] - q[0]) + abs(p[1] - q[1])


def kruskal(n: int, edges: list[Edge]) -> list[Edge]:
    parent = list(range(n))

    def find(a: int) -> int:
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    tree = []
    for d, a, b in sorted(edges):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb
            tree.append((d, a, b))
    return tree


def mst(pts: Sequence[Point]) -> list[Edge]:
    """Minimum spanning tree of pts under the L1 metric, by Kruskal on all pairs."""
    n = len(pts)
    return kruskal(n, [(l1(pts[i], pts[j]), i, j) for i in range(n) for j in range(i + 1, n)])


def mst_with(pts: Sequence[Point], tree: list[Edge], x: Point) -> list[Edge]:
    """MST of pts + [x], from the MST of pts and the edges from x, in O(n log n) time."""
    k = len(pts)
    edges = tree + [(l1(x, p), k, i) for i, p in enumerate(pts)]
    return kruskal(k + 1, edges)


def length(tree: list[Edge]) -> int:
    return sum(d for d, _, _ in tree)


def iterated_one_steiner(pins: Sequence[Point]) -> tuple[list[Point], list[Edge]]:
    """Kahng and Robins's iterated 1-Steiner heuristic for the rectilinear Steiner tree.

    Returns (points, tree): points is the pin list followed by the chosen Steiner
    points, and tree is the L1 minimum spanning tree of points as (length, i, j).
    Each round adds the Hanan point that lowers the MST length most, then drops
    the Steiner points of degree at most 2. The loop stops when no Hanan point helps.
    """
    pins = list(pins)
    n = len(pins)
    xs = sorted({p[0] for p in pins})
    ys = sorted({p[1] for p in pins})
    pinset = set(pins)
    hanan = [(x, y) for x in xs for y in ys if (x, y) not in pinset]  # @line L1
    steiner: list[Point] = []
    while True:  # @line L2
        pts = pins + steiner
        tree = mst(pts)
        base = length(tree)  # @line L3
        best_gain, best_x = 0, None
        used = set(steiner)
        for x in hanan:
            if x in used:
                continue
            gain = base - length(mst_with(pts, tree, x))  # @line L4
            if gain > best_gain:
                best_gain, best_x = gain, x
        if best_x is None:  # @line L5
            return pts, tree
        steiner.append(best_x)  # @line L6
        while True:
            pts = pins + steiner
            tree = mst(pts)
            deg = [0] * len(pts)
            for _, a, b in tree:
                deg[a] += 1
                deg[b] += 1
            keep = [p for i, p in enumerate(steiner) if deg[n + i] > 2]  # @line L7
            if len(keep) == len(steiner):  # @line L8
                break
            steiner = keep
