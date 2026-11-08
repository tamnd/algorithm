# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chebyshev-economization/. The authors are listed in prov/4BG9SS.jsonl.
"""Chebyshev economization of a polynomial given by monomial coefficients on [-1, 1].

Works with float or Fraction coefficients (Fraction gives exact results).
"""


def _times_x(c):
    """Chebyshev coefficients of x * sum c[j] T_j, using x T_0 = T_1 and
    x T_j = (T_{j+1} + T_{j-1}) / 2 for j >= 1."""
    n = len(c)
    d = [0 * c[0]] * (n + 1)
    d[1] = d[1] + c[0]
    for j in range(1, n):
        h = c[j] / 2
        d[j + 1] = d[j + 1] + h
        d[j - 1] = d[j - 1] + h
    return d


def power_to_chebyshev(b):
    """Chebyshev coefficients c with sum c[k] T_k = sum b[k] x^k."""
    if not b:
        raise ValueError("need at least one coefficient")
    c = [b[-1]]  # @line L1
    for k in range(len(b) - 2, -1, -1):  # @line L2
        c = _times_x(c)
        c[0] = c[0] + b[k]
    return c


def economize(b, tol):
    """Drop trailing Chebyshev terms whose absolute values sum to at most tol.

    Returns (c, e): the kept coefficients c[0..m] and the bound e, the sum of
    the dropped |c_k|, so that |p(x) - sum c[k] T_k(x)| <= e on [-1, 1].
    """
    if tol < 0:
        raise ValueError("tol must be nonnegative")
    c = power_to_chebyshev(b)
    m = len(c) - 1  # @line L3
    e = 0 * c[0]
    while m > 0 and e + abs(c[m]) <= tol:
        e = e + abs(c[m])
        m -= 1
    return c[:m + 1], e  # @line L4


def chebyshev_to_power(c):
    """Monomial coefficients of sum c[k] T_k (unstable in floating point for large degree)."""
    zero = 0 * c[0]
    a = [zero] * len(c)
    t_prev, t_cur = None, [zero + 1]  # T_0 = 1
    for k in range(len(c)):  # @line L5
        if k == 1:
            t_prev, t_cur = t_cur, [zero, zero + 1]
        elif k >= 2:
            nxt = [zero] + [2 * v for v in t_cur]
            for i, v in enumerate(t_prev):
                nxt[i] = nxt[i] - v
            t_prev, t_cur = t_cur, nxt
        for i, v in enumerate(t_cur):  # @line L6
            a[i] = a[i] + c[k] * v
    return a


def clenshaw(c, x):
    """Evaluate sum c[k] T_k(x)."""
    b1 = b2 = 0 * c[0]
    for k in range(len(c) - 1, 0, -1):
        b1, b2 = c[k] + 2 * x * b1 - b2, b1
    return c[0] + x * b1 - b2


def horner(b, x):
    s = 0 * b[0]
    for v in reversed(b):
        s = s * x + v
    return s
