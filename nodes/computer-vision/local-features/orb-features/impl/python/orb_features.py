# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/orb-features/. The authors are listed in prov/X00NNP.jsonl.

"""ORB: oriented FAST and rotated BRIEF (Rublee, Rabaud, Konolige and Bradski, 2011).

An image is a list of H rows of W integers; pixel (u, v) is img[v][u], with u
the column (to the right) and v the row (down). Angles are atan2(dv, du), so
the angle grows from the u axis toward the v axis.

1. FAST-9 corners: 9 contiguous pixels of the circle of 16 pixels at radius 3
   are all brighter than p + t or all darker than p - t.
2. The corners are ranked by the Harris measure det(M) - k tr(M)^2 over a
   7 x 7 window, and the best N are kept. With levels > 1 this runs on each
   level of a pyramid with the factor sqrt(2).
3. Orientation by the intensity centroid: m_pq = sum x^p y^q I(x, y) over a
   disk of radius 15, theta = atan2(m01, m10).
4. Steered BRIEF: 256 tests on a patch of 31 x 31 pixels. Each test point is
   the sum of a 5 x 5 window. The pattern is turned by theta rounded to one of
   the bins of 2 pi / 30; the turned patterns are computed once.
5. The tests can be learned by the greedy search of the paper: order the
   candidate tests by the distance of their mean from 1/2, and add a test when
   its correlation with every chosen test is below a threshold.

A descriptor is a Python int; bit i is 1 when the first point of test i is
darker than the second.
"""

import math
import random
from typing import List, Optional, Sequence, Tuple

Image = Sequence[Sequence[int]]
Point = Tuple[int, int]
Test = Tuple[Point, Point]

CIRCLE = [(0, -3), (1, -3), (2, -2), (3, -1), (3, 0), (3, 1), (2, 2), (1, 3),
          (0, 3), (-1, 3), (-2, 2), (-3, 1), (-3, 0), (-3, -1), (-2, -2), (-1, -3)]
PATCH_RADIUS = 15  # the patch is 31 x 31
PATTERN_RADIUS = 13  # test points stay inside the patch after turning and the 5 x 5 window
BORDER = PATCH_RADIUS + 2


def is_fast_corner(img: Image, u: int, v: int, t: int, n: int = 9) -> bool:
    """The segment test: n contiguous circle pixels all brighter or all darker."""
    p = img[v][u]
    states = []
    for du, dv in CIRCLE:
        q = img[v + dv][u + du]
        states.append(1 if q > p + t else (-1 if q < p - t else 0))
    for want in (1, -1):
        run = 0
        for s in states + states:
            run = run + 1 if s == want else 0
            if run >= n:
                return True
    return False


def harris(img: Image, u: int, v: int, half: int = 3, k: float = 0.04) -> float:
    """Harris measure with central differences summed over a (2 half + 1)^2 window."""
    a = b = c = 0.0
    for y in range(v - half, v + half + 1):
        for x in range(u - half, u + half + 1):
            gx = (img[y][x + 1] - img[y][x - 1]) / 2.0
            gy = (img[y + 1][x] - img[y - 1][x]) / 2.0
            a += gx * gx
            b += gx * gy
            c += gy * gy
    return a * c - b * b - k * (a + c) ** 2


def detect(img: Image, n_features: int = 50, t: int = 20) -> List[Tuple[int, int]]:
    """FAST-9 corners, kept where the Harris measure is the largest among the
    neighboring corners, ranked by the Harris measure; the best n_features."""
    h, w = len(img), len(img[0])
    score = {}
    for v in range(BORDER, h - BORDER):
        for u in range(BORDER, w - BORDER):
            if is_fast_corner(img, u, v, t):  # @line L1
                score[(u, v)] = harris(img, u, v)
    kept = [p for p, s in score.items()
            if all(score.get((p[0] + du, p[1] + dv), -math.inf) < s
                   for du in (-1, 0, 1) for dv in (-1, 0, 1) if du or dv)]
    kept.sort(key=lambda p: (-score[p], p[1], p[0]))
    return kept[:n_features]  # @line L2


def centroid_angle(img: Image, u: int, v: int, r: int = PATCH_RADIUS) -> float:
    """theta = atan2(m01, m10) over the disk of radius r around (u, v)."""
    m10 = m01 = 0
    for y in range(-r, r + 1):
        for x in range(-r, r + 1):
            if x * x + y * y <= r * r:
                p = img[v + y][u + x]
                m10 += x * p
                m01 += y * p
    return math.atan2(m01, m10)  # @line L3


def random_pattern(n: int = 256, seed: int = 0, radius: int = PATTERN_RADIUS) -> List[Test]:
    """n tests with both points uniform in the disk of the given radius."""
    rng = random.Random(seed)

    def point() -> Point:
        while True:
            x, y = rng.randint(-radius, radius), rng.randint(-radius, radius)
            if x * x + y * y <= radius * radius:
                return x, y

    tests = []
    while len(tests) < n:
        p, q = point(), point()
        if p != q:
            tests.append((p, q))
    return tests


def steered_patterns(pattern: Sequence[Test], bins: int = 30) -> List[List[Test]]:
    """The pattern turned by 2 pi b / bins for each b, rounded to pixels.

    When bins is a multiple of 4, the bins of the second to fourth quarter are
    exact 90 degree turns of the first quarter.
    """
    def turn(p: Point, a: float) -> Point:
        c, s = math.cos(a), math.sin(a)
        return int(round(c * p[0] - s * p[1])), int(round(s * p[0] + c * p[1]))

    out: List[List[Test]] = []
    for b in range(bins):
        if bins % 4 == 0 and b >= bins // 4:
            prev = out[b - bins // 4]
            out.append([((-p[1], p[0]), (-q[1], q[0])) for p, q in prev])
        else:
            a = 2 * math.pi * b / bins
            out.append([(turn(p, a), turn(q, a)) for p, q in pattern])
    return out


def angle_bin(theta: float, bins: int) -> int:
    return int(round(theta / (2 * math.pi / bins))) % bins


def integral_image(img: Image) -> List[List[int]]:
    h, w = len(img), len(img[0])
    ii = [[0] * (w + 1) for _ in range(h + 1)]
    for v in range(h):
        row = 0
        for u in range(w):
            row += img[v][u]
            ii[v + 1][u + 1] = ii[v][u + 1] + row
    return ii


def window_sum(ii, u: int, v: int) -> int:
    """Sum of the 5 x 5 window centered at (u, v)."""
    return ii[v + 3][u + 3] - ii[v - 2][u + 3] - ii[v + 3][u - 2] + ii[v - 2][u - 2]


def describe(ii, u: int, v: int, tests: Sequence[Test]) -> int:
    """The binary descriptor of (u, v) with already turned tests."""
    d = 0
    for i, ((px, py), (qx, qy)) in enumerate(tests):  # @line L5
        if window_sum(ii, u + px, v + py) < window_sum(ii, u + qx, v + qy):
            d |= 1 << i  # @line L6
    return d


def resize(img: Image, factor: float) -> List[List[int]]:
    """Bilinear resampling by 1 / factor, rounded to integers."""
    h, w = len(img), len(img[0])
    nh, nw = int(h / factor), int(w / factor)
    out = []
    for v in range(nh):
        y = min((v + 0.5) * factor - 0.5, h - 1.0)
        y0 = max(0, min(int(math.floor(y)), h - 2))
        fy = y - y0
        row = []
        for u in range(nw):
            x = min((u + 0.5) * factor - 0.5, w - 1.0)
            x0 = max(0, min(int(math.floor(x)), w - 2))
            fx = x - x0
            p = ((1 - fy) * ((1 - fx) * img[y0][x0] + fx * img[y0][x0 + 1])
                 + fy * ((1 - fx) * img[y0 + 1][x0] + fx * img[y0 + 1][x0 + 1]))
            row.append(int(round(p)))
        out.append(row)
    return out


def orb(img: Image, n_features: int = 50, t: int = 20, levels: int = 1, factor: float = math.sqrt(2.0),
        pattern: Optional[Sequence[Test]] = None, bins: int = 30, tables=None):
    """Keypoints (u, v, level, theta) in the coordinates of img, with their descriptors."""
    if tables is None:
        tables = steered_patterns(pattern if pattern is not None else random_pattern(), bins)
    out = []
    level_img: List[List[int]] = [list(row) for row in img]
    for level in range(levels):
        if level > 0:
            level_img = resize(img, factor ** level)
        if len(level_img) <= 2 * BORDER or len(level_img[0]) <= 2 * BORDER:
            break
        ii = integral_image(level_img)
        scale = factor ** level
        for u, v in detect(level_img, n_features, t):
            theta = centroid_angle(level_img, u, v)
            b = angle_bin(theta, bins)  # @line L4
            d = describe(ii, u, v, tables[b])
            out.append((((u + 0.5) * scale - 0.5, (v + 0.5) * scale - 0.5, level, theta), d))
    return out  # @line L7


def hamming(a: int, b: int) -> int:
    return (a ^ b).bit_count()


def bit_table(patches: Sequence[Image], tests: Sequence[Test]) -> List[int]:
    """For each test, an int whose bit j is the result of the test on patch j.

    Each patch is a 31 x 31 image already turned to its orientation; its center is (15, 15).
    """
    iis = [integral_image(p) for p in patches]
    out = []
    for (px, py), (qx, qy) in tests:
        bits = 0
        for j, ii in enumerate(iis):
            if window_sum(ii, 15 + px, 15 + py) < window_sum(ii, 15 + qx, 15 + qy):
                bits |= 1 << j
        out.append(bits)
    return out


def correlation(a: int, b: int, n: int) -> float:
    """Pearson correlation of two binary vectors of length n stored as ints."""
    pa, pb = a.bit_count() / n, b.bit_count() / n
    pab = (a & b).bit_count() / n
    den = math.sqrt(pa * (1 - pa) * pb * (1 - pb))
    return 0.0 if den == 0 else (pab - pa * pb) / den


def learn_tests(patches: Sequence[Image], candidates: Sequence[Test], n: int = 256,
                threshold: float = 0.2, step: float = 0.05):
    """The greedy search of ORB; returns (chosen tests, the threshold used)."""
    m = len(patches)
    bits = bit_table(patches, candidates)
    order = sorted(range(len(candidates)), key=lambda i: (abs(bits[i].bit_count() / m - 0.5), i))
    while True:
        chosen = [order[0]]
        for i in order[1:]:
            if len(chosen) == n:
                break
            if all(abs(correlation(bits[i], bits[j], m)) < threshold for j in chosen):
                chosen.append(i)
        if len(chosen) == n or threshold >= 1.0:
            return [candidates[i] for i in chosen], threshold
        threshold += step
