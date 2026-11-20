# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/periodic-homogenization/. The authors are listed in prov/W15DY8.jsonl.
"""Periodic homogenization: cell problems, the effective coefficient and the corrector.

The model problem is -div(A(x / eps) grad u) = f in a domain, u = 0 on its
boundary, with A(y) symmetric, bounded and uniformly positive, and
1-periodic in each variable y_i. The technique replaces A(x / eps) by a
constant matrix A* computed from cell problems on one period Y = [0, 1)^d.

1D: the cell problem is solved with P1 elements on a periodic mesh of n
cells with one value of a per cell. Its result is the harmonic mean of
the cell values, exactly in Fraction arithmetic.

2D: the cell problem is solved by finite volumes on a periodic n by n grid
of cells, with one value of a per cell and the harmonic mean of the two
cell values on each face. For a laminate this gives the exact A*.

Cost: 1D, Theta(n) with the Thomas algorithm. 2D, the dense solve of
n^2 - 1 unknowns costs Theta(n^6); this is for small checks only.
"""

from fractions import Fraction

from scimat import solve
from scisparse import thomas


def _one(values):
    """1 as a Fraction when the data are exact, else 1.0."""
    return Fraction(1) if all(isinstance(v, (int, Fraction)) for v in values) else 1.0


def cell_problem_1d(a):
    """Solve -(a (1 + chi'))' = 0 on the periodic cell [0, 1) with mean(chi) = 0.

    a[k] is the coefficient on cell k = [k h, (k + 1) h], h = 1 / n.
    Returns (a_star, chi) with chi the nodal values at k h, k = 0..n - 1.
    """
    n = len(a)
    one = _one(a)
    h = one / n
    # In 1D a periodic chi with chi(0) = 0 also has chi(1) = 0, so the
    # unknowns are chi_1 .. chi_(n-1) with zero values at both ends.
    sub = [0] + [-a[i - 1] / h for i in range(2, n)]                           # @line L2
    diag = [(a[i - 1] + a[i]) / h for i in range(1, n)]                        # @line L2
    sup = [-a[i] / h for i in range(1, n - 1)] + [0]                           # @line L2
    rhs = [a[i] - a[i - 1] for i in range(1, n)]                               # @line L2
    inner = thomas(sub, diag, sup, rhs) if n > 1 else []                       # @line L2
    chi = [0 * one] + inner
    mean = sum(chi) / n
    chi = [c - mean for c in chi]                                              # @line L2
    chi_ext = chi + [chi[0]]
    flux = [a[k] * (1 + (chi_ext[k + 1] - chi_ext[k]) / h) for k in range(n)]  # @line L3
    a_star = sum(flux) * h                                                     # @line L3
    return a_star, chi


def cell_problem_2d(a):
    """Effective 2 by 2 matrix of an isotropic coefficient a[j][i] on a periodic n by n grid.

    Cell (i, j) is [i h, (i + 1) h] x [j h, (j + 1) h], i along y_1, j along y_2.
    Returns (A_star, chi1, chi2) with chi_m the cell values of the corrector
    for direction e_m, normalized to mean zero.
    """
    n = len(a)
    one = _one([v for row in a for v in row])
    h = one / n
    N = n * n

    def idx(i, j):
        return (i % n) + n * (j % n)

    def face(p, q):
        return 2 * p * q / (p + q)

    mat = [[0 * one] * N for _ in range(N)]
    rhs = [[0 * one, 0 * one] for _ in range(N)]
    for j in range(n):
        for i in range(n):
            k = idx(i, j)
            east, west = face(a[j][i], a[j][(i + 1) % n]), face(a[j][i], a[j][(i - 1) % n])
            north, south = face(a[j][i], a[(j + 1) % n][i]), face(a[j][i], a[(j - 1) % n][i])
            for m, w in ((idx(i + 1, j), east), (idx(i - 1, j), west), (idx(i, j + 1), north), (idx(i, j - 1), south)):
                mat[k][k] += w / (h * h)                                       # @line L2
                mat[k][m] -= w / (h * h)                                       # @line L2
            rhs[k][0] = (east - west) / h                                      # @line L2
            rhs[k][1] = (north - south) / h                                    # @line L2
    # The periodic system is singular (constants); fix chi = 0 in cell 0.
    red = [row[1:] for row in mat[1:]]
    sol = solve(red, [r for r in rhs[1:]])                                     # @line L2
    chis = []
    for m in range(2):                                                         # @line L1
        chi = [0 * one] + [row[m] for row in sol]
        mean = sum(chi) / N
        chis.append([c - mean for c in chi])                                   # @line L2
    A_star = [[0 * one, 0 * one], [0 * one, 0 * one]]
    for j in range(n):
        for i in range(n):
            k = idx(i, j)
            east = face(a[j][i], a[j][(i + 1) % n])
            north = face(a[j][i], a[(j + 1) % n][i])
            for m in range(2):
                gx = (chis[m][idx(i + 1, j)] - chis[m][k]) / h + (1 if m == 0 else 0)
                gy = (chis[m][idx(i, j + 1)] - chis[m][k]) / h + (1 if m == 1 else 0)
                A_star[0][m] += east * gx / N                                  # @line L3
                A_star[1][m] += north * gy / N                                 # @line L3
    return A_star, chis[0], chis[1]                                            # @line L6


def homogenized_solve_1d(a_star, f, n):
    """P1 solution of -(a_star u0')' = f on (0, 1), u0(0) = u0(1) = 0, on n cells.

    f is a constant. Returns the nodal values at k / n, k = 0..n. For a
    constant coefficient and a constant f the nodal values are exact.
    """
    one = _one([a_star, f])
    h = one / n
    m = n - 1
    sub = [0] + [-a_star / h] * (m - 1)                                       # @line L4
    diag = [2 * a_star / h] * m                                                # @line L4
    sup = [-a_star / h] * (m - 1) + [0]                                       # @line L4
    load = [f * h] * m                                                         # @line L4
    return [0 * one] + thomas(sub, diag, sup, load) + [0 * one]               # @line L4


def corrector_gradient(a, a_star, du0, x, eps):
    """Gradient of u0 + eps u1 with u1 = chi(x / eps) u0'(x), up to O(eps).

    In 1D chi' = a_star / a - 1, so the leading term of the gradient is
    u0'(x) (1 + chi'(x / eps)) = u0'(x) a_star / a(x / eps). a is a
    function of the fast variable y.
    """
    return du0 * a_star / a(x / eps)                                           # @line L5
