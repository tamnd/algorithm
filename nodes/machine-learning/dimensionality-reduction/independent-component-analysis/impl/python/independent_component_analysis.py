# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/independent-component-analysis/. The authors are listed in prov/RPTZE3.jsonl.

"""Independent component analysis by whitening and Jacobi rotations.

This is the approach of Comon (1994): whiten the data, then apply plane
rotations to pairs of components, each chosen to maximize the contrast
sum_i kurt(y_i)^2, the sum of squared fourth-order cumulants. For whitened
data the kurtosis of a rotated pair is a quartic form in (cos t, sin t) whose
coefficients are five fourth-order moments, so the best angle is found by a
search over t in [0, pi/2) that costs O(1) per angle after O(n) work.
"""

import math

Vector = list[float]
Matrix = list[list[float]]


def jacobi_eigh(a: Matrix, tol: float = 1e-14, max_sweeps: int = 100) -> tuple[Vector, Matrix]:
    """Eigenvalues (descending) and eigenvectors (as columns) of a symmetric matrix."""
    d = len(a)
    m = [row[:] for row in a]
    v = [[1.0 if i == j else 0.0 for j in range(d)] for i in range(d)]
    for _ in range(max_sweeps):
        off = sum(m[i][j] ** 2 for i in range(d) for j in range(d) if i != j)
        scale = sum(m[i][i] ** 2 for i in range(d)) + off
        if off <= tol * tol * max(scale, 1e-300):
            break
        for p in range(d - 1):
            for q in range(p + 1, d):
                if m[p][q] == 0.0:
                    continue
                theta = (m[q][q] - m[p][p]) / (2.0 * m[p][q])
                t = math.copysign(1.0, theta) / (abs(theta) + math.sqrt(theta * theta + 1.0))
                c = 1.0 / math.sqrt(t * t + 1.0)
                s = t * c
                for k in range(d):
                    m[k][p], m[k][q] = c * m[k][p] - s * m[k][q], s * m[k][p] + c * m[k][q]
                for k in range(d):
                    m[p][k], m[q][k] = c * m[p][k] - s * m[q][k], s * m[p][k] + c * m[q][k]
                for k in range(d):
                    v[k][p], v[k][q] = c * v[k][p] - s * v[k][q], s * v[k][p] + c * v[k][q]
    order = sorted(range(d), key=lambda i: -m[i][i])
    return [m[i][i] for i in order], [[v[r][i] for i in order] for r in range(d)]


def whiten(xs: list[Vector]) -> tuple[list[Vector], Matrix, Vector]:
    """Return (components as rows, the whitening matrix V, the mean). Rows z_k have mean 0 and covariance I."""
    n, d = len(xs), len(xs[0])
    mean = [sum(x[j] for x in xs) / n for j in range(d)]
    xc = [[x[j] - mean[j] for j in range(d)] for x in xs]
    cov = [[sum(x[i] * x[j] for x in xc) / n for j in range(d)] for i in range(d)]
    lam, e = jacobi_eigh(cov)
    if lam[-1] <= 1e-12 * lam[0]:
        raise ValueError("the covariance is singular; reduce the dimension first")
    v = [[e[j][k] / math.sqrt(lam[k]) for j in range(d)] for k in range(d)]
    z = [[sum(v[k][j] * x[j] for j in range(d)) for x in xc] for k in range(d)]
    return z, v, mean


def kurtosis(y: Vector) -> float:
    """The fourth cumulant m4 - 3 m2^2 of the centred sample (excess kurtosis times m2^2)."""
    n = len(y)
    mu = sum(y) / n
    m2 = sum((v - mu) ** 2 for v in y) / n
    m4 = sum((v - mu) ** 4 for v in y) / n
    return m4 - 3.0 * m2 * m2


def contrast(rows: list[Vector]) -> float:
    """Comon's fourth-order contrast: the sum of squared kurtoses of the components."""
    return sum(kurtosis(r) ** 2 for r in rows)


BINOM4 = (1.0, 4.0, 6.0, 4.0, 1.0)


def _pair_kurtoses(mom: list[float], t: float) -> tuple[float, float]:
    """Kurtoses of c y_i + s y_j and -s y_i + c y_j for whitened y, from mom[a] = E[y_i^a y_j^(4-a)]."""
    c, s = math.cos(t), math.sin(t)
    k1 = sum(BINOM4[a] * c ** a * s ** (4 - a) * mom[a] for a in range(5)) - 3.0
    k2 = sum(BINOM4[a] * (-s) ** a * c ** (4 - a) * mom[a] for a in range(5)) - 3.0
    return k1, k2


def best_angle(yi: Vector, yj: Vector, grid: int = 720) -> tuple[float, float, float]:
    """Return (angle, pair contrast at the angle, pair contrast at 0) for one Jacobi step."""
    n = len(yi)
    mom = [sum(a ** p * b ** (4 - p) for a, b in zip(yi, yj)) / n for p in range(5)]

    def f(t: float) -> float:
        k1, k2 = _pair_kurtoses(mom, t)
        return k1 * k1 + k2 * k2

    h = (math.pi / 2) / grid
    f0 = f(0.0)
    best_t, best_f = 0.0, f0
    for g in range(1, grid):
        val = f(g * h)
        if val > best_f:
            best_t, best_f = g * h, val
    lo, hi = best_t - h, best_t + h  # golden section refinement inside the bracket
    phi = (math.sqrt(5.0) - 1.0) / 2.0
    a, b = hi - phi * (hi - lo), lo + phi * (hi - lo)
    fa, fb = f(a), f(b)
    for _ in range(40):
        if fa > fb:
            hi, b, fb = b, a, fa
            a = hi - phi * (hi - lo)
            fa = f(a)
        else:
            lo, a, fa = a, b, fb
            b = lo + phi * (hi - lo)
            fb = f(b)
    t_ref = (lo + hi) / 2
    if f(t_ref) > best_f:
        best_t, best_f = t_ref, f(t_ref)
    return best_t, best_f, f0


def ica_jacobi(xs: list[Vector], max_sweeps: int = 20, tol: float = 1e-10) -> tuple[Matrix, list[Vector], list[float]]:
    """Return (unmixing matrix B, estimated sources as rows, contrast after each rotation).

    The estimate of the source vector for an observation x is B (x - mean).
    """
    z, v, _ = whiten(xs)  # @line L1
    d = len(z)
    w = [[1.0 if i == j else 0.0 for j in range(d)] for i in range(d)]  # @line L2
    history = [contrast(z)]
    for _ in range(max_sweeps):  # @line L3
        gain = 0.0
        for i in range(d - 1):  # @line L4
            for j in range(i + 1, d):
                t, f_new, f_old = best_angle(z[i], z[j])  # @line L5
                if f_new <= f_old + tol:
                    continue
                gain += f_new - f_old
                c, s = math.cos(t), math.sin(t)
                z[i], z[j] = ([c * a + s * b for a, b in zip(z[i], z[j])],
                              [-s * a + c * b for a, b in zip(z[i], z[j])])  # @line L6
                w[i], w[j] = ([c * a + s * b for a, b in zip(w[i], w[j])],
                              [-s * a + c * b for a, b in zip(w[i], w[j])])
                history.append(contrast(z))
        if gain <= tol:  # @line L7
            break
    unmix = [[sum(w[i][k] * v[k][j] for k in range(d)) for j in range(d)] for i in range(d)]
    return unmix, z, history  # @line L8


def amari_index(p: Matrix) -> float:
    """Amari's performance index of P = B A, scaled to [0, 1]. It is 0 iff P is a scaled permutation."""
    m = len(p)
    a = [[abs(x) for x in row] for row in p]
    rows = sum(sum(row) / max(row) - 1.0 for row in a)
    cols = sum(sum(a[i][j] for i in range(m)) / max(a[i][j] for i in range(m)) - 1.0 for j in range(m))
    return (rows + cols) / (2.0 * m * (m - 1))
