# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/modified-discrete-cosine-transform/. The authors are listed in prov/PVNJ5C.jsonl.

"""The modified discrete cosine transform (MDCT), its inverse and overlap-add, in pure Python.

A frame has 2N samples and gives N coefficients. Frames overlap by N samples.
With a window w of length 2N that is symmetric, w[n] = w[2N - 1 - n], and
meets the Princen-Bradley condition w[n]^2 + w[n + N]^2 = 1, the time domain
aliasing of the inverse cancels in the overlap-add, and the signal comes back
exactly (up to rounding).

mdct and imdct follow the definition in Theta(N^2) operations. fast_mdct and
fast_imdct fold the frame into a DCT-IV of length N and compute that with one
complex FFT of length N/2, in Theta(N log N) operations.
"""

import cmath
import math
from typing import List, Sequence

Vector = List[float]


def sine_window(n: int) -> Vector:
    """The sine window of length 2N: w[i] = sin(pi (i + 1/2) / (2N))."""
    return [math.sin(math.pi * (i + 0.5) / (2 * n)) for i in range(2 * n)]


def _bessel_i0(x: float) -> float:
    """Modified Bessel function I_0 by its power series."""
    total, term, k = 1.0, 1.0, 0
    while term > 1e-17 * total:
        k += 1
        term *= (x / (2.0 * k)) ** 2
        total += term
    return total


def kbd_window(n: int, alpha: float) -> Vector:
    """Kaiser-Bessel-derived window of length 2N with parameter alpha.

    v is the Kaiser window of length N + 1. Then w[i] = sqrt(sum_{j <= i} v[j] / sum_j v[j])
    for i < N, and w[2N - 1 - i] = w[i].
    """
    v = [_bessel_i0(math.pi * alpha * math.sqrt(max(0.0, 1.0 - (2.0 * j / n - 1.0) ** 2))) for j in range(n + 1)]
    total = sum(v)
    w = [0.0] * (2 * n)
    acc = 0.0
    for i in range(n):
        acc += v[i]
        w[i] = math.sqrt(acc / total)
        w[2 * n - 1 - i] = w[i]
    return w


def mdct(x: Sequence[float], w: Sequence[float]) -> Vector:
    """Windowed orthonormal MDCT of one frame of 2N samples. Cost Theta(N^2).

    X[k] = sqrt(2/N) sum_{i=0}^{2N-1} w[i] x[i] cos(pi/N (i + 1/2 + N/2)(k + 1/2)).
    """
    n2 = len(x)
    n = n2 // 2
    g = math.sqrt(2.0 / n)
    out = []
    for k in range(n):  # @line L1
        out.append(g * sum(w[i] * x[i] * math.cos(math.pi / n * (i + 0.5 + n / 2.0) * (k + 0.5)) for i in range(n2)))  # @line L2
    return out


def imdct(c: Sequence[float], w: Sequence[float]) -> Vector:
    """Windowed inverse MDCT: 2N samples with time domain aliasing. Cost Theta(N^2).

    y[i] = sqrt(2/N) w[i] sum_{k=0}^{N-1} X[k] cos(pi/N (i + 1/2 + N/2)(k + 1/2)).
    """
    n = len(c)
    g = math.sqrt(2.0 / n)
    out = []
    for i in range(2 * n):  # @line L3
        out.append(g * w[i] * sum(c[k] * math.cos(math.pi / n * (i + 0.5 + n / 2.0) * (k + 0.5)) for k in range(n)))  # @line L4
    return out


def analysis(signal: Sequence[float], n: int, w: Sequence[float], transform=None) -> List[Vector]:
    """Split a signal into frames of 2N samples with hop N and transform each frame.

    The signal is padded with N zeros in front and with zeros at the end up
    to a multiple of N plus N, so that every sample lies in two frames.
    """
    transform = transform or mdct
    pad = [0.0] * n + list(signal)
    pad += [0.0] * ((-len(signal)) % n + n)
    frames = []
    for start in range(0, len(pad) - n, n):  # @line L5
        frames.append(transform(pad[start:start + 2 * n], w))  # @line L6
    return frames


def synthesis(frames: Sequence[Sequence[float]], n: int, w: Sequence[float], length: int, inverse=None) -> Vector:
    """Inverse MDCT of each frame and overlap-add with hop N (TDAC). Returns length samples."""
    inverse = inverse or imdct
    out = [0.0] * (n * (len(frames) + 1))
    for t, c in enumerate(frames):  # @line L7
        y = inverse(c, w)  # @line L8
        for i in range(2 * n):  # @line L9
            out[t * n + i] += y[i]
    return out[n:n + length]  # @line L10


def _fft(a: List[complex]) -> List[complex]:
    """Iterative radix-2 FFT, X[k] = sum_j a[j] exp(-2 pi i j k / m). len(a) is a power of two."""
    m = len(a)
    a = list(a)
    j = 0
    for i in range(1, m):
        bit = m >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j |= bit
        if i < j:
            a[i], a[j] = a[j], a[i]
    size = 2
    while size <= m:
        step = cmath.exp(-2j * math.pi / size)
        for start in range(0, m, size):
            tw = 1.0 + 0.0j
            for k in range(size // 2):
                u = a[start + k]
                v = a[start + k + size // 2] * tw
                a[start + k] = u + v
                a[start + k + size // 2] = u - v
                tw *= step
        size *= 2
    return a


def dct4(u: Sequence[float]) -> Vector:
    """Unnormalized DCT-IV, X[k] = sum_j u[j] cos(pi/N (j + 1/2)(k + 1/2)), by an FFT of length N/2.

    Precondition: N is a power of two and N >= 2.
    """
    n = len(u)
    h = n // 2
    z = [complex(u[2 * j], u[n - 1 - 2 * j]) * cmath.exp(-1j * math.pi * (4 * j + 1) / (4 * n)) for j in range(h)]
    big = _fft(z)
    out = [0.0] * n
    for k in range(h):
        d = big[k] * cmath.exp(-1j * math.pi * k / n)
        out[2 * k] = d.real
        out[n - 1 - 2 * k] = -d.imag
    return out


def fast_mdct(x: Sequence[float], w: Sequence[float]) -> Vector:
    """Same output as mdct, by folding to a DCT-IV of length N. N a power of two, N >= 2."""
    n = len(x) // 2
    h = n // 2
    z = [w[i] * x[i] for i in range(2 * n)]
    u = [0.0] * n
    for j in range(h):
        u[j] = -z[3 * h - 1 - j] - z[3 * h + j]
    for j in range(h, n):
        u[j] = z[j - h] - z[3 * h - 1 - j]
    g = math.sqrt(2.0 / n)
    return [g * v for v in dct4(u)]


def fast_imdct(c: Sequence[float], w: Sequence[float]) -> Vector:
    """Same output as imdct: a DCT-IV of length N, then unfolding to 2N samples."""
    n = len(c)
    h = n // 2
    v = dct4(c)
    g = math.sqrt(2.0 / n)
    y = [0.0] * (2 * n)
    for i in range(2 * n):
        m = i + h
        if m < n:
            val = v[m]
        elif m < 2 * n:
            val = -v[2 * n - 1 - m]
        else:
            val = -v[m - 2 * n]
        y[i] = g * w[i] * val
    return y
