# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/intersection-over-union/. The authors are listed in prov/20CWE7.jsonl.
"""Intersection over union (IoU) of axis-aligned boxes and of pixel sets.

A box is (x1, y1, x2, y2) with x1 <= x2 and y1 <= y2 in continuous image
coordinates, so its area is (x2 - x1) (y2 - y1). With inclusive=True the
corners are inclusive pixel indices, as in the PASCAL VOC development kit,
and every side length gets + 1. Integer or Fraction inputs give exact results
when the caller wraps them in Fraction; floats give float results.
Standard library only. Cost: O(1) per pair of boxes, O(|A| + |B|) per pair of
pixel sets.
"""

from fractions import Fraction


def box_area(b, inclusive=False):
    """Area of a box; 0 for a degenerate box."""
    e = 1 if inclusive else 0
    return max(0, b[2] - b[0] + e) * max(0, b[3] - b[1] + e)


def intersection_area(a, b, inclusive=False):
    """Area of the intersection box [max x1, min x2] x [max y1, min y2]."""
    e = 1 if inclusive else 0
    iw = min(a[2], b[2]) - max(a[0], b[0]) + e  # @line L1
    ih = min(a[3], b[3]) - max(a[1], b[1]) + e  # @line L2
    if iw <= 0 or ih <= 0:  # @line L3
        return 0
    return iw * ih


def iou(a, b, inclusive=False, empty=0):
    """IoU of two boxes. Returns `empty` when the union has area 0."""
    inter = intersection_area(a, b, inclusive)  # @line L3
    union = box_area(a, inclusive) + box_area(b, inclusive) - inter  # @line L4
    if union == 0:
        return empty
    if isinstance(inter, int) and isinstance(union, int):
        return Fraction(inter, union)  # @line L5
    return inter / union  # @line L5


def iou_matrix(boxes_a, boxes_b, inclusive=False):
    """All pairwise IoU values, as a list of rows (one row per box of boxes_a)."""
    return [[iou(a, b, inclusive) for b in boxes_b] for a in boxes_a]


def mask_iou(pa, pb, empty=0):
    """IoU of two finite sets of pixels, |A & B| / |A | B|."""
    sa, sb = set(pa), set(pb)
    union = len(sa | sb)
    if union == 0:
        return empty
    return Fraction(len(sa & sb), union)


def box_pixels(b):
    """The unit cells [u, u+1) x [v, v+1) inside an integer box, as (u, v) pairs."""
    return {(u, v) for v in range(b[1], b[3]) for u in range(b[0], b[2])}


def jaccard_distance(a, b):
    """1 - IoU of two boxes; a metric on boxes of positive area."""
    return 1 - iou(a, b)


def enclosing_box(a, b):
    return (min(a[0], b[0]), min(a[1], b[1]), max(a[2], b[2]), max(a[3], b[3]))


def giou(a, b):
    """Generalized IoU of Rezatofighi et al. 2019: IoU - |C minus (A u B)| / |C|.

    C is the smallest box that holds both boxes. The value lies in (-1, 1].
    """
    inter = intersection_area(a, b)
    union = box_area(a) + box_area(b) - inter
    c = box_area(enclosing_box(a, b))
    if isinstance(c, int) and isinstance(union, int):
        return Fraction(inter, union) - Fraction(c - union, c)
    return inter / union - (c - union) / c


def intersection_over_min(a, b):
    """|A & B| / min(|A|, |B|), the coverage overlap. This is NOT IoU."""
    inter = intersection_area(a, b)
    m = min(box_area(a), box_area(b))
    if isinstance(inter, int) and isinstance(m, int):
        return Fraction(inter, m)
    return inter / m
