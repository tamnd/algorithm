# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/interval-branch-and-bound/. The authors are listed in prov/AGSJXC.jsonl.
"""Interval branch and bound for global minimization over a box.

All arithmetic is exact, with fractions, so the interval bounds need no
outward rounding. The objective is a Python function that works both on
numbers and on Interval objects: on numbers it gives f, on intervals it gives
the natural interval extension F.
"""

from __future__ import annotations

import heapq
from fractions import Fraction
from typing import Callable, Optional, Sequence, Union

Num = Union[int, Fraction]


class Interval:
    """A closed interval [lo, hi] of rationals."""

    __slots__ = ("lo", "hi")

    def __init__(self, lo: Num, hi: Optional[Num] = None) -> None:
        self.lo = Fraction(lo)
        self.hi = Fraction(lo if hi is None else hi)
        if self.lo > self.hi:
            raise ValueError("empty interval")

    @staticmethod
    def of(x: Union["Interval", Num]) -> "Interval":
        return x if isinstance(x, Interval) else Interval(x)

    def __add__(self, other: Union["Interval", Num]) -> "Interval":
        o = Interval.of(other)
        return Interval(self.lo + o.lo, self.hi + o.hi)

    __radd__ = __add__

    def __neg__(self) -> "Interval":
        return Interval(-self.hi, -self.lo)

    def __sub__(self, other: Union["Interval", Num]) -> "Interval":
        return self + (-Interval.of(other))

    def __rsub__(self, other: Num) -> "Interval":
        return Interval.of(other) + (-self)

    def __mul__(self, other: Union["Interval", Num]) -> "Interval":
        o = Interval.of(other)
        p = (self.lo * o.lo, self.lo * o.hi, self.hi * o.lo, self.hi * o.hi)
        return Interval(min(p), max(p))

    __rmul__ = __mul__

    def __pow__(self, k: int) -> "Interval":
        """Power with a nonnegative integer exponent; even powers are not below 0."""
        if k < 0:
            raise ValueError("negative exponent")
        if k == 0:
            return Interval(1)
        a, b = self.lo ** k, self.hi ** k
        if k % 2 == 1:
            return Interval(a, b)
        if self.lo <= 0 <= self.hi:
            return Interval(0, max(a, b))
        return Interval(min(a, b), max(a, b))

    def __repr__(self) -> str:
        return "[%s, %s]" % (self.lo, self.hi)


Box = tuple[tuple[Fraction, Fraction], ...]


def width(box: Box) -> Fraction:
    return max(hi - lo for lo, hi in box)


def midpoint(box: Box) -> list[Fraction]:
    return [(lo + hi) / 2 for lo, hi in box]


def lower(func: Callable, box: Box) -> Fraction:
    return Interval.of(func([Interval(lo, hi) for lo, hi in box])).lo


def interval_branch_and_bound(
    func: Callable,
    box: Sequence[tuple[Num, Num]],
    eps: Num,
    stats: Optional[dict[str, int]] = None,
) -> tuple[Fraction, Fraction, list[Fraction], list[tuple[Fraction, Box]]]:
    """Enclose the global minimum of func over box.

    Return (lo, ub, xbest, boxes): lo <= min f <= ub = f(xbest), and every
    global minimizer lies in one of the boxes, each given with its lower bound.
    Every returned box has width at most eps.
    """
    eps = Fraction(eps)
    if eps <= 0:
        raise ValueError("eps must be positive")
    x0: Box = tuple((Fraction(lo), Fraction(hi)) for lo, hi in box)
    if stats is not None:
        stats.update(boxes=1, split=0)
    xbest = midpoint(x0)  # @line L1
    ub = Fraction(func(xbest))
    heap: list[tuple[Fraction, int, Box]] = [(lower(func, x0), 0, x0)]
    tick = 0
    result: list[tuple[Fraction, Box]] = []
    while heap:  # @line L2
        b, _, y = heapq.heappop(heap)  # @line L3
        if b > ub:  # @line L4
            break
        if width(y) <= eps:  # @line L5
            result.append((b, y))
            continue
        if stats is not None:
            stats["split"] += 1
        k = max(range(len(y)), key=lambda i: (y[i][1] - y[i][0], -i))  # @line L6
        lo, hi = y[k]
        mid = (lo + hi) / 2
        halves = (y[:k] + ((lo, mid),) + y[k + 1:], y[:k] + ((mid, hi),) + y[k + 1:])
        for z in halves:  # @line L7
            xm = midpoint(z)
            fm = Fraction(func(xm))
            if fm < ub:  # @line L8
                ub, xbest = fm, xm
            bz = lower(func, z)
            if bz <= ub:  # @line L9
                tick += 1
                heapq.heappush(heap, (bz, tick, z))
                if stats is not None:
                    stats["boxes"] += 1
    result = [(b, y) for b, y in result if b <= ub]  # @line L10
    return min(b for b, _ in result), ub, xbest, result
