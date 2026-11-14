# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/method-of-means-and-medians/. The authors are listed in prov/JBVF6M.jsonl.
"""Method of means and medians (MMM) for clock routing.

Sinks are points (x, y). The sinks are split at the median, alternately by x
and by y, and the centre of mass of each set is joined by a rectilinear wire
to the centres of mass of its two halves. Two lists, sorted once by (x, y, i)
and by (y, x, i), are split in linear time at each level, so the whole run
takes O(n log n) time. Coordinates are exact Fractions.
"""

from fractions import Fraction


class Node:
    def __init__(self, pt, sinks, kids=(), axis=None):
        self.pt = pt  # centre of mass of the sinks below
        self.sinks = sinks  # sink indices below, in the order of the split axis
        self.kids = list(kids)
        self.axis = axis  # 0 for a split by x, 1 for a split by y


def centre(points, idx):
    k = len(idx)
    return (sum(Fraction(points[i][0]) for i in idx) / k, sum(Fraction(points[i][1]) for i in idx) / k)


def key(points, i, axis):
    p = points[i]
    return (p[axis], p[1 - axis], i)


def split(points, by_x, by_y, axis):
    """Return the two halves (as pairs of sorted lists) of a split on axis."""
    first = by_x if axis == 0 else by_y
    h = len(first) // 2  # @line L3
    low = set(first[:h])  # @line L4
    lx = [i for i in by_x if i in low]
    ly = [i for i in by_y if i in low]
    hx = [i for i in by_x if i not in low]
    hy = [i for i in by_y if i not in low]
    return (lx, ly), (hx, hy)


def build(points, by_x, by_y, axis):
    idx = by_x if axis == 0 else by_y
    c = centre(points, idx)  # @line L1
    if len(idx) == 1:  # @line L2
        return Node(c, list(idx))
    (lx, ly), (hx, hy) = split(points, by_x, by_y, axis)
    left = build(points, lx, ly, 1 - axis)  # @line L5
    right = build(points, hx, hy, 1 - axis)
    return Node(c, list(idx), [left, right], axis)  # @line L6


def mmm(points):
    """Return the root of the MMM tree. The first split is by x."""
    n = len(points)
    by_x = sorted(range(n), key=lambda i: key(points, i, 0))
    by_y = sorted(range(n), key=lambda i: key(points, i, 1))
    return build(points, by_x, by_y, 0)  # @line L7


def l1(p, q):
    return abs(p[0] - q[0]) + abs(p[1] - q[1])


def path_lengths(root):
    """Wire length from the root to each sink, as a dict."""
    out = {}

    def walk(v, acc):
        if not v.kids:
            out[v.sinks[0]] = acc
        for k in v.kids:
            walk(k, acc + l1(v.pt, k.pt))

    walk(root, Fraction(0))
    return out


def wirelength(root):
    return sum(l1(root.pt, k.pt) + wirelength(k) for k in root.kids)


def depth(root):
    return 0 if not root.kids else 1 + max(depth(k) for k in root.kids)
