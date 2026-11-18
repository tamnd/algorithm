# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/spacetime-constraints/. The authors are listed in prov/5ZYH4C.jsonl.
"""Spacetime constraints on a one degree of freedom body (Witkin and Kass 1988).

The trajectory x(t) on [0, T] is sampled at n + 1 times with step h = T / n.
The unknowns are the states x_0 .. x_n and the controls f_1 .. f_(n-1), one per
interior time. The constraints are

    dynamics   (x_(i+1) - 2 x_i + x_(i-1)) / h^2 + k sin(x_i) + g - f_i = 0,
    boundary   x_0 = a, (x_1 - x_0) / h = 0, x_n = b, (x_n - x_(n-1)) / h = 0,

and the objective is the effort R = h sum f_i^2. With k = 0 this is a unit
mass under a constant gravity g, pushed by the force f. With g = 0 it is a
pendulum, x the angle and k = gravity / length, turned by the torque f.

The constrained problem is solved by sequential quadratic programming: at
each step the constraints are linearized, the Lagrangian is modeled to
second order, and one linear KKT system gives the step and the new
multipliers. For k = 0 the problem is a quadratic program, and the first step
is exact.
"""

import math

from anim import solve


def residuals(z, n, h, k, g, a, b):
    """Return the constraint values c(z): n - 1 dynamics rows, then 4 boundary rows."""
    x, f = z[: n + 1], z[n + 1 :]
    c = []
    for i in range(1, n):
        c.append((x[i + 1] - 2.0 * x[i] + x[i - 1]) / (h * h) + k * math.sin(x[i]) + g - f[i - 1])
    c.append(x[0] - a)
    c.append((x[1] - x[0]) / h)
    c.append(x[n] - b)
    c.append((x[n] - x[n - 1]) / h)
    return c


def jacobian(z, n, h, k):
    """Return the dense Jacobian of the constraints, one row per constraint."""
    size = 2 * n
    rows = []
    for i in range(1, n):
        r = [0.0] * size
        r[i - 1] += 1.0 / (h * h)
        r[i] += -2.0 / (h * h) + k * math.cos(z[i])
        r[i + 1] += 1.0 / (h * h)
        r[n + i] = -1.0
        rows.append(r)
    for idx, coef in (((0,), (1.0,)), ((0, 1), (-1.0 / h, 1.0 / h)), ((n,), (1.0,)), ((n - 1, n), (-1.0 / h, 1.0 / h))):
        r = [0.0] * size
        for j, w in zip(idx, coef):
            r[j] = w
        rows.append(r)
    return rows


def effort(z, n, h):
    """Return R = h sum f_i^2."""
    return h * sum(v * v for v in z[n + 1 :])


def spacetime(n, k=0.0, g=0.0, a=0.0, b=1.0, duration=1.0, max_iter=50, tol=1e-11):
    """Solve the spacetime problem. Return (x, f, effort, iterations)."""
    h = duration / n
    size = 2 * n
    z = [a + (b - a) * i / n for i in range(n + 1)] + [0.0] * (n - 1)  # @line L1
    lam = [0.0] * (n + 3)
    for it in range(1, max_iter + 1):  # @line L2
        c = residuals(z, n, h, k, g, a, b)  # @line L3
        jac = jacobian(z, n, h, k)
        grad = [0.0] * (n + 1) + [2.0 * h * v for v in z[n + 1 :]]
        m = len(c)
        kkt = [[0.0] * (size + m) for _ in range(size + m)]
        for i in range(1, n):  # @line L4
            kkt[i][i] = -lam[i - 1] * k * math.sin(z[i])
        for j in range(n + 1, size):
            kkt[j][j] = 2.0 * h
        for r in range(m):
            for j in range(size):
                kkt[size + r][j] = jac[r][j]
                kkt[j][size + r] = jac[r][j]
        rhs = [-v for v in grad] + [-v for v in c]
        sol = solve(kkt, rhs)  # @line L5
        dz, lam = sol[:size], sol[size:]
        z = [p + q for p, q in zip(z, dz)]  # @line L6
        if max(abs(v) for v in dz) <= tol * (1.0 + max(abs(v) for v in z)):  # @line L7
            break
    return z[: n + 1], z[n + 1 :], effort(z, n, h), it  # @line L8
