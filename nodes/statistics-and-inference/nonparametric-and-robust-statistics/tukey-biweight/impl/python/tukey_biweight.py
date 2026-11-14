# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tukey-biweight/. The authors are listed in prov/9NDW0S.jsonl.

from fractions import Fraction
from statistics import NormalDist

# Phi^{-1}(3/4): the MAD of N(0, 1).
Q3 = NormalDist().inv_cdf(0.75)


def weight(u, c):
    """Biweight weight psi(u)/u = (1 - (u/c)^2)^2 inside (-c, c), 0 outside."""
    if abs(u) >= c:
        return 0 * u
    t = 1 - (u / c) ** 2
    return t * t


def psi(u, c):
    return u * weight(u, c)


def rho(u, c):
    """Biweight loss (c^2/6)(1 - (1 - (u/c)^2)^3) inside, c^2/6 outside."""
    if abs(u) >= c:
        return c * c / 6
    return c * c / 6 * (1 - (1 - (u / c) ** 2) ** 3)


def exact_median(xs):
    s = sorted(xs)
    n = len(s)
    if n % 2 == 1:
        return s[n // 2]
    lo, hi = s[n // 2 - 1], s[n // 2]
    if isinstance(lo, (int, Fraction)) and isinstance(hi, (int, Fraction)):
        return Fraction(lo + hi, 2)
    return (lo + hi) / 2


def mad_scale(xs):
    m = exact_median(xs)
    return float(exact_median([abs(v - m) for v in xs])) / Q3


def objective(xs, theta, c, sigma):
    return sum(rho((v - theta) / sigma, c) for v in xs)


def biweight_step(xs, theta, c, sigma):
    """One reweighting step: the weighted mean with weights w((x_i - theta)/sigma)."""
    w = [weight((v - theta) / sigma, c) for v in xs]  # @line L4
    sw = sum(w)
    if sw == 0:
        raise ValueError("all weights are zero")
    return sum(wi * v for wi, v in zip(w, xs)) / sw  # @line L5


def biweight_location(xs, c=4.685, sigma=None, tol=1e-12, max_iter=1000, trace=None):
    """Tukey biweight M-estimate of location by IRLS from the median, with the scale fixed.

    sigma defaults to the normalized MAD. Returns a root of sum psi((x_i - theta)/sigma) = 0
    (up to tol); the objective does not increase along the iterates. If trace is a list,
    the iterates are appended to it. The iteration runs in floating point; use
    biweight_step for exact single steps.
    """
    x = [float(v) for v in xs]
    if not x:
        raise ValueError("empty sample")
    theta = exact_median(x)  # @line L1
    sigma = mad_scale(x) if sigma is None else float(sigma)  # @line L1
    c = float(c)
    if sigma == 0:
        return theta  # @line L1
    if trace is not None:
        trace.append(theta)
    for _ in range(max_iter):  # @line L2
        new = biweight_step(x, theta, c, sigma)  # @line L3
        if trace is not None:
            trace.append(new)
        if abs(new - theta) <= tol * sigma:  # @line L6
            return new
        theta = new  # @line L7
    return theta
