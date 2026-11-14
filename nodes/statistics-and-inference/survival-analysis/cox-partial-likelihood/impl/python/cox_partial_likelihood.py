# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cox-partial-likelihood/. The authors are listed in prov/9HJDFT.jsonl.
"""Cox partial likelihood: value, score, information, Newton fit, score test, Schoenfeld residuals.

Data: times[i] = y_i, events[i] = delta_i (1 event, 0 censored), X[i] = the
covariate vector x_i of length p, beta = the coefficient vector of length p.
Ties between event times are handled by the Breslow (1974) or Efron (1977)
approximation, or exactly by the discrete (conditional logistic) partial
likelihood of Cox (1972), computed with the subset-sum recursion of Gail,
Lubin and Rubinstein (1981). A censored time tied with an event time counts
as at risk at that time.

If every entry of beta is 0 and the covariates are ints or Fractions, the
weights exp(x_i' beta) are the integer 1 and the score and the information
come out exact (Fractions). The log partial likelihood is always a float.
"""

import math
from collections.abc import Sequence
from fractions import Fraction
from typing import NamedTuple

from stdist import chi2_sf

TIES = ("breslow", "efron", "exact")


def _check(times, events, X, beta):
    n = len(times)
    if n == 0 or len(events) != n or len(X) != n:
        raise ValueError("times, events and X must have the same positive length")
    if any(e not in (0, 1) for e in events):
        raise ValueError("event flags must be 0 or 1")
    p = len(beta)
    if any(len(x) != p for x in X):
        raise ValueError("every covariate vector must have the length of beta")
    return n, p


def _weights(X, beta):
    """exp(x_i' beta - c), with c the largest linear predictor; the integer 1 when beta = 0.

    The shift c cancels in every ratio of the partial likelihood, so it changes
    nothing but prevents overflow.
    """
    if all(b == 0 for b in beta):
        return [1] * len(X)
    eta = [sum(float(a) * float(b) for a, b in zip(x, beta)) for x in X]
    c = max(eta)
    return [math.exp(e - c) for e in eta]


def _groups(times, events):
    """Distinct times from the largest to the smallest, with all subjects and the events at each."""
    order = sorted(range(len(times)), key=lambda k: times[k], reverse=True)  # @line L1
    out, i = [], 0
    while i < len(order):
        t, members, dead = times[order[i]], [], []
        while i < len(order) and times[order[i]] == t:
            members.append(order[i])
            if events[order[i]]:
                dead.append(order[i])
            i += 1
        out.append((t, members, dead))
    return out


def _zero_vec(p):
    return [0] * p


def _zero_mat(p):
    return [[0] * p for _ in range(p)]


def _esp_derivatives(ws, xs, d, p):
    """e_d of the weights ws, with its gradient and Hessian in beta (Gail, Lubin and Rubinstein 1981).

    e_k is the sum over subsets of size k of the product of the weights. With
    w_i = exp(x_i' beta), the gradient of a product over a subset is that product
    times the sum of the x_i, which gives the recursions below.
    """
    E = [1] + [0] * d
    G = [_zero_vec(p) for _ in range(d + 1)]
    H = [_zero_mat(p) for _ in range(d + 1)]
    for w, x in zip(ws, xs):
        for k in range(d, 0, -1):
            e1, g1, h1 = E[k - 1], G[k - 1], H[k - 1]
            for a in range(p):
                for b in range(p):
                    H[k][a][b] += w * (x[a] * x[b] * e1 + x[a] * g1[b] + g1[a] * x[b] + h1[a][b])
            for a in range(p):
                G[k][a] += w * (x[a] * e1 + g1[a])
            E[k] += w * e1
    return E[d], G[d], H[d]


class Fit(NamedTuple):
    loglik: float  # log partial likelihood, up to the shift that cancels
    score: list  # U(beta), length p
    information: list  # I(beta) = minus the Hessian, p x p


def score_information(times: Sequence, events: Sequence[int], X: Sequence[Sequence], beta: Sequence, ties: str = "breslow") -> Fit:
    """Log partial likelihood, score vector and observed information at beta.

    Breslow and Efron: one sort and one backward pass with cumulative sums
    S0 = sum w, S1 = sum w x, S2 = sum w x x' over the risk set, O(n p^2) after
    the sort. Exact: the subset-sum recursion over each risk set with ties.
    """
    if ties not in TIES:
        raise ValueError(f"ties must be one of {TIES}")
    n, p = _check(times, events, X, beta)
    w = _weights(X, beta)
    eta_shift = None if all(b == 0 for b in beta) else [math.log(v) for v in w]
    # S0, S1, S2 are the sums over the subjects with y >= t.
    S0, S1, S2 = 0, _zero_vec(p), _zero_mat(p)  # @line L4
    seen = []  # subjects added so far, used only for exact ties
    ll, U, Imat = 0.0, _zero_vec(p), _zero_mat(p)
    for t, members, dead in _groups(times, events):  # @line L5
        # Every subject with y_i = t enters the risk set at t.
        for i in members:  # @line L6
            wi, xi = w[i], X[i]
            S0 += wi
            for a in range(p):
                S1[a] += wi * xi[a]
                for b in range(p):
                    S2[a][b] += wi * xi[a] * xi[b]
            seen.append(i)
        d = len(dead)  # @line L7
        if d == 0:
            continue
        s = [sum(X[i][a] for i in dead) for a in range(p)]  # sum of x over the events at t
        eta_dead = 0.0 if eta_shift is None else sum(eta_shift[i] for i in dead)
        for a in range(p):
            U[a] += s[a]
        if ties == "exact" and d > 1:
            E, G, H = _esp_derivatives([w[i] for i in seen], [X[i] for i in seen], d, p)
            ll += eta_dead - math.log(float(E))
            for a in range(p):
                U[a] -= Fraction(G[a]) / E if isinstance(E, int) else G[a] / E
                for b in range(p):
                    if isinstance(E, int):
                        Imat[a][b] += Fraction(H[a][b]) / E - Fraction(G[a] * G[b]) / (E * E)
                    else:
                        Imat[a][b] += H[a][b] / E - G[a] * G[b] / (E * E)
            continue
        if ties == "breslow" or d == 1:
            parts = [(S0, S1, S2, d)]  # with one event the three rules agree
        else:  # Efron: the r-th of the d events sees the risk set minus r/d of the dead
            D0 = sum(w[i] for i in dead)
            D1 = [sum(w[i] * X[i][a] for i in dead) for a in range(p)]
            D2 = [[sum(w[i] * X[i][a] * X[i][b] for i in dead) for b in range(p)] for a in range(p)]
            parts = []
            for r in range(d):
                f = Fraction(r, d)
                parts.append((S0 - f * D0, [S1[a] - f * D1[a] for a in range(p)],
                              [[S2[a][b] - f * D2[a][b] for b in range(p)] for a in range(p)], 1))
        ll += eta_dead
        for A0, A1, A2, m in parts:
            ll -= m * math.log(float(A0))
            A0q = Fraction(A0) if isinstance(A0, (int, Fraction)) else A0
            for a in range(p):
                U[a] -= m * A1[a] / A0q
                for b in range(p):
                    Imat[a][b] += m * (A2[a][b] / A0q - A1[a] * A1[b] / (A0q * A0q))
    return Fit(ll, U, Imat)


def solve(A, b):
    """Solve A z = b by Gaussian elimination with partial pivoting (works with floats or Fractions)."""
    m = len(b)
    M = [list(A[i]) + [b[i]] for i in range(m)]
    for c in range(m):
        piv = max(range(c, m), key=lambda r: abs(M[r][c]))
        if M[piv][c] == 0:
            raise ZeroDivisionError("the information matrix is singular")
        M[c], M[piv] = M[piv], M[c]
        for r in range(c + 1, m):
            f = M[r][c] / M[c][c]
            for k in range(c, m + 1):
                M[r][k] -= f * M[c][k]
    z = [0] * m
    for r in range(m - 1, -1, -1):
        z[r] = (M[r][m] - sum(M[r][k] * z[k] for k in range(r + 1, m))) / M[r][r]
    return z


def inverse(A):
    m = len(A)
    cols = [solve(A, [1 if i == j else 0 for i in range(m)]) for j in range(m)]
    return [[cols[j][i] for j in range(m)] for i in range(m)]


class CoxResult(NamedTuple):
    beta: list
    loglik: float
    information: list  # observed information at beta-hat
    covariance: list  # its inverse, the usual variance estimate of beta-hat
    iterations: int
    converged: bool  # False when Newton did not settle, as under a monotone likelihood


def fit(times, events, X, ties="breslow", beta0=None, tol=1e-10, max_iter=60) -> CoxResult:
    """Maximize the log partial likelihood by Newton's method with step halving.

    Stops when the largest step is below tol. The log partial likelihood is
    concave, so a step that does not decrease it is accepted, and halving
    always finds one while the score is not zero. Under a monotone likelihood
    (no finite maximum) the iterates drift to infinity and converged is False.
    """
    n, p = _check(times, events, X, [0] * (len(X[0]) if X else 0))
    beta = [float(b) for b in (beta0 if beta0 is not None else [0.0] * p)]  # @line L2
    cur = score_information(times, events, X, beta, ties)
    for it in range(1, max_iter + 1):  # @line L3
        try:
            step = [float(v) for v in solve([[float(v) for v in row] for row in cur.information], [float(u) for u in cur.score])]  # @line L8
        except ZeroDivisionError:
            return CoxResult(beta, cur.loglik, cur.information, None, it, False)
        for _ in range(60):  # step halving
            cand = [b + s for b, s in zip(beta, step)]
            new = score_information(times, events, X, cand, ties)
            if new.loglik >= cur.loglik - 1e-12 * (1 + abs(cur.loglik)):
                break
            step = [s / 2 for s in step]
        beta, cur = cand, new  # @line L9
        if max(abs(s) for s in step) < tol:  # @line L10
            info = [[float(v) for v in row] for row in cur.information]
            return CoxResult(beta, cur.loglik, info, inverse(info), it, True)  # @line L11
    info = [[float(v) for v in row] for row in cur.information]
    try:
        cov = inverse(info)
    except ZeroDivisionError:
        cov = None
    return CoxResult(beta, cur.loglik, info, cov, max_iter, False)


def score_test(times, events, X, beta0=None, ties="breslow"):
    """Score test of beta = beta0: returns (U' I^-1 U, p, upper chi-square p-value)."""
    p = len(X[0])
    beta0 = beta0 if beta0 is not None else [0] * p
    f = score_information(times, events, X, beta0, ties)
    z = solve(f.information, f.score)
    stat = sum(u * v for u, v in zip(f.score, z))
    return stat, p, chi2_sf(float(stat), p)


def schoenfeld_residuals(times, events, X, beta, ties="breslow"):
    """One residual per event: x_i minus the risk-set weighted mean of x at its time.

    With ties='efron' the mean is the average over r = 0..d-1 of the Efron
    means, so that the residuals add up to the Efron score. Returns a list of
    (time, subject index, residual vector) in increasing time.
    """
    if ties not in ("breslow", "efron"):
        raise ValueError("ties must be 'breslow' or 'efron'")
    n, p = _check(times, events, X, beta)
    w = _weights(X, beta)
    S0, S1, out = 0, _zero_vec(p), []
    for t, members, dead in _groups(times, events):
        for i in members:
            S0 += w[i]
            for a in range(p):
                S1[a] += w[i] * X[i][a]
        d = len(dead)
        if d == 0:
            continue
        if ties == "breslow" or d == 1:
            S0q = Fraction(S0) if isinstance(S0, int) else S0
            mean = [S1[a] / S0q for a in range(p)]
        else:
            D0 = sum(w[i] for i in dead)
            D1 = [sum(w[i] * X[i][a] for i in dead) for a in range(p)]
            mean = [0] * p
            for r in range(d):
                f = Fraction(r, d)
                A0 = S0 - f * D0
                for a in range(p):
                    mean[a] += (S1[a] - f * D1[a]) / A0 / d
        for i in sorted(dead):
            out.append((t, i, [X[i][a] - mean[a] for a in range(p)]))
    out.sort(key=lambda r: (r[0], r[1]))
    return out


def scaled_schoenfeld(times, events, X, beta, covariance, ties="breslow"):
    """Grambsch and Therneau (1994) scaled residuals beta + D * covariance * r, with D the number of events."""
    res = schoenfeld_residuals(times, events, X, beta, ties)
    D = len(res)
    out = []
    for t, i, r in res:
        out.append((t, i, [beta[a] + D * sum(covariance[a][b] * r[b] for b in range(len(r))) for a in range(len(r))]))
    return out
