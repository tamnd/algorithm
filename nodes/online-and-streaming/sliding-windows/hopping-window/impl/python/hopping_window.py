# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hopping-window/. The authors are listed in prov/RTYVEA.jsonl.
"""Hopping (sliding with a period) windows: assignment and sums through panes."""

from math import gcd
from typing import Dict, Iterable, List, Tuple


def hopping_assign(ts: int, size: int, hop: int, offset: int = 0) -> List[Tuple[int, int]]:
    """Return the windows [o + j*hop, o + j*hop + size) that hold `ts`, oldest first."""
    if size <= 0 or hop <= 0:
        raise ValueError("size and hop must be positive")
    hi = (ts - offset) // hop  # @line L1
    lo = (ts - offset - size) // hop + 1  # @line L2
    return [(offset + j * hop, offset + j * hop + size) for j in range(lo, hi + 1)]  # @line L3


def hopping_sums_direct(
    events: Iterable[Tuple[int, int]], size: int, hop: int, offset: int = 0
) -> Dict[Tuple[int, int], int]:
    """Sum of each nonempty window, by adding each item to each of its windows."""
    out: Dict[Tuple[int, int], int] = {}
    for ts, v in events:
        for w in hopping_assign(ts, size, hop, offset):
            out[w] = out.get(w, 0) + v
    return out


def hopping_sums_panes(
    events: Iterable[Tuple[int, int]], size: int, hop: int, offset: int = 0
) -> Dict[Tuple[int, int], int]:
    """Sum of each nonempty window, by panes of size gcd(size, hop) (lines L4 to L7).

    Each item is added to one pane; each window adds size/g pane sums.
    """
    g = gcd(size, hop)  # @line L4
    panes: Dict[int, int] = {}
    for ts, v in events:  # @line L5
        b = offset + g * ((ts - offset) // g)
        panes[b] = panes.get(b, 0) + v
    starts = set()
    for b in panes:  # @line L6
        # The windows that meet the pane [b, b + g) are the windows of its first instant.
        for lo, _ in hopping_assign(b, size, hop, offset):
            starts.add(lo)
    out: Dict[Tuple[int, int], int] = {}
    for b in starts:
        total = 0
        nonempty = False
        for i in range(size // g):  # @line L7
            p = b + i * g
            if p in panes:
                total += panes[p]
                nonempty = True
        if nonempty:
            out[(b, b + size)] = total
    return out
