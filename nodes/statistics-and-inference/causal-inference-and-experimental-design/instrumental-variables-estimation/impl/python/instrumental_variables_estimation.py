# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/instrumental-variables-estimation/. The authors are listed in prov/CM6TM9.jsonl.

"""Instrumental variables with one treatment d and one instrument z.

The structural model is y = alpha + beta d + e with z uncorrelated with e. The IV
estimate is the ratio of two regression slopes on z (the reduced form over the first
stage), beta = Cov(z, y) / Cov(z, d); for a binary z it is the Wald ratio.

The Anderson-Rubin (AR) test of beta = b0 regresses y - b0 d on (1, z) and uses the
F statistic of the slope. With normal errors independent of z it is exactly F(1, n - 2)
under the null, whatever the strength of the instrument. Inverting it gives a
confidence set that is an interval, the complement of an open interval, a half-line,
or the whole line.

The point estimates and the statistics are exact for Fraction inputs; the critical
values and p-values come from stdist.
"""

import math
from collections.abc import Sequence
from functools import lru_cache
from typing import NamedTuple

from stdist import f_ppf, f_sf, t_ppf


class Moments(NamedTuple):
    n: int
    szz: object
    szd: object
    szy: object
    sdd: object
    syd: object
    syy: object


class IVResult(NamedTuple):
    beta: object  # the IV estimate
    alpha: object  # the intercept
    se: float  # the homoskedastic standard error
    first_stage_f: object  # F statistic of z in the regression of d on (1, z)
    ar_set: tuple  # the AR confidence set, see ar_set()


def moments(y: Sequence, d: Sequence, z: Sequence) -> Moments:
    """Centred sums of squares and cross products (not divided by n)."""
    n = len(y)
    if len(d) != n or len(z) != n:
        raise ValueError("y, d and z need the same length")
    if n < 3:
        raise ValueError("need at least 3 units")
    my, md, mz = sum(y) / n, sum(d) / n, sum(z) / n
    cy = [v - my for v in y]
    cd = [v - md for v in d]
    cz = [v - mz for v in z]

    def dot(a, b):
        return sum(p * q for p, q in zip(a, b))

    return Moments(n, dot(cz, cz), dot(cz, cd), dot(cz, cy), dot(cd, cd), dot(cy, cd), dot(cy, cy))


def wald_estimate(y: Sequence, d: Sequence, z: Sequence) -> object:
    """(mean y | z = 1 - mean y | z = 0) / (mean d | z = 1 - mean d | z = 0) for a 0/1 instrument."""
    g1 = [i for i, v in enumerate(z) if v == 1]
    g0 = [i for i, v in enumerate(z) if v == 0]
    if not g1 or not g0 or len(g1) + len(g0) != len(z):
        raise ValueError("z must be 0/1 with both values present")
    dy = sum(y[i] for i in g1) / len(g1) - sum(y[i] for i in g0) / len(g0)
    dd = sum(d[i] for i in g1) / len(g1) - sum(d[i] for i in g0) / len(g0)
    if dd == 0:
        raise ZeroDivisionError("the instrument does not move the treatment in this sample")
    return dy / dd


def ar_statistic(m: Moments, b0) -> object:
    """F statistic of the slope of z in the regression of y - b0 d on (1, z)."""
    c = m.szy - b0 * m.szd
    sww = m.syy - 2 * b0 * m.syd + b0 * b0 * m.sdd
    resid = m.szz * sww - c * c  # szz times the residual sum of squares
    if resid == 0:
        return math.inf
    return (m.n - 2) * c * c / resid


@lru_cache(maxsize=256)
def _f_crit(alpha: float, df: int) -> float:
    return f_ppf(1 - alpha, 1, df)


def ar_set(m: Moments, alpha: float = 0.05) -> tuple:
    """{b0 : AR(b0) <= F_(1, n-2, 1-alpha)} as one of
    ("interval", lo, hi), ("complement", lo, hi) meaning (-inf, lo] and [hi, inf),
    ("ray_up", lo) meaning [lo, inf), ("ray_down", hi) meaning (-inf, hi], ("line",), ("empty",)."""
    q = _f_crit(alpha, m.n - 2)
    kappa = q / (m.n - 2 + q)
    szz, szd, szy, sdd, syd, syy = (float(v) for v in m[1:])
    # AR(b) <= q  <=>  (szy - b szd)^2 - kappa szz (syy - 2 b syd + b^2 sdd) <= 0
    a = szd * szd - kappa * szz * sdd
    b = -2 * szy * szd + 2 * kappa * szz * syd
    c = szy * szy - kappa * szz * syy
    if a == 0:
        if b > 0:
            return ("ray_down", -c / b)
        if b < 0:
            return ("ray_up", -c / b)
        return ("line",) if c <= 0 else ("empty",)
    disc = b * b - 4 * a * c
    if a > 0:
        if disc < 0:
            return ("empty",)
        r = math.sqrt(disc)
        lo, hi = sorted(((-b - r) / (2 * a), (-b + r) / (2 * a)))
        return ("interval", lo, hi)
    if disc <= 0:
        return ("line",)
    r = math.sqrt(disc)
    lo, hi = sorted(((-b - r) / (2 * a), (-b + r) / (2 * a)))
    return ("complement", lo, hi)


def in_set(s: tuple, v: float) -> bool:
    kind = s[0]
    if kind == "interval":
        return s[1] <= v <= s[2]
    if kind == "complement":
        return v <= s[1] or v >= s[2]
    if kind == "ray_up":
        return v >= s[1]
    if kind == "ray_down":
        return v <= s[1]
    return kind == "line"


def iv_analysis(y: Sequence, d: Sequence, z: Sequence, alpha: float = 0.05) -> IVResult:
    """The IV estimate, its standard error, the first-stage F and the AR set. Cost: Theta(n)."""
    m = moments(y, d, z)
    if m.szz == 0:
        raise ValueError("the instrument is constant")
    f1 = (m.n - 2) * m.szd * m.szd / (m.szz * m.sdd - m.szd * m.szd) if m.szz * m.sdd != m.szd * m.szd else math.inf  # @line L1
    rf = m.szy / m.szz  # @line L2
    if m.szd == 0:
        raise ZeroDivisionError("the instrument is uncorrelated with the treatment in this sample")
    beta = rf / (m.szd / m.szz)  # @line L3
    n = m.n
    alpha_hat = sum(y) / n - beta * sum(d) / n
    rss = m.syy - 2 * beta * m.syd + beta * beta * m.sdd  # @line L4
    se = math.sqrt(float(rss / (n - 2)) * float(m.szz)) / abs(float(m.szd))
    s = ar_set(m, alpha)  # @line L5
    return IVResult(beta, alpha_hat, se, f1, s)  # @line L6


def wald_interval(res: IVResult, n: int, alpha: float = 0.05) -> tuple[float, float]:
    """beta +- t_(n-2, 1-alpha/2) se, valid only with a strong instrument."""
    t = t_ppf(1 - alpha / 2, n - 2)
    return float(res.beta) - t * res.se, float(res.beta) + t * res.se


def ar_pvalue(m: Moments, b0) -> float:
    return f_sf(float(ar_statistic(m, b0)), 1, m.n - 2)
