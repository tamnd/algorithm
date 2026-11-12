# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/curve-intersection/. The authors are listed in prov/9E0B9K.jsonl.

"""Intersection of two planar Bezier curves by subdivision.

This is the bounding box method of Lane and Riesenfeld (1980). Each curve
lies in the axis-aligned box of its control points (the convex hull
property). If the boxes of two pieces are disjoint, the pieces cannot meet.
Otherwise both pieces are split at the middle of their parameter interval,
and the four pairs are tested again, until the parameter intervals are at
most eps wide. Use fractions.Fraction or int control points for exact
results; all split points are dyadic.
"""

from fractions import Fraction
from typing import Sequence


def split_half(c: Sequence) -> tuple[list, list]:
    """de Casteljau split of a planar control polygon at t = 1/2."""
    n = len(c) - 1
    b = [tuple(p) for p in c]
    left, right = [b[0]], [b[n]]
    for r in range(1, n + 1):
        for i in range(n - r + 1):
            b[i] = ((b[i][0] + b[i + 1][0]) / 2, (b[i][1] + b[i + 1][1]) / 2)
        left.append(b[0])
        right.append(b[n - r])
    right.reverse()
    return left, right


def box(c: Sequence) -> tuple:
    """Axis-aligned bounding box (xmin, xmax, ymin, ymax) of the points."""
    xs = [p[0] for p in c]
    ys = [p[1] for p in c]
    return min(xs), max(xs), min(ys), max(ys)


def boxes_meet(u: tuple, v: tuple) -> bool:
    """True when two closed boxes have a common point."""
    return u[0] <= v[1] and v[0] <= u[1] and u[2] <= v[3] and v[2] <= u[3]


def merge_boxes(found: list) -> list:
    """Merge parameter boxes that overlap or touch in both coordinates."""
    boxes = [[list(u), list(v)] for u, v in found]
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
    return sorted((tuple(u), tuple(v)) for u, v in boxes)


def intersect_by_subdivision(P: Sequence, Q: Sequence, eps=Fraction(1, 2**16), max_pairs: int = 200000) -> list:
    """Intersections of the Bezier curves P and Q, as parameter boxes.

    Return a sorted list of boxes ((a, b), (c, d)). Each intersection
    P(t) = Q(s) with t, s in [0, 1] has (t, s) in some box. Each box is a
    union of touching leaf boxes, and each leaf has b - a <= eps and
    d - c <= eps. Raise RuntimeError when more than max_pairs pairs are
    tested, which happens when the curves overlap along an arc.
    """
    one, zero = Fraction(1), Fraction(0)
    stack = [(list(P), (zero, one), list(Q), (zero, one))]
    found = []
    tested = 0
    while stack:
        Pc, (a, b), Qc, (c, d) = stack.pop()
        tested += 1
        if tested > max_pairs:
            raise RuntimeError("too many pairs; the curves may overlap")
        if not boxes_meet(box(Pc), box(Qc)):
            continue
        if b - a <= eps and d - c <= eps:
            found.append(((a, b), (c, d)))
            continue
        pl, pr = split_half(Pc)
        ql, qr = split_half(Qc)
        mp, mq = (a + b) / 2, (c + d) / 2
        for pp, pi in ((pl, (a, mp)), (pr, (mp, b))):
            for qq, qi in ((ql, (c, mq)), (qr, (mq, d))):
                stack.append((pp, pi, qq, qi))
    return merge_boxes(found)
