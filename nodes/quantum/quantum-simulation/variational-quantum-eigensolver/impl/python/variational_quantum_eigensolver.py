# SPDX-License-Identifier: MIT
"""The variational quantum eigensolver (VQE), simulated with exact state vectors.

The trial state is a hardware-efficient circuit: a layer of Y rotations
R_Y(theta) = e^(-i theta Y / 2) on every qubit, then a chain of CNOT gates,
repeated, and a last layer of Y rotations. The energy E(theta) = <psi(theta)|H|psi(theta)>
is minimized by gradient descent, with gradients from the parameter-shift rule.
Qubit 0 is the least significant bit, as in qsim.py.
"""

import math
import random

from qsim import (
    PAULI,
    apply_1q,
    apply_controlled,
    apply_pauli,
    basis_state,
    inner,
    pauli_rotation,
    pauli_sum_apply,
    probabilities,
    sample_index,
)

Terms = list[tuple[float, str]]


def ansatz(n: int, layers: int) -> list[tuple]:
    """The gate list of the circuit. ("R", P) is a rotation e^(-i theta P / 2) with its own
    parameter; ("CNOT", c, t) is a fixed gate. P is a Pauli string on n qubits."""
    gates: list[tuple] = []
    for layer in range(layers + 1):
        for q in range(n):
            gates.append(("R", "".join("Y" if n - 1 - pos == q else "I" for pos in range(n))))
        if layer < layers:
            for q in range(n - 1):
                gates.append(("CNOT", q, q + 1))
    return gates


def num_parameters(gates: list[tuple]) -> int:
    return sum(1 for g in gates if g[0] == "R")


def prepare(n: int, gates: list[tuple], theta: list[float], insert: int = -1) -> list[complex]:
    """The trial state U(theta)|0...0>. If insert = k, the operator -i P_k / 2 is applied right
    after rotation k, which gives the partial derivative of the state in theta_k."""
    psi = basis_state(n, 0)
    k = 0
    for g in gates:
        if g[0] == "R":
            psi = pauli_rotation(psi, g[1], theta[k])
            if k == insert:
                psi = [-0.5j * a for a in apply_pauli(psi, g[1])]
            k += 1
        else:
            psi = apply_controlled(psi, PAULI["X"], [g[1]], g[2])
    return psi


def energy(terms: Terms, n: int, gates: list[tuple], theta: list[float]) -> float:
    """E(theta) = <psi(theta)|H|psi(theta)>, exactly."""
    psi = prepare(n, gates, theta)
    return inner(psi, pauli_sum_apply(terms, psi)).real


def parameter_shift_gradient(terms: Terms, n: int, gates: list[tuple], theta: list[float]) -> list[float]:
    """dE/dtheta_k = (E(theta + (pi/2) e_k) - E(theta - (pi/2) e_k)) / 2 for each k."""
    grad = []
    for k in range(len(theta)):
        plus = list(theta)
        minus = list(theta)
        plus[k] += math.pi / 2
        minus[k] -= math.pi / 2
        grad.append(0.5 * (energy(terms, n, gates, plus) - energy(terms, n, gates, minus)))
    return grad


def exact_gradient(terms: Terms, n: int, gates: list[tuple], theta: list[float]) -> list[float]:
    """dE/dtheta_k = 2 Re <psi|H|d_k psi>, with d_k psi from prepare(..., insert=k)."""
    psi = prepare(n, gates, theta)
    hpsi = pauli_sum_apply(terms, psi)
    return [2 * inner(hpsi, prepare(n, gates, theta, insert=k)).real for k in range(len(theta))]


def finite_difference_gradient(terms: Terms, n: int, gates: list[tuple], theta: list[float], h: float = 1e-5) -> list[float]:
    """The central difference (E(theta + h e_k) - E(theta - h e_k)) / (2 h)."""
    grad = []
    for k in range(len(theta)):
        plus = list(theta)
        minus = list(theta)
        plus[k] += h
        minus[k] -= h
        grad.append((energy(terms, n, gates, plus) - energy(terms, n, gates, minus)) / (2 * h))
    return grad


def vqe(
    terms: Terms, n: int, layers: int, rng: random.Random, steps: int = 300, rate: float = 0.1, shots: int | None = None
) -> tuple[list[float], list[float]]:
    """Minimize E(theta) by gradient descent with parameter-shift gradients.

    The start point is uniform in [0, 2 pi) for each parameter, drawn from rng.
    If shots is None the energies are exact; otherwise each energy is estimated
    from that many shots per term, with randomness from rng.
    Returns the final parameters and the energy after each step (the first entry is the start).
    """
    gates = ansatz(n, layers)

    def value(th: list[float]) -> float:
        if shots is None:
            return energy(terms, n, gates, th)
        return estimate_energy(terms, prepare(n, gates, th), shots, rng)

    theta = [rng.uniform(0, 2 * math.pi) for _ in range(num_parameters(gates))]  # @line L1
    history = [value(theta)]
    for _ in range(steps):  # @line L2
        grad = []
        for k in range(len(theta)):  # @line L3
            plus = list(theta)
            minus = list(theta)
            plus[k] += math.pi / 2
            minus[k] -= math.pi / 2
            e_plus = value(plus)  # @line L4
            e_minus = value(minus)  # @line L5
            grad.append(0.5 * (e_plus - e_minus))  # @line L6
        theta = [t - rate * g for t, g in zip(theta, grad)]  # @line L7
        history.append(value(theta))
    return theta, history  # @line L8


# ---------------------------------------------------------------- energy from measurement shots


def _rotate_to_z_basis(psi: list[complex], s: str) -> list[complex]:
    """Apply H on each X position and H S^dagger on each Y position, so that a
    computational basis measurement measures the Pauli string s."""
    n = len(s)
    h = [[1 / math.sqrt(2), 1 / math.sqrt(2)], [1 / math.sqrt(2), -1 / math.sqrt(2)]]
    hsd = [[1 / math.sqrt(2), -1j / math.sqrt(2)], [1 / math.sqrt(2), 1j / math.sqrt(2)]]
    for pos, ch in enumerate(s):
        q = n - 1 - pos
        if ch == "X":
            psi = apply_1q(psi, h, q)
        elif ch == "Y":
            psi = apply_1q(psi, hsd, q)
    return psi


def estimate_term(psi: list[complex], s: str, shots: int, rng: random.Random) -> float:
    """The mean of the +1/-1 outcomes of the Pauli string s over the given number of shots."""
    n = len(s)
    support = sum(1 << (n - 1 - pos) for pos, ch in enumerate(s) if ch != "I")
    if support == 0:
        return 1.0
    p = probabilities(_rotate_to_z_basis(psi, s))
    total = 0
    for _ in range(shots):  # @line L10
        x = sample_index(p, rng)
        total += -1 if bin(x & support).count("1") & 1 else 1
    return total / shots  # @line L11


def estimate_energy(terms: Terms, psi: list[complex], shots: int, rng: random.Random) -> float:
    """sum_j c_j times the estimate of <P_j>, with the given number of shots for each term."""
    total = 0.0
    for c, s in terms:  # @line L9
        total += c * estimate_term(psi, s, shots, rng)
    return total  # @line L12
