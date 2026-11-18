# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/reinhard-tone-mapping/. The authors are listed in prov/FX4QEZ.jsonl.

"""The photographic tone reproduction operator of Reinhard, Stark, Shirley and Ferwerda (2002).

An image is a list of rows of world luminances Lw >= 0. The global operator
scales the image so that its log average luminance maps to the key a, and
then compresses each scaled value L with L (1 + L / Lwhite^2) / (1 + L).
The local operator replaces L in the denominator by a Gaussian average of L
over a neighborhood. It selects the size of the neighborhood per pixel from
a set of center-surround differences of Gaussians.

Constants of the paper: luminance 0.27 R + 0.67 G + 0.06 B, the key 0.18,
phi = 8, epsilon = 0.05, alpha1 = 1 / (2 sqrt 2), a ratio of 1.6 between
scales, and 8 scales. The key, phi and epsilon are tuning, not physics.
"""

import math

ALPHA1 = 1.0 / (2.0 * math.sqrt(2.0))
RATIO = 1.6


def luminance(rgb: tuple[float, float, float]) -> float:
    """The luminance weights that the paper uses."""
    r, g, b = rgb
    return 0.27 * r + 0.67 * g + 0.06 * b


def log_average(lw: list[list[float]], delta: float = 1e-6) -> float:
    """Equation 1: exp of the mean of log(delta + Lw) over all pixels."""
    total = 0.0
    count = 0
    for row in lw:
        for x in row:
            total += math.log(delta + x)
            count += 1
    return math.exp(total / count)


def compress(l: float, l_white: float | None = None) -> float:
    """Equation 4, or Equation 3 when l_white is None (an infinite Lwhite)."""
    if l_white is None:
        return l / (1.0 + l)
    return l * (1.0 + l / (l_white * l_white)) / (1.0 + l)


def scale_image(lw: list[list[float]], key: float, delta: float) -> list[list[float]]:
    """Equation 2: L = (a / Lbar) Lw."""
    lbar = log_average(lw, delta)
    return [[key * x / lbar for x in row] for row in lw]


def reinhard_global(
    lw: list[list[float]],
    key: float = 0.18,
    l_white: float | str | None = None,
    delta: float = 1e-6,
) -> list[list[float]]:
    """The global operator. l_white is a number, None (Equation 3) or "max".

    With "max", Lwhite is the largest scaled luminance of the image, the
    default of the paper, so the brightest pixel maps to exactly 1.
    """
    lbar = log_average(lw, delta)  # @line L1
    scaled = []
    for row in lw:  # @line L2
        scaled.append([key * x / lbar for x in row])  # @line L3
    if l_white == "max":
        l_white = max(max(row) for row in scaled)
    if l_white is not None and l_white <= 0.0:
        l_white = None
    out = [[compress(l, l_white) for l in row] for row in scaled]  # @line L4
    return out  # @line L5


def gaussian_kernel(width: float) -> list[float]:
    """The 1D factor of Equation 5, sampled at integer offsets and normalized.

    R(x, y, s) = exp(-(x^2 + y^2) / (alpha s)^2) / (pi (alpha s)^2) is the
    product of two 1D Gaussians. The kernel is cut at 3 alpha s and scaled
    to sum to 1, so a constant image stays constant.
    """
    radius = max(1, math.ceil(3.0 * width))
    taps = [math.exp(-(t * t) / (width * width)) for t in range(-radius, radius + 1)]
    total = sum(taps)
    return [w / total for w in taps]


def blur(img: list[list[float]], width: float) -> list[list[float]]:
    """Equation 6 as two 1D passes, rows then columns, with clamped borders."""
    k = gaussian_kernel(width)
    radius = len(k) // 2
    h = len(img)
    w = len(img[0])
    tmp = [[0.0] * w for _ in range(h)]
    for y in range(h):
        row = img[y]
        for x in range(w):
            acc = 0.0
            for t in range(-radius, radius + 1):
                xx = min(w - 1, max(0, x + t))
                acc += k[t + radius] * row[xx]
            tmp[y][x] = acc
    out = [[0.0] * w for _ in range(h)]
    for y in range(h):
        for x in range(w):
            acc = 0.0
            for t in range(-radius, radius + 1):
                yy = min(h - 1, max(0, y + t))
                acc += k[t + radius] * tmp[yy][x]
            out[y][x] = acc
    return out


def scales(r: int) -> list[float]:
    """The scales s_k = 1.6^k for k = 0 .. r - 1, in pixels."""
    return [RATIO ** k for k in range(r)]


def reinhard_local(
    lw: list[list[float]],
    key: float = 0.18,
    phi: float = 8.0,
    eps: float = 0.05,
    r: int = 8,
    delta: float = 1e-6,
    return_scales: bool = False,
):
    """The local dodging-and-burning operator, Equations 5 to 9.

    B[k] is the image blurred with the width alpha1 1.6^k. The center of
    scale k is B[k] and its surround is B[k + 1], because alpha2 = 1.6
    alpha1. For each pixel the loop goes up from the smallest scale while
    |V| < eps, and keeps the last scale that passed. If |V| >= eps already
    at the smallest scale, it keeps the smallest scale.
    """
    lbar = log_average(lw, delta)  # @line L6
    lum = [[key * x / lbar for x in row] for row in lw]
    s = scales(r)
    b = [blur(lum, ALPHA1 * RATIO ** k) for k in range(r + 1)]  # @line L7
    h = len(lw)
    w = len(lw[0])
    out = [[0.0] * w for _ in range(h)]
    chosen = [[0] * w for _ in range(h)]
    for y in range(h):  # @line L8
        for x in range(w):
            m = 0  # @line L9
            for k in range(r):  # @line L10
                c = b[k][y][x]
                v = (c - b[k + 1][y][x]) / (key * 2.0 ** phi / (s[k] * s[k]) + c)  # @line L11
                if abs(v) >= eps:  # @line L12
                    break
                m = k
            out[y][x] = min(1.0, lum[y][x] / (1.0 + b[m][y][x]))  # @line L13
            chosen[y][x] = m
    if return_scales:
        return out, chosen
    return out  # @line L14


def tone_map_rgb(
    rgb: list[list[tuple[float, float, float]]], ld: list[list[float]]
) -> list[list[tuple[float, float, float]]]:
    """Scale each color by Ld / Lw, a common way to carry the result to RGB."""
    out = []
    for y, row in enumerate(rgb):
        new = []
        for x, c in enumerate(row):
            lw = luminance(c)
            f = ld[y][x] / lw if lw > 0.0 else 0.0
            new.append((c[0] * f, c[1] * f, c[2] * f))
        out.append(new)
    return out
