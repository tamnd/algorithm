# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/johansen-test/. The authors are listed in prov/AA2XYN.jsonl.
"""The Johansen trace and maximum eigenvalue tests for the cointegration rank.

The vector error correction form of a VAR(p) in K variables is

    dY_t = Pi Y_(t-1) + sum_(i=1..p-1) G_i dY_(t-i) + mu + e_t.

The test removes the short-run terms (lagged differences and, in case "c",
the constant) from dY_t and from Y_(t-1) by least squares, forms the moment
matrices S_00, S_01, S_11 of the two residual sets, and solves the generalized
eigenproblem

    det(lambda S_11 - S_10 S_00^(-1) S_01) = 0.

The eigenvalues are the squared canonical correlations between the two
residual sets. The trace statistic for rank r is -T sum_(i>r) log(1 - lambda_i)
and the maximum eigenvalue statistic is -T log(1 - lambda_(r+1)).
"""

import math
import random

# Asymptotic quantiles (90%, 95%, 99%) from MacKinnon, Haug and Michelis (1999),
# as tabulated in statsmodels coint_tables.py. Row K - r = 1..5.
# "none": no deterministic terms. "c": unrestricted constant (linear trends in the data).
TRACE = {
    "none": [(2.9762, 4.1296, 6.9406), (10.4741, 12.3212, 16.3640), (21.7781, 24.2761, 29.5147),
             (37.0339, 40.1749, 46.5716), (56.2839, 60.0627, 67.6367)],
    "c": [(2.7055, 3.8415, 6.6349), (13.4294, 15.4943, 19.9349), (27.0669, 29.7961, 35.4628),
          (44.4929, 47.8545, 54.6815), (65.8202, 69.8189, 77.8202)],
}
MAX_EIG = {
    "none": [(2.9762, 4.1296, 6.9406), (9.4748, 11.2246, 15.0923), (15.7175, 17.7961, 22.2519),
             (21.8370, 24.1592, 29.0609), (27.9160, 30.4428, 35.7359)],
    "c": [(2.7055, 3.8415, 6.6349), (12.2971, 14.2639, 18.5200), (18.8928, 21.1314, 25.8650),
          (25.1236, 27.5858, 32.7172), (31.2379, 33.8777, 39.3693)],
}
_LEVEL_INDEX = {0.10: 0, 0.05: 1, 0.01: 2}


def critical_value(table, case, k_minus_r, level=0.05):
    """Asymptotic critical value for the trace ("trace") or max-eigenvalue ("max") statistic."""
    t = TRACE if table == "trace" else MAX_EIG
    return t[case][k_minus_r - 1][_LEVEL_INDEX[level]]


def _residualize(targets, regressors):
    """Residuals of each target column after least squares on the regressor columns.

    Uses modified Gram-Schmidt on the regressors, so the residual of each target
    is its projection onto the orthogonal complement of their span."""
    basis = []
    for col in regressors:
        v = [float(a) for a in col]
        norm0 = math.sqrt(sum(a * a for a in v))
        for q in basis:
            d = sum(a * b for a, b in zip(q, v))
            v = [a - d * b for a, b in zip(v, q)]
        nrm = math.sqrt(sum(a * a for a in v))
        if norm0 == 0.0 or nrm <= 1e-12 * norm0:
            raise ValueError("the short-run regressors are linearly dependent")
        basis.append([a / nrm for a in v])
    out = []
    for col in targets:
        v = [float(a) for a in col]
        for q in basis:
            d = sum(a * b for a, b in zip(q, v))
            v = [a - d * b for a, b in zip(v, q)]
        out.append(v)
    return out


def moments(a, b):
    """(1/T) sum_t a_t b_t^T for lists of columns a and b."""
    t = len(a[0])
    return [[sum(x * y for x, y in zip(ai, bj)) / t for bj in b] for ai in a]


def cholesky(s):
    """Lower triangular L with L L^T = s, for a symmetric positive definite s."""
    k = len(s)
    low = [[0.0] * k for _ in range(k)]
    for i in range(k):
        for j in range(i + 1):
            v = s[i][j] - sum(low[i][m] * low[j][m] for m in range(j))
            if i == j:
                if v <= 0.0:
                    raise ValueError("matrix is not positive definite")
                low[i][i] = math.sqrt(v)
            else:
                low[i][j] = v / low[j][j]
    return low


def lower_inverse(low):
    """Inverse of a lower triangular matrix by forward substitution."""
    k = len(low)
    inv = [[0.0] * k for _ in range(k)]
    for c in range(k):
        for i in range(c, k):
            rhs = (1.0 if i == c else 0.0) - sum(low[i][m] * inv[m][c] for m in range(c, i))
            inv[i][c] = rhs / low[i][i]
    return inv


def solve_spd(s, b):
    """s^(-1) b for symmetric positive definite s and a matrix b (list of rows)."""
    low = cholesky(s)
    li = lower_inverse(low)
    k = len(s)
    sinv = [[sum(li[m][i] * li[m][j] for m in range(k)) for j in range(k)] for i in range(k)]
    return [[sum(sinv[i][m] * b[m][j] for m in range(k)) for j in range(len(b[0]))] for i in range(k)]


def jacobi_eigen(a, tol=1e-14, max_sweeps=100):
    """Eigenvalues and eigenvectors of a symmetric matrix by cyclic Jacobi rotations.

    Returns (values, vectors) with values in decreasing order and vectors as
    columns of an orthogonal matrix (vectors[i][j] is entry i of vector j)."""
    k = len(a)
    a = [row[:] for row in a]
    v = [[1.0 if i == j else 0.0 for j in range(k)] for i in range(k)]
    for _ in range(max_sweeps):
        off = sum(a[i][j] ** 2 for i in range(k) for j in range(k) if i != j)
        scale = sum(a[i][i] ** 2 for i in range(k)) or 1.0
        if off <= tol * tol * scale:
            break
        for p in range(k - 1):
            for q in range(p + 1, k):
                if a[p][q] == 0.0:
                    continue
                theta = (a[q][q] - a[p][p]) / (2.0 * a[p][q])
                t = math.copysign(1.0, theta) / (abs(theta) + math.sqrt(theta * theta + 1.0))
                c = 1.0 / math.sqrt(t * t + 1.0)
                s = t * c
                for m in range(k):
                    amp, amq = a[m][p], a[m][q]
                    a[m][p], a[m][q] = c * amp - s * amq, s * amp + c * amq
                for m in range(k):
                    apm, aqm = a[p][m], a[q][m]
                    a[p][m], a[q][m] = c * apm - s * aqm, s * apm + c * aqm
                for m in range(k):
                    vmp, vmq = v[m][p], v[m][q]
                    v[m][p], v[m][q] = c * vmp - s * vmq, s * vmp + c * vmq
    order = sorted(range(k), key=lambda i: -a[i][i])
    return [a[i][i] for i in order], [[v[m][i] for i in order] for m in range(k)]


def johansen(data, case="none", lags=0, level=0.05):
    """Johansen rank tests for K series (data is a list of K series of equal length n).

    lags is the number of lagged differences (the VAR order minus 1). case is
    "none" (no deterministic terms) or "c" (unrestricted constant). Returns the
    eigenvalues, the trace and max-eigenvalue statistics for r = 0..K-1, their
    critical values, the rank chosen by the sequential trace test, the
    eigenvectors beta (columns, normalized by beta^T S_11 beta = I), alpha =
    S_01 beta and T."""
    if case not in TRACE:
        raise ValueError("case must be 'none' or 'c'")
    k = len(data)
    if not 1 <= k <= 5:
        raise ValueError("between 1 and 5 series are supported")
    n = len(data[0])
    rows = range(lags + 1, n)
    big_t = len(rows)
    if big_t <= k * (lags + 1) + 1:
        raise ValueError("series too short for this many lags")
    diff = [[0.0] + [s[t] - s[t - 1] for t in range(1, n)] for s in data]
    short = [[d[t - i] for t in rows] for i in range(1, lags + 1) for d in diff]
    if case == "c":
        short.append([1.0] * big_t)
    r0 = _residualize([[d[t] for t in rows] for d in diff], short)  # @line L1
    r1 = _residualize([[s[t - 1] for t in rows] for s in data], short)  # @line L2
    s00, s01, s11 = moments(r0, r0), moments(r0, r1), moments(r1, r1)  # @line L3
    s10 = [[s01[j][i] for j in range(k)] for i in range(k)]
    low = cholesky(s11)  # @line L4
    li = lower_inverse(low)
    m = [[sum(s10[i][a] * x for a, x in enumerate(col)) for col in zip(*solve_spd(s00, s01))]
         for i in range(k)]  # S_10 S_00^(-1) S_01
    c = [[sum(li[i][a] * m[a][b] * li[j][b] for a in range(k) for b in range(k)) for j in range(k)]
         for i in range(k)]
    c = [[(c[i][j] + c[j][i]) / 2.0 for j in range(k)] for i in range(k)]
    lam, vec = jacobi_eigen(c)  # @line L5
    lam = [min(max(x, 0.0), 1.0 - 1e-15) for x in lam]
    beta = [[sum(li[a][i] * vec[a][j] for a in range(k)) for j in range(k)] for i in range(k)]  # @line L6
    alpha = [[sum(s01[i][a] * beta[a][j] for a in range(k)) for j in range(k)] for i in range(k)]
    logs = [math.log(1.0 - x) for x in lam]
    trace = [-big_t * sum(logs[r:]) for r in range(k)]  # @line L7
    max_eig = [-big_t * logs[r] for r in range(k)]
    crit_trace = [critical_value("trace", case, k - r, level) for r in range(k)]
    crit_max = [critical_value("max", case, k - r, level) for r in range(k)]
    rank = next((r for r in range(k) if trace[r] < crit_trace[r]), k)  # @line L8
    return {"eigenvalues": lam, "trace": trace, "max_eig": max_eig, "crit_trace": crit_trace,  # @line L9
            "crit_max": crit_max, "rank": rank, "beta": beta, "alpha": alpha, "nobs": big_t,
            "s00": s00, "s01": s01, "s11": s11}


def simulate_trace(n, k, case="none", reps=500, rng=None):
    """Trace statistics for r = 0 from reps sets of k independent Gaussian random walks."""
    rng = rng or random.Random(0)
    out = []
    for _ in range(reps):
        data = []
        for _ in range(k):
            s, w = 0.0, []
            for _ in range(n):
                s += rng.gauss(0.0, 1.0)
                w.append(s)
            data.append(w)
        out.append(johansen(data, case, 0)["trace"][0])
    return out
