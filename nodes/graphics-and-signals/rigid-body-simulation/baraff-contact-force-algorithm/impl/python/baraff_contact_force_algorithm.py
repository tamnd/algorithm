# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/baraff-contact-force-algorithm/. The authors are listed in prov/APAZTF.jsonl.

"""Baraff's frictionless contact force algorithm (Dantzig's pivoting method for the LCP).

Given a symmetric positive semidefinite matrix A and a vector b, find f with

    f >= 0,  a = A f + b >= 0,  f_i a_i = 0 for every i.

In contact mechanics, f_i is the normal force at contact i and a_i the normal
relative acceleration there (Baraff, SIGGRAPH 94, Section 4). The algorithm
keeps a set C of clamped contacts (a_i = 0) and a set NC of contacts that do
not push (f_i = 0), and raises one force f_d at a time until a_d = 0.

All arithmetic is exact if the input is given as Fraction values. The linear
systems are solved by Gaussian elimination, as in Baraff's first
implementation.
"""

from fractions import Fraction


def solve(M, rhs):
    """Solve M x = rhs by Gaussian elimination with partial pivoting. Raise on a singular M."""
    n = len(rhs)
    aug = [list(M[i]) + [rhs[i]] for i in range(n)]
    for col in range(n):
        piv = max(range(col, n), key=lambda r: abs(aug[r][col]))
        if aug[piv][col] == 0:
            raise ZeroDivisionError("singular submatrix A_CC")
        aug[col], aug[piv] = aug[piv], aug[col]
        for r in range(col + 1, n):
            factor = aug[r][col] / aug[col][col]
            if factor:
                for c in range(col, n + 1):
                    aug[r][c] -= factor * aug[col][c]
    x = [0] * n
    for r in range(n - 1, -1, -1):
        s = aug[r][n] - sum(aug[r][c] * x[c] for c in range(r + 1, n))
        x[r] = s / aug[r][r]
    return x


def matvec(A, x):
    return [sum(A[i][j] * x[j] for j in range(len(x))) for i in range(len(A))]


def fdirection(A, C, d):
    """The force change df with df_d = 1, df_i = 0 outside C + {d}, and (A df)_i = 0 for i in C."""
    n = len(A)
    df = [0] * n  # @line L12
    df[d] = 1  # @line L12
    idx = sorted(C)
    if idx:
        x = solve([[A[i][j] for j in idx] for i in idx], [-A[i][d] for i in idx])  # @line L13
        for i, xi in zip(idx, x):  # @line L14
            df[i] = xi  # @line L14
    return df  # @line L14


def maxstep(f, a, df, da, C, NC, d):
    """The largest step s along df that keeps the invariants, and the index j that limits it."""
    s, j = None, None  # @line L15
    if da[d] > 0:  # @line L16
        s, j = -a[d] / da[d], d  # @line L16
    for i in sorted(C):  # @line L17
        if df[i] < 0:  # @line L17
            s1 = -f[i] / df[i]  # @line L17
            if s is None or s1 < s:  # @line L17
                s, j = s1, i  # @line L17
    for i in sorted(NC):  # @line L18
        if da[i] < 0:  # @line L18
            s1 = -a[i] / da[i]  # @line L18
            if s is None or s1 < s:  # @line L18
                s, j = s1, i  # @line L18
    return s, j  # @line L19


def drive_to_zero(A, f, a, C, NC, d, trace=None, max_pivots=10000):
    for _ in range(max_pivots):  # @line L5
        df = fdirection(A, C, d)  # @line L6
        da = matvec(A, df)  # @line L6
        s, j = maxstep(f, a, df, da, C, NC, d)  # @line L7
        if j is None:
            raise ArithmeticError("no step limit: the LCP has no solution")
        for i in range(len(f)):  # @line L8
            f[i] += s * df[i]  # @line L8
            a[i] += s * da[i]  # @line L8
        if j in C:  # @line L9
            C.remove(j)  # @line L9
            NC.add(j)  # @line L9
            f[j] = 0 * f[j]
            move = "C to NC"
        elif j in NC:  # @line L10
            NC.remove(j)  # @line L10
            C.add(j)  # @line L10
            a[j] = 0 * a[j]
            move = "NC to C"
        else:  # @line L11
            C.add(j)  # @line L11
            a[j] = 0 * a[j]
            move = "d to C"
        if trace is not None:
            trace.append((d, j, move, s))
        if move == "d to C":
            return  # @line L11
    raise RuntimeError("too many pivots")


def compute_forces(A, b, trace=None):
    """Return (f, a, C) with f >= 0, a = A f + b >= 0 and f . a = 0."""
    n = len(b)
    f = [0 * b[i] for i in range(n)]  # @line L1
    a = list(b)  # @line L1
    C, NC = set(), set()  # @line L2
    while True:  # @line L3
        neg = [i for i in range(n) if a[i] < 0]  # @line L3
        if not neg:  # @line L3
            return f, a, C
        drive_to_zero(A, f, a, C, NC, neg[0], trace)  # @line L4


def is_solution(A, b, f, a):
    """Check the LCP conditions exactly."""
    return (all(x >= 0 for x in f) and all(y >= 0 for y in a) and all(x * y == 0 for x, y in zip(f, a))
            and a == [p + q for p, q in zip(matvec(A, f), b)])


def box_contact_matrix(m, I, xs):
    """A and the map from external accelerations to b for a 2D body on contacts below it.

    The contacts are at the horizontal offsets xs from the center of mass, the
    normal is +y, and the body is at rest, so a_i = acc_y + alpha * x_i."""
    A = [[1 / Fraction(m) + Fraction(xi) * xj / Fraction(I) for xj in xs] for xi in xs]
    return A
