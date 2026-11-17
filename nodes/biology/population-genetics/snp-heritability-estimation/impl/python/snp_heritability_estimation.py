# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/snp-heritability-estimation/. The authors are listed in prov/Q44QVJ.jsonl.
"""SNP heritability by REML with the average information algorithm.

The model for n individuals is

    y = X beta + g_1 + ... + g_r + e,   g_i ~ N(0, s_i A_i),   e ~ N(0, s_e I),

so Var(y) = V = s_1 A_1 + ... + s_r A_r + s_e I. Each A_i is a genomic
relationship matrix (one for all SNPs gives the usual GREML model). The
SNP heritability is h2 = (s_1 + ... + s_r) / (s_1 + ... + s_r + s_e).

The variance components theta = (s_1, ..., s_r, s_e) maximize the restricted
log-likelihood

    l_R = -1/2 [ log det V + log det(X^T V^-1 X) + y^T P y ] + const,
    P = V^-1 - V^-1 X (X^T V^-1 X)^-1 X^T V^-1.

With V_k the derivative of V in theta_k (A_k, or I for s_e), the score is
    d_k = -1/2 [ tr(P V_k) - y^T P V_k P y ],
and the average information matrix is
    AI_kl = 1/2 y^T P V_k P V_l P y.
The update is theta <- theta + AI^-1 d (Gilmour, Thompson and Cullis 1995).
The first iteration is one EM-REML step, which is slower but stays positive.
"""

from __future__ import annotations

import math
from typing import Dict, List, Sequence

from pg4lmm import chol_inverse, chol_logdet, cholesky, dot, inverse_small, matvec, solve_small


def _reml_parts(As, y, X, theta):
    """P, P y and l_R (without the constant) at theta."""
    n, p = len(y), len(X[0])
    r = len(As)
    V = [[theta[r] if i == j else 0.0 for j in range(n)] for i in range(n)]
    for k in range(r):
        sk, Ak = theta[k], As[k]
        for i in range(n):
            Vi, Aki = V[i], Ak[i]
            for j in range(n):
                Vi[j] += sk * Aki[j]
    L = cholesky(V)
    Vinv = chol_inverse(L)
    VX = [[dot(Vinv[i], [X[t][a] for t in range(n)]) for a in range(p)] for i in range(n)]
    C = [[sum(X[t][a] * VX[t][b] for t in range(n)) for b in range(p)] for a in range(p)]
    Cinv = inverse_small(C)
    LC = cholesky(C)
    # P = Vinv - VX Cinv VX^T
    VXC = [[sum(VX[i][a] * Cinv[a][b] for a in range(p)) for b in range(p)] for i in range(n)]
    P = [[Vinv[i][j] - dot(VXC[i], VX[j]) for j in range(n)] for i in range(n)]
    Py = matvec(P, y)
    loglik = -0.5 * (chol_logdet(L) + chol_logdet(LC) + dot(y, Py))
    return P, Py, loglik


def reml_loglik(As, y, X, theta) -> float:
    """The restricted log-likelihood at theta = (s_1, ..., s_r, s_e), up to a constant."""
    return _reml_parts(As, y, X, theta)[2]


def greml(As: Sequence[Sequence[Sequence[float]]], y: Sequence[float], X,
          tol: float = 1e-10, max_iter: int = 200) -> Dict[str, object]:
    """REML estimates of the variance components and the SNP heritability.

    As is a list of r relationship matrices (n by n), X is n by p with full
    column rank. Returns a dict with theta, h2, its standard error se_h2,
    the inverse AI matrix, the log-likelihood and the number of iterations.
    """
    n, p = len(y), len(X[0])
    r = len(As)
    if n <= p:
        raise ValueError("need more individuals than covariates")
    mean = sum(y) / n
    vp = sum((v - mean) ** 2 for v in y) / (n - 1)
    theta = [vp / (r + 1)] * (r + 1)  # @line L1
    floor = 1e-6 * vp
    Vk = list(As) + [None]  # None stands for the identity
    P, Py, loglik = _reml_parts(As, y, X, theta)  # @line L2
    it = 0
    for it in range(1, max_iter + 1):
        VPy = [Py if M is None else matvec(M, Py) for M in Vk]
        PVPy = [matvec(P, u) for u in VPy]
        tr = [sum(P[i][i] for i in range(n)) if M is None
              else sum(dot(P[i], M[i]) for i in range(n)) for M in Vk]
        quad = [dot(Py, u) for u in VPy]
        score = [-0.5 * (tr[k] - quad[k]) for k in range(r + 1)]  # @line L3
        AI = [[0.5 * dot(VPy[k], PVPy[l]) for l in range(r + 1)] for k in range(r + 1)]  # @line L4
        if it == 1:
            # One EM-REML step: s_k <- s_k + s_k^2 (y'P V_k P y - tr(P V_k)) / n.
            step = [theta[k] ** 2 * (quad[k] - tr[k]) / n for k in range(r + 1)]
        else:
            step = solve_small(AI, score)  # @line L5
        # Keep the components above the floor and V positive definite, and do
        # not let l_R go down: halve the step until both hold.
        for _ in range(60):
            new = [max(theta[k] + step[k], floor) for k in range(r + 1)]
            try:
                parts = _reml_parts(As, y, X, new)
            except ValueError:
                parts = None
            if parts is not None and parts[2] >= loglik - 1e-12 * abs(loglik):
                break
            step = [v / 2.0 for v in step]
        else:
            break
        gain = parts[2] - loglik
        theta = new  # @line L6
        P, Py, loglik = parts
        if abs(gain) < tol:
            break
    VPy = [Py if M is None else matvec(M, Py) for M in Vk]
    PVPy = [matvec(P, u) for u in VPy]
    AI = [[0.5 * dot(VPy[k], PVPy[l]) for l in range(r + 1)] for k in range(r + 1)]
    AIinv = inverse_small(AI)
    sg = sum(theta[:r])
    total = sg + theta[r]
    h2 = sg / total  # @line L7
    # Delta method: dh2/ds_k = s_e / total^2 for k < r, and -sg / total^2 for s_e.
    grad = [theta[r] / total ** 2] * r + [-sg / total ** 2]
    var = sum(grad[a] * AIinv[a][b] * grad[b] for a in range(r + 1) for b in range(r + 1))
    return {"theta": theta, "h2": h2, "se_h2": math.sqrt(max(var, 0.0)),
            "AIinv": AIinv, "loglik": loglik, "iterations": it}  # @line L8
