# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hammersley-sampling-for-cmm/. The authors are listed in prov/9X9MZP.jsonl.

"""Hammersley sampling of a surface patch for coordinate measurement.

The Hammersley set of N points in the unit square is (i/N, phi_2(i)) for
i = 0, ..., N-1, where phi_2 reverses the binary digits of i about the
binary point. Woo and Liang (1993) proposed it to place the probe points of a
coordinate measuring machine on a surface. The points are mapped to a
rectangle or through a parameterization of the patch.

All coordinates are exact Fractions. The module also has the exact star
discrepancy of a planar point set by brute force, for checks.
"""

from fractions import Fraction
from math import log

PRIMES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29)


def radical_inverse(i, base=2):
    """phi_b(i): the base-b digits of i mirrored about the radix point."""
    if i < 0 or base < 2:
        raise ValueError("need i >= 0 and base >= 2")
    num, den = 0, 1
    while i > 0:
        i, digit = divmod(i, base)
        num = num * base + digit
        den *= base
    return Fraction(num, den)


def hammersley(n, dim=2):
    """The n-point Hammersley set in [0, 1)^dim, as tuples of Fractions.

    The first coordinate is i/n and coordinate k + 1 is the radical inverse
    of i in the k-th prime base.
    """
    if n < 1 or not 1 <= dim <= len(PRIMES) + 1:
        raise ValueError("bad n or dim")
    pts = []
    for i in range(n):  # @line L1
        u = Fraction(i, n)  # @line L2
        rest = tuple(radical_inverse(i, PRIMES[k]) for k in range(dim - 1))  # @line L3
        pts.append((u,) + rest)
    return pts


def probe_points_on_rectangle(n, x0, y0, width, height):
    """Hammersley probe points (x, y) on the rectangle [x0, x0+width) x [y0, y0+height)."""
    return [(x0 + u * width, y0 + v * height) for u, v in hammersley(n, 2)]  # @line L4


def probe_points_on_patch(n, surface):
    """Hammersley probe points on a patch surface(u, v) with (u, v) in [0, 1)^2.

    The map should be close to area preserving, or the points crowd where it
    shrinks area.
    """
    return [surface(u, v) for u, v in hammersley(n, 2)]  # @line L5


def star_discrepancy_2d(points):
    """Exact star discrepancy of points in [0, 1)^2.

    D* = sup over boxes [0, x) x [0, y) of |count / N - x y|. The supremum is
    approached at x and y taken from the point coordinates and 1: with open
    boxes from above (count too small) and closed boxes from below (count
    too large). Time O(N^3).
    """
    pts = [(Fraction(x), Fraction(y)) for x, y in points]
    n = len(pts)
    xs = sorted({x for x, _ in pts} | {Fraction(1)})
    ys = sorted({y for _, y in pts} | {Fraction(1)})
    best = Fraction(0)
    for x in xs:
        for y in ys:
            vol = x * y
            open_count = sum(1 for p, q in pts if p < x and q < y)
            closed_count = sum(1 for p, q in pts if p <= x and q <= y)
            best = max(best, vol - Fraction(open_count, n), Fraction(closed_count, n) - vol)
    return best


def niederreiter_bound(n, dim=2):
    """Niederreiter's bound (Theorem 3.8) on the star discrepancy of the
    n-point Hammersley set in the first dim - 1 prime bases:
    dim/n + (1/n) prod_k ((b_k - 1)/(2 log b_k) log n + (b_k + 1)/2)."""
    prod = 1.0
    for k in range(dim - 1):
        b = PRIMES[k]
        prod *= (b - 1) / (2 * log(b)) * log(n) + (b + 1) / 2
    return dim / n + prod / n


def net_bound(m):
    """The bound (m + 1)/2^m for the base-2 Hammersley set of 2^m points,
    proved on the correctness page from the net property."""
    return Fraction(m + 1, 2 ** m)


if __name__ == "__main__":
    for n in (4, 16, 64):
        d = star_discrepancy_2d(hammersley(n))
        print(n, float(d), niederreiter_bound(n))
