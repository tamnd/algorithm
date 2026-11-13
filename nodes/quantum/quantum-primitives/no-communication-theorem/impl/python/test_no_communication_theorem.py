# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/no-communication-theorem/. The authors are listed in prov/AMHNNQ.jsonl.

import math
import random

from no_communication_theorem import (
    apply_local_channel,
    bob_frequency_of_one,
    is_trace_preserving,
    reduced_a,
    selective_branches,
)
from qsim import X, apply_cnot, identity, kron_mat, matmul, matrix_of, max_abs_diff, outer, random_state, random_unitary_1q

TOL = 1e-12
N, K = 3, 2  # A is qubit 2, B is qubits 1 and 0


def random_two_qubit_unitary(rng):
    cnot = matrix_of(2, lambda s: apply_cnot(s, 1, 0))
    U = kron_mat(random_unitary_1q(rng), random_unitary_1q(rng))
    return matmul(matmul(kron_mat(random_unitary_1q(rng), random_unitary_1q(rng)), cnot), U)


def random_projective_measurement(rng):
    U = random_two_qubit_unitary(rng)
    return [outer([U[i][j] for i in range(4)], [U[i][j] for i in range(4)]) for j in range(4)]


def amplitude_damping_on_qubit0(g):
    k0 = [[1, 0], [0, math.sqrt(1 - g)]]
    k1 = [[0, math.sqrt(g)], [0, 0]]
    return [kron_mat(identity(2), k0), kron_mat(identity(2), k1)]


def test_local_operations_on_b_leave_rho_a_unchanged() -> None:
    rng = random.Random(31)
    for _ in range(30):
        psi = random_state(N, rng)
        rho = outer(psi, psi)
        rho_a = reduced_a(rho, N, K)
        for kraus in ([random_two_qubit_unitary(rng)], random_projective_measurement(rng), amplitude_damping_on_qubit0(rng.random())):
            assert is_trace_preserving(kraus)
            assert max_abs_diff(reduced_a(apply_local_channel(rho, N, K, kraus), N, K), rho_a) < TOL


def test_conditional_states_change_but_their_average_does_not() -> None:
    rng = random.Random(32)
    psi = random_state(N, rng)
    rho = outer(psi, psi)
    rho_a = reduced_a(rho, N, K)
    branches = selective_branches(rho, N, K, random_projective_measurement(rng))
    assert abs(sum(p for p, _ in branches) - 1) < TOL
    assert max(max_abs_diff(r, rho_a) for _, r in branches) > 1e-3
    avg = [[sum(p * r[i][j] for p, r in branches) for j in range(2)] for i in range(2)]
    assert max_abs_diff(avg, rho_a) < TOL


def test_an_operation_across_the_cut_does_change_rho_a() -> None:
    psi = [0] * 8
    psi[0b001] = 1  # |0>_A |01>_B
    rho = outer(psi, psi)
    cnot_b_to_a = matrix_of(3, lambda s: apply_cnot(s, 0, 2))
    after = matmul(matmul(cnot_b_to_a, rho), cnot_b_to_a)
    assert max_abs_diff(reduced_a(after, N, K), [[0, 0], [0, 1]]) < TOL


def test_bob_statistics_do_not_depend_on_alice_basis() -> None:
    rounds = 20000
    # Hoeffding: P(|rate - 1/2| >= 0.015) <= 2 exp(-2 * 20000 * 0.015^2) < 3e-4 for each basis.
    for basis, seed in ((0, 100), (1, 101)):
        assert abs(bob_frequency_of_one(basis, rounds, random.Random(seed)) - 0.5) < 0.015


def test_trace_preservation_check() -> None:
    assert not is_trace_preserving([[[1, 0], [0, 0]]])
    assert is_trace_preserving([X])
