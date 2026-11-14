# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/whittle-likelihood/. The authors are listed in prov/F9TJBR.jsonl.

"""The Whittle likelihood of a stationary series and the Whittle estimate of an ARMA(p, q) model.

Conventions:
    omega_j = 2 pi j / n,  j = 0, ..., n - 1 (the Fourier frequencies)
    I(omega_j) = |sum_(t=1..n) X_t exp(-i t omega_j)|^2 / (2 pi n)   (the periodogram)
    f(lambda) = (1 / (2 pi)) sum_h gamma(h) exp(-i h lambda)          (the spectral density)
    -2 log L_W = N log(2 pi) + sum_j [log(2 pi f(omega_j)) + I(omega_j) / f(omega_j)]
The sum runs over N frequencies: all n of them for a known zero mean, or j = 1..n-1 after
the sample mean is removed (the periodogram at j = 0 is then 0).
"""

from __future__ import annotations

import cmath
import math
from typing import Callable, Sequence


def fft(x: Sequence[complex]) -> list[complex]:
    """The DFT y_k = sum_t x_t exp(-2 pi i t k / n), t = 0..n-1.

    Radix-2 splitting while n is even, and the direct O(m^2) sum on an odd factor m, so a
    power of two costs O(n log n).
    """
    n = len(x)
    if n == 0:
        return []
    if n % 2 == 1:
        w = [cmath.exp(-2j * math.pi * k / n) for k in range(n)]
        return [sum(x[t] * w[(t * k) % n] for t in range(n)) for k in range(n)]
    even = fft(x[0::2])
    odd = fft(x[1::2])
    half = n // 2
    out = [0j] * n
    for k in range(half):
        tw = cmath.exp(-2j * math.pi * k / n) * odd[k]
        out[k] = even[k] + tw
        out[k + half] = even[k] - tw
    return out


def periodogram(x: Sequence[float]) -> list[float]:
    """I(omega_j) for j = 0..n-1 with the 1 / (2 pi n) scaling."""
    n = len(x)
    d = fft([complex(v) for v in x])
    return [abs(z) ** 2 / (2 * math.pi * n) for z in d]  # @line L1


def arma_spectral_density(phi: Sequence[float], theta: Sequence[float], sigma2: float,
                          lam: float) -> float:
    """f(lam) = sigma2 / (2 pi) |theta(e^(-i lam))|^2 / |phi(e^(-i lam))|^2."""
    z = cmath.exp(-1j * lam)
    num = 1 + sum(t * z ** (k + 1) for k, t in enumerate(theta))
    den = 1 - sum(a * z ** (k + 1) for k, a in enumerate(phi))
    return sigma2 / (2 * math.pi) * abs(num) ** 2 / abs(den) ** 2


def whittle_neg2loglik(x: Sequence[float], f: Callable[[float], float],
                       demean: bool = False) -> float:
    """-2 log L_W for the spectral density f. With demean, the mean is removed and j = 0 is dropped."""
    n = len(x)
    if demean:
        m = math.fsum(x) / n
        x = [v - m for v in x]
    per = periodogram(x)
    js = range(1, n) if demean else range(n)
    terms = []
    for j in js:
        fj = f(2 * math.pi * j / n)  # @line L2
        terms.append(math.log(2 * math.pi * fj) + per[j] / fj)  # @line L3
    return len(terms) * math.log(2 * math.pi) + math.fsum(terms)  # @line L4


def pacf_to_ar(r: Sequence[float]) -> list[float]:
    """Step-up (Durbin-Levinson) map from partial autocorrelations in (-1, 1) to a causal AR."""
    a: list[float] = []
    for k, rk in enumerate(r, start=1):
        a = [a[j] - rk * a[k - 2 - j] for j in range(k - 1)] + [rk]
    return a


def _unpack(u: Sequence[float], p: int, q: int) -> tuple[list[float], list[float]]:
    phi = pacf_to_ar([math.tanh(v) for v in u[:p]])
    theta = [-c for c in pacf_to_ar([math.tanh(v) for v in u[p:p + q]])]
    return phi, theta


def profiled_objective(per: Sequence[float], n: int, phi: Sequence[float],
                       theta: Sequence[float]) -> tuple[float, float]:
    """(-2 log L_W with sigma^2 profiled out, sigma2_hat), over j = 1..n-1."""
    g = [2 * math.pi * arma_spectral_density(phi, theta, 1.0, 2 * math.pi * j / n)
         for j in range(1, n)]
    big_n = n - 1
    sigma2 = 2 * math.pi * math.fsum(per[j] / g[j - 1] for j in range(1, n)) / big_n
    value = big_n * math.log(2 * math.pi) + big_n * math.log(sigma2) + \
        math.fsum(math.log(gj) for gj in g) + big_n
    return value, sigma2


def nelder_mead(fun: Callable[[list[float]], float], x0: Sequence[float], step: float = 0.3,
                tol: float = 1e-10, max_iter: int = 2000) -> list[float]:
    """Minimize fun by the Nelder-Mead simplex method with the standard coefficients."""
    d = len(x0)
    pts = [list(x0)] + [[x0[i] + (step if i == k else 0.0) for i in range(d)] for k in range(d)]
    vals = [fun(p) for p in pts]
    for _ in range(max_iter):
        order = sorted(range(d + 1), key=vals.__getitem__)
        pts = [pts[i] for i in order]
        vals = [vals[i] for i in order]
        if abs(vals[-1] - vals[0]) <= tol * (1 + abs(vals[0])):
            break
        cen = [math.fsum(p[i] for p in pts[:-1]) / d for i in range(d)]
        xr = [cen[i] + (cen[i] - pts[-1][i]) for i in range(d)]
        fr = fun(xr)
        if fr < vals[0]:
            xe = [cen[i] + 2 * (cen[i] - pts[-1][i]) for i in range(d)]
            fe = fun(xe)
            pts[-1], vals[-1] = (xe, fe) if fe < fr else (xr, fr)
        elif fr < vals[-2]:
            pts[-1], vals[-1] = xr, fr
        else:
            xc = [cen[i] + 0.5 * (pts[-1][i] - cen[i]) for i in range(d)]
            fc = fun(xc)
            if fc < vals[-1]:
                pts[-1], vals[-1] = xc, fc
            else:
                for k in range(1, d + 1):
                    pts[k] = [pts[0][i] + 0.5 * (pts[k][i] - pts[0][i]) for i in range(d)]
                    vals[k] = fun(pts[k])
    best = min(range(d + 1), key=vals.__getitem__)
    return pts[best]


def whittle_fit_arma(x: Sequence[float], p: int, q: int) -> tuple[list[float], list[float], float]:
    """Whittle estimate (phi_hat, theta_hat, sigma2_hat) of a causal invertible ARMA(p, q).

    The mean is removed, the periodogram is computed once by the FFT, and the profiled
    objective is minimized over unconstrained u with phi and theta built from tanh(u).
    """
    n = len(x)
    m = math.fsum(x) / n
    per = periodogram([v - m for v in x])
    if p + q == 0:
        return [], [], profiled_objective(per, n, [], [])[1]
    u = nelder_mead(lambda w: profiled_objective(per, n, *_unpack(w, p, q))[0], [0.0] * (p + q))  # @line L5
    phi, theta = _unpack(u, p, q)
    return phi, theta, profiled_objective(per, n, phi, theta)[1]
