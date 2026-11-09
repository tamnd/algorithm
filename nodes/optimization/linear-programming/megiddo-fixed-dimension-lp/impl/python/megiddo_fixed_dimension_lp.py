# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/megiddo-fixed-dimension-lp/. The authors are listed in prov/FG0RRG.jsonl.

"""Megiddo's prune-and-search algorithm for linear programming in two variables.

minimize c1 x1 + c2 x2 subject to a_i1 x1 + a_i2 x2 <= b_i for i = 1..m, in exact
rational arithmetic, in O(m) time. A change of variables turns the objective into
"minimize y". Then each constraint is a lower line y >= s x + t, an upper line
y <= s x + t, or a bound on x. The task is to minimize F(x) = max of the lower lines
over the x with F(x) <= G(x) = min of the upper lines and lo <= x <= hi. Each round
pairs the lines, finds the median of the crossing points of the pairs, asks an
oracle on which side of the median the optimum lies, and drops one line of each
pair whose crossing lies on the other side. The answer is one of
("optimal", point, value), ("unbounded", None, None) or ("infeasible", None, None).
"""

from dataclasses import dataclass, field
from fractions import Fraction
from typing import Optional, Sequence

Line = tuple[Fraction, Fraction]  # (slope s, intercept t) of y = s x + t
SMALL = 6  # solve directly when this many lines remain


@dataclass
class Result:
    status: str  # "optimal", "unbounded" or "infeasible"
    x: Optional[tuple[Fraction, Fraction]] = None
    value: Optional[Fraction] = None
    rounds: list[int] = field(default_factory=list)  # the number of lines at the start of each round


def select(values: list[Fraction], k: int) -> Fraction:
    """The k-th smallest value (0-based) in linear time by the median of medians."""
    while True:
        if len(values) <= 10:
            return sorted(values)[k]
        groups = [sorted(values[i : i + 5]) for i in range(0, len(values), 5)]
        pivot = select([g[len(g) // 2] for g in groups], (len(groups) - 1) // 2)
        less = [v for v in values if v < pivot]
        equal = len(values) - len(less) - sum(1 for v in values if v > pivot)
        if k < len(less):
            values = less
        elif k < len(less) + equal:
            return pivot
        else:
            k -= len(less) + equal
            values = [v for v in values if v > pivot]


def value_at(lines: Sequence[Line], x: Fraction, upper: bool) -> tuple[Fraction, Fraction, Fraction]:
    """(F(x), least slope, largest slope) over the lines that attain the max (or the min if upper)."""
    vals = [s * x + t for s, t in lines]
    best = min(vals) if upper else max(vals)
    slopes = [s for (s, _), v in zip(lines, vals) if v == best]
    return best, min(slopes), max(slopes)


def oracle(lower: list[Line], upper: list[Line], x: Fraction) -> str:
    """Where is the optimum relative to x: "optimal", "left", "right" or "infeasible"."""
    f, f_lo, f_hi = value_at(lower, x, False)
    if not upper or f <= value_at(upper, x, True)[0]:  # x is feasible
        if f_hi < 0:
            return "right"
        if f_lo > 0:
            return "left"
        return "optimal"  # 0 is in the subdifferential of F at x
    g, g_lo, g_hi = value_at(upper, x, True)  # F - G > 0 at x; it is convex with slopes in [f_lo - g_hi, f_hi - g_lo]
    if f_lo - g_hi > 0:
        return "left"
    if f_hi - g_lo < 0:
        return "right"
    return "infeasible"  # F - G has its minimum at x, and it is positive


def inside(x: Fraction, lo: Optional[Fraction], hi: Optional[Fraction]) -> bool:
    return (lo is None or x > lo) and (hi is None or x < hi)


def prune(lines: list[Line], lo, hi, upper: bool) -> tuple[list[Line], list[tuple[Line, Line, Fraction]]]:
    """Pair the lines. Keep the pairs that cross inside (lo, hi); for the others keep the line
    that is above (below if upper) on all of [lo, hi]. Returns (kept lines, crossing pairs)."""
    kept, pairs = [], []
    if len(lines) % 2:
        kept.append(lines[-1])
    for (s1, t1), (s2, t2) in zip(lines[0::2], lines[1::2]):
        if s1 == s2:
            kept.append((s1, min(t1, t2) if upper else max(t1, t2)))
            continue
        x = (t2 - t1) / (s1 - s2)
        if inside(x, lo, hi):
            pairs.append(((s1, t1), (s2, t2), x))
        else:
            kept.append(resolve((s1, t1), (s2, t2), x, lo is not None and x <= lo, upper))
    return kept, pairs


def resolve(l1: Line, l2: Line, x: Fraction, right: bool, upper: bool) -> Line:
    """The line of the pair that matters on the side (right of x if right) where the optimum lies."""
    steeper, flatter = (l1, l2) if l1[0] > l2[0] else (l2, l1)
    top = steeper if right else flatter  # the line that is higher on that side
    return (flatter if right else steeper) if upper else top


def small_lp(lower: list[Line], upper: list[Line], lo, hi) -> tuple[str, Optional[Fraction]]:
    """Brute force on few lines: minimize F over {x in [lo, hi] : F(x) <= G(x)}. Returns (status, x)."""

    def feasible(x):
        return not upper or max(s * x + t for s, t in lower) <= min(s * x + t for s, t in upper)

    # unbounded toward +infinity: feasible far right and F falls there
    if hi is None:
        sf, tf = max(lower)
        if (not upper or (sf, tf) <= min(upper)) and sf < 0:
            return "unbounded", None
    if lo is None:
        nf = max((-s, t) for s, t in lower)
        if (not upper or nf <= min((-s, t) for s, t in upper)) and nf[0] < 0:
            return "unbounded", None
    lines = lower + upper
    xs = [x for x in (lo, hi) if x is not None]
    for i in range(len(lines)):
        for j in range(i):
            (s1, t1), (s2, t2) = lines[i], lines[j]
            if s1 != s2:
                x = (t2 - t1) / (s1 - s2)
                if (lo is None or x >= lo) and (hi is None or x <= hi):
                    xs.append(x)
    if not xs:
        xs.append(Fraction(0))
    good = [x for x in xs if feasible(x)]
    if not good:
        return "infeasible", None
    return "optimal", min(good, key=lambda x: max(s * x + t for s, t in lower))


def megiddo_fixed_dimension_lp(a: Sequence[Sequence[int]], b: Sequence[int], c: Sequence[int]) -> Result:
    c1, c2 = Fraction(c[0]), Fraction(c[1])
    if c1 == 0 and c2 == 0:
        raise ValueError("the objective must not be zero")
    # @line L1: new variables (u, y) with y = c^T x; x = (u, (y - c1 u) / c2) or ((y / c1), u)
    lower: list[Line] = []
    upper: list[Line] = []
    lo: Optional[Fraction] = None
    hi: Optional[Fraction] = None
    for (p, q), r in zip(a, b):
        p, q, r = Fraction(p), Fraction(q), Fraction(r)
        if c2 != 0:  # p x1 + q x2 = (p - q c1 / c2) u + (q / c2) y
            alpha, beta = p - q * c1 / c2, q / c2
        else:  # x1 = y / c1, x2 = u
            alpha, beta = q, p / c1
        if beta < 0:  # alpha u + beta y <= r  means  y >= (alpha / -beta) u + r / beta
            lower.append((alpha / -beta, r / beta))
        elif beta > 0:
            upper.append((-alpha / beta, r / beta))
        elif alpha > 0:
            hi = r / alpha if hi is None else min(hi, r / alpha)
        elif alpha < 0:
            lo = r / alpha if lo is None else max(lo, r / alpha)
        elif r < 0:  # 0 <= r is false
            return Result("infeasible")
    res = Result("optimal")
    if lo is not None and hi is not None and lo > hi:
        res.status = "infeasible"
        return res
    if not lower:  # @line L2: y has no lower bound; the program is unbounded since lo <= hi
        res.status = "unbounded"
        return res
    found: Optional[Fraction] = None
    while len(lower) + len(upper) > SMALL:  # @line L3
        res.rounds.append(len(lower) + len(upper))
        lower, lp = prune(lower, lo, hi, False)  # @line L4
        upper, up = prune(upper, lo, hi, True)
        pairs = [(pr, False) for pr in lp] + [(pr, True) for pr in up]
        if not pairs:
            continue
        crossings = [pr[2] for pr, _ in pairs]
        xm = select(crossings, (len(crossings) - 1) // 2)  # @line L5
        all_lower = lower + [line for l1, l2, _ in lp for line in (l1, l2)]
        all_upper = upper + [line for l1, l2, _ in up for line in (l1, l2)]
        side = oracle(all_lower, all_upper, xm)  # @line L6
        if side == "optimal":
            found, lower = xm, all_lower
            break
        if side == "infeasible":
            res.status = "infeasible"
            return res
        if side == "left":
            hi = xm
        else:
            lo = xm
        for (l1, l2, x), is_upper in pairs:  # @line L7
            if inside(x, lo, hi):
                (upper if is_upper else lower).extend([l1, l2])
            else:
                (upper if is_upper else lower).append(resolve(l1, l2, x, lo is not None and x <= lo, is_upper))
    if found is None:
        status, found = small_lp(lower, upper, lo, hi)  # @line L8
        if status != "optimal":
            res.status = status
            return res
    y = max(s * found + t for s, t in lower)
    res.value = y
    res.x = (found, (y - c1 * found) / c2) if c2 != 0 else (y / c1, found)
    return res
