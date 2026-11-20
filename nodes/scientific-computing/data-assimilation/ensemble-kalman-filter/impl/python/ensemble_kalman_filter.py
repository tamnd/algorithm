# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ensemble-kalman-filter/. The authors are listed in prov/JS3602.jsonl.

"""Ensemble Kalman filter (EnKF) with perturbed observations.

Notation of Ide, Courtier, Ghil and Lorenc (1997). The forecast ensemble has
N members in R^n, the observations y^o in R^p have the error covariance R,
and h is the observation operator (it may be nonlinear).

enkf_analysis forms the gain from the sample covariances of the state and of
the predicted observations and moves each member towards its own perturbed
copy of the observations (Burgers, van Leeuwen and Evensen 1998; Houtekamer
and Mitchell 1998). The optional weights loc_xy (n by p) and loc_yy (p by p)
multiply the two sample covariances entry by entry, which localizes the gain.

enkf_forecast runs every member through the model.

Cost of one analysis: O(N p (n + p) + p^3) and N calls of h.
"""

import random

import scimat


def enkf_forecast(ens, model):
    """Return the forecast ensemble [model(x) for each member x]."""
    return [list(model(x)) for x in ens]


def observation_perturbations(R, N, rng):
    """Return N draws of N(0, R), one list of length p for each member."""
    low = scimat.cholesky(R)
    p = len(R)
    out = []
    for _ in range(N):
        z = [rng.gauss(0.0, 1.0) for _ in range(p)]
        out.append([sum(low[a][b] * z[b] for b in range(a + 1)) for a in range(p)])
    return out


def enkf_analysis(ens, yo, h, R, rng=None, eps=None, loc_xy=None, loc_yy=None):
    """Return the analysis ensemble of the perturbed observation EnKF.

    eps, if given, is the list of the N observation perturbations; otherwise
    they are drawn from N(0, R) with rng (a random.Random).
    """
    N, n, p = len(ens), len(ens[0]), len(yo)
    y = [list(h(x)) for x in ens]  # @line L1
    xbar = [sum(x[j] for x in ens) / N for j in range(n)]  # @line L2
    ybar = [sum(v[k] for v in y) / N for k in range(p)]
    X = [[x[j] - xbar[j] for j in range(n)] for x in ens]
    Y = [[v[k] - ybar[k] for k in range(p)] for v in y]
    PHt = [[sum(X[i][j] * Y[i][k] for i in range(N)) / (N - 1) for k in range(p)] for j in range(n)]  # @line L3
    HPHt = [[sum(Y[i][a] * Y[i][b] for i in range(N)) / (N - 1) for b in range(p)] for a in range(p)]
    if loc_xy is not None:
        PHt = [[PHt[j][k] * loc_xy[j][k] for k in range(p)] for j in range(n)]
    if loc_yy is not None:
        HPHt = [[HPHt[a][b] * loc_yy[a][b] for b in range(p)] for a in range(p)]
    if eps is None:  # @line L4
        eps = observation_perturbations(R, N, rng if rng is not None else random.Random(0))
    S = scimat.add(HPHt, R)  # @line L5
    D = [[yo[k] + eps[i][k] - y[i][k] for i in range(N)] for k in range(p)]  # @line L6
    Z = scimat.solve(S, D)  # p by N
    out = []
    for i in range(N):  # @line L7
        out.append([ens[i][j] + sum(PHt[j][k] * Z[k][i] for k in range(p)) for j in range(n)])
    return out  # @line L8


def ensemble_moments(ens):
    """Return (mean, P): the ensemble mean and the sample covariance with divisor N - 1."""
    N, n = len(ens), len(ens[0])
    mean = [sum(x[j] for x in ens) / N for j in range(n)]
    P = [[sum((x[a] - mean[a]) * (x[b] - mean[b]) for x in ens) / (N - 1) for b in range(n)] for a in range(n)]
    return mean, P
