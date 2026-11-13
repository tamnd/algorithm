# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/active-contours/. The authors are listed in prov/JHEZE1.jsonl.

"""A closed active contour (snake) of Kass, Witkin and Terzopoulos, with the semi-implicit step.

The contour is a list of n points (x, y) in image coordinates, x to the right
and y downward, with pixel (i, j) at [j][i]. The point after point n - 1 is
point 0. The energy is

    E(v) = sum_i alpha/2 |v[i+1] - v[i]|^2 + beta/2 |v[i+1] - 2 v[i] + v[i-1]|^2 + sum_i P(v[i])

where the image energy P is a function that returns (P, dP/dx, dP/dy). The
usual P is spline_potential(S, weight) = -weight * f, with f the cubic B-spline
function of an edge strength grid S. Each step solves
(A + gamma I) x' = gamma x - dP/dx(v), and the same for y, where A is the
matrix of the internal energy.
"""

import math
from typing import Callable

Grid = list[list[float]]
Potential = Callable[[float, float], tuple[float, float, float]]


def _bspline(t: float) -> tuple[float, float, float]:
    """Cubic B-spline b(t), b'(t), b''(t)."""
    a = abs(t)
    s = 1.0 if t >= 0 else -1.0
    if a < 1:
        return 2 / 3 - a * a + a ** 3 / 2, s * (-2 * a + 1.5 * a * a), -2 + 3 * a
    if a < 2:
        return (2 - a) ** 3 / 6, -s * (2 - a) ** 2 / 2, 2 - a
    return 0.0, 0.0, 0.0


def spline_potential(strength: Grid, weight: float) -> Potential:
    """P(x, y) = -weight * sum S[j][i] b(x - i) b(y - j), with clamped reads of S.

    P has two continuous derivatives, and its gradient is Lipschitz with constant
    6.25 * weight * max|S|, because sum |b''| <= 4 and sum |b'| <= 1.5."""
    h, w = len(strength), len(strength[0])

    def p(x: float, y: float) -> tuple[float, float, float]:
        x0, y0 = math.floor(x), math.floor(y)
        f = fx = fy = 0.0
        for j in range(y0 - 1, y0 + 3):
            by, dby, _ = _bspline(y - j)
            row = strength[min(max(j, 0), h - 1)]
            for i in range(x0 - 1, x0 + 3):
                bx, dbx, _ = _bspline(x - i)
                s = row[min(max(i, 0), w - 1)]
                f += s * bx * by
                fx += s * dbx * by
                fy += s * bx * dby
        return -weight * f, -weight * fx, -weight * fy

    return p


def internal_matrix(n: int, alpha: float, beta: float) -> list[list[float]]:
    """A = alpha L + beta L L, with L the circulant matrix of the cycle, rows (-1, 2, -1)."""
    lap = [[0.0] * n for _ in range(n)]
    for i in range(n):
        lap[i][i] += 2.0
        lap[i][(i - 1) % n] -= 1.0
        lap[i][(i + 1) % n] -= 1.0
    sq = [[sum(lap[i][k] * lap[k][j] for k in range(n)) for j in range(n)] for i in range(n)]
    return [[alpha * lap[i][j] + beta * sq[i][j] for j in range(n)] for i in range(n)]


def cholesky(a: list[list[float]]) -> list[list[float]]:
    """Return the lower triangular C with C C^T = a, for a symmetric positive definite a."""
    n = len(a)
    c = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1):
            s = a[i][j] - sum(c[i][k] * c[j][k] for k in range(j))
            if i == j:
                if s <= 0:
                    raise ValueError("matrix is not positive definite")
                c[i][i] = math.sqrt(s)
            else:
                c[i][j] = s / c[j][j]
    return c


def solve(c: list[list[float]], b: list[float]) -> list[float]:
    """Solve C C^T x = b by a forward and a back substitution."""
    n = len(b)
    z = [0.0] * n
    for i in range(n):
        z[i] = (b[i] - sum(c[i][k] * z[k] for k in range(i))) / c[i][i]
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (z[i] - sum(c[k][i] * x[k] for k in range(i + 1, n))) / c[i][i]
    return x


def energy(points: list[tuple[float, float]], potential: Potential, alpha: float, beta: float) -> float:
    """The discrete snake energy E(v), summed term by term."""
    n = len(points)
    e = 0.0
    for i in range(n):
        (xp, yp), (x, y), (xn, yn) = points[i - 1], points[i], points[(i + 1) % n]
        e += alpha / 2 * ((xn - x) ** 2 + (yn - y) ** 2)
        e += beta / 2 * ((xn - 2 * x + xp) ** 2 + (yn - 2 * y + yp) ** 2)
        e += potential(x, y)[0]
    return e


def snake(points: list[tuple[float, float]], potential: Potential, alpha: float, beta: float,
          gamma: float, iterations: int) -> list[tuple[float, float]]:
    """Run the semi-implicit iteration and return the final contour. Needs n >= 3 and gamma > 0."""
    n = len(points)
    if n < 3 or gamma <= 0 or alpha < 0 or beta < 0:
        raise ValueError("need n >= 3, gamma > 0, alpha >= 0 and beta >= 0")
    a = internal_matrix(n, alpha, beta)  # @line L1
    c = cholesky([[a[i][j] + (gamma if i == j else 0.0) for j in range(n)] for i in range(n)])  # @line L2
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    for _ in range(iterations):  # @line L3
        grad = [potential(xs[i], ys[i]) for i in range(n)]  # @line L4
        xs = solve(c, [gamma * xs[i] - grad[i][1] for i in range(n)])  # @line L5
        ys = solve(c, [gamma * ys[i] - grad[i][2] for i in range(n)])  # @line L6
    return list(zip(xs, ys))  # @line L7


def edge_strength(image: Grid, sigma: float) -> Grid:
    """Squared central difference gradient of the Gaussian smoothed image, scaled to a maximum of 1."""
    h, w = len(image), len(image[0])
    r = max(1, math.ceil(3 * sigma))
    raw = [math.exp(-(k * k) / (2 * sigma * sigma)) for k in range(-r, r + 1)]
    g = [v / sum(raw) for v in raw]
    tmp = [[sum(g[k + r] * image[y][min(max(x + k, 0), w - 1)] for k in range(-r, r + 1)) for x in range(w)]
           for y in range(h)]
    sm = [[sum(g[k + r] * tmp[min(max(y + k, 0), h - 1)][x] for k in range(-r, r + 1)) for x in range(w)]
          for y in range(h)]

    def at(x: int, y: int) -> float:
        return sm[min(max(y, 0), h - 1)][min(max(x, 0), w - 1)]

    out = [[(at(x + 1, y) - at(x - 1, y)) ** 2 + (at(x, y + 1) - at(x, y - 1)) ** 2 for x in range(w)]
           for y in range(h)]
    top = max(max(row) for row in out)
    return [[v / top for v in row] for row in out] if top > 0 else out
