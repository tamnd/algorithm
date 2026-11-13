# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/phase-kickback/. The authors are listed in prov/2ZD3YZ.jsonl.

import cmath
import math
import random

from phase_kickback import (
    bit_oracle_matrix,
    cnot_on,
    control_after_kickback,
    deutsch,
    eigen_2x2,
    kickback,
    kron_vec,
    readout_one_bit,
)
from qsim import (
    S,
    T,
    TOL,
    X,
    Z,
    apply_matrix,
    matmul,
    purity,
    random_unitary_2x2,
    reduced_density_matrix,
)

S2 = 1 / math.sqrt(2)
PLUS, MINUS = [S2, S2], [S2, -S2]


def close(u, v) -> bool:
    return max(abs(a - b) for a, b in zip(u, v)) <= TOL


def test_bit_oracle_kickback_on_every_basis_state() -> None:
    """U_f |x>|-> = (-1)^f(x) |x>|-> for the four functions on one bit and both x."""
    for f in ([0, 0], [0, 1], [1, 0], [1, 1]):
        for x in range(2):
            ket_x = [1 - x, x]
            out = apply_matrix(kron_vec(ket_x, MINUS), bit_oracle_matrix(f), [0, 1])
            assert close(out, [(-1) ** f[x] * a for a in kron_vec(ket_x, MINUS)])


def test_cnot_kicks_back_onto_the_control() -> None:
    """CNOT |+>|-> = |->|->, CNOT |->|-> = |+>|->, and CNOT |+>|+> = |+>|+>."""
    assert close(cnot_on(PLUS, MINUS), kron_vec(MINUS, MINUS))
    assert close(cnot_on(MINUS, MINUS), kron_vec(PLUS, MINUS))
    assert close(cnot_on(PLUS, PLUS), kron_vec(PLUS, PLUS))


def test_eigenvalue_kickback_is_exact() -> None:
    """For fixed gates and random unitaries (seed 8), each eigenvector and a random control state."""
    rng = random.Random(8)
    gates = [X, Z, S, T] + [random_unitary_2x2(rng) for _ in range(20)]
    for u in gates:
        for lam, v in eigen_2x2(u):
            assert abs(abs(lam) - 1) <= TOL
            uv = [u[0][0] * v[0] + u[0][1] * v[1], u[1][0] * v[0] + u[1][1] * v[1]]
            assert close(uv, [lam * a for a in v])
            a = complex(rng.gauss(0, 1), rng.gauss(0, 1))
            b = complex(rng.gauss(0, 1), rng.gauss(0, 1))
            s = math.sqrt(abs(a) ** 2 + abs(b) ** 2)
            control = [a / s, b / s]
            out = kickback(u, v, control)
            assert close(out, control_after_kickback(u, v, control, lam))
            assert abs(purity(reduced_density_matrix(out, [1])) - 1) <= TOL  # control not entangled


def test_two_qubit_target() -> None:
    """Controlled-(X x Z) on the eigenvector |-> (x) |1>, eigenvalue (-1)(-1) = 1, and on |-> (x) |0>,
    eigenvalue -1."""
    xz = [[X[i // 2][j // 2] * Z[i % 2][j % 2] for j in range(4)] for i in range(4)]
    for low, lam in (([0, 1], 1), ([1, 0], -1)):
        target = kron_vec(MINUS, low)
        out = kickback(xz, target, PLUS)
        assert close(out, kron_vec([S2, lam * S2], target))
        assert abs(readout_one_bit(out, 2) - (0 if lam == 1 else 1)) <= TOL


def test_readout_of_the_phase() -> None:
    """After H the control reads 1 with probability sin^2(phi/2) for the eigenvalue e^(i phi)."""
    for k in range(16):
        phi = 2 * math.pi * k / 16
        u = [[1, 0], [0, cmath.exp(1j * phi)]]
        out = kickback(u, [0, 1], PLUS)
        assert abs(readout_one_bit(out, 1) - math.sin(phi / 2) ** 2) <= TOL


def test_deutsch_with_one_query() -> None:
    for f in ([0, 0], [0, 1], [1, 0], [1, 1]):
        assert deutsch(f) == f[0] ^ f[1]


def test_target_that_is_not_an_eigenvector_gets_entangled() -> None:
    """CNOT on |+>|0> makes a Bell state: no phase is kicked back, the control becomes mixed."""
    out = cnot_on(PLUS, [1, 0])
    assert close(out, [S2, 0, 0, S2])
    assert abs(purity(reduced_density_matrix(out, [1])) - 0.5) <= TOL


def test_phase_of_u_squared() -> None:
    """Controlled-U^2 kicks back the square of the eigenvalue; this is the step that phase estimation
    repeats with U, U^2, U^4, ..."""
    rng = random.Random(9)
    u = random_unitary_2x2(rng)
    u2 = matmul(u, u)
    for lam, v in eigen_2x2(u):
        out = kickback(u2, v, PLUS)
        assert close(out, kron_vec([S2, lam * lam * S2], v))
