# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/phase-correlation/. The authors are listed in prov/D7EB05.jsonl.

"""Phase correlation: estimate a translation from the phase of the cross-power spectrum.

An image is a list of H rows of W real numbers; pixel (x, y) is img[y][x].
The border rule is circular: index x is taken mod W and y mod H. For a shift
(dx, dy) the moved image is g[y][x] = f[(y - dy) % H][(x - dx) % W].

The DFT is F[l][k] = sum f[y][x] exp(-2 pi i (k x / W + l y / H)). The
normalized cross-power spectrum R = G conj(F) / |G conj(F)| is set to 0 at the
bins where G conj(F) is 0. The inverse DFT of R has its peak at (dx, dy).
"""

import cmath
import math


def _fft_pow2(a, invert):
    n = len(a)
    a = list(a)
    j = 0
    for i in range(1, n):
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j |= bit
        if i < j:
            a[i], a[j] = a[j], a[i]
    sign = 1 if invert else -1
    length = 2
    while length <= n:
        wl = cmath.exp(sign * 2j * math.pi / length)
        half = length // 2
        for start in range(0, n, length):
            wk = 1 + 0j
            for k in range(half):
                x = a[start + k]
                y = a[start + k + half] * wk
                a[start + k] = x + y
                a[start + k + half] = x - y
                wk *= wl
        length <<= 1
    return a


def _dft_direct(a, invert):
    n = len(a)
    sign = 1 if invert else -1
    roots = [cmath.exp(sign * 2j * math.pi * m / n) for m in range(n)]
    return [sum(a[x] * roots[(k * x) % n] for x in range(n)) for k in range(n)]


def dft(a, invert=False):
    """1D DFT without the 1/n factor. Radix-2 FFT for a power-of-two length, direct O(n^2) sum otherwise."""
    n = len(a)
    if n & (n - 1) == 0:
        return _fft_pow2(a, invert)
    return _dft_direct(a, invert)


def dft2(img, invert=False):
    """Separable 2D DFT: rows, then columns. The inverse divides by W H."""
    h, w = len(img), len(img[0])
    rows = [dft([complex(v) for v in r], invert) for r in img]
    cols = [dft([rows[y][x] for y in range(h)], invert) for x in range(w)]
    out = [[cols[x][y] for x in range(w)] for y in range(h)]
    if invert:
        scale = w * h
        out = [[v / scale for v in r] for r in out]
    return out


def dft2_direct(img):
    """The 2D DFT by its definition, O((W H)^2). A reference for tests."""
    h, w = len(img), len(img[0])
    return [[sum(img[y][x] * cmath.exp(-2j * math.pi * (k * x / w + l * y / h))
                 for y in range(h) for x in range(w))
             for k in range(w)] for l in range(h)]


def circular_shift(img, dx, dy):
    """g[y][x] = f[(y - dy) % H][(x - dx) % W]."""
    h, w = len(img), len(img[0])
    return [[img[(y - dy) % h][(x - dx) % w] for x in range(w)] for y in range(h)]


def cross_power_spectrum(f_hat, g_hat, eps=1e-12):
    """R = G conj(F) / |G conj(F)|, and 0 where |G conj(F)| <= eps times the largest magnitude."""
    prod = [[gv * fv.conjugate() for fv, gv in zip(fr, gr)] for fr, gr in zip(f_hat, g_hat)]  # @line L3
    top = max(abs(v) for r in prod for v in r)
    cut = eps * top if top > 0 else 0.0
    out = []
    for row in prod:  # @line L2
        out.append([(v / abs(v)) if abs(v) > cut else 0j for v in row])  # @line L4
    return out


def correlation_surface(f, g):
    """The real part of the inverse DFT of the normalized cross-power spectrum."""
    f_hat = dft2(f)  # @line L1
    g_hat = dft2(g)
    r = cross_power_spectrum(f_hat, g_hat)
    return [[v.real for v in row] for row in dft2(r, invert=True)]  # @line L5


def phase_correlation(f, g):
    """Return (dx, dy, peak). (dx, dy) is the first maximum of the surface in row-major order."""
    surf = correlation_surface(f, g)
    best = None
    for y, row in enumerate(surf):
        for x, val in enumerate(row):
            if best is None or val > best[2]:  # @line L6
                best = (x, y, val)
    return best  # @line L7


def signed_shift(dx, dy, w, h):
    """Map a peak index to a shift in (-W/2, W/2] by (-H/2, H/2]."""
    if dx > w // 2:  # @line L8
        dx -= w
    if dy > h // 2:  # @line L9
        dy -= h
    return dx, dy
