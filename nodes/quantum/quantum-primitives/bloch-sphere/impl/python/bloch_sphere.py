# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bloch-sphere/. The authors are listed in prov/R8N0ZK.jsonl.
"""The Bloch sphere: one-qubit states as points of the unit ball in R^3.

A pure state a|0> + b|1> is cos(theta/2)|0> + e^(i phi) sin(theta/2)|1> up to a global phase,
and its Bloch vector is (sin theta cos phi, sin theta sin phi, cos theta).
"""

import cmath
import math

from qsim import TOL, add, dagger, identity, matmul, scale

Vector = list[complex]
Matrix = list[list[complex]]

X = [[0j, 1 + 0j], [1 + 0j, 0j]]
Y = [[0j, -1j], [1j, 0j]]
Z = [[1 + 0j, 0j], [0j, -1 + 0j]]
PAULIS = (X, Y, Z)


def state_from_angles(theta: float, phi: float) -> Vector:
    return [complex(math.cos(theta / 2)), cmath.exp(1j * phi) * math.sin(theta / 2)]


def angles(state: Vector) -> tuple[float, float]:
    """(theta, phi) with 0 <= theta <= pi and 0 <= phi < 2 pi. phi is 0 at the poles, where it has no meaning."""
    a, b = state
    theta = 2 * math.atan2(abs(b), abs(a))
    if abs(a) <= TOL or abs(b) <= TOL:
        return theta, 0.0
    phi = (cmath.phase(b) - cmath.phase(a)) % (2 * math.pi)
    return theta, phi


def bloch_vector(state: Vector) -> tuple[float, float, float]:
    """(2 Re(conj(a) b), 2 Im(conj(a) b), |a|^2 - |b|^2) for the unit vector a|0> + b|1>."""
    a, b = state
    c = a.conjugate() * b
    return 2 * c.real, 2 * c.imag, abs(a) ** 2 - abs(b) ** 2


def density(state: Vector) -> Matrix:
    """|psi><psi|."""
    return [[x * y.conjugate() for y in state] for x in state]


def density_from_vector(r: tuple[float, float, float]) -> Matrix:
    """rho = (I + x X + y Y + z Z) / 2. It is a density matrix exactly when |r| <= 1."""
    m = identity(2)
    for c, p in zip(r, PAULIS):
        m = add(m, scale(c, p))
    return scale(0.5, m)


def vector_of_density(rho: Matrix) -> tuple[float, float, float]:
    """(tr(rho X), tr(rho Y), tr(rho Z)) = (2 Re rho10, 2 Im rho10, rho00 - rho11)."""
    return 2 * rho[1][0].real, 2 * rho[1][0].imag, (rho[0][0] - rho[1][1]).real


def length(r: tuple[float, float, float]) -> float:
    return math.sqrt(sum(c * c for c in r))


def rotation(axis: tuple[float, float, float], alpha: float) -> Matrix:
    """exp(-i alpha (n . sigma) / 2) = cos(alpha/2) I - i sin(alpha/2) (n . sigma), for a unit axis n."""
    if abs(length(axis) - 1) > TOL:
        raise ValueError("the axis must be a unit vector")
    ns = [[0j, 0j], [0j, 0j]]
    for c, p in zip(axis, PAULIS):
        ns = add(ns, scale(c, p))
    return add(scale(math.cos(alpha / 2), identity(2)), scale(-1j * math.sin(alpha / 2), ns))


def so3(u: Matrix) -> list[list[float]]:
    """The 3 x 3 rotation R with R[i][j] = tr(sigma_i U sigma_j U^dagger) / 2. It maps the Bloch vector of psi to that of U psi."""
    ud = dagger(u)
    out = []
    for si in PAULIS:
        row = []
        for sj in PAULIS:
            m = matmul(si, matmul(u, matmul(sj, ud)))
            row.append(((m[0][0] + m[1][1]) / 2).real)
        out.append(row)
    return out


def apply_rotation(r: list[list[float]], v: tuple[float, float, float]) -> tuple[float, float, float]:
    return tuple(sum(r[i][j] * v[j] for j in range(3)) for i in range(3))
