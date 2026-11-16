# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shi-tomasi-corner-detector/. The authors are listed in prov/K93XA7.jsonl.

"""Shi-Tomasi corner detector (good features to track), with exact comparisons.

An image is a list of H rows of W integers; pixel (u, v) is img[v][u], with
u the column (to the right) and v the row (down). Reads outside the image
take the nearest edge pixel (clamp border rule).

X and Y are central differences, not divided by 2. The structure tensor
M = [[A, C], [C, B]] sums X^2, Y^2 and X Y with the binomial window of
radius r, (1, 2, 1) in each direction for r = 1. The response is the smaller
eigenvalue of M,

    lam = (A + B) / 2 - sqrt(((A - B) / 2)^2 + C^2).

For integer images A, B and C are integers, and 2 lam = s - sqrt(D) with
s = A + B and D = (A - B)^2 + 4 C^2. The code keeps the pair (s, D) and
compares such numbers exactly with integer arithmetic, so ties and the
threshold test do not depend on rounding.

Selection: keep the pixels with lam > q lam_max that are not smaller than
any of their 8 neighbours, sort them by lam in decreasing order (ties by v,
then u), and accept them greedily when they are at least d away from every
accepted point, up to n points.
"""

from fractions import Fraction
from functools import cmp_to_key
import math
from typing import List, Optional, Sequence, Tuple

Image = Sequence[Sequence[int]]


def binomial_row(radius: int) -> List[int]:
    """Row 2 radius of Pascal's triangle: (1, 2, 1) for radius 1."""
    row = [1]
    for _ in range(2 * radius):
        row = [a + b for a, b in zip([0] + row, row + [0])]
    return row


def _clamp(x: int, lo: int, hi: int) -> int:
    return lo if x < lo else hi if x > hi else x


def gradients(img: Image) -> Tuple[List[List[int]], List[List[int]]]:
    """Central differences X and Y with the clamp border rule."""
    h, w = len(img), len(img[0])
    gx = [[img[v][_clamp(u + 1, 0, w - 1)] - img[v][_clamp(u - 1, 0, w - 1)] for u in range(w)] for v in range(h)]
    gy = [[img[_clamp(v + 1, 0, h - 1)][u] - img[_clamp(v - 1, 0, h - 1)][u] for u in range(w)] for v in range(h)]
    return gx, gy


def _window_sum(field: List[List[int]], weights: List[int]) -> List[List[int]]:
    """Separable weighted sum with the clamp border rule: rows first, then columns."""
    h, w = len(field), len(field[0])
    r = len(weights) // 2
    tmp = [[sum(weights[i] * field[v][_clamp(u + i - r, 0, w - 1)] for i in range(len(weights)))
            for u in range(w)] for v in range(h)]
    return [[sum(weights[j] * tmp[_clamp(v + j - r, 0, h - 1)][u] for j in range(len(weights)))
             for u in range(w)] for v in range(h)]


def structure_tensor(img: Image, radius: int = 1):
    """Return the integer tables (A, B, C)."""
    gx, gy = gradients(img)  # @line L1
    wts = binomial_row(radius)
    xx = [[a * a for a in row] for row in gx]
    yy = [[b * b for b in row] for row in gy]
    xy = [[a * b for a, b in zip(ra, rb)] for ra, rb in zip(gx, gy)]
    return _window_sum(xx, wts), _window_sum(yy, wts), _window_sum(xy, wts)  # @line L2


def _sign_lin(a: int, b: int, n: int) -> int:
    """Sign of a + b sqrt(n) for integers a, b and n >= 0."""
    sa = (a > 0) - (a < 0)
    sb = ((b > 0) - (b < 0)) if n > 0 else 0
    if sb == 0:
        return sa
    if sa == 0 or sa == sb:
        return sb
    t = a * a - b * b * n
    return sa if t > 0 else (-sa if t < 0 else 0)


def compare_roots(p1: int, n1: int, p2: int, n2: int) -> int:
    """Sign of (p1 - sqrt(n1)) - (p2 - sqrt(n2)) for integers with n1, n2 >= 0."""
    e = p1 - p2
    # The sign of x - sqrt(n1) with x = e + sqrt(n2).
    if _sign_lin(e, 1, n2) < 0:
        return -1
    # x >= 0 and sqrt(n1) >= 0, so compare x^2 = e^2 + n2 + 2 e sqrt(n2) with n1.
    return _sign_lin(e * e + n2 - n1, 2 * e, n2)


def min_eigen_pairs(img: Image, radius: int = 1) -> List[List[Tuple[int, int]]]:
    """For each pixel the pair (s, D) with 2 lam = s - sqrt(D)."""
    a, b, c = structure_tensor(img, radius)
    h, w = len(img), len(img[0])
    out = []
    for v in range(h):
        row = []
        for u in range(w):
            aa, bb, cc = a[v][u], b[v][u], c[v][u]
            row.append((aa + bb, (aa - bb) ** 2 + 4 * cc * cc))  # @line L3
        out.append(row)
    return out


def pair_value(pair: Tuple[int, int]) -> float:
    """The eigenvalue lam of a pair (s, D), as a float, for display."""
    s, d = pair
    return (s - math.sqrt(d)) / 2


def shi_tomasi_response(img: Image, radius: int = 1) -> List[List[float]]:
    """The smaller eigenvalue of M at each pixel, as floats."""
    return [[pair_value(p) for p in row] for row in min_eigen_pairs(img, radius)]


def shi_tomasi_corners(img: Image, quality=Fraction(1, 100), min_distance: int = 0,
                       max_corners: Optional[int] = None, radius: int = 1) -> List[Tuple[int, int]]:
    """Return the selected corners (u, v), strongest first.

    Precondition: img is a non-empty rectangular list of integer rows,
    0 <= quality <= 1 (an int or a Fraction), min_distance >= 0 and
    max_corners is None (no limit) or at least 1.
    """
    q = Fraction(quality)
    qa, qb = q.numerator, q.denominator
    lam = min_eigen_pairs(img, radius)
    h, w = len(img), len(img[0])
    best = lam[0][0]
    for row in lam:  # @line L4
        for p in row:
            if compare_roots(p[0], p[1], best[0], best[1]) > 0:
                best = p
    cands = []
    for v in range(h):
        for u in range(w):
            s, d = lam[v][u]
            # lam > q lam_max, both sides multiplied by 2 qb.
            if compare_roots(qb * s, qb * qb * d, qa * best[0], qa * qa * best[1]) <= 0:  # @line L5
                continue
            ok = True
            for dv in (-1, 0, 1):
                for du in (-1, 0, 1):
                    uu, vv = u + du, v + dv
                    if (du or dv) and 0 <= uu < w and 0 <= vv < h:
                        o = lam[vv][uu]
                        if compare_roots(s, d, o[0], o[1]) < 0:
                            ok = False
            if ok:
                cands.append((u, v))

    def stronger_first(p, o):
        lp, lo = lam[p[1]][p[0]], lam[o[1]][o[0]]
        return compare_roots(lo[0], lo[1], lp[0], lp[1])

    # cands is in (v, u) order and the sort is stable, so ties stay in (v, u) order.
    cands.sort(key=cmp_to_key(stronger_first))  # @line L6
    kept: List[Tuple[int, int]] = []  # @line L7
    d2 = min_distance * min_distance
    for u, v in cands:  # @line L8
        if max_corners is not None and len(kept) >= max_corners:  # @line L9
            break
        if all((u - x) ** 2 + (v - y) ** 2 >= d2 for x, y in kept):
            kept.append((u, v))  # @line L10
    return kept  # @line L11
