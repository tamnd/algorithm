# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/two-dimensional-segment-tree/. The authors are listed in prov/QYYQT1.jsonl.

import operator
from collections.abc import Callable, Sequence
from typing import Generic, TypeVar

T = TypeVar("T")


class SegmentTree2D(Generic[T]):
    """A segment tree over rows whose nodes are segment trees over columns.

    Outer node vx covers a range of rows and inner node vy a range of
    columns, both numbered as in a binary heap (root 1, children 2v, 2v + 1).
    t[vx][vy] holds the op-product of M over the rows of vx and the columns of
    vy. op must be associative and commutative with the neutral element
    identity. Build takes O(nm) time; query and point assignment take
    O(log n log m) time.
    """

    def __init__(
        self,
        matrix: Sequence[Sequence[T]],
        op: Callable[[T, T], T] = operator.add,  # type: ignore[assignment]
        identity: T = 0,  # type: ignore[assignment]
    ) -> None:
        self.n = len(matrix)
        self.m = len(matrix[0]) if self.n else 0
        if self.n == 0 or self.m == 0:
            raise ValueError("the matrix must have at least one row and one column")
        for row in matrix:
            if len(row) != self.m:
                raise ValueError("all rows must have the same length")
        self.op = op
        self.e = identity
        self.mat = [list(row) for row in matrix]
        self.t: list[list[T]] = [
            [identity] * (4 * self.m) for _ in range(4 * self.n)
        ]
        self._build_x(1, 0, self.n - 1)

    # ----- build -----

    def _build_y(self, vx: int, lx: int, rx: int, vy: int, ly: int, ry: int) -> None:
        t = self.t
        if ly == ry:  # @line L1
            if lx == rx:  # @line L2
                t[vx][vy] = self.mat[lx][ly]
            else:
                t[vx][vy] = self.op(t[2 * vx][vy], t[2 * vx + 1][vy])
            return  # @line L3
        my = (ly + ry) // 2  # @line L4
        self._build_y(vx, lx, rx, 2 * vy, ly, my)
        self._build_y(vx, lx, rx, 2 * vy + 1, my + 1, ry)
        t[vx][vy] = self.op(t[vx][2 * vy], t[vx][2 * vy + 1])  # @line L5

    def _build_x(self, vx: int, lx: int, rx: int) -> None:
        if lx != rx:  # @line L6
            mx = (lx + rx) // 2
            self._build_x(2 * vx, lx, mx)
            self._build_x(2 * vx + 1, mx + 1, rx)
        self._build_y(vx, lx, rx, 1, 0, self.m - 1)  # @line L7

    # ----- query -----

    def _query_y(self, vx: int, vy: int, ly: int, ry: int, c1: int, c2: int) -> T:
        if c2 < ly or ry < c1:  # @line L8
            return self.e
        if c1 <= ly and ry <= c2:  # @line L9
            return self.t[vx][vy]
        my = (ly + ry) // 2  # @line L10
        return self.op(
            self._query_y(vx, 2 * vy, ly, my, c1, c2),
            self._query_y(vx, 2 * vy + 1, my + 1, ry, c1, c2),
        )

    def _query_x(
        self, vx: int, lx: int, rx: int, r1: int, r2: int, c1: int, c2: int
    ) -> T:
        if r2 < lx or rx < r1:  # @line L11
            return self.e
        if r1 <= lx and rx <= r2:  # @line L12
            return self._query_y(vx, 1, 0, self.m - 1, c1, c2)
        mx = (lx + rx) // 2  # @line L13
        return self.op(
            self._query_x(2 * vx, lx, mx, r1, r2, c1, c2),
            self._query_x(2 * vx + 1, mx + 1, rx, r1, r2, c1, c2),
        )

    def query(self, r1: int, c1: int, r2: int, c2: int) -> T:
        """Return the op-product of M[r][c] for r1 <= r <= r2, c1 <= c <= c2.

        An empty rectangle (r1 = r2 + 1 or c1 = c2 + 1) gives the identity.
        """
        if not (0 <= r1 <= r2 + 1 <= self.n and 0 <= c1 <= c2 + 1 <= self.m):
            raise IndexError("rectangle out of range")
        if r1 > r2 or c1 > c2:
            return self.e
        return self._query_x(1, 0, self.n - 1, r1, r2, c1, c2)

    # ----- update -----

    def _update_y(
        self, vx: int, lx: int, rx: int, vy: int, ly: int, ry: int, c: int
    ) -> None:
        t = self.t
        if ly == ry:  # @line L14
            if lx == rx:  # @line L15
                t[vx][vy] = self.mat[lx][ly]
            else:
                t[vx][vy] = self.op(t[2 * vx][vy], t[2 * vx + 1][vy])
            return  # @line L16
        my = (ly + ry) // 2  # @line L17
        if c <= my:
            self._update_y(vx, lx, rx, 2 * vy, ly, my, c)
        else:
            self._update_y(vx, lx, rx, 2 * vy + 1, my + 1, ry, c)
        t[vx][vy] = self.op(t[vx][2 * vy], t[vx][2 * vy + 1])  # @line L18

    def _update_x(self, vx: int, lx: int, rx: int, r: int, c: int) -> None:
        if lx != rx:  # @line L19
            mx = (lx + rx) // 2
            if r <= mx:
                self._update_x(2 * vx, lx, mx, r, c)
            else:
                self._update_x(2 * vx + 1, mx + 1, rx, r, c)
        self._update_y(vx, lx, rx, 1, 0, self.m - 1, c)  # @line L20

    def update(self, r: int, c: int, x: T) -> None:
        """Set M[r][c] = x, for 0 <= r < n and 0 <= c < m."""
        if not (0 <= r < self.n and 0 <= c < self.m):
            raise IndexError("cell out of range")
        self.mat[r][c] = x
        self._update_x(1, 0, self.n - 1, r, c)

    # ----- checks -----

    def _fold(self, r1: int, r2: int, c1: int, c2: int) -> T:
        acc = self.e
        for r in range(r1, r2 + 1):
            for c in range(c1, c2 + 1):
                acc = self.op(acc, self.mat[r][c])
        return acc

    def check_invariant(self) -> None:
        """Assert that each used cell holds the product of its rectangle."""

        def rows(vx: int, lx: int, rx: int) -> None:
            cols(vx, lx, rx, 1, 0, self.m - 1)
            if lx != rx:
                mx = (lx + rx) // 2
                rows(2 * vx, lx, mx)
                rows(2 * vx + 1, mx + 1, rx)

        def cols(vx: int, lx: int, rx: int, vy: int, ly: int, ry: int) -> None:
            assert self.t[vx][vy] == self._fold(lx, rx, ly, ry), (vx, vy)
            if ly != ry:
                my = (ly + ry) // 2
                cols(vx, lx, rx, 2 * vy, ly, my)
                cols(vx, lx, rx, 2 * vy + 1, my + 1, ry)

        rows(1, 0, self.n - 1)
