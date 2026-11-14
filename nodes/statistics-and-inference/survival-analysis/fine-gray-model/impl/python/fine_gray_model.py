# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fine-gray-model/. The authors are listed in prov/YSYJCC.jsonl.
"""Fine-Gray proportional subdistribution hazards model, fitted by weighted Cox Newton steps.

Input: times[i] = y_i, causes[i] = 0 (censored) or k >= 1 (event of cause k)
and covariate rows X[i]. For the cause of interest, a subject with another
cause stays in the risk set after its event time y_i with the weight
G(t-) / G(y_i-), where G is the Kaplan-Meier estimate of the censoring
distribution (censorings at a tied time come after the events). Ties of the
cause of interest use the Breslow rule. The weighted sums of a Newton step
are a backward cumulative sum (subjects still at risk) plus G(t-) times a
forward cumulative sum (subjects with another cause before t), so a step
costs O(n p^2) after one sort, plus O(p^3) for the solve.
"""

import math
from collections.abc import Sequence
from fractions import Fraction
from typing import NamedTuple


def censoring_survival(times: Sequence, causes: Sequence[int]) -> list[tuple]:
    """Kaplan-Meier (u, G(u)) of the censoring time; events at u leave before the censorings at u."""
    out, G = [], Fraction(1)
    order = sorted(range(len(times)), key=lambda i: times[i])
    at_risk, i, n = len(times), 0, len(times)
    while i < n:
        u, c, d = times[order[i]], 0, 0
        while i < n and times[order[i]] == u:
            if causes[order[i]] == 0:
                c += 1
            else:
                d += 1
            i += 1
        if c:
            G *= Fraction(at_risk - d - c, at_risk - d)
            out.append((u, G))
        at_risk -= c + d
    return out


def _left_limit(steps: list[tuple], t):
    """G(t-): the value at the last censoring time strictly before t, and 1 before the first."""
    value = Fraction(1)
    for u, g in steps:
        if u >= t:
            break
        value = g
    return value


class Design(NamedTuple):
    order: list  # subjects by increasing time
    event_times: list  # distinct times of the cause of interest, increasing
    g_event: list  # G(t_j-) at each of them
    g_subject: list  # G(y_i-) for every subject (used for the other causes)


def _design(times, causes, cause):
    n = len(times)
    if n == 0 or len(causes) != n:
        raise ValueError("times and causes must have the same positive length")
    if any(not isinstance(c, int) or c < 0 for c in causes):
        raise ValueError("causes must be integers >= 0 (0 = censored)")
    G = censoring_survival(times, causes)
    order = sorted(range(n), key=lambda i: times[i])
    ev = sorted(set(times[i] for i in range(n) if causes[i] == cause))
    return Design(order, ev, [_left_limit(G, t) for t in ev], [_left_limit(G, times[i]) for i in range(n)])


class Sums(NamedTuple):
    loglik: float
    score: list
    information: list
    risk_sums: list  # S0_j, the weighted risk set sums at the event times of interest


def weighted_sums(times, causes, X, beta, cause=1, design=None, exact=False) -> Sums:
    """The weighted log partial likelihood, its score and information at beta.

    With exact=True and beta = 0 everything is computed in Fractions (the
    log-likelihood is then None).
    """
    n, p = len(times), len(beta)
    des = design or _design(times, causes, cause)
    if exact:
        if any(b != 0 for b in beta):
            raise ValueError("exact arithmetic needs beta = 0")
        w = [1] * n
        conv = Fraction
    else:
        eta = [sum(a * b for a, b in zip(X[i], beta)) for i in range(n)]
        m = max(eta)
        w = [math.exp(e - m) for e in eta]
        conv = float
    zero = conv(0)

    def blank():
        return [zero, [zero] * p, [[zero] * p for _ in range(p)]]

    def add(acc, i, scale):
        ws = w[i] * scale
        acc[0] += ws
        for a in range(p):
            acc[1][a] += ws * X[i][a]
            for b in range(p):
                acc[2][a][b] += ws * X[i][a] * X[i][b]

    # Forward: subjects with another cause before t_j, each scaled by 1 / G(y_i-).
    # Backward: subjects with y_i >= t_j.
    k = len(des.event_times)
    fwd, back = [None] * k, [None] * k
    acc, pos = blank(), 0
    for j, t in enumerate(des.event_times):
        while pos < n and times[des.order[pos]] < t:
            i = des.order[pos]
            if causes[i] not in (0, cause):
                add(acc, i, conv(1) / conv(des.g_subject[i]))
            pos += 1
        fwd[j] = [acc[0], acc[1][:], [row[:] for row in acc[2]]]
    acc, pos = blank(), n - 1
    for j in range(k - 1, -1, -1):
        t = des.event_times[j]
        while pos >= 0 and times[des.order[pos]] >= t:
            add(acc, des.order[pos], conv(1))
            pos -= 1
        back[j] = [acc[0], acc[1][:], [row[:] for row in acc[2]]]
    ll = zero if not exact else None
    U = [zero] * p
    I = [[zero] * p for _ in range(p)]
    S0s = []
    dead = {}
    for i in range(n):
        if causes[i] == cause:
            dead.setdefault(times[i], []).append(i)
    for j, t in enumerate(des.event_times):
        g = conv(des.g_event[j])
        S0 = back[j][0] + g * fwd[j][0]
        S1 = [back[j][1][a] + g * fwd[j][1][a] for a in range(p)]
        S2 = [[back[j][2][a][b] + g * fwd[j][2][a][b] for b in range(p)] for a in range(p)]
        S0s.append(S0)
        d = len(dead[t])
        mean = [s / S0 for s in S1]
        for i in dead[t]:
            for a in range(p):
                U[a] += X[i][a] - mean[a]
            if not exact:
                ll += eta[i] - m - math.log(S0)
        for a in range(p):
            for b in range(p):
                I[a][b] += d * (S2[a][b] / S0 - mean[a] * mean[b])
    return Sums(ll, U, I, S0s)


def solve(A, b):
    """Gaussian elimination with partial pivoting; ZeroDivisionError if A is singular."""
    p = len(b)
    M = [list(map(float, A[r])) + [float(b[r])] for r in range(p)]
    for c in range(p):
        r = max(range(c, p), key=lambda q: abs(M[q][c]))
        if M[r][c] == 0.0:
            raise ZeroDivisionError("singular information matrix")
        M[c], M[r] = M[r], M[c]
        for q in range(c + 1, p):
            f = M[q][c] / M[c][c]
            for s in range(c, p + 1):
                M[q][s] -= f * M[c][s]
    x = [0.0] * p
    for c in range(p - 1, -1, -1):
        x[c] = (M[c][p] - sum(M[c][s] * x[s] for s in range(c + 1, p))) / M[c][c]
    return x


class FineGrayResult(NamedTuple):
    beta: list
    loglik: float
    information: list
    iterations: int
    converged: bool


def fit(times, causes, X, cause=1, beta0=None, tol=1e-10, max_iter=60) -> FineGrayResult:
    """Newton's method with step halving on the weighted log partial likelihood."""
    p = len(X[0])
    des = _design(times, causes, cause)
    if not des.event_times:
        raise ValueError("no event of the cause of interest")
    beta = list(beta0) if beta0 is not None else [0.0] * p
    cur = weighted_sums(times, causes, X, beta, cause, des)
    for it in range(1, max_iter + 1):
        try:
            step = solve(cur.information, cur.score)
        except ZeroDivisionError:
            return FineGrayResult(beta, cur.loglik, cur.information, it, False)
        scale = 1.0
        while True:
            trial = [b + scale * s for b, s in zip(beta, step)]
            new = weighted_sums(times, causes, X, trial, cause, des)
            if new.loglik >= cur.loglik - 1e-12 or scale < 1e-8:
                break
            scale /= 2.0  # step halving
        beta, cur = trial, new
        if max(abs(scale * s) for s in step) < tol:
            return FineGrayResult(beta, cur.loglik, cur.information, it, True)
    return FineGrayResult(beta, cur.loglik, cur.information, max_iter, False)


def baseline(times, causes, X, beta, cause=1) -> list[tuple]:
    """Breslow-type jumps of the baseline cumulative subdistribution hazard: (t_j, d_j / S0_j, cumulative).

    The weights use exp(x' beta) itself, not the shifted values of weighted_sums.
    """
    des = _design(times, causes, cause)
    exact = all(b == 0 for b in beta)
    sums = weighted_sums(times, causes, X, beta, cause, des, exact=exact)
    if not exact:
        m = max(sum(a * b for a, b in zip(x, beta)) for x in X)
        sums = sums._replace(risk_sums=[s * math.exp(m) for s in sums.risk_sums])
    out, H = [], 0
    for t, S0 in zip(des.event_times, sums.risk_sums):
        d = sum(1 for y, c in zip(times, causes) if c == cause and y == t)
        jump = Fraction(d) / S0 if exact else d / S0
        H += jump
        out.append((t, jump, H))
    return out


def predict_cif(steps: list[tuple], x: Sequence[float], beta: Sequence[float], t) -> float:
    """F_k(t | x) = 1 - exp(-Lambda0(t) exp(x' beta))."""
    H = 0.0
    for u, _, cum in steps:
        if u > t:
            break
        H = float(cum)
    return 1.0 - math.exp(-H * math.exp(sum(a * b for a, b in zip(x, beta))))
