# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/moravec-corner-detector/. The authors are listed in prov/S56VW3.jsonl.

"""Moravec corner detector (interest operator) with exact integer arithmetic.

An image is a list of H rows of W integers; pixel (u, v) is img[v][u], with
u the column (to the right) and v the row (down). The window has radius r,
so it holds (2 r + 1)^2 pixels. For a shift (a, b) the change of the window
at (u, v) is

    E_ab(u, v) = sum over |i| <= r, |j| <= r of
                 (I(u + i + a, v + j + b) - I(u + i, v + j))^2,

and the response is C(u, v) = min of E_ab over the four shifts
(1, 0), (0, 1), (1, 1) and (1, -1). C is defined only where every read is
inside the image: r + 1 <= u <= W - r - 2 and r + 1 <= v <= H - r - 2.
A corner is a defined pixel with C > tau that is not smaller than C at any
defined pixel of its (2 m + 1) x (2 m + 1) neighbourhood.

Cost: O(W H r^2) time and O(W H) extra space on a word RAM.
"""

from typing import Dict, List, Sequence, Tuple

Image = Sequence[Sequence[int]]
SHIFTS: Tuple[Tuple[int, int], ...] = ((1, 0), (0, 1), (1, 1), (1, -1))


def shift_change(img: Image, u: int, v: int, a: int, b: int, r: int) -> int:
    """Return E_ab(u, v), the sum of squared differences for the shift (a, b)."""
    total = 0
    for j in range(-r, r + 1):
        row = img[v + j]
        row_s = img[v + j + b]
        for i in range(-r, r + 1):
            d = row_s[u + i + a] - row[u + i]
            total += d * d
    return total


def moravec_response(img: Image, r: int = 1) -> Dict[Tuple[int, int], int]:
    """Return C as a dict from (u, v) to the response, for the defined pixels only."""
    h, w = len(img), len(img[0])
    resp: Dict[Tuple[int, int], int] = {}
    for v in range(r + 1, h - r - 1):  # @line L2
        for u in range(r + 1, w - r - 1):
            resp[(u, v)] = min(shift_change(img, u, v, a, b, r) for a, b in SHIFTS)  # @line L1 @line L3
    return resp


def moravec_corners(img: Image, r: int = 1, tau: int = 0, m: int = 1) -> List[Tuple[int, int]]:
    """Return the corners (u, v), sorted by v then u.

    Precondition: img is a non-empty rectangular list of integer rows,
    r >= 0, m >= 1 and tau >= 0.
    """
    resp = moravec_response(img, r)
    corners: List[Tuple[int, int]] = []  # @line L4
    for (u, v), c in sorted(resp.items(), key=lambda kv: (kv[0][1], kv[0][0])):
        if c <= tau:  # @line L5
            continue
        ok = True
        for dv in range(-m, m + 1):  # @line L6
            for du in range(-m, m + 1):
                other = resp.get((u + du, v + dv))
                if (du or dv) and other is not None and other > c:
                    ok = False
        if ok:
            corners.append((u, v))  # @line L7
    return corners  # @line L8
