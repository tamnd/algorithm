# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mosse-filter/. The authors are listed in prov/Q4156Y.jsonl.

"""The MOSSE correlation filter tracker of Bolme, Beveridge, Draper and Lui
(2010), with a radix-2 FFT in pure Python.

Images are lists of rows, indexed img[v][u]; the center of pixel (u, v) is the
point (u, v). Patches are n x n with n a power of two; the center of a patch
is its pixel (n // 2, n // 2). Correlation is circular: the response is
g[v][u] = sum over (i, j) of f[(j + v) % n][(i + u) % n] h[j][i], so that
G = F . conj(H) in the Fourier domain.
"""

import cmath
import math
import random


def fft(x, inverse=False):
    """Radix-2 FFT of a list of complex numbers whose length is a power of
    two. The inverse transform includes the factor 1 / n."""
    n = len(x)
    if n & (n - 1):
        raise ValueError("length must be a power of two")
    a = list(x)
    j = 0
    for i in range(1, n):
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j |= bit
        if i < j:
            a[i], a[j] = a[j], a[i]
    size = 2
    sign = 1 if inverse else -1
    while size <= n:
        w = cmath.exp(sign * 2j * math.pi / size)
        for start in range(0, n, size):
            t = 1
            for k in range(size // 2):
                e, o = a[start + k], a[start + k + size // 2] * t
                a[start + k], a[start + k + size // 2] = e + o, e - o
                t *= w
        size *= 2
    if inverse:
        a = [z / n for z in a]
    return a


def fft2(img, inverse=False):
    rows = [fft(row, inverse) for row in img]
    cols = [fft([rows[v][u] for v in range(len(rows))], inverse) for u in range(len(rows[0]))]
    return [[cols[u][v] for u in range(len(cols))] for v in range(len(rows))]


def gaussian_target(n, sigma=2.0):
    """The desired output: a Gaussian peak at the patch center."""
    c = n // 2
    return [[math.exp(-((u - c) ** 2 + (v - c) ** 2) / (2 * sigma * sigma)) for u in range(n)]
            for v in range(n)]


def preprocess(patch):
    """Log transform, zero mean and unit norm, then a cosine window."""
    n = len(patch)
    x = [[math.log(p + 1.0) for p in row] for row in patch]
    mean = sum(map(sum, x)) / (n * n)
    x = [[p - mean for p in row] for row in x]
    norm = math.sqrt(sum(p * p for row in x for p in row)) or 1.0
    win = [math.sin(math.pi * (i + 0.5) / n) for i in range(n)]
    return [[x[v][u] / norm * win[u] * win[v] for u in range(n)] for v in range(n)]


def sample(img, u, v):
    """Bilinear sample at a real point, indices clamped."""
    h, w = len(img), len(img[0])
    u0, v0 = math.floor(u), math.floor(v)
    fu, fv = u - u0, v - v0

    def at(vv, uu):
        return img[min(max(vv, 0), h - 1)][min(max(uu, 0), w - 1)]

    return ((1 - fv) * ((1 - fu) * at(v0, u0) + fu * at(v0, u0 + 1))
            + fv * ((1 - fu) * at(v0 + 1, u0) + fu * at(v0 + 1, u0 + 1)))


def crop(img, center, n, affine=None):
    """The n x n patch whose center pixel is at `center`. If `affine` is a
    2 x 2 matrix, patch offsets are mapped through it first."""
    c = n // 2
    a = affine or [[1.0, 0.0], [0.0, 1.0]]
    out = []
    for v in range(n):
        row = []
        for u in range(n):
            du, dv = u - c, v - c
            row.append(sample(img, center[0] + a[0][0] * du + a[0][1] * dv,
                              center[1] + a[1][0] * du + a[1][1] * dv))
        out.append(row)
    return out


def response(f_hat, a_hat, b_hat, eps):
    """The spatial response g = IFFT(F . A / (B + eps))."""
    n = len(f_hat)
    g_hat = [[f_hat[v][u] * a_hat[v][u] / (b_hat[v][u] + eps) for u in range(n)] for v in range(n)]
    return [[z.real for z in row] for row in fft2(g_hat, inverse=True)]


def psr(g, exclude=5):
    """Peak to sidelobe ratio: (peak - mean) / std of the response outside
    the (2 exclude + 1)-square around the peak. Returns (psr, (pu, pv))."""
    n = len(g)
    pv, pu = max(((v, u) for v in range(n) for u in range(n)), key=lambda t: g[t[0]][t[1]])
    side = [g[v][u] for v in range(n) for u in range(n)
            if min(abs(u - pu), n - abs(u - pu)) > exclude or min(abs(v - pv), n - abs(v - pv)) > exclude]
    mean = sum(side) / len(side)
    std = math.sqrt(sum((s - mean) ** 2 for s in side) / len(side))
    return (g[pv][pu] - mean) / std if std > 0 else math.inf, (pu, pv)


class Mosse:
    def __init__(self, img, center, n=32, sigma=2.0, eta=0.125, eps=1e-5,
                 perturbations=8, seed=0, psr_min=7.0):
        self.n, self.eta, self.eps, self.psr_min = n, eta, eps, psr_min
        self.center = center
        self.g_hat = fft2(gaussian_target(n, sigma))
        rng = random.Random(seed)
        affines = [None]
        for _ in range(perturbations):
            t = rng.uniform(-0.15, 0.15)
            s = rng.uniform(0.9, 1.1)
            affines.append([[s * math.cos(t), -s * math.sin(t)], [s * math.sin(t), s * math.cos(t)]])
        self.a_hat = [[0j] * n for _ in range(n)]
        self.b_hat = [[0j] * n for _ in range(n)]
        for aff in affines:  # @line L1
            f_hat = fft2(preprocess(crop(img, center, n, aff)))
            for v in range(n):  # @line L2
                for u in range(n):
                    self.a_hat[v][u] += self.g_hat[v][u] * f_hat[v][u].conjugate()
                    self.b_hat[v][u] += f_hat[v][u] * f_hat[v][u].conjugate()

    def update(self, img):
        """Track into the next frame. Returns (center, psr, ok)."""
        n = self.n
        f_hat = fft2(preprocess(crop(img, self.center, n)))  # @line L3
        g = response(f_hat, self.a_hat, self.b_hat, self.eps)  # @line L4
        score, (pu, pv) = psr(g)  # @line L5
        if score < self.psr_min:  # @line L6
            return self.center, score, False
        du, dv = pu - n // 2, pv - n // 2
        self.center = (self.center[0] + du, self.center[1] + dv)  # @line L7
        f_hat = fft2(preprocess(crop(img, self.center, n)))  # @line L8
        for v in range(n):  # @line L9
            for u in range(n):
                self.a_hat[v][u] = (self.eta * self.g_hat[v][u] * f_hat[v][u].conjugate()
                                    + (1 - self.eta) * self.a_hat[v][u])
                self.b_hat[v][u] = (self.eta * f_hat[v][u] * f_hat[v][u].conjugate()
                                    + (1 - self.eta) * self.b_hat[v][u])
        return self.center, score, True  # @line L10
