# SPDX-License-Identifier: MIT
# Shared helper of the natural-language-and-speech pages of https://algorithm.tamnd.com/. The authors are listed in prov/.

"""Small signal processing tools for the natural-language-and-speech pages.

A signal is a list of floats x[0], ..., x[L - 1], usually in [-1, 1]. A frame is
a list of floats. A spectrum is a list of floats or complex numbers.

The defaults of the area are fs = 16000 Hz, frames of 400 samples (25 ms), a hop
of 160 samples (10 ms), the symmetric Hamming window and an FFT length of 512.

The LPC sign convention is A(z) = 1 - sum_{k=1}^{p} a_k z^-k, so the prediction
of x[n] is sum_{k=1}^{p} a_k x[n - k].

This module holds no algorithm of any page of the area: no mel scale, no mel
filter bank, no feature extractor, no pre-emphasis and no zero-crossing rate.
The pages build those on top of it.
"""

import cmath
import math
from typing import List, Sequence, Tuple


def frames(x: Sequence[float], frame_len: int, hop: int) -> List[List[float]]:
    """Cut x into frames of frame_len samples, one every hop samples, with no padding.

    A signal of L >= frame_len samples gives 1 + (L - frame_len) // hop frames.
    A signal shorter than one frame gives no frame. The last samples that do not
    fill a frame are dropped.
    """
    if frame_len <= 0 or hop <= 0:
        raise ValueError("frame_len and hop must be positive")
    n = len(x)
    if n < frame_len:
        return []
    count = 1 + (n - frame_len) // hop
    return [list(x[i * hop : i * hop + frame_len]) for i in range(count)]


def hamming(n: int) -> List[float]:
    """The symmetric Hamming window w[i] = 0.54 - 0.46 cos(2 pi i / (n - 1)), i = 0 to n - 1."""
    if n <= 0:
        raise ValueError("the window length must be positive")
    if n == 1:
        return [1.0]
    return [0.54 - 0.46 * math.cos(2.0 * math.pi * i / (n - 1)) for i in range(n)]


def hann(n: int) -> List[float]:
    """The symmetric Hann window w[i] = 0.5 - 0.5 cos(2 pi i / (n - 1)), i = 0 to n - 1."""
    if n <= 0:
        raise ValueError("the window length must be positive")
    if n == 1:
        return [1.0]
    return [0.5 - 0.5 * math.cos(2.0 * math.pi * i / (n - 1)) for i in range(n)]


def fft(x: Sequence[complex]) -> List[complex]:
    """The DFT X[k] = sum_n x[n] exp(-2 pi i k n / N) by the iterative radix 2 FFT.

    The length N must be a power of 2. The cost is O(N log N) operations.
    """
    n = len(x)
    if n == 0 or n & (n - 1):
        raise ValueError("the FFT length must be a power of 2")
    a = [complex(v) for v in x]
    # bit reversal permutation
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
    while size <= n:
        half = size // 2
        w_step = cmath.exp(-2j * math.pi / size)
        for start in range(0, n, size):
            w = 1.0 + 0.0j
            for k in range(start, start + half):
                u = a[k]
                v = a[k + half] * w
                a[k] = u + v
                a[k + half] = u - v
                w *= w_step
        size *= 2
    return a


def power_spectrum(frame: Sequence[float], nfft: int) -> List[float]:
    """|X[k]|^2 for k = 0 to nfft / 2, where X is the DFT of the frame zero padded to nfft."""
    if len(frame) > nfft:
        raise ValueError("the frame is longer than the FFT length")
    spec = fft(list(frame) + [0.0] * (nfft - len(frame)))
    return [abs(spec[k]) ** 2 for k in range(nfft // 2 + 1)]


def dct2(x: Sequence[float], k: int) -> List[float]:
    """The first k coefficients of the orthonormal DCT-II of x.

    c[j] = s_j sum_{n=0}^{N-1} x[n] cos(pi j (2 n + 1) / (2 N)), with s_0 = sqrt(1 / N)
    and s_j = sqrt(2 / N) for j >= 1. The full transform (k = N) is an orthogonal matrix.
    """
    n = len(x)
    if n == 0:
        raise ValueError("empty input")
    if k < 0 or k > n:
        raise ValueError("k must be between 0 and len(x)")
    out = []
    for j in range(k):
        s = math.sqrt((1.0 if j == 0 else 2.0) / n)
        out.append(s * sum(x[i] * math.cos(math.pi * j * (2 * i + 1) / (2 * n)) for i in range(n)))
    return out


def autocorr(x: Sequence[float], max_lag: int) -> List[float]:
    """r[k] = sum_{n=0}^{L-1-k} x[n] x[n + k] for k = 0 to max_lag (no normalization)."""
    n = len(x)
    return [sum(x[i] * x[i + k] for i in range(n - k)) if k < n else 0.0 for k in range(max_lag + 1)]


def levinson(r: Sequence[float], p: int) -> Tuple[List[float], float]:
    """Solve the normal equations of linear prediction of order p by the Levinson-Durbin recursion.

    Returns (a, e): a = [a_1, ..., a_p] with A(z) = 1 - sum a_k z^-k, and e the
    prediction error of order p. Needs r[0] > 0 and len(r) > p. If the error
    reaches 0 before order p (a perfectly predictable signal), the remaining
    coefficients are 0.
    """
    if len(r) <= p:
        raise ValueError("need r[0] to r[p]")
    if r[0] <= 0:
        raise ValueError("r[0] must be positive")
    a = [0.0] * (p + 1)  # a[0] is unused
    e = float(r[0])
    for i in range(1, p + 1):
        if e <= 0.0:
            break
        acc = r[i] - sum(a[j] * r[i - j] for j in range(1, i))
        k = acc / e
        new = a[:]
        new[i] = k
        for j in range(1, i):
            new[j] = a[j] - k * a[i - j]
        a = new
        e *= 1.0 - k * k
    return a[1:], e


def sine(f: float, fs: float, n: int, amp: float = 1.0, phase: float = 0.0) -> List[float]:
    """x[i] = amp sin(2 pi f i / fs + phase) for i = 0 to n - 1."""
    return [amp * math.sin(2.0 * math.pi * f * i / fs + phase) for i in range(n)]


def pulse_train(f0: float, fs: float, n: int) -> List[float]:
    """Unit pulses at the samples round(j fs / f0), j = 0, 1, 2, ..., and 0 elsewhere, n samples."""
    if f0 <= 0:
        raise ValueError("f0 must be positive")
    x = [0.0] * n
    period = fs / f0
    j = 0
    while True:
        pos = int(math.floor(j * period + 0.5))
        if pos >= n:
            break
        x[pos] = 1.0
        j += 1
    return x


def white_noise(rng, n: int, sigma: float) -> List[float]:
    """n samples of Gaussian noise with mean 0 and standard deviation sigma, from rng (a random.Random)."""
    return [rng.gauss(0.0, sigma) for _ in range(n)]


def all_pole(x: Sequence[float], a: Sequence[float]) -> List[float]:
    """Filter x through 1 / A(z): y[n] = x[n] + sum_{k=1}^{p} a_k y[n - k], with zero initial state."""
    p = len(a)
    y: List[float] = []
    for i, v in enumerate(x):
        acc = float(v)
        for k in range(1, p + 1):
            if i - k < 0:
                break
            acc += a[k - 1] * y[i - k]
        y.append(acc)
    return y
