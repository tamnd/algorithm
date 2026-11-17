# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lotka-volterra-competition/. The authors are listed in prov/8SQFG6.jsonl.
"""The two-species Lotka-Volterra competition model.

    dN1/dt = r1 N1 (1 - (N1 + a12 N2) / K1)
    dN2/dt = r2 N2 (1 - (N2 + a21 N1) / K2)

All parameters are positive. a12 is the effect of one individual of
species 2 on species 1, in units of individuals of species 1, and a21 is
the reverse. The module classifies the outcome from the parameters,
gives the equilibria and their Jacobians, and integrates the model with
fixed step RK4 so that the tests can compare the two.
"""

import math


def field(n1: float, n2: float, p):
    """The vector field for p = (r1, r2, K1, K2, a12, a21)."""
    r1, r2, k1, k2, a12, a21 = p
    return r1 * n1 * (1.0 - (n1 + a12 * n2) / k1), r2 * n2 * (1.0 - (n2 + a21 * n1) / k2)


def outcome(p) -> str:
    """'coexist', 'species 1', 'species 2', 'bistable' or 'degenerate' from the invasion tests."""
    _, _, k1, k2, a12, a21 = p
    inv1 = k1 - a12 * k2  # @line L1
    inv2 = k2 - a21 * k1  # @line L2
    if inv1 > 0 and inv2 > 0:  # @line L3
        return "coexist"
    if inv1 > 0 and inv2 < 0:  # @line L4
        return "species 1"
    if inv1 < 0 and inv2 > 0:  # @line L5
        return "species 2"
    if inv1 < 0 and inv2 < 0:  # @line L6
        return "bistable"
    return "degenerate"  # @line L7


def interior_equilibrium(p):
    """(N1*, N2*) = ((K1 - a12 K2), (K2 - a21 K1)) / (1 - a12 a21), or None if a12 a21 = 1."""
    _, _, k1, k2, a12, a21 = p
    den = 1.0 - a12 * a21
    if den == 0.0:
        return None
    return (k1 - a12 * k2) / den, (k2 - a21 * k1) / den


def jacobian(n1: float, n2: float, p):
    """The Jacobian matrix of the field at (n1, n2)."""
    r1, r2, k1, k2, a12, a21 = p
    return (
        (r1 * (1.0 - (2.0 * n1 + a12 * n2) / k1), -r1 * a12 * n1 / k1),
        (-r2 * a21 * n2 / k2, r2 * (1.0 - (2.0 * n2 + a21 * n1) / k2)),
    )


def eigenvalues(m):
    """The two eigenvalues of a real 2 by 2 matrix, as complex numbers."""
    (a, b), (c, d) = m
    tr, det = a + d, a * d - b * c
    disc = complex(tr * tr - 4.0 * det) ** 0.5
    return (tr + disc) / 2.0, (tr - disc) / 2.0


def rk4(n1: float, n2: float, dt: float, steps: int, p):
    """The state after `steps` RK4 steps of size dt."""
    for _ in range(steps):
        k1 = field(n1, n2, p)
        k2 = field(n1 + dt * k1[0] / 2, n2 + dt * k1[1] / 2, p)
        k3 = field(n1 + dt * k2[0] / 2, n2 + dt * k2[1] / 2, p)
        k4 = field(n1 + dt * k3[0], n2 + dt * k3[1], p)
        n1 += dt * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]) / 6
        n2 += dt * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1]) / 6
    return n1, n2


def lyapunov(n1: float, n2: float, p) -> float:
    """V = sum of w_i (N_i - N_i* ln N_i), w1 = a21 K1 / r1, w2 = a12 K2 / r2; it decreases when a12 a21 < 1."""
    r1, r2, k1, k2, a12, a21 = p
    e1, e2 = interior_equilibrium(p)
    w1, w2 = a21 * k1 / r1, a12 * k2 / r2
    return w1 * (n1 - e1 * math.log(n1)) + w2 * (n2 - e2 * math.log(n2))
