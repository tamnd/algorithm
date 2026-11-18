# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/stable-neo-hookean/. The authors are listed in prov/F0PH35.jsonl.
"""The stable neo-Hookean energy of Smith, de Goes and Kim (2018), in 3D.

    I_C = tr(F^T F), J = det F
    Psi(F) = (mu / 2) (I_C - 3) + (lambda / 2) (J - alpha)^2 - (mu / 2) log(I_C + 1)
    alpha = 1 + 3 mu / (4 lambda)             (= 1 + mu / lambda - mu / (4 lambda))
    P(F) = mu (1 - 1 / (I_C + 1)) F + lambda (J - alpha) cof(F)

cof(F) is the cofactor matrix, with dJ/dF = cof(F) for every F, so Psi and P
are defined and smooth for all F, also for J <= 0. The model parameters
(mu, lambda) come from the Lame parameters (mu0, lambda0) of the linear limit
by mu = 4 mu0 / 3 and lambda = lambda0 + 5 mu0 / 6.
"""

import math

from anim import det, inv, mul, transpose


def lame(young, poisson):
    """Return the Lame parameters (mu0, lambda0) of Young's modulus and Poisson's ratio."""
    mu = young / (2.0 * (1.0 + poisson))
    lam = young * poisson / ((1.0 + poisson) * (1.0 - 2.0 * poisson))
    return mu, lam


def remap(mu0, lam0):
    """Return the model parameters (mu, lambda) whose linear limit has the Lame parameters mu0, lambda0."""
    return 4.0 * mu0 / 3.0, lam0 + 5.0 * mu0 / 6.0


def rest_alpha(mu, lam):
    return 1.0 + 0.75 * mu / lam


def cofactor(f):
    """The cofactor matrix of a 3 by 3 matrix: column k is the cross product of the other two columns."""
    c = [[0.0] * 3 for _ in range(3)]
    for i in range(3):
        for j in range(3):
            i1, i2 = (i + 1) % 3, (i + 2) % 3
            j1, j2 = (j + 1) % 3, (j + 2) % 3
            c[i][j] = f[i1][j1] * f[i2][j2] - f[i1][j2] * f[i2][j1]
    return c


def energy_density(f, mu, lam, alpha=None):
    if alpha is None:
        alpha = rest_alpha(mu, lam)
    ic = sum(v * v for row in f for v in row)
    j = det(f)
    return 0.5 * mu * (ic - 3.0) + 0.5 * lam * (j - alpha) ** 2 - 0.5 * mu * math.log(ic + 1.0)


def pk1(f, mu, lam, alpha=None):
    if alpha is None:
        alpha = rest_alpha(mu, lam)
    ic = sum(v * v for row in f for v in row)
    j = det(f)
    a = mu * (1.0 - 1.0 / (ic + 1.0))
    b = lam * (j - alpha)
    cof = cofactor(f)
    return [[a * f[i][k] + b * cof[i][k] for k in range(3)] for i in range(3)]


def edge_matrix(points):
    return [[points[k + 1][i] - points[0][i] for k in range(3)] for i in range(3)]


def element_forces(rest, cur, mu, lam):
    """The forces on the 4 vertices of a linear tetrahedron; valid also when it is flat or inverted."""
    dm = edge_matrix(rest)
    v0 = det(dm) / 6.0
    dm_inv = inv(dm)
    f = mul(edge_matrix(cur), dm_inv)
    h = mul(pk1(f, mu, lam), transpose(dm_inv))
    cols = [tuple(-v0 * h[i][k] for i in range(3)) for k in range(3)]
    first = tuple(-sum(c[i] for c in cols) for i in range(3))
    return [first] + cols


def element_energy(rest, cur, mu, lam):
    dm = edge_matrix(rest)
    f = mul(edge_matrix(cur), inv(dm))
    return det(dm) / 6.0 * energy_density(f, mu, lam)


def bar_stress(s, mu, lam):
    """P_xx = dPsi/ds for F = diag(s, 1, 1): mu s (s^2 + 2) / (s^2 + 3) + lambda (s - alpha)."""
    return mu * s * (s * s + 2.0) / (s * s + 3.0) + lam * (s - rest_alpha(mu, lam))


def effective_poisson(mu, lam):
    """The Poisson's ratio of the linear limit: (lambda - 5 mu / 8) / (2 (lambda + mu / 8))."""
    return (lam - 0.625 * mu) / (2.0 * (lam + 0.125 * mu))
