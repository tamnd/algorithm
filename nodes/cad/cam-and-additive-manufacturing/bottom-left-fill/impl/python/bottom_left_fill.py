# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bottom-left-fill/. The authors are listed in prov/28CHNP.jsonl.

"""Bottom-left fill of rectangles in a strip of fixed width.

Each rectangle, in the given order, goes to the feasible position (x, y) that
is lexicographically least in (y, x): first as low as possible, then as far
left as possible at that height. Positions inside holes between earlier
rectangles count, which is what "fill" means. For rectangles this is the
bottom-left rule of Baker, Coffman and Rivest (1980).

Input: the strip width W and a list of (w, h) pairs, with 0 < w <= W and h > 0.
Sizes may be int or Fraction. Output: a list of (x, y) lower-left corners, one
per rectangle, in input order. Two rectangles overlap when their interiors
meet; touching edges are allowed. Every test is a comparison of input sums,
so the result is exact for int and Fraction input.
"""


def place_one(width, placed, w, h):
    """Return the bottom-left position (x, y) of a w by h rectangle.

    placed is a list of (x, y, w, h) rectangles that do not overlap.
    """
    by_x = sorted(placed)  # sorted by the left edge x
    heights = sorted({0} | {py + ph for (_, py, _, ph) in placed})  # @line L3
    for y in heights:  # @line L4
        x = 0  # @line L5
        for (px, py, pw, ph) in by_x:  # @line L6
            if not (py < y + h and py + ph > y):
                continue  # not in the band of heights (y, y + h)
            if px >= x + w:  # @line L7
                break  # @line L7
            x = max(x, px + pw)  # @line L8
        if x + w <= width:  # @line L9
            return x, y  # @line L10
    raise AssertionError("unreachable: the highest top always has a free row")


def bottom_left_fill(width, rects):
    """Place the rectangles in order and return their lower-left corners."""
    for (w, h) in rects:
        if not (0 < w <= width and h > 0):
            raise ValueError("each rectangle needs 0 < w <= width and h > 0")
    placed = []  # @line L1
    out = []
    for (w, h) in rects:  # @line L2
        x, y = place_one(width, placed, w, h)
        placed.append((x, y, w, h))  # @line L10
        out.append((x, y))
    return out  # @line L11


def overlap(a, b):
    """True when the interiors of the rectangles a and b, as (x, y, w, h), meet."""
    ax, ay, aw, ah = a
    bx, by, bw, bh = b
    return ax < bx + bw and bx < ax + aw and ay < by + bh and by < ay + ah


def strip_height(rects, positions):
    """Height of the packing: the highest top edge, or 0 when empty."""
    return max((y + h for (w, h), (x, y) in zip(rects, positions)), default=0)
