# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fejer-quadrature/. The authors are listed in prov/MK9GM6.jsonl.

"""Fejér's first and second quadrature rules on [a, b].

Both are interpolatory rules on Chebyshev-type points that exclude the endpoints:
  first rule:  the n Chebyshev zeros     x_j = cos((j + 1/2) pi / n), j = 0..n-1;
  second rule: the n interior extrema    x_j = cos(j pi / (n + 1)),   j = 1..n.
The first rule finds the Chebyshev coefficients of the interpolant with a DCT-II and
uses the integral 2 / (1 - k^2) of T_k for even k. The second rule writes
p(cos t) sin t as a sine polynomial, found with a DST-I, and integrates sin(k t)
over [0, pi]. Both transforms are FFTs of length 2n or 2(n + 1), so a rule costs
n evaluations and O(n log n) operations. Degree n - 1, or n for odd n.
"""

import cmath
import math
from typing import Callable, List, Sequence, Tuple


def _fft_pow2(x: Sequence[complex]) -> List[complex]:
    """Iterative radix-2 FFT, X_k = sum_j x_j e^(-2 pi i j k / m), m a power of 2."""
    m = len(x)
    a = list(x)
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
        half = size // 2
        tw = [cmath.exp(-2j * math.pi * k / size) for k in range(half)]
        for start in range(0, m, size):
            for k in range(half):
                u, v = a[start + k], a[start + k + half] * tw[k]
                a[start + k], a[start + k + half] = u + v, u - v
        size *= 2
    return a


def fft(x: Sequence[complex]) -> List[complex]:
    """DFT of any length in O(m log m): radix 2, or Bluestein's chirp z-transform for other lengths."""
    m = len(x)
    if m == 0:
        return []
    if m & (m - 1) == 0:
        return _fft_pow2(x)
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
    conv = _fft_pow2([(p * q).conjugate() for p, q in zip(fu, fv)])
    return [w[k] * conv[k].conjugate() / size for k in range(m)]


def fejer_points(n: int, kind: int = 2) -> List[float]:
    """The n nodes of the rule on [-1, 1], decreasing, exactly symmetric (sine form of the cosines)."""
    if kind == 1:
        return [math.sin(math.pi * (n - 1 - 2 * j) / (2 * n)) for j in range(n)]
    big_n = n + 1
    return [math.sin(math.pi * (big_n - 2 * j) / (2 * big_n)) for j in range(1, n + 1)]


def fejer(f: Callable[[float], float], a: float, b: float, n: int = 32, kind: int = 2) -> float:
    """Integral of f over [a, b] by Fejér's first (kind=1) or second (kind=2) rule with n >= 1 nodes.

    n evaluations, all in the open interval (a, b).
    """
    # @line L1
    if n < 1 or kind not in (1, 2):
        raise ValueError("need n >= 1 and kind 1 or 2")
    if a == b:
        return 0.0
    c, h = 0.5 * (a + b), 0.5 * (b - a)
    # @line L2
    xs = fejer_points(n, kind)
    # @line L3
    fx = [f(c + h * x) for x in xs]
    if kind == 1:
        # @line L4
        # sum_j f_j cos(k (j + 1/2) pi / n) = (1/2) e^(-i pi k / (2n)) Y_k, Y the FFT of (f, reversed f)
        y = fft(fx + fx[::-1])
        coef = [(cmath.exp(-1j * math.pi * k / (2 * n)) * y[k]).real / n for k in range(n)]
        coef[0] *= 0.5
    else:
        # @line L5
        big_n = n + 1
        s = [fx[j - 1] * math.sin(j * math.pi / big_n) for j in range(1, big_n)]
        g = [0.0] + s + [0.0] + [-t for t in reversed(s)]  # odd extension, length 2N
        y = fft(g)  # Y_k = -2i sum_j s_j sin(j k pi / N)
        beta = [-y[k].imag / big_n for k in range(big_n)]
    # @line L6
    if kind == 1:
        q = math.fsum(coef[k] * 2.0 / (1.0 - k * k) for k in range(0, n, 2))
    else:
        q = math.fsum(beta[k] * 2.0 / k for k in range(1, big_n, 2))
    # @line L7
    return h * q


def fejer1_weights(n: int) -> List[float]:
    """Explicit weights of the first rule, in the order of fejer_points(n, 1). O(n^2)."""
    w = []
    for j in range(n):
        t = (j + 0.5) * math.pi / n
        s = sum(math.cos(2 * l * t) / (4 * l * l - 1) for l in range(1, n // 2 + 1))
        w.append(2.0 / n * (1.0 - 2.0 * s))
    return w


def fejer2_weights(n: int) -> List[float]:
    """Explicit weights of the second rule, in the order of fejer_points(n, 2). O(n^2)."""
    big_n = n + 1
    w = []
    for j in range(1, n + 1):
        t = j * math.pi / big_n
        s = sum(math.sin((2 * l - 1) * t) / (2 * l - 1) for l in range(1, big_n // 2 + 1))
        w.append(4.0 * math.sin(t) / big_n * s)
    return w


def integrate(f: Callable[[float], float], a: float, b: float, tol: float = 1e-10,
              max_n: int = 2 ** 16 - 1) -> Tuple[float, float, int, str]:
    """Nested doubling with the second rule: n = 7, 15, 31, ... (N = n + 1 doubles), reusing all values.

    Returns (value, |Q_new - Q_old|, evaluations, status), status "ok" or "limit". Never evaluates
    f at a or b. The stopping test is a heuristic.
    """
    if a == b:
        return 0.0, 0.0, 0, "ok"
    c, h = 0.5 * (a + b), 0.5 * (b - a)
    n = 7
    fx = [f(c + h * x) for x in fejer_points(n)]
    evals = n

    def rule(vals):
        big_n = len(vals) + 1
        s = [vals[j - 1] * math.sin(j * math.pi / big_n) for j in range(1, big_n)]
        y = fft([0.0] + s + [0.0] + [-t for t in reversed(s)])
        return h * math.fsum(-y[k].imag / big_n * 2.0 / k for k in range(1, big_n, 2))

    q_old = rule(fx)
    while True:
        new_n = 2 * n + 1
        if new_n > max_n:
            return q_old, math.inf, evals, "limit"
        pts = fejer_points(new_n)
        merged = [0.0] * new_n
        merged[1::2] = fx  # interior node j of the N-rule is node 2j of the 2N-rule
        for i in range(0, new_n, 2):
            merged[i] = f(c + h * pts[i])
        evals += new_n - n
        fx, n = merged, new_n
        q_new = rule(fx)
        diff = abs(q_new - q_old)
        if diff <= tol:
            return q_new, diff, evals, "ok"
        q_old = q_new
