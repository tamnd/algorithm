# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/knuth-plass-line-breaking/. The authors are listed in prov/RPQTNB.jsonl.

from typing import Optional, Sequence

INF = float("inf")

# An item is one of
#   ("box", width)
#   ("glue", width, stretch, shrink)        with 0 <= shrink <= width
#   ("penalty", width, penalty, flagged)    penalty INF: no break; -INF: forced
# All widths are >= 0. The last item must be a forced penalty.
Item = tuple


def is_legal_break(items: Sequence[Item], b: int) -> bool:
    it = items[b]
    if it[0] == "penalty":
        return it[2] < INF
    return it[0] == "glue" and b > 0 and items[b - 1][0] == "box"


def badness(r: float) -> float:
    """100 |r|^3, capped at 10000 as in TeX (a line with no stretch is 10000)."""
    return min(100 * abs(r) ** 3, 10000.0)


def fitness(r: float) -> int:
    if r < -0.5:
        return 0  # tight
    if r <= 0.5:
        return 1  # decent
    if r <= 1:
        return 2  # loose
    return 3  # very loose


class Paragraph:
    """Prefix sums over the items, and the measures of a line."""

    def __init__(self, items: Sequence[Item]) -> None:
        m = len(items)
        self.items = items
        self.w = [0.0] * (m + 1)  # width of boxes and glue
        self.y = [0.0] * (m + 1)  # stretch of glue
        self.z = [0.0] * (m + 1)  # shrink of glue
        for i, it in enumerate(items):
            dw = dy = dz = 0.0
            if it[0] in ("box", "glue"):
                dw = it[1]
            if it[0] == "glue":
                dy, dz = it[2], it[3]
            self.w[i + 1] = self.w[i] + dw
            self.y[i + 1] = self.y[i] + dy
            self.z[i + 1] = self.z[i] + dz
        # start[i]: first index >= i that is a box or a forced penalty
        self.start = [m] * (m + 1)
        for i in range(m - 1, -1, -1):
            it = items[i]
            keep = it[0] == "box" or (it[0] == "penalty" and it[2] == -INF)
            self.start[i] = i if keep else self.start[i + 1]

    def span(self, a: int, b: int) -> int:
        """First item of the line after a break at a (a = -1: paragraph start)."""
        return min(self.start[a + 1], b)

    def ratio(self, a: int, b: int, line_width: float) -> float:
        s = self.span(a, b)
        it = self.items[b]
        width = self.w[b] - self.w[s] + (it[1] if it[0] == "penalty" else 0)
        if width < line_width:
            stretch = self.y[b] - self.y[s]
            return (line_width - width) / stretch if stretch > 0 else INF
        if width > line_width:
            shrink = self.z[b] - self.z[s]
            return (line_width - width) / shrink if shrink > 0 else -INF
        return 0.0

    def min_width(self, a: int, b: int) -> float:
        """Width of the line a..b at full shrink, without the break item."""
        s = self.span(a, b)
        return (self.w[b] - self.w[s]) - (self.z[b] - self.z[s])


def line_demerits(items, a, b, r, prev_fit, line_penalty, flagged_demerits, fitness_demerits):
    bad = badness(r)
    it = items[b]
    p = it[2] if it[0] == "penalty" else 0
    if p >= 0:
        d = (line_penalty + bad) ** 2 + p * p
    elif p > -INF:
        d = (line_penalty + bad) ** 2 - p * p
    else:
        d = (line_penalty + bad) ** 2
    if a >= 0 and it[0] == "penalty" and it[3]:
        prev = items[a]
        if prev[0] == "penalty" and prev[3]:
            d += flagged_demerits
    if abs(fitness(r) - prev_fit) > 1:
        d += fitness_demerits
    return d


def knuth_plass(
    items: Sequence[Item],
    line_width: float,
    tolerance: float = INF,
    line_penalty: float = 10,
    flagged_demerits: float = 3000,
    fitness_demerits: float = 3000,
) -> Optional[tuple[float, list[int]]]:
    """Return (total demerits, break indices) of a best paragraph, or None.

    A line from a break at a to a break at b is feasible when its
    adjustment ratio r is >= -1 and its badness min(100|r|^3, 10000) is
    at most tolerance.
    """
    par = Paragraph(items)
    m = len(items)
    # an active node: (position, fitness class, total demerits, parent node)
    active = [(-1, 1, 0.0, None)]  # @line L1
    for b in range(m):  # @line L2
        if not is_legal_break(items, b):  # @line L3
            continue
        forced = items[b][0] == "penalty" and items[b][2] == -INF
        best = [None] * 4  # @line L4
        keep = []
        for node in active:  # @line L5
            a, fit, total, _ = node
            r = par.ratio(a, b, line_width)  # @line L6
            if r >= -1 and badness(r) <= tolerance:  # @line L7
                d = total + line_demerits(  # @line L8
                    items, a, b, r, fit, line_penalty, flagged_demerits, fitness_demerits
                )
                c = fitness(r)
                if best[c] is None or d < best[c][0]:  # @line L9
                    best[c] = (d, node)
            if not forced and par.min_width(a, b) <= line_width:  # @line L10
                keep.append(node)
        active = keep  # @line L11
        for c in range(4):  # @line L12
            if best[c] is not None:
                active.append((b, c, best[c][0], best[c][1]))
    final = [nd for nd in active if nd[0] == m - 1]  # @line L13
    if not final:
        return None
    node = min(final, key=lambda nd: nd[2])
    total, breaks = node[2], []
    while node[0] >= 0:  # @line L14
        breaks.append(node[0])
        node = node[3]
    breaks.reverse()
    return total, breaks  # @line L15


def paragraph_demerits(items, line_width, breaks, tolerance=INF, line_penalty=10,
                       flagged_demerits=3000, fitness_demerits=3000) -> Optional[float]:
    """Total demerits of a given list of breaks, or None if a line is infeasible."""
    par = Paragraph(items)
    a, fit, total = -1, 1, 0.0
    for b in breaks:
        r = par.ratio(a, b, line_width)
        if not (r >= -1 and badness(r) <= tolerance):
            return None
        total += line_demerits(items, a, b, r, fit, line_penalty, flagged_demerits, fitness_demerits)
        a, fit = b, fitness(r)
    return total
