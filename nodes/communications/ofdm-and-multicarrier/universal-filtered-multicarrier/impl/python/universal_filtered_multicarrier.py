# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/universal-filtered-multicarrier/. The authors are listed in prov/45M7YX.jsonl.

"""UFMC: OFDM in subbands, each subband filtered by its own short filter.

The N subcarriers are grouped into subbands. Subband i is turned into time
by an N-point inverse DFT, convolved with a filter f_i of length L, and the
subbands are added. A block has N + L - 1 samples and no cyclic prefix: the
filter ramps take its place. The filters are one Dolph-Chebyshev window
shifted to the center of each subband.

The receiver pads a block to 2N samples and takes a 2N-point DFT. Its even
bins are Y[2k] = H(2k) F_i(2k) X[k], where F_i and H are the 2N-point DFTs of
the filter and the channel, so dividing by them recovers X[k] exactly when
the received block fits in 2N samples. Bins are signed: -N/2 <= k < N/2,
stored at index k mod N.
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


def chebyshev(m: int, x: float) -> float:
    """The Chebyshev polynomial T_m(x) for any real x."""
    if abs(x) <= 1:
        return math.cos(m * math.acos(x))
    if x > 1:
        return math.cosh(m * math.acosh(x))
    return (-1) ** m * math.cosh(m * math.acosh(-x))


def dolph_chebyshev(length: int, attenuation_db: float) -> list[float]:
    """The Dolph-Chebyshev window of odd length with the given sidelobe attenuation, sum 1."""
    if length < 3 or length % 2 == 0:
        raise ValueError("length must be odd and at least 3")
    r = 10 ** (attenuation_db / 20)
    x0 = math.cosh(math.acosh(r) / (length - 1))
    c = (length - 1) / 2
    w = []
    for n in range(length):
        s = r + 2 * sum(chebyshev(length - 1, x0 * math.cos(math.pi * k / length)) * math.cos(2 * math.pi * k * (n - c) / length) for k in range(1, (length + 1) // 2))
        w.append(s)
    total = sum(w)
    return [v / total for v in w]


def subband_filters(bands: Sequence[Sequence[int]], n: int, window: Sequence[float]) -> list[list[complex]]:
    """The window shifted to the center of each subband (bins on the N-point grid)."""
    c = (len(window) - 1) / 2
    out = []
    for band in bands:
        f0 = sum(band) / len(band)
        out.append([w * cmath.exp(2j * math.pi * f0 * (t - c) / n) for t, w in enumerate(window)])
    return out


def transmit(X: Sequence[complex], bands: Sequence[Sequence[int]], filters: Sequence[Sequence[complex]]) -> list[complex]:
    """One UFMC block of N + L - 1 samples. X has N bins; only the bins in bands are sent."""
    n = len(X)
    length = len(filters[0])
    x = [0j] * (n + length - 1)
    for band, f in zip(bands, filters):
        Xi = [0j] * n
        for k in band:
            Xi[k % n] = X[k % n]
        xi = [v / math.sqrt(n) for v in fft(Xi, inverse=True)]  # @line L1
        for t, a in enumerate(xi):  # @line L2
            for l, b in enumerate(f):
                x[t + l] += a * b
    return x  # @line L3


def receive(y: Sequence[complex], n: int, bands: Sequence[Sequence[int]], filters: Sequence[Sequence[complex]], h: Sequence[complex] = (1,)) -> list[complex]:
    """The N bins of one block from at most 2N received samples, divided by filter and channel."""
    if len(y) > 2 * n:
        raise ValueError("the block does not fit in 2N samples")
    Y = fft(list(y) + [0j] * (2 * n - len(y)))  # @line L4
    H = fft(list(h) + [0j] * (2 * n - len(h)))
    X = [0j] * n
    for band, f in zip(bands, filters):
        F = fft(list(f) + [0j] * (2 * n - len(f)))
        for k in band:
            i = (2 * k) % (2 * n)
            X[k % n] = Y[i] / (math.sqrt(n) * F[i] * H[i])  # @line L5
    return X


def ofdm_block(X: Sequence[complex], bins: Sequence[int], cp: int) -> list[complex]:
    """A CP-OFDM block on the same bins, for comparison."""
    n = len(X)
    Z = [0j] * n
    for k in bins:
        Z[k % n] = X[k % n]
    x = [v / math.sqrt(n) for v in fft(Z, inverse=True)]
    return x[n - cp:] + x


def channel(x: Sequence[complex], h: Sequence[complex]) -> list[complex]:
    """Full linear convolution with h."""
    out = [0j] * (len(x) + len(h) - 1)
    for i, a in enumerate(x):
        for k, b in enumerate(h):
            out[i + k] += a * b
    return out


def spectrum(x: Sequence[complex], size: int) -> list[float]:
    """|DFT|^2 of x padded to size, on a grid of size / N points per subcarrier."""
    return [abs(v) ** 2 for v in fft(list(x) + [0j] * (size - len(x)))]
