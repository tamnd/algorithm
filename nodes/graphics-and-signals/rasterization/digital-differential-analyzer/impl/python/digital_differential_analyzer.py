# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/digital-differential-analyzer/. The authors are listed in prov/QJ39WT.jsonl.

import math
import struct
from typing import Callable


def to_float32(v: float) -> float:
    """Round a binary64 value to the nearest binary32 value (round half to even)."""
    return struct.unpack("f", struct.pack("f", v))[0]


def dda_line(x0: int, y0: int, x1: int, y1: int, single: bool = False) -> list[tuple[int, int]]:
    """Return the pixels of the segment from (x0, y0) to (x1, y1) by the floating-point DDA.

    The endpoints are integer pixel centers. The line gets n + 1 pixels, n = max(|x1 - x0|, |y1 - y0|).
    Each step adds the rounded increments to the two coordinates, and each pixel is
    (floor(x + 1/2), floor(y + 1/2)). With single=True every float result is rounded to
    binary32, as on hardware that uses 32-bit floats; else binary64 is used.
    Cost: n + 1 steps, O(1) extra space besides the output.
    """
    q: Callable[[float], float] = to_float32 if single else float
    n = max(abs(x1 - x0), abs(y1 - y0))  # @line L1
    if n == 0:  # @line L2
        return [(x0, y0)]
    dx = q((x1 - x0) / n)  # @line L3
    dy = q((y1 - y0) / n)
    x, y = q(float(x0)), q(float(y0))  # @line L4
    out: list[tuple[int, int]] = []
    for _ in range(n + 1):  # @line L5
        out.append((math.floor(q(x + 0.5)), math.floor(q(y + 0.5))))  # @line L6
        x, y = q(x + dx), q(y + dy)  # @line L7
    return out
