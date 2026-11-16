# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/control-limited-ddp/. The authors are listed in prov/DH08X0.jsonl.
"""Control-limited differential dynamic programming (Tassa, Mansard and Todorov).

The problem is

    minimize   J(U) = sum_k l(x_k, u_k) + l_f(x_N)
    subject to x_(k+1) = f(x_k, u_k),  x_0 given,  lo <= u_k <= hi.

The cost here is quadratic: l(x, u) = 1/2 (x - g)' Q (x - g) + 1/2 u' R u and
l_f(x) = 1/2 (x - g)' Q_f (x - g). The dynamics are any smooth function that
returns the next state and its Jacobians A = f_x and B = f_u. The second
derivatives of f are dropped (the Gauss-Newton form of DDP, often called
iLQR); the box handling below is the same for the full second-order form.

In the backward pass, the feedforward step of each stage is the solution of
a small quadratic program with box constraints, solved by a projected Newton
method. The feedback gain is computed on the free controls only, and its
rows for the clamped controls are zero, so a clamped control does not react
to state deviations. The forward pass clamps every control to the box.
"""

import math


def zeros(r, c):
    return [[0.0] * c for _ in range(r)]


def matmul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def matvec(a, v):
    return [sum(a[i][k] * v[k] for k in range(len(v))) for i in range(len(a))]


def transpose(a):
    return [list(r) for r in zip(*a)]


def madd(a, b, s=1.0):
    return [[a[i][j] + s * b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def vadd(a, b, s=1.0):
    return [a[i] + s * b[i] for i in range(len(a))]


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def symmetrize(a):
    n = len(a)
    return [[0.5 * (a[i][j] + a[j][i]) for j in range(n)] for i in range(n)]


def cholesky(a):
    """Lower triangular L with L L' = a, or None if a is not positive definite."""
    n = len(a)
    low = zeros(n, n)
    for i in range(n):
        for j in range(i + 1):
            s = a[i][j] - sum(low[i][k] * low[j][k] for k in range(j))
            if i == j:
                if s <= 0.0:
                    return None
                low[i][i] = math.sqrt(s)
            else:
                low[i][j] = s / low[j][j]
    return low


def chol_solve(low, b):
    n = len(low)
    y = [0.0] * n
    for i in range(n):
        y[i] = (b[i] - sum(low[i][k] * y[k] for k in range(i))) / low[i][i]
    x = [0.0] * n
    for i in reversed(range(n)):
        x[i] = (y[i] - sum(low[k][i] * x[k] for k in range(i + 1, n))) / low[i][i]
    return x


def clamp(v, lo, hi):
    return [min(max(v[i], lo[i]), hi[i]) for i in range(len(v))]


def qp_value(h, g, x):
    return 0.5 * dot(x, matvec(h, x)) + dot(g, x)


def box_qp(h, g, lo, hi, x0=None, max_iter=100, tol=1e-12):
    """Minimize 1/2 x' h x + g' x subject to lo <= x <= hi, h positive definite.

    Projected Newton: fix the variables that sit at a bound with the gradient
    pushing outward, take a Newton step in the others, project onto the box,
    and backtrack until the value drops enough. The value never goes up, so
    the result is never worse than the projection of x0. Returns x and the
    list of free indices at x."""
    n = len(g)
    x = clamp(x0 if x0 is not None else [0.0] * n, lo, hi)
    for _ in range(max_iter):
        grad = vadd(matvec(h, x), g)
        free = [i for i in range(n) if not ((x[i] <= lo[i] and grad[i] > 0.0) or (x[i] >= hi[i] and grad[i] < 0.0))]
        if not free or math.sqrt(sum(grad[i] ** 2 for i in free)) < tol:
            break
        low = cholesky([[h[i][j] for j in free] for i in free])
        step_f = chol_solve(low, [-grad[i] for i in free])
        direction = [0.0] * n
        for a, i in enumerate(free):
            direction[i] = step_f[a]
        fx, t, moved = qp_value(h, g, x), 1.0, False
        while t > 1e-14:
            xn = clamp(vadd(x, direction, t), lo, hi)
            if qp_value(h, g, xn) <= fx + 0.1 * min(0.0, dot(grad, vadd(xn, x, -1.0))):
                moved = xn != x
                x = xn
                break
            t *= 0.5
        if not moved:
            break
    grad = vadd(matvec(h, x), g)
    free = [i for i in range(n) if not ((x[i] <= lo[i] and grad[i] > 0.0) or (x[i] >= hi[i] and grad[i] < 0.0))]
    return x, free


class Problem:
    """Dynamics dyn(x, u) -> (x_next, A, B) and a quadratic cost."""

    def __init__(self, dyn, x0, goal, q, r, qf, lo, hi):
        self.dyn, self.x0, self.goal = dyn, list(x0), list(goal)
        self.q, self.r, self.qf = q, r, qf
        self.lo, self.hi = list(lo), list(hi)

    def running(self, x, u):
        e = vadd(x, self.goal, -1.0)
        return 0.5 * dot(e, matvec(self.q, e)) + 0.5 * dot(u, matvec(self.r, u))

    def final(self, x):
        e = vadd(x, self.goal, -1.0)
        return 0.5 * dot(e, matvec(self.qf, e))

    def rollout(self, us):
        xs = [list(self.x0)]
        for u in us:
            xs.append(self.dyn(xs[-1], u)[0])
        return xs

    def cost(self, xs, us):
        return sum(self.running(x, u) for x, u in zip(xs, us)) + self.final(xs[-1])


def backward(prob, xs, us, mu):
    """One backward pass. Returns (ks, Ks, dv1, dv2) or None if some Q_uu + mu I is not positive definite."""
    n = len(xs[0])
    vx = matvec(prob.qf, vadd(xs[-1], prob.goal, -1.0))  # @line L3
    vxx = [row[:] for row in prob.qf]
    ks, gains = [None] * len(us), [None] * len(us)
    dv1 = dv2 = 0.0
    for k in reversed(range(len(us))):  # @line L4
        x, u = xs[k], us[k]
        _, a, b = prob.dyn(x, u)
        at, bt = transpose(a), transpose(b)
        qx = vadd(matvec(prob.q, vadd(x, prob.goal, -1.0)), matvec(at, vx))  # @line L5
        qu = vadd(matvec(prob.r, u), matvec(bt, vx))
        qxx = madd(prob.q, matmul(matmul(at, vxx), a))
        quu = madd(prob.r, matmul(matmul(bt, vxx), b))
        qux = matmul(matmul(bt, vxx), a)
        m = len(u)
        h = [[quu[i][j] + (mu if i == j else 0.0) for j in range(m)] for i in range(m)]
        if cholesky(h) is None:
            return None
        lo_k = [prob.lo[i] - u[i] for i in range(m)]
        hi_k = [prob.hi[i] - u[i] for i in range(m)]
        kff, free = box_qp(h, qu, lo_k, hi_k)  # @line L6
        gain = zeros(m, n)  # @line L7
        if free:
            low = cholesky([[h[i][j] for j in free] for i in free])
            for c in range(n):
                col = chol_solve(low, [-qux[i][c] for i in free])
                for a_, i in enumerate(free):
                    gain[i][c] = col[a_]
        ks[k], gains[k] = kff, gain
        dv1 += dot(kff, qu)
        dv2 += 0.5 * dot(kff, matvec(h, kff))
        kt = transpose(gain)
        vx = vadd(vadd(vadd(qx, matvec(kt, matvec(quu, kff))), matvec(kt, qu)), matvec(transpose(qux), kff))  # @line L8
        vxx = symmetrize(madd(madd(madd(qxx, matmul(matmul(kt, quu), gain)), matmul(kt, qux)), matmul(transpose(qux), gain)))
    return ks, gains, dv1, dv2


def forward(prob, xs, us, ks, gains, alpha):
    new_x, new_u = [list(prob.x0)], []
    for k in range(len(us)):
        dx = vadd(new_x[-1], xs[k], -1.0)
        u = clamp(vadd(vadd(us[k], ks[k], alpha), matvec(gains[k], dx)), prob.lo, prob.hi)  # @line L11
        new_u.append(u)
        new_x.append(prob.dyn(new_x[-1], u)[0])
    return new_x, new_u


def control_limited_ddp(prob, us, iters=200, tol=1e-10, mu0=0.0, mu_min=1e-6, mu_max=1e10, c=0.1, log=None):
    """Returns (xs, us, info). info has the cost after every accepted iteration."""
    us = [clamp(u, prob.lo, prob.hi) for u in us]
    xs = prob.rollout(us)  # @line L1
    cost = prob.cost(xs, us)
    mu = mu0
    info = {"costs": [cost], "iterations": 0, "mu": mu}
    for _ in range(iters):  # @line L2
        out = backward(prob, xs, us, mu)
        if out is None:
            mu = max(mu * 10.0, mu_min)
            if mu > mu_max:
                break
            continue
        ks, gains, dv1, dv2 = out
        if -(dv1 + dv2) < tol:  # @line L9
            break
        accepted = False
        alpha = 1.0
        for _ in range(12):  # @line L10
            new_x, new_u = forward(prob, xs, us, ks, gains, alpha)
            new_cost = prob.cost(new_x, new_u)
            expected = alpha * dv1 + alpha * alpha * dv2
            if new_cost - cost <= c * expected:  # @line L12
                accepted = True
                break
            alpha *= 0.5
        if accepted:
            xs, us, cost = new_x, new_u, new_cost
            info["costs"].append(cost)
            info["iterations"] += 1
            mu = mu / 10.0 if mu / 10.0 >= mu_min else 0.0
            if log is not None:
                log.append((cost, alpha, mu))
        else:
            mu = max(mu * 10.0, mu_min)  # @line L13
            if mu > mu_max:
                break
    info["mu"] = mu
    return xs, us, info  # @line L14


def pendulum(dt=0.05, g=9.81, damping=0.1):
    """theta'' = u - g sin(theta) - damping * theta', explicit Euler. theta = 0 hangs down."""
    def dyn(x, u):
        th, om = x
        nx = [th + dt * om, om + dt * (u[0] - g * math.sin(th) - damping * om)]
        a = [[1.0, dt], [-dt * g * math.cos(th), 1.0 - dt * damping]]
        b = [[0.0], [dt]]
        return nx, a, b
    return dyn


def double_integrator(dt=0.1):
    def dyn(x, u):
        nx = [x[0] + dt * x[1], x[1] + dt * u[0]]
        return nx, [[1.0, dt], [0.0, 1.0]], [[0.0], [dt]]
    return dyn
