# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/median-cut/. The authors are listed in prov/FCH3KR.jsonl.

"""Median cut color quantization (Heckbert).

The input is a list of colors, one per pixel, each a tuple of integers such as
(r, g, b). The boxes are lists of these colors. A box is split on the axis of
its largest extent, at the median color along that axis, and the box with the
largest extent of all is split first. The palette is the mean of each box, kept
as exact fractions, and each pixel is mapped to the nearest palette color.
"""

from fractions import Fraction


def extent(box, axis):
    values = [c[axis] for c in box]
    return max(values) - min(values)


def median_cut(colors, k):
    """Split the colors into at most k boxes. Return the list of boxes."""
    boxes = [list(colors)]  # @line L1
    while len(boxes) < k:  # @line L2
        span, i, axis = 0, 0, 0
        for j, box in enumerate(boxes):  # @line L3
            for a in range(len(box[0])):
                if extent(box, a) > span:  # the first box and axis win a tie
                    span, i, axis = extent(box, a), j, a
        if span == 0:  # @line L4
            break
        box = sorted(boxes[i], key=lambda c: (c[axis], c))  # @line L5
        m = box[len(box) // 2][axis]  # @line L6
        left = [c for c in box if c[axis] < m]  # @line L7
        right = [c for c in box if c[axis] >= m]
        if not left:
            left = [c for c in box if c[axis] <= m]
            right = [c for c in box if c[axis] > m]
        boxes[i : i + 1] = [left, right]  # @line L8
    return boxes


def box_mean(box):
    n = len(box)
    return tuple(Fraction(sum(c[a] for c in box), n) for a in range(len(box[0])))


def palette(boxes):
    return [box_mean(box) for box in boxes]  # @line L9


def squared_distance(p, q):
    return sum((x - y) ** 2 for x, y in zip(p, q))


def nearest(color, pal):
    """Index of the nearest palette color; the lowest index on a tie."""
    return min(range(len(pal)), key=lambda j: (squared_distance(color, pal[j]), j))  # @line L10


def quantize(colors, k):
    """Return (palette, index of the palette color for each pixel)."""
    pal = palette(median_cut(colors, k))
    return pal, [nearest(c, pal) for c in colors]  # @line L11


def total_error(colors, pal, index):
    return sum(squared_distance(c, pal[j]) for c, j in zip(colors, index))
