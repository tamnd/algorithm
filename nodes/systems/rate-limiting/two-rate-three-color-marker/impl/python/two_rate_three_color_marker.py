# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/two-rate-three-color-marker/. The authors are listed in prov/2FQ2DX.jsonl.

"""Two rate three color marker, trTCM (RFC 2698, Heinanen and Guerin 1999).

Two independent token buckets: P fills at the peak rate PIR up to PBS, and
C fills at the committed rate CIR up to CBS. A packet of B bytes is red if
P holds fewer than B tokens, else yellow if C holds fewer than B tokens,
else green. A green packet takes B tokens from both buckets, a yellow
packet takes B tokens from P only, and a red packet takes nothing.

Time is an explicit number (int or Fraction) that the caller passes in, and
it must not go back. The refill is lazy and exact.
"""

from fractions import Fraction
from typing import Optional, Union

Number = Union[int, Fraction]

GREEN = "green"
YELLOW = "yellow"
RED = "red"
COLORS = (GREEN, YELLOW, RED)


class TwoRateThreeColorMarker:
    """trTCM in color-blind mode (default) or color-aware mode."""

    def __init__(
        self,
        pir: Number,
        pbs: Number,
        cir: Number,
        cbs: Number,
        color_aware: bool = False,
        start: Number = 0,
    ) -> None:
        if cir <= 0 or pir < cir:
            raise ValueError("need 0 < CIR <= PIR")
        if pbs <= 0 or cbs <= 0:
            raise ValueError("PBS and CBS must be positive")
        self.pir, self.pbs = pir, pbs
        self.cir, self.cbs = cir, cbs
        self.color_aware = color_aware
        self.tp: Number = pbs  # both buckets are full at the start
        self.tc: Number = cbs
        self.last: Number = start

    def refill(self, t: Number) -> None:
        """Bring both token counts up to time t; the buckets are independent."""
        if t < self.last:
            raise ValueError("time went back")
        self.tp = min(self.pbs, self.tp + self.pir * (t - self.last))  # @line L1
        self.tc = min(self.cbs, self.tc + self.cir * (t - self.last))  # @line L2
        self.last = t  # @line L3

    def meter(self, t: Number, size: Number, precolor: Optional[str] = None) -> str:
        """Color a packet of `size` bytes that arrives at time t.

        In color-blind mode the precolor is ignored. In color-aware mode it
        must be one of GREEN, YELLOW and RED.
        """
        if size <= 0:
            raise ValueError("packet size must be positive")
        pre = GREEN
        if self.color_aware:
            if precolor not in COLORS:
                raise ValueError("color-aware mode needs a precolor")
            pre = precolor
        self.refill(t)
        if pre == RED or self.tp - size < 0:  # @line L4
            return RED  # @line L4
        if pre == YELLOW or self.tc - size < 0:  # @line L5
            self.tp -= size  # @line L6
            return YELLOW  # @line L6
        self.tp -= size  # @line L7
        self.tc -= size  # @line L7
        return GREEN  # @line L8


def mark(
    packets: list[tuple],
    pir: Number,
    pbs: Number,
    cir: Number,
    cbs: Number,
    color_aware: bool = False,
) -> list[str]:
    """Color a list of (time, size) or (time, size, precolor) in time order."""
    if not packets:
        return []
    m = TwoRateThreeColorMarker(pir, pbs, cir, cbs, color_aware, packets[0][0])
    out = []
    for p in packets:
        pre = p[2] if len(p) > 2 else None
        out.append(m.meter(p[0], p[1], pre))
    return out
