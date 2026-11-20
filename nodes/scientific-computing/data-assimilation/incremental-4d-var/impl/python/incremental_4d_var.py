# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/incremental-4d-var/. The authors are listed in prov/FTZTDM.jsonl.

"""Incremental 4D-Var: outer loops with the full model, inner loops with a linear model.

Notation of Ide, Courtier, Ghil and Lorenc (1997). The window has the time
levels 0..K, the full model step is x_k = M_k(x_(k-1)), and obs maps a time
level k to (H_k, y_k, R_k) with a linear H_k. The full cost is

    J(x_0) = 1/2 (x_0 - x^b)^T B^-1 (x_0 - x^b) + sum_k 1/2 d_k^T R_k^-1 d_k,
    d_k = y_k - H_k M_(0->k)(x_0).

Each outer loop runs the full model from the current x_0, computes the
departures, and minimizes the quadratic cost for an increment dx_0 in which
the trajectory change is given by a linear model along the stored
trajectory. With the exact tangent linear model this is one Gauss-Newton
step for J. The inner minimization is the conjugate gradient method; each
product with the inner Hessian costs one linear model run and one adjoint run.

A linear model along the trajectory is given by two functions:
    tangent(k, x, dx)       the linear model of step k at x = x_(k-1), applied to dx
    adjoint(k, x, lam)      its transpose applied to lam
The inner model may differ from the exact tangent linear model, for example
a simplified or lower resolution one; it must then come with its own exact
transpose.
"""

import scimat


def trajectory(x0, step, K):
    """Return [x_0, x_1, ..., x_K] for the model step from x0."""
    xs = [list(x0)]
    for k in range(1, K + 1):
        xs.append(step(k, xs[-1]))
    return xs


def cost(x0, xb, B, obs, step, K):
    """Return the full cost J(x0)."""
    xs = trajectory(x0, step, K)
    e = scimat.sub(x0, xb)
    J = 0.5 * scimat.dot(e, scimat.solve(B, e))
    for k, (H, y, R) in obs.items():
        d = scimat.sub(y, scimat.matvec(H, xs[k]))
        J += 0.5 * scimat.dot(d, scimat.solve(R, d))
    return J


def tangent_sweep(xs, dx0, tangent, K):
    """Return [dx_0, ..., dx_K] for the linear model along the trajectory xs."""
    out = [list(dx0)]
    for k in range(1, K + 1):
        out.append(tangent(k, xs[k - 1], out[-1]))
    return out


def adjoint_sweep(xs, forcing, adjoint, K, n):
    """Return sum_k (linear model from 0 to k)^T forcing[k] by one backward run."""
    lam = [0.0] * n
    for k in range(K, -1, -1):
        if k in forcing:
            lam = scimat.add(lam, forcing[k])
        if k > 0:
            lam = adjoint(k, xs[k - 1], lam)
    return lam


def conjugate_gradient(apply_a, b, tol=1e-14, max_iter=None):
    """Solve A z = b for symmetric positive definite A given as a function."""
    n = len(b)
    if max_iter is None:
        max_iter = 2 * n
    z = [0.0] * n
    r = [float(v) for v in b]
    q = list(r)
    rr = scimat.dot(r, r)
    stop = (tol * scimat.norm2(b)) ** 2
    for _ in range(max_iter):
        if rr <= stop:
            break
        aq = apply_a(q)
        alpha = rr / scimat.dot(q, aq)
        z = [zi + alpha * qi for zi, qi in zip(z, q)]
        r = [ri - alpha * ai for ri, ai in zip(r, aq)]
        rr_new = scimat.dot(r, r)
        q = [ri + (rr_new / rr) * qi for ri, qi in zip(r, q)]
        rr = rr_new
    return z


def incremental_4dvar(xb, B, obs, step, tangent, adjoint, K, max_outer=30, tol=1e-12):
    """Return (x_0^a, outer iterates) for incremental 4D-Var.

    The outer loop stops when |dx_0| <= tol (1 + |x_0|) or after max_outer loops.
    """
    n = len(xb)
    LB = scimat.cholesky(B)
    ob = {k: (H, scimat.transpose(H), y, scimat.cholesky(R)) for k, (H, y, R) in obs.items()}
    x0 = [float(v) for v in xb]  # @line L1
    iterates = [list(x0)]
    for _ in range(max_outer):  # @line L2
        xs = trajectory(x0, step, K)  # @line L3
        d = {k: scimat.sub(y, scimat.matvec(H, xs[k])) for k, (H, Ht, y, LR) in ob.items()}  # @line L4
        forcing = {k: scimat.matvec(Ht, scimat.cholesky_solve(LR, d[k])) for k, (H, Ht, y, LR) in ob.items()}
        b = scimat.sub(adjoint_sweep(xs, forcing, adjoint, K, n), scimat.cholesky_solve(LB, scimat.sub(x0, xb)))  # @line L5

        def apply_a(v):  # @line L6
            vs = tangent_sweep(xs, v, tangent, K)
            f = {k: scimat.matvec(Ht, scimat.cholesky_solve(LR, scimat.matvec(H, vs[k]))) for k, (H, Ht, y, LR) in ob.items()}
            return scimat.add(scimat.cholesky_solve(LB, v), adjoint_sweep(xs, f, adjoint, K, n))

        dx = conjugate_gradient(apply_a, b)  # @line L7
        x0 = scimat.add(x0, dx)  # @line L8
        iterates.append(list(x0))
        if scimat.norm2(dx) <= tol * (1.0 + scimat.norm2(x0)):  # @line L9
            break
    return x0, iterates  # @line L10


def linear_model(M):
    """Return (step, tangent, adjoint) for the linear model x_k = M x_(k-1)."""
    Mt = scimat.transpose(M)
    return (
        lambda k, x: scimat.matvec(M, x),
        lambda k, x, dx: scimat.matvec(M, dx),
        lambda k, x, lam: scimat.matvec(Mt, lam),
    )


def lorenz63(dt=0.01, sigma=10.0, rho=28.0, beta=8.0 / 3.0):
    """Return (step, tangent, adjoint) for forward Euler steps of the Lorenz-63 model."""

    def f(x):
        return [sigma * (x[1] - x[0]), x[0] * (rho - x[2]) - x[1], x[0] * x[1] - beta * x[2]]

    def jac(x):
        return [[-sigma, sigma, 0.0], [rho - x[2], -1.0, -x[0]], [x[1], x[0], -beta]]

    def step(k, x):
        return [xi + dt * fi for xi, fi in zip(x, f(x))]

    def tangent(k, x, dx):
        return [di + dt * v for di, v in zip(dx, scimat.matvec(jac(x), dx))]

    def adjoint(k, x, lam):
        return [li + dt * v for li, v in zip(lam, scimat.matvec(scimat.transpose(jac(x)), lam))]

    return step, tangent, adjoint
