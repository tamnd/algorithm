# SPDX-License-Identifier: MIT
# Shared helper of the ci3 statistics pages of https://algorithm.tamnd.com/. The authors are listed in prov/.
"""The studentized range distribution in the standard library.

Q = R / S, where R is the range of k iid N(0, 1) variables and nu S^2 is an
independent chi-square with nu degrees of freedom (nu = inf means S = 1).

    P(R > w) = k * integral phi(z) (A(z)^(k-1) - (A(z) - A(z + w))^(k-1)) dz,
    A(z) = P(Z > z),

because the minimum of the k variables has density k phi(z) A(z)^(k-1), and
given the minimum z the other k - 1 lie in (z, z + w] with probability
((A(z) - A(z + w)) / A(z))^(k-1). The difference of powers is written as
-A^(k-1) expm1((k-1) log1p(-A(z + w) / A(z))), so a small tail keeps its
digits. Then P(Q > q) = integral g(s) P(R > q s) ds, where g is the density of
S. Both integrals use composite Gauss-Legendre rules; the outer range of s
holds all but 1e-30 of the mass of S. The tail is accurate to about 1e-11
absolutely for 2 <= k <= 100 and nu >= 1 (the tests compare it with the exact
k = 2 law and with Monte Carlo).
"""

import math

from stdist import chi2_cdf, chi2_sf, norm_sf

_SQRT_2PI = math.sqrt(2.0 * math.pi)


def _legendre_rule(m: int) -> list[tuple[float, float]]:
    """Nodes and weights of the m-point Gauss-Legendre rule on [-1, 1], by Newton's method."""
    rule = []
    for i in range(1, m + 1):
        x = math.cos(math.pi * (i - 0.25) / (m + 0.5))
        for _ in range(100):
            p0, p1 = 1.0, x
            for j in range(2, m + 1):
                p0, p1 = p1, ((2 * j - 1) * x * p1 - (j - 1) * p0) / j
            dp = m * (x * p1 - p0) / (x * x - 1.0)
            dx = p1 / dp
            x -= dx
            if abs(dx) < 1e-16:
                break
        p0, p1 = 1.0, x
        for j in range(2, m + 1):
            p0, p1 = p1, ((2 * j - 1) * x * p1 - (j - 1) * p0) / j
        dp = m * (x * p1 - p0) / (x * x - 1.0)
        rule.append((x, 2.0 / ((1.0 - x * x) * dp * dp)))
    return rule


_RULE = _legendre_rule(10)


def _panels(lo: float, hi: float, count: int) -> list[tuple[float, float]]:
    """Nodes and weights of the composite rule with count equal panels on [lo, hi]."""
    h = (hi - lo) / count
    out = []
    for p in range(count):
        mid = lo + (p + 0.5) * h
        out += [(mid + 0.5 * h * x, 0.5 * h * w) for x, w in _RULE]
    return out


Z_PANELS = 17  # panels of the inner rule on [-8.5, 8.5]
S_PANELS = 40  # panels of the outer rule
# Inner nodes z with the weight times phi(z), and A(z), computed once.
_Z_NODES = [(z, wt * math.exp(-0.5 * z * z) / _SQRT_2PI, norm_sf(z))
            for z, wt in _panels(-8.5, 8.5, Z_PANELS)]


def range_sf(w: float, k: int) -> float:
    """P(R > w) for the range R of k iid standard normal variables."""
    if k < 2:
        raise ValueError("need k >= 2")
    if w <= 0.0:
        return 1.0
    m = k - 1
    total = 0.0
    for z, wphi, a in _Z_NODES:
        r = norm_sf(z + w) / a
        diff = a ** m if r >= 1.0 else -(a ** m) * math.expm1(m * math.log1p(-r))
        total += wphi * diff
    return min(1.0, k * total)


def _chi2_point(nu: float, mass: float, upper: bool) -> float:
    """The x with P(X <= x) = mass (upper = False) or P(X > x) = mass, X chi-square with nu df."""
    f = (lambda x: chi2_sf(x, nu)) if upper else (lambda x: chi2_cdf(x, nu))
    lo, hi = 0.0, max(1.0, nu)
    if upper:
        while f(hi) > mass:
            lo, hi = hi, 2.0 * hi
    else:
        while f(lo) < mass and lo == 0.0 and f(hi) < mass:
            hi *= 2.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if mid <= lo or mid >= hi:
            break
        if (f(mid) > mass) == upper:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def srange_sf(q: float, k: int, nu: float) -> float:
    """P(Q > q) for the studentized range with k means and nu degrees of freedom."""
    if q <= 0.0:
        return 1.0
    if math.isinf(nu):
        return range_sf(q, k)
    s_lo = math.sqrt(_chi2_point(nu, 1e-30, False) / nu)
    s_hi = math.sqrt(_chi2_point(nu, 1e-30, True) / nu)
    # log of the density of S: nu^(nu/2) s^(nu-1) exp(-nu s^2 / 2) / (Gamma(nu/2) 2^(nu/2 - 1))
    log_c = 0.5 * nu * math.log(nu) - math.lgamma(0.5 * nu) - (0.5 * nu - 1.0) * math.log(2.0)
    total = 0.0
    for s, wt in _panels(s_lo, s_hi, S_PANELS):
        if s <= 0.0:
            continue
        dens = math.exp(log_c + (nu - 1.0) * math.log(s) - 0.5 * nu * s * s)
        total += wt * dens * range_sf(q * s, k)
    return min(1.0, total)


def srange_cdf(q: float, k: int, nu: float) -> float:
    """P(Q <= q)."""
    return 1.0 - srange_sf(q, k, nu)


def srange_ppf(p: float, k: int, nu: float) -> float:
    """The lower p-quantile of the studentized range, by bisection on the upper tail."""
    if not 0.0 < p < 1.0:
        raise ValueError("p must be in (0, 1)")
    tail = 1.0 - p
    lo, hi = 0.0, 4.0
    while srange_sf(hi, k, nu) > tail:
        lo, hi = hi, 2.0 * hi
    # Illinois false position on log tail, then a few bisection steps if it stalls.
    g = lambda x: math.log(srange_sf(x, k, nu)) - math.log(tail)
    a, b = lo, hi
    ga, gb = (math.inf if a == 0.0 else g(a)), g(b)
    if math.isinf(ga):
        a = 0.5 * b
        ga = g(a)
        while ga < 0.0:
            b, gb = a, ga
            a = 0.5 * a
            ga = g(a)
    side = 0
    for _ in range(100):
        x = b - gb * (b - a) / (gb - ga)
        gx = g(x)
        if abs(gx) < 1e-13 or abs(b - a) < 1e-12 * b:
            return x
        if gx * gb > 0.0:
            b, gb = x, gx
            if side == -1:
                ga *= 0.5
            side = -1
        else:
            a, ga = x, gx
            if side == 1:
                gb *= 0.5
            side = 1
    return 0.5 * (a + b)
