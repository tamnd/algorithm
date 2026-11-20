# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/interference-alignment/. The authors are listed in prov/BAD5BM.jsonl.

"""Interference alignment for the 3-user 2x2 MIMO interference channel.

Three transmitters and three receivers each have 2 antennas. h[k][j] is the
2x2 channel matrix from transmitter j to receiver k (users 0, 1, 2). Each
user sends one stream with the beam v[j]. Receiver k sees the two interfering
directions h[k][j] v[j], j != k, in its 2-dimensional space. If the two are
parallel, they fill only one dimension, and the receiver projects onto the
other dimension with u[k] to see its own stream free of interference. Then
all three users get one stream each, 3 streams in total in a space where
any one user alone could send 2.

The closed form of Cadambe and Jafar: with all channel matrices invertible,
    v[0] = an eigenvector of E = (h02 h12^-1 h10)^-1 (h01 h21^-1 h20),
    v[1] = h21^-1 h20 v[0],  v[2] = h12^-1 h10 v[0].
"""

import cmath
import math

from cbb import dot, inv, matmul, matvec


def _unit(x: list[complex]) -> list[complex]:
    n = math.sqrt(sum(abs(c) ** 2 for c in x))
    if n == 0.0:
        raise ValueError("zero vector")
    return [c / n for c in x]


def eigvec2(a: list[list[complex]], which: int = 0) -> tuple[complex, list[complex]]:
    """An eigenvalue and a unit eigenvector of a 2x2 matrix (which = 0 or 1 picks the root)."""
    tr = a[0][0] + a[1][1]
    dt = a[0][0] * a[1][1] - a[0][1] * a[1][0]
    root = cmath.sqrt(tr * tr - 4 * dt)
    lam = (tr + root) / 2 if which == 0 else (tr - root) / 2
    # (a - lam I) x = 0: use the row with the larger entries for a stable null vector
    r0 = [a[0][0] - lam, a[0][1]]
    r1 = [a[1][0], a[1][1] - lam]
    row = r0 if abs(r0[0]) + abs(r0[1]) >= abs(r1[0]) + abs(r1[1]) else r1
    if abs(row[0]) + abs(row[1]) == 0.0:
        return lam, [1 + 0j, 0j]
    return lam, _unit([-row[1], row[0]])


def orthogonal_unit(a: list[complex]) -> list[complex]:
    """A unit vector u in C^2 with u^H a = 0."""
    return _unit([-complex(a[1]).conjugate(), complex(a[0]).conjugate()])


def align_three_users(h: list[list[list[list[complex]]]], which: int = 0) -> tuple[list[list[complex]], list[list[complex]]]:
    """Beams v[k] and receive filters u[k] that align the interference of the 3-user 2x2 channel."""
    a = matmul(h[0][1], matmul(inv(h[2][1]), h[2][0]))  # @line L1
    b = matmul(h[0][2], matmul(inv(h[1][2]), h[1][0]))
    e = matmul(inv(b), a)
    _, v0 = eigvec2(e, which)  # @line L2
    v1 = _unit(matvec(inv(h[2][1]), matvec(h[2][0], v0)))  # @line L3
    v2 = _unit(matvec(inv(h[1][2]), matvec(h[1][0], v0)))  # @line L4
    v = [v0, v1, v2]
    u = []
    for k in range(3):  # @line L5
        j = (k + 1) % 3
        u.append(orthogonal_unit(matvec(h[k][j], v[j])))
    return v, u  # @line L6


def leakage(h, v, u) -> float:
    """Total interference power after the filters, sum over k and j != k of |u_k^H h_kj v_j|^2."""
    total = 0.0
    for k in range(3):
        for j in range(3):
            if j != k:
                total += abs(dot(u[k], matvec(h[k][j], v[j]))) ** 2
    return total


def desired_gains(h, v, u) -> list[float]:
    """The gains |u_k^H h_kk v_k|^2 of the wanted streams."""
    return [abs(dot(u[k], matvec(h[k][k], v[k]))) ** 2 for k in range(3)]


def parallel_defect(x: list[complex], y: list[complex]) -> float:
    """|det [x y]| / (|x| |y|): 0 exactly when the two vectors of C^2 are parallel."""
    nx = math.sqrt(sum(abs(c) ** 2 for c in x))
    ny = math.sqrt(sum(abs(c) ** 2 for c in y))
    return abs(x[0] * y[1] - x[1] * y[0]) / (nx * ny)


def sum_rate(h, v, u, snr: float) -> float:
    """Sum rate in bit/s/Hz with power snr per user, unit noise and the filters u (interference included)."""
    total = 0.0
    for k in range(3):
        s = snr * abs(dot(u[k], matvec(h[k][k], v[k]))) ** 2
        i = sum(snr * abs(dot(u[k], matvec(h[k][j], v[j]))) ** 2 for j in range(3) if j != k)
        total += math.log2(1.0 + s / (1.0 + i))
    return total
