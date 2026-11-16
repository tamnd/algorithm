# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tracking-learning-detection/. The authors are listed in prov/CCWPAB.jsonl.

"""Tracking-learning-detection (Kalal, Mikolajczyk and Matas), a compact
version: a median flow tracker, a cascaded detector (variance filter, fern
ensemble, nearest neighbor classifier), an integrator, and P-N learning.

Images are lists of rows of gray values, indexed img[v][u]; the center of
pixel (u, v) is the point (u, v). A box is (x1, y1, x2, y2) with x1 < x2 and
y1 < y2 in the same coordinates; an integer box holds the pixels with
x1 <= u < x2 and y1 <= v < y2.
"""

import math
import random

PATCH = 15  # side of the normalized patches of the nearest neighbor classifier


# ---------------------------------------------------------------- basics

def sample(img, u, v):
    """Bilinear sample at a real point, indices clamped."""
    h, w = len(img), len(img[0])
    u0, v0 = math.floor(u), math.floor(v)
    fu, fv = u - u0, v - v0

    def at(vv, uu):
        return img[min(max(vv, 0), h - 1)][min(max(uu, 0), w - 1)]

    return ((1 - fv) * ((1 - fu) * at(v0, u0) + fu * at(v0, u0 + 1))
            + fv * ((1 - fu) * at(v0 + 1, u0) + fu * at(v0 + 1, u0 + 1)))


def iou(a, b):
    """Intersection over union of two boxes."""
    w = min(a[2], b[2]) - max(a[0], b[0])
    h = min(a[3], b[3]) - max(a[1], b[1])
    if w <= 0 or h <= 0:
        return 0.0
    inter = w * h
    return inter / ((a[2] - a[0]) * (a[3] - a[1]) + (b[2] - b[0]) * (b[3] - b[1]) - inter)


def median(xs):
    s = sorted(xs)
    n = len(s)
    return s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2


def ncc(a, b):
    """Normalized cross-correlation of two equal-length vectors, in [-1, 1]."""
    ma, mb = sum(a) / len(a), sum(b) / len(b)
    da = [x - ma for x in a]
    db = [x - mb for x in b]
    na = math.sqrt(sum(x * x for x in da))
    nb = math.sqrt(sum(x * x for x in db))
    if na == 0 or nb == 0:
        return 0.0
    return sum(x * y for x, y in zip(da, db)) / (na * nb)


def patch(img, box, side=PATCH):
    """The box resampled to side x side values, then shifted to zero mean and
    scaled to unit norm, so that the dot product of two patches is their NCC."""
    x1, y1, x2, y2 = box
    sw, sh = (x2 - x1) / side, (y2 - y1) / side
    vals = [sample(img, x1 - 0.5 + (i + 0.5) * sw, y1 - 0.5 + (j + 0.5) * sh)
            for j in range(side) for i in range(side)]
    m = sum(vals) / len(vals)
    d = [x - m for x in vals]
    n = math.sqrt(sum(x * x for x in d))
    return [x / n for x in d] if n > 0 else [0.0] * len(d)


# ---------------------------------------------------------------- median flow

def lk(img_a, img_b, p, r=3, iters=15, tol=0.01):
    """Translation of the window of radius r around p from img_a to img_b,
    by Lucas-Kanade steps with the gradient of img_a. None if the window
    has no texture."""
    offs = [(i, j) for j in range(-r, r + 1) for i in range(-r, r + 1)]
    grads, vals = [], []
    gxx = gxy = gyy = 0.0
    for i, j in offs:
        u, v = p[0] + i, p[1] + j
        gx = (sample(img_a, u + 1, v) - sample(img_a, u - 1, v)) / 2
        gy = (sample(img_a, u, v + 1) - sample(img_a, u, v - 1)) / 2
        grads.append((gx, gy))
        vals.append(sample(img_a, u, v))
        gxx += gx * gx
        gxy += gx * gy
        gyy += gy * gy
    det = gxx * gyy - gxy * gxy
    if det <= 1e-9 * (gxx + gyy) ** 2 or gxx + gyy == 0:
        return None
    d = [0.0, 0.0]
    for _ in range(iters):
        bx = by = 0.0
        for (i, j), (gx, gy), a in zip(offs, grads, vals):
            e = a - sample(img_b, p[0] + i + d[0], p[1] + j + d[1])
            bx += gx * e
            by += gy * e
        sx = (gyy * bx - gxy * by) / det
        sy = (gxx * by - gxy * bx) / det
        d[0] += sx
        d[1] += sy
        if math.hypot(sx, sy) < tol:
            break
    return (d[0], d[1])


def median_flow(img_a, img_b, box, grid=10, fail=10.0, fb_max=5.0):
    """Move the box from img_a to img_b. Returns the new box, or None if the
    tracker fails: no point can be tracked, the median forward-backward error
    is above fb_max, or the median distance of the point displacements from
    the median displacement is above `fail`."""
    x1, y1, x2, y2 = box
    pts = [(x1 + (x2 - x1) * (i + 1) / (grid + 1) - 0.5, y1 + (y2 - y1) * (j + 1) / (grid + 1) - 0.5)
           for j in range(grid) for i in range(grid)]  # @line L1
    good = []
    for p in pts:
        d = lk(img_a, img_b, p)  # @line L2
        if d is None:
            continue
        q = (p[0] + d[0], p[1] + d[1])
        back = lk(img_b, img_a, q)
        if back is None:
            continue
        fb = math.hypot(d[0] + back[0], d[1] + back[1])  # @line L3
        pa = [sample(img_a, p[0] + i, p[1] + j) for j in range(-3, 4) for i in range(-3, 4)]
        pb = [sample(img_b, q[0] + i, q[1] + j) for j in range(-3, 4) for i in range(-3, 4)]
        good.append((p, q, fb, ncc(pa, pb)))
    if not good:
        return None
    mfb = median([g[2] for g in good])
    mncc = median([g[3] for g in good])
    kept = [g for g in good if g[2] <= mfb and g[3] >= mncc]  # @line L4
    if not kept or mfb > fb_max:
        return None
    dx = median([q[0] - p[0] for p, q, _, _ in kept])  # @line L5
    dy = median([q[1] - p[1] for p, q, _, _ in kept])
    residual = median([math.hypot(q[0] - p[0] - dx, q[1] - p[1] - dy) for p, q, _, _ in good])
    if residual > fail:  # @line L6
        return None
    ratios = []
    for i in range(len(kept)):
        for j in range(i + 1, len(kept)):
            da = math.dist(kept[i][0], kept[j][0])
            if da > 0:
                ratios.append(math.dist(kept[i][1], kept[j][1]) / da)
    s = median(ratios) if ratios else 1.0  # @line L7
    cx, cy = (x1 + x2) / 2 + dx, (y1 + y2) / 2 + dy
    hw, hh = (x2 - x1) * s / 2, (y2 - y1) * s / 2
    return (cx - hw, cy - hh, cx + hw, cy + hh)


# ---------------------------------------------------------------- detector

def integral_images(img):
    """Summed tables of the values and of their squares, of size (H+1) x (W+1)."""
    h, w = len(img), len(img[0])
    s = [[0.0] * (w + 1) for _ in range(h + 1)]
    s2 = [[0.0] * (w + 1) for _ in range(h + 1)]
    for v in range(h):
        row = row2 = 0.0
        for u in range(w):
            row += img[v][u]
            row2 += img[v][u] ** 2
            s[v + 1][u + 1] = s[v][u + 1] + row
            s2[v + 1][u + 1] = s2[v][u + 1] + row2
    return s, s2


def box_variance(tables, box):
    """The variance of the pixels of an integer box, in O(1)."""
    s, s2 = tables
    x1, y1, x2, y2 = box
    n = (x2 - x1) * (y2 - y1)
    t = s[y2][x2] - s[y1][x2] - s[y2][x1] + s[y1][x1]
    t2 = s2[y2][x2] - s2[y1][x2] - s2[y2][x1] + s2[y1][x1]
    return t2 / n - (t / n) ** 2


def scan_windows(width, height, bw, bh, scales=(1 / 1.2, 1.0, 1.2), step=0.1):
    """All integer boxes of the scaled sizes, shifted by a tenth of their size."""
    out = []
    for sc in scales:
        w, h = max(4, round(bw * sc)), max(4, round(bh * sc))
        su, sv = max(1, round(step * w)), max(1, round(step * h))
        for y in range(0, height - h + 1, sv):
            for x in range(0, width - w + 1, su):
                out.append((x, y, x + w, y + h))
    return out


class Ferns:
    """An ensemble of ferns; each fern compares `depth` pairs of points."""

    def __init__(self, count=10, depth=10, seed=0):
        rng = random.Random(seed)
        self.pairs = [[((rng.random(), rng.random()), (rng.random(), rng.random())) for _ in range(depth)]
                      for _ in range(count)]
        self.pos = [[0] * (1 << depth) for _ in range(count)]
        self.neg = [[0] * (1 << depth) for _ in range(count)]

    def codes(self, img, box, rng=None, noise=0.0):
        """One code per fern: bit k is 1 if the pixel nearest to the first point
        of pair k is brighter than the pixel nearest to the second point. With
        an rng, Gaussian noise of standard deviation `noise` is added to each
        value that is read."""
        x1, y1, x2, y2 = box
        w, h = x2 - x1 - 1, y2 - y1 - 1
        hi, wi = len(img) - 1, len(img[0]) - 1

        def px(fx, fy):
            u, v = math.floor(x1 + fx * w + 0.5), math.floor(y1 + fy * h + 0.5)
            value = img[min(max(v, 0), hi)][min(max(u, 0), wi)]
            return value + rng.gauss(0, noise) if rng else value

        out = []
        for fern in self.pairs:
            code = 0
            for (ax, ay), (bx, by) in fern:
                code = 2 * code + (1 if px(ax, ay) > px(bx, by) else 0)
            out.append(code)
        return out

    def posterior(self, codes):
        total = 0.0
        for f, c in enumerate(codes):
            p, n = self.pos[f][c], self.neg[f][c]
            total += p / (p + n) if p + n else 0.0
        return total / len(codes)

    def update(self, codes, label):
        for f, c in enumerate(codes):
            if label:
                self.pos[f][c] += 1
            else:
                self.neg[f][c] += 1


class NearestNeighbor:
    """Positive and negative patch sets with the similarities of TLD."""

    def __init__(self):
        self.pos, self.neg = [], []

    @staticmethod
    def sim(a, b):
        """0.5 (NCC + 1) of two normalized patches, in [0, 1]."""
        return 0.5 * (sum(x * y for x, y in zip(a, b)) + 1)

    def relative(self, p):
        """S+ / (S+ + S-) over all positives and negatives."""
        sp = max((self.sim(p, q) for q in self.pos), default=0.0)
        sn = max((self.sim(p, q) for q in self.neg), default=0.0)
        return sp / (sp + sn) if sp + sn else 0.0

    def conservative(self, p):
        """As relative, but S+ uses only the older half of the positives."""
        old = self.pos[:max(1, (len(self.pos) + 1) // 2)]
        sp = max((self.sim(p, q) for q in old), default=0.0)
        sn = max((self.sim(p, q) for q in self.neg), default=0.0)
        return sp / (sp + sn) if sp + sn else 0.0


# ---------------------------------------------------------------- TLD

class TLD:
    """The whole method. theta_nn is the threshold of the nearest neighbor
    classifier on the relative similarity, theta_core the threshold on the
    conservative similarity that makes the trajectory reliable, and margin the
    lambda of the model update."""

    def __init__(self, img, box, theta_nn=0.55, theta_core=0.55, margin=0.1, seed=0):
        self.theta_nn, self.theta_core, self.margin = theta_nn, theta_core, margin
        self.rng = random.Random(seed)
        self.box, self.valid = box, True
        b = tuple(int(round(t)) for t in box)
        self.windows = scan_windows(len(img[0]), len(img), b[2] - b[0], b[3] - b[1])
        self.var_min = 0.5 * box_variance(integral_images(img), b)
        self.ferns = Ferns(seed=seed)
        self.nn = NearestNeighbor()
        self.nn.pos.append(patch(img, box))
        self.learn(img, box, first=True)

    def detect(self, img):
        """The cascade: variance, ferns, nearest neighbor. Returns the boxes
        that pass all three stages."""
        tables = integral_images(img)
        found = []
        for w in self.windows:
            if box_variance(tables, w) < self.var_min:  # @line L8
                continue
            if self.ferns.posterior(self.ferns.codes(img, w)) <= 0.5:  # @line L9
                continue
            if self.nn.relative(patch(img, w)) > self.theta_nn:  # @line L10
                found.append(w)
        return found

    def warp(self, w):
        """A random small change of the box: shift up to 1 percent of its size
        and scale by up to 1 percent."""
        bw, bh = w[2] - w[0], w[3] - w[1]
        du, dv = self.rng.uniform(-0.01, 0.01) * bw, self.rng.uniform(-0.01, 0.01) * bh
        s = 1 + self.rng.uniform(-0.01, 0.01)
        cx, cy = (w[0] + w[2]) / 2 + du, (w[1] + w[3]) / 2 + dv
        return (cx - bw * s / 2, cy - bh * s / 2, cx + bw * s / 2, cy + bh * s / 2)

    def learn(self, img, box, first=False):
        """P-N learning around a reliable box."""
        tables = integral_images(img)
        near = sorted(self.windows, key=lambda w: -iou(w, box))[:10]
        for w in near:  # @line L16
            for _ in range(20 if first else 10):
                codes = self.ferns.codes(img, self.warp(w), self.rng, 5.0)
                if first or self.ferns.posterior(codes) <= 0.5:
                    self.ferns.update(codes, True)
        p = patch(img, box)
        if not first and self.nn.relative(p) - self.theta_nn < self.margin:  # @line L17
            self.nn.pos.append(p)
        for w in self.windows:  # @line L18
            if iou(w, box) >= 0.2 or box_variance(tables, w) < self.var_min:
                continue
            codes = self.ferns.codes(img, w)
            if first or self.ferns.posterior(codes) > 0.5:
                self.ferns.update(codes, False)
                q = patch(img, w)
                if self.nn.relative(q) > self.theta_nn - self.margin:  # @line L19
                    self.nn.neg.append(q)

    def update(self, prev, img):
        """Process the next frame. Returns the box, or None if the object is
        not visible."""
        tracked = median_flow(prev, img, self.box) if self.box else None  # @line L11
        clusters = []
        for w in self.detect(img):  # @line L12
            for c in clusters:
                if iou(c[0], w) > 0.5:
                    c.append(w)
                    break
            else:
                clusters.append([w])
        candidates = [tuple(sum(m[k] for m in c) / len(c) for k in range(4)) for c in clusters]
        if tracked is not None:
            candidates.append(tracked)
        if not candidates:
            self.box, self.valid = None, False
            return None
        conf = [self.nn.conservative(patch(img, c)) for c in candidates]
        best = max(range(len(candidates)), key=lambda i: conf[i])  # @line L13
        from_tracker = tracked is not None and best == len(candidates) - 1
        self.valid = (from_tracker and self.valid) or conf[best] > self.theta_core  # @line L14
        self.box = candidates[best]
        if self.valid:  # @line L15
            self.learn(img, self.box)
        return self.box
