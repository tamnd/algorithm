# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/schur-method-riccati/. The authors are listed in prov/TKPRJX.jsonl.

"""Schur method for the algebraic Riccati equations (Laub 1979).

Continuous time (CARE): A^T P + P A - P G P + Q = 0 with G = B R^(-1) B^T.
The Hamiltonian matrix H = [[A, -G], [-Q, -A^T]] is reduced to an upper
triangular Schur form T = Z^* H Z with a unitary Z. The diagonal of T is
reordered so that the n eigenvalues with negative real part come first.
Then the first n columns of Z, split as [U1; U2], span the stable invariant
subspace of H, and P = U2 U1^(-1). The gain is K = R^(-1) B^T P.

Discrete time (DARE): P = A^T P A - A^T P B (R + B^T P B)^(-1) B^T P A + Q.
The same steps are applied to the symplectic matrix

    S = [[A + G A^(-T) Q, -G A^(-T)], [-A^(-T) Q, A^(-T)]],

with the eigenvalues inside the unit circle put first. This form needs A to
be invertible.

Laub used the real Schur form, with 2 by 2 blocks for complex pairs. This
file uses the complex Schur form, which has only 1 by 1 blocks and so needs
only one kind of swap. The Schur form is computed by a reduction to
Hessenberg form with Givens rotations and an explicit shifted QR iteration
with the Wilkinson shift and deflation.

The functions raise ValueError if H (or S) has an eigenvalue on or near the
imaginary axis (or the unit circle), if the number of stable eigenvalues is
not n, or if U1 is singular or nearly singular. In each case the equation
has no stabilizing solution, or the data is too close to such a case.
"""

import cmath
import math

from ctlmat import add, block, inv, mul, norm2, scale, solve, sub, transpose

__all__ = [
    "hamiltonian", "symplectic", "schur_form", "swap", "reorder",
    "care_schur", "dare_schur", "care_residual", "dare_residual",
]

EPS = 2.0 ** -52


def _float(a):
    return [[float(v) for v in row] for row in a]


def _fro(a):
    return math.sqrt(sum(abs(v) ** 2 for row in a for v in row))


def _g(B, R):
    return _float(mul(B, solve(R, transpose(B))))


def hamiltonian(A, B, Q, R):
    """Return H = [[A, -G], [-Q, -A^T]] with G = B R^(-1) B^T, in float."""
    g = _g(B, R)
    a = _float(A)
    return block([[a, scale(-1.0, g)], [scale(-1.0, _float(Q)), scale(-1.0, transpose(a))]])


def symplectic(A, B, Q, R):
    """Return [[A + G A^(-T) Q, -G A^(-T)], [-A^(-T) Q, A^(-T)]] for the DARE.

    Raises ValueError if A is singular.
    """
    a = _float(A)
    q = _float(Q)
    g = _g(B, R)
    ait = transpose(inv(a))
    return block([
        [add(a, mul(g, mul(ait, q))), scale(-1.0, mul(g, ait))],
        [scale(-1.0, mul(ait, q)), ait],
    ])


def _rot(a, b):
    """Return (c, s) such that [[c, s], [-conj(s), c]] maps (a, b) to (r, 0)."""
    if b == 0:
        return 1.0, 0j
    if a == 0:
        return 0.0, 1 + 0j
    aa = abs(a)
    r = math.hypot(aa, abs(b))
    return aa / r, (a / aa) * b.conjugate() / r


def _left(t, i, j, c, s):
    """Rows i, j of t become c row_i + s row_j and -conj(s) row_i + c row_j."""
    ri, rj = t[i], t[j]
    sc = s.conjugate()
    for k in range(len(ri)):
        x, y = ri[k], rj[k]
        ri[k] = c * x + s * y
        rj[k] = -sc * x + c * y


def _right(t, i, j, c, s):
    """Multiply columns i, j of t on the right by the conjugate transpose of the rotation."""
    sc = s.conjugate()
    for row in t:
        x, y = row[i], row[j]
        row[i] = c * x + sc * y
        row[j] = -s * x + c * y


def _similar(t, z, i, j, c, s):
    _left(t, i, j, c, s)
    _right(t, i, j, c, s)
    _right(z, i, j, c, s)


def _wilkinson(a, b, c, d):
    """Return the eigenvalue of [[a, b], [c, d]] that is nearest to d."""
    h = (a - d) / 2
    disc = cmath.sqrt(h * h + b * c)
    den = h + disc if abs(h + disc) >= abs(h - disc) else h - disc
    if den == 0:
        return d
    return d - b * c / den


def schur_form(M, max_steps=30):
    """Return (T, Z) with Z unitary, T upper triangular and M = Z T Z^*.

    Entries are complex. Givens rotations reduce M to Hessenberg form, then
    the explicit shifted QR iteration with the Wilkinson shift reduces it to
    triangular form. A subdiagonal entry is set to 0 when it is below EPS
    times the sum of its two diagonal neighbours (or EPS times the norm of
    M). Raises ValueError after max_steps QR steps without a deflation.
    """
    n = len(M)
    t = [[complex(v) for v in row] for row in M]
    z = [[1 + 0j if i == j else 0j for j in range(n)] for i in range(n)]
    for j in range(n - 2):
        for i in range(n - 1, j + 1, -1):
            if t[i][j] != 0:
                c, s = _rot(t[i - 1][j], t[i][j])
                _similar(t, z, i - 1, i, c, s)
                t[i][j] = 0j
    hnorm = _fro(t)
    hi = n - 1
    steps = 0
    while hi > 0:
        l = hi
        while l > 0:
            sub_ = abs(t[l][l - 1])
            if sub_ <= EPS * (abs(t[l - 1][l - 1]) + abs(t[l][l])) or sub_ <= EPS * hnorm:
                t[l][l - 1] = 0j
                break
            l -= 1
        if l == hi:
            hi -= 1
            steps = 0
            continue
        steps += 1
        if steps > max_steps:
            raise ValueError("schur_form: the QR iteration does not converge")
        if steps % 10 == 0:
            mu = t[hi][hi] + abs(t[hi][hi - 1]) * (0.75 + 0.5j)
        else:
            mu = _wilkinson(t[hi - 1][hi - 1], t[hi - 1][hi], t[hi][hi - 1], t[hi][hi])
        for k in range(l, hi + 1):
            t[k][k] -= mu
        rots = []
        for k in range(l, hi):
            c, s = _rot(t[k][k], t[k + 1][k])
            _left(t, k, k + 1, c, s)
            t[k + 1][k] = 0j
            rots.append((k, c, s))
        for k, c, s in rots:
            _right(t, k, k + 1, c, s)
            _right(z, k, k + 1, c, s)
        for k in range(l, hi + 1):
            t[k][k] += mu
    for i in range(n):
        for j in range(i):
            t[i][j] = 0j
    return t, z


def swap(T, Z, k):
    """Swap the diagonal entries k and k + 1 of the triangular T in place.

    A Givens rotation G is built from the eigenvector (T[k][k+1], t2 - t1) of
    the 2 by 2 block, and T becomes G T G^*, Z becomes Z G^*.
    """
    t1, t2 = T[k][k], T[k + 1][k + 1]
    if t1 == t2:
        return
    c, s = _rot(T[k][k + 1], t2 - t1)
    _similar(T, Z, k, k + 1, c, s)
    T[k + 1][k] = 0j
    T[k][k] = t2
    T[k + 1][k + 1] = t1


def reorder(T, Z, select):
    """Move the diagonal entries d with select(d) true to the front, in place.

    Returns the number of selected entries. The relative order inside each
    group is kept.
    """
    pos = 0
    for i in range(len(T)):
        if select(T[i][i]):
            for k in range(i - 1, pos - 1, -1):
                swap(T, Z, k)
            pos += 1
    return pos


def _solve_basis(M, n, stable, margin, axis_tol, cond_tol):
    """Return P = U2 U1^(-1) from the stable invariant subspace of the 2n by 2n matrix M.

    stable(d) selects the wanted eigenvalues, and margin(d) is the distance
    of d from the stability boundary. Cost O(n^3) flops in the usual case.
    """
    T, Z = schur_form(M)  # @line L2
    scale_ = max(_fro(M), 1e-300)
    for i in range(2 * n):  # @line L3
        if margin(T[i][i]) <= axis_tol * scale_:
            raise ValueError("an eigenvalue lies on or near the stability boundary")
    count = reorder(T, Z, stable)  # @line L4
    if count != n:
        raise ValueError("the number of stable eigenvalues is not n")
    u1 = [row[:n] for row in Z[:n]]  # @line L5
    u2 = [row[:n] for row in Z[n:]]
    try:
        u1_inv = inv(u1)
    except ValueError:
        raise ValueError("U1 is singular: no stabilizing solution") from None
    if 1.0 / norm2(u1_inv) < cond_tol:
        raise ValueError("U1 is nearly singular: no stabilizing solution")
    pt = solve(transpose(u1), transpose(u2))  # @line L6
    p = [[v.real for v in row] for row in transpose(pt)]  # @line L7
    return p, T, Z


def care_schur(A, B, Q, R, axis_tol=1e-8, cond_tol=1e-10, symmetrize=True):
    """Return (P, K) for the stabilizing solution of the CARE by the Schur method.

    P solves A^T P + P A - P B R^(-1) B^T P + Q = 0, K = R^(-1) B^T P and
    A - B K is Hurwitz. With symmetrize=False the computed P is returned
    without the final (P + P^T) / 2.

    Precondition: R is symmetric positive definite and Q is symmetric. The
    result exists if (A, B) is stabilizable and H has no eigenvalue on the
    imaginary axis (for example if (Q^(1/2), A) is detectable). Cost: O(n^3)
    flops when each eigenvalue needs a bounded number of QR steps, which is
    the usual case; O(c n^3) with at most c QR steps per eigenvalue.
    """
    n = len(A)
    h = hamiltonian(A, B, Q, R)  # @line L1
    p, _, _ = _solve_basis(h, n, lambda d: d.real < 0, lambda d: abs(d.real), axis_tol, cond_tol)
    if symmetrize:
        p = [[(p[i][j] + p[j][i]) / 2 for j in range(n)] for i in range(n)]
    k = _float(solve(R, mul(transpose(B), p)))
    return p, k  # @line L8


def dare_schur(A, B, Q, R, axis_tol=1e-8, cond_tol=1e-10, symmetrize=True):
    """Return (P, K) for the stabilizing solution of the DARE by the Schur method.

    P solves P = A^T P A - A^T P B (R + B^T P B)^(-1) B^T P A + Q,
    K = (R + B^T P B)^(-1) B^T P A and A - B K is Schur. A must be invertible.
    """
    n = len(A)
    try:
        s = symplectic(A, B, Q, R)
    except ValueError:
        raise ValueError("dare_schur: A is singular") from None
    p, _, _ = _solve_basis(s, n, lambda d: abs(d) < 1, lambda d: abs(abs(d) - 1), axis_tol, cond_tol)
    if symmetrize:
        p = [[(p[i][j] + p[j][i]) / 2 for j in range(n)] for i in range(n)]
    pb = mul(p, _float(B))
    k = solve(add(_float(R), mul(transpose(_float(B)), pb)), mul(transpose(pb), _float(A)))
    return p, k


def care_residual(A, B, Q, R, P):
    """Return A^T P + P A - P G P + Q with G = B R^(-1) B^T."""
    a = _float(A)
    g = _g(B, R)
    return add(sub(add(mul(transpose(a), P), mul(P, a)), mul(P, mul(g, P))), _float(Q))


def dare_residual(A, B, Q, R, P):
    """Return A^T P A - A^T P B (R + B^T P B)^(-1) B^T P A + Q - P."""
    a = _float(A)
    b = _float(B)
    pb = mul(P, b)
    k = solve(add(_float(R), mul(transpose(b), pb)), mul(transpose(pb), a))
    at = transpose(a)
    return sub(add(sub(mul(at, mul(P, a)), mul(at, mul(pb, k))), _float(Q)), P)
