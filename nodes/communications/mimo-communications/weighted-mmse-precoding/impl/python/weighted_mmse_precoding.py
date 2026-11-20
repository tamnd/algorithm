# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/weighted-mmse-precoding/. The authors are listed in prov/9QVSR3.jsonl.

"""Weighted MMSE (WMMSE) precoding for the multiuser MISO downlink.

User k receives y_k = h_k^H x + w_k with w_k ~ CN(0, N0), and the base
station sends x = sum_k v_k s_k with sum_k ||v_k||^2 <= P. The goal is a
local maximum of the weighted sum rate sum_k a_k log2(1 + SINR_k).

WMMSE solves the equivalent problem

    minimize over (u, w, V)   sum_k a_k (w_k e_k - log w_k),
    e_k = E|conj(u_k) y_k - s_k|^2,

by block coordinate descent: the MMSE receive gains u (line L2), the weights
w = 1 / e (line L3), and the precoders V, a convex problem solved by a
Lagrange multiplier mu found by a safeguarded Newton search (lines L4 to L6). After the u and w
steps the objective equals sum_k a_k (1 - ln(1 + SINR_k)), so the weighted
sum rate never decreases from one iteration to the next.
"""

import math

import cbb


def sinr(h: list[list[complex]], v: list[list[complex]], n0: float) -> list[float]:
    """SINR_k = |h_k^H v_k|^2 / (sum over j != k of |h_k^H v_j|^2 + N0); v has the v_k as columns."""
    e = cbb.matmul(h, v)
    out = []
    for k in range(len(h)):
        sig = abs(e[k][k]) ** 2
        out.append(sig / (sum(abs(x) ** 2 for x in e[k]) - sig + n0))
    return out


def weighted_sum_rate(h, v, n0: float, weights: list[float]) -> float:
    """sum_k a_k log2(1 + SINR_k) in bits per channel use."""
    return sum(a * math.log2(1.0 + s) for a, s in zip(weights, sinr(h, v, n0)))


def _solve_mu(a: list[list[complex]], b: list[list[complex]], p_total: float):
    """The precoder (A + mu I)^(-1) B with the smallest mu >= 0 that keeps the power at most P.

    The power f(mu) = ||(A + mu I)^(-1) B||_F^2 decreases in mu, and
    f(mu) <= ||B||_F^2 / mu^2 because A is positive semidefinite, so
    mu = ||B||_F / sqrt(P) is an upper bound. The root of f(mu) = P is found
    by Newton's method on f^(-1/2) - P^(-1/2), which is close to linear in
    mu, with a bisection step whenever Newton leaves the bracket.
    Returns (V, mu).
    """
    m = len(a)

    def shifted(mu: float):
        return [[a[i][j] + (mu if i == j else 0.0) for j in range(m)] for i in range(m)]

    lo, hi = 0.0, math.sqrt(cbb.norm2(b) / p_total)
    try:
        v = cbb.solve(a, b)
        if cbb.norm2(v) <= p_total:
            return v, 0.0
        mu = 0.0
    except ValueError:
        mu = 1e-9 * hi  # A is singular, so start a little above 0
    v_hi = None
    for _ in range(100):
        am = shifted(mu)
        v = cbb.solve(am, b)
        f = cbb.norm2(v)
        if abs(f - p_total) <= 1e-14 * p_total:
            return v, mu
        if f > p_total:
            lo = mu
        else:
            hi, v_hi = mu, v
        y = cbb.solve(am, v)
        df = -2.0 * sum((v[i][k].conjugate() * y[i][k]).real for i in range(m) for k in range(len(v[0])))
        nxt = mu - (f ** -0.5 - p_total ** -0.5) / (-0.5 * f ** -1.5 * df) if df < 0 else -1.0
        mu = nxt if lo < nxt < hi else 0.5 * (lo + hi)
        if hi - lo <= 1e-15 * hi:
            break
    if v_hi is None:
        v_hi = cbb.solve(shifted(hi), b)
    return v_hi, hi


def wmmse(h: list[list[complex]], p_total: float, n0: float, weights=None, v0=None, iters: int = 200, tol: float = 1e-12):
    """Run WMMSE on the K by M channel h. Returns (v, rates) with the precoders as columns of v.

    rates[t] is the weighted sum rate after iteration t (rates[0] is the start).
    The start is v0, or by default the matched beams h_k scaled to the power P.
    """
    k_users, m = len(h), len(h[0])
    a = weights if weights is not None else [1.0] * k_users
    if v0 is None:
        v0 = cbb.herm(h)
        v0 = cbb.scale(math.sqrt(p_total / cbb.norm2(v0)), v0)
    v = [row[:] for row in v0]  # @line L1
    rates = [weighted_sum_rate(h, v, n0, a)]
    for _ in range(iters):
        e = cbb.matmul(h, v)
        tot = [sum(abs(x) ** 2 for x in e[k]) + n0 for k in range(k_users)]
        u = [e[k][k] / tot[k] for k in range(k_users)]  # @line L2
        w = [1.0 / (1.0 - (u[k].conjugate() * e[k][k]).real) for k in range(k_users)]  # @line L3
        amat = [[0j] * m for _ in range(m)]
        bmat = [[0j] * k_users for _ in range(m)]
        for k in range(k_users):
            c = a[k] * w[k] * abs(u[k]) ** 2
            hk = [complex(z).conjugate() for z in h[k]]  # the column h_k
            for i in range(m):
                for j in range(m):
                    amat[i][j] += c * hk[i] * hk[j].conjugate()  # @line L4
                bmat[i][k] = a[k] * w[k] * u[k] * hk[i]
        v, _ = _solve_mu(amat, bmat, p_total)  # @line L5
        rates.append(weighted_sum_rate(h, v, n0, a))  # @line L6
        if rates[-1] - rates[-2] < tol:
            break  # @line L7
    return v, rates
