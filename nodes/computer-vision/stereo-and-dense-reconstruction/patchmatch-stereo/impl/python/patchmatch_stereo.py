# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/patchmatch-stereo/. The authors are listed in prov/G3M5MP.jsonl.

"""PatchMatch stereo (Bleyer, Rhemann and Rother 2011) on grayscale images.

Images are lists of rows of numbers, indexed img[y][x], rectified, with the
right camera to the right of the left one. View 0 is the left view and view 1
the right view. A plane f = (a, b, c) gives the disparity a x + b y + c at the
pixel (x, y) of its own view. A left pixel (x, y) with disparity d matches the
right point (x - d, y); a right pixel (x, y) matches the left point (x + d, y).

Differences from the paper: gray values instead of RGB, so the weight and the
color term use one channel; no temporal propagation (one frame); the weighted
median filter of the post-processing is left out.
"""

import math
import random

INF = float("inf")


# ---------------------------------------------------------------- planes


def plane_from_point_normal(x0, y0, z0, n):
    """Plane (a, b, c) through disparity z0 at pixel (x0, y0) with normal n, n[2] != 0."""
    nx, ny, nz = n
    a = -nx / nz
    b = -ny / nz
    c = (nx * x0 + ny * y0 + nz * z0) / nz
    return (a, b, c)


def normal_of_plane(f):
    """Unit normal (with a positive z part) of the plane (a, b, c)."""
    a, b, _ = f
    s = math.sqrt(a * a + b * b + 1.0)
    return (-a / s, -b / s, 1.0 / s)


def disparity(f, x, y):
    a, b, c = f
    return a * x + b * y + c


def transfer_plane(f, from_view):
    """Express the plane of one view in the coordinates of the other view.

    Left to right: x' = x - d, so d = (a x' + b y + c) / (1 - a).
    Right to left: x = x' + d, so d = (a x + b y + c) / (1 + a).
    Returns None for the degenerate plane with 1 - a = 0 or 1 + a = 0.
    """
    a, b, c = f
    k = 1.0 - a if from_view == 0 else 1.0 + a
    if abs(k) < 1e-12:
        return None
    return (a / k, b / k, c / k)


# ---------------------------------------------------------------- images


def gradient(img):
    """Central difference gradient (gx, gy), one-sided at the border."""
    h, w = len(img), len(img[0])
    gx = [[0.0] * w for _ in range(h)]
    gy = [[0.0] * w for _ in range(h)]
    for y in range(h):
        for x in range(w):
            x0, x1 = max(x - 1, 0), min(x + 1, w - 1)
            y0, y1 = max(y - 1, 0), min(y + 1, h - 1)
            gx[y][x] = (img[y][x1] - img[y][x0]) / (x1 - x0) if x1 > x0 else 0.0
            gy[y][x] = (img[y1][x] - img[y0][x]) / (y1 - y0) if y1 > y0 else 0.0
    return gx, gy


def sample_row(row, x):
    """Linear interpolation in one row, clamped at the ends."""
    w = len(row)
    if x <= 0:
        return row[0]
    if x >= w - 1:
        return row[w - 1]
    i = int(x)
    t = x - i
    return (1.0 - t) * row[i] + t * row[i + 1]


class View:
    """One image with its gradient and the support weights of its windows."""

    def __init__(self, img, radius, gamma):
        self.img = img
        self.h, self.w = len(img), len(img[0])
        self.gx, self.gy = gradient(img)
        self.window = {}
        for y in range(self.h):
            for x in range(self.w):
                ip = img[y][x]
                ws = []
                for qy in range(max(0, y - radius), min(self.h, y + radius + 1)):
                    for qx in range(max(0, x - radius), min(self.w, x + radius + 1)):
                        ws.append((qx, qy, math.exp(-abs(ip - img[qy][qx]) / gamma)))
                self.window[(x, y)] = ws


class Params:
    def __init__(self, radius=3, max_disp=8.0, gamma=10.0, alpha=0.9,
                 tau_col=10.0, tau_grad=2.0, iterations=3, fronto=False):
        self.radius = radius
        self.max_disp = max_disp
        self.gamma = gamma
        self.alpha = alpha
        self.tau_col = tau_col
        self.tau_grad = tau_grad
        self.iterations = iterations
        self.fronto = fronto


def plane_cost(views, v, x, y, f, prm):
    """m(p, f): the weighted sum of rho over the window of p in view v."""
    me, other = views[v], views[1 - v]
    sign = -1.0 if v == 0 else 1.0
    a, b, c = f
    total = 0.0
    for qx, qy, wq in me.window[(x, y)]:
        xq = qx + sign * (a * qx + b * qy + c)
        col = abs(me.img[qy][qx] - sample_row(other.img[qy], xq))
        grad = (abs(me.gx[qy][qx] - sample_row(other.gx[qy], xq))
                + abs(me.gy[qy][qx] - sample_row(other.gy[qy], xq)))
        rho = ((1.0 - prm.alpha) * min(col, prm.tau_col)
               + prm.alpha * min(grad, prm.tau_grad))
        total += wq * rho
    return total


def _random_normal(rng, fronto):
    if fronto:
        return (0.0, 0.0, 1.0)
    while True:
        n = (rng.gauss(0, 1), rng.gauss(0, 1), rng.gauss(0, 1))
        s = math.sqrt(sum(t * t for t in n))
        if s > 1e-9 and abs(n[2]) / s > 1e-3:
            n = tuple(t / s for t in n)
            return n if n[2] > 0 else tuple(-t for t in n)


def _in_range(f, x, y, prm):
    d = disparity(f, x, y)
    return 0.0 <= d <= prm.max_disp


def patchmatch_stereo(left, right, prm, rng, history=None):
    """Return (planes, costs): two dicts per view, keyed by (x, y).

    history, if a list, gets a copy of the costs of both views after the
    initialization and after each iteration.
    """
    views = [View(left, prm.radius, prm.gamma), View(right, prm.radius, prm.gamma)]
    planes = [{}, {}]
    costs = [{}, {}]
    for v in (0, 1):
        for y in range(views[v].h):
            for x in range(views[v].w):
                z0 = rng.uniform(0.0, prm.max_disp)
                f = plane_from_point_normal(x, y, z0, _random_normal(rng, prm.fronto))  # @line L1
                planes[v][(x, y)] = f
                costs[v][(x, y)] = plane_cost(views, v, x, y, f, prm)
    if history is not None:
        history.append([dict(costs[0]), dict(costs[1])])

    def try_plane(v, x, y, f):
        if f is None or not _in_range(f, x, y, prm):
            return
        m = plane_cost(views, v, x, y, f, prm)
        if m < costs[v][(x, y)]:
            planes[v][(x, y)] = f
            costs[v][(x, y)] = m

    for it in range(prm.iterations):  # @line L2
        for v in (0, 1):  # @line L3
            o = 1 - v
            # Pixels of the other view, grouped by the pixel of view v they hit.
            hits = {}
            for (ox, oy), g in planes[o].items():
                d = disparity(g, ox, oy)
                tx = int(math.floor(ox + (d if o == 1 else -d) + 0.5))
                hits.setdefault((tx, oy), []).append(g)
            h, w = views[v].h, views[v].w
            if it % 2 == 0:  # @line L4
                order = [(x, y) for y in range(h) for x in range(w)]
                step = -1
            else:
                order = [(x, y) for y in range(h - 1, -1, -1) for x in range(w - 1, -1, -1)]
                step = 1
            for x, y in order:  # @line L5
                for nx, ny in ((x + step, y), (x, y + step)):  # @line L6
                    if 0 <= nx < w and 0 <= ny < h:
                        try_plane(v, x, y, planes[v][(nx, ny)])
                for g in hits.get((x, y), ()):  # @line L7
                    try_plane(v, x, y, transfer_plane(g, o))
                dz = prm.max_disp / 2.0  # @line L8
                dn = 1.0
                while dz >= 0.1:  # @line L9
                    f = planes[v][(x, y)]
                    z0 = disparity(f, x, y) + rng.uniform(-dz, dz)  # @line L10
                    n = normal_of_plane(f)
                    if not prm.fronto:
                        n = tuple(t + rng.uniform(-dn, dn) for t in n)
                        s = math.sqrt(sum(t * t for t in n))
                        n = tuple(t / s for t in n) if s > 1e-9 else None
                    if n is not None and n[2] > 1e-3:
                        try_plane(v, x, y, plane_from_point_normal(x, y, z0, n))  # @line L11
                    dz /= 2.0  # @line L12
                    dn /= 2.0
        if history is not None:
            history.append([dict(costs[0]), dict(costs[1])])
    return planes, costs  # @line L13


def disparity_maps(planes, shape):
    h, w = shape
    return [[[disparity(planes[v][(x, y)], x, y) for x in range(w)] for y in range(h)]
            for v in (0, 1)]


def left_right_check(dl, dr, tol=1.0):
    """Mark a left pixel invalid when its match in the right map disagrees by more than tol."""
    h, w = len(dl), len(dl[0])
    valid = [[False] * w for _ in range(h)]
    for y in range(h):
        for x in range(w):
            xr = int(math.floor(x - dl[y][x] + 0.5))
            if 0 <= xr < w and abs(dl[y][x] - dr[y][xr]) <= tol:
                valid[y][x] = True
    return valid


def fill_invalid(dl, valid, planes_left):
    """Fill each invalid pixel with the lower of the disparities that the planes
    of the nearest valid pixels to its left and to its right give at the pixel."""
    h, w = len(dl), len(dl[0])
    out = [row[:] for row in dl]
    for y in range(h):
        for x in range(w):
            if valid[y][x]:
                continue
            cand = []
            for step in (-1, 1):
                k = x + step
                while 0 <= k < w and not valid[y][k]:
                    k += step
                if 0 <= k < w:
                    cand.append(disparity(planes_left[(k, y)], x, y))
            if cand:
                out[y][x] = min(cand)
    return out


def best_fronto_parallel(left, right, prm, step=0.25):
    """Reference: the best constant disparity per window, on a grid of step pixels."""
    views = [View(left, prm.radius, prm.gamma), View(right, prm.radius, prm.gamma)]
    h, w = len(left), len(left[0])
    out = [[0.0] * w for _ in range(h)]
    ds = [i * step for i in range(int(prm.max_disp / step) + 1)]
    for y in range(h):
        for x in range(w):
            best = INF
            for d in ds:
                m = plane_cost(views, 0, x, y, (0.0, 0.0, d), prm)
                if m < best:
                    best, out[y][x] = m, d
    return out


if __name__ == "__main__":
    rng = random.Random(1)
    img = [[rng.randrange(256) for _ in range(12)] for _ in range(8)]
    prm = Params(radius=1, max_disp=3.0)
    planes, _ = patchmatch_stereo(img, img, prm, random.Random(2))
    print(disparity_maps(planes, (8, 12))[0][4])
