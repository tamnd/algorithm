# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/spatial-occupancy-enumeration/. The authors are listed in prov/F2JK2W.jsonl.

"""Spatial occupancy enumeration: a solid as a set of closed unit cells.

The cell (i, j, k) is the closed cube [i, i+1] x [j, j+1] x [k, k+1], and a
voxel set V stands for the union of its cells. Such a union is always a closed
regular set, and the set operations on the cells are the regularized set
operations on the solids. All tests are exact on integer and Fraction points.

The octree functions convert a voxel set inside the cube [0, 2^d)^3 to an
octree and back, and combine two octrees with a Boolean operation.
"""

from __future__ import annotations

import itertools
from fractions import Fraction
from typing import Callable, Iterable, Sequence, Union

Cell = tuple[int, int, int]
IN, ON, OUT = "in", "on", "out"
EMPTY, FULL = "E", "F"
Octree = Union[str, tuple]  # EMPTY, FULL, or a tuple of 8 children

NEIGHBOURS = ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))
UNION = lambda a, b: a or b  # noqa: E731
INTERSECTION = lambda a, b: a and b  # noqa: E731
DIFFERENCE = lambda a, b: a and not b  # noqa: E731


class VoxelSet:
    def __init__(self, cells: Iterable[Cell] = ()) -> None:
        self.cells: set[Cell] = {tuple(c) for c in cells}  # type: ignore[misc]

    @staticmethod
    def from_membership(inside: Callable[[tuple], bool], lo: Sequence[int], hi: Sequence[int]) -> "VoxelSet":
        """Sample a solid at the centre of each cell of the box [lo, hi)."""
        h = Fraction(1, 2)
        return VoxelSet(c for c in itertools.product(*(range(lo[j], hi[j]) for j in range(3)))
                        if inside((c[0] + h, c[1] + h, c[2] + h)))

    def __eq__(self, other: object) -> bool:
        return isinstance(other, VoxelSet) and self.cells == other.cells

    def __len__(self) -> int:
        return len(self.cells)

    # ----- the regularized operations are the set operations on cells -----

    def boolean(self, other: "VoxelSet", op: Callable[[bool, bool], bool]) -> "VoxelSet":
        return VoxelSet(c for c in self.cells | other.cells
                        if op(c in self.cells, c in other.cells))  # @line L6

    def union(self, other: "VoxelSet") -> "VoxelSet":
        return self.boolean(other, UNION)

    def intersection(self, other: "VoxelSet") -> "VoxelSet":
        return self.boolean(other, INTERSECTION)

    def difference(self, other: "VoxelSet") -> "VoxelSet":
        return self.boolean(other, DIFFERENCE)

    # ----- queries -----

    def classify(self, p: Sequence) -> str:
        """IN, ON or OUT for the closed union of the cells."""
        ranges = []
        for x in p:  # @line L1
            f = int(x // 1)
            ranges.append((f - 1, f) if x == f else (f,))
        around = list(itertools.product(*ranges))
        k = sum(1 for c in around if c in self.cells)  # @line L2
        if k == 0:  # @line L3
            return OUT
        if k == len(around):  # @line L4
            return IN
        return ON  # @line L5

    def volume(self) -> int:
        return len(self.cells)

    def area(self) -> int:
        """The number of unit squares between a cell of V and a cell not in V."""
        return sum(1 for c in self.cells for d in NEIGHBOURS
                   if (c[0] + d[0], c[1] + d[1], c[2] + d[2]) not in self.cells)


# ----- octrees -----

def to_octree(v: VoxelSet, depth: int) -> Octree:
    """The octree of v inside the cube [0, 2^depth)^3; cells outside it are an error."""
    side = 1 << depth
    for c in v.cells:
        if not all(0 <= x < side for x in c):
            raise ValueError("a cell is outside the cube of the octree")
    return _build(list(v.cells), (0, 0, 0), side)


def _child_corner(corner: Cell, half: int, i: int) -> Cell:
    return tuple(corner[j] + half * (i >> j & 1) for j in range(3))  # type: ignore[return-value]


def _build(cells: list[Cell], corner: Cell, side: int) -> Octree:
    if not cells:  # @line L7
        return EMPTY
    if len(cells) == side ** 3:  # @line L8
        return FULL
    half = side // 2  # @line L9
    parts: list[list[Cell]] = [[] for _ in range(8)]
    for c in cells:
        parts[sum(1 << j for j in range(3) if c[j] >= corner[j] + half)].append(c)
    return tuple(_build(parts[i], _child_corner(corner, half, i), half) for i in range(8))


def from_octree(t: Octree, depth: int) -> VoxelSet:
    out: set[Cell] = set()

    def walk(t: Octree, corner: Cell, side: int) -> None:
        if t == EMPTY:
            return
        if t == FULL:
            out.update(itertools.product(*(range(corner[j], corner[j] + side) for j in range(3))))
            return
        half = side // 2
        for i in range(8):
            walk(t[i], _child_corner(corner, half, i), half)

    walk(t, (0, 0, 0), 1 << depth)
    return VoxelSet(out)


def octree_boolean(a: Octree, b: Octree, op: Callable[[bool, bool], bool]) -> Octree:
    """Combine two octrees of the same cube in time linear in their sizes."""
    if isinstance(a, str) and isinstance(b, str):
        return FULL if op(a == FULL, b == FULL) else EMPTY
    ka = a if isinstance(a, tuple) else (a,) * 8
    kb = b if isinstance(b, tuple) else (b,) * 8
    kids = tuple(octree_boolean(x, y, op) for x, y in zip(ka, kb))
    if all(k == EMPTY for k in kids):
        return EMPTY
    if all(k == FULL for k in kids):
        return FULL
    return kids


def octree_size(t: Octree) -> int:
    return 1 if isinstance(t, str) else 1 + sum(octree_size(k) for k in t)
