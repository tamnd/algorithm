# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/proper-generalized-decomposition/. The authors are listed in prov/TWTF98.jsonl.
"""Proper generalized decomposition (PGD) by greedy rank-one enrichment with alternating directions.

The model problem is -a u_xx - b u_yy = f on the unit square with u = 0 on the boundary, with
central differences on nx by ny interior points. With U[i][j] = u(x_i, y_j), the discrete system is
    Kx U + U Ky = F,
where Kx = (a / hx^2) tridiag(-1, 2, -1) and Ky = (b / hy^2) tridiag(-1, 2, -1). This is the
Kronecker system (Kx (x) I + I (x) Ky) vec(U) = vec(F). PGD writes U as a sum of products
X_1 Y_1^T + ... + X_M Y_M^T and never forms a matrix of size nx * ny: F is given in the
separated form F = sum_s fx_s fy_s^T, and every residual is kept as a list of products.
"""

import math

Vector = list[float]
Terms = list[tuple[Vector, Vector]]  # a matrix sum_t p_t q_t^T


def dot(u: Vector, v: Vector) -> float:
    return sum(a * b for a, b in zip(u, v))


def tri_apply(d: float, o: float, v: Vector) -> Vector:
    """(d on the diagonal, o off the diagonal) times v."""
    n = len(v)
    return [d * v[i] + o * ((v[i - 1] if i > 0 else 0.0) + (v[i + 1] if i < n - 1 else 0.0)) for i in range(n)]


def tri_solve(d: float, o: float, rhs: Vector) -> Vector:
    """Solve the constant tridiagonal system (d, o) z = rhs by the Thomas algorithm."""
    n = len(rhs)
    c = [0.0] * n
    g = [0.0] * n
    m = d
    c[0], g[0] = o / m, rhs[0] / m
    for i in range(1, n):
        m = d - o * c[i - 1]
        c[i] = o / m
        g[i] = (rhs[i] - o * g[i - 1]) / m
    z = [0.0] * n
    z[-1] = g[-1]
    for i in range(n - 2, -1, -1):
        z[i] = g[i] - c[i] * z[i + 1]
    return z


class Laplace2D:
    def __init__(self, nx: int, ny: int, a: float = 1.0, b: float = 1.0):
        self.nx, self.ny = nx, ny
        hx, hy = 1.0 / (nx + 1), 1.0 / (ny + 1)
        self.kx = (2.0 * a / hx ** 2, -a / hx ** 2)
        self.ky = (2.0 * b / hy ** 2, -b / hy ** 2)

    def kx_apply(self, v: Vector) -> Vector:
        return tri_apply(self.kx[0], self.kx[1], v)

    def ky_apply(self, v: Vector) -> Vector:
        return tri_apply(self.ky[0], self.ky[1], v)


def residual_terms(op: Laplace2D, f: Terms, modes: Terms) -> Terms:
    """R = F - Kx U - U Ky for U = sum X_m Y_m^T, as a list of products."""
    out = list(f)
    for x, y in modes:
        out.append(([-t for t in op.kx_apply(x)], y))
        out.append(([-t for t in x], op.ky_apply(y)))
    return out


def norm2(terms: Terms) -> float:
    """Squared Frobenius norm of sum p_t q_t^T, by the Gram identity."""
    total = 0.0
    for i, (p, q) in enumerate(terms):
        total += dot(p, p) * dot(q, q)
        for p2, q2 in terms[i + 1:]:
            total += 2.0 * dot(p, p2) * dot(q, q2)
    return max(total, 0.0)


def times_right(terms: Terms, y: Vector) -> Vector:
    """R y."""
    out = [0.0] * len(terms[0][0])
    for p, q in terms:
        c = dot(q, y)
        out = [a + c * b for a, b in zip(out, p)]
    return out


def times_left(terms: Terms, x: Vector) -> Vector:
    """R^T x."""
    out = [0.0] * len(terms[0][1])
    for p, q in terms:
        c = dot(p, x)
        out = [a + c * b for a, b in zip(out, q)]
    return out


def start_vector(terms: Terms, nx: int) -> Vector:
    """A Y with R Y != 0 when R != 0: Y = R^T w for w = (1, ..., 1), then w = e_1, e_2, ..."""
    for w in [[1.0] * nx] + [[1.0 if i == j else 0.0 for i in range(nx)] for j in range(nx)]:
        y = times_left(terms, w)
        if any(t != 0.0 for t in y):
            return y
    raise ValueError("the residual is zero")


def solve_x(op: Laplace2D, terms: Terms, y: Vector) -> Vector:
    """The minimizer over X of the energy for a fixed Y: (|Y|^2 Kx + (Y^T Ky Y) I) X = R Y."""
    yy, yky = dot(y, y), dot(y, op.ky_apply(y))
    return tri_solve(yy * op.kx[0] + yky, yy * op.kx[1], times_right(terms, y))


def solve_y(op: Laplace2D, terms: Terms, x: Vector) -> Vector:
    """The minimizer over Y for a fixed X: ((X^T Kx X) I + |X|^2 Ky) Y = R^T X."""
    xx, xkx = dot(x, x), dot(x, op.kx_apply(x))
    return tri_solve(xx * op.ky[0] + xkx, xx * op.ky[1], times_left(terms, x))


def pgd(op: Laplace2D, f: Terms, m_max: int, tol: float = 1e-8, inner_tol: float = 1e-10, inner_max: int = 50) -> tuple[Terms, list[float], list[int]]:
    """Return the modes (X_m, Y_m), the relative residuals before each step, and the inner counts."""
    modes: Terms = []  # @line L1: U <- 0
    fnorm = math.sqrt(norm2(f))
    res: list[float] = []
    inner: list[int] = []
    for _ in range(m_max):  # @line L2
        terms = residual_terms(op, f, modes)  # @line L3: R = F - Kx U - U Ky
        res.append(math.sqrt(norm2(terms)) / fnorm)
        if res[-1] <= tol:  # @line L4: stop when the residual is small
            break
        y = start_vector(terms, op.nx)  # @line L5
        it = 0
        for it in range(inner_max):  # @line L6: alternating directions
            x = solve_x(op, terms, y)  # @line L7
            y_new = solve_y(op, terms, x)  # @line L8
            # the change from X Y^T to X Y_new^T in the Frobenius norm, relative
            xx = dot(x, x)
            ch = xx * (dot(y_new, y_new) - 2.0 * dot(y, y_new) + dot(y, y))
            y = y_new
            if ch <= inner_tol ** 2 * xx * dot(y, y):
                break
        inner.append(it + 1)
        modes.append((x, y))  # @line L9: U <- U + X Y^T
    return modes, res, inner  # @line L10


def to_dense(modes: Terms, nx: int, ny: int) -> list[Vector]:
    u = [[0.0] * ny for _ in range(nx)]
    for x, y in modes:
        for i in range(nx):
            for j in range(ny):
                u[i][j] += x[i] * y[j]
    return u
