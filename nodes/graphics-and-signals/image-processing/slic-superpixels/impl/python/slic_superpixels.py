# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/slic-superpixels/. The authors are listed in prov/2WFPAC.jsonl.

"""SLIC superpixels (Achanta et al., 2012) in exact arithmetic.

A pixel is a color vector c (a tuple of numbers, for example CIELAB values,
or a single gray value) at a position (x, y). A cluster center is a vector
[c, x, y]. The distance used is

    D^2 = d_c^2 + (d_s / S)^2 m^2

with d_c the Euclidean color distance, d_s the Euclidean distance in the
plane, S^2 = N / K for K centers and m the compactness. Distances are
compared squared, as exact fractions, so no square root is needed.

Each assignment step looks for the centers of a pixel only in the square
window |x - x_j| <= S, |y - y_j| <= S around each center, which is what makes
SLIC cost O(N) per iteration instead of O(K N).
"""

from collections import deque
from fractions import Fraction
from math import isqrt
from typing import Dict, List, Optional, Sequence, Tuple

Center = Tuple[Tuple[Fraction, ...], Fraction, Fraction]  # (color, x, y)


def _as_colors(img) -> List[List[Tuple[Fraction, ...]]]:
    out = []
    for row in img:
        out.append([tuple(Fraction(v) for v in p) if isinstance(p, (tuple, list)) else (Fraction(p),) for p in row])
    return out


def _sq(a: Sequence[Fraction], b: Sequence[Fraction]) -> Fraction:
    return sum(((u - v) * (u - v) for u, v in zip(a, b)), Fraction(0))


def gradient(img, x: int, y: int) -> Fraction:
    """Squared central differences, with indices clamped at the border."""
    h, w = len(img), len(img[0])
    xl, xr = img[y][max(x - 1, 0)], img[y][min(x + 1, w - 1)]
    yu, yd = img[max(y - 1, 0)][x], img[min(y + 1, h - 1)][x]
    return _sq(xr, xl) + _sq(yd, yu)


def grid_seeds(w: int, h: int, k: int) -> List[Tuple[int, int]]:
    """About k seeds on a regular grid, the centers of equal cells."""
    if k < 1:
        raise ValueError("k must be at least 1")
    s2 = Fraction(w * h, k)
    # The number of seeds along each side: round(w / S) and round(h / S), at least 1.
    nx = max(1, round(Fraction(w) / _sqrt_approx(s2)))
    ny = max(1, round(Fraction(h) / _sqrt_approx(s2)))
    return [((2 * i + 1) * w // (2 * nx), (2 * j + 1) * h // (2 * ny)) for j in range(ny) for i in range(nx)]


def _sqrt_approx(q: Fraction) -> Fraction:
    # A rational square root good to about 1e-12; only used to place the grid.
    scale = 10**12
    return Fraction(isqrt(q.numerator * scale * scale // q.denominator), scale)


def initial_centers(img, k: int) -> Tuple[List[Center], Fraction]:
    h, w = len(img), len(img[0])
    seeds = grid_seeds(w, h, k)  # @line L1
    centers = []
    for sx, sy in seeds:  # @line L2
        best = None
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                x, y = sx + dx, sy + dy
                if 0 <= x < w and 0 <= y < h:
                    key = (gradient(img, x, y), dy, dx)
                    if best is None or key < best[0]:
                        best = (key, x, y)
        _, x, y = best
        centers.append((img[y][x], Fraction(x), Fraction(y)))
    s2 = Fraction(w * h, len(centers))
    return centers, s2


def distance2(c: Tuple[Fraction, ...], x: int, y: int, center: Center, s2: Fraction, m) -> Fraction:
    cc, cx, cy = center
    ds2 = (x - cx) ** 2 + (y - cy) ** 2
    return _sq(c, cc) + ds2 * Fraction(m) ** 2 / s2


def in_window(x: int, y: int, center: Center, s2: Fraction) -> bool:
    _, cx, cy = center
    return (x - cx) ** 2 <= s2 and (y - cy) ** 2 <= s2


def assign(img, centers: List[Center], s2: Fraction, m, labels: List[List[int]]) -> List[List[int]]:
    """One assignment step. Pixels covered by no window keep their old label."""
    h, w = len(img), len(img[0])
    best: List[List[Optional[Fraction]]] = [[None] * w for _ in range(h)]  # @line L4
    labels = [row[:] for row in labels]
    r = isqrt(-(-s2.numerator // s2.denominator)) + 1  # an integer above S
    for j, cen in enumerate(centers):  # @line L5
        _, cx, cy = cen
        bx, by = cx.numerator // cx.denominator, cy.numerator // cy.denominator
        # Only the window (x - cx)^2 <= S^2, (y - cy)^2 <= S^2 is visited.
        for y in range(max(0, by - r), min(h, by + r + 2)):
            if (y - cy) ** 2 > s2:
                continue
            for x in range(max(0, bx - r), min(w, bx + r + 2)):
                if (x - cx) ** 2 > s2:
                    continue
                d = distance2(img[y][x], x, y, cen, s2, m)  # @line L6
                if best[y][x] is None or d < best[y][x]:
                    best[y][x] = d
                    labels[y][x] = j
    return labels


def update(img, labels: List[List[int]], centers: List[Center]) -> List[Center]:
    """New centers: the exact mean [c, x, y] of each cluster; an empty cluster keeps its center."""
    dim = len(centers[0][0])
    sums: Dict[int, list] = {}
    for y, row in enumerate(labels):
        for x, j in enumerate(row):
            if j < 0:
                continue
            s = sums.setdefault(j, [[Fraction(0)] * dim, Fraction(0), Fraction(0), 0])
            for t in range(dim):
                s[0][t] += img[y][x][t]
            s[1] += x
            s[2] += y
            s[3] += 1
    out = []
    for j, cen in enumerate(centers):
        if j in sums:
            c, sx, sy, n = sums[j]
            out.append((tuple(v / n for v in c), sx / n, sy / n))
        else:
            out.append(cen)
    return out


def enforce_connectivity(img, labels: List[List[int]], centers: List[Center], s2: Fraction, m) -> List[List[int]]:
    """Keep the largest 4-connected piece of each label; give every other pixel
    the label, among those of its already labeled neighbors, whose center is
    nearest in D. Pixels are taken in breadth-first order from the kept pieces."""
    h, w = len(labels), len(labels[0])
    nb = lambda x, y: [(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)) if 0 <= x + dx < w and 0 <= y + dy < h]
    piece = [[-1] * w for _ in range(h)]
    pieces: List[List[Tuple[int, int]]] = []
    for y in range(h):
        for x in range(w):
            if piece[y][x] >= 0 or labels[y][x] < 0:
                continue
            j, comp, stack = labels[y][x], [(x, y)], [(x, y)]
            piece[y][x] = len(pieces)
            while stack:
                cx, cy = stack.pop()
                for nx, ny in nb(cx, cy):
                    if piece[ny][nx] < 0 and labels[ny][nx] == j:
                        piece[ny][nx] = len(pieces)
                        comp.append((nx, ny))
                        stack.append((nx, ny))
            pieces.append(comp)
    keep: Dict[int, int] = {}  # label -> index of its largest piece (first in raster order on ties)
    for i, comp in enumerate(pieces):
        j = labels[comp[0][1]][comp[0][0]]
        if j not in keep or len(comp) > len(pieces[keep[j]]):
            keep[j] = i
    out = [[-1] * w for _ in range(h)]
    for j, i in keep.items():
        for x, y in pieces[i]:
            out[y][x] = j
    queue = deque()
    queued = set()
    for y in range(h):
        for x in range(w):
            if out[y][x] < 0 and any(out[ny][nx] >= 0 for nx, ny in nb(x, y)):
                queue.append((x, y))
                queued.add((x, y))
    while queue:
        x, y = queue.popleft()
        cands = sorted({out[ny][nx] for nx, ny in nb(x, y) if out[ny][nx] >= 0})
        out[y][x] = min(cands, key=lambda j: (distance2(img[y][x], x, y, centers[j], s2, m), j))
        for nx, ny in nb(x, y):
            if out[ny][nx] < 0 and (nx, ny) not in queued:
                queued.add((nx, ny))
                queue.append((nx, ny))
    return out


def relabel(labels: List[List[int]]) -> List[List[int]]:
    names: Dict[int, int] = {}
    return [[v if v < 0 else names.setdefault(v, len(names)) for v in row] for row in labels]


def slic(img, k: int, m=10, max_iter: int = 10, connected: bool = True):
    """Return (labels, centers, iterations). Labels are 0, 1, ... in raster order
    of first appearance; centers[j] is the exact mean (color, x, y) of label j."""
    img = _as_colors(img)
    h, w = len(img), len(img[0])
    centers, s2 = initial_centers(img, k)
    labels = [[-1] * w for _ in range(h)]
    it = 0
    while it < max_iter:  # @line L3
        it += 1
        labels = assign(img, centers, s2, m, labels)
        new = update(img, labels, centers)  # @line L7
        moved = any(a != b for a, b in zip(new, centers))
        centers = new
        if not moved:  # @line L8
            break
    if connected:
        labels = enforce_connectivity(img, labels, centers, s2, m)  # @line L9
    labels = relabel(labels)
    k_out = 1 + max(max(r) for r in labels)
    final = update(img, labels, [((Fraction(0),) * len(img[0][0]), Fraction(0), Fraction(0))] * k_out)
    return labels, final, it
