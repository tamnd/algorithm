# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/spatial-hashing/. The authors are listed in prov/D6C9DX.jsonl.
"""Spatial hashing: an unbounded uniform grid stored in a hash table.

Boxes are closed rectangles (xmin, ymin, xmax, ymax). A box is stored in
every cell of side h that it meets. Cell (i, j) goes to bucket
((i * P1) xor (j * P2)) mod T, after the hash of Teschner et al. (2003).
Each bucket entry keeps its cell, so two cells that share a bucket are
told apart. A query reports each hit once, in the cell that holds the
lower left corner of the intersection of the query and the box.
"""

from __future__ import annotations

import math
from typing import Dict, Hashable, List, Set, Tuple

Box = Tuple[float, float, float, float]
P1, P2 = 73856093, 19349663


def intersects(a: Box, b: Box) -> bool:
    return a[0] <= b[2] and b[0] <= a[2] and a[1] <= b[3] and b[1] <= a[3]


class SpatialHash:
    def __init__(self, h: float, table_size: int = 1024) -> None:
        if h <= 0 or table_size < 1:
            raise ValueError("need h > 0 and table_size >= 1")
        self.h = h
        self.T = table_size
        self.table: List[List[Tuple[int, int, Hashable, Box]]] = [
            [] for _ in range(table_size)]
        self.size = 0

    def cell(self, x: float, y: float) -> Tuple[int, int]:
        return math.floor(x / self.h), math.floor(y / self.h)

    def bucket(self, i: int, j: int) -> int:
        return ((i * P1) ^ (j * P2)) % self.T

    def cells_of(self, b: Box):
        i0, j0 = self.cell(b[0], b[1])
        i1, j1 = self.cell(b[2], b[3])
        for i in range(i0, i1 + 1):
            for j in range(j0, j1 + 1):
                yield i, j

    def insert(self, oid: Hashable, b: Box) -> None:
        if b[0] > b[2] or b[1] > b[3]:
            raise ValueError("empty box")
        for i, j in self.cells_of(b):  # @line L1
            self.table[self.bucket(i, j)].append((i, j, oid, b))  # @line L2
        self.size += 1  # @line L3

    def query(self, q: Box) -> List[Hashable]:
        """Ids of stored boxes that meet q, each once."""
        out: List[Hashable] = []
        for i, j in self.cells_of(q):  # @line L4
            for ci, cj, oid, b in self.table[self.bucket(i, j)]:  # @line L5
                if (ci, cj) != (i, j) or not intersects(q, b):  # @line L6
                    continue
                if self.cell(max(q[0], b[0]), max(q[1], b[1])) == (i, j):  # @line L7
                    out.append(oid)
        return out

    def delete(self, oid: Hashable, b: Box) -> bool:
        found = False
        for i, j in self.cells_of(b):  # @line L8
            bk = self.table[self.bucket(i, j)]
            for k, e in enumerate(bk):
                if e[0] == i and e[1] == j and e[2] == oid and e[3] == b:
                    bk[k] = bk[-1]  # @line L9
                    bk.pop()
                    found = True
                    break
        if found:
            self.size -= 1
        return found

    def close_pairs(self) -> Set[Tuple[Hashable, Hashable]]:
        """All pairs of stored boxes that meet, each once (broad phase)."""
        out: Set[Tuple[Hashable, Hashable]] = set()
        for bk in self.table:
            by_cell: Dict[Tuple[int, int], list] = {}
            for i, j, oid, b in bk:
                by_cell.setdefault((i, j), []).append((oid, b))
            for (i, j), es in by_cell.items():
                for x in range(len(es)):
                    for y in range(x + 1, len(es)):
                        (o1, b1), (o2, b2) = es[x], es[y]
                        if intersects(b1, b2) and self.cell(
                                max(b1[0], b2[0]), max(b1[1], b2[1])) == (i, j):
                            out.add((o1, o2) if repr(o1) <= repr(o2) else (o2, o1))
        return out

    def entry_count(self) -> int:
        return sum(len(bk) for bk in self.table)
