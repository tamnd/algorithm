# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/four-dimensional-ensemble-variational/. The authors are listed in prov/5MYERD.jsonl.

"""Four-dimensional ensemble-variational assimilation (4DEnVar).

Notation of Ide, Courtier, Ghil and Lorenc (1997). The window has the time
levels 0..K. Each ensemble member is run forward over the window with the
full model, and the scaled perturbations x'_i(k) = (x_i(k) - mean_k) /
sqrt(N - 1) at each time replace the tangent linear model of 4D-Var. The
increment at time k is

    dx_k = sum_i x'_i(k) o (U_L alpha_i),    U_L U_L^T = L,

with the same control alpha = (alpha_1, ..., alpha_N) at all times, and the
cost over alpha is

    J = 1/2 |alpha|^2 + sum_(k in T) 1/2 (d_k - H_k dx_k)^T R_k^-1 (d_k - H_k dx_k),

where d_k = y_k - H_k x^b_k is the departure from the background
trajectory. No tangent linear or adjoint model is needed: the model runs
only forward, once for the background and once for each member. The
implied covariance between the increments at times k and l is
L o (X'_k X'_l^T).

The model is a function step(k, x) = M_k(x) for x = x_(k-1). obs maps a
time k to (H_k, y_k, R_k), with a linear observation operator H_k.
"""

import math

import scimat


def run(x0, step, K):
    """Return the trajectory [x_0, ..., x_K] of the model from x0."""
    xs = [list(x0)]
    for k in range(1, K + 1):
        xs.append(step(k, xs[-1]))
    return xs


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


def four_d_envar(xb, members, L, obs, step, K):
    """Return {k: x^a_k} of 4DEnVar with localization matrix L, for k = 0, K and every observation time."""
    n = len(xb)
    N = len(members)
    background = run(xb, step, K)  # @line L1
    trajs = [run(m, step, K) for m in members]  # @line L2
    s = 1.0 / math.sqrt(N - 1)
    xp = {}
    for k in sorted(set(obs) | {0, K}):
        mean = [sum(t[k][j] for t in trajs) / N for j in range(n)]
        xp[k] = [[s * (t[k][j] - mean[j]) for j in range(n)] for t in trajs]
    UL = _square_root(L)  # @line L3
    ULt = scimat.transpose(UL)
    ob = {k: (H, scimat.transpose(H), y, scimat.cholesky(R)) for k, (H, y, R) in obs.items()}
    d = {k: scimat.sub(y, scimat.matvec(H, background[k])) for k, (H, Ht, y, LR) in ob.items()}  # @line L4

    def U(k, a, loc=None):  # @line L5
        if loc is None:
            loc = [scimat.matvec(UL, a[n * i : n * (i + 1)]) for i in range(N)]
        dx = [0.0] * n
        for i in range(N):
            dx = [v + p * q for v, p, q in zip(dx, xp[k][i], loc[i])]
        return dx

    def Ut(k, g):
        out = []
        for i in range(N):
            out.extend(scimat.matvec(ULt, [p * q for p, q in zip(xp[k][i], g)]))
        return out

    b = [0.0] * (N * n)  # @line L6
    for k, (H, Ht, y, LR) in ob.items():
        b = scimat.add(b, Ut(k, scimat.matvec(Ht, scimat.cholesky_solve(LR, d[k]))))

    def apply_a(a):  # @line L7
        loc = [scimat.matvec(UL, a[n * i : n * (i + 1)]) for i in range(N)]
        out = list(a)
        for k, (H, Ht, y, LR) in ob.items():
            g = scimat.matvec(Ht, scimat.cholesky_solve(LR, scimat.matvec(H, U(k, a, loc))))
            out = scimat.add(out, Ut(k, g))
        return out

    a = conjugate_gradient(apply_a, b)  # @line L8
    loc = [scimat.matvec(UL, a[n * i : n * (i + 1)]) for i in range(N)]
    analysis = {}
    for k in xp:  # @line L9
        analysis[k] = scimat.add(background[k], U(k, a, loc))
    return analysis  # @line L10


def linear_model(M):
    """Return step for the linear model x_k = M x_(k-1)."""
    return lambda k, x: scimat.matvec(M, x)


def lorenz63(dt=0.01, sigma=10.0, rho=28.0, beta=8.0 / 3.0):
    """Return step for forward Euler steps of the Lorenz-63 model."""

    def step(k, x):
        f = [sigma * (x[1] - x[0]), x[0] * (rho - x[2]) - x[1], x[0] * x[1] - beta * x[2]]
        return [xi + dt * fi for xi, fi in zip(x, f)]

    return step
