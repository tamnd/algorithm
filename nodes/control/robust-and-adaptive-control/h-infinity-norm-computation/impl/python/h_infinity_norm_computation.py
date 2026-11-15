# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/h-infinity-norm-computation/. The authors are listed in prov/KBHPWA.jsonl.

"""H-infinity norm of a stable state-space system by Hamiltonian tests.

The system is x' = A x + B u, y = C x + D u with A Hurwitz (n by n), B
(n by m), C (p by n) and D (p by m). Matrices are lists of rows. The
transfer matrix is G(s) = C (s I - A)^(-1) B + D, and the H-infinity norm is
the supremum over real w of the largest singular value of G(j w).

The test behind both methods (pseudocode lines L1 to L3): for gamma larger
than the largest singular value of D, gamma is a singular value of G(j w)
if and only if j w is an eigenvalue of the Hamiltonian matrix

    H = [[A, 0], [0, -A^T]] + [[B, 0], [0, -C^T]] M^(-1) [[-C, 0], [0, -B^T]],
    M = [[D, -gamma I_p], [-gamma I_m, D^T]].

The characteristic polynomial of H is even, det(s I - H) = r(s^2), so the
imaginary eigenvalues j w are the real roots t = -w^2 <= 0 of r.

- hinf_norm_bisection: the bisection of Boyd, Balakrishnan and Kabamba
  (1989), lines L4 to L10.
- hinf_norm_level_set: the level set iteration of Bruinsma and Steinbuch
  (1990) and Boyd and Balakrishnan (1990), lines L11 to L16.

Both return an interval [lo, hi] that holds the norm, with
hi - lo <= 2 eps lo. Floating point tolerances: the characteristic
polynomial comes from ctlmat.charpoly and its roots from ctlmat.polyroots.
A root t of r is taken as real if |Im t| <= IMAG_TOL (1 + |t|), and as
nonpositive if Re t <= SIGN_TOL (1 + |t|). A double root of r (a tangent
of the singular value curve to the level gamma) is computed with an error
near 1e-8, so a decision can be wrong only when gamma is within about
1e-12 (relative) of the norm.
"""

import math

from ctlmat import (add, block, charpoly, eye, kron, mul, norm2, polyroots,
                    scale, solve, transpose, unvec, vec, zeros)

IMAG_TOL = 1e-6
SIGN_TOL = 1e-10
MAX_ITER = 500


def eigenvalues(a):
    """Eigenvalues of a small square matrix, as roots of its characteristic polynomial."""
    return polyroots(charpoly([[float(v) for v in row] for row in a]))


def is_hurwitz(a):
    """True if every eigenvalue of a has a negative real part."""
    return all(lam.real < 0 for lam in eigenvalues(a))


def freq_response(A, B, C, D, w):
    """Return G(j w) = C (j w I - A)^(-1) B + D as a complex matrix."""
    n = len(A)
    jwa = [[(1j * w if i == j else 0) - A[i][j] for j in range(n)] for i in range(n)]
    x = solve(jwa, [[complex(v) for v in row] for row in B])
    g = mul(C, x)
    return [[g[i][j] + D[i][j] for j in range(len(D[0]))] for i in range(len(D))]


def sigma_max(A, B, C, D, w):
    """Largest singular value of G(j w)."""
    return norm2(freq_response(A, B, C, D, w))


def hamiltonian(A, B, C, D, gamma):
    """The Hamiltonian matrix H_gamma (exact when the data and gamma are int or Fraction)."""
    n, m, p = len(A), len(B[0]), len(C)
    big_m = block([[D, scale(-gamma, eye(p))], [scale(-gamma, eye(m)), transpose(D)]])
    right = block([[scale(-1, C), zeros(p, n)], [zeros(m, n), scale(-1, transpose(B))]])
    left = block([[B, zeros(n, p)], [zeros(n, m), scale(-1, transpose(C))]])
    h0 = block([[A, zeros(n)], [zeros(n), scale(-1, transpose(A))]])
    return add(h0, mul(left, solve(big_m, right)))


def even_polynomial(h):
    """The coefficients of r with det(s I - h) = r(s^2), highest power first."""
    c = charpoly(h)
    return [c[k] for k in range(0, len(c), 2)]


def imaginary_frequencies(A, B, C, D, gamma):
    """The w >= 0 such that j w is an eigenvalue of H_gamma, sorted."""
    h = hamiltonian(A, B, C, D, gamma)  # @line L1
    r = even_polynomial([[float(v) for v in row] for row in h])  # @line L2
    out = []
    for t in polyroots(r):  # @line L3
        if abs(t.imag) <= IMAG_TOL * (1 + abs(t)) and t.real <= SIGN_TOL * (1 + abs(t)):
            out.append(math.sqrt(max(0.0, -t.real)))
    return sorted(out)


def gramians(A, B, C):
    """Controllability and observability gramians of a Hurwitz A.

    A W_c + W_c A^T + B B^T = 0 and A^T W_o + W_o A + C^T C = 0, solved
    through the Kronecker form (I kron A + A kron I) vec(W) = -vec(B B^T).
    """
    n = len(A)
    at = transpose(A)
    k_c = add(kron(eye(n), A), kron(A, eye(n)))
    k_o = add(kron(eye(n), at), kron(at, eye(n)))
    wc = unvec(solve(k_c, [-v for v in vec(mul(B, transpose(B)))]), n)
    wo = unvec(solve(k_o, [-v for v in vec(mul(transpose(C), C))]), n)
    return wc, wo


def hankel_singular_values(A, B, C):
    """Square roots of the eigenvalues of W_c W_o, largest first."""
    wc, wo = gramians(A, B, C)
    lam = eigenvalues(mul(wc, wo))
    return sorted((math.sqrt(max(v.real, 0.0)) for v in lam), reverse=True)


def hinf_norm_bisection(A, B, C, D, eps=1e-8):
    """Bisection on gamma. Returns (lo, hi, iterations) with lo <= norm <= hi."""
    if not is_hurwitz(A):  # @line L4
        raise ValueError("A is not Hurwitz")
    d = norm2(D)
    hsv = hankel_singular_values(A, B, C)  # @line L5
    lo = max(d, hsv[0])  # @line L6
    hi = max(lo, d + 2 * sum(hsv))
    iterations = 0
    while hi - lo > 2 * eps * lo:  # @line L7
        gamma = (lo + hi) / 2  # @line L8
        if imaginary_frequencies(A, B, C, D, gamma):  # @line L9
            lo = gamma
        else:
            hi = gamma
        iterations += 1
    return lo, hi, iterations  # @line L10


def hinf_norm_level_set(A, B, C, D, eps=1e-8):
    """Level set iteration. Returns (lo, hi, w, iterations).

    lo is the largest singular value of G(j w) at the returned w (w is
    math.inf when lo comes from D), and lo <= norm <= hi.
    """
    if not is_hurwitz(A):  # @line L11
        raise ValueError("A is not Hurwitz")
    lb, w_lb = norm2(D), math.inf
    for w in [0.0] + [abs(lam) for lam in eigenvalues(A)]:
        s = sigma_max(A, B, C, D, w)
        if s > lb:
            lb, w_lb = s, w
    if lb == 0:
        raise ValueError("G is zero at 0, at infinity and at the pole moduli; use the bisection")
    iterations = 0
    while iterations < MAX_ITER:  # @line L12
        gamma = (1 + 2 * eps) * lb  # @line L13
        freqs = imaginary_frequencies(A, B, C, D, gamma)
        if not freqs:  # @line L14
            return lb, gamma, w_lb, iterations
        iterations += 1
        ws = sorted([-w for w in freqs] + freqs)  # @line L15
        best, w_best = lb, w_lb
        for a, b in zip(ws, ws[1:]):
            mid = abs((a + b) / 2)
            s = sigma_max(A, B, C, D, mid)
            if s > best:
                best, w_best = s, mid
        if best <= gamma:  # @line L16
            return best, gamma, w_best, iterations
        lb, w_lb = best, w_best
    raise RuntimeError("level set iteration did not stop")
