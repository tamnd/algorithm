# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/corner-table/. The authors are listed in prov/FBTW3E.jsonl.

"""The corner table of Rossignac: a triangle mesh as two integer arrays V and O.

Corner c = 3t + k is corner k of triangle t. V[c] is its vertex and O[c] is the
opposite corner, the corner of the neighbouring triangle across the edge that
does not touch c, or -1 on a border. The mesh must be oriented consistently
and every edge must have one or two triangles.
"""

from typing import Iterator, Sequence


def next_corner(c: int) -> int:
    """The next corner in the same triangle."""
    return 3 * (c // 3) + (c + 1) % 3  # @line L10


def prev_corner(c: int) -> int:
    """The previous corner in the same triangle."""
    return next_corner(next_corner(c))  # @line L11


def triangle(c: int) -> int:
    return c // 3


class CornerTable:
    """The arrays V and O, and one corner for each vertex."""

    def __init__(self, n_vertices: int, triangles: Sequence[Sequence[int]]) -> None:
        """Build V and O. Raise ValueError if an edge is used twice in one direction."""
        self.V: list[int] = []
        for t in triangles:  # @line L1
            if len(t) != 3 or len(set(t)) != 3:
                raise ValueError(f"not a triangle: {t}")
            self.V.extend(t)
        nc = len(self.V)
        self.O: list[int] = [-1] * nc
        h: dict[tuple[int, int], int] = {}  # @line L2
        for c in range(nc):  # @line L3
            key = (self.V[next_corner(c)], self.V[prev_corner(c)])  # @line L4
            if key in h:  # @line L5
                raise ValueError(f"directed edge {key} is used twice")
            h[key] = c  # @line L6
        for c in range(nc):  # @line L7
            d = h.get((self.V[prev_corner(c)], self.V[next_corner(c)]), -1)  # @line L8
            self.O[c] = d  # @line L9
        self.C: list[int] = [-1] * n_vertices
        for c in range(nc):
            if self.C[self.V[c]] == -1:
                self.C[self.V[c]] = c

    def opposite(self, c: int) -> int:
        return self.O[c]

    def left(self, c: int) -> int:
        """The corner opposite the edge from V[c] to V[prev(c)], seen from c."""
        return self.O[next_corner(c)]

    def right(self, c: int) -> int:
        return self.O[prev_corner(c)]

    def swing(self, c: int) -> int:
        """The corner of the same vertex in the next triangle counterclockwise, or -1."""
        d = self.O[next_corner(c)]  # @line L12
        return -1 if d == -1 else next_corner(d)

    def unswing(self, c: int) -> int:
        """The corner of the same vertex in the next triangle clockwise, or -1."""
        d = self.O[prev_corner(c)]
        return -1 if d == -1 else prev_corner(d)

    def ring(self, c: int) -> list[int]:
        """The corners of the fan of V[c] that contains c, in counterclockwise order.

        For an inner vertex the list starts at c. For a border vertex it starts
        at the most clockwise triangle.
        """
        start = c
        while True:  # @line L13
            u = self.unswing(start)
            if u == c:
                start = c
                break
            if u == -1:
                break
            start = u
        out = [start]
        x = self.swing(start)  # @line L14
        while x != -1 and x != start:
            out.append(x)
            x = self.swing(x)
        return out

    def vertex_neighbors(self, v: int) -> list[int]:
        """The neighbours of v in counterclockwise order (for one fan)."""
        if self.C[v] == -1:
            return []
        r = self.ring(self.C[v])
        out = [self.V[next_corner(c)] for c in r]
        if self.unswing(r[0]) == -1:  # border vertex: add the last neighbour
            out.append(self.V[prev_corner(r[-1])])
        return out

    def border_corners(self) -> Iterator[int]:
        """Corners whose opposite edge is a border edge."""
        return (c for c in range(len(self.V)) if self.O[c] == -1)
