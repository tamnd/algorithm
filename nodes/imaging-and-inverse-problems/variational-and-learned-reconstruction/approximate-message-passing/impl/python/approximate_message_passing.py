# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/approximate-message-passing/. The authors are listed in prov/SKJZMH.jsonl.
"""Approximate message passing (AMP) with soft thresholding, and its state evolution.

A is a list of m rows of length n, scaled so that the columns have norm
close to 1 (i.i.d. N(0, 1/m) entries in the theory). The iteration of
Donoho, Maleki and Montanari (2009) is

    x^{t+1} = eta(x^t + A^T z^t; theta_t)
    z^{t+1} = y - A x^{t+1} + (||x^{t+1}||_0 / m) z^t

where eta is soft thresholding and the last term is the Onsager correction.
"""

import math


def soft(v, theta):
    """Soft thresholding eta(v; theta) = sign(v) max(|v| - theta, 0)."""
    if v > theta:
        return v - theta
    if v < -theta:
        return v + theta
    return 0.0


def _matvec(a, x):
    return [sum(aij * xj for aij, xj in zip(row, x)) for row in a]


def _rmatvec(a, z):
    out = [0.0] * len(a[0])
    for row, zi in zip(a, z):
        if zi != 0.0:
            for j, aij in enumerate(row):
                out[j] += aij * zi
    return out


def amp(a, y, alpha=None, theta=None, iters=30, onsager=True, tol=0.0):
    """Run AMP. Returns (x, z, history).

    Give either alpha (threshold theta_t = alpha * ||z^t|| / sqrt(m), the rule
    of the paper) or a fixed threshold theta. With onsager=False the
    correction term is dropped, which gives plain iterative soft
    thresholding with the same thresholds. history holds (x^t, tau_t) with
    tau_t = ||z^t|| / sqrt(m), the estimate of the effective noise level.
    The loop stops early when ||x^{t+1} - x^t|| <= tol.
    """
    if (alpha is None) == (theta is None):
        raise ValueError("give exactly one of alpha and theta")
    m, n = len(a), len(a[0])
    x = [0.0] * n  # @line L1
    z = list(y)
    history = []
    for _ in range(iters):  # @line L2
        tau = math.sqrt(sum(v * v for v in z) / m)  # @line L3
        th = alpha * tau if alpha is not None else theta  # @line L4
        history.append((x, tau))
        r = _rmatvec(a, z)
        x_new = [soft(xj + rj, th) for xj, rj in zip(x, r)]  # @line L5
        b = sum(1 for v in x_new if v != 0.0) / m if onsager else 0.0  # @line L6
        ax = _matvec(a, x_new)
        z = [yi - axi + b * zi for yi, axi, zi in zip(y, ax, z)]  # @line L7
        step = math.sqrt(sum((p - q) ** 2 for p, q in zip(x_new, x)))
        x = x_new
        if step <= tol:
            break
    history.append((x, math.sqrt(sum(v * v for v in z) / m)))
    return x, z, history  # @line L8


def _gauss_expect(f, mu, tau, points=801, width=8.0):
    """E[f(mu + tau Z)] for Z ~ N(0, 1), by Simpson's rule on [-width, width]."""
    h = 2.0 * width / (points - 1)
    total = 0.0
    for k in range(points):
        u = -width + k * h
        w = 1.0 if k in (0, points - 1) else (4.0 if k % 2 else 2.0)
        total += w * f(mu + tau * u) * math.exp(-0.5 * u * u)
    return total * h / 3.0 / math.sqrt(2.0 * math.pi)


def mse_soft(prior, tau, theta):
    """E[(eta(X + tau Z; theta) - X)^2] for a discrete prior [(value, prob), ...]."""
    return sum(p * _gauss_expect(lambda w, x0=x0: (soft(w, theta) - x0) ** 2, x0, tau) for x0, p in prior)


def state_evolution(prior, delta, sigma2, alpha, steps):
    """tau_t^2 for t = 0..steps, from tau_{t+1}^2 = sigma2 + mse(tau_t, alpha tau_t) / delta.

    The start is tau_0^2 = sigma2 + E[X^2] / delta (the iteration starts at x = 0).
    Returns (taus2, mses) with mses[t] the predicted per-entry MSE of x^{t+1}.
    """
    taus2 = [sigma2 + sum(p * x0 * x0 for x0, p in prior) / delta]
    mses = []
    for _ in range(steps):
        tau = math.sqrt(taus2[-1])
        e = mse_soft(prior, tau, alpha * tau)
        mses.append(e)
        taus2.append(sigma2 + e / delta)
    return taus2, mses
