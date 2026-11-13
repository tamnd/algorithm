# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quantum-teleportation/. The authors are listed in prov/WR96G8.jsonl.

import random

from quantum_teleportation import BELL_PAIR, alice_circuit, teleport, teleport_branch
from qsim import H, X, Z, apply_1q, apply_cnot, inner, kron_vec, max_abs_diff, project_qubit, random_state, reduced_density

TOL = 1e-12


def fidelity(a, b):
    return abs(inner(a, b)) ** 2


def test_every_outcome_has_probability_one_quarter_and_restores_the_state() -> None:
    rng = random.Random(42)
    for _ in range(200):
        psi = random_state(1, rng)
        for m_z in (0, 1):
            for m_x in (0, 1):
                p, before, after = teleport_branch(psi, m_z, m_x)
                assert abs(p - 0.25) < TOL
                assert max_abs_diff(after, psi) < 1e-12
                # Before the correction Bob holds X^(m_x) Z^(m_z) psi.
                expected = psi
                if m_z:
                    expected = apply_1q(expected, Z, 0)
                if m_x:
                    expected = apply_1q(expected, X, 0)
                assert max_abs_diff(before, expected) < 1e-12


def test_basis_and_special_inputs() -> None:
    s = 2 ** -0.5
    for psi in ([1, 0], [0, 1], [s, s], [s, -s], [s, 1j * s], [0.6, 0.8j]):
        for m_z in (0, 1):
            for m_x in (0, 1):
                assert fidelity(teleport_branch(psi, m_z, m_x)[2], psi) > 1 - TOL


def test_bob_learns_nothing_before_the_two_bits_arrive() -> None:
    rng = random.Random(9)
    for _ in range(50):
        rho_bob = reduced_density(alice_circuit(random_state(1, rng)), 3, [0])
        assert max_abs_diff(rho_bob, [[0.5, 0], [0, 0.5]]) < TOL


def test_without_the_correction_the_average_fidelity_is_one_half() -> None:
    rng = random.Random(10)
    for _ in range(50):
        psi = random_state(1, rng)
        avg = sum(fidelity(teleport_branch(psi, z, x)[1], psi) for z in (0, 1) for x in (0, 1)) / 4
        assert abs(avg - 0.5) < TOL


def test_sampled_runs() -> None:
    rng = random.Random(2025)
    counts = {}
    runs = 2000
    for _ in range(runs):
        psi = random_state(1, rng)
        m_z, m_x, out = teleport(psi, rng)
        counts[(m_z, m_x)] = counts.get((m_z, m_x), 0) + 1
        assert fidelity(out, psi) > 1 - 1e-12
    # Hoeffding for each outcome: P(|rate - 1/4| >= 0.05) <= 2 exp(-2 * 2000 * 0.05^2) < 1e-4.
    assert len(counts) == 4 and all(abs(c / runs - 0.25) < 0.05 for c in counts.values())


def test_entanglement_swapping() -> None:
    # Qubit 3 is a reference entangled with qubit 2; teleporting qubit 2 to qubit 0
    # leaves qubits 3 and 0 in the Bell pair.
    s = kron_vec(BELL_PAIR, BELL_PAIR)
    s = apply_1q(apply_cnot(s, 2, 1), H, 2)
    for m_z in (0, 1):
        for m_x in (0, 1):
            p2, t = project_qubit(s, 2, m_z)
            p1, t = project_qubit(t, 1, m_x)
            assert abs(p2 * p1 - 0.25) < TOL
            if m_x:
                t = apply_1q(t, X, 0)
            if m_z:
                t = apply_1q(t, Z, 0)
            rho = reduced_density(t, 4, [3, 0])
            target = [[BELL_PAIR[i] * BELL_PAIR[j] for j in range(4)] for i in range(4)]
            assert max_abs_diff(rho, target) < TOL
