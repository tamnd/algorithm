# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ensemble-transform-kalman-filter/. The authors are listed in prov/5GQ96N.jsonl.

"""Ensemble transform Kalman filter (ETKF), in the form of Hunt, Kostelich and Szunyogh (2007).

Notation of Ide, Courtier, Ghil and Lorenc (1997). The forecast ensemble has
N members x_1..x_N in R^n, the observations y^o in R^p have the error
covariance R, and h maps a state to R^p (it may be nonlinear).

X and Y hold the unscaled perturbations x_i - xbar and h(x_i) - ybar, so the
sample covariance is P^f = X X^T / (N - 1). The analysis works in the
N-dimensional ensemble space:

    A = (N - 1) / rho I + Y^T R^-1 Y = Q diag(lam) Q^T
    P~ = A^-1,  wbar = P~ Y^T R^-1 (y^o - ybar),  W = sqrt(N - 1) P~^(1/2)
    x^a_i = xbar + X (wbar + W_i)

W is the symmetric square root. rho multiplies the covariance, so the
perturbations grow by sqrt(rho). Cost: O(p^3 + p^2 N) for R^-1 Y with a dense
R, O(p N^2) for A, O(N^3) for the Jacobi eigendecomposition with a fixed
number of sweeps, and O(n N^2) for the update.
"""

import math

import scimat


def sym_eig(a, tol=1e-14, max_sweeps=60):
    """Return (values, V) with a = V diag(values) V^T, by the cyclic Jacobi method.

    a is a symmetric matrix (list of rows). The columns of V are orthonormal
    eigenvectors. The values are not sorted.
    """
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


def etkf_transform(Y, R, innov, rho=1.0):
    """Return (wbar, W) for the unscaled observation perturbations Y (p by N).

    innov = y^o - ybar. W is the symmetric matrix sqrt(N - 1) P~^(1/2).
    """
    N = len(Y[0])
    C = scimat.transpose(scimat.solve(R, Y))  # @line L3
    A = scimat.add(scimat.scale((N - 1) / rho, scimat.eye(N)), scimat.matmul(C, Y))  # @line L4
    lam, Q = sym_eig(A)  # @line L5
    Pt = [[sum(Q[a][m] * Q[b][m] / lam[m] for m in range(N)) for b in range(N)] for a in range(N)]  # @line L6
    W = [[sum(Q[a][m] * math.sqrt((N - 1) / lam[m]) * Q[b][m] for m in range(N)) for b in range(N)] for a in range(N)]
    wbar = scimat.matvec(Pt, scimat.matvec(C, innov))  # @line L7
    return wbar, W


def etkf_analysis(ens, yo, h, R, rho=1.0):
    """Return the ETKF analysis ensemble (a list of N members).

    ens: the forecast members, each a list of n numbers. yo: the observations.
    h(x): the observation operator. R: the p by p observation error
    covariance (symmetric positive definite). rho: multiplicative inflation
    of the covariance.
    """
    N, n = len(ens), len(ens[0])
    xbar = [sum(x[j] for x in ens) / N for j in range(n)]  # @line L1
    X = [[ens[i][j] - xbar[j] for i in range(N)] for j in range(n)]
    hx = [list(h(x)) for x in ens]  # @line L2
    p = len(yo)
    ybar = [sum(v[k] for v in hx) / N for k in range(p)]
    Y = [[hx[i][k] - ybar[k] for i in range(N)] for k in range(p)]
    wbar, W = etkf_transform(Y, R, [yo[k] - ybar[k] for k in range(p)], rho)
    out = []
    for i in range(N):  # @line L8
        coef = [wbar[k] + W[k][i] for k in range(N)]
        out.append([xbar[j] + scimat.dot(X[j], coef) for j in range(n)])
    return out  # @line L9


def ensemble_moments(ens):
    """Return (mean, P): the ensemble mean and the sample covariance with divisor N - 1."""
    N, n = len(ens), len(ens[0])
    mean = [sum(x[j] for x in ens) / N for j in range(n)]
    P = [[sum((x[a] - mean[a]) * (x[b] - mean[b]) for x in ens) / (N - 1) for b in range(n)] for a in range(n)]
    return mean, P
