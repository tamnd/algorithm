# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/self-tuning-regulator/. The authors are listed in prov/KY0VB7.jsonl.

"""The direct minimum variance self-tuning regulator of Astrom and Wittenmark.

Plant (ARMAX, delay one sample):

    y_t = -a_1 y_(t-1) - ... - a_n y_(t-n) + b_1 u_(t-1) + ... + b_m u_(t-m)
          + e_t + c_1 e_(t-1) + ... + c_k e_(t-k),

with white noise e_t. The regulator estimates by recursive least squares
the predictor model

    y_(t+1) - beta0 u_t = s_0 y_t + ... + s_ns y_(t-ns) + r_1 u_(t-1) + ... + r_nr u_(t-nr),

with beta0 fixed (a guess of b_1), and applies the control that makes the
predicted output zero (certainty equivalence):

    u_t = -(s_0 y_t + ... + r_nr u_(t-nr)) / beta0.

rls_update works with float or Fraction entries; with Fraction it is exact.
"""

import random

__all__ = ["rls_update", "str_minimum_variance", "mv_gain_first_order"]


def rls_update(theta, P, phi, z, lam=1):
    """One recursive least squares step with forgetting factor lam.

    theta: estimate (list), P: covariance (list of rows), phi: regressor,
    z: new measurement. Returns (theta, P) for the data up to z.
    """
    n = len(theta)
    Pphi = [sum(P[i][j] * phi[j] for j in range(n)) for i in range(n)]
    den = lam + sum(phi[i] * Pphi[i] for i in range(n))
    K = [v / den for v in Pphi]  # @line L5
    eps = z - sum(phi[i] * theta[i] for i in range(n))
    theta = [theta[i] + K[i] * eps for i in range(n)]  # @line L6
    P = [[(P[i][j] - K[i] * Pphi[j]) / lam for j in range(n)] for i in range(n)]  # @line L7
    return theta, P


def str_minimum_variance(a, b, c, beta0, N, seed, ns=0, nr=0, sigma=1.0, p0=100.0, lam=1.0,
                         theta0=None, adapt=True):
    """Run the self-tuning regulator for N samples on the ARMAX plant.

    a, b, c are the coefficient lists [a_1..a_n], [b_1..b_m], [c_1..c_k].
    The noise e_t is Gaussian with standard deviation sigma from
    random.Random(seed). The estimate starts at theta0 (zeros if None).
    With adapt=False the estimate stays at theta0, which gives a fixed
    controller. Returns (thetas, ys, us, es): the estimate after each
    sample, the outputs, the inputs and the noise.
    """
    rng = random.Random(seed)
    d = ns + 1 + nr
    theta = [0.0] * d if theta0 is None else [float(v) for v in theta0]  # @line L1
    P = [[p0 if i == j else 0.0 for j in range(d)] for i in range(d)]
    hist = max(len(a), len(b), len(c), ns + 1, nr + 1) + 1
    ys, us, es = [0.0] * hist, [0.0] * hist, [0.0] * hist
    thetas = []
    phi_prev = None
    for _ in range(N):  # @line L2
        e = rng.gauss(0.0, sigma)
        y = (-sum(ai * ys[-1 - i] for i, ai in enumerate(a))
             + sum(bi * us[-1 - i] for i, bi in enumerate(b))
             + e + sum(ci * es[-1 - i] for i, ci in enumerate(c)))  # @line L3
        ys.append(y)
        es.append(e)
        if phi_prev is not None and adapt:
            z = y - beta0 * us[-1]  # @line L4
            theta, P = rls_update(theta, P, phi_prev, z, lam)
        phi = [ys[-1 - i] for i in range(ns + 1)] + [us[-1 - i] for i in range(nr)]
        u = -sum(t * p for t, p in zip(theta, phi)) / beta0  # @line L8
        us.append(u)
        phi_prev = phi
        thetas.append(list(theta))
    return thetas, ys[hist:], us[hist:], es[hist:]  # @line L9


def mv_gain_first_order(a, b, c):
    """Minimum variance gain for y_(t+1) = -a y_t + b u_t + e_(t+1) + c e_t.

    u_t = g y_t with g = (a - c) / b makes y_t = e_t.
    """
    return (a - c) / b
