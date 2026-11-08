# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/clenshaw-curtis-quadrature/. The authors are listed in prov/AP29J0.jsonl.

"""Clenshaw-Curtis quadrature on [a, b].

The n-point rule (N = n - 1) samples f at the Chebyshev extreme points
x_j = cos(j pi / N), j = 0..N, computes the Chebyshev coefficients of the
interpolant by a DCT-I (an FFT of length 2N of the even extension), and
integrates the interpolant exactly: the integral of T_k over [-1, 1] is
2 / (1 - k^2) for even k and 0 for odd k. Degree N, or N + 1 for even N.
The FFT is a radix-2 transform, with Bluestein's method for other lengths,
so the rule costs O(n log n) operations besides the n evaluations.
"""

import cmath
import math
from typing import Callable, List, Sequence, Tuple


def _fft_pow2(x: Sequence[complex]) -> List[complex]:
    """Iterative radix-2 FFT, X_k = sum_j x_j e^(-2 pi i j k / m), m a power of 2."""
    m = len(x)
    a = list(x)
    j = 0
    for i in range(1, m):  # bit-reversal permutation
        bit = m >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j |= bit
        if i < j:
            a[i], a[j] = a[j], a[i]
    size = 2
    while size <= m:
        half = size // 2
        tw = [cmath.exp(-2j * math.pi * k / size) for k in range(half)]
        for start in range(0, m, size):
            for k in range(half):
                u, v = a[start + k], a[start + k + half] * tw[k]
                a[start + k], a[start + k + half] = u + v, u - v
        size *= 2
    return a


def fft(x: Sequence[complex]) -> List[complex]:
    """DFT of any length in O(m log m): radix 2 directly, other lengths by Bluestein's chirp z-transform."""
    m = len(x)
    if m == 0:
        return []
    if m & (m - 1) == 0:
        return _fft_pow2(x)
    # chirp w_j = e^(-i pi j^2 / m); j^2 is reduced mod 2m so the angle stays small and accurate
    w = [cmath.exp(-1j * math.pi * ((j * j) % (2 * m)) / m) for j in range(m)]
    size = 1
    while size < 2 * m - 1:
        size *= 2
    u = [x[j] * w[j] for j in range(m)] + [0j] * (size - m)
    v = [0j] * size
    for j in range(m):
        v[j] = w[j].conjugate()
        if j:
            v[size - j] = w[j].conjugate()
    fu, fv = _fft_pow2(u), _fft_pow2(v)
    conv = _fft_pow2([(p * q).conjugate() for p, q in zip(fu, fv)])  # inverse FFT via conjugation
    return [w[k] * conv[k].conjugate() / size for k in range(m)]


def dct1(f: Sequence[float]) -> List[float]:
    """Chebyshev coefficients of the interpolant at x_j = cos(j pi / N): returns a_0..a_N with
    p = sum a_k T_k (the end coefficients already halved). Needs N = len(f) - 1 >= 1."""
    big_n = len(f) - 1
    g = list(f) + list(f[big_n - 1:0:-1])  # even extension, length 2N
    c = fft(g)
    a = [c[k].real / big_n for k in range(big_n + 1)]
    a[0] *= 0.5
    a[big_n] *= 0.5
    return a


def chebyshev_points(n: int) -> List[float]:
    """The n Chebyshev extreme points cos(j pi / (n - 1)), j = 0..n-1, decreasing, exactly symmetric."""
    big_n = n - 1
    # sin form: x_j = sin(pi (N - 2j) / (2N)) is exactly antisymmetric in floating point
    return [math.sin(math.pi * (big_n - 2 * j) / (2 * big_n)) for j in range(n)]


def clenshaw_curtis(f: Callable[[float], float], a: float, b: float, n: int = 33) -> float:
    """Integral of f over [a, b] by the n-point Clenshaw-Curtis rule (n >= 2). n evaluations, endpoints included."""
    # @line L1
    if n < 2:
        raise ValueError("need n >= 2")
    if a == b:
        return 0.0
    # @line L2
    big_n = n - 1
    c, h = 0.5 * (a + b), 0.5 * (b - a)
    fx = [f(c + h * x) for x in chebyshev_points(n)]
    # @line L3
    # @line L4
    # @line L5
    coef = dct1(fx)
    # @line L6
    q = math.fsum(coef[k] * 2.0 / (1.0 - k * k) for k in range(0, big_n + 1, 2))
    # @line L7
    return h * q


def clenshaw_curtis_weights(n: int) -> Tuple[List[float], List[float]]:
    """Nodes and weights on [-1, 1] in O(n log n): the weights are a DCT-I of the moments.

    The rule is sum_k a_k m_k with a_k = (2 / N) e_k sum_j g_j f_j cos(j k pi / N), where e and g
    halve the end terms, so w_j = (2 / N) g_j sum_k e_k m_k cos(j k pi / N), m_k = 2 / (1 - k^2) for even k.
    """
    if n < 2:
        raise ValueError("need n >= 2")
    big_n = n - 1
    m = [2.0 / (1.0 - k * k) if k % 2 == 0 else 0.0 for k in range(big_n + 1)]
    g = m + m[big_n - 1:0:-1]  # its FFT is 2 sum_k e_k m_k cos(j k pi / N), e_k = 1/2 at k = 0, N
    c = fft(g)
    w = [c[j].real / big_n for j in range(big_n + 1)]
    w[0] *= 0.5
    w[big_n] *= 0.5
    w = [0.5 * (w[j] + w[big_n - j]) for j in range(n)]  # exact symmetry
    return chebyshev_points(n), w


def clenshaw_curtis_weights_direct(n: int) -> List[float]:
    """The explicit O(n^2) weight formula w_j = (c_j / N)(1 - sum_l b_l cos(2 l j pi / N) / (4 l^2 - 1))."""
    big_n = n - 1
    w = []
    for j in range(n):
        s = 0.0
        for l in range(1, big_n // 2 + 1):
            b = 1.0 if 2 * l == big_n else 2.0
            s += b * math.cos(2 * l * j * math.pi / big_n) / (4 * l * l - 1)
        cj = 1.0 if j in (0, big_n) else 2.0
        w.append(cj / big_n * (1.0 - s))
    return w


def integrate(f: Callable[[float], float], a: float, b: float, tol: float = 1e-12,
              max_n: int = 2 ** 16 + 1) -> Tuple[float, float, int, str]:
    """Nested doubling: n = 9, 17, 33, ... reusing every old value, until |Q_2N - Q_N| <= tol.

    Returns (value, |Q_2N - Q_N|, evaluations, status) with status "ok" or "limit".
    The difference is an error estimate for Q_N, used here for Q_2N: a heuristic.
    """
    if a == b:
        return 0.0, 0.0, 0, "ok"
    c, h = 0.5 * (a + b), 0.5 * (b - a)
    big_n = 8
    fx = [f(c + h * x) for x in chebyshev_points(big_n + 1)]
    evals = big_n + 1

    def rule(vals):
        coef = dct1(vals)
        return h * math.fsum(coef[k] * 2.0 / (1.0 - k * k) for k in range(0, len(vals), 2))

    q_old = rule(fx)
    while True:
        if 2 * big_n + 1 > max_n:
            return q_old, math.inf, evals, "limit"
        new_n = 2 * big_n
        pts = chebyshev_points(new_n + 1)
        merged = [0.0] * (new_n + 1)
        merged[0::2] = fx  # node j of the N-rule is node 2j of the 2N-rule
        for j in range(1, new_n, 2):
            merged[j] = f(c + h * pts[j])
        evals += big_n
        fx, big_n = merged, new_n
        q_new = rule(fx)
        diff = abs(q_new - q_old)
        if diff <= tol:
            return q_new, diff, evals, "ok"
        q_old = q_new
