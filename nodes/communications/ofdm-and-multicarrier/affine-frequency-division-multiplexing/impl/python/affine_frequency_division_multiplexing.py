# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/affine-frequency-division-multiplexing/. The authors are listed in prov/94W5XF.jsonl.

"""AFDM: N symbols on N chirps given by the inverse discrete affine Fourier transform.

The transmitted block is

    s[n] = (1/sqrt(N)) sum_m x[m] e^(j 2 pi (c1 n^2 + c2 m^2 + n m / N)),

an inverse DFT between two chirp multiplications. The chirp-periodic prefix
s[n] = s[N + n] e^(-j 2 pi c1 (N^2 + 2 N n)), for -cp <= n < 0, makes this
formula hold for negative n too. A path with gain h, integer delay l and
integer Doppler a (in units of 1 / N cycles per sample),

    r[n] = h e^(j 2 pi a n / N) s[n - l],

moves symbol m to bin q = (m + a - 2 N c1 l) mod N of the receiver's
forward transform when 2 N c1 is an integer. With c1 = (2 A + 1) / (2 N),
paths with |a| <= A and 0 <= l <= L land on distinct bins whenever
(L + 1)(2 A + 1) <= N. The FFT size must be a power of 2.
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


def chirp(c: float, n: int) -> complex:
    return cmath.exp(2j * math.pi * c * n * n)


def c1_for(max_doppler: int, n: int) -> float:
    """The chirp rate c1 = (2 A + 1) / (2 N) that separates Dopplers |a| <= A."""
    return (2 * max_doppler + 1) / (2 * n)


def modulate(x: Sequence[complex], c1: float, c2: float, cp: int) -> list[complex]:
    """The block with its chirp-periodic prefix of cp samples."""
    n = len(x)
    u = [x[m] * chirp(c2, m) for m in range(n)]
    v = fft(u, inverse=True)
    s = [v[t] / math.sqrt(n) * chirp(c1, t) for t in range(n)]  # @line L1
    pre = [s[n + t] * cmath.exp(-2j * math.pi * c1 * (n * n + 2 * n * t)) for t in range(-cp, 0)]  # @line L2
    return pre + s  # @line L3


def demodulate(r: Sequence[complex], n: int, c1: float, c2: float, cp: int) -> list[complex]:
    """The forward transform of one received block after its prefix."""
    body = list(r[cp: cp + n])
    v = [body[t] * chirp(-c1, t) for t in range(n)]
    u = fft(v)
    return [u[q] / math.sqrt(n) * chirp(-c2, q) for q in range(n)]  # @line L4


def channel(s: Sequence[complex], paths: Sequence[tuple[complex, int, int]], n: int, cp: int) -> list[complex]:
    """Paths (h, l, a): delay l samples (at most cp) and Doppler a / N cycles per sample."""
    r = [0j] * len(s)
    for h, l, a in paths:
        if l > cp:
            raise ValueError("delay longer than the prefix")
        for t in range(l, len(s)):
            r[t] += h * cmath.exp(2j * math.pi * a * (t - cp) / n) * s[t - l]
    return r


def effective_channel(paths: Sequence[tuple[complex, int, int]], n: int, c1: float, c2: float) -> list[list[complex]]:
    """The N by N matrix H with y = H x in the noiseless case. Needs 2 N c1 to be an integer."""
    q2 = 2 * n * c1
    if abs(q2 - round(q2)) > 1e-9:
        raise ValueError("2 N c1 must be an integer")
    q2 = round(q2)
    H = [[0j] * n for _ in range(n)]
    for h, l, a in paths:
        for m in range(n):
            q = (m + a - q2 * l) % n
            H[q][m] += h * cmath.exp(2j * math.pi * (c1 * l * l - l * m / n + c2 * (m * m - q * q)))
    return H


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


def lmmse(H: Sequence[Sequence[complex]], y: Sequence[complex], noise_var: float) -> list[complex]:
    """x = (H^H H + noise_var I)^-1 H^H y for unit-energy symbols."""
    n = len(H)
    Hh = [[H[i][j].conjugate() for i in range(n)] for j in range(n)]
    A = [[sum(Hh[i][t] * H[t][j] for t in range(n)) + (noise_var if i == j else 0) for j in range(n)] for i in range(n)]
    z = [sum(Hh[i][t] * y[t] for t in range(n)) for i in range(n)]
    return solve(A, z)  # @line L5
