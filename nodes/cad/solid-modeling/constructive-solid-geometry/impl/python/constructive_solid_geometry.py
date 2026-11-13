# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/constructive-solid-geometry/. The authors are listed in prov/QD8QB3.jsonl.

"""A CSG tree of axis-aligned boxes with regularized point membership.

The leaves are closed boxes with integer corners. The inner nodes are union,
intersection, difference and rigid motions that keep the axes: a rotation by
quarter turns (a signed permutation matrix with determinant 1) followed by an
integer translation. The tree describes the regularized result.

CLASSIFY(p) returns IN, ON or OUT for the regularized solid at any point with
integer or Fraction coordinates. It evaluates the tree at p + e*s for the 8
directions s in {-1, +1}^3 and all small e > 0 at once. All planes of all
leaves are axis planes, so each of these 8 open octants at p lies wholly inside
or wholly outside each leaf, and the ordinary set operations on the octants
give the regularized result.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Sequence, Union as TUnion

Num = TUnion[int, Fraction]
ALL = 0xFF  # the 8 octants
IN, ON, OUT = "in", "on", "out"


def octant(i: int) -> tuple[int, int, int]:
    """The direction s of octant i: bit j of i says s_j = +1."""
    return tuple(1 if i >> j & 1 else -1 for j in range(3))  # type: ignore[return-value]


def index(s: Sequence[int]) -> int:
    return sum(1 << j for j in range(3) if s[j] > 0)


class Node:
    def mask(self, p: Sequence[Num]) -> int:
        raise NotImplementedError

    def classify(self, p: Sequence[Num]) -> str:
        m = self.mask(p)  # @line L7
        if m == 0:  # @line L8
            return OUT
        if m == ALL:  # @line L9
            return IN
        return ON  # @line L10

    def raw(self, p: Sequence[Num]) -> bool:
        """The ordinary, not regularized, membership of p in the closed sets."""
        raise NotImplementedError

    def bound(self) -> tuple[tuple[int, ...], tuple[int, ...]]:
        """A box that contains the solid."""
        raise NotImplementedError

    def __or__(self, other: "Node") -> "Node":
        return Op("union", self, other)

    def __and__(self, other: "Node") -> "Node":
        return Op("intersection", self, other)

    def __sub__(self, other: "Node") -> "Node":
        return Op("difference", self, other)


class Box(Node):
    def __init__(self, lo: Sequence[int], hi: Sequence[int]) -> None:
        if any(a >= b for a, b in zip(lo, hi)):
            raise ValueError("a box needs lo < hi on every axis")
        self.lo, self.hi = tuple(lo), tuple(hi)

    def mask(self, p: Sequence[Num]) -> int:
        m = ALL  # @line L1
        for j in range(3):
            if p[j] == self.lo[j]:
                m &= sum(1 << i for i in range(8) if i >> j & 1)  # only s_j = +1 enters the box
            elif p[j] == self.hi[j]:
                m &= sum(1 << i for i in range(8) if not i >> j & 1)  # only s_j = -1
            elif not self.lo[j] < p[j] < self.hi[j]:
                return 0
        return m

    def raw(self, p: Sequence[Num]) -> bool:
        return all(self.lo[j] <= p[j] <= self.hi[j] for j in range(3))

    def bound(self):
        return self.lo, self.hi


class Op(Node):
    def __init__(self, kind: str, a: Node, b: Node) -> None:
        if kind not in ("union", "intersection", "difference"):
            raise ValueError(kind)
        self.kind, self.a, self.b = kind, a, b

    def mask(self, p: Sequence[Num]) -> int:
        ma, mb = self.a.mask(p), self.b.mask(p)  # @line L3
        if self.kind == "union":
            return ma | mb  # @line L4
        if self.kind == "intersection":
            return ma & mb  # @line L5
        return ma & ~mb & ALL  # @line L6

    def raw(self, p: Sequence[Num]) -> bool:
        a, b = self.a.raw(p), self.b.raw(p)
        if self.kind == "union":
            return a or b
        if self.kind == "intersection":
            return a and b
        return a and not b

    def bound(self):
        (alo, ahi), (blo, bhi) = self.a.bound(), self.b.bound()
        if self.kind == "union":
            return tuple(map(min, alo, blo)), tuple(map(max, ahi, bhi))
        if self.kind == "intersection":
            lo, hi = tuple(map(max, alo, blo)), tuple(map(min, ahi, bhi))
            if any(x > y for x, y in zip(lo, hi)):
                return alo, alo  # empty: any degenerate box will do
            return lo, hi
        return alo, ahi


def rotation(axis: int, quarter_turns: int) -> tuple[tuple[int, ...], ...]:
    """The matrix of a rotation by quarter_turns * 90 degrees about an axis, counterclockwise."""
    r = [[1 if i == j else 0 for j in range(3)] for i in range(3)]
    b, c = (axis + 1) % 3, (axis + 2) % 3
    for _ in range(quarter_turns % 4):
        # multiply on the right by the quarter turn e_b -> e_c, e_c -> -e_b
        new = [row[:] for row in r]
        for i in range(3):
            new[i][b] = r[i][c]
            new[i][c] = -r[i][b]
        r = new
    return tuple(tuple(row) for row in r)


def mat_vec(r, v):
    return tuple(sum(r[i][j] * v[j] for j in range(3)) for i in range(3))


def transpose(r):
    return tuple(tuple(r[j][i] for j in range(3)) for i in range(3))


class Move(Node):
    """The set {R x + t : x in child}, R a rotation by quarter turns and t an integer vector."""

    def __init__(self, child: Node, r=None, t: Sequence[int] = (0, 0, 0)) -> None:
        self.child = child
        self.r = r if r is not None else rotation(0, 0)
        self.rt = transpose(self.r)
        self.t = tuple(t)
        self.perm = [index(mat_vec(self.rt, octant(i))) for i in range(8)]

    def _back(self, p):
        return mat_vec(self.rt, tuple(p[j] - self.t[j] for j in range(3)))

    def mask(self, p: Sequence[Num]) -> int:
        m = self.child.mask(self._back(p))  # @line L2
        return sum(1 << i for i in range(8) if m >> self.perm[i] & 1)

    def raw(self, p: Sequence[Num]) -> bool:
        return self.child.raw(self._back(p))

    def bound(self):
        lo, hi = self.child.bound()
        a, b = mat_vec(self.r, lo), mat_vec(self.r, hi)
        return (tuple(min(x, y) + t for x, y, t in zip(a, b, self.t)),
                tuple(max(x, y) + t for x, y, t in zip(a, b, self.t)))


def neighbourhood(node: Node, p: Sequence[Num]) -> list[tuple[int, int, int]]:
    """The octant directions at p that are inside the regularized solid."""
    m = node.mask(p)
    return [octant(i) for i in range(8) if m >> i & 1]
