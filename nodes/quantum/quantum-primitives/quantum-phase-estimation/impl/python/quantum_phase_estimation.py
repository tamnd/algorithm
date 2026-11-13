# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quantum-phase-estimation/. The authors are listed in prov/6JAGW4.jsonl.
"""Quantum phase estimation on the qp3 state-vector simulator.

Register A (the phase register) is qubits 0 to t - 1, and qubit 0 is the
least significant bit of the outcome m. Register B holds the eigenvector
on qubits t to t + b - 1. The oracle is a function cu(state, control, first, j)
that applies controlled U^(2^j) to register B. The estimate is m / 2^t.
"""

import math
import random

from qsim import H, Matrix, apply_1q, apply_controlled_matrix, apply_controlled_phase, apply_swap
from qsim import marginal_probabilities, matmul, sample


def inverse_qft(state: list[complex], t: int) -> None:
    """The inverse QFT on qubits 0 .. t - 1: the QFT circuit run backward."""
    for q in range(t // 2):
        apply_swap(state, q, t - 1 - q)
    for q in range(t):
        for p in range(q):
            apply_controlled_phase(state, p, q, -2 * math.pi / 2 ** (q - p + 1))
        apply_1q(state, q, H)


class PowerOracle:
    """Controlled U^(2^j) from the matrix U, by repeated squaring of U.

    Each call counts as one query. This is the cheap case, as for modular
    multiplication, where U^(2^j) is as cheap as U.
    """

    def __init__(self, u: Matrix, b: int) -> None:
        self.b = b
        self.powers = [u]
        self.queries = 0

    def __call__(self, state: list[complex], control: int, first: int, j: int) -> None:
        while len(self.powers) <= j:
            p = self.powers[-1]
            self.powers.append(matmul(p, p))
        apply_controlled_matrix(state, control, first, self.b, self.powers[j])
        self.queries += 1


class RepeatedOracle:
    """Controlled U^(2^j) as 2^j uses of controlled U. Counts the uses of U."""

    def __init__(self, u: Matrix, b: int) -> None:
        self.u, self.b, self.uses = u, b, 0

    def __call__(self, state: list[complex], control: int, first: int, j: int) -> None:
        for _ in range(1 << j):
            apply_controlled_matrix(state, control, first, self.b, self.u)
            self.uses += 1


def phase_estimation_distribution(t: int, b: int, cu, eigen: list[complex]) -> list[float]:
    """The exact distribution of the outcome m for the input |0^t> |eigen>."""
    if len(eigen) != 1 << b:
        raise ValueError("the eigenvector must have 2^b entries")
    state = [0j] * (1 << (t + b))  # @line L1
    for i, a in enumerate(eigen):  # @line L1
        state[i << t] = a  # @line L1
    for j in range(t):  # @line L2
        apply_1q(state, j, H)  # @line L2
    for j in range(t):  # @line L3
        cu(state, j, t, j)  # @line L3
    inverse_qft(state, t)  # @line L4
    return marginal_probabilities(state, list(range(t)))


def quantum_phase_estimation(t: int, b: int, cu, eigen: list[complex], rng: random.Random) -> float:
    """One run: return the estimate m / 2^t of the phase phi in [0, 1)."""
    m = sample(phase_estimation_distribution(t, b, cu, eigen), rng)  # @line L5
    return m / (1 << t)  # @line L6


def outcome_probability(phi: float, t: int, m: int) -> float:
    """The closed form P(m) = sin^2(pi T d) / (T^2 sin^2(pi d)), d = phi - m / T, T = 2^t."""
    size = 1 << t
    d = phi - m / size
    s = math.sin(math.pi * d)
    if abs(s) < 1e-15:
        return 1.0
    return (math.sin(math.pi * size * d) / (size * s)) ** 2


def circular_distance(a: float, b: float) -> float:
    """The distance of a and b on the circle of length 1."""
    d = (a - b) % 1.0
    return min(d, 1.0 - d)


def qubits_for(n: int, delta: float) -> int:
    """t = n + ceil(log2(2 + 1/(2 delta))): n correct bits with probability at least 1 - delta."""
    return n + math.ceil(math.log2(2 + 1 / (2 * delta)))
