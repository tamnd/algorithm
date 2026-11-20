# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ensemble-adjustment-kalman-filter/. The authors are listed in prov/NP9ZCK.jsonl.

"""Ensemble adjustment Kalman filter (EAKF) of Anderson (2001, 2003).

Notation of Ide, Courtier, Ghil and Lorenc (1997). The forecast ensemble has
N members in R^n; the observations y^o have error variances r_k.

eakf_serial is the two step form of Anderson (2003) used in practice: for
each scalar observation, adjust the ensemble of the predicted observation so
that it has the Gaussian posterior mean and variance, then regress the
increments onto every state value and every other predicted observation.

eakf_joint is the matrix form of Anderson (2001, Appendix A): with
P = F D F^T (the nonzero eigenvalues only), G = D^(1/2) and
G F^T H^T R^-1 H F G = U Lam U^T, the adjustment matrix
A = F G U (I + Lam)^(-1/2) U^T G^-1 F^T maps each forecast perturbation to
an analysis perturbation, and A P A^T is the Kalman analysis covariance.

Costs: eakf_serial O(p N (n + p)); eakf_joint O(n^3 + n^2 (N + p) + p^3) with
a fixed number of Jacobi sweeps.
"""

import math

import scimat


def eakf_serial(ens, yo, h, r_var, loc_state=None, loc_obs=None):
    """Return the analysis ensemble of the serial EAKF (a list of N members).

    h(x) is evaluated once per member. loc_state[k][j] and loc_obs[k][l] are
    optional weights that multiply the regression coefficients.
    """
    N, n, p = len(ens), len(ens[0]), len(yo)
    x = [list(m) for m in ens]
    y = [list(h(m)) for m in ens]  # @line L1
    for k in range(p):  # @line L2
        yk = [y[i][k] for i in range(N)]
        ybar = sum(yk) / N  # @line L3
        s = sum((v - ybar) ** 2 for v in yk) / (N - 1)
        if s == 0.0:
            continue
        sa = 1.0 / (1.0 / s + 1.0 / r_var[k])  # @line L4
        ya = sa * (ybar / s + yo[k] / r_var[k])
        f = math.sqrt(sa / s)
        dy = [ya + f * (v - ybar) - v for v in yk]  # @line L5
        xbar = [sum(x[i][j] for i in range(N)) / N for j in range(n)]  # @line L6
        bx = [sum((x[i][j] - xbar[j]) * (yk[i] - ybar) for i in range(N)) / ((N - 1) * s) for j in range(n)]
        if loc_state is not None:
            bx = [b * w for b, w in zip(bx, loc_state[k])]
        ymean = [sum(y[i][l] for i in range(N)) / N for l in range(p)]  # @line L7
        by = [sum((y[i][l] - ymean[l]) * (yk[i] - ybar) for i in range(N)) / ((N - 1) * s) for l in range(p)]
        if loc_obs is not None:
            by = [b * w for b, w in zip(by, loc_obs[k])]
        for i in range(N):
            for j in range(n):
                x[i][j] += bx[j] * dy[i]
            for l in range(p):
                y[i][l] += by[l] * dy[i]
    return x  # @line L8


def sym_eig(a, tol=1e-14, max_sweeps=60):
    """Return (values, V) with a = V diag(values) V^T, by the cyclic Jacobi method."""
    n = len(a)
    a = [[float(v) for v in row] for row in a]
    v = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    for _ in range(max_sweeps):
        off = sum(a[p][q] ** 2 for p in range(n) for q in range(p + 1, n))
        diag = sum(a[p][p] ** 2 for p in range(n))
        if off <= tol * tol * diag or off == 0.0:
            break
        for p in range(n - 1):
            for q in range(p + 1, n):
                apq = a[p][q]
                if apq == 0.0:
                    continue
                theta = (a[q][q] - a[p][p]) / (2.0 * apq)
                t = (1.0 if theta >= 0 else -1.0) / (abs(theta) + math.sqrt(theta * theta + 1.0))
                cs = 1.0 / math.sqrt(t * t + 1.0)
                sn = t * cs
                for k in range(n):
                    akp, akq = a[k][p], a[k][q]
                    a[k][p] = cs * akp - sn * akq
                    a[k][q] = sn * akp + cs * akq
                for k in range(n):
                    apk, aqk = a[p][k], a[q][k]
                    a[p][k] = cs * apk - sn * aqk
                    a[q][k] = sn * apk + cs * aqk
                a[p][q] = 0.0
                a[q][p] = 0.0
                for k in range(n):
                    vkp, vkq = v[k][p], v[k][q]
                    v[k][p] = cs * vkp - sn * vkq
                    v[k][q] = sn * vkp + cs * vkq
    return [a[i][i] for i in range(n)], v


def adjustment_matrix(P, H, R, rel_tol=1e-10):
    """Return A = F G U (I + Lam)^(-1/2) U^T G^-1 F^T for the covariance P (n by n)."""
    n = len(P)
    d, V = sym_eig(P)  # @line J2
    top = max(d) if d else 0.0
    keep = [m for m in range(n) if d[m] > rel_tol * top]
    F = [[V[j][m] for m in keep] for j in range(n)]  # n by r
    g = [math.sqrt(d[m]) for m in keep]
    FG = [[F[j][a] * g[a] for a in range(len(keep))] for j in range(n)]
    B = scimat.matmul(H, FG)  # @line J3
    M = scimat.matmul(scimat.transpose(B), scimat.solve(R, B))
    lam, U = sym_eig(M) if keep else ([], [])
    rr = len(keep)
    core = [[sum(U[a][m] * U[b][m] / math.sqrt(1.0 + lam[m]) for m in range(rr)) for b in range(rr)] for a in range(rr)]
    right = [[F[j][b] / g[b] for b in range(rr)] for j in range(n)]  # F G^-1, so the last factor is right^T
    return scimat.matmul(scimat.matmul(FG, core), scimat.transpose(right))  # @line J4


def eakf_joint(ens, yo, H, R):
    """Return the analysis ensemble of the joint EAKF for a linear H (p by n) and a covariance R."""
    N, n = len(ens), len(ens[0])
    xbar = [sum(x[j] for x in ens) / N for j in range(n)]  # @line J1
    X = [[x[j] - xbar[j] for j in range(n)] for x in ens]
    P = [[sum(X[i][a] * X[i][b] for i in range(N)) / (N - 1) for b in range(n)] for a in range(n)]
    A = adjustment_matrix(P, H, R)
    PHt = scimat.matmul(P, scimat.transpose(H))  # @line J5
    S = scimat.add(scimat.matmul(H, PHt), R)
    z = scimat.solve(S, scimat.sub(yo, scimat.matvec(H, xbar)))
    xa = scimat.add(xbar, scimat.matvec(PHt, z))
    return [scimat.add(xa, scimat.matvec(A, X[i])) for i in range(N)]  # @line J6


def ensemble_moments(ens):
    """Return (mean, P): the ensemble mean and the sample covariance with divisor N - 1."""
    N, n = len(ens), len(ens[0])
    mean = [sum(x[j] for x in ens) / N for j in range(n)]
    P = [[sum((x[a] - mean[a]) * (x[b] - mean[b]) for x in ens) / (N - 1) for b in range(n)] for a in range(n)]
    return mean, P
