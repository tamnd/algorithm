# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dqds-algorithm/. The authors are listed in prov/BE4Y2X.jsonl.
"""The dqds algorithm (differential quotient-difference with shifts) for the
singular values of an upper bidiagonal matrix, in the positive qd form
q_k = a_k^2, e_k = b_k^2. Python standard library only.

singular_values(a, b) returns (sigma, stats) with sigma[0] >= ... >= sigma[n-1] >= 0.
"""
import math

U = 2.0 ** -53


def dqds_step(q, e, n, tau):
    """One dqds transform of the leading n entries with shift tau.

    Returns (qh, eh, dmin) on success, or None if a new q would be <= 0 or a d < 0,
    which means tau is not below the smallest eigenvalue."""
    qh, eh = [0.0] * n, [0.0] * (n - 1)
    d = q[0] - tau  # @line L4
    dmin = d
    for k in range(n - 1):  # @line L5
        if d < 0:
            return None
        qh[k] = d + e[k]  # @line L6
        if qh[k] == 0.0:  # zero block boundary: e_k = 0 and d = 0
            eh[k] = 0.0
            d = q[k + 1] - tau
        else:
            t = q[k + 1] / qh[k]
            eh[k] = e[k] * t  # @line L7
            d = d * t - tau  # @line L8
        dmin = min(dmin, d)
    if d < 0:
        return None
    qh[n - 1] = d  # @line L9
    return qh, eh, dmin


def newton_shift(q, e, n):
    """Newton step for det(B B^T - x I) from x = 0: 1 / trace((B B^T)^-1) = 1 / ||B^-1||_F^2.

    Since every eigenvalue is real and positive, this is a lower bound for the
    smallest one. The column norms c_j of B^-1 satisfy c_1 = 1 / q_1 and
    c_j = (1 + e_j-1 c_j-1) / q_j, all with positive terms."""
    c = 1.0 / q[0]
    total = c
    for j in range(1, n):
        c = (1.0 + e[j - 1] * c) / q[j]
        total += c
    return 1.0 / total


def singular_values(a, b, max_steps_per_value=60):
    """Singular values of the bidiagonal matrix with diagonal a and superdiagonal b."""
    q = [float(x) * float(x) for x in a]  # @line L1
    e = [float(x) * float(x) for x in b]
    n = len(q)
    stats = {"steps": 0, "failures": 0}
    sigma2 = []
    shift = 0.0
    limit = max_steps_per_value * max(n, 1)
    while n > 0:
        if n == 1:
            sigma2.append(shift + q[0])
            break
        if e[n - 2] <= U * U * (shift + q[n - 1]) or e[n - 2] == 0.0:  # @line L2
            sigma2.append(shift + q[n - 1])
            n -= 1
            continue
        if stats["steps"] >= limit:
            raise ArithmeticError("dqds did not converge")
        # Newton's lower bound for the smallest eigenvalue; tau = 0 if B is singular
        tau = newton_shift(q, e, n) if min(q[:n]) > 0.0 else 0.0  # @line L3
        out = dqds_step(q, e, n, tau)
        if out is None:  # tau was not below the smallest eigenvalue after rounding
            stats["failures"] += 1
            tau = 0.0
            out = dqds_step(q, e, n, tau)
        qh, eh, _ = out
        q[:n], e[:n - 1] = qh, eh
        shift += tau  # @line L10
        stats["steps"] += 1
    sigma = sorted((math.sqrt(max(s, 0.0)) for s in sigma2), reverse=True)  # @line L11
    return sigma, stats
