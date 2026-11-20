# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/linked-cell-list/. The authors are listed in prov/4RS32Z.jsonl.

import itertools
import math

Point = list[float]


def minimum_image_dist2(a: Point, b: Point, box: float) -> float:
    """Squared distance from a to the nearest periodic image of b in a cubic box of side box."""
    s = 0.0
    for x, y in zip(a, b):
        d = x - y
        d -= box * round(d / box)
        s += d * d
    return s


def half_shell(dim: int) -> list[tuple[int, ...]]:
    """The offsets o in {-1, 0, 1}^dim whose first nonzero entry is positive.

    These are 4 offsets in 2D and 13 in 3D. With the zero offset they cover
    each unordered pair of neighboring cells once.
    """
    out = []
    for o in itertools.product((-1, 0, 1), repeat=dim):
        nz = [v for v in o if v != 0]
        if nz and nz[0] > 0:
            out.append(o)
    return out


class CellList:
    """A linked-cell list of the atoms in a periodic cubic box of side box.

    The box is cut into s cells per side, with s = floor(box / rc), so each
    cell has side box / s >= rc. head[c] is the last atom put in cell c, or -1,
    and nxt[i] is the atom after i in the chain of its cell, or -1.
    """

    def __init__(self, positions: list[Point], box: float, rc: float) -> None:
        self.dim = len(positions[0]) if positions else 3
        self.box, self.rc = box, rc
        self.s = int(math.floor(box / rc))  # @line L1
        if self.s < 3:
            raise ValueError("the box must hold at least 3 cells of side rc per side")
        self.side = box / self.s  # @line L1
        self.positions = positions
        self.head = [-1] * (self.s ** self.dim)  # @line L2
        self.nxt = [-1] * len(positions)  # @line L2
        self.cell_of = [0] * len(positions)
        for i, r in enumerate(positions):  # @line L3
            c = self.cell_index(self.cell_coords(r))  # @line L4
            self.cell_of[i] = c
            self.nxt[i] = self.head[c]  # @line L5
            self.head[c] = i  # @line L5

    def cell_coords(self, r: Point) -> tuple[int, ...]:
        """The integer cell coordinates of r, after wrapping r into [0, box)."""
        out = []
        for x in r:
            k = int(math.floor((x % self.box) / self.side))
            out.append(min(max(k, 0), self.s - 1))
        return tuple(out)

    def cell_index(self, k: tuple[int, ...]) -> int:
        c = 0
        for v in reversed(k):
            c = c * self.s + v
        return c

    def chain(self, c: int) -> list[int]:
        """The atoms of cell c, in chain order (the reverse of insertion order)."""
        out = []
        i = self.head[c]
        while i != -1:
            out.append(i)
            i = self.nxt[i]
        return out

    def pairs(self) -> tuple[list[tuple[int, int]], int]:
        """All pairs i < j at minimum image distance below rc, and the number of distances computed."""
        rc2 = self.rc * self.rc
        shell = half_shell(self.dim)
        found: list[tuple[int, int]] = []
        tests = 0
        for k in itertools.product(range(self.s), repeat=self.dim):  # @line L6
            c = self.cell_index(k)
            mine = self.chain(c)
            for o in [(0,) * self.dim] + shell:  # @line L7
                c2 = self.cell_index(tuple((a + b) % self.s for a, b in zip(k, o)))  # @line L8
                other = mine if c2 == c else self.chain(c2)
                for a, i in enumerate(mine):  # @line L9
                    start = a + 1 if c2 == c else 0
                    for j in other[start:]:  # @line L10
                        tests += 1
                        d2 = minimum_image_dist2(self.positions[i], self.positions[j], self.box)
                        if d2 < rc2:  # @line L11
                            found.append((min(i, j), max(i, j)))  # @line L11
        return found, tests


def cell_list_pairs(positions: list[Point], box: float, rc: float) -> list[tuple[int, int]]:
    """The sorted list of pairs i < j closer than rc under the minimum image rule."""
    return sorted(CellList(positions, box, rc).pairs()[0])
