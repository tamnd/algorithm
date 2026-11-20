# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/first-order-reliability-method/. The authors are listed in prov/B2CCS2.jsonl.
"""First-order reliability method (FORM) by the HL-RF iteration, with Breitung's SORM correction.

The physical inputs X_1..X_d are independent with continuous marginal laws.
Each marginal is given by its inverse CDF, so x_k = F_k^(-1)(Phi(u_k)) maps a
standard normal vector u to X. Failure is g(x) <= 0. In the standard normal
space the limit state is G(u) = g(T(u)). The design point u* is the point of
G(u) = 0 closest to the origin, the reliability index is beta = +-||u*||
(positive when the origin is safe), and FORM gives P_f ~ Phi(-beta).
Gradients and the Hessian of G are central finite differences.
"""

import math
from statistics import NormalDist
from typing import Callable

Vector = list[float]
_STD = NormalDist()


def phi_cdf(t: float) -> float:
    """The standard normal CDF, by erfc, accurate in the far tail."""
    return 0.5 * math.erfc(-t / math.sqrt(2.0))


def normal_marginal(mean: float, sd: float) -> Callable[[float], float]:
    """x = mean + sd u: the map from u to a normal variable."""
    return lambda u: mean + sd * u


def lognormal_marginal(lam: float, zeta: float) -> Callable[[float], float]:
    """x = exp(lam + zeta u): the map from u to a lognormal variable with log-mean lam and log-sd zeta."""
    return lambda u: math.exp(lam + zeta * u)


def uniform_marginal(a: float, b: float) -> Callable[[float], float]:
    """x = a + (b - a) Phi(u): the map from u to a uniform variable on [a, b]."""
    return lambda u: a + (b - a) * phi_cdf(u)


def from_inverse_cdf(ppf: Callable[[float], float]) -> Callable[[float], float]:
    """The map u -> F^(-1)(Phi(u)) for a marginal given by its inverse CDF."""
    return lambda u: ppf(_STD.cdf(u))


def gradient(fun: Callable[[Vector], float], u: Vector, h: float = 1e-6) -> Vector:
    """Central difference gradient."""
    out = []
    for k in range(len(u)):
        up, dn = list(u), list(u)
        up[k] += h
        dn[k] -= h
        out.append((fun(up) - fun(dn)) / (2.0 * h))
    return out


def hessian(fun: Callable[[Vector], float], u: Vector, h: float = 1e-4) -> list[list[float]]:
    """Central difference Hessian."""
    d = len(u)
    hes = [[0.0] * d for _ in range(d)]
    for i in range(d):
        for j in range(i, d):
            vals = []
            for si, sj in ((1, 1), (1, -1), (-1, 1), (-1, -1)):
                v = list(u)
                v[i] += si * h
                v[j] += sj * h
                vals.append(fun(v))
            hes[i][j] = hes[j][i] = (vals[0] - vals[1] - vals[2] + vals[3]) / (4.0 * h * h)
    return hes


def det(a: list[list[float]]) -> float:
    """Determinant by Gaussian elimination with partial pivoting."""
    m = [list(r) for r in a]
    n = len(m)
    out = 1.0
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(m[r][c]))
        if m[p][c] == 0.0:
            return 0.0
        if p != c:
            m[c], m[p] = m[p], m[c]
            out = -out
        out *= m[c][c]
        for r in range(c + 1, n):
            f = m[r][c] / m[c][c]
            for k in range(c, n):
                m[r][k] -= f * m[c][k]
    return out


def form(g: Callable[[Vector], float], marginals: list[Callable[[float], float]], tol: float = 1e-8, max_iter: int = 100) -> dict:
    """HL-RF iteration for the design point; returns beta, the FORM P_f, u*, x*, alpha and the step count."""
    def big_g(u: Vector) -> float:
        return g([t(v) for t, v in zip(marginals, u)])

    d = len(marginals)
    u = [0.0] * d  # @line L1
    g0 = big_g(u)
    steps = 0
    for steps in range(1, max_iter + 1):  # @line L2
        val = big_g(u)
        grad = gradient(big_g, u)  # @line L3
        n2 = sum(t * t for t in grad)
        if n2 == 0.0:
            raise ValueError("zero gradient of the limit state")
        lam = (sum(a * b for a, b in zip(grad, u)) - val) / n2
        new = [lam * t for t in grad]  # @line L4
        done = math.sqrt(sum((a - b) ** 2 for a, b in zip(new, u))) <= tol * max(1.0, math.sqrt(sum(t * t for t in new)))
        u = new
        if done:  # @line L5
            break
    else:
        raise RuntimeError("HL-RF did not converge")
    grad = gradient(big_g, u)
    norm = math.sqrt(sum(t * t for t in grad))
    alpha = [-t / norm for t in grad]
    beta = math.copysign(math.sqrt(sum(t * t for t in u)), g0)  # @line L6
    return {"beta": beta, "pf": phi_cdf(-beta), "u": u, "x": [t(v) for t, v in zip(marginals, u)], "alpha": alpha, "steps": steps, "G": big_g}  # @line L7


def breitung(result: dict) -> float:
    """Breitung's SORM: P_f ~ Phi(-beta) / sqrt(det(I + beta K)), K the curvature matrix in the tangent plane."""
    u, alpha, beta, big_g = result["u"], result["alpha"], result["beta"], result["G"]
    d = len(u)
    if d == 1:
        return result["pf"]
    norm = math.sqrt(sum(t * t for t in gradient(big_g, u)))
    hes = hessian(big_g, u)
    basis: list[Vector] = []
    for k in range(d):  # an orthonormal basis of the plane orthogonal to alpha, by Gram-Schmidt
        v = [1.0 if i == k else 0.0 for i in range(d)]
        for w in [alpha] + basis:
            c = sum(a * b for a, b in zip(v, w))
            v = [a - c * b for a, b in zip(v, w)]
        n = math.sqrt(sum(t * t for t in v))
        if n > 1e-8 and len(basis) < d - 1:
            basis.append([t / n for t in v])
    curv = [[sum(basis[i][p] * hes[p][q] * basis[j][q] for p in range(d) for q in range(d)) / norm for j in range(d - 1)] for i in range(d - 1)]
    mat = [[(1.0 if i == j else 0.0) + beta * curv[i][j] for j in range(d - 1)] for i in range(d - 1)]
    dt = det(mat)
    if dt <= 0.0:
        raise ValueError("Breitung's formula needs 1 + beta kappa > 0 for every curvature")
    return phi_cdf(-beta) / math.sqrt(dt)
