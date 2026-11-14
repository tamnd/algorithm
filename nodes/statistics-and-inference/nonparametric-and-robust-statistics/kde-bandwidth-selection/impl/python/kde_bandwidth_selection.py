# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kde-bandwidth-selection/. The authors are listed in prov/677AW6.jsonl.
"""Bandwidth selectors for a Gaussian-kernel density estimate in one dimension.

normal_reference, silverman, lscv_bandwidth (least squares cross-validation)
and dpi_bandwidth (two-stage direct plug-in, Sheather-Jones type).
"""

import math

SQRTPI = math.sqrt(math.pi)
SQRT2PI = math.sqrt(2 * math.pi)
RK = 1 / (2 * SQRTPI)  # R(K) for the Gaussian kernel; mu2(K) = 1


def phi(u):
    return math.exp(-0.5 * u * u) / SQRT2PI


def sample_sd(data):
    n = len(data)
    m = sum(data) / n
    return math.sqrt(sum((x - m) ** 2 for x in data) / (n - 1))


def quantile(data, p):
    """Linear interpolation between order statistics at position (n-1)p."""
    s = sorted(data)
    t = (len(s) - 1) * p
    j = int(math.floor(t))
    if j + 1 >= len(s):
        return s[-1]
    return s[j] + (t - j) * (s[j + 1] - s[j])


def iqr(data):
    return quantile(data, 0.75) - quantile(data, 0.25)


def normal_reference(data):
    """AMISE-optimal h if f were normal: (4/(3n))^(1/5) sigma, about 1.06 sigma n^(-1/5)."""
    return (4 / (3 * len(data))) ** 0.2 * sample_sd(data)


def silverman(data):
    """0.9 min(sigma, IQR/1.34) n^(-1/5)."""
    return 0.9 * min(sample_sd(data), iqr(data) / 1.34) * len(data) ** -0.2


def lscv(h, data):
    """LSCV(h) = R(f_h) - (2/n) sum_i f_{h,-i}(X_i), closed form for the Gaussian kernel.

    R(f_h) = n^-2 sum_{i,j} phi_{h sqrt 2}(X_i - X_j) and
    f_{h,-i}(X_i) = (n-1)^-1 sum_{j != i} phi_h(X_i - X_j). O(n^2) time.
    """
    n = len(data)
    s2 = math.sqrt(2) * h
    r = n / (s2 * SQRT2PI)  # the diagonal terms i = j
    loo = 0.0
    for i in range(n):
        for j in range(i + 1, n):
            d = data[i] - data[j]
            r += 2 * phi(d / s2) / s2
            loo += 2 * phi(d / h) / h
    return r / (n * n) - 2 * loo / (n * (n - 1))


def golden_min(f, a, b, tol=1e-10):
    g = (math.sqrt(5) - 1) / 2
    c, d = b - g * (b - a), a + g * (b - a)
    fc, fd = f(c), f(d)
    while b - a > tol * (abs(a) + abs(b)):
        if fc < fd:
            b, d, fd = d, c, fc
            c = b - g * (b - a)
            fc = f(c)
        else:
            a, c, fc = c, d, fd
            d = a + g * (b - a)
            fd = f(d)
    return (a + b) / 2


def lscv_bandwidth(data, grid=60, lo=0.05, hi=2.0):
    """Minimise LSCV over a log-spaced grid of h/sigma, then refine by golden section.

    LSCV can have several local minima; the grid picks the smallest grid value
    and the refinement stays between its two neighbours.
    """
    s = sample_sd(data)
    hs = [s * lo * (hi / lo) ** (k / (grid - 1)) for k in range(grid)]
    vals = [lscv(h, data) for h in hs]
    k = min(range(grid), key=vals.__getitem__)
    a, b = hs[max(k - 1, 0)], hs[min(k + 1, grid - 1)]
    return golden_min(lambda h: lscv(h, data), a, b)


def hermite(r, u):
    """Probabilists' Hermite polynomial He_r(u)."""
    h0, h1 = 1.0, u
    if r == 0:
        return h0
    for k in range(1, r):
        h0, h1 = h1, u * h1 - k * h0
    return h1


def psi_hat(r, g, data):
    """psi_r = integral f^(r) f, estimated by n^-2 sum_{i,j} phi_g^(r)(X_i - X_j), r even.

    phi_g^(r)(x) = g^(-r-1) He_r(x/g) phi(x/g), as (-1)^r He_r = He_r for even r.
    """
    n = len(data)
    tot = n * hermite(r, 0.0) * phi(0.0)
    for i in range(n):
        for j in range(i + 1, n):
            u = (data[i] - data[j]) / g
            tot += 2 * hermite(r, u) * phi(u)
    return tot / (n * n * g ** (r + 1))


def psi_normal(r, sigma):
    """psi_r for N(mu, sigma^2): (-1)^(r/2) r! / ((2 sigma)^(r+1) (r/2)! sqrt(pi))."""
    return (-1) ** (r // 2) * math.factorial(r) / ((2 * sigma) ** (r + 1) * math.factorial(r // 2) * SQRTPI)


def dpi_bandwidth(data):
    """Two-stage direct plug-in (Wand and Jones 1995, Section 3.6.1), Gaussian kernel.

    psi_8 from a normal scale, then psi_6 and psi_4 by kernel estimates with
    their own AMSE-optimal pilot bandwidths, then h = (R(K)/(psi_4 n))^(1/5).
    """
    n = len(data)
    s = min(sample_sd(data), iqr(data) / 1.349)
    psi8 = psi_normal(8, s)
    # g = (-2 L^(r)(0) / (mu2 psi_{r+2} n))^(1/(r+3)); phi^(6)(0) = -15 phi(0), phi^(4)(0) = 3 phi(0).
    g1 = (2 * 15 * phi(0.0) / (psi8 * n)) ** (1 / 9)
    psi6 = psi_hat(6, g1, data)
    g2 = (-2 * 3 * phi(0.0) / (psi6 * n)) ** (1 / 7)
    psi4 = psi_hat(4, g2, data)
    return (RK / (psi4 * n)) ** 0.2


def kde(x, data, h):
    return sum(phi((x - xi) / h) for xi in data) / (len(data) * h)


def exact_mise_mixture(h, n, weights, means, sds):
    """Exact MISE of the Gaussian-kernel KDE for a normal mixture (Marron and Wand 1992)."""
    k = len(weights)

    def omega(a):
        return [[phi((means[l] - means[m]) / math.sqrt(a * h * h + sds[l] ** 2 + sds[m] ** 2))
                 / math.sqrt(a * h * h + sds[l] ** 2 + sds[m] ** 2) for m in range(k)] for l in range(k)]

    o2, o1, o0 = omega(2), omega(1), omega(0)
    quad = sum(weights[l] * weights[m] * ((1 - 1 / n) * o2[l][m] - 2 * o1[l][m] + o0[l][m])
               for l in range(k) for m in range(k))
    return RK / (n * h) + quad
