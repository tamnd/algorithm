# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/seam-carving/. The authors are listed in prov/9886BS.jsonl.

"""Seam carving (Avidan and Shamir 2007) for one gray channel.

An image is a list of H rows, each a list of W numbers (int, float or
Fraction). Pixel (x, y) is img[y][x]. The energy is the e1 energy of the
paper, |dI/dx| + |dI/dy|, with central differences and a clamp-to-edge
border rule. A vertical seam is a list s of H column indices with
|s[y] - s[y - 1]| <= 1; it removes one pixel from each row.

One seam costs O(WH) time and O(WH) extra space. Removing k seams costs
O(kWH) time, because the energy is computed again after each removal.
"""

from fractions import Fraction
from typing import List, Sequence, Union

Num = Union[int, float, Fraction]
Image = List[List[Num]]


def energy(img: Sequence[Sequence[Num]]) -> Image:
    """The e1 energy |I(x+1,y) - I(x-1,y)| + |I(x,y+1) - I(x,y-1)|, indices clamped. O(WH)."""
    h = len(img)
    w = len(img[0]) if h else 0
    out: Image = []
    for y in range(h):
        row: List[Num] = []
        for x in range(w):
            dx = img[y][min(x + 1, w - 1)] - img[y][max(x - 1, 0)]
            dy = img[min(y + 1, h - 1)][x] - img[max(y - 1, 0)][x]
            row.append(abs(dx) + abs(dy))
        out.append(row)
    return out


def min_vertical_seam(e: Sequence[Sequence[Num]]) -> List[int]:
    """A connected vertical seam of least total energy; ties go to the leftmost column. O(WH)."""
    h = len(e)
    if h == 0 or len(e[0]) == 0:
        raise ValueError("the image is empty")
    w = len(e[0])
    m: List[List[Num]] = [list(e[0])]  # @line L6
    parent: List[List[int]] = [[0] * w]
    for y in range(1, h):  # @line L7
        row: List[Num] = []
        par: List[int] = []
        prev = m[y - 1]
        for x in range(w):  # @line L8
            b = max(x - 1, 0)  # @line L9: the leftmost least of the up to three cells above
            for c in range(b + 1, min(x + 1, w - 1) + 1):
                if prev[c] < prev[b]:
                    b = c
            row.append(e[y][x] + prev[b])  # @line L10
            par.append(b)
        m.append(row)
        parent.append(par)
    last = m[h - 1]
    s = [0] * h
    best = 0  # @line L11
    for x in range(1, w):
        if last[x] < last[best]:
            best = x
    s[h - 1] = best
    for y in range(h - 1, 0, -1):  # @line L12
        s[y - 1] = parent[y][s[y]]
    return s  # @line L13


def seam_energy(e: Sequence[Sequence[Num]], s: Sequence[int]) -> Num:
    """The total energy of the pixels on seam s."""
    return sum(e[y][s[y]] for y in range(len(s)))


def remove_vertical_seam(img: Sequence[Sequence[Num]], s: Sequence[int]) -> Image:
    """Delete pixel (s[y], y) from each row y. O(WH)."""
    return [list(row[: s[y]]) + list(row[s[y] + 1:]) for y, row in enumerate(img)]


def transpose(img: Sequence[Sequence[Num]]) -> Image:
    """Swap rows and columns, so that a horizontal seam becomes a vertical one."""
    return [list(col) for col in zip(*img)]


def seam_carve(img: Sequence[Sequence[Num]], k: int) -> Image:
    """Remove k vertical seams, one at a time, so the width drops from W to W - k. O(kWH)."""
    w = len(img[0]) if img else 0
    if not 0 <= k < max(w, 1):
        raise ValueError("k must satisfy 0 <= k < W")
    cur: Image = [list(row) for row in img]
    for _ in range(k):  # @line L1
        e = energy(cur)  # @line L2
        s = min_vertical_seam(e)  # @line L3
        cur = remove_vertical_seam(cur, s)  # @line L4
    return cur  # @line L5


def seam_carve_height(img: Sequence[Sequence[Num]], k: int) -> Image:
    """Remove k horizontal seams: carve the transposed image, then transpose back."""
    return transpose(seam_carve(transpose(img), k))
