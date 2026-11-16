# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/siamese-tracking/. The authors are listed in prov/RDHCZ9.jsonl.
"""Siamese tracking by cross-correlation of feature maps.

The embedding here is fixed: four 3 x 3 gradient filters with a ReLU, stride 1
and no padding. A trained network is outside this page; any function with the
same signature (image in, list of channel maps out, no padding) can replace
`features`, and the rest of the code does not change.

Images are lists of rows, img[v][u], and pixel (u, v) has its center at (u, v).
"""

import math

KERNELS = [
    [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]],  # horizontal gradient
    [[1, 0, -1], [2, 0, -2], [1, 0, -1]],
    [[-1, -2, -1], [0, 0, 0], [1, 2, 1]],  # vertical gradient
    [[1, 2, 1], [0, 0, 0], [-1, -2, -1]],
]


def features(img):
    """phi(img): valid 3 x 3 correlation with each kernel, then ReLU. Stride 1."""
    h, w = len(img), len(img[0])
    out = []
    for k in KERNELS:
        ch = []
        for v in range(h - 2):
            r0, r1, r2 = img[v], img[v + 1], img[v + 2]
            row = []
            for u in range(w - 2):
                s = (k[0][0] * r0[u] + k[0][1] * r0[u + 1] + k[0][2] * r0[u + 2]
                     + k[1][0] * r1[u] + k[1][1] * r1[u + 1] + k[1][2] * r1[u + 2]
                     + k[2][0] * r2[u] + k[2][1] * r2[u + 1] + k[2][2] * r2[u + 2])
                row.append(s if s > 0 else 0.0)
            ch.append(row)
        out.append(ch)
    return out


def xcorr(fz, fx, bias=0.0):
    """Score map v[i][j] = sum over c, a, b of fz[c][a][b] * fx[c][i + a][j + b] + bias."""
    hz, wz = len(fz[0]), len(fz[0][0])
    hx, wx = len(fx[0]), len(fx[0][0])
    out = [[bias] * (wx - wz + 1) for _ in range(hx - hz + 1)]
    for cz, cx in zip(fz, fx):
        for a in range(hz):
            zrow = cz[a]
            terms = [(b, t) for b, t in enumerate(zrow) if t != 0.0]
            for i in range(hx - hz + 1):
                xrow = cx[i + a]
                orow = out[i]
                for j in range(wx - wz + 1):
                    s = 0.0
                    for b, t in terms:
                        s += t * xrow[j + b]
                    orow[j] += s
    return out


def score(z, x, bias=0.0):
    """f(z, x) = phi(z) * phi(x) + b, one value per translated sub-window of x."""
    return xcorr(features(z), features(x), bias)


def logistic_loss(y, v):
    """l(y, v) = log(1 + exp(-y v)), computed without overflow."""
    m = -y * v
    return m + math.log1p(math.exp(-m)) if m > 0 else math.log1p(math.exp(m))


def logistic_grad(y, v):
    """d l / d v = -y / (1 + exp(y v))."""
    m = y * v
    if m >= 0:
        e = math.exp(-m)
        return -y * e / (1 + e)
    return -y / (1 + math.exp(m))


def label_map(size, radius, stride):
    """y[u] = +1 if stride * |u - c| <= radius, else -1, on a size x size map."""
    c = (size - 1) / 2
    return [[1 if stride * math.hypot(i - c, j - c) <= radius else -1  # @line L1
             for j in range(size)] for i in range(size)]


def map_loss(y, v, balance=True):
    """Mean logistic loss over the map; with balance, positives and negatives weigh half each."""
    cells = [(a, b) for ra, rb in zip(y, v) for a, b in zip(ra, rb)]
    npos = sum(1 for a, _ in cells if a > 0)
    nneg = len(cells) - npos
    total = 0.0
    for a, b in cells:  # @line L2
        if balance:
            wgt = 0.5 / npos if a > 0 else 0.5 / nneg
        else:
            wgt = 1.0 / len(cells)
        total += wgt * logistic_loss(a, b)
    return total


def bias_step(y, v, bias, rate):
    """One gradient step of line L3 for the bias alone; dv[u]/db = 1 for every cell.

    The step for the weights of phi needs the network and is outside this page.
    """
    cells = [(a, b) for ra, rb in zip(y, v) for a, b in zip(ra, rb)]
    npos = sum(1 for a, _ in cells if a > 0)
    nneg = len(cells) - npos
    grad = sum((0.5 / npos if a > 0 else 0.5 / nneg) * logistic_grad(a, b) for a, b in cells)
    return bias - rate * grad, grad  # @line L3


def bilinear(img, x, y, fill):
    h, w = len(img), len(img[0])
    if x < 0 or y < 0 or x > w - 1 or y > h - 1:
        return fill
    u0, v0 = min(int(x), w - 2), min(int(y), h - 2)
    a, b = x - u0, y - v0
    r0, r1 = img[v0], img[v0 + 1]
    return ((1 - a) * (1 - b) * r0[u0] + a * (1 - b) * r0[u0 + 1]
            + (1 - a) * b * r1[u0] + a * b * r1[u0 + 1])


def crop(img, center, side, out, fill):
    """Resample the square of the given side around center to out x out pixels."""
    step = side / out
    cx, cy = center
    h = (out - 1) / 2
    return [[bilinear(img, cx + (j - h) * step, cy + (i - h) * step, fill)
             for j in range(out)] for i in range(out)]


def cubic_weights(t):
    """Keys cubic convolution weights (a = -0.5) for the taps at -1, 0, 1, 2, with 0 <= t < 1."""
    a = -0.5

    def k(s):
        s = abs(s)
        if s <= 1:
            return (a + 2) * s ** 3 - (a + 3) * s ** 2 + 1
        if s < 2:
            return a * s ** 3 - 5 * a * s ** 2 + 8 * a * s - 4 * a
        return 0.0

    return [k(t + 1), k(t), k(1 - t), k(2 - t)]


def upsample(m, factor):
    """Bicubic upsampling of a square map; output pixel k sits at k / factor.

    Bilinear upsampling would be useless here: its maximum is always at a node
    of the original grid, so it cannot move the peak by less than one cell.
    """
    n = len(m)
    size = (n - 1) * factor + 1
    taps = []
    for k in range(size):
        i0 = min(k // factor, n - 1)
        wts = cubic_weights(k / factor - i0)
        taps.append([(min(max(i0 + d, 0), n - 1), w) for d, w in zip((-1, 0, 1, 2), wts)])
    rows = [[sum(w * row[j] for j, w in tj) for tj in taps] for row in m]
    return [[sum(w * rows[i][c] for i, w in ti) for c in range(size)] for ti in taps]


def hann(n):
    if n == 1:
        return [[1.0]]
    """Outer product of two Hann windows; 1 at the center, 0 at the border."""
    h = [0.5 - 0.5 * math.cos(2 * math.pi * k / (n - 1)) for k in range(n)]
    return [[a * b for b in h] for a in h]


def context_side(w, h):
    """Side of the square with the area of (w + 2p) x (h + 2p), p = (w + h) / 4."""
    p = (w + h) / 4
    return math.sqrt((w + 2 * p) * (h + 2 * p))


class SiameseTracker:
    def __init__(self, img, box, exemplar=20, search=44, scales=(1 / 1.025, 1.0, 1.025),
                 scale_penalty=0.97, damping=0.35, window=0.25, up=4):
        x1, y1, x2, y2 = box
        self.center = ((x1 + x2) / 2 - 0.5, (y1 + y2) / 2 - 0.5)  # pixel centers at integers
        self.size = (x2 - x1, y2 - y1)
        self.ez, self.ex = exemplar, search
        self.scales, self.penalty, self.damping = scales, scale_penalty, damping
        self.window, self.up = window, up
        side = context_side(*self.size)
        fill = sum(map(sum, img)) / (len(img) * len(img[0]))
        self.fz = features(crop(img, self.center, side, exemplar, fill))  # @line L4
        self.side = side
        n = search - exemplar + 1
        self.cos = hann((n - 1) * up + 1)

    def update(self, img):
        fill = sum(map(sum, img)) / (len(img) * len(img[0]))
        maps = []
        for s in self.scales:  # @line L5
            side = self.side * s * self.ex / self.ez
            x = crop(img, self.center, side, self.ex, fill)
            v = xcorr(self.fz, features(x))  # @line L6
            peak = max(map(max, v))
            maps.append((peak * (1.0 if s == 1.0 else self.penalty), s, v, side))  # @line L7
        _, s_best, v, side = max(maps, key=lambda t: t[0])  # @line L8
        big = upsample(v, self.up)
        lo = min(map(min, big))
        hi = max(map(max, big))
        span = hi - lo if hi > lo else 1.0
        best, bi, bj = -1.0, 0, 0
        for i, (row, crow) in enumerate(zip(big, self.cos)):  # @line L9
            for j, (t, c) in enumerate(zip(row, crow)):
                val = (1 - self.window) * (t - lo) / span + self.window * c
                if val > best:
                    best, bi, bj = val, i, j
        c = (len(big) - 1) / 2
        px = side / self.ex  # image pixels per search-crop pixel; the stride is 1
        du, dv = (bj - c) / self.up * px, (bi - c) / self.up * px  # @line L10
        self.center = (self.center[0] + du, self.center[1] + dv)
        f = (1 - self.damping) + self.damping * s_best  # @line L11
        self.side *= f
        self.size = (self.size[0] * f, self.size[1] * f)
        w, h = self.size
        cx, cy = self.center[0] + 0.5, self.center[1] + 0.5
        return (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)  # @line L12
