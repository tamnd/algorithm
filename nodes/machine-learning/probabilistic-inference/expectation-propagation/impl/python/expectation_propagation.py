# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/expectation-propagation/. The authors are listed in prov/6W6NCV.jsonl.

"""Expectation propagation (Minka 2001) for the one-dimensional clutter problem.

Model: theta ~ N(0, b); each observation x_n ~ (1 - w) N(theta, 1) + w N(0, a).
The posterior is p(theta | x) proportional to N(theta; 0, b) prod_n t_n(theta) with
t_n(theta) = (1 - w) N(x_n; theta, 1) + w N(x_n; 0, a).

EP keeps a Gaussian site for each t_n in natural parameters: precision tau_n and
precision times mean nu_n. The approximation is q = prior times all sites,
a Gaussian N(m, v) with 1 / v = 1 / b + sum tau_n and m / v = sum nu_n.
"""

import math


def normal_pdf(x, mean, var):
    return math.exp(-0.5 * (x - mean) ** 2 / var) / math.sqrt(2 * math.pi * var)


def tilted_moments(x, w, a, m_c, v_c):
    """Z, mean and variance of t(theta) N(theta; m_c, v_c), in closed form (Minka 2001)."""
    z_signal = (1 - w) * normal_pdf(x, m_c, v_c + 1)
    z_clutter = w * normal_pdf(x, 0.0, a)
    Z = z_signal + z_clutter
    r = z_signal / Z  # the probability that x is not clutter, under the tilted distribution
    d = x - m_c
    mean = m_c + v_c * r * d / (v_c + 1)
    var = v_c - r * v_c ** 2 / (v_c + 1) + r * (1 - r) * v_c ** 2 * d ** 2 / (v_c + 1) ** 2
    return Z, mean, var


def ep_clutter(xs, w=0.5, a=10.0, b=100.0, tol=1e-10, max_sweeps=1000, damping=0.0):
    """Run EP with sequential updates. Return (m, v, sweeps, converged, skipped),
    where skipped counts the updates left out because the cavity was improper."""
    n = len(xs)
    tau = [0.0] * n  # @line L1
    nu = [0.0] * n
    prec, pm = 1.0 / b, 0.0  # natural parameters of q: 1/v and m/v
    skipped = 0
    for sweep in range(1, max_sweeps + 1):  # @line L2
        delta = 0.0
        for i, x in enumerate(xs):
            prec_c, pm_c = prec - tau[i], pm - nu[i]  # @line L3
            if prec_c <= 0:
                skipped += 1
                continue
            v_c, m_c = 1.0 / prec_c, pm_c / prec_c
            _, m_new, v_new = tilted_moments(x, w, a, m_c, v_c)  # @line L4
            new_prec, new_pm = 1.0 / v_new, m_new / v_new  # @line L5
            t_new = (1 - damping) * (new_prec - prec_c) + damping * tau[i]  # @line L6
            n_new = (1 - damping) * (new_pm - pm_c) + damping * nu[i]
            delta = max(delta, abs(t_new - tau[i]), abs(n_new - nu[i]))
            tau[i], nu[i] = t_new, n_new
            prec, pm = prec_c + t_new, pm_c + n_new
        if delta < tol:  # @line L7
            return pm / prec, 1.0 / prec, sweep, True, skipped  # @line L8
    return pm / prec, 1.0 / prec, max_sweeps, False, skipped


def ep_sites(xs, w=0.5, a=10.0, b=100.0, tol=1e-12, max_sweeps=1000):
    """The same EP run, returning the site parameters as well, for checks."""
    n = len(xs)
    tau, nu = [0.0] * n, [0.0] * n
    prec, pm = 1.0 / b, 0.0
    for _ in range(max_sweeps):
        delta = 0.0
        for i, x in enumerate(xs):
            prec_c, pm_c = prec - tau[i], pm - nu[i]
            if prec_c <= 0:
                continue
            _, m_new, v_new = tilted_moments(x, w, a, pm_c / prec_c, 1.0 / prec_c)
            t_new, n_new = 1.0 / v_new - prec_c, m_new / v_new - pm_c
            delta = max(delta, abs(t_new - tau[i]), abs(n_new - nu[i]))
            tau[i], nu[i] = t_new, n_new
            prec, pm = prec_c + t_new, pm_c + n_new
        if delta < tol:
            break
    return tau, nu, prec, pm


def log_posterior(theta, xs, w, a, b):
    s = -0.5 * theta * theta / b
    for x in xs:
        s += math.log((1 - w) * normal_pdf(x, theta, 1.0) + w * normal_pdf(x, 0.0, a))
    return s


def integrate_moments(logf, lo, hi, steps):
    """Mean and variance of the density proportional to exp(logf) on [lo, hi], by the trapezoid rule."""
    h = (hi - lo) / steps
    ts = [lo + k * h for k in range(steps + 1)]
    ls = [logf(t) for t in ts]
    top = max(ls)
    fs = [math.exp(l - top) for l in ls]
    wts = [0.5 if k in (0, steps) else 1.0 for k in range(steps + 1)]
    z = sum(c * f for c, f in zip(wts, fs))
    mean = sum(c * f * t for c, f, t in zip(wts, fs, ts)) / z
    var = sum(c * f * (t - mean) ** 2 for c, f, t in zip(wts, fs, ts)) / z
    return mean, var


def clutter_data(n, theta, w, a, rng):
    return [rng.gauss(0.0, math.sqrt(a)) if rng.random() < w else rng.gauss(theta, 1.0) for _ in range(n)]
