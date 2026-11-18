# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/neo-hookean-model/. The authors are listed in prov/DY1W7J.jsonl.
"""The compressible neo-Hookean model in the form of Bonet and Wood, in 2D or 3D.

    J = det F, I1 = tr(F^T F)
    Psi(F) = (mu / 2) (I1 - d) - mu log J + (lambda / 2) (log J)^2
    P(F) = mu (F - F^(-T)) + lambda log(J) F^(-T)

Psi and P are defined only for J > 0; for J <= 0 the functions raise
ValueError. The forces of a linear element with rest volume V0 are the
columns of -V0 P D_m^(-T) on the vertices 1 to d, and vertex 0 gets minus
their sum.
"""

import math

from anim import det, inv, mul, transpose


def lame(young, poisson):
    """Return (mu, lambda) from Young's modulus and Poisson's ratio."""
    mu = young / (2.0 * (1.0 + poisson))
    lam = young * poisson / ((1.0 + poisson) * (1.0 - 2.0 * poisson))
    return mu, lam


def _volume_ratio(f):
    j = det(f)
    if j <= 0.0:
        raise ValueError("the neo-Hookean energy is undefined for det F <= 0")
    return j


def energy_density(f, mu, lam):
    j = _volume_ratio(f)
    d = len(f)
    i1 = sum(v * v for row in f for v in row)
    lj = math.log(j)
    return 0.5 * mu * (i1 - d) - mu * lj + 0.5 * lam * lj * lj


def pk1(f, mu, lam):
    j = _volume_ratio(f)
    d = len(f)
    fit = transpose(inv(f))
    lj = math.log(j)
    return [[mu * (f[i][k] - fit[i][k]) + lam * lj * fit[i][k] for k in range(d)] for i in range(d)]


def edge_matrix(points):
    d = len(points) - 1
    return [[points[k + 1][i] - points[0][i] for k in range(d)] for i in range(d)]


def element_forces(rest, cur, mu, lam):
    """The forces on the d + 1 vertices of a linear triangle or tetrahedron."""
    dm = edge_matrix(rest)
    d = len(dm)
    v0 = det(dm) / (2.0 if d == 2 else 6.0)
    dm_inv = inv(dm)
    f = mul(edge_matrix(cur), dm_inv)
    h = mul(pk1(f, mu, lam), transpose(dm_inv))
    cols = [tuple(-v0 * h[i][k] for i in range(d)) for k in range(d)]
    first = tuple(-sum(c[i] for c in cols) for i in range(d))
    return [first] + cols


def element_energy(rest, cur, mu, lam):
    dm = edge_matrix(rest)
    f = mul(edge_matrix(cur), inv(dm))
    return det(dm) / (2.0 if len(dm) == 2 else 6.0) * energy_density(f, mu, lam)


def bar_energy(s, mu, lam):
    """Psi for F = diag(s, 1, 1) with s > 0."""
    return 0.5 * mu * (s * s - 1.0) - mu * math.log(s) + 0.5 * lam * math.log(s) ** 2


def bar_stress(s, mu, lam):
    """P_xx for F = diag(s, 1, 1) with s > 0: mu (s - 1/s) + lambda log(s) / s."""
    return mu * (s - 1.0 / s) + lam * math.log(s) / s
