# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/weak-constraint-4d-var/. The authors are listed in prov/2GGXNP.jsonl.

"""Weak-constraint 4D-Var in the model error forcing form.

Notation of Ide, Courtier, Ghil and Lorenc (1997). The window has the time
levels 0..K. The model is not exact: x_k = M_k(x_(k-1)) + eta_k, where the
model error eta_k has the covariance Q_k. The control variable is
z = (x_0, eta_1, ..., eta_K), and the cost is

    J(z) = 1/2 (x_0 - x^b)^T B^-1 (x_0 - x^b) + sum_k 1/2 eta_k^T Q_k^-1 eta_k
         + sum_(k in T) 1/2 d_k^T R_k^-1 d_k,       d_k = y_k - H_k x_k.

The minimizer is Gauss-Newton: each outer loop linearizes the model along
the current trajectory and solves the quadratic problem for the increment
dz with the conjugate gradient method. Products with the Gauss-Newton
Hessian cost one tangent linear run and one adjoint run. For a linear model
one outer loop gives the exact minimizer, which is the Kalman smoother
estimate with model error covariance Q.

The model is given by three functions:
    step(k, x)              M_k(x) for x = x_(k-1), without the model error
    tangent(k, x, dx)       M_k'(x) dx
    adjoint(k, x, lam)      M_k'(x)^T lam
Q is a list with Q[k] the covariance of eta_k for k = 1..K (Q[0] is not used).
"""

import scimat


def trajectory(x0, eta, step, K):
    """Return [x_0, ..., x_K] with x_k = M_k(x_(k-1)) + eta_k."""
    xs = [list(x0)]
    for k in range(1, K + 1):
        xs.append(scimat.add(step(k, xs[-1]), eta[k]))
    return xs


def cost(x0, eta, xb, B, Q, obs, step, K):
    """Return J(x_0, eta)."""
    xs = trajectory(x0, eta, step, K)
    e = scimat.sub(x0, xb)
    J = 0.5 * scimat.dot(e, scimat.solve(B, e))
    for k in range(1, K + 1):
        J += 0.5 * scimat.dot(eta[k], scimat.solve(Q[k], eta[k]))
    for k, (H, y, R) in obs.items():
        d = scimat.sub(y, scimat.matvec(H, xs[k]))
        J += 0.5 * scimat.dot(d, scimat.solve(R, d))
    return J


def _backward(xs, forcing, adjoint, K, n):
    """Return [mu_0, ..., mu_K]: mu_k is the sensitivity to x_k after the forcing at time k."""
    mu = [None] * (K + 1)
    lam = [0.0] * n
    for k in range(K, -1, -1):
        if k in forcing:
            lam = scimat.add(lam, forcing[k])
        mu[k] = lam
        if k > 0:
            lam = adjoint(k, xs[k - 1], lam)
    return mu


def gradient(x0, eta, xb, B, Q, obs, step, adjoint, K):
    """Return (grad over x_0, [None, grad over eta_1, ..., grad over eta_K])."""
    n = len(x0)
    xs = trajectory(x0, eta, step, K)
    forcing = {}
    for k, (H, y, R) in obs.items():
        d = scimat.sub(y, scimat.matvec(H, xs[k]))
        forcing[k] = [-v for v in scimat.matvec(scimat.transpose(H), scimat.solve(R, d))]
    mu = _backward(xs, forcing, adjoint, K, n)
    g0 = scimat.add(scimat.solve(B, scimat.sub(x0, xb)), mu[0])
    geta = [None] + [scimat.add(scimat.solve(Q[k], eta[k]), mu[k]) for k in range(1, K + 1)]
    return g0, geta


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


def _split(v, n, K):
    return v[:n], [None] + [v[n * k : n * (k + 1)] for k in range(1, K + 1)]


def _join(v0, w, K):
    out = list(v0)
    for k in range(1, K + 1):
        out.extend(w[k])
    return out


def weak_4dvar(xb, B, Q, obs, step, tangent, adjoint, K, max_outer=30, tol=1e-12):
    """Return (trajectory, x_0, eta, number of outer loops) for weak-constraint 4D-Var."""
    n = len(xb)
    LB = scimat.cholesky(B)
    LQ = [None] + [scimat.cholesky(Q[k]) for k in range(1, K + 1)]
    ob = {k: (H, scimat.transpose(H), y, scimat.cholesky(R)) for k, (H, y, R) in obs.items()}
    x0 = [float(v) for v in xb]  # @line L1
    eta = [None] + [[0.0] * n for _ in range(K)]
    outer = 0
    for outer in range(1, max_outer + 1):  # @line L2
        xs = trajectory(x0, eta, step, K)  # @line L3
        d = {k: scimat.sub(y, scimat.matvec(H, xs[k])) for k, (H, Ht, y, LR) in ob.items()}  # @line L4
        forcing = {k: [-v for v in scimat.matvec(Ht, scimat.cholesky_solve(LR, d[k]))] for k, (H, Ht, y, LR) in ob.items()}
        mu = _backward(xs, forcing, adjoint, K, n)  # @line L5
        g = _join(
            scimat.add(scimat.cholesky_solve(LB, scimat.sub(x0, xb)), mu[0]),
            [None] + [scimat.add(scimat.cholesky_solve(LQ[k], eta[k]), mu[k]) for k in range(1, K + 1)],
            K,
        )

        def apply_a(v):  # @line L6
            v0, w = _split(v, n, K)
            dx = [v0]
            for k in range(1, K + 1):
                dx.append(scimat.add(tangent(k, xs[k - 1], dx[-1]), w[k]))
            f = {k: scimat.matvec(Ht, scimat.cholesky_solve(LR, scimat.matvec(H, dx[k]))) for k, (H, Ht, y, LR) in ob.items()}
            m = _backward(xs, f, adjoint, K, n)
            out0 = scimat.add(scimat.cholesky_solve(LB, v0), m[0])
            outw = [None] + [scimat.add(scimat.cholesky_solve(LQ[k], w[k]), m[k]) for k in range(1, K + 1)]
            return _join(out0, outw, K)

        dz = conjugate_gradient(apply_a, [-v for v in g])  # @line L7
        d0, dw = _split(dz, n, K)
        x0 = scimat.add(x0, d0)  # @line L8
        eta = [None] + [scimat.add(eta[k], dw[k]) for k in range(1, K + 1)]
        size = scimat.norm2(x0) + sum(scimat.norm2(eta[k]) for k in range(1, K + 1))
        if scimat.norm2(dz) <= tol * (1.0 + size):  # @line L9
            break
    return trajectory(x0, eta, step, K), x0, eta, outer  # @line L10


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
