# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/representer-method/. The authors are listed in prov/6YYQY7.jsonl.

"""The representer method for weak-constraint variational assimilation.

Notation of Ide, Courtier, Ghil and Lorenc (1997). The window has the time
levels 0..K, the model is linear with model error, x_k = M_k x_(k-1) + eta_k,
and the cost is

    J = 1/2 (x_0 - x^b)^T B^-1 (x_0 - x^b) + sum_k 1/2 eta_k^T Q_k^-1 eta_k
      + 1/2 (y - H x)^T R^-1 (y - H x),

where y stacks all the scalar observations y_i = h_i^T x_(k_i) + e_i and R
is their error covariance. The minimizer is the first guess (the model run
from x^b with no model error) plus a combination sum_i beta_i r_i of the
representers r_i, one per observation. The representer r_i is found by one
adjoint run forced by h_i at time k_i and one forward run forced by B and
Q_k times the adjoint variable. The coefficients solve (P + R) beta = d,
with P_ji = h_j^T r_i(k_j) and d the innovation of the first guess.

The model is given by two functions:
    step(k, x)        M_k x, for x = x_(k-1)
    adjoint(k, lam)   M_k^T lam
B, Q[k] (k = 1..K, Q[0] is not used), the observation operators and the data
may hold Fraction entries; then every result is exact.
"""

import scimat


def observation_list(obs):
    """Return [(k_i, h_i, y_i)] for obs = {k: (H_k, y_k, R_k)} and the block diagonal R."""
    items = []
    blocks = []
    for k in sorted(obs):
        H, y, R = obs[k]
        for row, value in zip(H, y):
            items.append((k, row, value))
        blocks.append(R)
    p = len(items)
    Rall = scimat.zeros(p)
    i = 0
    for R in blocks:
        for a in range(len(R)):
            for b in range(len(R)):
                Rall[i + a][i + b] = R[a][b]
        i += len(R)
    return items, Rall


def backward(forcing, adjoint, K, n):
    """Return [lam_0, ..., lam_K] with lam_k = M_(k+1)^T lam_(k+1) + forcing at time k."""
    lam = [None] * (K + 1)
    v = [0] * n
    for k in range(K, -1, -1):
        if k in forcing:
            v = scimat.add(v, forcing[k])
        lam[k] = v
        if k > 0:
            v = adjoint(k, v)
    return lam


def forward(start, lam, B, Q, step, K):
    """Return [x_0, ..., x_K] with x_0 = start + B lam_0 and x_k = M_k x_(k-1) + Q_k lam_k."""
    xs = [scimat.add(start, scimat.matvec(B, lam[0]))]
    for k in range(1, K + 1):
        xs.append(scimat.add(step(k, xs[-1]), scimat.matvec(Q[k], lam[k])))
    return xs


def representer_method(xb, B, Q, obs, step, adjoint, K):
    """Return (estimate [x_0, ..., x_K], beta, representer matrix P)."""
    n = len(xb)
    items, R = observation_list(obs)
    p = len(items)
    zero = [0] * n
    first = [list(xb)]  # @line L1
    for k in range(1, K + 1):
        first.append(step(k, first[-1]))
    P = scimat.zeros(p)
    for i, (ki, hi, _) in enumerate(items):  # @line L2
        lam = backward({ki: list(hi)}, adjoint, K, n)  # @line L3
        r = forward(zero, lam, B, Q, step, K)  # @line L4
        for j, (kj, hj, _) in enumerate(items):  # @line L5
            P[j][i] = scimat.dot(hj, r[kj])
    d = [yi - scimat.dot(hi, first[ki]) for ki, hi, yi in items]  # @line L6
    beta = scimat.solve(scimat.add(P, R), d)  # @line L7
    forcing = {}
    for (ki, hi, _), bi in zip(items, beta):  # @line L8
        forcing[ki] = scimat.add(forcing.get(ki, zero), scimat.scale(bi, hi))
    lam = backward(forcing, adjoint, K, n)
    estimate = forward(list(xb), lam, B, Q, step, K)  # @line L9
    return estimate, beta, P  # @line L10


def linear_model(M):
    """Return (step, adjoint) for the linear model x_k = M x_(k-1)."""
    Mt = scimat.transpose(M)
    return (lambda k, x: scimat.matvec(M, x), lambda k, lam: scimat.matvec(Mt, lam))
