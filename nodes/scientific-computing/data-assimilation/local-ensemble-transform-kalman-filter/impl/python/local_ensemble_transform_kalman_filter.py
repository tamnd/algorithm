# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/local-ensemble-transform-kalman-filter/. The authors are listed in prov/HEPB83.jsonl.

"""Local ensemble transform Kalman filter (LETKF) with R-localization.

Notation of Ide, Courtier, Ghil and Lorenc (1997) and of Hunt, Kostelich and
Szunyogh (2007). The forecast ensemble has N members x_1..x_N in R^n. The
observations y^o in R^p have independent errors with variances r_k. The
observation operator h maps a state to R^p and may be nonlinear.

X and Y hold the unscaled perturbations x_i - xbar and h(x_i) - ybar. For each
grid point j the LETKF takes the observations k within distance 2c, divides
row k of Y by sqrt(r_k / w_k) with w_k = GC(dist / c) (Gaspari-Cohn), and
solves the ETKF problem in the N-dimensional ensemble space:

    P~ = ((N - 1) / rho I + S^T S)^-1,  wbar = P~ S^T d,  W = sqrt(N - 1) P~^(1/2)
    x^a_{j,i} = xbar_j + X_j (wbar + W_i)

S has p_l rows, one per local observation, and N columns. The code does not
form the N by N matrices. It finds the eigenpairs of the small p_l by p_l
matrix S S^T and uses them to apply P~ and W, so one grid point costs
O(p_l^2 N + p_l^3) and the analysis costs O(n (p_l^2 N + p_l^3)) after the
O(N (n + p)) set up. rho multiplies the covariance (the perturbations grow by
sqrt(rho)).
"""

import math

import scimat


def gaspari_cohn(r, c):
    """Return the Gaspari-Cohn function (eq. 4.10 of Gaspari and Cohn 1999) at distance r.

    c is the half-width: the value is 1 at r = 0, 5/24 at r = c and 0 for
    |r| >= 2c. Integer and Fraction arguments give exact values.
    """
    z = abs(r) / c
    if z >= 2:
        return 0 * z
    if z <= 1:
        return -z**5 / 4 + z**4 / 2 + 5 * z**3 / 8 - 5 * z**2 / 3 + 1
    return z**5 / 12 - z**4 / 2 + 5 * z**3 / 8 + 5 * z**2 / 3 - 5 * z + 4 - 2 / (3 * z)


def periodic_distance(period):
    """Return dist(a, b) = the distance between positions a and b on a circle of length period."""

    def dist(a, b):
        r = abs(a - b) % period
        return min(r, period - r)

    return dist


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


def letkf_analysis(ens, yo, h, r_var, grid_pos=None, obs_pos=None, c=None, rho=1.0, dist=None):
    """Return the LETKF analysis ensemble (a list of N members).

    ens: the forecast members, each a list of n floats.
    yo: the p observations. h(x): the observation operator. r_var: the p
    observation error variances (R is diagonal).
    grid_pos, obs_pos: the positions of the n state values and the p
    observations. c: the Gaspari-Cohn half-width; None uses every observation
    with weight 1 at every point, which is the global ETKF.
    rho: multiplicative inflation of the covariance. dist(a, b): the distance,
    by default |a - b|.
    """
    N, n, p = len(ens), len(ens[0]), len(yo)
    if dist is None:
        dist = lambda a, b: abs(a - b)
    hx = [list(h(x)) for x in ens]  # @line L1
    ybar = [sum(hx[i][k] for i in range(N)) / N for k in range(p)]
    Y = [[hx[i][k] - ybar[k] for i in range(N)] for k in range(p)]
    xbar = [sum(ens[i][j] for i in range(N)) / N for j in range(n)]  # @line L2
    X = [[ens[i][j] - xbar[j] for i in range(N)] for j in range(n)]
    gamma = (N - 1) / rho
    sr = math.sqrt(rho)
    out = [[0.0] * n for _ in range(N)]
    for j in range(n):  # @line L3
        if c is None:  # @line L4
            loc = [(k, 1.0) for k in range(p)]
        else:
            loc = []
            for k in range(p):
                w = gaspari_cohn(dist(grid_pos[j], obs_pos[k]), c)
                if w > 0:
                    loc.append((k, w))
        scl = [math.sqrt(w / r_var[k]) for k, w in loc]  # @line L5
        S = [[s * v for v in Y[k]] for (k, _), s in zip(loc, scl)]
        dl = [s * (yo[k] - ybar[k]) for (k, _), s in zip(loc, scl)]
        G = [[scimat.dot(S[a], S[b]) for b in range(len(S))] for a in range(len(S))]  # @line L6
        sig, V = sym_eig(G) if S else ([], [])
        top = max(sig) if sig else 0.0
        modes = []
        for m, s in enumerate(sig):
            if s > 1e-12 * top:
                u = [sum(V[a][m] * S[a][i] for a in range(len(S))) / math.sqrt(s) for i in range(N)]
                modes.append((s, u))
        b = [sum(S[a][i] * dl[a] for a in range(len(S))) for i in range(N)]  # @line L7
        wbar = [bi / gamma for bi in b]
        for s, u in modes:
            f = (1.0 / (gamma + s) - 1.0 / gamma) * scimat.dot(u, b)
            wbar = [wi + f * ui for wi, ui in zip(wbar, u)]
        xj = X[j]  # @line L8
        row = [sr * v for v in xj]
        for s, u in modes:
            f = (math.sqrt((N - 1) / (gamma + s)) - sr) * scimat.dot(xj, u)
            row = [ri + f * ui for ri, ui in zip(row, u)]
        base = xbar[j] + scimat.dot(xj, wbar)
        for i in range(N):
            out[i][j] = base + row[i]  # @line L9
    return out  # @line L10


def mean_and_spread(ens):
    """Return (mean, var): the ensemble mean and the sample variance (divisor N - 1) of each component."""
    N, n = len(ens), len(ens[0])
    mean = [sum(x[j] for x in ens) / N for j in range(n)]
    var = [sum((x[j] - mean[j]) ** 2 for x in ens) / (N - 1) for j in range(n)]
    return mean, var
