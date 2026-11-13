# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/phase-and-t-gates/. The authors are listed in prov/XQY3VF.jsonl.
"""The phase gates R(phi) = diag(1, e^(i phi)), S = R(pi/2) and T = R(pi/4), and the one-qubit Clifford group.

Qubit order: qubit j is bit j of the basis index.
"""

import cmath
import math

from qsim import apply_diagonal, matmul

Matrix = list[list[complex]]

R2 = math.sqrt(0.5)
H = [[complex(R2), complex(R2)], [complex(R2), complex(-R2)]]


def phase(phi: float) -> Matrix:
    """R(phi) = diag(1, e^(i phi))."""
    return [[1 + 0j, 0j], [0j, cmath.exp(1j * phi)]]


S = [[1 + 0j, 0j], [0j, 1j]]
T = [[1 + 0j, 0j], [0j, cmath.exp(1j * math.pi / 4)]]


def rz(theta: float) -> Matrix:
    """R_z(theta) = exp(-i theta Z / 2) = diag(e^(-i theta/2), e^(i theta/2))."""
    return [[cmath.exp(-0.5j * theta), 0j], [0j, cmath.exp(0.5j * theta)]]


def apply_phase(state: list[complex], phi: float, q: int) -> list[complex]:
    """R(phi) on qubit q: multiply the amplitude of |x> by e^(i phi) when bit q of x is 1."""
    w = cmath.exp(1j * phi)
    return apply_diagonal(state, [w if (x >> q) & 1 else 1 + 0j for x in range(len(state))])


def canonical(u: Matrix, digits: int = 9) -> tuple:
    """A key for u up to a global phase: divide by the phase of the first entry that is not zero, then round."""
    flat = [z for row in u for z in row]
    lead = next(z for z in flat if abs(z) > 1e-9)
    w = abs(lead) / lead
    return tuple((round((z * w).real, digits) + 0.0, round((z * w).imag, digits) + 0.0) for z in flat)


def generate_group(generators: list[Matrix], limit: int = 1000) -> dict:
    """All products of the generators, up to global phase, found by breadth-first search."""
    ident = [[1 + 0j, 0j], [0j, 1 + 0j]]
    seen = {canonical(ident): ident}
    frontier = [ident]
    while frontier:
        nxt = []
        for u in frontier:
            for g in generators:
                v = matmul(g, u)
                k = canonical(v)
                if k not in seen:
                    seen[k] = v
                    nxt.append(v)
                    if len(seen) > limit:
                        raise ValueError("the group is larger than the limit")
        frontier = nxt
    return seen


def rotation_angle(u: Matrix) -> float:
    """The Bloch-sphere rotation angle theta of a 2 x 2 unitary: |tr u| = 2 |cos(theta/2)|."""
    return 2 * math.acos(min(1.0, abs(u[0][0] + u[1][1]) / 2))
