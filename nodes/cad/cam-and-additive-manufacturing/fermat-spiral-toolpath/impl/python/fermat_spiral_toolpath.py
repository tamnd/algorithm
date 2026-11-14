# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fermat-spiral-toolpath/. The authors are listed in prov/RPHNQ4.jsonl.

"""A connected Fermat spiral on an axis-aligned rectangle, with exact offsets.

This is the basic step of Zhao et al. (2016) on the simplest region. The
iso-contours of the distance to the boundary at spacing w are the rectangles
inset by d_i = (i - 1/2) w. Each contour is cut open on its bottom edge. The
odd contours are linked into one inward spiral, the even contours into a
second one, and the two spirals are joined at the center. The result is one
path that goes in and comes out again, and both of its ends lie on the outer
contour, at distance w from each other.

The general pipeline of the paper (contours of a distance field on any region,
the split into spiralable parts, and the linking of many spirals into one
path) is not implemented here.

Coordinates are int or Fraction, so every test on the result is exact.
"""

from fractions import Fraction


def ring_count(height, w):
    """Number of contours i >= 1 with (i - 1/2) w < height / 2."""
    half = Fraction(height) / 2
    n = 0
    while (n + Fraction(1, 2)) * w < half:
        n += 1
    return n


def link_range(width, height, w):
    """The open interval of link abscissas X that give a valid path."""
    width, height, w = Fraction(width), Fraction(height), Fraction(w)
    n = ring_count(height, w)
    return n, (2 * n - Fraction(3, 2)) * w, width - Fraction(3, 2) * w


def fermat_rectangle(width, height, w, x_link=None):
    """Return the path as a list of (x, y) points.

    The rectangle is [0, width] x [0, height] with width >= height, and w is
    the spacing. x_link is the abscissa X of the links. It must satisfy
    (2n - 3/2) w < X < width - 3w/2. The default is the midpoint.
    Raises ValueError if no valid path of this form exists.
    """
    width, height, w = Fraction(width), Fraction(height), Fraction(w)
    if height > width:
        raise ValueError("expects width >= height; swap the axes")
    n, lo, hi = link_range(width, height, w)  # @line L1
    if x_link is None:
        x_link = (lo + hi) / 2
    x_link = Fraction(x_link)
    if n < 2 or not lo < x_link < hi:  # @line L2
        raise ValueError("the rectangle is too small or too narrow for this spacing")
    rings = []
    for i in range(1, n + 1):  # @line L3
        d = (i - Fraction(1, 2)) * w  # @line L4
        s = (x_link - (i - 2) * w, d)  # @line L5
        e = (x_link - min(i, n - 1) * w, d)  # @line L6
        rings.append([s, (width - d, d), (width - d, height - d), (d, height - d), (d, d), e])  # @line L7
    odd = [p for ring in rings[0::2] for p in ring]  # @line L8
    even = [p for ring in rings[1::2] for p in ring]  # @line L9
    path = odd + even[::-1]  # @line L10
    path.append((x_link, w / 2))  # the exit: back down to contour 1  # @line L11
    return path  # @line L12


def segments(path):
    return [(path[i], path[i + 1]) for i in range(len(path) - 1)]


def length(path):
    """Length of the path. Every segment is axis-parallel."""
    return sum(abs(b[0] - a[0]) + abs(b[1] - a[1]) for a, b in segments(path))


if __name__ == "__main__":
    p = fermat_rectangle(6, 4, 1, Fraction(7, 2))
    print(" ".join("(%s, %s)" % (x, y) for x, y in p))
    print("length", length(p))
