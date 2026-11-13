# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/swap-test/. The authors are listed in prov/P7XCAZ.jsonl.
"""The swap test on a state-vector simulator, and the overlap estimate from many runs.

Qubit layout for two n-qubit states (qubit 0 is the least significant bit,
see qsim.py): register A is qubits 0 .. n-1 and holds psi, register B is
qubits n .. 2n-1 and holds phi, and the ancilla c is qubit 2n. So the full
state is |c> tensor |phi> tensor |psi>, with basis index c * 4^n + b * 2^n + a.
"""

import math
import random
from typing import Callable, Sequence, Tuple

from qsim import H, Matrix, Vector, apply_1q, apply_permutation, apply_to_density
from qsim import kron, kron_vec, measure_qubit, prob_qubit_zero


def cnot(control: int, target: int) -> Callable[[int], int]:
    """The basis permutation of a CNOT gate."""
    c, t = 1 << control, 1 << target
    return lambda i: i ^ t if i & c else i


def controlled_swap(state: Vector, control: int, q1: int, q2: int) -> Vector:
    """The Fredkin gate: swap qubits q1 and q2 when the control qubit is 1."""
    c, b1, b2 = 1 << control, 1 << q1, 1 << q2

    def perm(i: int) -> int:
        if i & c and bool(i & b1) != bool(i & b2):
            return i ^ b1 ^ b2
        return i

    return apply_permutation(state, perm)


def circuit(state: Vector, n: int) -> Vector:
    """Lines L2 to L4: H on the ancilla, n controlled swaps, H on the ancilla."""
    c = 2 * n
    state = apply_1q(state, H, c)  # @line L2
    for j in range(n):  # @line L3
        state = controlled_swap(state, c, j, n + j)
    return apply_1q(state, H, c)  # @line L4


def num_qubits(psi: Sequence[complex]) -> int:
    n = len(psi).bit_length() - 1
    if len(psi) != 1 << n:
        raise ValueError("the length of a state must be a power of 2")
    return n


def swap_test(psi: Sequence[complex], phi: Sequence[complex], rng: random.Random) -> int:
    """One run of the swap test on fresh copies of psi and phi. Returns the ancilla outcome 0 or 1."""
    n = num_qubits(psi)
    if len(phi) != len(psi):
        raise ValueError("the two states must have the same number of qubits")
    state = kron_vec([1, 0], kron_vec(phi, psi))  # @line L1
    state = circuit(state, n)
    outcome, _ = measure_qubit(state, 2 * n, rng)  # @line L5
    return outcome


def final_state(psi: Sequence[complex], phi: Sequence[complex]) -> Vector:
    """The state of all 2n + 1 qubits just before the measurement."""
    return circuit(kron_vec([1, 0], kron_vec(phi, psi)), num_qubits(psi))


def probability_zero(psi: Sequence[complex], phi: Sequence[complex]) -> float:
    """The exact probability that the ancilla reads 0. It equals (1 + |<psi|phi>|^2) / 2."""
    return prob_qubit_zero(final_state(psi, phi), 2 * num_qubits(psi))


def probability_zero_mixed(rho: Matrix, sigma: Matrix) -> float:
    """The probability of outcome 0 for density matrices rho (register A) and sigma (register B).

    It equals (1 + Tr(rho sigma)) / 2.
    """
    d = len(rho)
    n = d.bit_length() - 1
    start = kron([[1, 0], [0, 0]], kron(sigma, rho))
    out = apply_to_density(start, lambda v: circuit(v, n))
    return sum(out[i][i].real for i in range(d * d))  # ancilla 0 is the first half of the indices


def runs_needed(eps: float, delta: float) -> int:
    """Runs so that the estimate 2 k / N - 1 is within eps of the overlap with probability >= 1 - delta.

    Hoeffding: P(|k/N - p| >= eps/2) <= 2 exp(-2 N (eps/2)^2) = 2 exp(-N eps^2 / 2).
    """
    return math.ceil(2 * math.log(2 / delta) / (eps * eps))


def estimate_overlap(
    psi: Sequence[complex], phi: Sequence[complex], eps: float, delta: float, rng: random.Random
) -> Tuple[float, int]:
    """Estimate |<psi|phi>|^2 to within eps with probability at least 1 - delta.

    Returns the estimate and the number of runs, each of which uses one copy of psi and one of phi.
    """
    runs = runs_needed(eps, delta)  # @line L6
    zeros = sum(1 for _ in range(runs) if swap_test(psi, phi, rng) == 0)  # @line L7
    return max(0.0, 2 * zeros / runs - 1), runs  # @line L8


# ---------------------------------------------------------------- the variant without an ancilla


def destructive_swap_test(psi: Sequence[complex], phi: Sequence[complex], rng: random.Random) -> int:
    """Measure each pair (A_j, B_j) in the Bell basis: CNOT from A_j to B_j, then H on A_j.

    A pair is in the singlet exactly when both bits are 1. The result is the parity
    of the number of singlet pairs; it is 0 with probability (1 + |<psi|phi>|^2) / 2.
    """
    n = num_qubits(psi)
    bits = sample_basis(bell_rotated(psi, phi), rng)
    return singlet_parity(bits, n)


def bell_rotated(psi: Sequence[complex], phi: Sequence[complex]) -> Vector:
    n = num_qubits(psi)
    state = kron_vec(phi, psi)
    for j in range(n):
        state = apply_permutation(state, cnot(j, n + j))
        state = apply_1q(state, H, j)
    return state


def singlet_parity(bits: int, n: int) -> int:
    return sum((bits >> j) & (bits >> (n + j)) & 1 for j in range(n)) % 2


def destructive_probability_zero(psi: Sequence[complex], phi: Sequence[complex]) -> float:
    n = num_qubits(psi)
    return sum(abs(x) ** 2 for i, x in enumerate(bell_rotated(psi, phi)) if singlet_parity(i, n) == 0)


def sample_basis(state: Sequence[complex], rng: random.Random) -> int:
    return rng.choices(range(len(state)), weights=[abs(x) ** 2 for x in state], k=1)[0]


def overlap_by_destructive_test(psi: Sequence[complex], phi: Sequence[complex], runs: int, rng: random.Random) -> float:
    zeros = sum(1 for _ in range(runs) if destructive_swap_test(psi, phi, rng) == 0)
    return 2 * zeros / runs - 1


def exact_overlap(psi: Sequence[complex], phi: Sequence[complex]) -> float:
    return abs(sum(complex(x).conjugate() * y for x, y in zip(psi, phi))) ** 2
