# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/four-dimensional-variational-assimilation/. The authors are listed in prov/XB7N6C.jsonl.

"""Strong-constraint four-dimensional variational assimilation (4D-Var).

Notation of Ide, Courtier, Ghil and Lorenc (1997). The window has the time
levels 0, 1, ..., K. The model step k maps x_(k-1) to x_k = M_k(x_(k-1)),
and the model is a perfect constraint, so the initial state x_0 fixes the
whole trajectory. Observations y_k with a linear operator H_k and an error
covariance R_k can be given at any subset of the time levels. The cost is

    J(x_0) = 1/2 (x_0 - x^b)^T B^-1 (x_0 - x^b) + sum_k 1/2 d_k^T R_k^-1 d_k,
    d_k = y_k - H_k x_k.

The gradient comes from one forward run and one backward run of the
adjoint model. The minimizer is BFGS with a backtracking line search,
started with B as the inverse Hessian, which is the inverse Hessian of the
background term.

A model is given by two functions:
    step(k, x)              returns x_k = M_k(x) for x = x_(k-1)
    adjoint(k, x, lam)      returns M_k'(x)^T lam, the adjoint of step k at x
"""

import scimat


def trajectory(x0, step, K):
    """Return [x_0, x_1, ..., x_K] for the model step from x0."""
    xs = [list(x0)]
    for k in range(1, K + 1):
        xs.append(step(k, xs[-1]))
    return xs


def cost_and_gradient(x0, xb, LB, obs, step, adjoint, K):
    """Return (J(x0), grad J(x0)).

    LB is the Cholesky factor of B, and obs maps a time level k to
    (H_k, y_k, LR_k) with LR_k the Cholesky factor of R_k.
    """
    xs = trajectory(x0, step, K)  # @line L3
    e = scimat.sub(x0, xb)
    J = 0.5 * scimat.dot(e, scimat.cholesky_solve(LB, e))
    forcing = {}
    for k, (H, y, LR) in obs.items():
        d = scimat.sub(y, scimat.matvec(H, xs[k]))
        rd = scimat.cholesky_solve(LR, d)
        J += 0.5 * scimat.dot(d, rd)  # @line L4
        forcing[k] = scimat.matvec(scimat.transpose(H), rd)
    lam = [0.0] * len(x0)  # @line L5
    for k in range(K, -1, -1):  # @line L6
        if k in forcing:
            lam = scimat.sub(lam, forcing[k])  # @line L7
        if k > 0:
            lam = adjoint(k, xs[k - 1], lam)  # @line L8
    g = scimat.add(scimat.cholesky_solve(LB, e), lam)  # @line L9
    return J, g


def _bfgs_update(Hinv, s, y):
    """Return the BFGS update of the inverse Hessian Hinv for the step s and the gradient change y."""
    sy = scimat.dot(s, y)
    if sy <= 0.0:
        return Hinv
    rho = 1.0 / sy
    hy = scimat.matvec(Hinv, y)
    c = rho * rho * scimat.dot(y, hy) + rho
    n = len(s)
    return [[Hinv[i][j] - rho * (s[i] * hy[j] + hy[i] * s[j]) + c * s[i] * s[j] for j in range(n)] for i in range(n)]


def var4d(xb, B, obs, step, adjoint, K, max_iter=500, tol=1e-12):
    """Return (x_0^a, number of iterations) for strong-constraint 4D-Var.

    obs maps a time level k in 0..K to (H_k, y_k, R_k). The iteration stops
    when |grad J| <= tol (1 + |grad J(x^b)|) or after max_iter iterations.
    """
    LB = scimat.cholesky(B)
    ob = {k: (H, y, scimat.cholesky(R)) for k, (H, y, R) in obs.items()}
    x = [float(v) for v in xb]  # @line L1
    J, g = cost_and_gradient(x, xb, LB, ob, step, adjoint, K)
    g0 = scimat.norm2(g)
    Hinv = [[float(v) for v in row] for row in B]
    it = 0
    for it in range(max_iter):  # @line L2
        if scimat.norm2(g) <= tol * (1.0 + g0):  # @line L10
            break
        p = [-v for v in scimat.matvec(Hinv, g)]  # @line L11
        gp = scimat.dot(g, p)
        if gp >= 0.0:
            Hinv = [[float(v) for v in row] for row in B]
            p = [-v for v in scimat.matvec(Hinv, g)]
            gp = scimat.dot(g, p)
        a = 1.0
        while True:
            xn = [xi + a * pi for xi, pi in zip(x, p)]
            Jn, gn = cost_and_gradient(xn, xb, LB, ob, step, adjoint, K)
            # Armijo test, with a rounding allowance for the last steps
            if Jn <= J + 1e-4 * a * gp + 1e-14 * abs(J) or a < 1e-12:
                break
            a *= 0.5
        Hinv = _bfgs_update(Hinv, scimat.sub(xn, x), scimat.sub(gn, g))
        x, J, g = xn, Jn, gn
    return x, it  # @line L12


def linear_model(M):
    """Return (step, adjoint) for the linear model x_k = M x_(k-1) with a fixed matrix M."""
    Mt = scimat.transpose(M)
    return (lambda k, x: scimat.matvec(M, x)), (lambda k, x, lam: scimat.matvec(Mt, lam))


def lorenz63(dt=0.01, sigma=10.0, rho=28.0, beta=8.0 / 3.0):
    """Return (step, tangent, adjoint) for forward Euler steps of the Lorenz-63 model.

    tangent(k, x, dx) is M_k'(x) dx and adjoint(k, x, lam) is M_k'(x)^T lam.
    """

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
