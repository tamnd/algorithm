# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chazelle-dobkin-algorithm/. The authors are listed in prov/FCMSRJ.jsonl.
"""Logarithmic-time intersection test for two convex polygons.

A convex polygon is stored as its two chains: the upper chain (the graph of
the largest y over each x) and the lower chain, each as a list of vertices
with strictly increasing x. `chains` builds them once from the vertices.
The query `convex_polygons_intersect` reads O(log p + log q) array entries:

  P and Q meet  iff  (region below the upper chain of P) meets (region above
  the lower chain of Q), and (region below the upper chain of Q) meets
  (region above the lower chain of P).

Each of the two tests is the question whether the concave function
g = u - l on the common x-range has a nonnegative maximum, and a prune and
search on the slopes of the two chains finds a window where g is linear.
This follows the slope search idea of Chazelle and Dobkin; it is a compact
version for the decision problem, not a transcription of their paper.
"""

from fractions import Fraction


class Counter:
    def __init__(self):
        self.steps = 0


def _cross(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def _upper(points):
    top = {}
    for x, y in points:
        if x not in top or y > top[x]:
            top[x] = y
    out = []
    for p in sorted(top.items()):
        while len(out) >= 2 and _cross(out[-2], out[-1], p) >= 0:
            out.pop()
        out.append(p)
    return out


def chains(points):
    """The upper and lower chains of the convex hull of the points (preprocessing)."""
    if not points:
        raise ValueError("a polygon needs at least one vertex")
    up = _upper(points)
    low = [(x, -y) for x, y in _upper([(x, -y) for x, y in points])]
    return up, low


def _slope(c, i, cnt):
    """Slope of edge i of chain c, from c[i] to c[i + 1]."""
    cnt.steps += 1
    (x0, y0), (x1, y1) = c[i], c[i + 1]
    return Fraction(y1 - y0, x1 - x0)


def _first_index_greater(c, x, cnt):
    """The smallest index i with c[i].x > x (binary search)."""
    lo, hi = 0, len(c)
    while lo < hi:
        cnt.steps += 1
        mid = (lo + hi) // 2
        if c[mid][0] > x:
            hi = mid
        else:
            lo = mid + 1
    return lo


def _value(c, x, cnt):
    """The height of chain c at x, for x in its x-range."""
    i = _first_index_greater(c, x, cnt)
    if i == len(c):
        return Fraction(c[-1][1])
    (x0, y0), (x1, y1) = c[i - 1], c[i]
    return y0 + Fraction((y1 - y0) * (x - x0), x1 - x0)


def _edge_at(c, x, cnt):
    """The index of the edge of c that contains x in its interior or at its left end."""
    return _first_index_greater(c, x, cnt) - 1


def gap_nonnegative(u, l, cnt=None):
    """Does the region below the concave chain u meet the region above the convex chain l?"""
    cnt = cnt or Counter()
    lo, hi = max(u[0][0], l[0][0]), min(u[-1][0], l[-1][0])  # @line L3
    if lo > hi:
        return False
    ia, ib = _first_index_greater(u, lo, cnt), _first_index_greater(u, hi, cnt) - 1  # @line L4
    if ib >= 0 and u[ib][0] == hi:
        ib -= 1
    ja, jb = _first_index_greater(l, lo, cnt), _first_index_greater(l, hi, cnt) - 1
    if jb >= 0 and l[jb][0] == hi:
        jb -= 1
    wl, wr = lo, hi  # @line L5
    while ia <= ib and ja <= jb:  # @line L6
        i, j = (ia + ib) // 2, (ja + jb) // 2
        a, b = u[i][0], l[j][0]
        if a == b:
            s = _slope(u, i, cnt) - _slope(l, j, cnt)
            if s > 0:
                wl, ia, ja = max(wl, a), i + 1, j + 1
            else:
                wr, ib, jb = min(wr, a), i - 1, j - 1
        elif a < b:
            if _slope(u, i, cnt) - _slope(l, j - 1, cnt) > 0:
                wl, ia = max(wl, a), i + 1
            else:
                wr, jb = min(wr, b), j - 1
        else:
            if _slope(u, i - 1, cnt) - _slope(l, j, cnt) <= 0:
                wr, ib = min(wr, a), i - 1
            else:
                wl, ja = max(wl, b), j + 1
    if ia <= ib and wl < wr:  # @line L7
        sl = _slope(l, _edge_at(l, wl, cnt), cnt)
        while ia <= ib:
            i = (ia + ib) // 2
            if u[i][0] <= wl:
                ia = i + 1
            elif u[i][0] >= wr:
                ib = i - 1
            elif _slope(u, i, cnt) - sl > 0:
                wl, ia = u[i][0], i + 1
            else:
                wr, ib = u[i][0], i - 1
    if ja <= jb and wl < wr:  # @line L8
        su = _slope(u, _edge_at(u, wl, cnt), cnt)
        while ja <= jb:
            j = (ja + jb) // 2
            if l[j][0] <= wl:
                ja = j + 1
            elif l[j][0] >= wr:
                jb = j - 1
            elif su - _slope(l, j, cnt) > 0:
                wl, ja = l[j][0], j + 1
            else:
                wr, jb = l[j][0], j - 1
    return max(_value(u, x, cnt) - _value(l, x, cnt) for x in (wl, wr)) >= 0  # @line L9


def convex_polygons_intersect(cp, cq, cnt=None):
    """cp and cq are (upper, lower) chain pairs; True if the closed polygons meet."""
    cnt = cnt or Counter()
    (up, lp), (uq, lq) = cp, cq  # @line L1
    return gap_nonnegative(up, lq, cnt) and gap_nonnegative(uq, lp, cnt)  # @line L2
