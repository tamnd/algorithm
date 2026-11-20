# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/orthogonal-time-frequency-space-modulation/. The authors are listed in prov/6XP9EH.jsonl.

"""OTFS with rectangular pulses and one cyclic prefix per frame.

A frame carries an N by M grid of symbols x[k][l] in the delay-Doppler domain:
k is the Doppler index (0 <= k < N) and l the delay index (0 <= l < M). The
inverse symplectic finite Fourier transform (ISFFT) takes the grid to the
time-frequency grid X[n][m], and the Heisenberg transform with a rectangular
pulse sends each row n as an M-sample OFDM symbol without its own prefix.
The frame has M N samples and one cyclic prefix. The receiver reverses the
two steps: an M-point DFT of each segment (Wigner transform) and the SFFT.

A channel of P paths with integer delays l_p and Doppler shifts k_p,

    r[q] = sum_p h_p e^(j 2 pi k_p (q - l_p) / (M N)) s[q - l_p],

acts on the delay-Doppler grid as a sparse matrix with P entries per column
(dd_channel). The detector here is the linear MMSE solve with that matrix.
The transforms are unitary, and the FFT sizes must be powers of 2.
"""

import cmath
import math
from typing import Sequence


def fft(a: Sequence[complex], inverse: bool = False) -> list[complex]:
    """Radix-2 DFT with no factor; inverse uses e^(+j). The length must be a power of 2."""
    n = len(a)
    if n & (n - 1):
        raise ValueError("length must be a power of 2")
    a = [complex(v) for v in a]
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
    s = 1 if inverse else -1
    while size <= n:
        w = cmath.exp(s * 2j * math.pi / size)
        for start in range(0, n, size):
            t = 1 + 0j
            for k in range(size // 2):
                u = a[start + k]
                v = a[start + k + size // 2] * t
                a[start + k] = u + v
                a[start + k + size // 2] = u - v
                t *= w
        size *= 2
    return a


def udft(a: Sequence[complex]) -> list[complex]:
    return [v / math.sqrt(len(a)) for v in fft(a)]


def uidft(a: Sequence[complex]) -> list[complex]:
    return [v / math.sqrt(len(a)) for v in fft(a, inverse=True)]


def columns(g: Sequence[Sequence[complex]]) -> list[list[complex]]:
    return [list(c) for c in zip(*g)]


def isfft(x: Sequence[Sequence[complex]]) -> list[list[complex]]:
    """X[n][m] = (1/sqrt(N M)) sum_k sum_l x[k][l] e^(j 2 pi (n k / N - m l / M))."""
    a = columns([uidft(c) for c in columns(x)])  # inverse DFT along Doppler k -> time n
    return [udft(row) for row in a]  # DFT along delay l -> frequency m


def sfft(X: Sequence[Sequence[complex]]) -> list[list[complex]]:
    """The inverse of isfft."""
    a = [uidft(row) for row in X]
    return columns([udft(c) for c in columns(a)])


def modulate(x: Sequence[Sequence[complex]], cp: int) -> list[complex]:
    """The frame of M N samples with a cyclic prefix of cp samples."""
    X = isfft(x)  # @line L1
    s = [v for row in X for v in uidft(row)]  # @line L2
    return s[len(s) - cp:] + s  # @line L3


def demodulate(r: Sequence[complex], n: int, m: int, cp: int) -> list[list[complex]]:
    """The received delay-Doppler grid from one frame with its prefix."""
    body = list(r[cp: cp + n * m])
    Y = [udft(body[i * m: (i + 1) * m]) for i in range(n)]  # @line L4
    return sfft(Y)  # @line L5


def channel(s: Sequence[complex], paths: Sequence[tuple[complex, int, int]], n: int, m: int, cp: int) -> list[complex]:
    """Paths (h, l, k): delay l samples (at most cp) and Doppler k / (M N) cycles per sample."""
    r = [0j] * len(s)
    for h, l, k in paths:
        if l > cp:
            raise ValueError("delay longer than the prefix")
        for q in range(l, len(s)):
            r[q] += h * cmath.exp(2j * math.pi * k * (q - cp - l) / (n * m)) * s[q - l]
    return r


def dd_channel(paths: Sequence[tuple[complex, int, int]], n: int, m: int) -> list[list[complex]]:
    """The M N by M N matrix G with vec(y) = G vec(x), index k M + l, from the path list."""
    size = n * m
    G = [[0j] * size for _ in range(size)]
    for k0 in range(n):
        for l0 in range(m):
            for h, l, k in paths:
                k1, l1 = (k0 + k) % n, (l0 + l) % m
                g = h * cmath.exp(2j * math.pi * k * l0 / size)
                if l0 + l >= m:
                    g *= cmath.exp(-2j * math.pi * k1 / n)
                G[k1 * m + l1][k0 * m + l0] += g
    return G


def solve(a: Sequence[Sequence[complex]], b: Sequence[complex]) -> list[complex]:
    """Gaussian elimination with partial pivoting."""
    size = len(a)
    t = [list(r) + [b[i]] for i, r in enumerate(a)]
    for c in range(size):
        p = max(range(c, size), key=lambda i: abs(t[i][c]))
        if t[p][c] == 0:
            raise ValueError("matrix is singular")
        t[c], t[p] = t[p], t[c]
        for i in range(c + 1, size):
            f = t[i][c] / t[c][c]
            if f:
                ri, rc = t[i], t[c]
                for j in range(c, size + 1):
                    ri[j] -= f * rc[j]
    x = [0j] * size
    for i in range(size - 1, -1, -1):
        x[i] = (t[i][size] - sum(t[i][j] * x[j] for j in range(i + 1, size))) / t[i][i]
    return x


def lmmse(G: Sequence[Sequence[complex]], y: Sequence[Sequence[complex]], noise_var: float) -> list[list[complex]]:
    """x = (G^H G + noise_var I)^-1 G^H y for unit-energy symbols, on the grid."""
    size = len(G)
    m = len(y[0])
    v = [c for row in y for c in row]
    Gh = [[G[i][j].conjugate() for i in range(size)] for j in range(size)]
    A = [[sum(Gh[i][t] * G[t][j] for t in range(size)) + (noise_var if i == j else 0) for j in range(size)] for i in range(size)]
    z = [sum(Gh[i][t] * v[t] for t in range(size)) for i in range(size)]
    x = solve(A, z)  # @line L6
    return [x[i * m: (i + 1) * m] for i in range(size // m)]
