# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/balanced-truncation/. The authors are listed in prov/F4R34P.jsonl.

"""Balanced truncation of a continuous-time LTI system (square root method).

For x' = A x + B u, y = C x + D u with A Hurwitz, the gramians solve

    A W_c + W_c A^T + B B^T = 0,    A^T W_o + W_o A + C^T C = 0.

With W_c = L_c L_c^T, W_o = L_o L_o^T and the SVD L_o^T L_c = U S V^T, the
Hankel singular values are the diagonal of S. The reduced model of order r is

    T_r = L_c V_r S_r^(-1/2),   W_r = L_o U_r S_r^(-1/2),
    A_r = W_r^T A T_r,  B_r = W_r^T B,  C_r = C T_r,  D_r = D.

W_r^T T_r = I, and the reduced model is balanced with gramians S_r. If
sigma_r > sigma_(r+1), A_r is Hurwitz and the H-infinity norm of the error is
at most 2 times the sum of the distinct values among sigma_(r+1), ..., sigma_n.

Everything is in float. The gramians are found by the Kronecker method
(O(n^6) work), which is fine for the small n of the tests and the page.
"""

import math

from ctlmat import eye, kron, mul, norm2, solve, sub, transpose, unvec, vec

__all__ = [
    "lyap", "gramians", "sym_eig", "sqrt_factor", "svd", "hankel_singular_values",
    "balanced_truncation", "error_bound", "freq_response", "hinf_on_grid",
]


def lyap(a, q):
    """Return X with A X + X A^T + Q = 0 (A Hurwitz), in float."""
    n = len(a)
    af = [[float(v) for v in row] for row in a]
    big = [[x + y for x, y in zip(r1, r2)] for r1, r2 in zip(kron(eye(n), af), kron(af, eye(n)))]
    x = unvec(solve(big, [-float(v) for v in vec(q)]), n, n)
    return [[(x[i][j] + x[j][i]) / 2.0 for j in range(n)] for i in range(n)]


def gramians(a, b, c):
    """Return (W_c, W_o), the controllability and observability gramians."""
    wc = lyap(a, mul(b, transpose(b)))
    wo = lyap(transpose(a), mul(transpose(c), c))
    return wc, wo


def sym_eig(s, sweeps=100):
    """Return (values, vectors) of a real symmetric matrix by cyclic Jacobi.

    vectors is a matrix whose columns are orthonormal eigenvectors, so
    s = vectors diag(values) vectors^T up to rounding.
    """
    n = len(s)
    a = [[float(v) for v in row] for row in s]
    q = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    for _ in range(sweeps):
        off = sum(a[i][j] ** 2 for i in range(n) for j in range(n) if i != j)
        diag = sum(a[i][i] ** 2 for i in range(n))
        if off <= 1e-30 * max(diag, 1e-300):
            break
        for p in range(n - 1):
            for r in range(p + 1, n):
                if a[p][r] == 0.0:
                    continue
                theta = (a[r][r] - a[p][p]) / (2.0 * a[p][r])
                t = math.copysign(1.0, theta) / (abs(theta) + math.sqrt(theta * theta + 1.0))
                c = 1.0 / math.sqrt(t * t + 1.0)
                sn = t * c
                for k in range(n):
                    akp, akr = a[k][p], a[k][r]
                    a[k][p] = c * akp - sn * akr
                    a[k][r] = sn * akp + c * akr
                for k in range(n):
                    apk, ark = a[p][k], a[r][k]
                    a[p][k] = c * apk - sn * ark
                    a[r][k] = sn * apk + c * ark
                for k in range(n):
                    qkp, qkr = q[k][p], q[k][r]
                    q[k][p] = c * qkp - sn * qkr
                    q[k][r] = sn * qkp + c * qkr
    return [a[i][i] for i in range(n)], q


def sqrt_factor(w):
    """Return L with W = L L^T for a symmetric positive semidefinite W.

    L = Q diag(sqrt(max(lambda, 0))) from the eigendecomposition, so a
    gramian that is singular to rounding error still gets a factor.
    """
    vals, q = sym_eig(w)
    n = len(w)
    return [[q[i][j] * math.sqrt(max(vals[j], 0.0)) for j in range(n)] for i in range(n)]


def svd(m, sweeps=100):
    """Return (U, s, V) with M = U diag(s) V^T for a square M (one-sided Jacobi).

    s is sorted in decreasing order. A column of U that belongs to a zero
    singular value is set to zero.
    """
    n = len(m)
    g = [[float(m[i][j]) for j in range(n)] for i in range(n)]
    v = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    for _ in range(sweeps):
        rotated = False
        for p in range(n - 1):
            for r in range(p + 1, n):
                alpha = sum(g[k][p] ** 2 for k in range(n))
                beta = sum(g[k][r] ** 2 for k in range(n))
                gamma = sum(g[k][p] * g[k][r] for k in range(n))
                if abs(gamma) <= 1e-15 * math.sqrt(alpha * beta) or gamma == 0.0:
                    continue
                rotated = True
                zeta = (beta - alpha) / (2.0 * gamma)
                t = math.copysign(1.0, zeta) / (abs(zeta) + math.sqrt(1.0 + zeta * zeta))
                c = 1.0 / math.sqrt(1.0 + t * t)
                sn = c * t
                for k in range(n):
                    gp, gr = g[k][p], g[k][r]
                    g[k][p] = c * gp - sn * gr
                    g[k][r] = sn * gp + c * gr
                    vp, vr = v[k][p], v[k][r]
                    v[k][p] = c * vp - sn * vr
                    v[k][r] = sn * vp + c * vr
        if not rotated:
            break
    s = [math.sqrt(sum(g[k][j] ** 2 for k in range(n))) for j in range(n)]
    order = sorted(range(n), key=lambda j: -s[j])
    s = [s[j] for j in order]
    vv = [[v[i][j] for j in order] for i in range(n)]
    u = [[(g[i][j] / s[jj]) if s[jj] > 0.0 else 0.0 for jj, j in enumerate(order)] for i in range(n)]
    return u, s, vv


def hankel_singular_values(a, b, c):
    """Return the Hankel singular values sigma_1 >= ... >= sigma_n."""
    wc, wo = gramians(a, b, c)
    _, s, _ = svd(mul(transpose(sqrt_factor(wo)), sqrt_factor(wc)))
    return s


def error_bound(sigma, r, rtol=1e-9):
    """Return 2 times the sum of the distinct values among sigma[r:].

    Two values count as equal when they differ by at most rtol * sigma[0].
    """
    tail = sigma[r:]
    tol = rtol * (sigma[0] if sigma else 0.0)
    distinct = []
    for x in tail:
        if not any(abs(x - y) <= tol for y in distinct):
            distinct.append(x)
    return 2.0 * sum(distinct)


def balanced_truncation(a, b, c, d, r, rtol=1e-9):
    """Return (A_r, B_r, C_r, D_r, sigma, bound) for the reduced order r.

    sigma is the list of all Hankel singular values and bound is the
    H-infinity error bound. Raises ValueError if 0 < r < n and
    sigma_r - sigma_(r+1) <= rtol * sigma_1, because the cut then splits a
    repeated value and the theorem gives no guarantee.
    """
    n = len(a)
    wc, wo = gramians(a, b, c)  # @line L1
    lc, lo = sqrt_factor(wc), sqrt_factor(wo)  # @line L2
    u, sigma, v = svd(mul(transpose(lo), lc))  # @line L3
    if not 0 <= r <= n:
        raise ValueError("r must be between 0 and n")
    if 0 < r < n and sigma[r - 1] - sigma[r] <= rtol * sigma[0]:  # @line L4
        raise ValueError("sigma_r equals sigma_(r+1): choose another r")
    if r > 0 and sigma[r - 1] <= 0.0:
        raise ValueError("the system has fewer than r controllable and observable modes")
    isq = [1.0 / math.sqrt(sigma[j]) for j in range(r)]
    tr = [[sum(lc[i][k] * v[k][j] for k in range(n)) * isq[j] for j in range(r)] for i in range(n)]  # @line L5
    wr = [[sum(lo[i][k] * u[k][j] for k in range(n)) * isq[j] for j in range(r)] for i in range(n)]
    wrt = transpose(wr) if r > 0 else []
    ar = mul(mul(wrt, a), tr) if r > 0 else []  # @line L6
    br = mul(wrt, b) if r > 0 else []
    cr = mul(c, tr) if r > 0 else [[] for _ in c]
    dr = [list(row) for row in d]
    bound = error_bound(sigma, r, rtol)  # @line L7
    return ar, br, cr, dr, sigma, bound  # @line L8


def freq_response(a, b, c, d, s):
    """Return G(s) = C (s I - A)^(-1) B + D as a complex matrix."""
    n = len(a)
    p = len(d)
    m = len(d[0])
    if n == 0:
        return [[complex(d[i][j]) for j in range(m)] for i in range(p)]
    si_a = sub([[complex(s) if i == j else 0j for j in range(n)] for i in range(n)], [[complex(v) for v in row] for row in a])
    x = solve(si_a, [[complex(v) for v in row] for row in b])
    g = mul([[complex(v) for v in row] for row in c], x)
    return [[g[i][j] + d[i][j] for j in range(m)] for i in range(p)]


def hinf_on_grid(sys1, sys2, omegas):
    """Return the largest 2-norm of G1(j w) - G2(j w) over the grid (a lower estimate)."""
    best = 0.0
    for w in omegas:
        g1 = freq_response(*sys1, 1j * w)
        g2 = freq_response(*sys2, 1j * w)
        e = [[x - y for x, y in zip(r1, r2)] for r1, r2 in zip(g1, g2)]
        best = max(best, norm2(e))
    return best
