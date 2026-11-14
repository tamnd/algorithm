# SPDX-License-Identifier: MIT
# Shared helper of the pe1 statistics pages of https://algorithm.tamnd.com/. The authors are listed in prov/.
"""Normal, chi-square, t and F distribution functions in the standard library.

The incomplete gamma and beta functions return a lower tail and an upper
tail, and each tail is computed directly where it is small, so an upper tail
such as chi2_sf(200, 3) does not come from 1 - cdf and does not cancel.
Quantiles use a safeguarded bisection on the CDF (lower half) or on the upper
tail (upper half); the bracket shrinks until floating point stops it, so the
probability error is that of the CDF, below 1e-12 for moderate parameters.
"""

import math
from statistics import NormalDist

_STD = NormalDist()
_EPS = 1e-16
_TINY = 1e-300
_MAXIT = 10000


def norm_cdf(x: float) -> float:
    """P(Z <= x) for a standard normal Z."""
    return 0.5 * math.erfc(-x / math.sqrt(2.0))


def norm_sf(x: float) -> float:
    """P(Z > x), computed with erfc, so it is accurate for large x."""
    return 0.5 * math.erfc(x / math.sqrt(2.0))


def norm_ppf(p: float) -> float:
    """The lower p-quantile z_p of the standard normal, 0 < p < 1."""
    if not 0.0 < p < 1.0:
        raise ValueError("p must be in (0, 1)")
    return _STD.inv_cdf(p)


def _gamma_tails(a: float, x: float) -> tuple[float, float]:
    """(P(a, x), Q(a, x)), the regularized lower and upper incomplete gamma."""
    if a <= 0.0 or x < 0.0:
        raise ValueError("need a > 0 and x >= 0")
    if x == 0.0:
        return 0.0, 1.0
    if math.isinf(x):
        return 1.0, 0.0
    front = math.exp(-x + a * math.log(x) - math.lgamma(a))
    if x < a + 1.0:
        # Series: P = front * sum_{j >= 0} x^j / (a (a + 1) ... (a + j)).
        ap, term = a, 1.0 / a
        total = term
        for _ in range(_MAXIT):
            ap += 1.0
            term *= x / ap
            total += term
            if abs(term) < abs(total) * _EPS:
                break
        p = front * total
        return p, 1.0 - p
    # Continued fraction for Q, modified Lentz.
    b = x + 1.0 - a
    c = 1.0 / _TINY
    d = 1.0 / b
    h = d
    for i in range(1, _MAXIT):
        an = -i * (i - a)
        b += 2.0
        d = an * d + b
        if abs(d) < _TINY:
            d = _TINY
        c = b + an / c
        if abs(c) < _TINY:
            c = _TINY
        d = 1.0 / d
        step = d * c
        h *= step
        if abs(step - 1.0) < _EPS:
            break
    q = front * h
    return 1.0 - q, q


def gamma_p(a: float, x: float) -> float:
    """Regularized lower incomplete gamma P(a, x)."""
    return _gamma_tails(a, x)[0]


def gamma_q(a: float, x: float) -> float:
    """Regularized upper incomplete gamma Q(a, x) = 1 - P(a, x)."""
    return _gamma_tails(a, x)[1]


def _beta_cf(a: float, b: float, x: float) -> float:
    """The continued fraction of I_x(a, b), modified Lentz."""
    qab, qap, qam = a + b, a + 1.0, a - 1.0
    c = 1.0
    d = 1.0 - qab * x / qap
    if abs(d) < _TINY:
        d = _TINY
    d = 1.0 / d
    h = d
    for m in range(1, _MAXIT):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d
        if abs(d) < _TINY:
            d = _TINY
        c = 1.0 + aa / c
        if abs(c) < _TINY:
            c = _TINY
        d = 1.0 / d
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d
        if abs(d) < _TINY:
            d = _TINY
        c = 1.0 + aa / c
        if abs(c) < _TINY:
            c = _TINY
        d = 1.0 / d
        step = d * c
        h *= step
        if abs(step - 1.0) < _EPS:
            break
    return h


def _beta_tails(a: float, b: float, x: float, y: float | None = None) -> tuple[float, float]:
    """(I_x(a, b), 1 - I_x(a, b)), each computed directly where it is small.

    y is 1 - x; pass it when it is known more accurately than 1 - x.
    """
    if a <= 0.0 or b <= 0.0:
        raise ValueError("need a > 0 and b > 0")
    if y is None:
        y = 1.0 - x
    if x <= 0.0:
        return 0.0, 1.0
    if y <= 0.0:
        return 1.0, 0.0
    front = math.exp(
        math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b)
        + a * math.log(x) + b * math.log(y)
    )
    if x < (a + 1.0) / (a + b + 2.0):
        low = front * _beta_cf(a, b, x) / a
        return low, 1.0 - low
    # Symmetry: I_x(a, b) = 1 - I_(1-x)(b, a).
    up = front * _beta_cf(b, a, y) / b
    return 1.0 - up, up


def beta_inc(a: float, b: float, x: float) -> float:
    """Regularized incomplete beta function I_x(a, b)."""
    return _beta_tails(a, b, x)[0]


def chi2_cdf(x: float, k: float) -> float:
    """P(X <= x) for X chi-square with k > 0 degrees of freedom."""
    return 0.0 if x <= 0.0 else gamma_p(k / 2.0, x / 2.0)


def chi2_sf(x: float, k: float) -> float:
    """P(X > x) for X chi-square with k degrees of freedom, without 1 - cdf."""
    return 1.0 if x <= 0.0 else gamma_q(k / 2.0, x / 2.0)


def t_sf(x: float, k: float) -> float:
    """P(T > x) for T Student t with k > 0 degrees of freedom."""
    if math.isfinite(x):
        s = k + x * x
        half = 0.5 * _beta_tails(k / 2.0, 0.5, k / s, x * x / s)[0]  # P(|T| > |x|) / 2
    else:
        half = 0.0
    return half if x >= 0.0 else 1.0 - half


def t_cdf(x: float, k: float) -> float:
    """P(T <= x) for T Student t with k degrees of freedom."""
    return t_sf(-x, k)


def f_cdf(x: float, k1: float, k2: float) -> float:
    """P(F <= x) for F with (k1, k2) degrees of freedom."""
    if x <= 0.0:
        return 0.0
    return _beta_tails(k2 / 2.0, k1 / 2.0, k2 / (k2 + k1 * x), k1 * x / (k2 + k1 * x))[1]


def f_sf(x: float, k1: float, k2: float) -> float:
    """P(F > x) = I_(k2 / (k2 + k1 x))(k2 / 2, k1 / 2)."""
    if x <= 0.0:
        return 1.0
    return _beta_tails(k2 / 2.0, k1 / 2.0, k2 / (k2 + k1 * x), k1 * x / (k2 + k1 * x))[0]


def _quantile(cdf, sf, p: float, lo: float, hi: float) -> float:
    """The x with cdf(x) = p, by bisection on cdf (p <= 1/2) or on sf (p > 1/2).

    lo must satisfy cdf(lo) <= p; hi is doubled until cdf(hi) >= p.
    """
    if not 0.0 < p < 1.0:
        raise ValueError("p must be in (0, 1)")
    if p <= 0.5:
        g = lambda x: cdf(x) - p  # increasing in x
    else:
        q = 1.0 - p
        g = lambda x: q - sf(x)  # increasing in x, and no cancellation in sf
    while g(hi) < 0.0:
        lo, hi = hi, 2.0 * hi if hi > 0.0 else 1.0
    for _ in range(400):
        mid = 0.5 * (lo + hi)
        if mid <= lo or mid >= hi:
            break
        if g(mid) < 0.0:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def chi2_ppf(p: float, k: float) -> float:
    """The lower p-quantile chi^2_(k, p)."""
    return _quantile(lambda x: chi2_cdf(x, k), lambda x: chi2_sf(x, k), p, 0.0, max(1.0, k))


def t_ppf(p: float, k: float) -> float:
    """The lower p-quantile t_(k, p)."""
    if p == 0.5:
        return 0.0
    if p < 0.5:
        return -t_ppf(1.0 - p, k)
    return _quantile(lambda x: t_cdf(x, k), lambda x: t_sf(x, k), p, 0.0, 1.0)


def f_ppf(p: float, k1: float, k2: float) -> float:
    """The lower p-quantile F_(k1, k2, p)."""
    return _quantile(lambda x: f_cdf(x, k1, k2), lambda x: f_sf(x, k1, k2), p, 0.0, 1.0)
