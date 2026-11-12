# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/warnock-algorithm/. The authors are listed in prov/NST03R.jsonl.

"""Warnock's area subdivision algorithm (Warnock 1969), in the form that
Foley, van Dam, Feiner and Hughes give.

A triangle is ((x0, y0, z0), (x1, y1, z1), (x2, y2, z2)) in pixel units, x to
the right, y down, pixel centers at (i + 1/2, j + 1/2), smaller z nearer. A
window is a square [x, x + s] x [y, y + s] with integer corners. The output
gives each pixel the triangle that is nearest at the pixel center (the
earlier triangle on a tie), under the top-left rule, or the background.
"""

from fractions import Fraction

HALF = Fraction(1, 2)

DISJOINT, SURROUNDING, OTHER = 0, 1, 2


def _edge(ax, ay, bx, by, px, py):
    return (bx - ax) * (py - ay) - (by - ay) * (px - ax)


def _top_left(ax, ay, bx, by):
    dx, dy = bx - ax, by - ay
    return dy < 0 or (dy == 0 and dx > 0)


class Tri:
    """A triangle with a positive edge function inside and its depth plane
    z = a x + b y + c."""

    def __init__(self, verts, k):
        (x0, y0, z0), (x1, y1, z1), (x2, y2, z2) = verts
        area = _edge(x0, y0, x1, y1, x2, y2)
        if area < 0:
            x1, y1, z1, x2, y2, z2 = x2, y2, z2, x1, y1, z1
            area = -area
        self.k, self.area = k, Fraction(area)
        self.v = ((x0, y0), (x1, y1), (x2, y2))
        self.edges = ((x1, y1, x2, y2), (x2, y2, x0, y0), (x0, y0, x1, y1))
        self.tl = [_top_left(*e) for e in self.edges]
        # z at p is the barycentric mix; it is affine, so store its plane.
        w = lambda px, py: [_edge(*e, px, py) for e in self.edges]
        zs = (z0, z1, z2)
        z = lambda px, py: sum(a * b for a, b in zip(w(px, py), zs)) / self.area
        self.c = z(0, 0)
        self.a = z(1, 0) - self.c
        self.b = z(0, 1) - self.c

    def depth(self, px, py):
        return self.a * px + self.b * py + self.c

    def covers(self, px, py):
        for e, t in zip(self.edges, self.tl):
            w = _edge(*e, px, py)
            if w < 0 or (w == 0 and not t):
                return False
        return True

    def classify(self, x, y, s):
        """DISJOINT if the triangle meets no point inside the open window,
        SURROUNDING if it contains the closed window, else OTHER."""
        corners = ((x, y), (x + s, y), (x, y + s), (x + s, y + s))
        xs = [p[0] for p in self.v]
        ys = [p[1] for p in self.v]
        if max(xs) <= x or min(xs) >= x + s or max(ys) <= y or min(ys) >= y + s:
            return DISJOINT
        inside_all = True
        for e in self.edges:
            vals = [_edge(*e, px, py) for px, py in corners]
            if max(vals) <= 0:
                return DISJOINT  # the edge line separates window and triangle
            if min(vals) < 0:
                inside_all = False
        return SURROUNDING if inside_all else OTHER

    def min_depth(self, x, y, s):
        return min(self.depth(px, py) for px in (x, x + s) for py in (y, y + s))

    def max_depth(self, x, y, s):
        return max(self.depth(px, py) for px in (x, x + s) for py in (y, y + s))


def warnock(width, height, triangles, background=None):
    """Return a height x width grid with a triangle index or background, and
    the number of windows visited."""
    image = [[background] * width for _ in range(height)]
    tris = [Tri(t, k) for k, t in enumerate(triangles) if _edge(*t[0][:2], *t[1][:2], *t[2][:2]) != 0]
    side = 1
    while side < max(width, height):
        side *= 2

    def fill(x, y, s, value):
        for j in range(y, min(y + s, height)):
            for i in range(x, min(x + s, width)):
                image[j][i] = value

    stack = [(0, 0, side, tris)]  # @line L1
    windows = 0
    while stack:  # @line L2
        x, y, s, parent = stack.pop()
        if x >= width or y >= height:
            continue
        windows += 1
        rel, surround = [], []
        for t in parent:  # @line L3: classify against the window
            c = t.classify(x, y, s)
            if c != DISJOINT:
                rel.append(t)
                if c == SURROUNDING:
                    surround.append(t)
        if not rel:  # @line L4: case 1, nothing in the window
            fill(x, y, s, background)
            continue
        if len(rel) == 1 and not surround:  # @line L5: case 2, one polygon
            t = rel[0]
            for j in range(y, min(y + s, height)):
                for i in range(x, min(x + s, width)):
                    image[j][i] = t.k if t.covers(i + HALF, j + HALF) else background
            continue
        front = None  # @line L6: cases 3 and 4, a surrounding polygon in front
        for t in surround:
            zmax = t.max_depth(x, y, s)
            if all(zmax < u.min_depth(x, y, s) for u in rel if u is not t):
                front = t
                break
        if front is not None:
            fill(x, y, s, front.k)  # @line L7
            continue
        if s == 1:  # @line L8: one pixel, decide at its center
            px, py = x + HALF, y + HALF
            hits = [(t.depth(px, py), t.k) for t in rel if t.covers(px, py)]
            fill(x, y, 1, min(hits)[1] if hits else background)
            continue
        h = s // 2  # @line L9: split into four and recur
        for dx, dy in ((h, h), (0, h), (h, 0), (0, 0)):
            stack.append((x + dx, y + dy, h, rel))
    return image, windows
