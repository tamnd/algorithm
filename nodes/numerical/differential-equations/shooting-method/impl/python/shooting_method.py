# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shooting-method/. The authors are listed in prov/XXZ87A.jsonl.

"""Single and multiple shooting for y'' = g(x, y, y'), y(a) = alpha, y(b) = beta.

The initial value problems are solved with fixed-step classical RK4. Single shooting uses
Newton's method with the variational equation when the partial derivatives of g are given,
and the secant method otherwise. Multiple shooting uses Newton's method on the matching
conditions, with the variational equations for the Jacobian.
"""

from dataclasses import dataclass
from typing import Callable, List, Optional, Tuple

Vec = List[float]


def rk4(F: Callable[[float, Vec], Vec], x0: float, u0: Vec, x1: float, n: int) -> Vec:
    """Integrate u' = F(x, u) from x0 to x1 with n >= 1 RK4 steps; return u(x1)."""
    if n < 1:
        raise ValueError("need at least one step")
    h = (x1 - x0) / n
    u = list(u0)
    for i in range(n):
        x = x0 + i * h
        k1 = F(x, u)
        k2 = F(x + h / 2, [a + h / 2 * b for a, b in zip(u, k1)])
        k3 = F(x + h / 2, [a + h / 2 * b for a, b in zip(u, k2)])
        k4 = F(x + h, [a + h * b for a, b in zip(u, k3)])
        u = [a + h / 6 * (p + 2 * q + 2 * r + w) for a, p, q, r, w in zip(u, k1, k2, k3, k4)]
    return u


def _flow(g, gy, gp, x0, y0, p0, x1, n, with_jac):
    """Solve from (y0, p0) at x0 to x1. Returns (y, p) and, if with_jac, the 2x2 Jacobian
    d(y, p)(x1) / d(y0, p0) from the variational equation."""
    if not with_jac:
        y, p = rk4(lambda x, u: [u[1], g(x, u[0], u[1])], x0, [y0, p0], x1, n)
        return y, p, None

    def F(x, u):
        y, p = u[0], u[1]
        a, c = gy(x, y, p), gp(x, y, p)
        # columns (z, z') for the perturbations of y0 and of p0
        return [p, g(x, y, p), u[3], a * u[2] + c * u[3], u[5], a * u[4] + c * u[5]]

    u = rk4(F, x0, [y0, p0, 1.0, 0.0, 0.0, 1.0], x1, n)
    return u[0], u[1], [[u[2], u[4]], [u[3], u[5]]]


@dataclass
class ShootResult:
    slope: float
    iterations: int
    residual: float
    ivp_solves: int


def single_shooting(g, a, b, alpha, beta, s0, n=100, gy=None, gp=None, s1=None,
                    tol=1e-12, max_iter=50) -> ShootResult:
    """Find s with y(b; s) = beta, where y solves y'' = g, y(a) = alpha, y'(a) = s."""
    newton = gy is not None and gp is not None
    solves = 0
    if newton:
        s = s0  # @line L1
        for it in range(1, max_iter + 1):  # @line L2
            y, _, J = _flow(g, gy, gp, a, alpha, s, b, n, True)  # @line L3
            solves += 1
            r = y - beta  # @line L4
            if abs(r) <= tol * max(1.0, abs(beta)):
                return ShootResult(s, it - 1, r, solves)
            ds = J[0][1]
            if ds == 0:
                raise ZeroDivisionError("dy(b)/ds = 0: the shooting function has a critical point")
            step = r / ds
            s = s - step  # @line L5
            if abs(step) <= tol * (1.0 + abs(s)):  # @line L6
                return ShootResult(s, it, r, solves)
        raise RuntimeError("Newton iteration did not converge")  # @line L7
    # secant method
    s_prev, s = s0, (s1 if s1 is not None else s0 + 1.0)
    r_prev = _flow(g, gy, gp, a, alpha, s_prev, b, n, False)[0] - beta
    solves += 1
    for it in range(1, max_iter + 1):
        r = _flow(g, gy, gp, a, alpha, s, b, n, False)[0] - beta
        solves += 1
        if abs(r) <= tol * max(1.0, abs(beta)):
            return ShootResult(s, it, r, solves)
        if r == r_prev:
            raise ZeroDivisionError("secant step undefined")
        s_prev, s, r_prev = s, s - r * (s - s_prev) / (r - r_prev), r
    raise RuntimeError("secant iteration did not converge")


def profile(g, a, alpha, s, b, n) -> List[Tuple[float, float]]:
    """The values (x_i, y_i) of the IVP solution on the RK4 grid."""
    h = (b - a) / n
    out = [(a, alpha)]
    u = [alpha, s]
    for i in range(n):
        u = rk4(lambda x, v: [v[1], g(x, v[0], v[1])], a + i * h, u, a + (i + 1) * h, 1)
        out.append((a + (i + 1) * h, u[0]))
    return out


def _solve(M: List[List[float]], r: Vec) -> Vec:
    """Solve M x = r by Gaussian elimination with partial pivoting."""
    n = len(r)
    M = [row[:] + [r[i]] for i, row in enumerate(M)]
    for k in range(n):
        piv = max(range(k, n), key=lambda i: abs(M[i][k]))
        if M[piv][k] == 0:
            raise ZeroDivisionError("singular Jacobian")
        M[k], M[piv] = M[piv], M[k]
        for i in range(k + 1, n):
            m = M[i][k] / M[k][k]
            if m:
                for j in range(k, n + 1):
                    M[i][j] -= m * M[k][j]
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (M[i][n] - sum(M[i][j] * x[j] for j in range(i + 1, n))) / M[i][i]
    return x


def multiple_shooting(g, gy, gp, a, b, alpha, beta, segments, n_per, guess=None,
                      tol=1e-12, max_iter=50):
    """Multiple shooting with K = segments equal segments and n_per RK4 steps on each.

    Unknowns: the slope p_0 at a and (y_k, p_k) at the inner nodes x_1..x_(K-1).
    guess(x) gives a start profile (y, y'); default: the straight line from alpha to beta.
    Returns (nodes, values y_k, slopes p_k, iterations).
    """
    K = segments
    if K < 1:
        raise ValueError("need at least one segment")
    xs = [a + (b - a) * k / K for k in range(K + 1)]
    if guess is None:
        m = (beta - alpha) / (b - a)
        guess = lambda x: (alpha + m * (x - a), m)
    ys = [alpha] + [guess(x)[0] for x in xs[1:K]]
    ps = [guess(x)[1] for x in xs[:K]]
    for it in range(max_iter):
        # residuals and Jacobian; unknown order: p_0, y_1, p_1, ..., y_(K-1), p_(K-1)
        nU = 2 * K - 1
        J = [[0.0] * nU for _ in range(nU)]
        res = [0.0] * nU
        for k in range(K):
            y1, p1, Phi = _flow(g, gy, gp, xs[k], ys[k], ps[k], xs[k + 1], n_per, True)
            col_y = None if k == 0 else 2 * k - 1  # column of y_k
            col_p = 0 if k == 0 else 2 * k  # column of p_k
            if k < K - 1:
                rows = (2 * k, 2 * k + 1)  # y and p matching at x_(k+1)
                res[rows[0]] = y1 - ys[k + 1]
                res[rows[1]] = p1 - ps[k + 1]
                for r_i, row in enumerate(rows):
                    if col_y is not None:
                        J[row][col_y] += Phi[r_i][0]
                    J[row][col_p] += Phi[r_i][1]
                    J[row][2 * (k + 1) - 1 + r_i] -= 1.0
            else:
                row = nU - 1
                res[row] = y1 - beta
                if col_y is not None:
                    J[row][col_y] += Phi[0][0]
                J[row][col_p] += Phi[0][1]
        if max(abs(v) for v in res) <= tol * max(1.0, abs(beta)):
            return xs, ys + [beta], ps, it
        d = _solve(J, res)
        ps[0] -= d[0]
        for k in range(1, K):
            ys[k] -= d[2 * k - 1]
            ps[k] -= d[2 * k]
        if max(abs(v) for v in d) <= tol * (1.0 + max(abs(v) for v in ys + ps)):
            return xs, ys + [beta], ps, it + 1
    raise RuntimeError("Newton iteration did not converge")
