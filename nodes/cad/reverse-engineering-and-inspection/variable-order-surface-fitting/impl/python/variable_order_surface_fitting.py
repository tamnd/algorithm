# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/variable-order-surface-fitting/. The authors are listed in prov/710BVP.jsonl.

"""Variable-order surface fitting segmentation of a range image, after Besl and Jain.

A range image is a grid Z[i][j] of heights z over the points x = j h, y = i h.
The method has three parts:

1. The HK sign map: at every pixel the mean curvature H and the Gaussian
   curvature K of the graph z = f(x, y) are estimated by a local quadratic fit,
   and the pixel gets one of the eight surface types of (sign H, sign K).
2. Seeds: a seed is a 5 by 5 block of unused pixels of one surface type, the
   one deepest inside its block of equal types.
3. Variable-order growth: a polynomial of total degree d = 1 (planar),
   2 (biquadratic), 3 (bicubic) or 4 (biquartic) is fitted to the region by
   least squares. If its RMS error is above tol, the order goes up; if the
   order is already 4, the seed is rejected. Otherwise the region grows to all
   pixels connected to it through unused pixels whose residual is at most band,
   and the fit is repeated, until the region stops growing.

There is no merging of regions and no refinement of boundaries here.
"""

from collections import deque
from math import sqrt
from typing import List, Optional, Sequence, Set, Tuple

from re1lin import solve

Pixel = Tuple[int, int]
ORDER_NAMES = {1: "planar", 2: "biquadratic", 3: "bicubic", 4: "biquartic"}

# surface types of Besl and Jain by (sign of H, sign of K); H > 0 for a cup z = x^2 + y^2
SURFACE_TYPES = {(-1, 1): "peak", (-1, 0): "ridge", (-1, -1): "saddle ridge", (0, 0): "flat",
                 (0, -1): "minimal", (1, 1): "pit", (1, 0): "valley", (1, -1): "saddle valley"}


def monomials(d: int) -> List[Tuple[int, int]]:
    """The exponents (a, b) of x^a y^b with a + b <= d: (d + 1)(d + 2) / 2 of them."""
    return [(t - b, b) for t in range(d + 1) for b in range(t + 1)]


class Poly:
    """A bivariate polynomial in the shifted and scaled variables u = (x - cx) / s, v = (y - cy) / s."""

    def __init__(self, d: int, coef: Sequence[float], cx: float, cy: float, s: float):
        self.d, self.coef, self.cx, self.cy, self.s = d, list(coef), cx, cy, s
        self.mons = monomials(d)

    def __call__(self, x: float, y: float) -> float:
        u, v = (x - self.cx) / self.s, (y - self.cy) / self.s
        return sum(c * u ** a * v ** b for c, (a, b) in zip(self.coef, self.mons))


def fit_polynomial(pts: Sequence[Tuple[float, float, float]], d: int) -> Tuple[Poly, float]:
    """Least-squares polynomial of total degree d through the points (x, y, z), and its RMS error.

    Uses modified Gram-Schmidt, done twice, on the shifted and scaled monomials.
    Raises ValueError when the points do not determine the polynomial.
    Cost: Theta(n q^2) for n points and q = (d + 1)(d + 2) / 2 unknowns.
    """
    n = len(pts)
    cx = sum(p[0] for p in pts) / n
    cy = sum(p[1] for p in pts) / n
    s = max(max(abs(p[0] - cx), abs(p[1] - cy)) for p in pts) or 1.0
    mons = monomials(d)
    q = len(mons)
    if n < q:
        raise ValueError("too few points for this order")
    uv = [((p[0] - cx) / s, (p[1] - cy) / s) for p in pts]
    cols = [[u ** a * v ** b for u, v in uv] for a, b in mons]
    R = [[0.0] * q for _ in range(q)]
    for k in range(q):
        size = sqrt(sum(x * x for x in cols[k]))
        for _ in range(2):
            for i in range(k):
                r = sum(a * b for a, b in zip(cols[i], cols[k]))
                R[i][k] += r
                cols[k] = [b - r * a for a, b in zip(cols[i], cols[k])]
        nk = sqrt(sum(x * x for x in cols[k]))
        if nk <= 1e-10 * size:
            raise ValueError("the points do not determine a polynomial of this order")
        R[k][k] = nk
        cols[k] = [x / nk for x in cols[k]]
    z = [p[2] for p in pts]
    qz = [sum(a * b for a, b in zip(c, z)) for c in cols]
    coef = [0.0] * q
    for k in range(q - 1, -1, -1):
        coef[k] = (qz[k] - sum(R[k][j] * coef[j] for j in range(k + 1, q))) / R[k][k]
    f = Poly(d, coef, cx, cy, s)
    rms = sqrt(sum((f(x, y) - zz) ** 2 for x, y, zz in pts) / n)
    return f, rms


# ---- the HK sign map ----


def curvatures(fx: float, fy: float, fxx: float, fxy: float, fyy: float) -> Tuple[float, float]:
    """Mean and Gaussian curvature of the graph z = f(x, y), with the normal pointing up."""
    g = 1 + fx * fx + fy * fy
    H = ((1 + fy * fy) * fxx - 2 * fx * fy * fxy + (1 + fx * fx) * fyy) / (2 * g ** 1.5)
    K = (fxx * fyy - fxy * fxy) / (g * g)
    return H, K


def hk_map(Z: Sequence[Sequence[float]], h: float, eps_h: float, eps_k: float, half: int = 2
           ) -> List[List[Optional[str]]]:
    """Surface type of every pixel from a local quadratic fit on a (2 half + 1)^2 window; None near the border."""
    rows, cols = len(Z), len(Z[0])
    offs = [(di, dj) for di in range(-half, half + 1) for dj in range(-half, half + 1)]
    # the quadratic fit on the window is one fixed linear filter per coefficient
    basis = [(1.0, dj * h, di * h, (dj * h) ** 2, dj * h * di * h, (di * h) ** 2) for di, dj in offs]
    A =[[sum(b[r] * b[c] for b in basis) for c in range(6)] for r in range(6)]
    filters = []
    for k in range(6):
        e = [1.0 if r == k else 0.0 for r in range(6)]
        w = solve(A, e)                                     # row k of A^{-1}
        filters.append([sum(w[r] * b[r] for r in range(6)) for b in basis])
    types: List[List[Optional[str]]] = [[None] * cols for _ in range(rows)]
    for i in range(half, rows - half):
        for j in range(half, cols - half):
            vals = [Z[i + di][j + dj] for di, dj in offs]
            c = [sum(f * z for f, z in zip(filt, vals)) for filt in filters]
            H, K = curvatures(c[1], c[2], 2 * c[3], c[4], 2 * c[5])
            sh = 0 if abs(H) <= eps_h else (1 if H > 0 else -1)
            sk = 0 if abs(K) <= eps_k else (1 if K > 0 else -1)
            types[i][j] = SURFACE_TYPES.get((sh, sk))        # (0, +1) cannot occur exactly; it gets None
    return types


# ---- seeds and growth ----


def pick_seed(types: List[List[Optional[str]]], blocked: Set[Pixel], radius: int = 2) -> Optional[Set[Pixel]]:
    """The (2 radius + 1)^2 block around the pixel deepest inside a block of one surface type."""
    rows, cols = len(types), len(types[0])

    def ok(i, j):
        return types[i][j] is not None and (i, j) not in blocked

    depth = [[1 if ok(i, j) else 0 for j in range(cols)] for i in range(rows)]
    level = 1
    while True:
        nxt = [[0] * cols for _ in range(rows)]
        changed = False
        for i in range(1, rows - 1):
            for j in range(1, cols - 1):
                if depth[i][j] >= level and all(depth[i + a][j + b] >= level and types[i + a][j + b] == types[i][j]
                                                for a in (-1, 0, 1) for b in (-1, 0, 1)):
                    nxt[i][j] = 1
                    changed = True
        if not changed:
            break
        for i in range(rows):
            for j in range(cols):
                if nxt[i][j]:
                    depth[i][j] = level + 1
        level += 1
    best = max(((depth[i][j], -i, -j) for i in range(rows) for j in range(cols)), default=(0, 0, 0))
    if best[0] < radius + 1:
        return None
    ci, cj = -best[1], -best[2]
    return {(ci + a, cj + b) for a in range(-radius, radius + 1) for b in range(-radius, radius + 1)}


def grow_region(Z: Sequence[Sequence[float]], h: float, seed: Set[Pixel], used: Set[Pixel], tol: float,
                band: float, max_order: int = 4) -> Optional[Tuple[Set[Pixel], Poly, int]]:
    """Variable-order region growing from a seed: (region, polynomial, order), or None if no order fits."""
    rows, cols = len(Z), len(Z[0])
    R, d = set(seed), 1                                                        # @line L3
    while True:
        f, rms = fit_polynomial([(j * h, i * h, Z[i][j]) for i, j in sorted(R)], d)  # @line L4
        if rms > tol:
            if d == max_order:
                return None
            d += 1                                                             # @line L5
            continue
        grown, queue = set(R), deque(R)                                        # @line L6
        while queue:
            i, j = queue.popleft()
            for a, b in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
                if 0 <= a < rows and 0 <= b < cols and (a, b) not in grown and (a, b) not in used \
                        and abs(Z[a][b] - f(b * h, a * h)) <= band:
                    grown.add((a, b))
                    queue.append((a, b))
        if len(grown) == len(R):                                               # @line L7
            return R, f, d
        R = grown


def variable_order_segmentation(Z: Sequence[Sequence[float]], h: float, tol: float, band: float,
                                eps_h: float = 1e-6, eps_k: float = 1e-6, max_order: int = 4
                                ) -> List[Tuple[Set[Pixel], Poly, int]]:
    """Segment a range image into regions, each with a polynomial of order 1 to max_order.

    Precondition: Z is a rectangular grid of heights with spacing h; tol is the
    largest RMS error accepted for a region and band >= tol the largest residual
    of a pixel added to a region. Cost: Theta(N w^2) for the HK map on N pixels
    with a w by w window, plus Theta(N r) per seed search with r the largest
    depth, plus Theta(|R| q^2) per fit with q <= 15 unknowns.
    """
    types = hk_map(Z, h, eps_h, eps_k)                                         # @line L1
    used: Set[Pixel] = set()
    blocked: Set[Pixel] = set()
    regions = []
    while True:
        seed = pick_seed(types, blocked)                                       # @line L2
        if seed is None:
            break
        blocked |= seed
        result = grow_region(Z, h, seed, used, tol, band, max_order)
        if result is not None:
            region = result[0]
            regions.append(result)
            used |= region
            blocked |= region
    return regions                                                             # @line L8
