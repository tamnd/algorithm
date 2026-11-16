# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fast-corner-detector/. The authors are listed in prov/99A606.jsonl.

"""FAST corner detector (features from accelerated segment test).

An image is a list of H rows of W integers; pixel (u, v) is img[v][u], with
u the column (to the right) and v the row (down). The test reads the 16
pixels of a circle of radius 3 around p, numbered 1 to 16 clockwise from the
top. A pixel x of the circle is brighter when I(x) >= I(p) + t and darker
when I(x) <= I(p) - t (equation 8 of Rosten, Porter and Drummond, 2010).
p is a corner when n contiguous circle pixels are all brighter or all darker.

The score V(p) is the largest t for which p is still a corner. For integer
images it has the closed form

    V(p) = max over the 16 arcs A of n contiguous circle pixels of
           max(min over x in A of (I(x) - I(p)), min over x in A of (I(p) - I(x))),

and p is a corner for the threshold t >= 1 exactly when V(p) >= t.
Only pixels with 3 <= u <= W - 4 and 3 <= v <= H - 4 are tested.
"""

from typing import Dict, List, Sequence, Tuple

Image = Sequence[Sequence[int]]

# Circle offsets (du, dv) for the pixels 1 to 16, clockwise from the top.
CIRCLE: Tuple[Tuple[int, int], ...] = (
    (0, -3), (1, -3), (2, -2), (3, -1), (3, 0), (3, 1), (2, 2), (1, 3),
    (0, 3), (-1, 3), (-2, 2), (-3, 1), (-3, 0), (-3, -1), (-2, -2), (-1, -3),
)
COMPASS = (0, 4, 8, 12)  # the pixels 1, 5, 9 and 13


def ring(img: Image, u: int, v: int) -> List[int]:
    """The 16 circle values around (u, v), in the order of CIRCLE."""
    return [img[v + dv][u + du] for du, dv in CIRCLE]


def high_speed_reject(center: int, values: List[int], t: int) -> bool:
    """True when fewer than 3 of the pixels 1, 5, 9, 13 are brighter and fewer than 3 are darker.

    Valid for n = 12 only: then a rejected pixel is never a corner.
    """
    bright = sum(1 for i in COMPASS if values[i] >= center + t)
    dark = sum(1 for i in COMPASS if values[i] <= center - t)
    return bright < 3 and dark < 3


def fast_score(center: int, values: List[int], n: int) -> int:
    """V(p): the largest t for which some arc of n contiguous pixels is all brighter or all darker."""
    best = None
    for s in range(16):
        arc = [values[(s + k) % 16] for k in range(n)]
        up = min(x - center for x in arc)
        down = min(center - x for x in arc)
        cand = up if up > down else down
        if best is None or cand > best:
            best = cand
    return best


def fast_scores(img: Image, t: int = 20, n: int = 9, high_speed: bool = True) -> Dict[Tuple[int, int], int]:
    """Return {(u, v): V} for the pixels that pass the segment test with threshold t."""
    h, w = len(img), len(img[0])
    found: Dict[Tuple[int, int], int] = {}
    for v in range(3, h - 3):  # @line L1
        for u in range(3, w - 3):
            c = img[v][u]
            vals = ring(img, u, v)
            if high_speed and n == 12 and high_speed_reject(c, vals, t):  # @line L2
                continue
            score = fast_score(c, vals, n)  # @line L3
            if score >= t:  # @line L4
                found[(u, v)] = score
    return found


def fast_corners(img: Image, t: int = 20, n: int = 9, nms: bool = True, high_speed: bool = True) -> List[Tuple[int, int]]:
    """Return the corners (u, v), sorted by v then u.

    Precondition: img is a non-empty rectangular list of integer rows,
    t >= 1 and 1 <= n <= 16. With nms, a corner is kept when its score is
    not smaller than the score of any detected corner among its 8 neighbours.
    """
    scores = fast_scores(img, t, n, high_speed)
    keys = sorted(scores, key=lambda p: (p[1], p[0]))
    if not nms:
        return keys
    out: List[Tuple[int, int]] = []  # @line L5
    for u, v in keys:  # @line L6
        s = scores[(u, v)]
        if all(scores.get((u + du, v + dv), s) <= s for du in (-1, 0, 1) for dv in (-1, 0, 1)):  # @line L7
            out.append((u, v))  # @line L8
    return out  # @line L9
