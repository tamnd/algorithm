# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mean-shift-segmentation/. The authors are listed in prov/YT936C.jsonl.

"""Mean shift segmentation (Comaniciu and Meer, 2002) in exact arithmetic.

Each pixel is a point (x, y, c) in the joint spatial-range domain, where c is
a color vector (or one gray value). Distances are measured after dividing the
position by h_s and the color by h_r. The kernel used here is flat on the
unit ball of these scaled coordinates,

    ||(x_j - y_s) / h_s||^2 + ||(c_j - y_r) / h_r||^2 <= 1,

so each mean shift step moves a point to the plain mean of the pixels inside
its window. This flat kernel is the shadow of the Epanechnikov kernel, and
with exact fractions every mean shift path stops after finitely many steps
at a point where the window mean is the point itself.

kernel="product" uses the window ||x_j - y_s|| <= h_s and ||c_j - y_r|| <= h_r,
the product of two flat kernels that Comaniciu and Meer use in their
examples. That kernel is not radially symmetric in the joint domain, so the
convergence argument for the ball does not cover it; the iteration is capped.
"""

from fractions import Fraction
from typing import Dict, List, Sequence, Tuple

Point = Tuple[Fraction, ...]  # (x, y, c_1, ..., c_d)


def _points(img) -> List[Point]:
    pts = []
    for y, row in enumerate(img):
        for x, p in enumerate(row):
            c = tuple(p) if isinstance(p, (tuple, list)) else (p,)
            pts.append((Fraction(x), Fraction(y)) + tuple(Fraction(v) for v in c))
    return pts


def _sq(a, b) -> Fraction:
    return sum(((u - v) * (u - v) for u, v in zip(a, b)), Fraction(0))


def in_window(p: Point, y: Point, hs: Fraction, hr: Fraction, kernel: str) -> bool:
    ds, dr = _sq(p[:2], y[:2]), _sq(p[2:], y[2:])
    if kernel == "ball":
        return ds / (hs * hs) + dr / (hr * hr) <= 1
    if kernel == "product":
        return ds <= hs * hs and dr <= hr * hr
    raise ValueError("kernel must be 'ball' or 'product'")


def mean_shift_point(pts: Sequence[Point], start: Point, hs, hr, kernel: str = "ball", max_iter: int = 1000):
    """Follow the mean shift path from start. Returns (mode, path)."""
    hs, hr = Fraction(hs), Fraction(hr)
    y = start
    path = [y]
    for _ in range(max_iter):  # @line L2
        win = [p for p in pts if abs(p[0] - y[0]) <= hs and abs(p[1] - y[1]) <= hs and in_window(p, y, hs, hr, kernel)]  # @line L3
        n = len(win)
        new = tuple(sum((p[t] for p in win), Fraction(0)) / n for t in range(len(y)))  # @line L4
        if new == y:
            return y, path
        y = new
        path.append(y)
    raise RuntimeError("mean shift did not converge within max_iter steps")


def epanechnikov_density(pts: Sequence[Point], y: Point, hs, hr) -> Fraction:
    """Sum over pixels of (1 - u)_+ with u the scaled squared distance (no constant)."""
    hs, hr = Fraction(hs), Fraction(hr)
    total = Fraction(0)
    for p in pts:
        u = _sq(p[:2], y[:2]) / (hs * hs) + _sq(p[2:], y[2:]) / (hr * hr)
        if u < 1:
            total += 1 - u
    return total


def _components(n: int, edges) -> List[int]:
    parent = list(range(n))

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    for a, b in edges:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[max(ra, rb)] = min(ra, rb)
    return [find(a) for a in range(n)]


def group_modes(modes: Sequence[Point], hs, hr) -> List[int]:
    """Clusters of the modes: join two pixels whose modes are closer than h_s in
    position and closer than h_r in color, and take connected components."""
    hs, hr = Fraction(hs), Fraction(hr)
    distinct = sorted(set(modes))
    index = {m: i for i, m in enumerate(distinct)}
    edges = [
        (i, j)
        for i in range(len(distinct))
        for j in range(i + 1, len(distinct))
        if _sq(distinct[i][:2], distinct[j][:2]) < hs * hs and _sq(distinct[i][2:], distinct[j][2:]) < hr * hr
    ]
    comp = _components(len(distinct), edges)
    return [comp[index[m]] for m in modes]


def _regions(labels: List[List[int]]) -> List[List[int]]:
    """Split each label into 4-connected regions, numbered in raster order."""
    h, w = len(labels), len(labels[0])
    out = [[-1] * w for _ in range(h)]
    k = 0
    for y in range(h):
        for x in range(w):
            if out[y][x] >= 0:
                continue
            out[y][x] = k
            stack = [(x, y)]
            while stack:
                cx, cy = stack.pop()
                for nx, ny in ((cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1)):
                    if 0 <= nx < w and 0 <= ny < h and out[ny][nx] < 0 and labels[ny][nx] == labels[y][x]:
                        out[ny][nx] = k
                        stack.append((nx, ny))
            k += 1
    return out


def _region_stats(img_pts: List[Point], regions: List[List[int]]):
    w = len(regions[0])
    stats: Dict[int, list] = {}
    for y, row in enumerate(regions):
        for x, r in enumerate(row):
            c = img_pts[y * w + x][2:]
            s = stats.setdefault(r, [[Fraction(0)] * len(c), 0, (y, x)])
            for t, v in enumerate(c):
                s[0][t] += v
            s[1] += 1
    return {r: (tuple(v / s[1] for v in s[0]), s[1], s[2]) for r, s in stats.items()}


def merge_small_regions(img_pts: List[Point], regions: List[List[int]], min_size: int) -> List[List[int]]:
    """While a region has fewer than min_size pixels and is not alone, merge the
    smallest one (first in raster order on ties) into the adjacent region with
    the nearest mean color (the lowest number on ties)."""
    h, w = len(regions), len(regions[0])
    regions = [row[:] for row in regions]
    while True:
        stats = _region_stats(img_pts, regions)
        if len(stats) < 2:
            return regions
        r = min(stats, key=lambda q: (stats[q][1], stats[q][2]))
        if stats[r][1] >= min_size:
            return regions
        adj = set()
        for y in range(h):
            for x in range(w):
                if regions[y][x] == r:
                    for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                        if 0 <= nx < w and 0 <= ny < h and regions[ny][nx] != r:
                            adj.add(regions[ny][nx])
        target = min(adj, key=lambda q: (_sq(stats[q][0], stats[r][0]), q))
        regions = [[target if v == r else v for v in row] for row in regions]


def renumber(labels: List[List[int]]) -> List[List[int]]:
    names: Dict[int, int] = {}
    return [[names.setdefault(v, len(names)) for v in row] for row in labels]


def mean_shift_filter(img, hs, hr, kernel: str = "ball"):
    """Return (filtered, modes): each pixel keeps its position and takes the
    color of the mode its mean shift path reaches."""
    pts = _points(img)
    w = len(img[0])
    modes = [mean_shift_point(pts, p, hs, hr, kernel)[0] for p in pts]
    filtered = [[modes[y * w + x][2:] for x in range(w)] for y in range(len(img))]
    return filtered, modes


def mean_shift_segmentation(img, hs, hr, min_size: int = 0, kernel: str = "ball"):
    """Labels 0, 1, ... of connected regions, in raster order of first appearance."""
    pts = _points(img)
    h, w = len(img), len(img[0])
    modes = []
    for p in pts:  # @line L1
        mode, _ = mean_shift_point(pts, p, hs, hr, kernel)
        modes.append(mode)  # @line L5
    cluster = group_modes(modes, hs, hr)  # @line L6
    regions = _regions([[cluster[y * w + x] for x in range(w)] for y in range(h)])  # @line L7
    if min_size > 1:
        regions = merge_small_regions(pts, regions, min_size)  # @line L8
    return renumber(regions)  # @line L9
