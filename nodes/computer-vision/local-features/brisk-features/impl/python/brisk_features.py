# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/brisk-features/. The authors are listed in prov/7MW0CV.jsonl.

"""BRISK: binary robust invariant scalable keypoints (Leutenegger, Chli and Siegwart, 2011).

An image is a list of H rows of W numbers; pixel (u, v) is img[v][u], with u
the column (to the right) and v the row (down). Angles are atan2(dv, du).

Detector (simplified, see the page): layers c_0, d_0, c_1, d_1, ... with the
scales 1, 1.5, 2, 3, 4, 6, ...; on each layer the FAST 9-16 score s, the
largest threshold for which the pixel is still a corner. A keypoint is a point
with s above a threshold that is larger than its 8 neighbors and than the
scores of the layers above and below near the same place; its scale is refined
by a parabola through the three scores.

Descriptor: the pattern of 60 points on rings with the radii
0.85 (0, 2.9, 4.9, 7.4, 10.8) and the counts 1, 10, 14, 15, 20, scaled by the
keypoint scale t. Each point is sampled with a Gaussian of sigma about
1.3 r sin(pi / n) for its ring, our choice in the spirit of the paper (sigma
grows with the spacing of the points). Short pairs (distance < 5.85 t) give
the 512 bits, long pairs (distance > 8.2 t) give the local gradient and so the
orientation. These two thresholds are the values of the OpenCV pattern; the
paper gives 9.75 t and 13.67 t in its own units.
"""

import math
from typing import List, Sequence, Tuple

Image = Sequence[Sequence[float]]

RADII = tuple(0.85 * r for r in (0.0, 2.9, 4.9, 7.4, 10.8))
COUNTS = (1, 10, 14, 15, 20)
D_MAX = 5.85
D_MIN = 8.2
OFFSETS = [(0, -3), (1, -3), (2, -2), (3, -1), (3, 0), (3, 1), (2, 2), (1, 3),
           (0, 3), (-1, 3), (-2, 2), (-3, 1), (-3, 0), (-3, -1), (-2, -2), (-1, -3)]


def pattern() -> List[Tuple[float, float, float]]:
    """The 60 points (x, y, sigma) of the pattern at scale 1."""
    pts = []
    for r, n in zip(RADII, COUNTS):
        sigma = 0.5 if n == 1 else 1.3 * r * math.sin(math.pi / n)
        for k in range(n):
            a = 2 * math.pi * k / n
            pts.append((r * math.cos(a), r * math.sin(a), sigma))
    return pts


def pairs(pts=None):
    """(short pairs, long pairs) as lists of index pairs (i, j) with i < j."""
    pts = pts or pattern()
    short, long_ = [], []
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            d = math.hypot(pts[j][0] - pts[i][0], pts[j][1] - pts[i][1])
            if d < D_MAX:
                short.append((i, j))
            elif d > D_MIN:
                long_.append((i, j))
    return short, long_


SHORT, LONG = pairs()


def sample(img: Image, x: float, y: float, sigma: float) -> float:
    """Gaussian weighted mean of the pixels within 3 sigma (at least 1) of (x, y)."""
    h, w = len(img), len(img[0])
    rad = max(1.0, 3.0 * sigma)
    num = den = 0.0
    for v in range(max(0, math.ceil(y - rad)), min(h - 1, math.floor(y + rad)) + 1):
        for u in range(max(0, math.ceil(x - rad)), min(w - 1, math.floor(x + rad)) + 1):
            d2 = (u - x) ** 2 + (v - y) ** 2
            if d2 <= rad * rad:
                wt = math.exp(-d2 / (2 * sigma * sigma))
                num += wt * img[v][u]
                den += wt
    return num / den


def sample_pattern(img: Image, u: float, v: float, t: float, alpha: float = 0.0) -> List[float]:
    """The smoothed intensities of the pattern at (u, v), scale t, turned by alpha."""
    c, s = math.cos(alpha), math.sin(alpha)
    return [sample(img, u + t * (c * x - s * y), v + t * (s * x + c * y), t * sg)  # @line L3
            for x, y, sg in pattern()]


def orientation(img: Image, u: float, v: float, t: float) -> float:
    """alpha = atan2(g_y, g_x), g the mean local gradient over the long pairs."""
    pts = pattern()
    vals = sample_pattern(img, u, v, t)
    gx = gy = 0.0
    for i, j in LONG:
        dx, dy = t * (pts[j][0] - pts[i][0]), t * (pts[j][1] - pts[i][1])
        k = (vals[j] - vals[i]) / (dx * dx + dy * dy)
        gx += dx * k
        gy += dy * k  # @line L4
    return math.atan2(gy / len(LONG), gx / len(LONG))  # @line L5


def describe(img: Image, u: float, v: float, t: float, alpha: float) -> int:
    """The 512-bit descriptor: bit k is 1 when I(p_j) > I(p_i) for the short pair k."""
    vals = sample_pattern(img, u, v, t, alpha)  # @line L6
    d = 0
    for k, (i, j) in enumerate(SHORT):
        if vals[j] > vals[i]:
            d |= 1 << k  # @line L7
    return d


def fast_score(img: Image, u: int, v: int) -> float:
    """The FAST 9-16 score: the pixel is a corner for a threshold t exactly when t < score."""
    p = img[v][u]
    ring = [img[v + dv][u + du] - p for du, dv in OFFSETS]
    ring += ring[:8]
    neg = [-x for x in ring]
    best = 0.0
    for j in range(16):
        best = max(best, min(ring[j:j + 9]), min(neg[j:j + 9]))
    return best


def is_corner(img: Image, u: int, v: int, t: float) -> bool:
    p = img[v][u]
    for sign in (1, -1):
        run = 0
        for k in range(32):
            q = img[v + OFFSETS[k % 16][1]][u + OFFSETS[k % 16][0]]
            run = run + 1 if sign * (q - p) > t else 0
            if run >= 9:
                return True
    return False


def downsample(img: Image, factor: float) -> List[List[float]]:
    """Mean of the source area of each target pixel (box filter), by factor 2 or 1.5."""
    h, w = len(img), len(img[0])
    nh, nw = int(h / factor), int(w / factor)
    out = []
    for v in range(nh):
        y0, y1 = v * factor, (v + 1) * factor
        row = []
        for u in range(nw):
            x0, x1 = u * factor, (u + 1) * factor
            num = 0.0
            for yy in range(int(y0), min(h, math.ceil(y1))):
                wy = min(y1, yy + 1) - max(y0, yy)
                for xx in range(int(x0), min(w, math.ceil(x1))):
                    wx = min(x1, xx + 1) - max(x0, xx)
                    num += wy * wx * img[yy][xx]
            row.append(num / (factor * factor))
        out.append(row)
    return out


def layers(img: Image, n: int = 4):
    """The layers c_0, d_0, c_1, d_1, ... with their scales 1, 1.5, 2, 3, ..."""
    out = []
    c, d = [list(map(float, row)) for row in img], downsample(img, 1.5)
    scale = 1.0
    while len(out) < n:
        out.append((c, scale))
        if len(out) < n:
            out.append((d, 1.5 * scale))
        c, d = downsample(c, 2.0), downsample(d, 2.0)
        scale *= 2.0
        if len(c) < 8 or len(c[0]) < 8:
            break
    return out


def detect(img: Image, threshold: float = 20.0, n_layers: int = 4, margin: int = 3):
    """Keypoints (u, v, t, score) in the coordinates of img."""
    ls = layers(img, n_layers)
    maps = []
    for lay, _ in ls:
        h, w = len(lay), len(lay[0])
        maps.append([[fast_score(lay, u, v) if 3 <= u < w - 3 and 3 <= v < h - 3 else 0.0
                      for u in range(w)] for v in range(h)])  # @line L1

    def score_near(k, x, y):
        """The largest score of layer k in the 3 x 3 pixels around the image point (x, y)."""
        m, sc = maps[k], ls[k][1]
        cu, cv = int(round((x + 0.5) / sc - 0.5)), int(round((y + 0.5) / sc - 0.5))
        best = 0.0
        for v in range(cv - 1, cv + 2):
            for u in range(cu - 1, cu + 2):
                if 0 <= v < len(m) and 0 <= u < len(m[0]):
                    best = max(best, m[v][u])
        return best

    out = []
    for k, (lay, sc) in enumerate(ls):
        m = maps[k]
        h, w = len(m), len(m[0])
        for v in range(margin, h - margin):
            for u in range(margin, w - margin):
                s = m[v][u]
                if s <= threshold:
                    continue
                # A neighbor with the same score wins when it comes first in raster order.
                if any(m[v + dv][u + du] > s or (m[v + dv][u + du] == s and (dv, du) < (0, 0))
                       for du in (-1, 0, 1) for dv in (-1, 0, 1) if du or dv):
                    continue
                x, y = (u + 0.5) * sc - 0.5, (v + 0.5) * sc - 0.5
                below = score_near(k - 1, x, y) if k > 0 else 0.0
                above = score_near(k + 1, x, y) if k + 1 < len(ls) else 0.0
                if below > s or above > s:
                    continue
                # Vertex of the parabola through (lo, below), (mid, s), (hi, above) in log scale.
                # A missing layer counts as score 0 at the scale 1.5 times smaller or larger.
                mid = math.log(sc)
                lo = math.log(ls[k - 1][1]) if k > 0 else mid - math.log(1.5)
                hi = math.log(ls[k + 1][1]) if k + 1 < len(ls) else mid + math.log(1.5)
                num = (mid - lo) ** 2 * (s - above) - (mid - hi) ** 2 * (s - below)
                den = (mid - lo) * (s - above) - (mid - hi) * (s - below)
                best = min(max(mid - 0.5 * num / den, lo), hi) if den > 0 else mid
                out.append((x, y, math.exp(best), s))  # @line L2
    return out


def brisk(img: Image, threshold: float = 20.0, n_layers: int = 4):
    """Keypoints (u, v, t, alpha) with their 512-bit descriptors; points too near the border are skipped."""
    h, w = len(img), len(img[0])
    out = []
    for u, v, t, _ in detect(img, threshold, n_layers):
        reach = t * (RADII[-1] + 3 * 1.3 * RADII[-1] * math.sin(math.pi / COUNTS[-1])) + 1
        if u - reach < 0 or v - reach < 0 or u + reach > w - 1 or v + reach > h - 1:
            continue
        alpha = orientation(img, u, v, t)
        out.append(((u, v, t, alpha), describe(img, u, v, t, alpha)))
    return out  # @line L8


def hamming(a: int, b: int) -> int:
    return (a ^ b).bit_count()
