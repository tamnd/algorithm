# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/grid-file/. The authors are listed in prov/0WX5ZW.jsonl.

from bisect import bisect_right, insort

Point = tuple[int, int]


class Bucket:
    """A bucket of at most B points. Its region is the box of grid cells
    with columns c0 to c1 - 1 and rows r0 to r1 - 1."""

    __slots__ = ("points", "c0", "c1", "r0", "r1")

    def __init__(self, c0: int, c1: int, r0: int, r1: int) -> None:
        self.points: list[Point] = []
        self.c0, self.c1, self.r0, self.r1 = c0, c1, r0, r1


class GridFile:
    """A two-dimensional grid file with bucket capacity B.

    The scales xs and ys are sorted lists of split values: column c holds the
    x with c = bisect_right(xs, x), and rows are the same with ys. The directory
    grid[c][r] names the bucket of each cell. Invariant: the regions of the
    buckets are boxes of cells that partition the grid, the directory agrees
    with them, each point lies in a cell of its bucket's region, and each
    bucket holds at most B points.
    """

    def __init__(self, capacity: int = 2) -> None:
        if capacity < 1:
            raise ValueError("need capacity >= 1")
        self.capacity = capacity
        self.xs: list[int] = []
        self.ys: list[int] = []
        first = Bucket(0, 1, 0, 1)
        self.buckets: list[Bucket] = [first]
        self.grid: list[list[Bucket]] = [[first]]
        self.size = 0

    def __len__(self) -> int:
        return self.size

    def cell(self, p: Point) -> tuple[int, int]:
        return bisect_right(self.xs, p[0]), bisect_right(self.ys, p[1])

    def bucket_of(self, p: Point) -> Bucket:
        """The bucket whose region holds p: two binary searches and one directory read."""
        c = bisect_right(self.xs, p[0])  # @line L1
        r = bisect_right(self.ys, p[1])  # @line L2
        return self.grid[c][r]  # @line L3

    def __contains__(self, p: Point) -> bool:
        p = (int(p[0]), int(p[1]))
        return p in self.bucket_of(p).points

    def insert(self, p: Point) -> bool:
        """Add p. Returns False if p was stored."""
        p = (int(p[0]), int(p[1]))
        b = self.bucket_of(p)  # @line L4
        if p in b.points:
            return False
        b.points.append(p)  # @line L5
        self.size += 1
        while len(b.points) > self.capacity:  # @line L6
            if b.c1 - b.c0 > 1 or b.r1 - b.r0 > 1:  # @line L7
                axis = 0 if b.c1 - b.c0 >= b.r1 - b.r0 else 1
                at = (b.c0 + b.c1) // 2 if axis == 0 else (b.r0 + b.r1) // 2  # @line L8
            else:
                axis, at = self._refine(b)  # @line L9
            b = self._split(b, axis, at)  # @line L10
        return True  # @line L11

    def _refine(self, b: Bucket) -> tuple[int, int]:
        """Add a split value inside the single cell of b, between its points; return the new line.

        The axis is the one with fewer split values so far, if the points of b
        differ on it, with x first on a tie; the value is the median of the
        distinct coordinates, so both sides get a point.
        """
        dx = sorted({q[0] for q in b.points})
        dy = sorted({q[1] for q in b.points})
        if len(dy) < 2 or (len(dx) >= 2 and len(self.xs) <= len(self.ys)):
            v = dx[len(dx) // 2]
            insort(self.xs, v)
            c = b.c0
            self.grid.insert(c + 1, list(self.grid[c]))
            for u in self.buckets:
                if u.c0 > c:
                    u.c0 += 1
                if u.c1 > c:
                    u.c1 += 1
            return 0, c + 1
        v = dy[len(dy) // 2]
        insort(self.ys, v)
        r = b.r0
        for col in self.grid:
            col.insert(r + 1, col[r])
        for u in self.buckets:
            if u.r0 > r:
                u.r0 += 1
            if u.r1 > r:
                u.r1 += 1
        return 1, r + 1

    def _split(self, b: Bucket, axis: int, at: int) -> Bucket:
        """Split b at the grid line at, on the axis; return the half that holds the most points."""
        if axis == 0:
            nb = Bucket(at, b.c1, b.r0, b.r1)
            b.c1 = at
            cut = self.xs[at - 1]
            keep = [q for q in b.points if q[0] < cut]
            nb.points = [q for q in b.points if q[0] >= cut]
        else:
            nb = Bucket(b.c0, b.c1, at, b.r1)
            b.r1 = at
            cut = self.ys[at - 1]
            keep = [q for q in b.points if q[1] < cut]
            nb.points = [q for q in b.points if q[1] >= cut]
        b.points = keep
        self.buckets.append(nb)
        for c in range(nb.c0, nb.c1):
            for r in range(nb.r0, nb.r1):
                self.grid[c][r] = nb
        return b if len(b.points) >= len(nb.points) else nb

    def delete(self, p: Point) -> bool:
        """Remove p, then merge its bucket with a neighbor if their union is a box that fits."""
        p = (int(p[0]), int(p[1]))
        b = self.bucket_of(p)  # @line L12
        if p not in b.points:
            return False
        b.points.remove(p)  # @line L13
        self.size -= 1
        for u in self.buckets:  # @line L14
            if u is b or len(u.points) + len(b.points) > self.capacity:
                continue
            same_rows = (u.r0, u.r1) == (b.r0, b.r1) and (u.c1 == b.c0 or u.c0 == b.c1)
            same_cols = (u.c0, u.c1) == (b.c0, b.c1) and (u.r1 == b.r0 or u.r0 == b.r1)
            if same_rows or same_cols:
                b.points.extend(u.points)
                b.c0, b.c1 = min(b.c0, u.c0), max(b.c1, u.c1)
                b.r0, b.r1 = min(b.r0, u.r0), max(b.r1, u.r1)
                for c in range(u.c0, u.c1):
                    for r in range(u.r0, u.r1):
                        self.grid[c][r] = b
                self.buckets.remove(u)
                break
        return True

    def range_search(self, lo: Point, hi: Point) -> list[Point]:
        """The points in the closed box [lo, hi], reading each bucket of the cells it meets once."""
        c0, r0 = self.cell(lo)  # @line L15
        c1, r1 = self.cell(hi)
        seen: set[int] = set()
        out: list[Point] = []
        for c in range(c0, c1 + 1):  # @line L16
            for r in range(r0, r1 + 1):
                b = self.grid[c][r]
                if id(b) in seen:
                    continue
                seen.add(id(b))
                out.extend(q for q in b.points if lo[0] <= q[0] <= hi[0] and lo[1] <= q[1] <= hi[1])  # @line L17
        return out

    def points(self) -> list[Point]:
        return [q for b in self.buckets for q in b.points]

    def check_invariant(self) -> None:
        nc, nr = len(self.xs) + 1, len(self.ys) + 1
        assert self.xs == sorted(set(self.xs)) and self.ys == sorted(set(self.ys)), "scales not sorted"
        assert len(self.grid) == nc and all(len(col) == nr for col in self.grid), "directory has the wrong size"
        owner: dict[tuple[int, int], Bucket] = {}
        total = 0
        for b in self.buckets:
            assert 0 <= b.c0 < b.c1 <= nc and 0 <= b.r0 < b.r1 <= nr, "bad region"
            assert len(b.points) <= self.capacity, "bucket overflow"
            total += len(b.points)
            for c in range(b.c0, b.c1):
                for r in range(b.r0, b.r1):
                    assert (c, r) not in owner, "regions overlap"
                    owner[(c, r)] = b
                    assert self.grid[c][r] is b, "directory disagrees"
            for q in b.points:
                c, r = self.cell(q)
                assert b.c0 <= c < b.c1 and b.r0 <= r < b.r1, "point outside its region"
        assert len(owner) == nc * nr, "regions do not cover the grid"
        assert total == self.size and len(set(self.points())) == total, "size is wrong"
