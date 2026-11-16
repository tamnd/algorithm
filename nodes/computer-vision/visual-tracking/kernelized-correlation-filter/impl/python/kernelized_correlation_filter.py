# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kernelized-correlation-filter/. The authors are listed in prov/D8MKGV.jsonl.

"""The kernelized correlation filter (Henriques, Caseiro, Martins and Batista,
2015) on single-channel patches, with a radix-2 FFT in pure Python.

A patch is an r x c array (r and c powers of two) indexed x[v][u], P = r c.
The cyclic shift by d = (du, dv) is (S_d x)[v][u] = x[(v - dv) % r][(u - du) % c].
The training set is every shift S_d x with the label y(d), a Gaussian of the
wrapped shift d. The response at d is the regression value of S_{-d} z, so a
patch z = S_d x gives the peak at d.

kernel(z, x)[s] is kappa(z, S_s x) for every shift s. For the Gaussian kernel
kappa(a, b) = exp(-|a - b|^2 / (sigma^2 P)) (the division by P follows the
authors' code); for the linear kernel kappa(a, b) = <a, b> / P.
"""

import cmath
import math


def fft(x, inverse=False):
    """Radix-2 FFT; the inverse includes the factor 1 / n."""
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


def shift(x, d):
    """The cyclic shift S_d x."""
    r, c = len(x), len(x[0])
    return [[x[(v - d[1]) % r][(u - d[0]) % c] for u in range(c)] for v in range(r)]


def wrap(i, n):
    """The representative of i modulo n in [-n/2, n/2)."""
    return (i + n // 2) % n - n // 2


def gaussian_labels(r, c, s):
    """y(d) = exp(-|d|^2 / (2 s^2)) with d wrapped, so the peak is at d = 0."""
    return [[math.exp(-(wrap(u, c) ** 2 + wrap(v, r) ** 2) / (2 * s * s)) for u in range(c)]
            for v in range(r)]


def kernel(z, x, sigma=None):
    """The array k[s] = kappa(z, S_s x) for every shift s, by the FFT. With
    sigma None the kernel is linear, otherwise Gaussian."""
    r, c = len(x), len(x[0])
    p = r * c
    zf, xf = fft2(z), fft2(x)
    # cross[s] = sum_t z(t) x(t - s), whose transform is zf . conj(xf)
    cross = fft2([[zf[v][u] * xf[v][u].conjugate() for u in range(c)] for v in range(r)], inverse=True)  # @line L1
    if sigma is None:
        return [[cross[v][u].real / p for u in range(c)] for v in range(r)]
    zz = sum(t * t for row in z for t in row)
    xx = sum(t * t for row in x for t in row)
    return [[math.exp(-max(zz + xx - 2 * cross[v][u].real, 0.0) / (sigma * sigma * p))  # @line L2
             for u in range(c)] for v in range(r)]


def train(x, y, lam, sigma=None):
    """The transform of the dual coefficients: alpha_hat = y_hat / (k_hat + lam)."""
    kf = fft2(kernel(x, x, sigma))  # @line L3
    yf = fft2(y)
    return [[yf[v][u] / (kf[v][u] + lam) for u in range(len(y[0]))] for v in range(len(y))]  # @line L4


def detect(alpha_f, x, z, sigma=None):
    """The response r(d) = sum_e alpha(e) kappa(S_{-d} z, S_e x) for every d."""
    kf = fft2(kernel(z, x, sigma))  # @line L5
    rf = [[kf[v][u] * alpha_f[v][u].conjugate() for u in range(len(x[0]))] for v in range(len(x))]
    return [[t.real for t in row] for row in fft2(rf, inverse=True)]  # @line L6


def sample(img, u, v):
    h, w = len(img), len(img[0])
    u0, v0 = math.floor(u), math.floor(v)
    fu, fv = u - u0, v - v0

    def at(vv, uu):
        return img[min(max(vv, 0), h - 1)][min(max(uu, 0), w - 1)]

    return ((1 - fv) * ((1 - fu) * at(v0, u0) + fu * at(v0, u0 + 1))
            + fv * ((1 - fu) * at(v0 + 1, u0) + fu * at(v0 + 1, u0 + 1)))


class KCF:
    """A tracker on raw gray values scaled to [-0.5, 0.5] with a cosine window."""

    def __init__(self, img, center, n=32, target=13, sigma=0.2, lam=1e-4, gamma=0.075):
        self.n, self.sigma, self.lam, self.gamma = n, sigma, lam, gamma
        self.center = center
        self.win = [math.sin(math.pi * (i + 0.5) / n) for i in range(n)]
        self.y = gaussian_labels(n, n, target / 10)
        self.x = self.features(img, center)
        self.alpha_f = train(self.x, self.y, lam, sigma)

    def features(self, img, center):
        n, c = self.n, self.n // 2
        return [[(sample(img, center[0] + u - c, center[1] + v - c) / 255 - 0.5) * self.win[u] * self.win[v]
                 for u in range(n)] for v in range(n)]

    def update(self, img):
        """Track into the next frame and update the model. Returns the center."""
        n = self.n
        z = self.features(img, self.center)
        resp = detect(self.alpha_f, self.x, z, self.sigma)  # @line L7
        pv, pu = max(((v, u) for v in range(n) for u in range(n)), key=lambda t: resp[t[0]][t[1]])
        self.center = (self.center[0] + wrap(pu, n), self.center[1] + wrap(pv, n))  # @line L8
        x_new = self.features(img, self.center)
        a_new = train(x_new, self.y, self.lam, self.sigma)  # @line L9
        g = self.gamma
        self.x = [[(1 - g) * a + g * b for a, b in zip(r1, r2)] for r1, r2 in zip(self.x, x_new)]  # @line L10
        self.alpha_f = [[(1 - g) * a + g * b for a, b in zip(r1, r2)] for r1, r2 in zip(self.alpha_f, a_new)]
        return self.center  # @line L11
