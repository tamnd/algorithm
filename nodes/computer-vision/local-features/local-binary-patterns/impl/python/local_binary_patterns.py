# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/local-binary-patterns/. The authors are listed in prov/BQGMR7.jsonl.

"""Local binary patterns LBP_{P,R} with the u2, riu2 and ri mappings.

An image is a list of H rows of W numbers; pixel (u, v) is img[v][u], with u
the column (to the right) and v the row (down). Neighbor p of a center pixel
is at the offset (R cos(2 pi p / P), -R sin(2 pi p / P)), so p = 0 is to the
right and the neighbors go counterclockwise on the screen. A neighbor that is
not on a pixel center gets its value by bilinear interpolation.

Bit p of the code is s(g_p - g_c), with s(x) = 1 for x >= 0 and 0 otherwise
(Ojala, Pietikainen and Maenpaa 2002). The interpolated difference is rounded
to 9 decimals before the sign test, so that a difference that is zero in exact
arithmetic is not turned into a tiny positive or negative number by floating
point rounding.

Mappings of a P-bit code to a histogram label:
- "none": the code itself, 2^P labels.
- "u2": one label per uniform code (at most 2 circular 0/1 changes) and one
  shared label for all other codes, P (P - 1) + 3 labels.
- "riu2": the number of ones for a uniform code, P + 1 otherwise, P + 2 labels.
- "ri": the smallest circular rotation of the code, one label per necklace.
"""

import math
from typing import Dict, List, Sequence, Tuple

Image = Sequence[Sequence[float]]


def transitions(code: int, p_count: int) -> int:
    """U(code): the number of circular 0/1 changes in the P-bit code."""
    u = 0
    for p in range(p_count):
        a = (code >> p) & 1
        b = (code >> ((p + 1) % p_count)) & 1
        u += a ^ b
    return u


def min_rotation(code: int, p_count: int) -> int:
    """The smallest value among the P circular rotations of the code."""
    mask = (1 << p_count) - 1
    best = code
    c = code
    for _ in range(p_count - 1):
        c = ((c >> 1) | ((c & 1) << (p_count - 1))) & mask
        best = min(best, c)
    return best


def build_mapping(p_count: int, kind: str) -> Tuple[List[int], int]:
    """Return (table, number of labels): table[code] is the label of the code."""
    size = 1 << p_count
    if kind == "none":
        return list(range(size)), size
    if kind == "riu2":
        table = []
        for code in range(size):
            if transitions(code, p_count) <= 2:
                table.append(bin(code).count("1"))
            else:
                table.append(p_count + 1)
        return table, p_count + 2
    if kind == "u2":
        table = [0] * size
        nxt = 0
        uniform_label: Dict[int, int] = {}
        for code in range(size):
            if transitions(code, p_count) <= 2:
                uniform_label[code] = nxt
                nxt += 1
        other = nxt
        for code in range(size):
            table[code] = uniform_label.get(code, other)
        return table, nxt + 1
    if kind == "ri":
        labels: Dict[int, int] = {}
        table = []
        for code in range(size):
            r = min_rotation(code, p_count)
            if r not in labels:
                labels[r] = len(labels)
            table.append(labels[r])
        return table, len(labels)
    raise ValueError("unknown mapping: " + kind)


def offsets(p_count: int, radius: float) -> List[Tuple[float, float]]:
    """Offsets (du, dv) of the P neighbors, rounded to 12 decimals."""
    out = []
    for p in range(p_count):
        a = 2.0 * math.pi * p / p_count
        du = round(radius * math.cos(a), 12) + 0.0
        dv = round(-radius * math.sin(a), 12) + 0.0
        out.append((du, dv))
    return out


def bilinear(img: Image, x: float, y: float) -> float:
    """Bilinear value at (x, y) = (u, v). Exact for a constant cell."""
    u0 = math.floor(x)
    v0 = math.floor(y)
    fx = x - u0
    fy = y - v0
    if fx == 0.0 and fy == 0.0:
        return img[v0][u0]
    u1 = u0 + 1 if fx > 0.0 else u0
    v1 = v0 + 1 if fy > 0.0 else v0
    a, b = img[v0][u0], img[v0][u1]
    c, d = img[v1][u0], img[v1][u1]
    top = a + fx * (b - a)
    bottom = c + fx * (d - c)
    return top + fy * (bottom - top)


def lbp_codes(img: Image, p_count: int = 8, radius: float = 1.0) -> List[List[int]]:
    """The LBP code of each pixel whose circle lies inside the image.

    Row j of the result holds the codes of the pixels v = m + j, u = m, m + 1, ...
    with the margin m = ceil(R).
    """
    h, w = len(img), len(img[0])
    m = int(math.ceil(radius))
    offs = offsets(p_count, radius)  # @line L1
    rows = []
    for v in range(m, h - m):  # @line L3
        row = []
        for u in range(m, w - m):
            gc = img[v][u]
            code = 0  # @line L4
            for p in range(p_count):  # @line L5
                gp = bilinear(img, u + offs[p][0], v + offs[p][1])  # @line L6
                if round(gp - gc, 9) >= 0:  # @line L7
                    code |= 1 << p
            row.append(code)
        rows.append(row)
    return rows


def lbp_histogram(img: Image, p_count: int = 8, radius: float = 1.0, kind: str = "riu2") -> List[int]:
    """The histogram of the mapped LBP codes over the image."""
    table, nbins = build_mapping(p_count, kind)
    hist = [0] * nbins  # @line L2
    for row in lbp_codes(img, p_count, radius):
        for code in row:
            hist[table[code]] += 1  # @line L8
    return hist  # @line L9


def chi_square(h1: Sequence[float], h2: Sequence[float]) -> float:
    """Chi-square distance sum (a - b)^2 / (a + b), with 0/0 taken as 0."""
    d = 0.0
    for a, b in zip(h1, h2):
        if a + b > 0:
            d += (a - b) * (a - b) / (a + b)
    return d
