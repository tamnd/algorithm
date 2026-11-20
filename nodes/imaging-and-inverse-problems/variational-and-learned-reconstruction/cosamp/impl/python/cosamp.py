# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cosamp/. The authors are listed in prov/E7NF54.jsonl.
"""CoSaMP (compressive sampling matching pursuit) of Needell and Tropp.

A is a list of m rows of length n, y has length m and s is the sparsity
level. Each iteration picks the 2s largest entries of the proxy A^T v,
merges them with the current support, solves least squares on the merged
set and keeps the s largest entries of the solution.
"""

from imgla import matvec, norm2, rmatvec, svd


def largest(v, k):
    """Indices of the k entries of largest magnitude (ties: lower index first)."""
    return sorted(range(len(v)), key=lambda i: (-abs(v[i]), i))[:k]


def least_squares_on(a, y, cols, rcond=1e-12):
    """argmin_z ||y - A_T z|| for the columns T = cols.

    The pseudoinverse is applied through a thin SVD of A_T, so the result is
    the least squares solution of minimum norm when A_T has dependent
    columns (for example when |T| > m).
    """
    at = [[row[i] for i in cols] for row in a]
    u, sig, v = svd(at)
    cut = rcond * sig[0] if sig else 0.0
    z = [0.0] * len(cols)
    for k, sk in enumerate(sig):
        if sk <= cut:
            continue
        c = sum(u[r][k] * y[r] for r in range(len(y))) / sk
        for j in range(len(cols)):
            z[j] += c * v[j][k]
    return z


def cosamp(a, y, s, iters=50, tol=1e-12, x0=None):
    """Run CoSaMP. Returns (x, residual_norms) with residual_norms[k] = ||y - A x^k||.

    x0 is an optional s-sparse start (default 0). The loop stops after iters
    steps, when the residual is at most tol * ||y||, or when the support and
    the residual stop changing.
    """
    n = len(a[0])
    x = list(x0) if x0 is not None else [0.0] * n  # @line L1
    v = [yi - ai for yi, ai in zip(y, matvec(a, x))]
    res = [norm2(v)]
    if res[0] == 0.0:
        return x, res
    for _ in range(iters):  # @line L2
        if res[-1] <= tol * norm2(y):
            break
        p = rmatvec(a, v)  # @line L3
        omega = largest(p, 2 * s)  # @line L4
        t = sorted(set(omega) | {i for i in range(n) if x[i] != 0.0})  # @line L5
        bt = least_squares_on(a, y, t)  # @line L6
        b = [0.0] * n
        for i, val in zip(t, bt):
            b[i] = val
        keep = largest(b, s)  # @line L7
        x_new = [0.0] * n
        for i in keep:
            x_new[i] = b[i]
        v = [yi - ai for yi, ai in zip(y, matvec(a, x_new))]  # @line L8
        res.append(norm2(v))
        same = all((x_new[i] != 0.0) == (x[i] != 0.0) for i in range(n))
        x = x_new
        if same and res[-1] >= res[-2] * (1.0 - 1e-12):
            break
    return x, res  # @line L9
