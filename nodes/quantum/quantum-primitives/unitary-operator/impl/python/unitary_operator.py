# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/unitary-operator/. The authors are listed in prov/M3YVJN.jsonl.
"""Unitary matrices: tests, 2 x 2 eigenvalues, exponentials of Hermitian matrices, the ZYZ decomposition
and random unitaries.
"""

import cmath
import math
import random

from qsim import TOL, add, dagger, identity, inner, is_unitary, matmul, norm, scale

Matrix = list[list[complex]]

X = [[0j, 1 + 0j], [1 + 0j, 0j]]
Y = [[0j, -1j], [1j, 0j]]
Z = [[1 + 0j, 0j], [0j, -1 + 0j]]


def det_2x2(u: Matrix) -> complex:
    return u[0][0] * u[1][1] - u[0][1] * u[1][0]


def eigenvalues_2x2(u: Matrix) -> tuple[complex, complex]:
    """The roots of t^2 - tr(u) t + det(u)."""
    tr = u[0][0] + u[1][1]
    disc = cmath.sqrt(tr * tr - 4 * det_2x2(u))
    return (tr + disc) / 2, (tr - disc) / 2


def expm_taylor(a: Matrix, terms: int = 40) -> Matrix:
    """exp(a) = sum_k a^k / k!, truncated after the given number of terms."""
    d = len(a)
    out = identity(d)
    term = identity(d)
    for k in range(1, terms):
        term = scale(1 / k, matmul(term, a))
        out = add(out, term)
    return out


def exp_i_hermitian_2x2(h: Matrix) -> Matrix:
    """exp(i h) for a Hermitian 2 x 2 matrix h = c I + r (n . sigma): e^(i c) (cos r I + i sin r (n . sigma))."""
    if any(abs(h[i][j] - h[j][i].conjugate()) > TOL for i in range(2) for j in range(2)):
        raise ValueError("h must be Hermitian")
    c = ((h[0][0] + h[1][1]) / 2).real
    v = (h[1][0].real, h[1][0].imag, ((h[0][0] - h[1][1]) / 2).real)  # h = c I + vx X + vy Y + vz Z
    r = math.sqrt(sum(t * t for t in v))
    ns = add(add(scale(v[0], X), scale(v[1], Y)), scale(v[2], Z))
    s = math.sin(r) / r if r > 1e-15 else 1.0
    return scale(cmath.exp(1j * c), add(scale(math.cos(r), identity(2)), scale(1j * s, ns)))


def rz(t: float) -> Matrix:
    return [[cmath.exp(-0.5j * t), 0j], [0j, cmath.exp(0.5j * t)]]


def ry(t: float) -> Matrix:
    c, s = math.cos(t / 2), math.sin(t / 2)
    return [[complex(c), complex(-s)], [complex(s), complex(c)]]


def from_zyz(alpha: float, beta: float, gamma: float, delta: float) -> Matrix:
    """e^(i alpha) Rz(beta) Ry(gamma) Rz(delta)."""
    return scale(cmath.exp(1j * alpha), matmul(rz(beta), matmul(ry(gamma), rz(delta))))


def zyz(u: Matrix) -> tuple[float, float, float, float]:
    """(alpha, beta, gamma, delta) with u = e^(i alpha) Rz(beta) Ry(gamma) Rz(delta), for a 2 x 2 unitary u."""
    if not is_unitary(u):
        raise ValueError("u must be unitary")
    alpha = cmath.phase(det_2x2(u)) / 2
    v = scale(cmath.exp(-1j * alpha), u)  # det v = 1, v = [[a, -conj(b)], [b, conj(a)]]
    a, b = v[0][0], v[1][0]
    gamma = 2 * math.atan2(abs(b), abs(a))
    if abs(b) <= TOL:
        return alpha, -2 * cmath.phase(a), gamma, 0.0
    if abs(a) <= TOL:
        return alpha, 2 * cmath.phase(b), gamma, 0.0
    pa, pb = cmath.phase(a), cmath.phase(b)
    return alpha, pb - pa, gamma, -pa - pb


def random_unitary(d: int, rng: random.Random) -> Matrix:
    """Gram-Schmidt on d independent complex Gaussian columns, which gives a Haar-random unitary."""
    cols: list[list[complex]] = []
    while len(cols) < d:
        w = [complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(d)]
        for c in cols:
            ip = inner(c, w)
            w = [x - ip * y for x, y in zip(w, c)]
        r = norm(w)
        if r > 1e-8:
            cols.append([x / r for x in w])
    return [[cols[j][i] for j in range(d)] for i in range(d)]


def inverse(u: Matrix) -> Matrix:
    """The inverse of a unitary matrix is its conjugate transpose."""
    return dagger(u)
