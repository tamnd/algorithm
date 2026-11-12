# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/regularization/. The authors are listed in prov/M5KEQK.jsonl.
"""Tikhonov (L2) regularization of least squares in its penalized and constrained forms, its MAP
reading, the stability bound of regularized loss minimization, the L1 and L2 shrinkage maps, and early
stopping of gradient descent.

Convention: L_S(w) = (1/n) sum_i (w . x_i - y_i)^2 and the penalized objective is L_S(w) + lam ||w||^2.
"""

import math
import random

Vec = list[float]
Mat = list[list[float]]


def dot(a: Vec, b: Vec) -> float:
    return sum(x * y for x, y in zip(a, b))


def norm(a: Vec) -> float:
    return math.sqrt(dot(a, a))


def solve(a: Mat, b: Vec) -> Vec:
    """Gaussian elimination with partial pivoting."""
    n = len(a)
    m = [row[:] + [b[i]] for i, row in enumerate(a)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(m[r][c]))
        m[c], m[p] = m[p], m[c]
        for r in range(c + 1, n):
            t = m[r][c] / m[c][c]
            for k in range(c, n + 1):
                m[r][k] -= t * m[c][k]
    x = [0.0] * n
    for r in range(n - 1, -1, -1):
        x[r] = (m[r][n] - sum(m[r][k] * x[k] for k in range(r + 1, n))) / m[r][r]
    return x


def moments(xs: Mat, ys: Vec) -> tuple[Mat, Vec]:
    """Sigma = X^T X / n and c = X^T y / n."""
    n, d = len(xs), len(xs[0])
    sig = [[sum(x[i] * x[j] for x in xs) / n for j in range(d)] for i in range(d)]
    c = [sum(x[i] * y for x, y in zip(xs, ys)) / n for i in range(d)]
    return sig, c


def empirical_risk(w: Vec, xs: Mat, ys: Vec) -> float:
    return sum((dot(w, x) - y) ** 2 for x, y in zip(xs, ys)) / len(xs)


def ridge(xs: Mat, ys: Vec, lam: float) -> Vec:
    """The minimizer of L_S(w) + lam ||w||^2: (Sigma + lam I) w = c."""
    sig, c = moments(xs, ys)
    for i in range(len(c)):
        sig[i][i] += lam
    return solve(sig, c)


def lambda_for_radius(xs: Mat, ys: Vec, t: float, iters: int = 200) -> float:
    """The lam > 0 with ||ridge(lam)|| = t, by bisection on a log scale (||ridge(lam)|| falls with lam).
    Requires 0 < t < ||ridge(0)||."""
    lo, hi = 1e-12, 1.0
    while norm(ridge(xs, ys, hi)) > t:
        hi *= 2
    for _ in range(iters):
        mid = math.sqrt(lo * hi)
        if norm(ridge(xs, ys, mid)) > t:
            lo = mid
        else:
            hi = mid
    return math.sqrt(lo * hi)


def constrained_least_squares(xs: Mat, ys: Vec, t: float, steps: int = 20000) -> Vec:
    """Minimize L_S(w) subject to ||w|| <= t, by projected gradient descent with step 1 / (2 s_max)."""
    sig, c = moments(xs, ys)
    d = len(c)
    s_max = max(sum(abs(v) for v in row) for row in sig)  # an upper bound on the largest eigenvalue
    eta = 1 / (2 * s_max)
    w = [0.0] * d
    for _ in range(steps):
        g = [2 * (dot(sig[i], w) - c[i]) for i in range(d)]
        w = [w[i] - eta * g[i] for i in range(d)]
        r = norm(w)
        if r > t:
            w = [v * t / r for v in w]
    return w


def map_gradient(w: Vec, xs: Mat, ys: Vec, noise_var: float, prior_var: float) -> Vec:
    """The gradient of the negative log posterior, Gaussian likelihood and prior N(0, prior_var I)."""
    d = len(w)
    r = [dot(w, x) - y for x, y in zip(xs, ys)]
    return [sum(ri * x[i] for ri, x in zip(r, xs)) / noise_var + w[i] / prior_var for i in range(d)]


def soft_threshold(z: float, a: float) -> float:
    """argmin_w (1/2)(w - z)^2 + a |w|: the L1 (lasso) shrinkage of one coordinate."""
    return math.copysign(max(abs(z) - a, 0.0), z)


def l2_shrink(z: float, a: float) -> float:
    """argmin_w (1/2)(w - z)^2 + (a/2) w^2: the L2 (ridge) shrinkage of one coordinate."""
    return z / (1 + a)


def gradient_descent_path(xs: Mat, ys: Vec, eta: float, steps: int) -> list[Vec]:
    """Plain gradient descent on L_S from w = 0; returns w_0, ..., w_steps."""
    sig, c = moments(xs, ys)
    d = len(c)
    w = [0.0] * d
    path = [w]
    for _ in range(steps):
        w = [w[i] - eta * 2 * (dot(sig[i], w) - c[i]) for i in range(d)]
        path.append(w)
    return path


def stability_bound(xs: Mat, ys: Vec, lam: float, n: int) -> float:
    """2 rho / (lam n) for samples of size n, with rho = 2 (B R + Y) R, the Lipschitz constant of the
    squared loss on the ball of radius B = Y / sqrt(lam). Here R bounds ||x|| and Y bounds |y| over all the
    given points (pass the union of S and the replaced example). Both minimizers lie in that ball."""
    r_max = max(norm(x) for x in xs)
    y_max = max(abs(y) for y in ys)
    b = y_max / math.sqrt(lam)
    rho = 2 * (b * r_max + y_max) * r_max
    return 2 * rho / (lam * n)


def make_data(n: int, d: int, rng: random.Random) -> tuple[Mat, Vec]:
    w_true = [rng.uniform(-1, 1) for _ in range(d)]
    xs = [[rng.uniform(-1, 1) for _ in range(d)] for _ in range(n)]
    ys = [max(-2.0, min(2.0, dot(w_true, x) + rng.gauss(0, 0.3))) for x in xs]
    return xs, ys


if __name__ == "__main__":
    xs, ys = make_data(20, 3, random.Random(1))
    for lam in (0.0, 0.01, 0.1, 1.0):
        w = ridge(xs, ys, lam)
        print(lam, [round(v, 4) for v in w], round(norm(w), 4), round(empirical_risk(w, xs, ys), 4))
