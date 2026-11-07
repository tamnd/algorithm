# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hagers-condition-estimator/. The authors are listed in prov/TXN1K8.jsonl.

"""Hager's estimator of the 1-norm of a matrix B that is known only through
products B x and B^T x, and its use for the condition number
kappa_1(A) = ||A||_1 ||A^{-1}||_1 with B = A^{-1} applied by LU solves.

variant="hager" is Hager's 1984 iteration run to its stopping test.
variant="higham" is Higham's refinement used in LAPACK (xLACON/xLACN2):
at most itmax iterations, a test for a repeated sign vector, and an extra
estimate from the vector b_i = (-1)^i (1 + i/(n-1)).
Works with floats or fractions.Fraction: the probe vectors are exact
Fractions, so the arithmetic follows the type of B. Standard library only.
"""

from fractions import Fraction


class Singular(ArithmeticError):
    """The matrix is singular to working precision (a zero pivot)."""


def norm1(a):
    """The 1-norm of a dense matrix: the largest column sum of absolute values."""
    n = len(a[0]) if a else 0
    return max((sum(abs(row[j]) for row in a) for j in range(n)), default=0)


def _sign(v):
    return -1 if v < 0 else 1


def norm1_estimate(apply, apply_t, n, variant="higham", itmax=5, stats=None):
    """Return (est, v) with est = ||B v||_1 / ||v||_1 <= ||B||_1.

    apply(x) returns B x and apply_t(x) returns B^T x. stats (a dict) receives
    "products" (the number of calls to apply and apply_t) and "iterations".
    """
    if n == 0:
        return 0, []
    one = Fraction(1)
    prods = 0
    x = [one / n] * n if n > 1 else [one]  # @line L1
    est, v = None, None
    xi_old = None
    it = 0
    limit = itmax if variant == "higham" else n + 1
    while it < limit:  # @line L2
        it += 1
        y = apply(x)  # @line L3
        prods += 1
        new = sum(abs(t) for t in y)  # @line L4
        if est is not None and new <= est:
            break  # no increase: keep the previous estimate
        est, v = new, x
        xi = [_sign(t) for t in y]  # @line L5
        if variant == "higham" and xi == xi_old:
            break  # repeated sign vector: the next step would repeat too
        z = apply_t(xi)  # @line L6
        prods += 1
        j = max(range(n), key=lambda i: abs(z[i]))  # @line L7
        ztx = sum(p * q for p, q in zip(z, x))
        if (variant == "hager" or it > 1) and abs(z[j]) <= ztx:  # @line L8
            break  # Hager's test: x is a local maximum
        x = [0 * one] * n  # @line L9
        x[j] = one
        xi_old = xi
    if variant == "higham" and n > 1:  # @line L10
        b = [(-1) ** i * (one + one * i / (n - 1)) for i in range(n)]
        y = apply(b)
        prods += 1
        alt = 2 * sum(abs(t) for t in y) / (3 * n)
        if alt > est:
            est, v = alt, b
    if stats is not None:
        stats["products"] = prods
        stats["iterations"] = it
    return est, v  # @line L11


def lu_factor(a):
    """LU with partial pivoting, P A = L U, stored in one matrix. Raises Singular."""
    n = len(a)
    m = [row[:] for row in a]
    piv = list(range(n))
    for k in range(n):
        p = max(range(k, n), key=lambda i: abs(m[i][k]))
        if m[p][k] == 0:
            raise Singular("zero pivot in column %d" % k)
        if p != k:
            m[k], m[p] = m[p], m[k]
            piv[k], piv[p] = piv[p], piv[k]
        for i in range(k + 1, n):
            f = m[i][k] / m[k][k]
            m[i][k] = f
            if f:
                rk, ri = m[k], m[i]
                for j in range(k + 1, n):
                    ri[j] -= f * rk[j]
    return m, piv


def lu_solve(f, b):
    """Solve A x = b with the factors of lu_factor."""
    m, piv = f
    n = len(m)
    y = [b[p] for p in piv]
    for i in range(n):
        s = y[i]
        row = m[i]
        for j in range(i):
            s -= row[j] * y[j]
        y[i] = s
    for i in range(n - 1, -1, -1):
        s = y[i]
        row = m[i]
        for j in range(i + 1, n):
            s -= row[j] * y[j]
        y[i] = s / row[i]
    return y


def lu_solve_t(f, b):
    """Solve A^T x = b with the factors of lu_factor (A^T = U^T L^T P)."""
    m, piv = f
    n = len(m)
    w = list(b)
    for i in range(n):
        s = w[i]
        for j in range(i):
            s -= m[j][i] * w[j]
        w[i] = s / m[i][i]
    for i in range(n - 1, -1, -1):
        s = w[i]
        for j in range(i + 1, n):
            s -= m[j][i] * w[j]
        w[i] = s
    x = [0 * b[0]] * n if n else []
    for k, p in enumerate(piv):
        x[p] = w[k]
    return x


def cond1_estimate(a, variant="higham", itmax=5, stats=None):
    """Estimate kappa_1(A) = ||A||_1 ||A^{-1}||_1 from one LU factorization.

    The estimate is a lower bound of kappa_1(A) in exact arithmetic.
    Raises Singular for a matrix with an exactly zero pivot.
    """
    f = lu_factor(a)
    n = len(a)
    est, _ = norm1_estimate(lambda x: lu_solve(f, x), lambda x: lu_solve_t(f, x), n, variant, itmax, stats)
    return norm1(a) * est
