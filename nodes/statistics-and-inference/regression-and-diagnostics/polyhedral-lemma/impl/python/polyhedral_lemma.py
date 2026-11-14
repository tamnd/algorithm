# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/polyhedral-lemma/. The authors are listed in prov/TA2HX1.jsonl.
"""The polyhedral lemma of Lee, Sun, Sun and Taylor (2016), and the selective test and interval it gives.

Let y ~ N(mu, Sigma) and let the selection event be a polyhedron {A y <= b}.
For a direction eta set c = Sigma eta / (eta^T Sigma eta) and z = y - c eta^T y.
Then {A y <= b} = {V-(z) <= eta^T y <= V+(z), V0(z) >= 0} with

    alpha = A c,
    V-(z) = max over alpha_j < 0 of (b_j - (A z)_j) / alpha_j,
    V+(z) = min over alpha_j > 0 of (b_j - (A z)_j) / alpha_j,
    V0(z) = min over alpha_j = 0 of  b_j - (A z)_j,

and z is independent of eta^T y. So, given the event and z, eta^T y is normal
with mean eta^T mu and variance eta^T Sigma eta, truncated to [V-, V+], and
its truncated CDF at the observed value is uniform on (0, 1).

The truncated CDF uses log tails, so it stays accurate when both limits are
far out in the same tail (the case that a plain difference of Phi values gets
wrong).
"""

import math

_SQRT2 = math.sqrt(2.0)
_LOG_SQRT_2PI = 0.5 * math.log(2.0 * math.pi)


def log_norm_sf(x):
    """log P(Z > x) for a standard normal Z, accurate in the far upper tail."""
    if x == math.inf:
        return -math.inf
    if x == -math.inf:
        return 0.0
    if x < 30.0:
        return math.log(0.5 * math.erfc(x / _SQRT2))
    # Asymptotic series of the Mills ratio; for x >= 30 the first omitted term is below 3e-14.
    u = 1.0 / (x * x)
    series = -u + 3.0 * u ** 2 - 15.0 * u ** 3 + 105.0 * u ** 4 - 945.0 * u ** 5
    return -0.5 * x * x - math.log(x) - _LOG_SQRT_2PI + math.log1p(series)


def truncated_normal_cdf(x, mu, sd, a, b):
    """P(T <= x) for T normal with mean mu and standard deviation sd, conditioned on a <= T <= b."""
    if not a < b:
        raise ValueError("need a < b")
    if x <= a:
        return 0.0
    if x >= b:
        return 1.0
    za, zb, zx = (a - mu) / sd, (b - mu) / sd, (x - mu) / sd
    if za >= 0.0:
        # Whole interval in the upper tail: (Q(za) - Q(zx)) / (Q(za) - Q(zb)), with ratios of tails.
        la = log_norm_sf(za)
        rx = math.exp(log_norm_sf(zx) - la)
        rb = math.exp(log_norm_sf(zb) - la)
        return (1.0 - rx) / (1.0 - rb)
    if zb <= 0.0:
        # Whole interval in the lower tail: mirror, Phi(t) = Q(-t).
        lb = log_norm_sf(-zb)
        rx = math.exp(log_norm_sf(-zx) - lb)
        ra = math.exp(log_norm_sf(-za) - lb)
        return (rx - ra) / (1.0 - ra)
    lo = 0.5 * math.erfc(-za / _SQRT2)
    hi = 0.5 * math.erfc(-zb / _SQRT2)
    mid = 0.5 * math.erfc(-zx / _SQRT2)
    return (mid - lo) / (hi - lo)


def truncation_limits(a_mat, b_vec, eta, sigma, y):
    """(V-, V+, V0, eta^T y, eta^T Sigma eta) for the event {A y <= b} and the direction eta."""
    n = len(y)
    s_eta = [math.fsum(sigma[i][k] * eta[k] for k in range(n)) for i in range(n)]
    var = math.fsum(e * s for e, s in zip(eta, s_eta))
    if not var > 0.0:
        raise ValueError("eta^T Sigma eta must be positive")
    c = [s / var for s in s_eta]
    t = math.fsum(e * v for e, v in zip(eta, y))
    z = [v - ci * t for v, ci in zip(y, c)]
    vminus, vplus, v0 = -math.inf, math.inf, math.inf
    for row, bj in zip(a_mat, b_vec):
        alpha = math.fsum(r * ci for r, ci in zip(row, c))
        rest = bj - math.fsum(r * zi for r, zi in zip(row, z))
        if alpha > 0.0:
            vplus = min(vplus, rest / alpha)
        elif alpha < 0.0:
            vminus = max(vminus, rest / alpha)
        else:
            v0 = min(v0, rest)
    return vminus, vplus, v0, t, var


def max_abs_selection(y):
    """The index j and sign s of the largest |y_j|, and the polyhedron {A y <= 0} of that event."""
    p = len(y)
    j = max(range(p), key=lambda k: abs(y[k]))
    s = 1.0 if y[j] >= 0.0 else -1.0
    rows = []
    for k in range(p):
        if k == j:
            continue
        for sign in (1.0, -1.0):
            row = [0.0] * p
            row[j] = -s          # -s y_j + sign * y_k <= 0, that is s y_j >= sign * y_k
            row[k] = sign
            rows.append(row)
    row = [0.0] * p
    row[j] = -s
    rows.append(row)            # s y_j >= 0
    return j, s, rows, [0.0] * len(rows)


def selective_pivot(a_mat, b_vec, eta, sigma, y, mu_eta=0.0):
    """The truncated normal CDF of eta^T y at mean mu_eta; uniform on (0, 1) given the event when mu_eta is true."""
    vm, vp, v0, t, var = truncation_limits(a_mat, b_vec, eta, sigma, y)
    if v0 < 0.0 or not vm <= t <= vp:
        raise ValueError("y is not in the selection event")
    return truncated_normal_cdf(t, mu_eta, math.sqrt(var), vm, vp)


def selective_p_value(a_mat, b_vec, eta, sigma, y):
    """One-sided p-value for H0: eta^T mu = 0 against eta^T mu > 0, valid given the selection event."""
    return 1.0 - selective_pivot(a_mat, b_vec, eta, sigma, y, 0.0)


def selective_interval(a_mat, b_vec, eta, sigma, y, level=0.95):
    """The equal-tailed interval for eta^T mu by inverting the pivot, which decreases in the mean."""
    vm, vp, v0, t, var = truncation_limits(a_mat, b_vec, eta, sigma, y)
    sd = math.sqrt(var)
    alpha = 1.0 - level

    def root(target):
        lo, hi = t - sd, t + sd
        while truncated_normal_cdf(t, lo, sd, vm, vp) < target:
            lo -= 2.0 * (hi - lo)
        while truncated_normal_cdf(t, hi, sd, vm, vp) > target:
            hi += 2.0 * (hi - lo)
        for _ in range(200):
            mid = 0.5 * (lo + hi)
            if truncated_normal_cdf(t, mid, sd, vm, vp) > target:
                lo = mid
            else:
                hi = mid
        return 0.5 * (lo + hi)

    return root(1.0 - alpha / 2.0), root(alpha / 2.0)
