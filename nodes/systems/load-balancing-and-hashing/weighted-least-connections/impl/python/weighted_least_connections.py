# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/weighted-least-connections/. The authors are listed in prov/FXQQ1P.jsonl.

"""Weighted least connections (WLC) load balancing.

Backend j has an integer weight w[j] >= 0 and a load h[j]. pick() returns the
first up backend with w[j] > 0 that has the smallest ratio h[j] / w[j], and
compares two ratios by cross-multiplication, h[i] * w[j] < h[j] * w[i], so no
division and no rounding happen. Cost: Theta(n) per pick, Theta(1) per done.

The load is the number of active connections (nginx least_conn), or the LVS
overhead 256 * active + inactive (ip_vs_wlc). sed_pick() is the shortest
expected delay rule, which ranks (active + 1) / w instead.
"""

from typing import List, Optional, Sequence


class WeightedLeastConnections:
    """WLC with active connection counts. Ties go to the lowest index."""

    def __init__(self, weights: Sequence[int]) -> None:
        if any(w < 0 for w in weights):
            raise ValueError("weights must be >= 0")
        self.w = list(weights)
        self.a = [0] * len(self.w)
        self.up = [True] * len(self.w)

    def pick(self) -> Optional[int]:
        j = wlc_choose(self.a, self.w, self.up)
        if j is not None:  # @line L6
            self.a[j] += 1
        return j  # @line L7

    def done(self, j: int) -> None:
        if self.a[j] <= 0:
            raise ValueError("no active connection on this backend")
        self.a[j] -= 1  # @line L8


def wlc_choose(h: Sequence[int], w: Sequence[int], up: Sequence[bool]) -> Optional[int]:
    """Index of the first up backend with w > 0 and the smallest h / w, or None."""
    best = None  # @line L1
    for j in range(len(h)):  # @line L2
        if not up[j] or w[j] <= 0:  # @line L3
            continue
        if best is None or h[j] * w[best] < h[best] * w[j]:  # @line L4
            best = j  # @line L5
    return best


def lvs_overhead(active: int, inactive: int) -> int:
    """The LVS load of a real server: active connections count 256 times an inactive one."""
    return (active << 8) + inactive


def lvs_wlc_pick(active: Sequence[int], inactive: Sequence[int], w: Sequence[int]) -> Optional[int]:
    """The ip_vs_wlc rule: smallest overhead / weight, by cross-multiplication."""
    h = [lvs_overhead(a, i) for a, i in zip(active, inactive)]
    return wlc_choose(h, w, [True] * len(h))


def sed_pick(active: Sequence[int], w: Sequence[int]) -> Optional[int]:
    """Shortest expected delay: smallest (active + 1) / w among w > 0."""
    return wlc_choose([a + 1 for a in active], w, [True] * len(active))


def picks_from_zero(weights: Sequence[int], k: int) -> List[int]:
    """The first k picks of WLC from all-zero counts when no connection closes."""
    lb = WeightedLeastConnections(weights)
    return [lb.pick() for _ in range(k)]
