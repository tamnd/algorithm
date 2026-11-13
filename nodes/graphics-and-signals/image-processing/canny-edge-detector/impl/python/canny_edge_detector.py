# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/canny-edge-detector/. The authors are listed in prov/XAAHCF.jsonl.

"""The Canny edge detector: Gaussian derivative, non-maximum suppression, hysteresis.

An image is a list of H rows of W numbers, with pixel (x, y) at [y][x], x to
the right and y downward. Reads outside the image use the nearest border pixel
(clamp). The thresholds low and high are on the gradient magnitude, in
intensity units per pixel. The output is an H by W mask of booleans.
"""

import math

Grid = list[list[float]]
STEPS = ((1, 0), (1, 1), (0, 1), (-1, 1))
NEIGHBORS = ((-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1))


def gaussian_kernels(sigma: float) -> tuple[list[float], list[float], int]:
    """Return (g, d, r): the sampled Gaussian with sum 1 and its sampled derivative,
    scaled so that the derivative of the ramp I(x) = x is exactly 1, on offsets -r..r."""
    if sigma <= 0:
        raise ValueError("sigma must be positive")
    r = max(1, math.ceil(3 * sigma))
    raw = [math.exp(-(k * k) / (2 * sigma * sigma)) for k in range(-r, r + 1)]
    total = sum(raw)
    g = [v / total for v in raw]
    second = sum(k * k * g[k + r] for k in range(-r, r + 1))
    d = [k * g[k + r] / second for k in range(-r, r + 1)]
    return g, d, r


def _rows(image: Grid, kernel: list[float], r: int) -> Grid:
    h, w = len(image), len(image[0])
    return [[sum(kernel[k + r] * image[y][min(max(x + k, 0), w - 1)] for k in range(-r, r + 1))
             for x in range(w)] for y in range(h)]


def _cols(image: Grid, kernel: list[float], r: int) -> Grid:
    h, w = len(image), len(image[0])
    return [[sum(kernel[k + r] * image[min(max(y + k, 0), h - 1)][x] for k in range(-r, r + 1))
             for x in range(w)] for y in range(h)]


def gradient(image: Grid, sigma: float) -> tuple[Grid, Grid]:
    """Return (gx, gy), the image correlated with the x and y derivatives of a Gaussian."""
    g, d, r = gaussian_kernels(sigma)
    gx = _cols(_rows(image, d, r), g, r)
    gy = _rows(_cols(image, d, r), g, r)
    return gx, gy


def sector(gx: float, gy: float) -> int:
    """Direction sector 0, 1, 2, 3 for 0, 45, 90, 135 degrees; see non-maximum-suppression."""
    ax, ay = abs(gx), abs(gy)
    s = (ax + ay) * (ax + ay)
    if s < 2 * ax * ax:
        return 0
    if s < 2 * ay * ay:
        return 2
    return 1 if gx * gy > 0 else 3


def suppress(gx: Grid, gy: Grid) -> Grid:
    """Keep the squared magnitude m where m(p) > m(p - d) and m(p) >= m(p + d); border pixels are dropped."""
    h, w = len(gx), len(gx[0])
    m = [[gx[y][x] ** 2 + gy[y][x] ** 2 for x in range(w)] for y in range(h)]
    out = [[0.0] * w for _ in range(h)]
    for y in range(1, h - 1):
        for x in range(1, w - 1):
            if m[y][x] == 0:
                continue
            dx, dy = STEPS[sector(gx[y][x], gy[y][x])]
            if m[y][x] > m[y - dy][x - dx] and m[y][x] >= m[y + dy][x + dx]:
                out[y][x] = m[y][x]
    return out


def suppress_interpolated(gx: Grid, gy: Grid) -> Grid:
    """Variant: compare the magnitude with its bilinear interpolation at p - u and p + u,
    where u is the unit gradient direction. Returns the squared magnitude where kept."""
    h, w = len(gx), len(gx[0])
    m = [[math.hypot(gx[y][x], gy[y][x]) for x in range(w)] for y in range(h)]

    def sample(px: float, py: float) -> float:
        x0, y0 = math.floor(px), math.floor(py)
        fx, fy = px - x0, py - y0
        x1, y1 = min(x0 + 1, w - 1), min(y0 + 1, h - 1)
        top = (1 - fx) * m[y0][x0] + fx * m[y0][x1]
        bottom = (1 - fx) * m[y1][x0] + fx * m[y1][x1]
        return (1 - fy) * top + fy * bottom

    out = [[0.0] * w for _ in range(h)]
    for y in range(1, h - 1):
        for x in range(1, w - 1):
            mp = m[y][x]
            if mp == 0:
                continue
            ux, uy = gx[y][x] / mp, gy[y][x] / mp
            if mp > sample(x - ux, y - uy) and mp >= sample(x + ux, y + uy):
                out[y][x] = mp * mp
    return out


def hysteresis(strength: Grid, low: float, high: float) -> list[list[bool]]:
    """Keep each pixel >= low that an 8-connected path of pixels >= low joins to a pixel >= high."""
    h, w = len(strength), len(strength[0])
    edge = [[False] * w for _ in range(h)]
    stack = []
    for y in range(h):
        for x in range(w):
            if strength[y][x] >= high:
                edge[y][x] = True
                stack.append((x, y))
    while stack:
        x, y = stack.pop()
        for dx, dy in NEIGHBORS:
            xx, yy = x + dx, y + dy
            if 0 <= xx < w and 0 <= yy < h and not edge[yy][xx] and strength[yy][xx] >= low:
                edge[yy][xx] = True
                stack.append((xx, yy))
    return edge


def canny(image: Grid, sigma: float, low: float, high: float, interpolate: bool = False) -> list[list[bool]]:
    """Return the Canny edge mask. Requires sigma > 0 and 0 < low <= high.

    With interpolate=False the suppression uses the four quantized directions;
    with interpolate=True it uses the bilinear variant."""
    if not 0 < low <= high:
        raise ValueError("need 0 < low <= high")
    if not image or not image[0]:
        return []
    gx, gy = gradient(image, sigma)  # @line L1
    thin = suppress_interpolated(gx, gy) if interpolate else suppress(gx, gy)  # @line L2
    return hysteresis(thin, low * low, high * high)  # @line L3
