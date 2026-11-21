# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/siddon-algorithm/. The authors are listed in prov/3SDE4K.jsonl.
"""Siddon's algorithm: exact intersection lengths of a ray with a pixel grid.

Conventions:
- The image is n x n on the square [-1, 1]^2, stored as img[i][j] with row i
  from the top and column j from the left. Column j covers
  x in [-1 + 2 j / n, -1 + 2 (j + 1) / n] and row i covers
  y in [1 - 2 (i + 1) / n, 1 - 2 i / n], so y goes up.
- A ray is the segment p(alpha) = p0 + alpha (p1 - p0), 0 <= alpha <= 1.
- The code works with float or with fractions.Fraction coordinates. With
  Fraction input every alpha is exact, and the lengths are exact when the
  length of p1 - p0 is rational (for example a 3-4-5 direction).
"""

import math
from fractions import Fraction


def seg_length(dx, dy):
    """The length of (dx, dy): exact for Fraction input with a rational length."""
    if isinstance(dx, Fraction) or isinstance(dy, Fraction):
        q = Fraction(dx) ** 2 + Fraction(dy) ** 2
        rn, rd = math.isqrt(q.numerator), math.isqrt(q.denominator)
        if rn * rn == q.numerator and rd * rd == q.denominator:
            return Fraction(rn, rd)
        return math.sqrt(q)
    return math.hypot(dx, dy)


def _plane_alphas(n, c0, dc, a_lo, a_hi):
    """The alphas in (a_lo, a_hi) where c0 + alpha dc meets a plane -1 + 2 k / n, in increasing order."""
    if dc == 0:
        return []
    u_lo = n * (c0 + a_lo * dc + 1) / 2  # the plane index at a_lo, as a real number
    u_hi = n * (c0 + a_hi * dc + 1) / 2
    k_first, k_last = math.floor(min(u_lo, u_hi)) + 1, math.ceil(max(u_lo, u_hi)) - 1
    ks = range(k_first, k_last + 1) if dc > 0 else range(k_last, k_first - 1, -1)
    if isinstance(dc, Fraction) or isinstance(c0, Fraction):
        return [(Fraction(2 * k, n) - 1 - c0) / dc for k in ks]
    return [(-1.0 + 2.0 * k / n - c0) / dc for k in ks]


def _merge(xs, ys):
    """Merge two increasing lists into one increasing list."""
    out, p, q = [], 0, 0
    while p < len(xs) and q < len(ys):
        if xs[p] <= ys[q]:
            out.append(xs[p])
            p += 1
        else:
            out.append(ys[q])
            q += 1
    return out + xs[p:] + ys[q:]


def siddon_ray(n, p0, p1):
    """The list of (i, j, length) of the pixels that the segment p0 -> p1 crosses, in ray order.

    A ray that lies on a grid line gives its length to the pixels on the
    right of it (for a vertical line) or below it (for a horizontal line).
    """
    (x0, y0), (x1, y1) = p0, p1
    dx, dy = x1 - x0, y1 - y0  # @line L1
    dist = seg_length(dx, dy)
    a_min, a_max = 0, 1  # @line L2
    for c0, dc in ((x0, dx), (y0, dy)):
        if dc == 0:
            if not -1 <= c0 < 1:
                return []
            continue
        a_a, a_b = (-1 - c0) / dc, (1 - c0) / dc
        a_min, a_max = max(a_min, min(a_a, a_b)), min(a_max, max(a_a, a_b))
    if a_min >= a_max:  # @line L3
        return []
    ax = _plane_alphas(n, x0, dx, a_min, a_max)  # @line L4
    ay = _plane_alphas(n, y0, dy, a_min, a_max)  # @line L5
    alphas = [a_min] + _merge(ax, ay) + [a_max]  # @line L6
    out = []
    for a_prev, a_next in zip(alphas, alphas[1:]):  # @line L7
        if a_next <= a_prev:
            continue  # a ray through a grid corner meets two planes at one alpha
        a_mid = (a_prev + a_next) / 2  # @line L8
        xm, ym = x0 + a_mid * dx, y0 + a_mid * dy
        j = min(n - 1, max(0, math.floor(n * (xm + 1) / 2)))  # @line L9
        i = min(n - 1, max(0, math.floor(n * (1 - ym) / 2)))
        out.append((i, j, (a_next - a_prev) * dist))  # @line L10
    return out


def parallel_rays(angles, nbins):
    """One ray per angle and bin, on the line x cos(theta) + y sin(theta) = s_b.

    The bins cover [-sqrt(2), sqrt(2)] with centers s_b = -sqrt(2) + (b + 1/2) w,
    w = 2 sqrt(2) / nbins, as in the pixel-driven projector of imgkit. Each ray
    runs from s omega - 2 omega_perp to s omega + 2 omega_perp, so it crosses the
    whole square. Ray k * nbins + b holds angle k and bin b.
    """
    smax = math.sqrt(2.0)
    width = 2.0 * smax / nbins
    rays = []
    for theta in angles:
        c, s = math.cos(theta), math.sin(theta)
        for b in range(nbins):
            sb = -smax + (b + 0.5) * width
            rays.append(((sb * c + 2.0 * s, sb * s - 2.0 * c), (sb * c - 2.0 * s, sb * s + 2.0 * c)))
    return rays


def siddon_project(img, rays):
    """The ray sums: for each ray, the sum over its pixels of length times value."""
    n = len(img)
    return [sum(w * img[i][j] for i, j, w in siddon_ray(n, p0, p1)) for p0, p1 in rays]


def siddon_back_project(n, rays, values):
    """The adjoint of siddon_project: each ray adds length times its value to its pixels."""
    out = [[0.0] * n for _ in range(n)]
    for (p0, p1), v in zip(rays, values):
        for i, j, w in siddon_ray(n, p0, p1):
            out[i][j] += w * v
    return out


def siddon_matrix(n, rays):
    """The system matrix as sparse rows of (column, weight) pairs, column i * n + j."""
    return [sorted((i * n + j, w) for i, j, w in siddon_ray(n, p0, p1)) for p0, p1 in rays]
