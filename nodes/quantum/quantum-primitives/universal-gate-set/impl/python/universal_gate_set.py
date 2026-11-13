# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/universal-gate-set/. The authors are listed in prov/FYQ408.jsonl.
"""The constructive steps of universality, in the order of Nielsen and Chuang, Section 4.5.

1. two_level_decomposition: any d x d unitary is a product of at most d(d-1)/2 two-level unitaries.
2. zyz: any one-qubit unitary is e^(i alpha) Rz(beta) Ry(gamma) Rz(delta).
3. controlled_u: a controlled-U is CNOT gates and one-qubit gates (U = e^(i alpha) A X B X C, ABC = I).
4. TOFFOLI_CIRCUIT: the Toffoli gate exactly in H, T, T^dagger and CNOT.
5. ht_rotation_angle: T H T H is a rotation by an angle that is not a rational multiple of pi,
   so its powers are dense on a circle; this is the core of "H and T are dense in SU(2)".

Qubit order: qubit 0 is the least significant bit of a basis index (see qsim.py).
"""

import cmath
import math

from qsim import H, T, X, apply_1q, apply_cnot, dagger, matmul

Matrix = list[list[complex]]


def rz(beta: float) -> Matrix:
    return [[cmath.exp(-0.5j * beta), 0j], [0j, cmath.exp(0.5j * beta)]]


def ry(gamma: float) -> Matrix:
    c, s = math.cos(gamma / 2), math.sin(gamma / 2)
    return [[c + 0j, -s + 0j], [s + 0j, c + 0j]]


def zyz(u: Matrix) -> tuple[float, float, float, float]:
    """(alpha, beta, gamma, delta) with u = e^(i alpha) Rz(beta) Ry(gamma) Rz(delta)."""
    det = u[0][0] * u[1][1] - u[0][1] * u[1][0]
    alpha = cmath.phase(det) / 2
    ph = cmath.exp(-1j * alpha)
    a, b = ph * u[0][0], ph * u[1][0]  # the special unitary e^(-i alpha) u is [[a, -b*], [b, a*]]
    gamma = 2 * math.atan2(abs(b), abs(a))
    pa, pb = cmath.phase(a), cmath.phase(b)
    return alpha, pb - pa, gamma, -pa - pb


def controlled_u(state: list[complex], u: Matrix, control: int, target: int) -> list[complex]:
    """Controlled-U from two CNOT gates and one-qubit gates (Nielsen and Chuang, Corollary 4.2)."""
    alpha, beta, gamma, delta = zyz(u)
    a = matmul(rz(beta), ry(gamma / 2))
    b = matmul(ry(-gamma / 2), rz(-(delta + beta) / 2))
    c = rz((delta - beta) / 2)
    state = apply_1q(state, c, target)
    state = apply_cnot(state, control, target)
    state = apply_1q(state, b, target)
    state = apply_cnot(state, control, target)
    state = apply_1q(state, a, target)
    return apply_1q(state, [[1 + 0j, 0j], [0j, cmath.exp(1j * alpha)]], control)


def two_level_decomposition(u: Matrix) -> list[tuple[int, int, Matrix]]:
    """A list of (j, i, m), with j < i and m a 2 x 2 unitary acting on basis states j and i, whose
    product in list order is u. At most d(d-1)/2 factors."""
    d = len(u)
    w = [row[:] for row in u]
    factors: list[tuple[int, int, Matrix]] = []
    for j in range(d - 1):
        for i in range(j + 1, d):
            a, b = w[j][j], w[i][j]
            if abs(b) < 1e-15:
                continue
            r = math.sqrt(abs(a) ** 2 + abs(b) ** 2)
            g = [[a.conjugate() / r, b.conjugate() / r], [-b / r, a / r]]  # sends (a, b) to (r, 0)
            rj, ri = w[j], w[i]
            w[j] = [g[0][0] * x + g[0][1] * y for x, y in zip(rj, ri)]
            w[i] = [g[1][0] * x + g[1][1] * y for x, y in zip(rj, ri)]
            factors.append((j, i, dagger(g)))
        # now w[j][j] is real and positive, so it is 1, and the rest of row j is 0
        if abs(w[j][j] - 1) > 1e-9:  # only when the column was already (a, 0, ..., 0)
            ph = w[j][j]
            factors.append((j, j + 1, [[ph, 0j], [0j, 1 + 0j]]))
            w[j] = [x / ph for x in w[j]]
    ph = w[d - 1][d - 1]
    if abs(ph - 1) > 1e-12:
        if factors and factors[-1][:2] == (d - 2, d - 1):
            j, i, m = factors.pop()
            factors.append((j, i, matmul(m, [[1 + 0j, 0j], [0j, ph]])))
        else:
            factors.append((d - 2, d - 1, [[1 + 0j, 0j], [0j, ph]]))
    return factors


def embed(d: int, j: int, i: int, m: Matrix) -> Matrix:
    out = [[1 + 0j if r == c else 0j for c in range(d)] for r in range(d)]
    out[j][j], out[j][i], out[i][j], out[i][i] = m[0][0], m[0][1], m[1][0], m[1][1]
    return out


TDG = dagger(T)
# Toffoli with controls on qubits 2 and 1 and target qubit 0, in H, T, T^dagger and CNOT
# (6 CNOT, 7 T or T^dagger, 2 H; Nielsen and Chuang, Figure 4.9). Read left to right in time.
TOFFOLI_CIRCUIT = [("H", 0), ("CNOT", 1, 0), ("Tdg", 0), ("CNOT", 2, 0), ("T", 0), ("CNOT", 1, 0), ("Tdg", 0),
                   ("CNOT", 2, 0), ("T", 1), ("T", 0), ("H", 0), ("CNOT", 2, 1), ("T", 2), ("Tdg", 1),
                   ("CNOT", 2, 1)]
ONE_QUBIT = {"H": H, "T": T, "Tdg": TDG, "X": X}


def run_circuit(state: list[complex], circuit) -> list[complex]:
    for g in circuit:
        if g[0] == "CNOT":
            state = apply_cnot(state, g[1], g[2])
        else:
            state = apply_1q(state, ONE_QUBIT[g[0]], g[1])
    return state


def ht_rotation_angle() -> float:
    """The rotation angle theta of T H T H, from cos(theta/2) = |tr V| / 2 with V = U / sqrt(det U)."""
    u = matmul(matmul(T, H), matmul(T, H))
    det = u[0][0] * u[1][1] - u[0][1] * u[1][0]
    tr = (u[0][0] + u[1][1]) / cmath.sqrt(det)
    return 2 * math.acos(min(1.0, abs(tr) / 2))


def largest_gap(theta: float, k: int) -> float:
    """The largest gap between the points j theta mod 2 pi, j = 0..k, on the circle."""
    pts = sorted((j * theta) % (2 * math.pi) for j in range(k + 1))
    gaps = [b - a for a, b in zip(pts, pts[1:])] + [2 * math.pi - pts[-1] + pts[0]]
    return max(gaps)
