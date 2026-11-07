# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cyclic-reduction/. The authors are listed in prov/4MBFM8.jsonl.

"""Cyclic (odd-even) reduction for tridiagonal systems.

Row i of the system reads a[i] x[i-1] + b[i] x[i] + c[i] x[i+1] = d[i] for
i = 0..n-1; a[0] and c[n-1] are ignored. Each level eliminates the unknowns
with even index (0-based) from the equations with odd index, which leaves a
tridiagonal system of half the size in the odd unknowns. The work inside a
level is independent across rows, so a parallel machine does a level in O(1)
steps. Entries may be floats or fractions.Fraction. Standard library only.
"""


class ZeroPivot(ValueError):
    """A diagonal entry used as a pivot is zero, so reduction without pivoting fails."""


def reduce_once(a, b, c, d, stats=None):
    """One level of odd-even reduction. Returns the reduced (a, b, c, d) of length n // 2.

    The returned system is the Schur complement of the even unknowns in the
    odd-even permuted matrix. Raises ZeroPivot if an even diagonal entry is zero.
    """
    n = len(b)
    ra, rb, rc, rd = [], [], [], []
    for i in range(1, n, 2):  # @line L3
        if b[i - 1] == 0 or (i + 1 < n and b[i + 1] == 0):
            raise ZeroPivot("zero pivot next to row %d" % i)
        alpha = -a[i] / b[i - 1]  # @line L4
        ai = alpha * a[i - 1]
        bi = b[i] + alpha * c[i - 1]
        di = d[i] + alpha * d[i - 1]
        ci = b[i] * 0
        flops = 6  # one division, three multiplications, two additions
        if i + 1 < n:
            gamma = -c[i] / b[i + 1]  # @line L5
            bi = bi + gamma * a[i + 1]
            ci = gamma * c[i + 1]
            di = di + gamma * d[i + 1]
            flops += 6
        ra.append(ai)  # @line L6
        rb.append(bi)
        rc.append(ci)
        rd.append(di)
        if stats is not None:
            stats["flops"] = stats.get("flops", 0) + flops
    return ra, rb, rc, rd


def cyclic_reduction(a, b, c, d, stats=None):
    """Solve the tridiagonal system by cyclic reduction, without pivoting.

    Precondition for success: every pivot is nonzero, which holds for matrices
    strictly diagonally dominant by rows and for symmetric positive definite
    matrices. Raises ZeroPivot otherwise, in particular for every singular matrix.
    If stats is a dict, it receives "flops" and "levels" (the number of reductions).
    Cost: 17 n - O(log n) flops, depth O(log n), Theta(n) extra storage.
    """
    n = len(b)
    if n == 0:
        return []
    zero = b[0] * 0
    sysm = (list(a[:n]), list(b), list(c[:n]), list(d))  # @line L1
    sysm[0][0] = zero
    sysm[2][n - 1] = zero
    stack = []
    if stats is not None:
        stats.setdefault("flops", 0)
        stats["levels"] = 0
    while len(sysm[1]) > 1:  # @line L2
        stack.append(sysm)
        sysm = reduce_once(*sysm, stats=stats)
        if stats is not None:
            stats["levels"] += 1
    if sysm[1][0] == 0:
        raise ZeroPivot("zero pivot in the last 1 by 1 system")
    x = [sysm[3][0] / sysm[1][0]]  # @line L7
    if stats is not None:
        stats["flops"] += 1
    while stack:  # @line L8
        la, lb, lc, ld = stack.pop()
        m = len(lb)
        full = [zero] * m
        for k, v in enumerate(x):  # @line L9
            full[2 * k + 1] = v
        for i in range(0, m, 2):  # @line L10
            s = ld[i]
            f = 1
            if i > 0:
                s = s - la[i] * full[i - 1]
                f += 2
            if i + 1 < m:
                s = s - lc[i] * full[i + 1]
                f += 2
            full[i] = s / lb[i]  # @line L11
            if stats is not None:
                stats["flops"] += f
        x = full
    return x  # @line L12


def matvec(a, b, c, x):
    """Return A x for the tridiagonal matrix (a, b, c)."""
    n = len(b)
    y = []
    for i in range(n):
        s = b[i] * x[i]
        if i > 0:
            s += a[i] * x[i - 1]
        if i + 1 < n:
            s += c[i] * x[i + 1]
        y.append(s)
    return y


def backward_error(a, b, c, d, x):
    """Normwise backward error ||d - A x||_inf / (||A||_inf ||x||_inf + ||d||_inf)."""
    n = len(b)
    r = [di - yi for di, yi in zip(d, matvec(a, b, c, x))]
    na = max(abs(b[i]) + (abs(a[i]) if i > 0 else 0) + (abs(c[i]) if i + 1 < n else 0) for i in range(n))
    den = na * max(abs(v) for v in x) + max(abs(v) for v in d)
    return 0.0 if den == 0 else max(abs(v) for v in r) / den
