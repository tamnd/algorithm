# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/variational-bayes-blind-deconvolution/. The authors are listed in prov/JZ0W9B.jsonl.
"""Blind deconvolution by variational Bayes in the gradient domain.

The model follows Fergus et al. (2006) in one dimension, with the kernel as a
point estimate as in Levin et al. (2011). On a periodic grid of n points,

    d = k * g + e,   e ~ N(0, sigma2 I),

where d is the gradient of the blurred signal, g the unknown gradient of the
sharp signal and k the unknown kernel (centered at index 0, k >= 0, zero
outside a support, sum 1). Each g_i is drawn from a mixture of zero mean
Gaussians with weights pi_j and variances v_j, through a hidden label z_i.

The method maximizes the free energy (the evidence lower bound)

    F(q, k) = E_q[log p(d, g, z | k)] + H[q],   q(g, z) = q(g) q(z),

by exact coordinate steps: q(g) is a full Gaussian N(mu, S), q(z) is a table
of label probabilities r[i][j], and k minimizes the expected misfit
E_q ||d - k * g||^2, which includes the covariance S of g. Dropping S gives
the "naive" joint estimate, which the tests compare with.
"""

import math
from itertools import combinations

from imgla import cho_solve, cholesky, solve


def gradient(y):
    """Periodic forward difference: d_i = y_{i+1} - y_i."""
    n = len(y)
    return [y[(i + 1) % n] - y[i] for i in range(n)]


def conv(k, g):
    """(k * g)_r = sum_s k_s g_{r - s}, indices modulo n."""
    n = len(g)
    return [sum(k[s] * g[(r - s) % n] for s in range(n) if k[s] != 0) for r in range(n)]


def kernel_matrix(k):
    """The circulant matrix K with K g = k * g."""
    n = len(k)
    return [[k[(r - c) % n] for c in range(n)] for r in range(n)]


def update_q_g(d, k, w, sigma2):
    """The optimal Gaussian q(g) = N(mu, S) for fixed q(z) (precisions w) and k.

    S^{-1} = K^T K / sigma2 + diag(w), mu = S K^T d / sigma2.
    Returns (mu, S, logdet of S^{-1}).
    """
    n = len(d)
    km = kernel_matrix(k)
    prec = [[sum(km[r][a] * km[r][b] for r in range(n)) / sigma2 for b in range(n)] for a in range(n)]
    for i in range(n):
        prec[i][i] += w[i]
    low = cholesky(prec)
    ktd = [sum(km[r][a] * d[r] for r in range(n)) / sigma2 for a in range(n)]
    mu = cho_solve(low, ktd)
    cols = [cho_solve(low, [1.0 if i == j else 0.0 for i in range(n)]) for j in range(n)]
    cov = [[cols[j][i] for j in range(n)] for i in range(n)]
    logdet = 2.0 * sum(math.log(low[i][i]) for i in range(n))
    return mu, cov, logdet


def second_moments(mu, cov, use_cov=True):
    """E[g_i^2] = mu_i^2 + S_ii (or mu_i^2 alone for the naive estimate)."""
    return [m * m + (cov[i][i] if use_cov else 0.0) for i, m in enumerate(mu)]


def update_q_z(m2, pi, v):
    """Label probabilities r[i][j] proportional to pi_j N-density with variance v_j at E[g_i^2].

    Returns (r, w) with w_i = sum_j r[i][j] / v_j, the expected precision of g_i.
    """
    r, w = [], []
    for e in m2:
        logs = [math.log(p) - 0.5 * math.log(vj) - e / (2.0 * vj) for p, vj in zip(pi, v)]
        top = max(logs)
        ex = [math.exp(t - top) for t in logs]
        s = sum(ex)
        ri = [t / s for t in ex]
        r.append(ri)
        w.append(sum(a / vj for a, vj in zip(ri, v)))
    return r, w


def kernel_quadratic(d, mu, cov, support, use_cov=True):
    """A and b with E_q ||d - k * g||^2 = k^T A k - 2 b^T k + const over the support offsets."""
    n = len(d)
    a = [[0.0] * len(support) for _ in support]
    b = [0.0] * len(support)
    for p, s in enumerate(support):
        b[p] = sum(d[r] * mu[(r - s) % n] for r in range(n))
        for q, t in enumerate(support):
            val = sum(mu[(r - s) % n] * mu[(r - t) % n] for r in range(n))
            if use_cov:
                val += sum(cov[(r - s) % n][(r - t) % n] for r in range(n))
            a[p][q] = val
    return a, b


def simplex_qp(a, b, ridge=1e-12):
    """Exact minimizer of k^T A k - 2 b^T k over k >= 0, sum k = 1 (A symmetric PSD).

    The minimizer lies in the relative interior of some face of the simplex. For
    each face (a nonempty subset T of the coordinates) solve the problem with the
    equality constraints only, keep the solutions with k_T >= 0, and return the best.
    """
    m = len(b)
    best, best_val = None, math.inf
    for size in range(1, m + 1):
        for t in combinations(range(m), size):
            # KKT system: 2 A_TT k_T + lam 1 = 2 b_T, 1^T k_T = 1.
            mat = [[2.0 * a[i][j] + (2.0 * ridge if i == j else 0.0) for j in t] + [1.0] for i in t]
            mat.append([1.0] * size + [0.0])
            rhs = [2.0 * b[i] for i in t] + [1.0]
            try:
                sol = solve(mat, rhs)
            except ValueError:
                continue
            if min(sol[:size]) < -1e-12:
                continue
            k = [0.0] * m
            for i, v in zip(t, sol[:size]):
                k[i] = max(v, 0.0)
            tot = sum(k)
            k = [v / tot for v in k]
            val = sum(k[i] * a[i][j] * k[j] for i in range(m) for j in range(m)) - 2.0 * sum(bi * ki for bi, ki in zip(b, k))
            if val < best_val:
                best, best_val = k, val
    return best


def free_energy(d, k, mu, cov, logdet_prec, r, pi, v, sigma2):
    """F = E_q[log p(d | g, k)] + E_q[log p(g | z)] + E_q[log p(z)] + H[q(g)] + H[q(z)]."""
    n = len(d)
    km = kernel_matrix(k)
    res = [di - sum(km[i][j] * mu[j] for j in range(n)) for i, di in enumerate(d)]
    ksk = sum(km[i][a] * cov[a][b] * km[i][b] for i in range(n) for a in range(n) for b in range(n) if km[i][a] and km[i][b])
    lik = -0.5 * n * math.log(2 * math.pi * sigma2) - (sum(t * t for t in res) + ksk) / (2 * sigma2)
    m2 = second_moments(mu, cov)
    prior = 0.0
    ent_z = 0.0
    for e, ri in zip(m2, r):
        for p, vj, rij in zip(pi, v, ri):
            if rij > 0:
                prior += rij * (math.log(p) - 0.5 * math.log(2 * math.pi * vj) - e / (2 * vj))
                ent_z -= rij * math.log(rij)
    ent_g = 0.5 * n * math.log(2 * math.pi * math.e) - 0.5 * logdet_prec
    return lik + prior + ent_g + ent_z


def embed(kv, support, n):
    """The full length n kernel with values kv at the support offsets (taken modulo n)."""
    k = [0.0] * n
    for s, val in zip(support, kv):
        k[s % n] += val
    return k


def vb_blind(d, k0, support, pi, v, sigma2, iters=20, use_cov=True, history=None):
    """Variational EM for the kernel. Returns (k, mu, cov) with k of length n.

    k0: the start kernel on the support offsets. use_cov=False gives the naive
    estimate, which ignores the uncertainty of g. If history is a list, the
    free energy after each of the three steps is appended (for use_cov=True).
    """
    n = len(d)
    track = history is not None and use_cov
    k = embed(k0, support, n)  # @line L1
    w = [sum(p / vj for p, vj in zip(pi, v))] * n  # @line L2
    r = mu = cov = None
    for it in range(iters):  # @line L3
        mu, cov, logdet = update_q_g(d, k, w, sigma2)  # @line L4
        if track and it > 0:
            history.append(free_energy(d, k, mu, cov, logdet, r, pi, v, sigma2))
        r, w = update_q_z(second_moments(mu, cov, use_cov), pi, v)  # @line L5
        if track:
            history.append(free_energy(d, k, mu, cov, logdet, r, pi, v, sigma2))
        a, b = kernel_quadratic(d, mu, cov, support, use_cov)  # @line L6
        k = embed(simplex_qp(a, b), support, n)  # @line L7
        if track:
            history.append(free_energy(d, k, mu, cov, logdet, r, pi, v, sigma2))
    return k, mu, cov  # @line L8
