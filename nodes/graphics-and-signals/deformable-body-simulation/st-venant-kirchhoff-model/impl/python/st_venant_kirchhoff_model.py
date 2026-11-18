# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/st-venant-kirchhoff-model/. The authors are listed in prov/H0C71P.jsonl.
"""The St. Venant-Kirchhoff (StVK) hyperelastic model in 2D or 3D.

    E = (F^T F - I) / 2                       the Green strain
    Psi(F) = mu |E|_F^2 + (lambda / 2) tr(E)^2
    S = 2 mu E + lambda tr(E) I               the second Piola-Kirchhoff stress
    P = F S                                   the first Piola-Kirchhoff stress

The forces of a linear element with rest volume V0 are the columns of
-V0 P D_m^(-T) on the vertices 1 to d, and vertex 0 gets minus their sum.

For the deformation F = diag(s, 1, 1) (a bar that cannot shrink sideways),
Psi = (mu + lambda / 2) (s^2 - 1)^2 / 4 and P_xx = (2 mu + lambda) (s^3 - s) / 2.
"""

from anim import det, inv, mul, transpose


def lame(young, poisson):
    """Return (mu, lambda) from Young's modulus and Poisson's ratio."""
    mu = young / (2.0 * (1.0 + poisson))
    lam = young * poisson / ((1.0 + poisson) * (1.0 - 2.0 * poisson))
    return mu, lam


def green_strain(f):
    c = mul(transpose(f), f)
    d = len(f)
    return [[0.5 * (c[i][j] - (1.0 if i == j else 0.0)) for j in range(d)] for i in range(d)]


def energy_density(f, mu, lam):
    e = green_strain(f)
    tr = sum(e[i][i] for i in range(len(f)))
    return mu * sum(v * v for row in e for v in row) + 0.5 * lam * tr * tr


def pk2(f, mu, lam):
    e = green_strain(f)
    d = len(f)
    tr = sum(e[i][i] for i in range(d))
    return [[2.0 * mu * e[i][j] + (lam * tr if i == j else 0.0) for j in range(d)] for i in range(d)]


def pk1(f, mu, lam):
    return mul(f, pk2(f, mu, lam))


def edge_matrix(points):
    d = len(points) - 1
    return [[points[k + 1][i] - points[0][i] for k in range(d)] for i in range(d)]


def element_forces(rest, cur, mu, lam):
    """The forces on the d + 1 vertices of a linear triangle or tetrahedron."""
    dm = edge_matrix(rest)
    d = len(dm)
    fact = 2.0 if d == 2 else 6.0
    v0 = det(dm) / fact
    dm_inv = inv(dm)
    f = mul(edge_matrix(cur), dm_inv)
    h = mul(pk1(f, mu, lam), transpose(dm_inv))
    cols = [tuple(-v0 * h[i][k] for i in range(d)) for k in range(d)]
    first = tuple(-sum(c[i] for c in cols) for i in range(d))
    return [first] + cols


def element_energy(rest, cur, mu, lam):
    dm = edge_matrix(rest)
    fact = 2.0 if len(dm) == 2 else 6.0
    f = mul(edge_matrix(cur), inv(dm))
    return det(dm) / fact * energy_density(f, mu, lam)


def bar_stress(s, mu, lam):
    """P_xx for F = diag(s, 1, 1): (2 mu + lambda) (s^3 - s) / 2."""
    return 0.5 * (2.0 * mu + lam) * (s ** 3 - s)


def linearized_stress(h, mu, lam):
    """The small strain stress 2 mu sym(H) + lambda tr(H) I, the limit of P(I + H) at first order."""
    d = len(h)
    tr = sum(h[i][i] for i in range(d))
    return [[mu * (h[i][j] + h[j][i]) + (lam * tr if i == j else 0.0) for j in range(d)] for i in range(d)]
