# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/harris-affine-detector/. The authors are listed in prov/3SB3Q7.jsonl.

"""Affine shape adaptation of Harris and Hessian points, after Mikolajczyk and Schmid (2004).

An image is a list of H rows of W floats; pixel (u, v) is img[v][u], with u
the column (to the right) and v the row (down). Positions are real numbers
and the image is read with bilinear interpolation and the clamp border rule.

A region is (x, y, sigma_i, U). U = (a, b, c) is the symmetric positive
definite matrix [[a, b], [b, c]] with largest eigenvalue 1. The normalized
patch is W(p) = I((x, y) + U p), and the region is the ellipse of the points
(x, y) + sigma_i U p with |p| <= 1. At a converged region the second moment
matrix of W at its center is close to a multiple of the identity.

Gaussian sums are sampled, cut at radius ceil(3 sigma) and normalized.
"""

import math
from typing import List, Optional, Sequence, Tuple

Sym = Tuple[float, float, float]
Region = Tuple[float, float, float, Sym]

T_VALUES = tuple(0.7 * 1.1 ** j for j in range(8))   # 0.70 to 1.36, the search range for sigma_i
S_VALUES = (0.5, 0.55, 0.6, 0.65, 0.7, 0.75)         # the ratios sigma_d / sigma_i
OFFSETS = [(p, q) for q in (-1, 0, 1) for p in (-1, 0, 1)]


def gaussian_kernel(sigma: float) -> List[float]:
    rad = max(1, int(math.ceil(3 * sigma)))
    k = [math.exp(-(i * i) / (2 * sigma * sigma)) for i in range(-rad, rad + 1)]
    s = sum(k)
    return [x / s for x in k]


def sym_eig(m: Sym) -> Tuple[float, float]:
    """Eigenvalues (smaller, larger) of [[a, b], [b, c]]."""
    a, b, c = m
    mid, rad = (a + c) / 2, math.hypot((a - c) / 2, b)
    return mid - rad, mid + rad


def sym_sqrt(m: Sym) -> Sym:
    """The symmetric positive definite square root of a positive definite m."""
    a, b, c = m
    d = math.sqrt(a * c - b * b)
    t = math.sqrt(a + c + 2 * d)
    return (a + d) / t, b / t, (c + d) / t


def sym_inv(m: Sym) -> Sym:
    a, b, c = m
    det = a * c - b * b
    return c / det, -b / det, a / det


def sym_inv_sqrt(m: Sym) -> Sym:
    return sym_inv(sym_sqrt(m))


def bilinear(img: Sequence[Sequence[float]], x: float, y: float) -> float:
    h, w = len(img), len(img[0])
    x = min(max(x, 0.0), w - 1.0)
    y = min(max(y, 0.0), h - 1.0)
    u0, v0 = min(int(x), w - 2) if w > 1 else 0, min(int(y), h - 2) if h > 1 else 0
    fx, fy = x - u0, y - v0
    u1, v1 = min(u0 + 1, w - 1), min(v0 + 1, h - 1)
    top = img[v0][u0] * (1 - fx) + img[v0][u1] * fx
    bot = img[v1][u0] * (1 - fx) + img[v1][u1] * fx
    return top * (1 - fy) + bot * fy


def warp(img: Sequence[Sequence[float]], x: float, y: float, U: Sym, R: int) -> List[List[float]]:
    """The patch P[R + q][R + p] = I((x, y) + U (p, q)) for -R <= p, q <= R."""
    a, b, c = U
    return [[bilinear(img, x + a * p + b * q, y + b * p + c * q) for p in range(-R, R + 1)]
            for q in range(-R, R + 1)]


def smooth_box(P: List[List[float]], sigma: float, h: int) -> List[List[float]]:
    """The patch blurred by sigma, on the (2h + 1) x (2h + 1) box around its center."""
    n = len(P)
    c = n // 2
    k = gaussian_kernel(sigma)
    r = len(k) // 2
    rows = range(c - h - r, c + h + r + 1)
    tmp = {j: [sum(k[i] * P[min(max(j, 0), n - 1)][min(max(u + i - r, 0), n - 1)] for i in range(len(k)))
               for u in range(c - h, c + h + 1)] for j in rows}
    return [[sum(k[i] * tmp[v + i - r][u] for i in range(len(k))) for u in range(2 * h + 1)]
            for v in range(c - h, c + h + 1)]


def center_laplacian(P: List[List[float]], sigma: float) -> float:
    """sigma^2 |Lxx + Lyy| at the center of the patch, with the 5-point Laplacian."""
    L = smooth_box(P, sigma, 1)
    return sigma * sigma * abs(L[1][2] + L[1][0] + L[2][1] + L[0][1] - 4 * L[1][1])


def moments(P: List[List[float]], si: float, sd: float, offsets=OFFSETS):
    """Second moment matrices and Hessian determinants at the given offsets (at most 1) from the center."""
    ki = gaussian_kernel(si)
    ri = len(ki) // 2
    h = ri + 2
    L = smooth_box(P, sd, h)
    n = 2 * h + 1
    lo, hi = 1, n - 1
    xx, xy, yy = {}, {}, {}
    for v in range(lo, hi):
        for u in range(lo, hi):
            gx = (L[v][u + 1] - L[v][u - 1]) / 2
            gy = (L[v + 1][u] - L[v - 1][u]) / 2
            xx[v, u], xy[v, u], yy[v, u] = gx * gx, gx * gy, gy * gy
    out = {}
    for p, q in offsets:
        u, v = h + p, h + q
        sums = []
        for prod in (xx, xy, yy):
            # Separable Gaussian sum: first along the rows, then down the column.
            rows = [sum(ki[i] * prod[v + j - ri, u + i - ri] for i in range(len(ki))) for j in range(len(ki))]
            sums.append(sum(ki[j] * rows[j] for j in range(len(ki))))
        A, B, C = sums
        dxx = L[v][u + 1] - 2 * L[v][u] + L[v][u - 1]
        dyy = L[v + 1][u] - 2 * L[v][u] + L[v - 1][u]
        dxy = (L[v + 1][u + 1] - L[v + 1][u - 1] - L[v - 1][u + 1] + L[v - 1][u - 1]) / 4
        s2 = sd * sd
        out[(p, q)] = ((s2 * A, s2 * B, s2 * C), s2 * s2 * (dxx * dyy - dxy * dxy))
    return out


def _ratio(m: Sym) -> float:
    lo, hi = sym_eig(m)
    return lo / hi if hi > 0 else 0.0


def adapt_point(img: Sequence[Sequence[float]], x: float, y: float, sigma_i: float, alpha: float = 0.06,
                eps_c: float = 0.05, eps_l: float = 6.0, max_iter: int = 10, measure: str = "harris",
                t_values: Sequence[float] = T_VALUES, s_values: Sequence[float] = S_VALUES) -> Optional[Region]:
    """Adapt one point (x, y) with integration scale sigma_i; None if it is rejected."""
    U = (1.0, 0.0, 1.0)  # @line L3
    for _ in range(max_iter):  # @line L4
        rl = int(math.ceil(3 * sigma_i * max(t_values)))
        R = rl + int(math.ceil(3 * max(s_values) * sigma_i * max(t_values))) + 4
        P = warp(img, x, y, U, R)  # @line L5
        sigma_i = max((sigma_i * t for t in t_values), key=lambda s: center_laplacian(P, s))  # @line L6
        sigma_d = max((s * sigma_i for s in s_values),
                      key=lambda d: _ratio(moments(P, sigma_i, d, [(0, 0)])[(0, 0)][0]))  # @line L7
        mom = moments(P, sigma_i, sigma_d)

        def score(o):
            m, det_h = mom[o]
            return det_h if measure == "hessian" else m[0] * m[2] - m[1] ** 2 - alpha * (m[0] + m[2]) ** 2

        p, q = max(OFFSETS, key=lambda o: (score(o), o == (0, 0)))  # @line L8
        a, b, c = U
        x, y = x + a * p + b * q, y + b * p + c * q
        M = mom[(p, q)][0]  # @line L9
        lo, hi = sym_eig(M)
        if lo <= 1e-12 * max(hi, 1e-300):
            return None
        Pm = sym_inv_sqrt(M)
        e, f, g = Pm
        v11, v12 = a * e + b * f, a * f + b * g  # @line L10
        v21, v22 = b * e + c * f, b * f + c * g
        S = (v11 * v11 + v12 * v12, v11 * v21 + v12 * v22, v21 * v21 + v22 * v22)
        U = sym_sqrt(S)
        ulo, uhi = sym_eig(U)
        U = (U[0] / uhi, U[1] / uhi, U[2] / uhi)
        if uhi / ulo > eps_l:  # @line L11
            return None
        if 1 - _ratio(Pm) < eps_c:  # @line L12
            return x, y, sigma_i, U
    return None


def harris_affine(img: Sequence[Sequence[float]], points: Sequence[Tuple[float, float, float]], **options) -> List[Region]:
    """Adapt each point (x, y, sigma_i), for example from the Harris-Laplace detector.

    Precondition: img is a rectangular list of rows of floats, at least 2 x 2,
    and each sigma_i > 0. Options are passed to adapt_point.
    """
    regions = []  # @line L1
    for x, y, s in points:  # @line L2
        r = adapt_point(img, x, y, s, **options)
        if r is not None:
            regions.append(r)
    return regions  # @line L13
