# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/single-rate-three-color-marker/. The authors are listed in prov/M9FPKM.jsonl.

"""Single rate three color marker, srTCM (RFC 2697, Heinanen and Guerin 1999).

Two token buckets share one rate CIR. Bucket C has depth CBS and bucket E
has depth EBS. Tokens go to C; when C is full they go to E; when both are
full they are lost. A packet of B bytes is green if C holds B tokens, else
yellow if E holds B tokens, else red. A red packet takes no tokens.

Time is an explicit number (int or Fraction) that the caller passes in, and
it must not go back. The refill is lazy and exact: it adds CIR * (t - last)
tokens at each packet, first to C and then to E.
"""

from fractions import Fraction
from typing import Optional, Union

Number = Union[int, Fraction]

GREEN = "green"
YELLOW = "yellow"
RED = "red"
COLORS = (GREEN, YELLOW, RED)


class SingleRateThreeColorMarker:
    """srTCM in color-blind mode (default) or color-aware mode."""

    def __init__(
        self,
        cir: Number,
        cbs: Number,
        ebs: Number,
        color_aware: bool = False,
        start: Number = 0,
    ) -> None:
        if cir <= 0:
            raise ValueError("CIR must be positive")
        if cbs < 0 or ebs < 0:
            raise ValueError("CBS and EBS must not be negative")
        if cbs == 0 and ebs == 0:
            raise ValueError("at least one of CBS and EBS must be larger than 0")
        self.cir = cir
        self.cbs = cbs
        self.ebs = ebs
        self.color_aware = color_aware
        self.tc: Number = cbs  # both buckets are full at the start
        self.te: Number = ebs
        self.last: Number = start

    def refill(self, t: Number) -> None:
        """Bring the token counts up to time t: fill C first, then E."""
        if t < self.last:
            raise ValueError("time went back")
        a = self.cir * (t - self.last)  # @line L1
        self.last = t  # @line L1
        f = min(a, self.cbs - self.tc)  # @line L2
        self.tc += f  # @line L3
        self.te = min(self.ebs, self.te + (a - f))  # @line L4

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
        self.refill(t)  # @line L5
        if pre == GREEN and self.tc - size >= 0:  # @line L6
            self.tc -= size  # @line L7
            return GREEN  # @line L7
        if pre in (GREEN, YELLOW) and self.te - size >= 0:  # @line L8
            self.te -= size  # @line L9
            return YELLOW  # @line L9
        return RED  # @line L10


def mark(
    packets: list[tuple],
    cir: Number,
    cbs: Number,
    ebs: Number,
    color_aware: bool = False,
) -> list[str]:
    """Color a list of (time, size) or (time, size, precolor) in time order."""
    if not packets:
        return []
    m = SingleRateThreeColorMarker(cir, cbs, ebs, color_aware, packets[0][0])
    out = []
    for p in packets:
        pre = p[2] if len(p) > 2 else None
        out.append(m.meter(p[0], p[1], pre))
    return out
