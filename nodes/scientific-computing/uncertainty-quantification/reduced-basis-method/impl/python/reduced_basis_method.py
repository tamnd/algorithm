# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/reduced-basis-method/. The authors are listed in prov/YM1D2Z.jsonl.
"""Reduced basis method with an offline-online split and a residual based error bound.

The model problem is -u'' + mu u = 1 on (0, 1) with u(0) = u(1) = 0, in P1 finite elements on a
uniform mesh. Its matrix is affine in the parameter: A(mu) = theta_1 K + theta_2 M with theta = (1, mu).
"""

import math

from scimat import matmul, matvec, solve, transpose

Matrix = list[list[float]]
Vector = list[float]


def fe_model(n: int) -> tuple[list[Matrix], Vector]:
    """Return ([K, M], F) for P1 elements with n interior nodes and h = 1/(n+1)."""
    h = 1.0 / (n + 1)
    k = [[0.0] * n for _ in range(n)]
    m = [[0.0] * n for _ in range(n)]
    for i in range(n):
        k[i][i] = 2.0 / h
        m[i][i] = 4.0 * h / 6.0
        if i > 0:
            k[i][i - 1] = k[i - 1][i] = -1.0 / h
            m[i][i - 1] = m[i - 1][i] = h / 6.0
    return [k, m], [h] * n


def theta(mu: float) -> Vector:
    """Return the affine coefficients (1, mu) of A(mu) = K + mu M."""
    return [1.0, mu]


def assemble(aq: list[Matrix], mu: float) -> Matrix:
    """Return A(mu) = sum over q of theta_q(mu) A_q."""
    th = theta(mu)
    n = len(aq[0])
    return [[sum(th[q] * aq[q][i][j] for q in range(len(aq))) for j in range(n)] for i in range(n)]


def truth_solve(aq: list[Matrix], f: Vector, mu: float) -> Vector:
    """Return the finite element solution u(mu) of A(mu) u = F."""
    return solve(assemble(aq, mu), f)


def x_dot(x: Matrix, u: Vector, v: Vector) -> float:
    """Return the X inner product u^T X v."""
    return sum(ui * xv for ui, xv in zip(u, matvec(x, v)))


def alpha_lb(mu: float, mu_bar: float) -> float:
    """Return the min-theta lower bound min(1, mu / mu_bar) of the coercivity constant in the norm of X = K + mu_bar M."""
    return min(1.0, mu / mu_bar)


def offline(aq: list[Matrix], f: Vector, x: Matrix, samples: list[float]) -> dict:
    """Build the reduced basis from the snapshots at the sample parameters and all mu independent quantities."""
    snaps = [truth_solve(aq, f, mu) for mu in samples]  # @line L1: snapshots u(mu_1), ..., u(mu_r)
    z: list[Vector] = []
    for u in snaps:  # @line L2: Gram-Schmidt in the X inner product, two passes
        w = list(u)
        for _ in range(2):
            for zj in z:
                c = x_dot(x, zj, w)
                w = [wi - c * zi for wi, zi in zip(w, zj)]
        nw = math.sqrt(x_dot(x, w, w))
        if nw <= 1e-10 * math.sqrt(x_dot(x, u, u)):
            raise ValueError("the snapshots are linearly dependent")
        z.append([wi / nw for wi in w])
    zt = z  # rows of zt are the basis vectors
    zm = transpose(zt)  # n by r
    aqr = [matmul(zt, matmul(a, zm)) for a in aq]  # @line L3: A_q^r = Z^T A_q Z and F_r = Z^T F
    fr = matvec(zt, f)
    # @line L4: Riesz representers X^-1 F and X^-1 A_q z_j, and their Gram quantities
    aqz = [transpose(matmul(a, zm)) for a in aq]  # aqz[q][j] = A_q z_j
    rhs = [f] + [v for q in range(len(aq)) for v in aqz[q]]
    reps = transpose(solve(x, transpose(rhs)))
    ef, eq = reps[0], reps[1:]
    r = len(z)
    gff = sum(a * b for a, b in zip(f, ef))
    gf = [[sum(a * b for a, b in zip(f, eq[q * r + j])) for j in range(r)] for q in range(len(aq))]
    gqq = [[[[sum(a * b for a, b in zip(aqz[q][i], eq[p * r + j])) for j in range(r)] for i in range(r)] for p in range(len(aq))] for q in range(len(aq))]
    return {"Z": zm, "Aqr": aqr, "Fr": fr, "gff": gff, "gf": gf, "gqq": gqq}


def online(rb: dict, mu: float, mu_bar: float) -> tuple[Vector, float, float, float]:
    """Return (u_r, Delta, s_r, Delta_s) at mu, at a cost independent of n except for lifting u_r = Z c."""
    th = theta(mu)
    qn = len(th)
    r = len(rb["Fr"])
    ar = [[sum(th[q] * rb["Aqr"][q][i][j] for q in range(qn)) for j in range(r)] for i in range(r)]
    c = solve(ar, rb["Fr"])  # @line L5: solve A_r(mu) c = F_r
    res2 = rb["gff"]  # @line L6: the dual norm of the residual, squared
    for q in range(qn):
        res2 -= 2.0 * th[q] * sum(c[j] * rb["gf"][q][j] for j in range(r))
        for p in range(qn):
            g = rb["gqq"][q][p]
            res2 += th[q] * th[p] * sum(c[i] * g[i][j] * c[j] for i in range(r) for j in range(r))
    res = math.sqrt(max(res2, 0.0))
    a = alpha_lb(mu, mu_bar)
    delta = res / a  # @line L7
    s_r = sum(fi * ci for fi, ci in zip(rb["Fr"], c))
    return matvec(rb["Z"], c), delta, s_r, res * res / a  # @line L8
