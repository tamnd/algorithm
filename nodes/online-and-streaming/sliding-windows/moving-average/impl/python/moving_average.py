# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/moving-average/. The authors are listed in prov/G6SM48.jsonl.
"""Simple moving average with a running sum, Neumaier compensation and periodic recomputation."""

import math
from collections import deque
from typing import Iterable, Iterator, List, Optional


class MovingAverage:
    """Average of the last w items.

    compensated: use Neumaier's compensated addition for the running sum.
    recompute: if set, recompute the sum exactly from the buffer every
    `recompute` steps.
    """

    def __init__(self, w: int, compensated: bool = True, recompute: Optional[int] = None) -> None:
        if w < 1:
            raise ValueError("window size must be at least 1")
        if recompute is not None and recompute < 1:
            raise ValueError("recompute period must be at least 1")
        self.w = w
        self.compensated = compensated
        self.recompute = recompute
        self.buf: deque = deque()
        self.t = 0
        self.s = 0.0
        self.c = 0.0

    def _add(self, y: float) -> None:
        if not self.compensated:
            self.s += y
            return
        s = self.s
        u = s + y  # @line L6
        if abs(s) >= abs(y):  # @line L7
            self.c += (s - u) + y
        else:
            self.c += (y - u) + s
        self.s = u  # @line L8

    def step(self, x: float) -> float:
        """Add item x and return the average of the window."""
        self.t += 1  # @line L1
        self.buf.append(x)
        self._add(x)  # @line L2
        if self.t > self.w:  # @line L3
            self._add(-self.buf.popleft())
        if self.recompute and self.t % self.recompute == 0:  # @line L4
            self.s, self.c = math.fsum(self.buf), 0.0
        return (self.s + self.c) / len(self.buf)  # @line L5


def moving_averages(xs: Iterable[float], w: int, **kw) -> Iterator[float]:
    m = MovingAverage(w, **kw)
    for x in xs:
        yield m.step(x)


def integer_moving_sums(xs: Iterable[int], w: int, bits: int = 64) -> Iterator[int]:
    """Window sums with wrapping arithmetic modulo 2**bits, as in fixed-width registers.

    The result is exact whenever the true window sum fits in a signed word,
    because addition modulo 2**bits is a group.
    """
    mask = (1 << bits) - 1
    half = 1 << (bits - 1)
    buf: deque = deque()
    s = 0
    for x in xs:
        buf.append(x)
        s = (s + x) & mask
        if len(buf) > w:
            s = (s - buf.popleft()) & mask
        yield s - (1 << bits) if s >= half else s


def weighted_moving_sums(xs: List[float], w: int) -> Iterator[float]:
    """Numerators sum_j (w - j) x_{t-j} of the linear weighted moving average, in O(1) per step."""
    buf: deque = deque()
    s = 0  # sum of the window
    num = 0  # weighted numerator
    for x in xs:
        # Every item ages by one weight step, and x enters with weight w.
        num += w * x - s
        s += x
        if len(buf) == w:
            s -= buf.popleft()
        buf.append(x)
        yield num
