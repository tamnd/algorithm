# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kaze-features/. The authors are listed in prov/VCC3TB.jsonl.

"""KAZE features (Alcantarilla, Bartoli and Davison): detection and description
in a nonlinear scale space.

An image is a list of H rows of W numbers; pixel (u, v) is img[v][u], with u
the column (to the right) and v the row (down). Angles grow from the u axis
toward the v axis.

1. The image, scaled to [0, 1], is blurred with a Gaussian of sigma_0. The
   contrast k is the 70 percent point of the gradient magnitudes of this image.
2. The levels have sigma_i = sigma_0 2^(o + s / S) and the times
   t_i = sigma_i^2 / 2. Each level comes from the one before by one AOS step
   of the Perona and Malik equation with the conductivity
   g2 = 1 / (1 + |grad L_sigma|^2 / k^2), where L_sigma is the level blurred
   with sigma = 1. There is no downsampling.
3. The response is sigma_i^2 (Lxx Lyy - Lxy^2), with 3 x 3 Scharr filters of
   step round(sigma_i). Keypoints are the strict maxima over 3 x 3 x 3 above a
   threshold, for the levels 1 to N - 2.
4. The orientation is the longest sum of the gradients in a window of pi / 3,
   over a disk of radius 6 sigma sampled with the step sigma.
5. The descriptor is M-SURF: a 24 sigma grid turned by the orientation, 4 x 4
   subregions of 9 sigma with the centers 5 sigma apart, a Gaussian of 2.5 sigma
   in each subregion and a Gaussian of 1.5 subregions over the grid; 64 values
   scaled to unit length.
"""

import math
from typing import List, Sequence, Tuple

Image = Sequence[Sequence[float]]
Map = List[List[float]]


def gaussian_kernel(sigma: float) -> List[float]:
    r = max(1, int(math.ceil(3 * sigma)))
    k = [math.exp(-(x * x) / (2 * sigma * sigma)) for x in range(-r, r + 1)]
    s = sum(k)
    return [x / s for x in k]


def convolve(m: Image, sigma: float) -> Map:
    """Separable Gaussian convolution with the border pixels repeated."""
    k = gaussian_kernel(sigma)
    r = len(k) // 2
    h, w = len(m), len(m[0])
    tmp = [[sum(k[i] * row[min(max(u + i - r, 0), w - 1)] for i in range(len(k))) for u in range(w)] for row in m]
    return [[sum(k[i] * tmp[min(max(v + i - r, 0), h - 1)][u] for i in range(len(k))) for u in range(w)]
            for v in range(h)]


def scharr(m: Image, step: int, axis: int) -> Map:
    """The 3 x 3 Scharr derivative with pixels `step` apart: axis 0 is d/du, axis 1 is d/dv."""
    h, w = len(m), len(m[0])

    def at(u, v):
        return m[min(max(v, 0), h - 1)][min(max(u, 0), w - 1)]

    s = step
    out = []
    for v in range(h):
        row = []
        for u in range(w):
            if axis == 0:
                d = sum(c * (at(u + s, v + t) - at(u - s, v + t)) for c, t in ((3, -s), (10, 0), (3, s)))
            else:
                d = sum(c * (at(u + t, v + s) - at(u + t, v - s)) for c, t in ((3, -s), (10, 0), (3, s)))
            row.append(d / (32.0 * s))
        out.append(row)
    return out


def contrast_factor(L: Image, percentile: float = 0.7) -> float:
    """The given fraction point of the nonzero gradient magnitudes of L."""
    gu, gv = scharr(L, 1, 0), scharr(L, 1, 1)
    mags = sorted(math.hypot(a, b) for ru, rv in zip(gu, gv) for a, b in zip(ru, rv))
    mags = [x for x in mags if x > 0]
    if not mags:
        return 1.0
    return mags[min(len(mags) - 1, int(percentile * len(mags)))]


def conductivity(L: Image, k: float) -> Map:
    Ls = convolve(L, 1.0)
    gu, gv = scharr(Ls, 1, 0), scharr(Ls, 1, 1)
    return [[1.0 / (1.0 + (a * a + b * b) / (k * k)) for a, b in zip(ru, rv)] for ru, rv in zip(gu, gv)]


def thomas(a: List[float], b: List[float], c: List[float], d: List[float]) -> List[float]:
    """Solve the tridiagonal system a_j x_{j-1} + b_j x_j + c_j x_{j+1} = d_j."""
    n = len(d)
    cp, dp = [0.0] * n, [0.0] * n
    cp[0], dp[0] = c[0] / b[0], d[0] / b[0]
    for j in range(1, n):
        den = b[j] - a[j] * cp[j - 1]
        cp[j] = c[j] / den
        dp[j] = (d[j] - a[j] * dp[j - 1]) / den
    x = [0.0] * n
    x[n - 1] = dp[n - 1]
    for j in range(n - 2, -1, -1):
        x[j] = dp[j] - cp[j] * x[j + 1]
    return x


def implicit_1d(f: List[float], g: List[float], tau: float) -> List[float]:
    """Solve (I - tau A) x = f, where (A x)_j = sum over the neighbors n of (g_j + g_n) / 2 (x_n - x_j)."""
    n = len(f)
    w = [(g[j] + g[j + 1]) / 2.0 for j in range(n - 1)]
    a = [0.0] + [-tau * w[j - 1] for j in range(1, n)]
    c = [-tau * w[j] for j in range(n - 1)] + [0.0]
    b = [1.0 + tau * ((w[j - 1] if j > 0 else 0.0) + (w[j] if j < n - 1 else 0.0)) for j in range(n)]
    return thomas(a, b, c, f)


def aos_step(L: Image, g: Image, tau: float) -> Map:
    """One AOS step: the mean of the implicit steps of time 2 tau along the rows and along the columns."""
    h, w = len(L), len(L[0])
    rows = [implicit_1d(list(L[v]), list(g[v]), 2 * tau) for v in range(h)]
    cols = [implicit_1d([L[v][u] for v in range(h)], [g[v][u] for v in range(h)], 2 * tau) for u in range(w)]
    return [[(rows[v][u] + cols[u][v]) / 2.0 for u in range(w)] for v in range(h)]


def level_sigmas(sigma0: float = 1.6, O: int = 4, S: int = 3) -> List[float]:
    return [sigma0 * 2 ** (o + s / S) for o in range(O) for s in range(S)]


def nonlinear_scale_space(img: Image, sigma0: float = 1.6, O: int = 4, S: int = 3) -> Tuple[List[Map], List[float], float]:
    """The levels L_i, their sigma_i and the contrast k."""
    L0 = convolve([[x / 255.0 for x in row] for row in img], sigma0)
    k = contrast_factor(L0)  # @line L1
    sig = level_sigmas(sigma0, O, S)
    levels = [L0]
    for i in range(1, len(sig)):
        g = conductivity(levels[-1], k)  # @line L2
        tau = (sig[i] ** 2 - sig[i - 1] ** 2) / 2.0
        levels.append(aos_step(levels[-1], g, tau))  # @line L3
    return levels, sig, k


def derivatives(L: Image, sigma: float):
    """Lu, Lv and the response sigma^2 (Luu Lvv - Luv^2)."""
    s = max(1, int(round(sigma)))
    lu, lv = scharr(L, s, 0), scharr(L, s, 1)
    luu, lvv, luv = scharr(lu, s, 0), scharr(lv, s, 1), scharr(lu, s, 1)
    det = [[sigma * sigma * (a * b - c * c) for a, b, c in zip(ra, rb, rc)] for ra, rb, rc in zip(luu, lvv, luv)]
    return lu, lv, det  # @line L4


def detect(dets: List[Map], sigmas: List[float], threshold: float = 1e-4):
    """Strict maxima over 3 x 3 x 3 with a response above the threshold: (u, v, i, sigma_i)."""
    out = []
    h, w = len(dets[0]), len(dets[0][0])
    for i in range(1, len(dets) - 1):
        for v in range(1, h - 1):
            for u in range(1, w - 1):
                x = dets[i][v][u]
                if x <= threshold:
                    continue
                if all(dets[j][v + dv][u + du] < x for j in (i - 1, i, i + 1)
                       for dv in (-1, 0, 1) for du in (-1, 0, 1) if (j, dv, du) != (i, 0, 0)):
                    out.append((u, v, i, sigmas[i]))  # @line L5
    return out


def bilinear(m: Image, x: float, y: float) -> float:
    h, w = len(m), len(m[0])
    x = min(max(x, 0.0), w - 1.0)
    y = min(max(y, 0.0), h - 1.0)
    x0, y0 = min(int(x), w - 2), min(int(y), h - 2)
    fx, fy = x - x0, y - y0
    return ((1 - fy) * ((1 - fx) * m[y0][x0] + fx * m[y0][x0 + 1])
            + fy * ((1 - fx) * m[y0 + 1][x0] + fx * m[y0 + 1][x0 + 1]))


def orientation(lu: Image, lv: Image, u: float, v: float, sigma: float) -> float:
    pts = []
    for j in range(-6, 7):
        for i in range(-6, 7):
            if i * i + j * j <= 36:
                wt = math.exp(-(i * i + j * j) / (2 * 2.5 ** 2))
                x, y = u + i * sigma, v + j * sigma
                pts.append((wt * bilinear(lu, x, y), wt * bilinear(lv, x, y)))
    angles = [math.atan2(b, a) for a, b in pts]
    best, best_n = 0.0, -1.0
    for a0 in angles:
        su = sv = 0.0
        for (a, b), t in zip(pts, angles):
            if (t - a0) % (2 * math.pi) < math.pi / 3:
                su, sv = su + a, sv + b
        n = su * su + sv * sv
        if n > best_n:
            best, best_n = math.atan2(sv, su), n
    return best  # @line L6


def describe(lu: Image, lv: Image, u: float, v: float, sigma: float, theta: float) -> List[float]:
    c, s = math.cos(theta), math.sin(theta)
    out = []
    for cy in (-1.5, -0.5, 0.5, 1.5):
        for cx in (-1.5, -0.5, 0.5, 1.5):
            sx = sy = ax = ay = 0.0
            for k in range(-4, 5):
                for l in range(-4, 5):
                    x, y = 5 * cx + l, 5 * cy + k
                    px, py = u + sigma * (c * x - s * y), v + sigma * (s * x + c * y)
                    gu, gv = bilinear(lu, px, py), bilinear(lv, px, py)
                    wt = math.exp(-(l * l + k * k) / (2 * 2.5 ** 2))
                    du, dv = wt * (c * gu + s * gv), wt * (-s * gu + c * gv)
                    sx, sy, ax, ay = sx + du, sy + dv, ax + abs(du), ay + abs(dv)
            g2 = math.exp(-(cx * cx + cy * cy) / (2 * 1.5 ** 2))
            out.extend([g2 * sx, g2 * sy, g2 * ax, g2 * ay])
    n = math.sqrt(sum(x * x for x in out))
    return [x / n for x in out] if n > 0 else out  # @line L7


def kaze(img: Image, sigma0: float = 1.6, O: int = 4, S: int = 3, threshold: float = 1e-4):
    """Keypoints (u, v, sigma, theta) with their 64 values."""
    levels, sig, _ = nonlinear_scale_space(img, sigma0, O, S)
    ders = [derivatives(L, s) for L, s in zip(levels, sig)]
    out = []
    for u, v, i, s in detect([d[2] for d in ders], sig, threshold):
        lu, lv, _ = ders[i]
        theta = orientation(lu, lv, u, v, s)
        out.append(((u, v, s, theta), describe(lu, lv, u, v, s, theta)))
    return out  # @line L8
