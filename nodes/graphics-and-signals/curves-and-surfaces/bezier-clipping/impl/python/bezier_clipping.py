# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bezier-clipping/. The authors are listed in prov/FFP21G.jsonl.

"""Bezier clipping (Sederberg and Nishita 1990).

Two functions are given:

- bezier_clip_roots(coeffs, eps) finds the roots in [0, 1] of the
  polynomial with the Bernstein coefficients `coeffs`.
- bezier_clip_intersect(P, Q, eps) finds the intersections of two planar
  Bezier curves with control points P and Q.

Both stop on parameter intervals of width at most eps, and return the
unions of the final intervals that touch. Together they contain every root
or intersection. Use fractions.Fraction (or int) input:
the arithmetic is exact, and each new interval end is rounded outward to a
dyadic grid, so that the numbers stay small and no root is lost.
"""

from fractions import Fraction
from typing import Optional, Sequence

SHRINK = Fraction(4, 5)  # split when an interval keeps more than 80 percent


def _split(c: Sequence, t) -> tuple[list, list]:
    """de Casteljau split of a control polygon (numbers or tuples) at t."""
    n = len(c) - 1
    b = list(c)
    left, right = [b[0]], [b[n]]
    for r in range(1, n + 1):
        for i in range(n - r + 1):
            if isinstance(b[i], tuple):
                b[i] = tuple((1 - t) * p + t * q for p, q in zip(b[i], b[i + 1]))
            else:
                b[i] = (1 - t) * b[i] + t * b[i + 1]
        left.append(b[0])
        right.append(b[n - r])
    right.reverse()
    return left, right


def restrict(c: Sequence, a, b) -> list:
    """Control polygon of the curve c on the parameter interval [a, b]."""
    left, _ = _split(c, b)
    if b == 0:
        return [left[0]] * len(c)
    _, mid = _split(left, Fraction(a) / b)
    return mid


def clip_range(xs: Sequence, ys: Sequence, lo, hi) -> Optional[tuple]:
    """Range of x over conv{(xs[i], ys[i])} intersected with lo <= y <= hi.

    The extreme points of that set are input points inside the band, or
    crossings of a segment between two input points with y = lo or y = hi,
    so it is enough to look at these candidates. Return None if it is empty.
    """
    cand = [x for x, y in zip(xs, ys) if lo <= y <= hi]
    k = len(xs)
    for level in {lo, hi}:
        for i in range(k):
            for j in range(i + 1, k):
                yi, yj = ys[i] - level, ys[j] - level
                if yi * yj < 0:
                    cand.append(xs[i] + (xs[j] - xs[i]) * yi / (yi - yj))
    if not cand:
        return None
    return min(cand), max(cand)


def _grid(eps) -> Fraction:
    """A power of two that is at most eps / 16."""
    g = Fraction(1)
    while g > Fraction(eps) / 16:
        g /= 2
    return g


def _round_out(a, b, lo, hi, g) -> tuple:
    """Round [a, b] outward to multiples of g, and keep it inside [lo, hi]."""
    ra = Fraction((Fraction(a) / g).__floor__()) * g
    rb = Fraction((Fraction(b) / g).__ceil__()) * g
    return max(ra, lo), min(rb, hi)


def _fat_line(Qc: Sequence) -> tuple:
    """Affine function l(x, y) that is zero on the line through the end points."""
    x0, y0 = Qc[0]
    dx, dy = Qc[-1][0] - x0, Qc[-1][1] - y0
    if dx == 0 and dy == 0:
        for p in Qc:
            if p != Qc[0]:
                dx, dy = p[0] - x0, p[1] - y0
                break
        else:
            dx, dy = 1, 0
    return dy, -dx, -(dy * x0 - dx * y0)


def fat_line_clip(Pc: Sequence, Qc: Sequence) -> Optional[tuple]:
    """Parameter range of the curve Pc that can meet the fat line of Qc."""
    a, b, c = _fat_line(Qc)  # @line L12
    dq = [a * x + b * y + c for x, y in Qc]  # @line L13
    m = len(Pc) - 1
    xs = [Fraction(i, m) if m else Fraction(0) for i in range(m + 1)]  # @line L14
    ys = [a * x + b * y + c for x, y in Pc]  # @line L14
    return clip_range(xs, ys, min(dq), max(dq))  # @line L15


def merge_boxes(boxes: list) -> list:
    """Merge parameter boxes that overlap or touch in every coordinate."""
    boxes = [list(map(list, bx)) for bx in boxes]
    merged = True
    while merged:
        merged = False
        out = []
        for bx in boxes:
            for ob in out:
                if all(u[0] <= v[1] and v[0] <= u[1] for u, v in zip(bx, ob)):
                    for u, v in zip(bx, ob):
                        v[0], v[1] = min(u[0], v[0]), max(u[1], v[1])
                    merged = True
                    break
            else:
                out.append(bx)
        boxes = out
    return sorted(tuple(tuple(iv) for iv in bx) for bx in boxes)


def bezier_clip_intersect(P: Sequence, Q: Sequence, eps=Fraction(1, 2**20), max_steps: int = 20000) -> list:
    """Intersections of two planar Bezier curves by Bezier clipping.

    Return a sorted list of boxes ((a, b), (c, d)): each intersection
    P(t) = Q(s) has (t, s) in some box. Each box is a union of touching
    final boxes, and each final box has b - a <= eps and d - c <= eps. Raise RuntimeError after max_steps steps, which happens
    when the curves overlap along an arc.
    """
    g = _grid(eps)
    one, zero = Fraction(1), Fraction(0)
    stack = [((zero, one), (zero, one))]  # @line L1
    found = []  # @line L1
    steps = 0
    while stack:  # @line L2
        steps += 1
        if steps > max_steps:
            raise RuntimeError("too many steps; the curves may overlap")
        (a, b), (c, d) = stack.pop()  # @line L3
        Pc, Qc = restrict(P, a, b), restrict(Q, c, d)  # @line L3
        if b - a <= eps and d - c <= eps:  # @line L4
            found.append(((a, b), (c, d)))  # @line L4
            continue
        wp, wq = b - a, d - c
        r = fat_line_clip(Pc, Qc)  # @line L5
        if r is None:  # @line L5
            continue
        a, b = _round_out(a + r[0] * wp, a + r[1] * wp, a, b, g)  # @line L6
        Pc = restrict(P, a, b)  # @line L6
        r = fat_line_clip(Qc, Pc)  # @line L7
        if r is None:  # @line L7
            continue
        c, d = _round_out(c + r[0] * wq, c + r[1] * wq, c, d, g)  # @line L8
        # Progress means that an interval wider than eps lost 20 percent.
        progress = (wp > eps and b - a <= SHRINK * wp) or (wq > eps and d - c <= SHRINK * wq)
        if not progress and not (b - a <= eps and d - c <= eps):  # @line L9
            if b - a >= d - c:  # @line L9
                m = (a + b) / 2
                stack.append(((a, m), (c, d)))
                stack.append(((m, b), (c, d)))
            else:  # @line L9
                m = (c + d) / 2
                stack.append(((a, b), (c, m)))
                stack.append(((a, b), (m, d)))
        else:
            stack.append(((a, b), (c, d)))  # @line L10
    return merge_boxes(found)  # @line L11


def bezier_clip_roots(coeffs: Sequence, eps=Fraction(1, 2**20), max_steps: int = 20000) -> list:
    """Roots in [0, 1] of the polynomial sum c_i B_i^n(t), by Bezier clipping.

    The graph (t, f(t)) is a Bezier curve with control points (i/n, c_i),
    and it is clipped against the band y = 0. Return a sorted list of
    disjoint intervals (a, b) that contain all roots. Each one is a union of
    touching final intervals of width at most eps.
    """
    if all(c == 0 for c in coeffs):
        raise ValueError("the zero polynomial has every t as a root")
    n = len(coeffs) - 1
    xs = [Fraction(i, n) if n else Fraction(0) for i in range(n + 1)]
    g = _grid(eps)
    stack = [(Fraction(0), Fraction(1))]
    found = []
    steps = 0
    while stack:
        steps += 1
        if steps > max_steps:
            raise RuntimeError("too many steps")
        a, b = stack.pop()
        c = restrict(coeffs, a, b)
        if b - a <= eps:
            if clip_range(xs, c, 0, 0) is not None:
                found.append(((a, b),))
            continue
        r = clip_range(xs, c, 0, 0)
        if r is None:
            continue
        w = b - a
        a2, b2 = _round_out(a + r[0] * w, a + r[1] * w, a, b, g)
        if b2 - a2 > SHRINK * w:
            m = (a2 + b2) / 2
            stack.append((a2, m))
            stack.append((m, b2))
        else:
            stack.append((a2, b2))
    return [bx[0] for bx in merge_boxes(found)]
