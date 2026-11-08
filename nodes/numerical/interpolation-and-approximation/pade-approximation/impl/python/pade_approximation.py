# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pade-approximation/. The authors are listed in prov/Q79FRC.jsonl.

"""Padé approximation from Taylor coefficients.

pade(c, m, n) returns the coefficient lists p (degree <= m) and q (degree
<= n, q[0] = 1) of the [m/n] Padé approximant of f(x) = sum c[k] x^k, using
c[0..m+n]. Works with floats or with fractions.Fraction for exact results.
"""


def _solve(a, b):
    """Gaussian elimination with partial pivoting. Raises ZeroDivisionError
    if the matrix is singular (exactly, for Fraction input)."""
    n = len(a)
    m = [row[:] + [b[i]] for i, row in enumerate(a)]
    for col in range(n):
        piv = max(range(col, n), key=lambda r: abs(m[r][col]))
        if m[piv][col] == 0:
            raise ZeroDivisionError("singular")
        m[col], m[piv] = m[piv], m[col]
        for r in range(col + 1, n):
            f = m[r][col] / m[col][col]
            if f:
                for k in range(col, n + 1):
                    m[r][k] -= f * m[col][k]
    x = [0] * n
    for i in range(n - 1, -1, -1):
        s = m[i][n]
        for j in range(i + 1, n):
            s -= m[i][j] * x[j]
        x[i] = s / m[i][i]
    return x


def pade(c, m, n):
    """Return (p, q) with q[0] = 1 and f q - p = O(x^(m+n+1)).

    Raises ValueError if fewer than m + n + 1 coefficients are given, or if
    the denominator system is singular (the [m/n] entry lies in a block of
    the Padé table and has no normal representation with q[0] = 1 here).
    """
    if m < 0 or n < 0:
        raise ValueError("m and n must be non-negative")
    if len(c) < m + n + 1:
        raise ValueError("need the coefficients c[0..m+n]")
    coef = lambda k: c[k] if k >= 0 else 0 * c[0]
    one = c[0] ** 0 if c[0] != 0 else type(c[0])(1)
    a = [[coef(m + i - j) for j in range(1, n + 1)] for i in range(1, n + 1)]  # @line L1
    b = [-coef(m + i) for i in range(1, n + 1)]  # @line L2
    try:
        qs = _solve(a, b) if n > 0 else []  # @line L3
    except ZeroDivisionError:
        raise ValueError("singular Toeplitz system: [%d/%d] is not normal" % (m, n))
    q = [one] + list(qs)  # @line L4
    p = [sum((q[j] * c[k - j] for j in range(0, min(k, n) + 1)), 0 * one)  # @line L5
         for k in range(m + 1)]
    return p, q  # @line L6


def poly_eval(a, x):
    """Horner's rule for sum a[k] x^k."""
    s = 0 * x
    for ak in reversed(a):
        s = s * x + ak
    return s


def pade_eval(p, q, x):
    """Value of p(x)/q(x)."""
    return poly_eval(p, x) / poly_eval(q, x)


def series_divide(a, b, N):
    """First N Taylor coefficients of a(x)/b(x), with b[0] != 0."""
    out = []
    for k in range(N):
        s = a[k] if k < len(a) else 0 * b[0]
        for j in range(1, min(k, len(b) - 1) + 1):
            s -= b[j] * out[k - j]
        out.append(s / b[0])
    return out
