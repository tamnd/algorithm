# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/diffusion-posterior-sampling/. The authors are listed in prov/K0GFYT.jsonl.
"""Diffusion posterior sampling (DPS) of Chung, Kim, McCann, Klasky and Ye.

The score network is given: a function score(x, t) that approximates the
gradient of log p_t at x, and a function score_vjp(x, t, v) that returns
J^T v for the Jacobian J of score(., t) at x. The forward operator is given
by apply_a and apply_at. Steps are indexed t = N, ..., 1 with alpha_bars[t - 1]
the product of (1 - beta_s) for s <= t, and alpha_bar_0 = 1.
Vectors are lists of floats.
"""

import math


def schedule(alpha_bars, t):
    """Return (alpha_bar_t, alpha_bar_{t-1}, beta_t) for 1 <= t <= N."""
    ab = alpha_bars[t - 1]
    ab_prev = alpha_bars[t - 2] if t > 1 else 1.0
    return ab, ab_prev, 1.0 - ab / ab_prev


def tweedie(x, s, ab):
    """The denoised estimate (x + (1 - ab) s) / sqrt(ab)."""
    c = 1.0 / math.sqrt(ab)
    return [c * (xi + (1.0 - ab) * si) for xi, si in zip(x, s)]


def guidance_gradient(x, t, ab, x0, y, apply_a, apply_at, score_vjp):
    """The gradient of ||y - A x0(x)||^2 with respect to x, and the residual.

    x0(x) = (x + (1 - ab) score(x, t)) / sqrt(ab), so its Jacobian is
    (I + (1 - ab) J) / sqrt(ab) and the gradient is 2 times its transpose
    applied to A^T (A x0 - y).
    """
    r = [p - q for p, q in zip(apply_a(x0), y)]
    u = apply_at(r)
    ju = score_vjp(x, t, u)
    c = 2.0 / math.sqrt(ab)
    return [c * (ui + (1.0 - ab) * ji) for ui, ji in zip(u, ju)], r


def dps(y, apply_a, apply_at, score, score_vjp, alpha_bars, zeta, rng,
        normalize=True, x_start=None, n=None):
    """Run DPS from x_N ~ N(0, I) and return x_0.

    zeta is a number or a list with zeta[t - 1] for step t. With
    normalize=True the step is zeta / ||y - A x0||, as in the paper;
    with normalize=False it is zeta itself. Each step calls score once,
    score_vjp once, A once and A^T once.
    """
    big_n = len(alpha_bars)
    if x_start is None:
        x = [rng.gauss(0.0, 1.0) for _ in range(n)]  # @line L1
    else:
        x = list(x_start)  # @line L1
    for t in range(big_n, 0, -1):  # @line L2
        ab, ab_prev, beta = schedule(alpha_bars, t)
        s = score(x, t)  # @line L3
        x0 = tweedie(x, s, ab)  # @line L4
        c_x = math.sqrt(1.0 - beta) * (1.0 - ab_prev) / (1.0 - ab)  # @line L5
        c_0 = math.sqrt(ab_prev) * beta / (1.0 - ab)  # @line L5
        sd = math.sqrt((1.0 - ab_prev) / (1.0 - ab) * beta)  # @line L5
        xp = [c_x * xi + c_0 * x0i + sd * rng.gauss(0.0, 1.0)  # @line L5
              for xi, x0i in zip(x, x0)]
        g, r = guidance_gradient(x, t, ab, x0, y, apply_a, apply_at, score_vjp)  # @line L6
        z = zeta[t - 1] if isinstance(zeta, (list, tuple)) else zeta
        if normalize:  # @line L7
            norm = math.sqrt(sum(v * v for v in r))  # @line L7
            z = z / norm if norm > 0.0 else 0.0  # @line L7
        x = [a - z * b for a, b in zip(xp, g)]  # @line L8
    return x  # @line L9


def linear_alpha_bars(big_n, beta_min, beta_max):
    """alpha_bar_t for a linear beta schedule from beta_min to beta_max."""
    out, prod = [], 1.0
    for t in range(big_n):
        beta = beta_min + (beta_max - beta_min) * t / max(big_n - 1, 1)
        prod *= 1.0 - beta
        out.append(prod)
    return out


def gaussian_score(alpha_bars, prior_var):
    """The exact score of p_t when x_0 ~ N(0, diag(prior_var)).

    p_t = N(0, ab * prior_var + 1 - ab) in each coordinate, so the score is
    -x / v and its Jacobian is diagonal with entries -1 / v.
    """
    def var(t, j):
        ab = alpha_bars[t - 1]
        return ab * prior_var[j] + 1.0 - ab

    def score(x, t):
        return [-xi / var(t, j) for j, xi in enumerate(x)]

    def score_vjp(x, t, v):
        return [-vi / var(t, j) for j, vi in enumerate(v)]

    return score, score_vjp


def linear_dps_moments(a_scalar, y, alpha_bars, prior_var, zetas):
    """Exact mean and variance of DPS output for a 1D Gaussian prior.

    With A = a_scalar, the exact score of N(0, prior_var) and the unnormalized
    step zetas[t - 1], every step is x <- k x + b + sd * noise, so the mean and
    the variance follow a linear recursion from N(0, 1).
    """
    mean, var = 0.0, 1.0
    for t in range(len(alpha_bars), 0, -1):
        ab, ab_prev, beta = schedule(alpha_bars, t)
        v = ab * prior_var + 1.0 - ab
        c = math.sqrt(ab) * prior_var / v  # x0 = c x, Tweedie for a Gaussian
        c_x = math.sqrt(1.0 - beta) * (1.0 - ab_prev) / (1.0 - ab)
        c_0 = math.sqrt(ab_prev) * beta / (1.0 - ab)
        sd2 = (1.0 - ab_prev) / (1.0 - ab) * beta
        z = zetas[t - 1]
        # g = 2 c a (a c x - y)
        k = c_x + c_0 * c - z * 2.0 * c * c * a_scalar * a_scalar
        b = z * 2.0 * c * a_scalar * y
        mean = k * mean + b
        var = k * k * var + sd2
    return mean, var
