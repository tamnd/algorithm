# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ensemble-kalman-smoother/. The authors are listed in prov/G9PNFT.jsonl.

"""Fixed-lag ensemble Kalman smoother (EnKS) with a square root analysis.

Notation of Ide, Courtier, Ghil and Lorenc (1997). The ensemble has N members
in R^n, the observations at time t have the error covariance R, and h is the
observation operator.

At each observation time the analysis is written as a linear combination of
the forecast members: x^a_i = xbar + X (wbar + W_i), with the weights of the
ensemble transform Kalman filter. The smoother applies the same weights to
the stored ensembles of the last L times (Evensen and van Leeuwen 2000;
Evensen 2003 writes this as E^a = E^f X5). With L = 0 it is the filter.

Cost of one analysis: O(N^2 p + p^3 + N^3) for the weights and O(N^2 n) for
each stored time, so O(N^2 (p + n (L + 1)) + p^3 + N^3) in all.
"""

import math

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


def transform_weights(ens, yo, h, R):
    """Return (wbar, W): the ETKF weights of the forecast ensemble for the observations yo."""
    N = len(ens)
    hx = [list(h(x)) for x in ens]  # @line L4
    p = len(yo)
    ybar = [sum(v[k] for v in hx) / N for k in range(p)]
    Y = [[hx[i][k] - ybar[k] for i in range(N)] for k in range(p)]  # p by N
    C = scimat.transpose(scimat.solve(R, Y))  # @line L5
    A = scimat.add(scimat.scale(N - 1, scimat.eye(N)), scimat.matmul(C, Y))
    lam, Q = sym_eig(A)
    Pt = [[sum(Q[a][m] * Q[b][m] / lam[m] for m in range(N)) for b in range(N)] for a in range(N)]
    W = [[sum(Q[a][m] * math.sqrt((N - 1) / lam[m]) * Q[b][m] for m in range(N)) for b in range(N)] for a in range(N)]
    wbar = scimat.matvec(Pt, scimat.matvec(C, [yo[k] - ybar[k] for k in range(p)]))
    return wbar, W


def apply_weights(ens, wbar, W):
    """Return the members sbar + S (wbar + W_i) of the ensemble ens (any state, any time)."""
    N, n = len(ens), len(ens[0])
    sbar = [sum(s[j] for s in ens) / N for j in range(n)]
    S = [[s[j] - sbar[j] for j in range(n)] for s in ens]
    out = []
    for i in range(N):
        c = [wbar[m] + W[m][i] for m in range(N)]
        out.append([sbar[j] + sum(c[m] * S[m][j] for m in range(N)) for j in range(n)])
    return out


def inflate(ens, rho):
    """Return the ensemble with its perturbations multiplied by sqrt(rho)."""
    N, n = len(ens), len(ens[0])
    m = [sum(x[j] for x in ens) / N for j in range(n)]
    f = math.sqrt(rho)
    return [[m[j] + f * (x[j] - m[j]) for j in range(n)] for x in ens]


def enks(ens0, model, h, R, obs, lag, rho=1.0):
    """Run the fixed-lag EnKS from the ensemble ens0 at time 0.

    obs[t - 1] is the observation vector at time t (t = 1..T) or None.
    rho multiplies the covariance of each forecast before its analysis.
    Return (filt, smooth): lists of the ensembles at the times 0..T. filt[t]
    has used the data up to time t, smooth[t] the data up to time t + lag.
    """
    filt = [[list(x) for x in ens0]]
    smooth = [[list(x) for x in ens0]]
    window = [0] if lag >= 1 else []  # times whose ensembles the next analysis still updates
    for t in range(1, len(obs) + 1):  # @line L1
        ens = [list(model(x)) for x in filt[-1]]  # @line L2
        if rho != 1.0:
            ens = inflate(ens, rho)
        smooth.append(ens)
        window.append(t)
        if obs[t - 1] is not None:  # @line L3
            wbar, W = transform_weights(ens, obs[t - 1], h, R)
            for s in window:  # @line L6
                smooth[s] = apply_weights(smooth[s], wbar, W)
        filt.append(smooth[t])
        while window and window[0] < t - lag + 1:  # @line L7
            window.pop(0)
    return filt, smooth  # @line L8


def ensemble_moments(ens):
    """Return (mean, P): the ensemble mean and the sample covariance with divisor N - 1."""
    N, n = len(ens), len(ens[0])
    mean = [sum(x[j] for x in ens) / N for j in range(n)]
    P = [[sum((x[a] - mean[a]) * (x[b] - mean[b]) for x in ens) / (N - 1) for b in range(n)] for a in range(n)]
    return mean, P
