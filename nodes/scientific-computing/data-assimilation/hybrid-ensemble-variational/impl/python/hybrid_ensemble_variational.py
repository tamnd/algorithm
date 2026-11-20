# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hybrid-ensemble-variational/. The authors are listed in prov/GBD29Q.jsonl.

"""Hybrid ensemble-variational analysis (hybrid 3D-Var) with the alpha control variable.

Notation of Ide, Courtier, Ghil and Lorenc (1997). The analysis increment is

    dx = beta_c U_c v_c + beta_e sum_i x'_i o (U_L alpha_i),

where U_c U_c^T = B_c is the static (climatological) covariance, the x'_i =
(x_i - mean) / sqrt(N - 1) are the scaled ensemble perturbations, o is the
entrywise product, and U_L U_L^T = L is the localization matrix. The cost
over the control w = (v_c, alpha_1, ..., alpha_N) is

    J(w) = 1/2 |w|^2 + 1/2 (d - H dx)^T R^-1 (d - H dx),   d = y - H x^b,

and it is the 3D-Var cost with the hybrid background covariance

    B = beta_c^2 B_c + beta_e^2 L o (X' X'^T)

(Lorenc 2003; Wang, Snyder and Hamill 2007). The observation operator H is
linear here, and the minimizer is the conjugate gradient method.
"""

import math

import scimat


def gaspari_cohn(r, c):
    """Return the Gaspari-Cohn fifth order correlation at distance r for the half-width c (zero beyond 2c)."""
    z = abs(r) / c
    if z <= 1.0:
        return -0.25 * z**5 + 0.5 * z**4 + 0.625 * z**3 - (5.0 / 3.0) * z**2 + 1.0
    if z <= 2.0:
        return z**5 / 12.0 - 0.5 * z**4 + 0.625 * z**3 + (5.0 / 3.0) * z**2 - 5.0 * z + 4.0 - 2.0 / (3.0 * z)
    return 0.0


def localization_matrix(positions, c):
    """Return the matrix L_jk = gaspari_cohn(positions[j] - positions[k], c)."""
    return [[gaspari_cohn(a - b, c) for b in positions] for a in positions]


def perturbations(ensemble):
    """Return (mean, [x'_i]) with x'_i = (x_i - mean) / sqrt(N - 1)."""
    N = len(ensemble)
    n = len(ensemble[0])
    mean = [sum(x[j] for x in ensemble) / N for j in range(n)]
    s = 1.0 / math.sqrt(N - 1)
    return mean, [[s * (x[j] - mean[j]) for j in range(n)] for x in ensemble]


def _square_root(A):
    """Return a lower triangular U with U U^T = A, with a tiny shift if A is only semidefinite."""
    try:
        return scimat.cholesky(A)
    except ValueError:
        n = len(A)
        eps = 1e-12 * max(1.0, max(abs(A[i][i]) for i in range(n)))
        return scimat.cholesky([[A[i][j] + (eps if i == j else 0.0) for j in range(n)] for i in range(n)])


def conjugate_gradient(apply_a, b, tol=1e-13, max_iter=None):
    """Solve A w = b for symmetric positive definite A given as a function."""
    n = len(b)
    if max_iter is None:
        max_iter = 2 * n
    w = [0.0] * n
    r = list(b)
    q = list(r)
    rr = scimat.dot(r, r)
    stop = (tol * scimat.norm2(b)) ** 2
    for _ in range(max_iter):
        if rr <= stop:
            break
        aq = apply_a(q)
        alpha = rr / scimat.dot(q, aq)
        w = [wi + alpha * qi for wi, qi in zip(w, q)]
        r = [ri - alpha * ai for ri, ai in zip(r, aq)]
        rr_new = scimat.dot(r, r)
        q = [ri + (rr_new / rr) * qi for ri, qi in zip(r, q)]
        rr = rr_new
    return w


def hybrid_envar(xb, ensemble, Bc, L, beta_c2, beta_e2, y, H, R):
    """Return the hybrid analysis x^a, with the weights beta_c^2 and beta_e^2 of the two covariances."""
    n = len(xb)
    N = len(ensemble)
    _, xp = perturbations(ensemble)  # @line L1
    Uc = _square_root(Bc)  # @line L2
    UL = _square_root(L)
    bc, be = math.sqrt(beta_c2), math.sqrt(beta_e2)
    LR = scimat.cholesky(R)
    Ht = scimat.transpose(H)
    Uct, ULt = scimat.transpose(Uc), scimat.transpose(UL)
    d = scimat.sub(y, scimat.matvec(H, xb))  # @line L3

    def U(w):  # @line L4
        dx = scimat.scale(bc, scimat.matvec(Uc, w[:n]))
        for i in range(N):
            loc = scimat.matvec(UL, w[n * (i + 1) : n * (i + 2)])
            dx = [a + be * p * q for a, p, q in zip(dx, xp[i], loc)]
        return dx

    def Ut(g):
        out = scimat.scale(bc, scimat.matvec(Uct, g))
        for i in range(N):
            out.extend(scimat.scale(be, scimat.matvec(ULt, [p * q for p, q in zip(xp[i], g)])))
        return out

    b = Ut(scimat.matvec(Ht, scimat.cholesky_solve(LR, d)))  # @line L5

    def apply_a(w):  # @line L6
        g = scimat.matvec(Ht, scimat.cholesky_solve(LR, scimat.matvec(H, U(w))))
        return [wi + gi for wi, gi in zip(w, Ut(g))]

    w = conjugate_gradient(apply_a, b)  # @line L7
    xa = scimat.add(xb, U(w))  # @line L8
    return xa  # @line L9


def hybrid_covariance(ensemble, Bc, L, beta_c2, beta_e2):
    """Return the hybrid covariance beta_c^2 B_c + beta_e^2 L o (X' X'^T) as a dense matrix."""
    _, xp = perturbations(ensemble)
    n = len(Bc)
    return [[beta_c2 * Bc[j][k] + beta_e2 * L[j][k] * sum(x[j] * x[k] for x in xp) for k in range(n)] for j in range(n)]
