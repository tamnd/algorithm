# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lemke-algorithm/. The authors are listed in prov/8FV1QP.jsonl.
"""Lemke's complementary pivot algorithm for the linear complementarity problem, in Fraction.

The problem LCP(M, q): find z >= 0 with w = M z + q >= 0 and z . w = 0. The tableau is
w - M z - d z0 = q, with a covering vector d > 0 (all ones by default). Column i is w_i,
column n + i is z_i and column 2 n is the artificial variable z0. The minimum ratio test is
lexicographic, which is the same as perturbing q by (eps, eps^2, ..., eps^n); so the method
ends on every input, also on degenerate ones.
"""

from fractions import Fraction


def _complement(v, n):
    return v + n if v < n else v - n


def lemke(M, q, d=None, trace=None):
    """Solve LCP(M, q) with Lemke's method.

    Return ("solution", z, w) or ("ray", None, None). Ray termination means that the method
    found an unbounded edge; for P-matrices it never happens, and for copositive-plus matrices
    (for example positive semidefinite ones) it happens only if z >= 0, M z + q >= 0 has no solution.
    If trace is a list, the pair (entering column, leaving column) of each pivot is appended to it.
    """
    n = len(q)
    q = [Fraction(v) for v in q]
    if all(v >= 0 for v in q):  # @line L1
        return "solution", [Fraction(0)] * n, list(q)
    d = [Fraction(1)] * n if d is None else [Fraction(v) for v in d]
    if any(v <= 0 for v in d):
        raise ValueError("the covering vector d must be positive")
    rows = [[Fraction(int(c == i)) for c in range(n)] + [-Fraction(M[i][j]) for j in range(n)]
            + [-d[i], q[i]] for i in range(n)]  # @line L2
    basis = list(range(n))

    def key(r, col):
        # (rhs, the w columns, which hold the inverse of the basis), divided by the pivot entry
        a = rows[r][col]
        return tuple(rows[r][c] / a for c in [-1] + list(range(n)))

    def pivot(r, col):
        p = rows[r][col]
        rows[r] = [v / p for v in rows[r]]
        for i in range(n):
            f = rows[i][col]
            if i != r and f != 0:
                rows[i] = [a - f * b for a, b in zip(rows[i], rows[r])]
        leaving, basis[r] = basis[r], col
        if trace is not None:
            trace.append((col, leaving))
        return leaving

    z0 = 2 * n
    # The column of z0 is -d; z0 enters at the row of the lexicographic minimum of q_i / d_i.
    r = min(range(n), key=lambda i: tuple(rows[i][c] / d[i] for c in [-1] + list(range(n))))  # @line L3
    entering = _complement(pivot(r, z0), n)  # @line L4
    while True:  # @line L5
        cand = [i for i in range(n) if rows[i][entering] > 0]
        if not cand:  # @line L6
            return "ray", None, None
        r = min(cand, key=lambda i: key(i, entering))
        leaving = pivot(r, entering)  # @line L7
        if leaving == z0:
            vals = [Fraction(0)] * (2 * n + 1)
            for i, c in enumerate(basis):
                vals[c] = rows[i][-1]
            return "solution", vals[n:2 * n], vals[:n]
        entering = _complement(leaving, n)  # @line L8


def bimatrix_lcp(A, B):
    """Return (M, q) of an LCP whose solutions z = (x, y) give the equilibria (x / sum x, y / sum y).

    Shift A and B to A', B' >= 1 and form the symmetric game S = [[0, A'], [B'^T, 0]] of size
    m + n. With K = 1 + the largest entry of S, the cost matrix M = K - S is positive, so it is
    strictly copositive and Lemke's method with d = 1 ends with a solution of LCP(M, -1).
    In a solution, the rows i < m with z_i > 0 maximize (A' y)_i and the rows m + j with
    z_(m+j) > 0 maximize (B'^T x)_j, and both parts of z are nonzero.
    """
    m, n = len(A), len(A[0])
    c = 1 - min(min(min(r) for r in A), min(min(r) for r in B), 1)
    S = [[Fraction(0)] * (m + n) for _ in range(m + n)]
    for i in range(m):
        for j in range(n):
            S[i][m + j] = Fraction(A[i][j]) + c
            S[m + j][i] = Fraction(B[i][j]) + c
    K = 1 + max(max(r) for r in S)
    return [[K - v for v in r] for r in S], [Fraction(-1)] * (m + n)


def bimatrix_equilibrium(A, B):
    """Return a Nash equilibrium (x, y) of (A, B), found by Lemke's method on bimatrix_lcp(A, B)."""
    m = len(A)
    M, q = bimatrix_lcp(A, B)
    status, z, _ = lemke(M, q)
    if status != "solution":
        raise AssertionError("Lemke's method does not end on a ray for this LCP")
    x, y = z[:m], z[m:]
    return [v / sum(x) for v in x], [v / sum(y) for v in y]
