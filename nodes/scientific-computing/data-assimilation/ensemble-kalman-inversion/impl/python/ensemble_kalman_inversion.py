# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ensemble-kalman-inversion/. The authors are listed in prov/421ZWN.jsonl.

"""Ensemble Kalman inversion (EKI) for y = G(u) + noise, noise ~ N(0, Gamma).

Each step is an ensemble Kalman update with the noise covariance Gamma / h
(Iglesias, Law and Stuart 2013; Schillings and Stuart 2017). With K steps of
size h = 1/K and perturbed data this is the ensemble smoother with multiple
data assimilation of Emerick and Reynolds (2013) with all factors equal to K.
G is called once for each member and step; no derivative of G is used.

mode = "perturbed": each member sees y + eta_j with eta_j ~ N(0, Gamma / h).
mode = "none":      each member sees y itself (the deterministic EKI).
mode = "sqrt":      the mean moves by the Kalman gain and the perturbations
                    by the symmetric ensemble transform; for a linear G this
                    gives exactly the moments of one tempered Bayes step.

Cost of one step: O(N p (d + p) + p^3) plus N calls of G (O(N^3) more for "sqrt").
"""

import math
import random

import scimat


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


def eki_step(ens, G, y, Gamma, h=1.0, mode="perturbed", rng=None):
    """Return the ensemble after one EKI step of size h."""
    N, d, p = len(ens), len(ens[0]), len(y)
    g = [list(G(u)) for u in ens]  # @line L2
    ubar = [sum(u[a] for u in ens) / N for a in range(d)]  # @line L3
    gbar = [sum(v[k] for v in g) / N for k in range(p)]
    U = [[u[a] - ubar[a] for a in range(d)] for u in ens]
    Gp = [[v[k] - gbar[k] for k in range(p)] for v in g]
    Gh = scimat.scale(1.0 / h, Gamma)
    if mode == "sqrt":
        Y = scimat.transpose(Gp)  # p by N
        C = scimat.transpose(scimat.solve(Gh, Y))
        A = scimat.add(scimat.scale(N - 1, scimat.eye(N)), scimat.matmul(C, Y))
        lam, Q = sym_eig(A)
        Pt = [[sum(Q[a][m] * Q[b][m] / lam[m] for m in range(N)) for b in range(N)] for a in range(N)]
        W = [[sum(Q[a][m] * math.sqrt((N - 1) / lam[m]) * Q[b][m] for m in range(N)) for b in range(N)] for a in range(N)]
        wbar = scimat.matvec(Pt, scimat.matvec(C, scimat.sub(y, gbar)))
        return [[ubar[a] + sum((wbar[m] + W[m][i]) * U[m][a] for m in range(N)) for a in range(d)] for i in range(N)]
    Cug = [[sum(U[i][a] * Gp[i][k] for i in range(N)) / (N - 1) for k in range(p)] for a in range(d)]
    Cgg = [[sum(Gp[i][k] * Gp[i][l] for i in range(N)) / (N - 1) for l in range(p)] for k in range(p)]
    targets = [list(y) for _ in range(N)]  # @line L4
    if mode == "perturbed":
        rng = rng if rng is not None else random.Random(0)
        low = scimat.cholesky(Gh)
        for t in targets:
            z = [rng.gauss(0.0, 1.0) for _ in range(p)]
            for k in range(p):
                t[k] += sum(low[k][l] * z[l] for l in range(k + 1))
    S = scimat.add(Cgg, Gh)  # @line L5
    D = [[targets[i][k] - g[i][k] for i in range(N)] for k in range(p)]
    Z = scimat.solve(S, D)
    return [[ens[i][a] + sum(Cug[a][k] * Z[k][i] for k in range(p)) for a in range(d)] for i in range(N)]


def eki(ens0, G, y, Gamma, h=1.0, steps=1, mode="perturbed", rng=None):
    """Run steps EKI steps from ens0 and return the list of the ensembles, ens0 first."""
    out = [[list(u) for u in ens0]]
    for _ in range(steps):  # @line L1
        out.append(eki_step(out[-1], G, y, Gamma, h, mode, rng))
    return out  # @line L6


def ensemble_moments(ens):
    """Return (mean, P): the ensemble mean and the sample covariance with divisor N - 1."""
    N, n = len(ens), len(ens[0])
    mean = [sum(x[j] for x in ens) / N for j in range(n)]
    P = [[sum((x[a] - mean[a]) * (x[b] - mean[b]) for x in ens) / (N - 1) for b in range(n)] for a in range(n)]
    return mean, P
