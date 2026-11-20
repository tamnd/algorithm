# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/optimal-interpolation/. The authors are listed in prov/BG2VYK.jsonl.

"""Optimal interpolation (OI) with local data selection.

Notation of Ide, Courtier, Ghil and Lorenc (1997): background x^b in R^n,
observations y^o in R^p, a linear observation operator H (p by n), the
background error covariance B (n by n) and the observation error covariance
R (p by p). The innovation is d = y^o - H x^b.

For each grid point i, OI picks a set S_i of observations, solves the small
system (H B H^T + R)[S_i, S_i] w = (H B)[S_i, i] and sets
x^a_i = x^b_i + w^T d[S_i]. With S_i = all observations for every i, the
result is x^b + K d with the Kalman gain K = B H^T (H B H^T + R)^-1.

Matrices are lists of rows, as in scimat. With Fraction data the result is
exact. Cost: forming H B H^T and H B is O(p n^2) for a dense H; each point
then costs O(s^3) for s = |S_i|, so the analysis costs O(n s^3) after that.
"""

import math

import scimat


def oi_analysis(xb, B, yo, H, R, select=None):
    """Return (xa, var_a): the OI analysis and its error variance at each point.

    select(i) returns the list of observation indices used for grid point i;
    None means all observations for every point (the global analysis).
    var_a[i] = B[i][i] - w^T c is the analysis error variance of point i when
    B and R are the true covariances.
    """
    n, p = len(xb), len(yo)
    Hxb = scimat.matvec(H, xb)
    d = [yo[k] - Hxb[k] for k in range(p)]  # @line L1
    HB = scimat.matmul(H, B)  # p by n, column i holds cov(H x, x_i)
    A = scimat.add(scimat.matmul(HB, scimat.transpose(H)), R)  # H B H^T + R
    xa, var_a = [], []
    for i in range(n):  # @line L2
        S = list(range(p)) if select is None else list(select(i))  # @line L3
        if not S:
            xa.append(xb[i])
            var_a.append(B[i][i])
            continue
        As = [[A[a][b] for b in S] for a in S]  # @line L4
        c = [HB[a][i] for a in S]  # @line L5
        w = scimat.solve(As, c)  # @line L6
        xa.append(xb[i] + sum(w[t] * d[S[t]] for t in range(len(S))))  # @line L7
        var_a.append(B[i][i] - sum(w[t] * c[t] for t in range(len(S))))  # @line L8
    return xa, var_a  # @line L9


def radius_selector(grid_pos, obs_pos, radius, max_obs=None, period=None):
    """Return select(i): the observations within radius of grid point i.

    Distances are |grid_pos[i] - obs_pos[k]|, or the distance on a circle of
    length period. If max_obs is given, keep only the max_obs nearest ones.
    """

    def dist(a, b):
        r = abs(a - b)
        if period is not None:
            r = min(r, period - r)
        return r

    def select(i):
        near = [(dist(grid_pos[i], q), k) for k, q in enumerate(obs_pos) if dist(grid_pos[i], q) <= radius]
        near.sort()
        if max_obs is not None:
            near = near[:max_obs]
        return sorted(k for _, k in near)

    return select


def ar1_covariance(n, sigma2, rho):
    """Return B with B_ij = sigma2 rho^|i - j|, the covariance of an AR(1) sequence.

    B is symmetric positive definite for |rho| < 1 and sigma2 > 0.
    """
    return [[sigma2 * rho ** abs(i - j) for j in range(n)] for i in range(n)]


def gaussian_covariance(pos, sigma2, length, period=None):
    """Return B_ij = sigma2 exp(-r_ij^2 / (2 length^2)) for points at pos.

    With period, r_ij is the distance on a circle of that length. The Gaussian
    correlation on a line is positive definite; on a circle it is positive
    definite only when length is small compared with the period.
    """
    n = len(pos)
    B = scimat.zeros(n)
    for i in range(n):
        for j in range(n):
            r = abs(pos[i] - pos[j])
            if period is not None:
                r = min(r, period - r)
            B[i][j] = sigma2 * math.exp(-r * r / (2.0 * length * length))
    return B


def interpolation_operator(obs_pos, n, dx, period=True):
    """Return H (p by n) for linear interpolation from grid points j dx to obs_pos.

    On a periodic grid of n points the position is taken modulo n dx.
    """
    H = scimat.zeros(len(obs_pos), n)
    for k, q in enumerate(obs_pos):
        s = q / dx
        j = math.floor(s)
        a = s - j
        if period:
            H[k][j % n] += 1 - a
            H[k][(j + 1) % n] += a
        else:
            H[k][j] += 1 - a
            if a != 0:
                H[k][j + 1] += a
    return H
