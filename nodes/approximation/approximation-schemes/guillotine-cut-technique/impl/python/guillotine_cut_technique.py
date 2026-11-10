# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/guillotine-cut-technique/. The authors are listed in prov/Z1DTDF.jsonl.

"""The m-guillotine technique for sets of axis-parallel segments, and a dynamic program over windows.

A segment is (axis, c, lo, hi): ("h", y, x_lo, x_hi) lies on the line y = c, and ("v", x, y_lo, y_hi) on x = c.
A window is (x0, x1, y0, y1). Only the parts of segments in the open window count. Coordinates are ints or
Fractions, so all lengths are exact."""

from fractions import Fraction
from typing import Optional, Sequence

Seg = tuple
Window = tuple


def flip(segs: Sequence[Seg], w: Window) -> tuple[list[Seg], Window]:
    """Swap x and y, so that a horizontal line becomes a vertical one."""
    return [("v" if s[0] == "h" else "h",) + tuple(s[1:]) for s in segs], (w[2], w[3], w[0], w[1])


def meets(s: Seg, w: Window) -> bool:
    x0, x1, y0, y1 = w
    if s[0] == "h":
        return y0 < s[1] < y1 and s[2] < x1 and s[3] > x0
    return x0 < s[1] < x1 and s[2] < y1 and s[3] > y0


def critical(segs: Sequence[Seg], w: Window) -> list:
    """The x coordinates strictly inside the window where a segment in it starts, ends or lies."""
    x0, x1 = w[0], w[1]
    xs = set()
    for s in segs:
        if meets(s, w):
            xs.update([s[1]] if s[0] == "v" else [s[2], s[3]])
    return sorted(x for x in xs if x0 < x < x1)


def components(segs: Sequence[Seg], w: Window, c) -> list[tuple]:
    """The parts of the vertical line x = c in the open window that lie on segments, merged, in order."""
    x0, x1, y0, y1 = w
    parts = []
    for s in segs:
        if s[0] == "v" and s[1] == c and s[2] < y1 and s[3] > y0:
            parts.append((max(s[2], y0), min(s[3], y1)))
        elif s[0] == "h" and y0 < s[1] < y1 and s[2] <= c <= s[3]:
            parts.append((s[1], s[1]))
    out: list[list] = []
    for lo, hi in sorted(parts):
        if out and lo <= out[-1][1]:
            out[-1][1] = max(out[-1][1], hi)
        else:
            out.append([lo, hi])
    return [tuple(p) for p in out]


def m_span(comps: Sequence[tuple], m: int) -> Optional[tuple]:
    """From the low end of the m-th part to the high end of the m-th part from the top; None if there are at most
    2(m - 1) parts."""
    k = len(comps)
    if k <= 2 * (m - 1):
        return None
    return comps[m - 1][0], comps[k - m][1]


def uncovered(segs: Sequence[Seg], c, span: Optional[tuple]):
    """The length of the span on the line x = c that no vertical segment covers."""
    if span is None:
        return 0
    lo, hi = span
    free, pos = 0, lo
    for a, b in sorted((s[2], s[3]) for s in segs if s[0] == "v" and s[1] == c):
        if b <= pos:
            continue
        if a > pos:
            free += min(a, hi) - pos
        pos = max(pos, b)
        if pos >= hi:
            break
    return free + max(0, hi - pos)


def dark(segs: Sequence[Seg], w: Window, c, m: int):
    """The length of the part of the line x = c whose horizontal line has at least m parts on each side of c."""
    x0, x1, y0, y1 = w
    vert = [s for s in segs if s[0] == "v" and meets(s, w)]
    ys = sorted({y0, y1} | {t for s in vert for t in (s[2], s[3]) if y0 < t < y1})
    total = 0
    for u, v in zip(ys, ys[1:]):
        mid = Fraction(u + v, 2)
        cols = {s[1] for s in vert if s[2] < mid < s[3]}
        if sum(x < c for x in cols) >= m and sum(x > c for x in cols) >= m:
            total += v - u
    return total


def line_data(segs: Sequence[Seg], w: Window, axis: str, c, m: int) -> tuple:
    """(span, length of the span, uncovered length, dark length) for the line x = c (axis "x") or y = c (axis "y")."""
    if axis == "y":
        segs, w = flip(segs, w)
    sp = m_span(components(segs, w, c), m)
    return sp, (0 if sp is None else sp[1] - sp[0]), uncovered(segs, c, sp), dark(segs, w, c, m)


def coords(segs: Sequence[Seg], w: Window, axis: str) -> list:
    return critical(*flip(segs, w)) if axis == "y" else critical(segs, w)


def areas(segs: Sequence[Seg], w: Window, axis: str, m: int) -> tuple:
    """Integrals over all lines of one direction of the span length and of the dark length, piece by piece."""
    lo, hi = (w[2], w[3]) if axis == "y" else (w[0], w[1])
    cut = [lo] + coords(segs, w, axis) + [hi]
    span_area = dark_area = 0
    for a, b in zip(cut, cut[1:]):
        _, f, _, h = line_data(segs, w, axis, Fraction(a + b, 2), m)
        span_area += f * (b - a)
        dark_area += h * (b - a)
    return span_area, dark_area


def favorable_cut(segs: Sequence[Seg], w: Window, m: int) -> Optional[tuple]:
    """A line between two critical coordinates whose span is at most its dark length, with the least span."""
    best = None
    for axis in ("x", "y"):
        cut = coords(segs, w, axis)
        for a, b in zip(cut, cut[1:]):
            c = Fraction(a + b, 2)
            sp, f, _, h = line_data(segs, w, axis, c, m)  # @line L3
            if f <= h and (best is None or f < best[0]):  # @line L4
                best = (f, h, axis, c, sp)
    return best


def free_cut(segs: Sequence[Seg], w: Window, m: int) -> Optional[tuple]:
    """A line through a critical coordinate whose span already lies on segments."""
    for axis in ("x", "y"):
        for c in coords(segs, w, axis):
            sp, _, free, h = line_data(segs, w, axis, c, m)
            if free == 0:
                return 0, h, axis, c, sp
    return None


def split(w: Window, axis: str, c) -> tuple[Window, Window]:
    x0, x1, y0, y1 = w
    if axis == "x":
        return (x0, c, y0, y1), (c, x1, y0, y1)
    return (x0, x1, y0, c), (x0, x1, c, y1)


def make_m_guillotine(segs: Sequence[Seg], box: Window, m: int, stats: Optional[dict] = None) -> list[Seg]:
    """Add spans on cuts until the segments are m-guillotine in the box. Each added span is at most the dark
    length of its line, and the total is at most L / m (the theorem on the page)."""
    g = list(segs)
    stack = [box]
    cuts = []
    while stack:
        w = stack.pop()
        if not any(meets(s, w) for s in g):  # @line L1
            continue
        found = free_cut(g, w, m)  # @line L2
        if found is None:
            found = favorable_cut(g, w, m)
        if found is None:
            raise AssertionError("no free or favorable cut; the lemma says this cannot happen")
        f, h, axis, c, sp = found
        cuts.append((w, axis, c, f, h))
        if sp is not None and f > 0:
            g.append(("v" if axis == "x" else "h", c, sp[0], sp[1]))  # @line L5
        stack.extend(split(w, axis, c))  # @line L6
    if stats is not None:
        stats["cuts"] = cuts
    return g  # @line L7


def has_perfect_cut(segs: Sequence[Seg], w: Window, m: int, interior_only: bool = False) -> list[tuple]:
    """The m-perfect cuts of a window, one line per class of equal lines: each critical line and a line inside each
    piece between them. With interior_only, the pieces next to the sides of the window are left out."""
    out = []
    for axis in ("x", "y"):
        lo, hi = (w[2], w[3]) if axis == "y" else (w[0], w[1])
        crit = coords(segs, w, axis)
        cut = crit if interior_only else [lo] + crit + [hi]
        lines = list(crit) + [Fraction(a + b, 2) for a, b in zip(cut, cut[1:])]
        for c in lines:
            if line_data(segs, w, axis, c, m)[2] == 0:
                out.append((axis, c))
    return out


def is_m_guillotine(segs: Sequence[Seg], box: Window, m: int) -> bool:
    """True if some cut tree, with an m-perfect cut in every window that has a segment inside, ends in windows with
    no segment inside. Pieces next to a side are skipped: such a cut leaves a window equal to the old one."""
    memo: dict = {}

    def ok(w: Window) -> bool:
        if w not in memo:
            memo[w] = not any(meets(s, w) for s in segs) or any(
                all(ok(part) for part in split(w, axis, c)) for axis, c in has_perfect_cut(segs, w, m, True))
        return memo[w]

    return ok(box)


def total_length(segs: Sequence[Seg]):
    """The length of the union of the segments; overlaps on one line count once."""
    lines: dict = {}
    for s in segs:
        lines.setdefault((s[0], s[1]), []).append((s[2], s[3]))
    total = 0
    for parts in lines.values():
        pos = None
        for a, b in sorted(parts):
            if pos is None or a > pos:
                total += b - a
                pos = b
            elif b > pos:
                total += b - pos
                pos = b
    return total


def guillotine_partition(points: Sequence[tuple[int, int]], width: int, height: int,
                         stats: Optional[dict] = None) -> tuple[int, list[Seg]]:
    """The least total length of a guillotine partition of [0, width] x [0, height] into rectangles such that every
    point lies on a cut. Windows have sides on the lines through the points; bottom-up over windows."""
    xs = sorted({0, width} | {p[0] for p in points})
    ys = sorted({0, height} | {p[1] for p in points})
    windows = [(i0, i1, j0, j1) for i0 in range(len(xs)) for i1 in range(i0 + 1, len(xs))
               for j0 in range(len(ys)) for j1 in range(j0 + 1, len(ys))]
    windows.sort(key=lambda t: (t[1] - t[0]) + (t[3] - t[2]))
    best: dict = {}
    transitions = 0
    for i0, i1, j0, j1 in windows:
        inside = any(xs[i0] < p[0] < xs[i1] and ys[j0] < p[1] < ys[j1] for p in points)
        if not inside:
            best[(i0, i1, j0, j1)] = (0, None)
            continue
        options = []
        for i in range(i0 + 1, i1):
            transitions += 1
            options.append((ys[j1] - ys[j0] + best[(i0, i, j0, j1)][0] + best[(i, i1, j0, j1)][0], ("x", i)))
        for j in range(j0 + 1, j1):
            transitions += 1
            options.append((xs[i1] - xs[i0] + best[(i0, i1, j0, j)][0] + best[(i0, i1, j, j1)][0], ("y", j)))
        best[(i0, i1, j0, j1)] = min(options)
    segs: list[Seg] = []
    todo = [(0, len(xs) - 1, 0, len(ys) - 1)]
    while todo:
        i0, i1, j0, j1 = todo.pop()
        choice = best[(i0, i1, j0, j1)][1]
        if choice is None:
            continue
        axis, k = choice
        if axis == "x":
            segs.append(("v", xs[k], ys[j0], ys[j1]))
            todo += [(i0, k, j0, j1), (k, i1, j0, j1)]
        else:
            segs.append(("h", ys[k], xs[i0], xs[i1]))
            todo += [(i0, i1, j0, k), (i0, i1, k, j1)]
    if stats is not None:
        stats["windows"] = len(windows)
        stats["transitions"] = transitions
    return best[(0, len(xs) - 1, 0, len(ys) - 1)][0], segs
