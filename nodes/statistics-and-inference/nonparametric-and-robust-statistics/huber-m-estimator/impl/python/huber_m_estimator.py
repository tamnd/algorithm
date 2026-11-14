# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/huber-m-estimator/. The authors are listed in prov/ASDS28.jsonl.

from fractions import Fraction
from statistics import NormalDist

# Phi^{-1}(3/4): the MAD of N(0, 1).
Q3 = NormalDist().inv_cdf(0.75)


def psi(u, k):
    """Huber's psi: u clipped to [-k, k]."""
    if u > k:
        return k
    if u < -k:
        return -k
    return u


def rho(u, k):
    """Huber's loss: u^2/2 for |u| <= k, k|u| - k^2/2 beyond."""
    a = abs(u)
    return u * u / 2 if a <= k else k * a - k * k / 2


def exact_median(xs):
    """Median; exact (int or Fraction) for int or Fraction data."""
    s = sorted(xs)
    n = len(s)
    if n % 2 == 1:
        return s[n // 2]
    lo, hi = s[n // 2 - 1], s[n // 2]
    if isinstance(lo, (int, Fraction)) and isinstance(hi, (int, Fraction)):
        return Fraction(lo + hi, 2)
    return (lo + hi) / 2


def mad_scale(xs):
    """Normalized MAD: median |x - median| divided by Phi^{-1}(3/4)."""
    m = exact_median(xs)
    return float(exact_median([abs(v - m) for v in xs])) / Q3


def objective(xs, theta, k, sigma):
    """sum rho_k((x_i - theta)/sigma)."""
    return sum(rho((v - theta) / sigma, k) for v in xs)


def estimating_function(xs, theta, k, sigma):
    """Lambda(theta) = sum psi_k((x_i - theta)/sigma): continuous, nonincreasing, piecewise linear."""
    return sum(psi((v - theta) / sigma, k) for v in xs)


def huber_location(xs, k=1.345, sigma=None):
    """Huber M-estimate of location with a fixed scale.

    sigma defaults to the normalized MAD of xs. The result is the midpoint of the
    set of roots of Lambda, which is also the set of minimizers of the objective.
    With int or Fraction data and Fraction k and sigma the result is exact.
    Time O(n log n).
    """
    x = list(xs)
    if not x:
        raise ValueError("empty sample")
    if not k > 0:
        raise ValueError("k must be positive")
    if sigma is None:
        sigma = mad_scale(x)  # @line L1
    if sigma == 0:
        return exact_median(x)  # @line L1
    if sigma < 0:
        raise ValueError("sigma must be positive")
    c = k * sigma
    b = sorted({v - c for v in x} | {v + c for v in x})  # @line L2

    def lam(t):
        return estimating_function(x, t, k, sigma)  # @line L3

    # Lambda(b[0]) = n k > 0 and Lambda(b[-1]) = -n k < 0.
    lo, hi = 1, len(b) - 1
    while lo < hi:  # @line L4
        mid = (lo + hi) // 2
        if lam(b[mid]) <= 0:
            hi = mid
        else:
            lo = mid + 1
    t = lo
    l0, l1 = lam(b[t - 1]), lam(b[t])
    theta_lo = b[t - 1] + (b[t] - b[t - 1]) * l0 / (l0 - l1)  # @line L5

    lo, hi = 0, len(b) - 2
    while lo < hi:  # @line L6
        mid = (lo + hi + 1) // 2
        if lam(b[mid]) >= 0:
            lo = mid
        else:
            hi = mid - 1
    u = lo
    m0, m1 = lam(b[u]), lam(b[u + 1])
    theta_hi = b[u] + (b[u + 1] - b[u]) * m0 / (m0 - m1)  # @line L7
    return (theta_lo + theta_hi) / 2  # @line L8


def huber_irls(xs, k=1.345, sigma=None, tol=1e-12, max_iter=500):
    """The usual iteration: weighted means with weights min(1, k sigma / |x - theta|)."""
    x = [float(v) for v in xs]
    if sigma is None:
        sigma = mad_scale(x)
    theta = float(exact_median(x))
    if sigma == 0:
        return theta
    c = k * sigma
    for _ in range(max_iter):
        w = [1.0 if abs(v - theta) <= c else c / abs(v - theta) for v in x]
        new = sum(wi * v for wi, v in zip(w, x)) / sum(w)
        if abs(new - theta) <= tol * (1.0 + abs(theta)):
            return new
        theta = new
    return theta
