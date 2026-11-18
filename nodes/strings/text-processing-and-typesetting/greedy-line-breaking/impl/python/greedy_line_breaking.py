# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/greedy-line-breaking/. The authors are listed in prov/HF8Z28.jsonl.

"""Greedy (first-fit) line breaking on boxes, glue and penalties.

Each line takes the farthest legal break that does not make the line
overfull, that is, the line fits when its glue shrinks fully. The method
never looks at later lines.
"""

from typing import Optional, Sequence

from boxglue import NORMAL, Item, Measures, adjustment_ratio, is_forced, is_legal_break, is_overfull


def _length(line_width, j: int):
    """The length l_j of line j (0-based). A sequence repeats its last entry."""
    if isinstance(line_width, (list, tuple)):
        return line_width[min(j, len(line_width) - 1)]
    return line_width


def fits(meas: Measures, a: int, b: int, l) -> bool:
    """True when the line from break a to break b is not overfull at length l."""
    L, Y, Z = meas.line(a, b)
    r, order = adjustment_ratio(l, L, Y, Z)
    return not is_overfull(r, order)


def _min_width(meas: Measures, a: int, b: int):
    """The width at full shrink of the line a..b without the item x_b.

    This value never decreases when b grows, so it tells when to stop.
    It is None when the line has shrink of an infinite order (never overfull).
    """
    s = meas.start(a, b)
    if any(meas.Z[o][b] - meas.Z[o][s] for o in range(1, len(meas.Z))):
        return None
    return (meas.W[b] - meas.W[s]) - (meas.Z[NORMAL][b] - meas.Z[NORMAL][s])


def greedy_line_breaks(items: Sequence[Item], line_width, stats: Optional[dict] = None) -> list[int]:
    """The breaks b_1 < ... < b_k = m - 1 that first fit chooses.

    line_width is one length for every line, or a sequence of lengths l_0,
    l_1, ... (the last one repeats). The last item must be a forced
    penalty. When no legal break gives a line that fits, the line ends at
    the first legal break and is overfull. If stats is a dict, stats["tests"]
    counts the lines that were measured.
    """
    m = len(items)
    if m == 0 or not is_forced(items[-1]):
        raise ValueError("the last item must be a forced penalty")
    meas = Measures(items)
    legal = [b for b in range(m) if is_legal_break(items, b)]
    tests = 0
    breaks: list[int] = []  # @line L1
    a, k = -1, 0  # k indexes legal: the first legal break after a
    while a < m - 1:  # @line L2
        l = _length(line_width, len(breaks))
        best = None  # @line L3
        first = legal[k]
        i = k
        while i < len(legal):  # @line L4
            b = legal[i]
            tests += 1
            if fits(meas, a, b, l):  # @line L5
                best = b  # @line L6
            mw = _min_width(meas, a, b)
            if is_forced(items[b]) or (mw is not None and mw > l):  # @line L7
                break
            i += 1
        if best is None:  # @line L8
            best = first
        breaks.append(best)  # @line L9
        a = best
        while k < len(legal) and legal[k] <= a:
            k += 1
    if stats is not None:
        stats["tests"] = tests
    return breaks  # @line L10
