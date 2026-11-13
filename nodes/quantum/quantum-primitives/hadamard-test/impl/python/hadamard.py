# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hadamard-test/. The authors are listed in prov/N1NJ1H.jsonl.
"""The Hadamard test: estimate Re <psi|U|psi> (or Im with an S^dagger gate) with one ancilla.

Layout: the state |psi> is on qubits 0 .. t-1 and the ancilla is qubit t (the high qubit).
Qubit 0 is the least significant bit (see qsim.py).
"""

import math

from qsim import H, SDG, apply_1q, apply_matrix, measure_qubit, prob_qubit


def hadamard_test_state(u, psi, imaginary: bool = False, extra: int = 0):
    """The state just before the measurement. u acts on qubits 0 .. k-1, where 2**k = len(u); psi may
    have extra qubits above them (extra = their number), which u does not touch. The ancilla is the
    highest qubit."""
    k = len(u).bit_length() - 1
    t = k + extra
    state = [a for a in psi] + [0j] * len(psi)  # @line L1
    state = apply_1q(state, H, t)  # @line L2
    if imaginary:
        state = apply_1q(state, SDG, t)  # @line L3
    state = apply_matrix(state, u, list(range(k)), [t])  # @line L4
    return apply_1q(state, H, t), t  # @line L5


def hadamard_test_exact(u, psi, imaginary: bool = False, extra: int = 0) -> float:
    """P(0) - P(1) of the ancilla, computed from the amplitudes."""
    state, t = hadamard_test_state(u, psi, imaginary, extra)
    return prob_qubit(state, t, 0) - prob_qubit(state, t, 1)


def hadamard_test_sampled(u, psi, shots: int, rng, imaginary: bool = False) -> float:
    """The estimate (n0 - n1) / shots from shots measurements of the ancilla."""
    state, t = hadamard_test_state(u, psi, imaginary)  # the same state is prepared for each shot
    total = 0
    for _ in range(shots):
        b, _post = measure_qubit(state, t, rng)  # @line L6
        total += 1 - 2 * b
    return total / shots


def hoeffding_radius(shots: int, delta: float) -> float:
    """With probability at least 1 - delta the estimate of P(0) - P(1) is within this distance.
    Each shot gives +1 or -1, a range of 2, so the radius is 2 sqrt(ln(2/delta) / (2 shots))."""
    return 2 * math.sqrt(math.log(2 / delta) / (2 * shots))


def shots_for(eps: float, delta: float) -> int:
    """The number of shots for which hoeffding_radius(shots, delta) <= eps."""
    return math.ceil(2 * math.log(2 / delta) / eps ** 2)


def expectation(u, psi) -> complex:
    """<psi|U|psi> when U acts on all qubits of psi: the exact reference."""
    upsi = [sum(u[r][c] * psi[c] for c in range(len(psi))) for r in range(len(psi))]
    return sum(complex(a).conjugate() * b for a, b in zip(psi, upsi))
