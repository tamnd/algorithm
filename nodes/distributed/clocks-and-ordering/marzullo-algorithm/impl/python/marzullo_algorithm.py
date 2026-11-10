# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/marzullo-algorithm/. The authors are listed in prov/61GKS9.jsonl.

"""Marzullo's interval intersection, and the variant of NTP (RFC 5905, Section 11.2.1).

Each source gives a closed interval [lo, hi] that should hold the true time.
marzullo() returns the largest number of intervals that share a point, and the
leftmost maximal region [a, b] where that many intervals meet. Every point of
[a, b] lies in exactly that many intervals. It sorts the 2k endpoints, so it
takes O(k log k) time for k intervals.

ntp_select() follows the numbered steps of RFC 5905, Section 11.2.1, with the
test of step 5 in the form of the C code of Appendix A.5.5.1. Each candidate is (theta, lam): the offset and the root
distance. It returns (l, u, f) or None.
"""

from typing import Optional

START, END = 0, 1  # at equal positions a start sorts first, so closed intervals that touch meet


def marzullo(intervals: list[tuple[float, float]]) -> tuple[int, Optional[float], Optional[float]]:
    """Return (best, a, b): the most intervals that meet at one point, and the
    leftmost region [a, b] where that many meet."""
    table = []
    for lo, hi in intervals:
        if lo > hi:
            raise ValueError("an interval needs lo <= hi")
        table.append((lo, START))  # @line L1
        table.append((hi, END))
    table.sort()  # @line L2
    best, count = 0, 0  # @line L3
    a = b = None
    for i, (x, kind) in enumerate(table):  # @line L4
        if kind == START:
            count += 1  # @line L5
            if count > best:  # @line L6
                best = count  # @line L7
                a, b = x, table[i + 1][0]  # the next entry is the right end
        else:
            count -= 1  # @line L8
    return best, a, b


def marzullo_with_faults(intervals: list[tuple[float, float]], f: int) -> Optional[tuple[float, float]]:
    """The region of marzullo() if at least k - f intervals meet there, else None."""
    best, a, b = marzullo(intervals)
    if best >= len(intervals) - f and a is not None:
        return a, b
    return None


def depth_at(intervals: list[tuple[float, float]], x: float) -> int:
    return sum(1 for lo, hi in intervals if lo <= x <= hi)


def brute_force(intervals: list[tuple[float, float]]) -> tuple[int, Optional[float]]:
    """The largest depth and the smallest point that reaches it. The depth is a
    step function that changes only at endpoints, so the endpoints suffice."""
    best, where = 0, None
    for x in sorted({p for iv in intervals for p in iv}):
        d = depth_at(intervals, x)
        if d > best:
            best, where = d, x
    return best, where


def ntp_select(cands: list[tuple[float, float]]) -> Optional[tuple[float, float, int]]:
    """The selection steps of RFC 5905, Section 11.2.1, for candidates (theta, lam)."""
    m = len(cands)
    if m == 0:
        return None
    # Step 1 and 2: tuples (edge, type) with type -1 low, 0 mid, +1 high.
    pts = []
    for theta, lam in cands:
        pts += [(theta - lam, -1), (theta, 0), (theta + lam, +1)]
    pts.sort()
    f = 0
    while 2 * f < m:
        d = 0
        c = 0
        low = float("inf")
        for edge, t in pts:  # step 3: scan upward
            if t == -1:
                c += 1
            elif t == +1:
                c -= 1
            else:
                d += 1
            if c >= m - f:
                low = edge
                break
        c = 0
        high = float("-inf")
        for edge, t in reversed(pts):  # step 4: scan downward
            if t == +1:
                c += 1
            elif t == -1:
                c -= 1
            else:
                d += 1
            if c >= m - f:
                high = edge
                break
        # Step 5 of the text says d = f; the C code of Appendix A.5.5.1 goes
        # round again only when d > f, so it accepts d <= f. We do the same.
        if d <= f and low < high:  # step 5
            return low, high, f  # step 5A
        f += 1  # step 5B
    return None  # step 6
