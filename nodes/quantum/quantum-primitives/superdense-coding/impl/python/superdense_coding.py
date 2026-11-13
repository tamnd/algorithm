# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/superdense-coding/. The authors are listed in prov/4E2Q6C.jsonl.

"""Superdense coding of two classical bits in one qubit, on the state-vector simulator.

Qubit 1 is Alice's half of the Bell pair and qubit 0 is Bob's half. The ket
|q1 q0> is the binary form of the list index.
"""

from qsim import H, X, Z, apply_1q, apply_cnot, probabilities, project_qubit

BELL_PAIR = [2 ** -0.5, 0, 0, 2 ** -0.5]  # (|00> + |11>)/sqrt(2)


def encode(x, y):
    """Lines L2 and L3: Alice applies X^y, then Z^x, to her half (qubit 1)."""
    s = list(BELL_PAIR)  # @line L1
    if y:
        s = apply_1q(s, X, 1)  # @line L2
    if x:
        s = apply_1q(s, Z, 1)  # @line L3
    return s


def decode_circuit(state):
    """Lines L5 and L6: Bob applies CNOT from qubit 1 to qubit 0, then H on qubit 1."""
    s = apply_cnot(state, 1, 0)  # @line L5
    return apply_1q(s, H, 1)  # @line L6


def decode_probabilities(x, y):
    """The exact distribution of Bob's two outcome bits (x', y') for the message (x, y)."""
    p = probabilities(decode_circuit(encode(x, y)))
    return {(i >> 1, i & 1): p[i] for i in range(4)}


def send(x, y, rng):
    """Run the protocol once and return Bob's decoded pair (x', y')."""
    s = decode_circuit(encode(x, y))  # @line L4: Alice sends qubit 1 to Bob.
    p1, post1 = project_qubit(s, 1, 1)  # @line L7
    bx, s = (1, post1) if rng.random() < p1 else (0, project_qubit(s, 1, 0)[1])
    p1, _ = project_qubit(s, 0, 1)  # @line L7
    by = 1 if rng.random() < p1 else 0
    return bx, by
