# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/correlative-scan-matching/. The authors are listed in prov/1ZMBCJ.jsonl.

"""Real-time correlative scan matching with a two-level branch and bound.

The method follows Olson (2009). A reference set of 2D points (a previous
scan or a map) gives a lookup table on a grid with the cell size r. A cell
holds the largest value of a kernel around the reference points, rounded to
an integer: round(100 exp(-d^2 / (2 sigma^2))), where d is the distance from
the center of the cell to a reference point. Olson stores log probabilities;
any score that grows with the fit works for the search, and integers make
the comparisons exact.

A query scan is a list of points in the frame of the robot. A pose of the
search is (theta, tx, ty): a rotation from a list of angles and a shift of
whole cells. The score of a pose is the sum of the table over the cells of
the rotated and shifted query points. The search finds a pose of the largest
score in the window, exactly, and evaluates far fewer poses than a search of
the whole window.
"""

import heapq
import math


class Table:
    """A grid of integer scores. Cells outside the grid score 0."""

    def __init__(self, ox, oy, r, nx, ny, pad=0):
        self.ox, self.oy, self.r = ox, oy, r
        self.nx, self.ny, self.pad = nx, ny, pad
        self.v = [[0] * (ny + pad) for _ in range(nx + pad)]

    def get(self, i, j):
        i += self.pad
        j += self.pad
        if 0 <= i < self.nx + self.pad and 0 <= j < self.ny + self.pad:
            return self.v[i][j]
        return 0

    def cell(self, x, y):
        return round((x - self.ox) / self.r), round((y - self.oy) / self.r)


def lookup_table(ref, r, sigma, margin):
    """Return the high resolution table of the points ref, with the cell size r.

    The grid covers the box of ref grown by margin on each side.
    """
    if not ref or r <= 0.0 or sigma <= 0.0:
        raise ValueError("need points, r > 0 and sigma > 0")
    xs = [p[0] for p in ref]
    ys = [p[1] for p in ref]
    ox, oy = min(xs) - margin, min(ys) - margin
    nx = int(math.ceil((max(xs) + margin - ox) / r)) + 1
    ny = int(math.ceil((max(ys) + margin - oy) / r)) + 1
    t = Table(ox, oy, r, nx, ny)
    reach = int(math.ceil(3.0 * sigma / r))
    for px, py in ref:
        ci, cj = t.cell(px, py)
        for i in range(max(0, ci - reach), min(nx, ci + reach + 1)):
            dx = ox + i * r - px
            for j in range(max(0, cj - reach), min(ny, cj + reach + 1)):
                dy = oy + j * r - py
                val = round(100.0 * math.exp(-(dx * dx + dy * dy) / (2.0 * sigma * sigma)))
                if val > t.v[i][j]:
                    t.v[i][j] = val
    return t


def window_max_table(t, d):
    """Return the table T_d with T_d(i, j) = max of t over cells (i + a, j + b), 0 <= a, b < d.

    T_d is defined for i from -(d - 1) on, so that it bounds every shift.
    """
    low = Table(t.ox, t.oy, t.r, t.nx, t.ny, pad=d - 1)
    # first along j, then along i, each a running max over d cells
    rows = [[max(t.get(i, j + b) for b in range(d)) for j in range(-(d - 1), t.ny)] for i in range(-(d - 1), t.nx + d - 1)]
    for a in range(t.nx + d - 1):
        for b in range(t.ny + d - 1):
            low.v[a][b] = max(rows[a + k][b] for k in range(d) if a + k < len(rows))
    return low


def rotated_cells(t, scan, theta, x0, y0):
    """Return the table cells of the scan points rotated by theta and moved to (x0, y0)."""
    c, s = math.cos(theta), math.sin(theta)
    return [t.cell(x0 + c * qx - s * qy, y0 + s * qx + c * qy) for qx, qy in scan]


def score(t, cells, tx, ty):
    return sum(t.get(i + tx, j + ty) for i, j in cells)


def brute_force(t, scan, x0, y0, thetas, w):
    """Return (best score, (theta, tx, ty), number of poses), over all poses of the window."""
    best, pose, count = -1, None, 0
    for th in thetas:
        cells = rotated_cells(t, scan, th, x0, y0)
        for tx in range(-w, w + 1):
            for ty in range(-w, w + 1):
                count += 1
                s = score(t, cells, tx, ty)
                if s > best:
                    best, pose = s, (th, tx, ty)
    return best, pose, count


def correlative_scan_match(t, low, d, scan, x0, y0, thetas, w):
    """Return (best score, (theta, tx, ty), number of full resolution poses scored).

    t is the high resolution table, low = window_max_table(t, d). The window
    is the angles thetas and the shifts tx, ty in [-w, w] cells around (x0, y0).
    """
    heap = []
    cells_of = {}
    for th in thetas:  # @line L3
        cells = rotated_cells(t, scan, th, x0, y0)
        cells_of[th] = cells
        for bx in range(-w, w + 1, d):  # @line L4
            for by in range(-w, w + 1, d):
                heapq.heappush(heap, (-score(low, cells, bx, by), th, bx, by))  # @line L5
    best, pose, count = -1, None, 0  # @line L6
    while heap:  # @line L7
        neg_u, th, bx, by = heapq.heappop(heap)  # @line L8
        if -neg_u <= best:  # @line L9
            break
        cells = cells_of[th]
        for tx in range(bx, min(bx + d, w + 1)):  # @line L10
            for ty in range(by, min(by + d, w + 1)):
                count += 1
                s = score(t, cells, tx, ty)  # @line L11
                if s > best:
                    best, pose = s, (th, tx, ty)
    return best, pose, count  # @line L12


def build_tables(ref, r, sigma, margin, d):
    """Lines L1 and L2: the high resolution table and its window max table."""
    t = lookup_table(ref, r, sigma, margin)  # @line L1
    low = window_max_table(t, d)  # @line L2
    return t, low


def pose_of(t, x0, y0, p):
    """Return the metric pose (x, y, theta) of a search pose (theta, tx, ty)."""
    th, tx, ty = p
    return (x0 + tx * t.r, y0 + ty * t.r, th)


def covariance(t, scan, x0, y0, thetas, w, scale):
    """Return the mean and covariance of the poses of the window, weighted by exp(scale * (s - s_max)).

    This is the estimate of Olson's equation (3): Sigma = K / s - u u^T / s^2,
    with K = sum w x x^T, u = sum w x and s = sum w, over all poses x of the window.
    scale converts a score to a log likelihood.
    """
    poses = []
    for th in thetas:
        cells = rotated_cells(t, scan, th, x0, y0)
        for tx in range(-w, w + 1):
            for ty in range(-w, w + 1):
                poses.append((score(t, cells, tx, ty), pose_of(t, x0, y0, (th, tx, ty))))
    top = max(s for s, _ in poses)
    sw = 0.0
    u = [0.0, 0.0, 0.0]
    k = [[0.0] * 3 for _ in range(3)]
    for s, x in poses:
        wt = math.exp(scale * (s - top))
        sw += wt
        for a in range(3):
            u[a] += wt * x[a]
            for b in range(3):
                k[a][b] += wt * x[a] * x[b]
    mean = [v / sw for v in u]
    cov = [[k[a][b] / sw - u[a] * u[b] / (sw * sw) for b in range(3)] for a in range(3)]
    return mean, cov
