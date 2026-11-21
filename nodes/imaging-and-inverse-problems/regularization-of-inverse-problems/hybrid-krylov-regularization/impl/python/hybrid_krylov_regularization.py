# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hybrid-krylov-regularization/. The authors are listed in prov/WCZ0JJ.jsonl.
"""A hybrid LSQR method: Golub-Kahan bidiagonalization with Tikhonov on the projected problem.

After k steps, A V_k = U_{k+1} B_k with B_k lower bidiagonal of size (k+1) x k
and y = beta_1 U_{k+1} e_1. For a Tikhonov parameter lam the projected problem

    z_k = argmin ||B_k z - beta_1 e_1||^2 + lam ||z||^2,   x_k = V_k z_k,

gives the minimizer of ||A x - y||^2 + lam ||x||^2 over x in V_k = K_k(A^T A, A^T y).
The parameter is chosen again at every step from the small problem only:
"dp" is the projected discrepancy principle, "wgcv" is weighted GCV, and a
number is a fixed parameter. Both rules use the SVD of B_k, which costs
O(k^3) and is small next to the products with A when k is much less than n.

Full reorthogonalization keeps U and V orthonormal in floating point. Without
it the projected problem drifts from the true one.
"""

import math

from imgla import matvec, rmatvec, svd


def _norm(v):
    return math.sqrt(sum(t * t for t in v))


def _reorth(w, basis):
    for _ in range(2):
        for b in basis:
            h = sum(p * q for p, q in zip(b, w))
            w = [p - h * q for p, q in zip(w, b)]
    return w


def bidiag_matrix(alphas, betas, k):
    """B_k: alphas[0..k-1] on the diagonal, betas[1..k] below it."""
    b = [[0.0] * k for _ in range(k + 1)]
    for i in range(k):
        b[i][i] = alphas[i]
        b[i + 1][i] = betas[i + 1]
    return b


class Projected:
    """The SVD of B_k and the coefficients g_i = beta_1 (P^T e_1)_i, with the
    part of beta_1 e_1 outside range(B_k) (zero in exact arithmetic only if
    the Krylov space holds the least squares solution)."""

    def __init__(self, bk, beta1):
        p, s, q = svd(bk)
        self.s, self.q, self.k = s, q, len(s)
        self.g = [beta1 * p[0][i] for i in range(self.k)]
        self.out2 = max(beta1 * beta1 - sum(t * t for t in self.g), 0.0)

    def z(self, lam):
        """z = sum_i s_i g_i / (s_i^2 + lam) q_i, the projected Tikhonov solution."""
        coef = [si * gi / (si * si + lam) if si * si + lam > 0 else 0.0
                for si, gi in zip(self.s, self.g)]
        return [sum(c * self.q[j][i] for i, c in enumerate(coef)) for j in range(self.k)]

    def res2(self, lam):
        """||B_k z_lam - beta_1 e_1||^2 = ||A x_lam - y||^2."""
        tot = self.out2
        for si, gi in zip(self.s, self.g):
            if si * si + lam > 0:
                tot += (lam * gi / (si * si + lam)) ** 2
            else:
                tot += gi * gi
        return tot

    def gcv(self, lam, omega=1.0):
        """Weighted GCV: ||res||^2 / (k + 1 - omega sum_i s_i^2 / (s_i^2 + lam))^2."""
        tr = self.k + 1 - omega * sum(si * si / (si * si + lam) for si in self.s if si * si + lam > 0)
        return self.res2(lam) / (tr * tr) if tr > 0 else math.inf


def choose_dp(proj, delta, tau):
    """The lam with ||B_k z_lam - beta_1 e_1|| = tau delta, by bisection on log lam.

    The residual grows with lam. If tau delta is below the residual at lam = 0,
    the Krylov space is still too small and lam = 0 is returned.
    """
    target = (tau * delta) ** 2
    if proj.res2(0.0) >= target:
        return 0.0
    smax = proj.s[0] if proj.s and proj.s[0] > 0 else 1.0
    lo, hi = math.log(smax * smax * 1e-30), math.log(smax * smax * 1e6)
    if proj.res2(math.exp(hi)) <= target:
        return math.exp(hi)
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if proj.res2(math.exp(mid)) < target:
            lo = mid
        else:
            hi = mid
        if hi - lo < 1e-12:
            break
    return math.exp(0.5 * (lo + hi))


def choose_wgcv(proj, omega=1.0, points=81):
    """Minimize the weighted GCV function over a log grid, then refine by golden section."""
    smax = proj.s[0] if proj.s and proj.s[0] > 0 else 1.0
    lo, hi = math.log(smax * smax * 1e-14), math.log(smax * smax)
    grid = [lo + (hi - lo) * i / (points - 1) for i in range(points)]
    vals = [proj.gcv(math.exp(t), omega) for t in grid]
    i = min(range(points), key=lambda j: vals[j])
    a, b = grid[max(i - 1, 0)], grid[min(i + 1, points - 1)]
    ratio = (math.sqrt(5.0) - 1.0) / 2.0
    for _ in range(60):
        c, d = b - ratio * (b - a), a + ratio * (b - a)
        if proj.gcv(math.exp(c), omega) < proj.gcv(math.exp(d), omega):
            b = d
        else:
            a = c
    return math.exp(0.5 * (a + b))


class HybridResult:
    """x: the last iterate; k: steps done; iterates: x_1, ..., x_k; lams: the
    parameter chosen at each step; resnorms: ||y - A x_j||; stopped:
    "breakdown" (the Krylov space is invariant) or "maxit"; proj and basis: the
    projected problem and V_k of the last step."""

    def __init__(self, **kw):
        self.__dict__.update(kw)

    def solve(self, lam):
        """x = V_k z_lam for any lam >= 0, with no new products with A."""
        z = self.proj.z(lam)
        return [sum(z[j] * self.basis[j][i] for j in range(len(z)))
                for i in range(len(self.basis[0]))]


def hybrid_lsqr(apply_a, apply_at, y, kmax, rule="dp", delta=None, tau=1.01, omega=1.0):
    """Run kmax steps of the hybrid method; rule is "dp", "wgcv" or a fixed lam >= 0."""
    if rule == "dp" and delta is None:
        raise ValueError("the discrepancy rule needs delta")
    beta1 = _norm(y)
    u = [t / beta1 for t in y]
    v = apply_at(u)
    alpha = _norm(v)
    v = [t / alpha for t in v]  # @line L1
    us, vs, alphas, betas = [u], [v], [alpha], [beta1]
    iterates, lams, resnorms = [], [], []
    stopped = "maxit"
    for k in range(1, kmax + 1):  # @line L2
        w = _reorth([p - alpha * q for p, q in zip(apply_a(v), u)], us)
        beta = _norm(w)
        u = [t / beta for t in w] if beta > 0 else [0.0] * len(w)  # @line L3
        w = _reorth([p - beta * q for p, q in zip(apply_at(u), v)], vs)
        alpha = _norm(w)
        v = [t / alpha for t in w] if alpha > 0 else [0.0] * len(w)  # @line L4
        us.append(u)
        vs.append(v)
        alphas.append(alpha)
        betas.append(beta)
        proj = Projected(bidiag_matrix(alphas, betas, k), beta1)  # @line L5
        if rule == "dp":
            lam = choose_dp(proj, delta, tau)
        elif rule == "wgcv":
            lam = choose_wgcv(proj, omega)
        else:
            lam = float(rule)  # @line L6
        z = proj.z(lam)  # @line L7
        x = [sum(z[j] * vs[j][i] for j in range(k)) for i in range(len(v))]  # @line L8
        iterates.append(x)
        lams.append(lam)
        resnorms.append(math.sqrt(proj.res2(lam)))
        if alpha <= 1e-14 * alphas[0] or beta <= 1e-14 * beta1:
            stopped = "breakdown"
            break
    return HybridResult(x=iterates[-1], k=len(iterates), iterates=iterates, lams=lams,  # @line L9
                        resnorms=resnorms, stopped=stopped, proj=proj, basis=vs[:len(iterates)])


def hybrid_matrix(a, y, kmax, rule="dp", delta=None, tau=1.01, omega=1.0):
    """The hybrid method for a dense matrix A (a list of rows)."""
    return hybrid_lsqr(lambda x: matvec(a, x), lambda r: rmatvec(a, r), y, kmax,
                       rule=rule, delta=delta, tau=tau, omega=omega)
