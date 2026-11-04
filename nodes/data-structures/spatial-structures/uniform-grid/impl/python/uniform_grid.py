# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/uniform-grid/. The authors are listed in prov/F5M3BP.jsonl.

import math

Point = tuple[float, float]


class UniformGrid:
    """A uniform grid of nx by ny square cells of side h over the box
    [x0, x0 + nx*h) x [y0, y0 + ny*h).

    Cell (i, j) is the half-open square [x0 + i*h, x0 + (i+1)*h) x
    [y0 + j*h, y0 + (j+1)*h); its bucket is the list cells[j*nx + i].
    Invariant: each stored point is in the bucket of the cell that holds it,
    once per copy (the grid stores a multiset of points).
    Space: O(nx*ny + n).
    """

    def __init__(self, x0: float, y0: float, h: float, nx: int, ny: int) -> None:
        if h <= 0 or nx < 1 or ny < 1:
            raise ValueError("need h > 0, nx >= 1 and ny >= 1")
        self.x0, self.y0, self.h, self.nx, self.ny = x0, y0, h, nx, ny
        self.cells: list[list[Point]] = [[] for _ in range(nx * ny)]
        self.n = 0

    def __len__(self) -> int:
        return self.n

    def cell_of(self, p: Point) -> tuple[int, int]:
        """The cell (i, j) that holds p. O(1). Raises ValueError outside the box."""
        i = math.floor((p[0] - self.x0) / self.h)
        j = math.floor((p[1] - self.y0) / self.h)
        if not (0 <= i < self.nx and 0 <= j < self.ny):
            raise ValueError("the point is outside the grid")
        return i, j

    def insert(self, p: Point) -> None:
        """Add one copy of p. O(1)."""
        i, j = self.cell_of(p)  # @line L9
        self.cells[j * self.nx + i].append(p)  # @line L10
        self.n += 1

    def delete(self, p: Point) -> bool:
        """Remove one copy of p; return False if p is not stored. O(1 + size of its bucket)."""
        i, j = self.cell_of(p)  # @line L11
        bucket = self.cells[j * self.nx + i]
        if p not in bucket:  # @line L12
            return False
        bucket.remove(p)  # @line L13
        self.n -= 1
        return True

    def radius_query(self, q: Point, r: float) -> list[Point]:
        """All stored points p with |p - q| <= r (Euclidean), q anywhere.

        Scans the cells that meet the square [q - r, q + r]^2, so the cost is
        O((2*ceil(r/h) + 1)^2 + the number of points in those cells).
        """
        if r < 0:
            return []
        h = self.h
        i0 = max(0, math.floor((q[0] - r - self.x0) / h))  # @line L1
        i1 = min(self.nx - 1, math.floor((q[0] + r - self.x0) / h))
        j0 = max(0, math.floor((q[1] - r - self.y0) / h))
        j1 = min(self.ny - 1, math.floor((q[1] + r - self.y0) / h))
        out: list[Point] = []  # @line L2
        rr = r * r
        for j in range(j0, j1 + 1):  # @line L3
            for i in range(i0, i1 + 1):
                for p in self.cells[j * self.nx + i]:  # @line L4
                    dx, dy = p[0] - q[0], p[1] - q[1]
                    if dx * dx + dy * dy <= rr:  # @line L5
                        out.append(p)
        return out  # @line L6

    def close_pairs(self) -> list[tuple[Point, Point]]:
        """All unordered pairs of stored copies at distance at most h.

        Each cell is paired with itself and with four of its neighbors
        (east, north-east, north, north-west), so each pair of cells is
        examined once. O(nx*ny + n + K) for K pairs at distance at most h.
        """
        out: list[tuple[Point, Point]] = []
        hh = self.h * self.h
        nx, ny = self.nx, self.ny
        for j in range(ny):  # @line L14
            for i in range(nx):
                a = self.cells[j * nx + i]
                for s in range(len(a)):  # @line L15: pairs inside the cell
                    for t in range(s + 1, len(a)):
                        if _d2(a[s], a[t]) <= hh:
                            out.append((a[s], a[t]))
                for di, dj in ((1, 0), (1, 1), (0, 1), (-1, 1)):  # @line L16
                    ii, jj = i + di, j + dj
                    if 0 <= ii < nx and jj < ny:
                        b = self.cells[jj * nx + ii]
                        for p in a:  # @line L17
                            for p2 in b:
                                if _d2(p, p2) <= hh:
                                    out.append((p, p2))
        return out

    def points(self) -> list[Point]:
        """All stored copies. O(nx*ny + n)."""
        return [p for c in self.cells for p in c]

    def check_invariant(self) -> None:
        """Raise AssertionError if a point is in the wrong bucket or the count is wrong."""
        total = 0
        for k, c in enumerate(self.cells):
            for p in c:
                i, j = self.cell_of(p)
                assert j * self.nx + i == k
            total += len(c)
        assert total == self.n


def _d2(a: Point, b: Point) -> float:
    dx, dy = a[0] - b[0], a[1] - b[1]
    return dx * dx + dy * dy
