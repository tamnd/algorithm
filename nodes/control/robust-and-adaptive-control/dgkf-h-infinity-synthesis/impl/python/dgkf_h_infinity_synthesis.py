# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dgkf-h-infinity-synthesis/. The authors are listed in prov/DM08Z2.jsonl.

"""Two-Riccati H-infinity synthesis (Doyle, Glover, Khargonekar, Francis 1989).

The generalized plant has the normalized form of the page:

    x' = A x + B1 w + B2 u
    z  = C1 x + D12 u          with D12^T [C1 D12] = [0 I]
    y  = C2 x + D21 w          with [B1; D21] D21^T = [0; I]

and D11 = 0, D22 = 0. A plant is a dict with the keys "A", "B1", "B2",
"C1", "C2", "D12", "D21" (lists of rows). The controller is wired as
u = K y, the lower linear fractional transformation, with no sign change.

Each Riccati equation is solved from the stable invariant subspace of its
Hamiltonian matrix, found with the matrix sign function (Newton iteration
with determinant scaling). All results are floats.
"""

import math

from ctlmat import (
    add, block, charpoly, det, eye, inv, is_pos_def, mul, norm2, polyroots,
    scale, solve, sub, transpose, zeros,
)

__all__ = [
    "matrix_sign", "riccati", "is_hurwitz", "spectral_radius",
    "gamma_feasible", "optimal_gamma", "central_controller", "closed_loop",
    "freq_gain", "dgkf_synthesis",
]


def _flo(a):
    return [[float(v) for v in row] for row in a]


def _big(a):
    return max((abs(v) for row in a for v in row), default=0.0)


def matrix_sign(h, tol=1e-13, maxiter=100):
    """Return sign(H) by the scaled Newton iteration, or None.

    None means that the iteration did not converge, which happens when H
    has an eigenvalue on or very near the imaginary axis.
    """
    n = len(h)
    z = _flo(h)
    for _ in range(maxiter):
        d = abs(det(z))
        if not d > 0.0 or not math.isfinite(d):
            return None
        mu = d ** (-1.0 / n)
        zi = inv(z)
        znew = [[0.5 * (mu * z[i][j] + zi[i][j] / mu) for j in range(n)] for i in range(n)]
        diff = _big(sub(znew, z))
        z = znew
        if diff <= tol * max(1.0, _big(z)):
            break
    if _big(sub(mul(z, z), eye(n))) > 1e-8:
        return None
    return z


def is_hurwitz(m, tol=1e-9):
    """Return True if every eigenvalue of m has real part below -tol."""
    roots = polyroots(charpoly(_flo(m)))
    return max(r.real for r in roots) < -tol


def spectral_radius(m):
    """Return the largest modulus of an eigenvalue of m."""
    return max(abs(r) for r in polyroots(charpoly(_flo(m))))


def riccati(a, r, q):
    """Return the stabilizing solution X of A^T X + X A + X R X + Q = 0, or None.

    R and Q are symmetric. The solution is X = Ric(H) for the Hamiltonian
    H = [[A, R], [-Q, -A^T]]: the stable invariant subspace of H is the
    range of [I; X], and A + R X is Hurwitz. None means that H has an
    eigenvalue on the imaginary axis or that the stable subspace is not a
    graph over its first n coordinates.
    """
    n = len(a)
    a, r, q = _flo(a), _flo(r), _flo(q)
    h = block([[a, r], [scale(-1.0, q), scale(-1.0, transpose(a))]])
    w = matrix_sign(h)
    if w is None:
        return None
    # The stable subspace is the kernel of W + I, so (W + I) [I; X] = 0.
    wp = add(w, eye(2 * n))
    lhs = [row[n:] for row in wp]
    rhs = [[-v for v in row[:n]] for row in wp]
    lt = transpose(lhs)
    try:
        x = solve(mul(lt, lhs), mul(lt, rhs))
    except ValueError:
        return None
    x = [[0.5 * (x[i][j] + x[j][i]) for j in range(n)] for i in range(n)]
    res = add(add(mul(transpose(a), x), mul(x, a)), add(mul(mul(x, r), x), q))
    size = 1.0 + _big(mul(transpose(a), x)) + _big(mul(mul(x, r), x)) + _big(q)
    if not math.isfinite(_big(x)) or _big(res) > 1e-7 * size:
        return None
    if not is_hurwitz(add(a, mul(r, x))):
        return None
    return x


def _psd(x, rel=1e-9):
    return is_pos_def(x, -rel * (1.0 + _big(x)))


def gamma_feasible(p, gamma):
    """Test the three DGKF conditions at gamma. Return (ok, X, Y)."""
    a, b1, b2, c1, c2 = (_flo(p[k]) for k in ("A", "B1", "B2", "C1", "C2"))
    g2 = 1.0 / (gamma * gamma)
    rx = sub(scale(g2, mul(b1, transpose(b1))), mul(b2, transpose(b2)))
    x = riccati(a, rx, mul(transpose(c1), c1))  # @line L11
    if x is None or not _psd(x):
        return False, x, None
    ry = sub(scale(g2, mul(transpose(c1), c1)), mul(transpose(c2), c2))
    y = riccati(transpose(a), ry, mul(b1, transpose(b1)))  # @line L12
    if y is None or not _psd(y):
        return False, x, y
    ok = spectral_radius(mul(x, y)) < gamma * gamma * (1.0 - 1e-9)  # @line L13
    return ok, x, y


def optimal_gamma(p, rtol=1e-6):
    """Bisect for the smallest gamma that passes gamma_feasible."""
    lo, hi = 0.0, 1.0  # @line L1
    while not gamma_feasible(p, hi)[0]:  # @line L2
        lo, hi = hi, 2.0 * hi
        if hi > 1e8:
            raise ValueError("no gamma below 1e8 passes the test")
    while hi - lo > rtol * hi:  # @line L3
        g = 0.5 * (lo + hi)  # @line L4
        if gamma_feasible(p, g)[0]:  # @line L5
            hi = g
        else:
            lo = g
    return hi


def central_controller(p, gamma):
    """Return (A_K, B_K, C_K, D_K) of the central controller at gamma.

    Raises ValueError if gamma does not pass the three conditions.
    """
    ok, x, y = gamma_feasible(p, gamma)  # @line L7
    if not ok:
        raise ValueError("gamma does not pass the DGKF conditions")
    a, b1, b2, c2 = (_flo(p[k]) for k in ("A", "B1", "B2", "C2"))
    n = len(a)
    g2 = 1.0 / (gamma * gamma)
    f = scale(-1.0, mul(transpose(b2), x))  # @line L8
    l = scale(-1.0, mul(y, transpose(c2)))
    z = inv(sub(eye(n), scale(g2, mul(y, x))))
    ak = add(add(a, scale(g2, mul(mul(b1, transpose(b1)), x))),  # @line L9
             add(mul(b2, f), mul(mul(z, l), c2)))
    bk = scale(-1.0, mul(z, l))
    dk = zeros(len(f), len(bk[0]))
    return ak, bk, f, dk  # @line L10


def closed_loop(p, k):
    """Return (A, B, C, D) of the map w -> z with u = K y."""
    a, b1, b2, c1, c2, d12, d21 = (_flo(p[s]) for s in ("A", "B1", "B2", "C1", "C2", "D12", "D21"))
    ak, bk, ck, dk = (_flo(m) for m in k)
    acl = block([[add(a, mul(mul(b2, dk), c2)), mul(b2, ck)],
                 [mul(bk, c2), ak]])
    bcl = block([[add(b1, mul(mul(b2, dk), d21))], [mul(bk, d21)]])
    ccl = block([[add(c1, mul(mul(d12, dk), c2)), mul(d12, ck)]])
    dcl = mul(mul(d12, dk), d21)
    return acl, bcl, ccl, dcl


def freq_gain(sys, w):
    """Return the largest singular value of C (j w I - A)^-1 B + D."""
    a, b, c, d = sys
    n = len(a)
    m = [[(1j * w if i == j else 0.0) - a[i][j] for j in range(n)] for i in range(n)]
    g = add(mul(c, solve(m, [[complex(v) for v in row] for row in b])), d)
    return norm2(g)


def dgkf_synthesis(p, rtol=1e-6, backoff=1.01):
    """Return (gamma_opt, gamma_used, controller).

    gamma_opt is the bisection estimate of the optimal level. The
    controller is the central one at gamma_used = backoff * gamma_opt,
    since the central controller degenerates at the optimum itself.
    """
    gopt = optimal_gamma(p, rtol)
    g = backoff * gopt  # @line L6
    return gopt, g, central_controller(p, g)
