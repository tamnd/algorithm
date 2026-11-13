# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/connected-component-labeling/. The authors are listed in prov/FCV9GC.jsonl.

"""Two-pass connected component labeling with union-find.

A binary image is a list of H rows, each a list of W values; a pixel is
foreground when its value is nonzero. The first pass scans in raster order
and gives each foreground pixel a provisional label, taken from a scanned
neighbor or new, and records in a disjoint-set forest that the labels of
all scanned foreground neighbors are equivalent. The second pass replaces
each provisional label by a final label of its set.

Final labels are 1..K, numbered in the raster order of the first pixel of
each component, and the background is 0. The forest uses union by rank and
path halving, so the cost is O(N alpha(N)) time and O(N) space for N = WH.
"""

from typing import List, Sequence, Tuple

Image = List[List[int]]

# Neighbors that the raster scan has already visited: (dx, dy).
_PREV4 = ((-1, 0), (0, -1))
_PREV8 = ((-1, 0), (-1, -1), (0, -1), (1, -1))


class DisjointSet:
    """Disjoint-set forest on 1..n with union by rank and path halving."""

    def __init__(self) -> None:
        self.parent: List[int] = [0]
        self.rank: List[int] = [0]

    def make_set(self) -> int:
        self.parent.append(len(self.parent))
        self.rank.append(0)
        return len(self.parent) - 1

    def find(self, x: int) -> int:
        p = self.parent
        while p[x] != x:
            p[x] = p[p[x]]
            x = p[x]
        return x

    def union(self, a: int, b: int) -> None:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return
        if self.rank[ra] < self.rank[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] += 1


def label(img: Sequence[Sequence[int]], connectivity: int = 8) -> Tuple[Image, int]:
    """Label the foreground components of img. Returns (labels, K)."""
    if connectivity not in (4, 8):
        raise ValueError("connectivity must be 4 or 8")
    prev = _PREV4 if connectivity == 4 else _PREV8
    h = len(img)
    w = len(img[0]) if h else 0
    lab: Image = [[0] * w for _ in range(h)]
    ds = DisjointSet()  # @line L1
    for y in range(h):  # @line L2
        for x in range(w):  # @line L3
            if not img[y][x]:  # @line L4
                continue
            seen = []  # @line L5
            for dx, dy in prev:
                nx, ny = x + dx, y + dy
                if 0 <= nx < w and 0 <= ny and lab[ny][nx]:
                    seen.append(lab[ny][nx])
            if not seen:  # @line L6
                lab[y][x] = ds.make_set()  # @line L7
            else:  # @line L8
                lab[y][x] = seen[0]  # @line L9
                for b in seen[1:]:  # @line L10
                    ds.union(seen[0], b)
    final = {}
    for y in range(h):  # @line L11
        for x in range(w):
            if lab[y][x]:
                r = ds.find(lab[y][x])  # @line L12
                if r not in final:  # @line L13
                    final[r] = len(final) + 1
                lab[y][x] = final[r]  # @line L14
    return lab, len(final)  # @line L15


def label_background(img: Sequence[Sequence[int]], connectivity: int = 4) -> Tuple[Image, int]:
    """Label the components of the background (the zero pixels)."""
    inv = [[0 if v else 1 for v in row] for row in img]
    return label(inv, connectivity)


def count_holes(img: Sequence[Sequence[int]], background_connectivity: int = 4) -> int:
    """Background components that do not touch the image border."""
    h = len(img)
    w = len(img[0]) if h else 0
    lab, k = label_background(img, background_connectivity)
    border = set()
    for y in range(h):
        for x in range(w):
            if (x in (0, w - 1) or y in (0, h - 1)) and lab[y][x]:
                border.add(lab[y][x])
    return k - len(border)


def component_sizes(lab: Sequence[Sequence[int]], k: int) -> List[int]:
    """sizes[i] is the number of pixels with label i, for i = 1..k (index 0 unused)."""
    sizes = [0] * (k + 1)
    for row in lab:
        for v in row:
            if v:
                sizes[v] += 1
    return sizes
