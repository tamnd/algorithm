# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ensemble-square-root-filter/. The authors are listed in prov/W0YQYW.jsonl.

"""Serial ensemble square root filter (EnSRF) of Whitaker and Hamill (2002).

Notation of Ide, Courtier, Ghil and Lorenc (1997). The forecast ensemble has
N members in R^n. The p observations have independent errors with variances
r_k, so R is diagonal and the observations can be taken one at a time.

The filter keeps the state ensemble and the ensemble of predicted
observations y_i = h(x_i), and updates both with each scalar observation k:

    s = var(y_k), K = cov(x, y_k) / (s + r_k), alpha = 1 / (1 + sqrt(r_k / (s + r_k)))
    mean <- mean + K (y^o_k - ybar_k),  x'_i <- x'_i - alpha K y'_{k,i}

The mean moves by the Kalman gain and the perturbations by the reduced gain
alpha K, with no perturbed observations. Optional localization weights
multiply K entry by entry (the Schur product applied to the gain). Cost:
O(p N (n + p)) for the p observations.
"""

import math


def ensrf_analysis(ens, yo, h, r_var, loc_state=None, loc_obs=None):
    """Return the EnSRF analysis ensemble (a list of N members).

    ens: forecast members (lists of n floats). yo: the p observations.
    h(x): the observation operator, evaluated once per member. r_var: the
    error variances of the observations. loc_state[k][j] and loc_obs[k][l]:
    optional localization weights between observation k and state value j,
    or observation l. None means weight 1.
    """
    N, n, p = len(ens), len(ens[0]), len(yo)
    xbar = [sum(x[j] for x in ens) / N for j in range(n)]  # @line L1
    X = [[x[j] - xbar[j] for x in ens] for j in range(n)]
    hx = [list(h(x)) for x in ens]
    ybar = [sum(v[k] for v in hx) / N for k in range(p)]
    Y = [[hx[i][k] - ybar[k] for i in range(N)] for k in range(p)]
    for k in range(p):  # @line L2
        yk = list(Y[k])
        s = sum(v * v for v in yk) / (N - 1)  # @line L3
        b = [sum(a * v for a, v in zip(X[j], yk)) / (N - 1) for j in range(n)]  # @line L4
        c = [sum(a * v for a, v in zip(Y[l], yk)) / (N - 1) for l in range(p)]
        if loc_state is not None:
            b = [bj * wj for bj, wj in zip(b, loc_state[k])]
        if loc_obs is not None:
            c = [cl * wl for cl, wl in zip(c, loc_obs[k])]
        K = [bj / (s + r_var[k]) for bj in b]  # @line L5
        Ky = [cl / (s + r_var[k]) for cl in c]
        alpha = 1.0 / (1.0 + math.sqrt(r_var[k] / (s + r_var[k])))  # @line L6
        d = yo[k] - ybar[k]  # @line L7
        xbar = [m + kj * d for m, kj in zip(xbar, K)]  # @line L8
        ybar = [m + kl * d for m, kl in zip(ybar, Ky)]
        X = [[a - alpha * kj * v for a, v in zip(X[j], yk)] for j, kj in enumerate(K)]  # @line L9
        Y = [[a - alpha * kl * v for a, v in zip(Y[l], yk)] for l, kl in enumerate(Ky)]
    return [[xbar[j] + X[j][i] for j in range(n)] for i in range(N)]  # @line L10


def ensemble_moments(ens):
    """Return (mean, P): the ensemble mean and the sample covariance with divisor N - 1."""
    N, n = len(ens), len(ens[0])
    mean = [sum(x[j] for x in ens) / N for j in range(n)]
    P = [[sum((x[a] - mean[a]) * (x[b] - mean[b]) for x in ens) / (N - 1) for b in range(n)] for a in range(n)]
    return mean, P
