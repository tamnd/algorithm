# SPDX-License-Identifier: MIT
# Shared helper of the text processing and typesetting pages of https://algorithm.tamnd.com/. The authors are listed in prov/.

"""Boxes, glue and penalties, in the notation of the typesetting pages.

This module holds no line breaking or page breaking method. It gives:

- the item types Box, Glue and Penalty, and the constant INF_PENALTY;
- a paragraph builder from word widths, with an interword glue and the
  ending of TeX (penalty 10000, glue 0 plus 1fil, penalty -10000);
- the legal breakpoints of an item list;
- the measures (L, Y, Z) of a line between two breaks, by prefix sums;
- the adjustment ratio r as a Fraction;
- the real badness min(100 |r|^3, 10000) as an exact Fraction, and the
  integer badness of TeX: The Program, section 108;
- a brute force that lists every breaking of a tiny paragraph;
- a text renderer for examples.

Widths are ints or fractions.Fraction. Do not use floats for widths.

A break is an index b of the item list. The start of the paragraph is the
break -1. A line from break a to break b holds the items a+1 .. b-1, less
the glue and penalties that follow a before the first box (TeX discards
them), plus the width of x_b when x_b is a penalty (a hyphen). Nothing is
discarded at the start of the paragraph (a = -1).

Glue can have an infinite order: 0 is normal, 1 is fil, 2 is fill and 3 is
filll, as in TeX. Stretch and shrink totals are tuples with one entry per
order.
"""

from dataclasses import dataclass
from fractions import Fraction
from itertools import product
import math
from typing import Iterator, Sequence, Union

Number = Union[int, Fraction]

INF_PENALTY = 10000  # a penalty >= INF_PENALTY forbids a break, <= -INF_PENALTY forces one
INF_BAD = 10000  # the largest finite badness (inf_bad in TeX)
NORMAL, FIL, FILL, FILLL = 0, 1, 2, 3
ORDERS = 4


@dataclass(frozen=True)
class Box:
    """A rigid item: a letter, a word or a line. text is for the renderer."""

    width: Number
    height: Number = 0
    depth: Number = 0
    text: str = ""


@dataclass(frozen=True)
class Glue:
    """A space with natural width, stretchability y and shrinkability z."""

    width: Number
    stretch: Number = 0
    shrink: Number = 0
    stretch_order: int = NORMAL
    shrink_order: int = NORMAL


@dataclass(frozen=True)
class Penalty:
    """A possible break with cost penalty. flagged marks a hyphen."""

    width: Number
    penalty: int
    flagged: bool = False


Item = Union[Box, Glue, Penalty]


def is_forced(item: Item) -> bool:
    """True for a penalty of -INF_PENALTY or less (a forced break)."""
    return isinstance(item, Penalty) and item.penalty <= -INF_PENALTY


def is_legal_break(items: Sequence[Item], b: int) -> bool:
    """A penalty below INF_PENALTY, or a glue right after a box."""
    x = items[b]
    if isinstance(x, Penalty):
        return x.penalty < INF_PENALTY
    if isinstance(x, Glue):
        return b > 0 and isinstance(items[b - 1], Box)
    return False


def legal_breakpoints(items: Sequence[Item]) -> list[int]:
    """The indices of all legal breakpoints, in increasing order."""
    return [b for b in range(len(items)) if is_legal_break(items, b)]


def _box(piece) -> Box:
    if isinstance(piece, Box):
        return piece
    if isinstance(piece, str):
        return Box(len(piece), text=piece)
    return Box(piece)


def paragraph(
    words: Sequence,
    space: Glue = Glue(1, 0, 0),
    hyphen_width: Number = 1,
    hyphen_penalty: int = 50,
    finish: bool = True,
) -> list[Item]:
    """Build the item list of a paragraph.

    Each word is a width (int or Fraction), a str (width len(str), and the
    text is kept), a Box, or a list or tuple of such pieces. Between two
    pieces of one word the builder puts a flagged penalty (a hyphenation
    point) of width hyphen_width and cost hyphen_penalty. Between two words
    it puts the glue space. With finish, it adds the ending of TeX:
    Penalty(0, INF_PENALTY), Glue(0, 1, 0, FIL) (the parfillskip) and
    Penalty(0, -INF_PENALTY).
    """
    items: list[Item] = []
    for k, word in enumerate(words):
        if k > 0:
            items.append(space)
        pieces = word if isinstance(word, (list, tuple)) else [word]
        for t, piece in enumerate(pieces):
            if t > 0:
                items.append(Penalty(hyphen_width, hyphen_penalty, True))
            items.append(_box(piece))
    if finish:
        items.append(Penalty(0, INF_PENALTY))
        items.append(Glue(0, 1, 0, stretch_order=FIL))
        items.append(Penalty(0, -INF_PENALTY))
    return items


class Measures:
    """Prefix sums over an item list, and the measures of a line in O(1).

    With vertical=True the size of a box is its height plus its depth and a
    penalty has no size, a simple model of a vertical list. The page builder
    of TeX treats the depth of the last box apart; a page that needs this
    must correct for it.
    """

    def __init__(self, items: Sequence[Item], vertical: bool = False) -> None:
        m = len(items)
        self.items = list(items)
        self.vertical = vertical
        self.W: list[Number] = [0] * (m + 1)
        self.Y: list[list[Number]] = [[0] * (m + 1) for _ in range(ORDERS)]
        self.Z: list[list[Number]] = [[0] * (m + 1) for _ in range(ORDERS)]
        for i, x in enumerate(self.items):
            dw: Number = 0
            for o in range(ORDERS):
                self.Y[o][i + 1] = self.Y[o][i]
                self.Z[o][i + 1] = self.Z[o][i]
            if isinstance(x, Box):
                dw = x.height + x.depth if vertical else x.width
            elif isinstance(x, Glue):
                dw = x.width
                self.Y[x.stretch_order][i + 1] += x.stretch
                self.Z[x.shrink_order][i + 1] += x.shrink
            self.W[i + 1] = self.W[i] + dw
        # next_box[i]: the least index >= i that holds a box, or m
        self.next_box = [m] * (m + 1)
        for i in range(m - 1, -1, -1):
            self.next_box[i] = i if isinstance(self.items[i], Box) else self.next_box[i + 1]

    def start(self, a: int, b: int) -> int:
        """The index of the first item of the line from break a to break b."""
        if a < 0:
            return 0
        return min(self.next_box[a + 1], b)

    def line(self, a: int, b: int) -> tuple[Number, tuple, tuple]:
        """(L, Y, Z) of the line from break a to break b, with a < b.

        L is the natural width, Y and Z are the total stretch and shrink,
        one entry per glue order.
        """
        s = self.start(a, b)
        L = self.W[b] - self.W[s]
        x = self.items[b]
        if isinstance(x, Penalty) and not self.vertical:
            L += x.width
        Y = tuple(self.Y[o][b] - self.Y[o][s] for o in range(ORDERS))
        Z = tuple(self.Z[o][b] - self.Z[o][s] for o in range(ORDERS))
        return L, Y, Z


def _orders(v) -> tuple:
    if isinstance(v, tuple):
        return v + (0,) * (ORDERS - len(v))
    return (v,) + (0,) * (ORDERS - 1)


def adjustment_ratio(l: Number, L: Number, Y, Z) -> tuple:
    """(r, order) for a line of natural width L set to the length l.

    Y and Z are numbers (normal order only) or tuples by order. The ratio
    uses the highest order with a nonzero total. r is a Fraction, or
    math.inf when the line must stretch and cannot, or -math.inf when it
    must shrink and cannot.
    """
    Yo, Zo = _orders(Y), _orders(Z)
    if L == l:
        return Fraction(0), NORMAL
    tot = Yo if L < l else Zo
    for o in range(ORDERS - 1, -1, -1):
        if tot[o] != 0:
            return Fraction(l - L) / Fraction(tot[o]), o
    return (math.inf if L < l else -math.inf), NORMAL


def is_overfull(r, order: int = NORMAL) -> bool:
    """True when the glue must shrink more than its shrinkability."""
    return order == NORMAL and r < -1


def badness(r, order: int = NORMAL):
    """The real badness min(100 |r|^3, 10000) of Knuth and Plass, exact.

    Glue of infinite order gives 0. An overfull line (r < -1) gives
    math.inf, so that it loses to every legal line. A line that cannot
    stretch (r = math.inf) gives 10000.
    """
    if order != NORMAL:
        return Fraction(0)
    if r < -1:
        return math.inf
    if r == math.inf:
        return Fraction(INF_BAD)
    return min(100 * abs(Fraction(r)) ** 3, Fraction(INF_BAD))


def tex_badness(t: int, s: int) -> int:
    """The integer badness(t, s) of TeX: The Program, section 108.

    t >= 0 is the amount to stretch or shrink and s the total stretch or
    shrink, both in scaled points (integers). The value is about
    100 (t/s)^3, and 10000 stands for infinitely bad.
    """
    if t < 0:
        raise ValueError("t must be >= 0")
    if t == 0:
        return 0
    if s <= 0:
        return INF_BAD
    if t <= 7230584:
        r = (t * 297) // s  # 297^3 = 99.94 * 2^18
    elif s >= 1663497:
        r = t // (s // 297)
    else:
        r = t
    if r > 1290:  # 1290^3 < 2^31 < 1291^3
        return INF_BAD
    return (r * r * r + 0o400000) // 0o1000000  # r^3 / 2^18, rounded


def tex_line_badness(l: int, L: int, Y, Z) -> int:
    """The badness that the line breaker of TeX gives a line (sections 852 and 853).

    Integer widths only. A line that needs stretch and has stretch of an
    infinite order gets 0. An overfull line gets INF_BAD + 1. Infinite
    shrink, which TeX reports as an error in a paragraph, gives 0 here.
    """
    Yo, Zo = _orders(Y), _orders(Z)
    shortfall = l - L
    if shortfall > 0:
        if any(Yo[1:]):
            return 0
        return tex_badness(shortfall, Yo[0])
    if shortfall < 0:
        if any(Zo[1:]):
            return 0
        if -shortfall > Zo[0]:
            return INF_BAD + 1
        return tex_badness(-shortfall, Zo[0])
    return 0


def all_breakings(items: Sequence[Item]) -> Iterator[tuple[int, ...]]:
    """Yield every breaking of the paragraph, for tiny paragraphs only.

    A breaking is a tuple b_1 < ... < b_k of legal breaks with b_k = m - 1
    that holds every forced break. The last item must be a forced penalty.
    There are 2^q breakings for q optional breakpoints.
    """
    m = len(items)
    if m == 0 or not is_forced(items[-1]):
        raise ValueError("the last item must be a forced penalty")
    legal = legal_breakpoints(items)
    optional = [b for b in legal if b != m - 1 and not is_forced(items[b])]
    forced = [b for b in legal if b == m - 1 or is_forced(items[b])]
    for choice in product((False, True), repeat=len(optional)):
        chosen = [b for b, c in zip(optional, choice) if c]
        yield tuple(sorted(chosen + forced))


def render(items: Sequence[Item], breaks: Sequence[int]) -> list[str]:
    """The text of each line of a breaking, for examples.

    A box shows its text (or 'x' repeated by its integer width), a glue of
    positive width shows one space, and a flagged penalty at a break shows
    '-'. Trailing spaces are removed.
    """
    meas = Measures(items)
    out: list[str] = []
    a = -1
    for b in breaks:
        parts: list[str] = []
        for x in items[meas.start(a, b) : b]:
            if isinstance(x, Box):
                if x.text:
                    parts.append(x.text)
                else:
                    parts.append("x" * x.width if isinstance(x.width, int) else "x")
            elif isinstance(x, Glue) and x.width > 0:
                parts.append(" ")
        x = items[b]
        if isinstance(x, Penalty) and x.flagged and not is_forced(x):
            parts.append("-")
        out.append("".join(parts).rstrip())
        a = b
    return out
