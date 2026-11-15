# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ackermann-formula/. The authors are listed in prov/DZTY4S.jsonl.

"""Ackermann's formula for single-input pole placement.

For x' = A x + b u (or x_(k+1) = A x_k + b u_k) with one input and the
control u = -K x, the closed-loop matrix is A - b K. If (A, b) is
controllable, the only row vector K with det(s I - (A - b K)) = p(s) for a
given monic p of degree n is

    K = [0 ... 0 1] W^(-1) p(A),    W = [b, A b, ..., A^(n-1) b].

The code computes q^T = e_n^T W^(-1) by one linear solve W^T q = e_n, so W
is never inverted, and then K = q^T p(A) by Horner's rule on row vectors,
K <- K A + p_i q^T, so p(A) is never formed. The cost is O(n^3).
With int and Fraction data the result is exact. With
float data the formula is numerically unstable for larger n, because W is
then badly conditioned (see the page).
"""

from fractions import Fraction

from ctlmat import matvec, mul, polymul, solve, transpose, zeros

__all__ = ["controllability_matrix", "poly_of_matrix", "poly_from_roots", "ackermann", "ackermann_poles"]


def controllability_matrix(A, b):
    """Return W = [b, A b, ..., A^(n-1) b] for a flat vector b."""
    n = len(A)
    if len(b) != n or any(len(row) != n for row in A):
        raise ValueError("A must be n by n and b must have n entries")
    cols = [list(b)]
    for _ in range(n - 1):
        cols.append(matvec(A, cols[-1]))
    return transpose(cols)


def poly_of_matrix(p, A):
    """Return p(A) = p_0 A^n + p_1 A^(n-1) + ... + p_n I by Horner's rule."""
    n = len(A)
    P = zeros(n)
    for c in p:
        P = mul(A, P)
        for i in range(n):
            P[i][i] += c
    return P


def poly_from_roots(roots):
    """Return the monic polynomial with the given roots, highest power first.

    Exact roots (int, Fraction) give exact coefficients. If the roots are
    closed under complex conjugation, the tiny imaginary parts of the
    coefficients are removed and the coefficients are real floats.
    """
    p = [1]
    for r in roots:
        p = polymul(p, [1, -r])
    if any(isinstance(c, complex) for c in p):
        big = max(abs(c) for c in p)
        if all(abs(complex(c).imag) <= 1e-12 * big for c in p):
            p = [complex(c).real for c in p]
    return p


def ackermann(A, b, p):
    """Return the row vector K (a flat list) with charpoly(A - b K) = p.

    p is monic of degree n, highest power first. Raises ValueError if p has
    the wrong form or if (A, b) is not controllable (W is singular).
    """
    n = len(A)
    if len(p) != n + 1 or p[0] != 1:
        raise ValueError("p must be monic of degree n")
    W = controllability_matrix(A, b)  # @line L1
    e_n = [0] * (n - 1) + [1]
    try:
        q = solve(transpose(W), e_n)  # @line L2
    except ValueError:
        raise ValueError("(A, b) is not controllable") from None
    At = transpose(A)
    K = [0] * n
    for c in p:  # @line L3
        K = [x + c * y for x, y in zip(matvec(At, K), q)]  # @line L4
    return K  # @line L5


def ackermann_poles(A, b, poles):
    """Return K that places the eigenvalues of A - b K at the given poles.

    Complex poles must come in conjugate pairs, so that K is real.
    """
    if len(poles) != len(A):
        raise ValueError("give exactly n poles")
    p = poly_from_roots(poles)
    if any(isinstance(c, complex) for c in p):
        raise ValueError("complex poles must come in conjugate pairs")
    return ackermann(A, b, p)


if __name__ == "__main__":
    h = Fraction(1, 10)
    print(ackermann([[0, 1], [0, 0]], [0, 1], [1, 2, 2]))
    print(ackermann([[1, h], [0, 1]], [h * h / 2, h], [1, 0, 0]))
