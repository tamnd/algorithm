# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kernel-density-estimation/. The authors are listed in prov/29Z7ZM.jsonl.

import cmath
import math

SQRT2PI = math.sqrt(2 * math.pi)


def gaussian(u):
    return math.exp(-0.5 * u * u) / SQRT2PI


def epanechnikov(u):
    """(3/4)(1 - u^2) on [-1, 1]; works with floats and Fractions."""
    return 3 * (1 - u * u) / 4 if -1 <= u <= 1 else 0 * u


# R(K) = integral of K^2 and mu2(K) = integral of u^2 K, for the AMISE formula.
KERNEL_CONSTANTS = {
    "gaussian": (1 / (2 * math.sqrt(math.pi)), 1.0),
    "epanechnikov": (3 / 5, 1 / 5),
}


def kde(x, data, h, kernel=gaussian):
    """Direct estimate f(x) = (1/(n h)) sum K((x - X_i)/h). O(n) per point."""
    n = len(data)
    return sum(kernel((x - xi) / h) for xi in data) / (n * h)  # @line L1


def kde_grid_direct(grid, data, h, kernel=gaussian):
    """The direct estimate at every grid point. O(n m)."""
    return [kde(g, data, h, kernel) for g in grid]


def _fft(a, invert=False):
    """Iterative radix-2 FFT; len(a) must be a power of two."""
    n = len(a)
    a = list(a)
    j = 0
    for i in range(1, n):  # bit-reversal permutation
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j |= bit
        if i < j:
            a[i], a[j] = a[j], a[i]
    length = 2
    while length <= n:
        ang = (2 if invert else -2) * math.pi / length
        wl = cmath.exp(1j * ang)
        for i in range(0, n, length):
            w = 1
            for k in range(length // 2):
                u, v = a[i + k], a[i + k + length // 2] * w
                a[i + k], a[i + k + length // 2] = u + v, u - v
                w *= wl
        length <<= 1
    if invert:
        a = [v / n for v in a]
    return a


def linear_binning(data, lo, delta, m):
    """Grid counts c_0..c_{m-1}: each point splits its unit weight between
    the two nearest grid points, in proportion to closeness."""
    c = [0.0] * m
    for xi in data:
        t = (xi - lo) / delta
        j = int(math.floor(t))
        f = t - j
        if 0 <= j < m:
            c[j] += 1 - f
        if 0 <= j + 1 < m:
            c[j + 1] += f
    return c


def kde_binned_fft(data, h, lo, hi, m, kernel=gaussian, support=None):
    """Binned estimate on the grid lo + k delta, k = 0..m-1, delta = (hi-lo)/(m-1).

    Linear binning, then a discrete convolution of the counts with the kernel
    weights, done by FFT. O(n + m log m) time.
    """
    n = len(data)
    delta = (hi - lo) / (m - 1)
    c = linear_binning(data, lo, delta, m)  # @line L2
    reach = support if support is not None else (1.0 if kernel is epanechnikov else 8.0)
    L = min(m - 1, int(math.ceil(reach * h / delta)))
    kap = [kernel(l * delta / h) / (n * h) for l in range(-L, L + 1)]  # @line L3
    size = 1
    while size < m + 2 * L:
        size <<= 1
    A = _fft(c + [0.0] * (size - m))  # @line L4
    B = _fft(kap + [0.0] * (size - len(kap)))
    conv = _fft([u * v for u, v in zip(A, B)], invert=True)  # @line L5
    return [conv[k + L].real for k in range(m)]  # @line L6


def binned_direct(data, h, lo, hi, m, kernel=gaussian):
    """The same binned estimate by a direct O(m^2) convolution (for tests)."""
    n = len(data)
    delta = (hi - lo) / (m - 1)
    c = linear_binning(data, lo, delta, m)
    return [sum(c[j] * kernel((k - j) * delta / h) for j in range(m)) / (n * h)
            for k in range(m)]


def amise_bandwidth(n, r_f2, kernel="gaussian"):
    """h* = (R(K) / (mu2^2 R(f'') n))^(1/5)."""
    rk, mu2 = KERNEL_CONSTANTS[kernel]
    return (rk / (mu2 * mu2 * r_f2 * n)) ** 0.2


def amise(h, n, r_f2, kernel="gaussian"):
    """(1/4) h^4 mu2^2 R(f'') + R(K)/(n h)."""
    rk, mu2 = KERNEL_CONSTANTS[kernel]
    return 0.25 * h ** 4 * mu2 * mu2 * r_f2 + rk / (n * h)


def normal_density(x, s):
    return math.exp(-0.5 * (x / s) ** 2) / (s * SQRT2PI)


def exact_mise_gaussian(h, n, sigma):
    """Exact MISE of the Gaussian-kernel KDE for N(0, sigma^2) data."""
    c = 1 / (2 * math.sqrt(math.pi))
    s1 = math.sqrt(sigma * sigma + h * h)
    bias2 = c / s1 - 2 / (SQRT2PI * math.sqrt(s1 * s1 + sigma * sigma)) + c / sigma
    var = (c / h - c / s1) / n
    return bias2 + var
