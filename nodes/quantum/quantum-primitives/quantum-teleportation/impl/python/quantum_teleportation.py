# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quantum-teleportation/. The authors are listed in prov/WR96G8.jsonl.

"""Quantum teleportation of one qubit, on the state-vector simulator.

Qubit 2 holds the input state psi (Alice), qubit 1 is Alice's half of the Bell
pair and qubit 0 is Bob's half. The ket |q2 q1 q0> is the binary form of the
list index.
"""

from qsim import H, X, Z, apply_1q, apply_cnot, kron_vec, project_qubit

BELL_PAIR = [2 ** -0.5, 0, 0, 2 ** -0.5]  # (|00> + |11>)/sqrt(2) on qubits 1 and 0


def alice_circuit(psi):
    """Lines L1 to L3: share the pair, then CNOT from qubit 2 to qubit 1 and H on qubit 2."""
    s = kron_vec(psi, BELL_PAIR)  # @line L1
    s = apply_cnot(s, 2, 1)  # @line L2
    return apply_1q(s, H, 2)  # @line L3


def bob_qubit(state):
    """The state of qubit 0 when qubits 2 and 1 are in a basis state."""
    nz = [i for i, a in enumerate(state) if abs(a) > 1e-12]
    high = nz[0] >> 1
    return [state[(high << 1) | 0], state[(high << 1) | 1]]


def correct(bob, m_z, m_x):
    """Lines L6 and L7: apply X^(m_x), then Z^(m_z)."""
    if m_x:
        bob = apply_1q(bob, X, 0)  # @line L6
    if m_z:
        bob = apply_1q(bob, Z, 0)  # @line L7
    return bob


def teleport_branch(psi, m_z, m_x):
    """The branch with outcomes m_z (qubit 2) and m_x (qubit 1).

    Returns (probability of the branch, Bob's qubit before the correction,
    Bob's qubit after the correction).
    """
    s = alice_circuit(psi)
    p2, s = project_qubit(s, 2, m_z)
    p1, s = project_qubit(s, 1, m_x)
    before = bob_qubit(s)
    return p2 * p1, before, correct(before, m_z, m_x)


def teleport(psi, rng):
    """Run the protocol with random measurement outcomes. Returns (m_z, m_x, Bob's qubit)."""
    s = alice_circuit(psi)
    p1, post1 = project_qubit(s, 2, 1)  # @line L4
    m_z, s = (1, post1) if rng.random() < p1 else (0, project_qubit(s, 2, 0)[1])
    p1, post1 = project_qubit(s, 1, 1)  # @line L4
    m_x, s = (1, post1) if rng.random() < p1 else (0, project_qubit(s, 1, 0)[1])
    # @line L5: Alice sends the two bits (m_z, m_x) to Bob.
    return m_z, m_x, correct(bob_qubit(s), m_z, m_x)
