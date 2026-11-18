# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/best-fit-page-breaking/. The authors are listed in prov/81895S.jsonl.

"""Best-fit page breaking: the page builder of TeX, without insertions.

The input is a vertical list of boxes (lines, with height and depth), glue
(the space between lines) and penalties. The builder fills one page at a
time. At each legal breakpoint it computes the cost c of a break there, as
in The TeXbook, chapter 15, and TeX: The Program, part 45. It keeps the
break of least cost seen so far (a later break wins a tie), and it ends the
page at that break as soon as c is infinite or a penalty forces a break.
It never looks at later pages.

Simplifications, each one stated on the page: no insertions (so q = 0),
no \\topskip glue, no marks and no kerns. Glue with infinite shrink is
rejected, as TeX reports it as an error on a page.
"""

import math
from typing import Optional, Sequence

from boxglue import INF_BAD, INF_PENALTY, NORMAL, Box, Glue, Item, Measures, Penalty, all_breakings, is_forced, is_legal_break, tex_badness

AWFUL_BAD = math.inf  # awful_bad of TeX: the cost of a page that does not fit
DEPLORABLE = 100000  # the cost of a page with badness INF_BAD


class Page:
    """Prefix data for the pages of one vertical list.

    total(s, b) is the page total of TeX for the items s .. b-1: the heights
    of the boxes, the depths of all boxes but the last one, and the natural
    sizes of the glue. The depth of the last box counts only when a glue
    follows it on the page, as in TeX, and only the part above max_depth.
    """

    def __init__(self, items: Sequence[Item], max_depth=None) -> None:
        for x in items:
            if isinstance(x, Glue) and x.shrink != 0 and x.shrink_order != NORMAL:
                raise ValueError("infinite shrink on a page")
        self.items = list(items)
        self.meas = Measures(items, vertical=True)
        self.max_depth = max_depth
        m = len(items)
        # last_box[i], last_glue[i]: the largest index < i that holds a box or a glue, or -1
        self.last_box = [-1] * (m + 1)
        self.last_glue = [-1] * (m + 1)
        for i, x in enumerate(items):
            self.last_box[i + 1] = i if isinstance(x, Box) else self.last_box[i]
            self.last_glue[i + 1] = i if isinstance(x, Glue) else self.last_glue[i]

    def first_box(self, a: int) -> int:
        """The first item of the page after break a: discardable items are dropped."""
        return self.meas.next_box[a + 1]

    def total(self, s: int, b: int):
        """(page total, stretch by order, normal shrink) of the items s .. b-1."""
        W, Y, Z = self.meas.W, self.meas.Y, self.meas.Z
        t = W[b] - W[s]
        k = self.last_box[b]
        if k >= s and self.last_glue[b] < k:
            d = self.items[k].depth  # the page depth: not yet in the total
            t -= d
            if self.max_depth is not None and d > self.max_depth:
                t += d - self.max_depth
        stretch = tuple(Y[o][b] - Y[o][s] for o in range(len(Y)))
        return t, stretch, Z[NORMAL][b] - Z[NORMAL][s]


def page_badness(total, stretch, shrink, goal):
    """The badness b of a page with this total, set to the page goal.

    It is 0 when the page must stretch and has stretch of an infinite order,
    AWFUL_BAD when it must shrink more than its shrink, and otherwise the
    integer badness of TeX. Sizes are integers (scaled points or abstract
    units).
    """
    if total < goal:
        if any(stretch[1:]):
            return 0
        return tex_badness(goal - total, stretch[NORMAL])
    if total - goal > shrink:
        return AWFUL_BAD
    return tex_badness(total - goal, shrink)


def break_cost(b, p: int, q: int = 0):
    """The cost c of a page break with page badness b, penalty p and insert penalties q.

    The TeXbook, chapter 15: c = p for a forced break on a page that fits,
    b + p + q when b < 10000, 100000 when b = 10000, and infinite when the
    page does not fit or q >= 10000.
    """
    if b < AWFUL_BAD:
        if p <= -INF_PENALTY:
            c = p
        elif b < INF_BAD:
            c = b + p + q
        else:
            c = DEPLORABLE
    else:
        c = AWFUL_BAD
    if q >= INF_PENALTY:
        c = AWFUL_BAD
    return c


def _penalty(x: Item) -> int:
    return x.penalty if isinstance(x, Penalty) else 0


def page_builder(items: Sequence[Item], goal, max_depth=None, stats: Optional[dict] = None):
    """Break a vertical list into pages as TeX does. Returns (breaks, costs).

    breaks[j] is the index of the item where page j ends (the item itself
    is dropped), and costs[j] is the cost c of that break. The last item
    must be a forced penalty. When no break on a page fits, the builder
    takes the first break where the page does not fit (an overfull page),
    as TeX does. A forced penalty that comes at the top of a page is
    discarded with the glue there, so the breaks can end before the last
    item. If stats is a dict, stats["tests"] counts the breakpoints at
    which a cost was computed.
    """
    m = len(items)
    if m == 0 or not is_forced(items[-1]):
        raise ValueError("the last item must be a forced penalty")
    pg = Page(items, max_depth)
    tests = 0
    breaks: list[int] = []  # @line L1
    costs: list = []
    a = -1
    while True:  # @line L2
        s = pg.first_box(a)  # @line L3
        if s >= m:  # @line L4
            break
        least, best = AWFUL_BAD, None  # @line L5
        for b in range(s + 1, m):  # @line L6
            if not is_legal_break(items, b):  # @line L7
                continue
            tests += 1
            p = _penalty(items[b])
            total, stretch, shrink = pg.total(s, b)  # @line L8
            c = break_cost(page_badness(total, stretch, shrink, goal), p)  # @line L9
            if c <= least:  # @line L10
                least, best = c, b  # @line L11
            if c == AWFUL_BAD or p <= -INF_PENALTY:  # @line L12
                break
        breaks.append(best)  # @line L13
        costs.append(least)
        a = best  # @line L14
    if stats is not None:
        stats["tests"] = tests
    return breaks, costs  # @line L15


def breaking_cost(items: Sequence[Item], breaks: Sequence[int], goal, max_depth=None):
    """The total cost of a breaking: the sum of c over its unforced breaks.

    A forced break adds 0, since every breaking has the same forced breaks.
    The value is AWFUL_BAD when a page does not fit, when a page has no box,
    or when a page runs past a forced break.
    """
    pg = Page(items, max_depth)
    total_cost = 0
    a = -1
    for b in breaks:
        s = pg.first_box(a)
        if s >= b:
            return AWFUL_BAD
        for i in range(s, b):
            if is_forced(items[i]):
                return AWFUL_BAD
        p = _penalty(items[b])
        t, stretch, shrink = pg.total(s, b)
        c = break_cost(page_badness(t, stretch, shrink, goal), p)
        if c == AWFUL_BAD:
            return AWFUL_BAD
        if p > -INF_PENALTY:
            total_cost += c
        a = b
    if pg.first_box(a) < len(items):
        return AWFUL_BAD  # a box is left after the last break
    return total_cost


def optimal_breaking(items: Sequence[Item], goal, max_depth=None):
    """The brute force optimum (cost, breaks) over all breakings, for tiny lists only.

    A breaking may also stop before the last item when only glue and
    penalties follow its last break (TeX discards them at the top of the
    next page), so each breaking is tried with and without its last break.
    """
    best_cost, best_breaks = AWFUL_BAD, None
    for full in all_breakings(items):
        for br in (full, full[:-1]):
            if not br:
                continue
            c = breaking_cost(items, br, goal, max_depth)
            if c < best_cost:
                best_cost, best_breaks = c, br
    return best_cost, best_breaks


def lines(heights, glue: Glue, penalties: Optional[Sequence[int]] = None, finish: bool = True) -> list[Item]:
    """A vertical list of lines of the given heights (depth 0), with glue between them.

    penalties[i], when given and nonzero, is a penalty put before the glue
    that follows line i (a club or widow penalty, say). With finish, the
    list ends as \\end does in plain TeX: a glue 0 plus 1fill and a forced
    break.
    """
    items: list[Item] = []
    for i, h in enumerate(heights):
        if i > 0:
            pen = penalties[i - 1] if penalties else 0
            if pen:
                items.append(Penalty(0, pen))
            items.append(glue)
        items.append(Box(0, h))
    if finish:
        items.append(Glue(0, 1, 0, stretch_order=2))
        items.append(Penalty(0, -INF_PENALTY))
    return items
