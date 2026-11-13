# SPDX-License-Identifier: MIT
# Shared helper of the qs1 quantum pages of https://algorithm.tamnd.com/. The authors are listed in prov/.
"""A small state-vector simulator in pure Python.

A state on n qubits is a list of 2^n complex amplitudes. The basis index
i = sum of b_q 2^q, so qubit 0 is the least significant bit of the index.
This module holds only gates, probabilities and measurement. It holds no
algorithm of any page.
"""

import cmath
import math
import random
from typing import Callable, Sequence

Matrix2 = tuple[tuple[complex, complex], tuple[complex, complex]]

SQRT_HALF = 1.0 / math.sqrt(2.0)
H: Matrix2 = ((SQRT_HALF, SQRT_HALF), (SQRT_HALF, -SQRT_HALF))
X: Matrix2 = ((0.0, 1.0), (1.0, 0.0))
Z: Matrix2 = ((1.0, 0.0), (0.0, -1.0))


def phase_gate(phi: float) -> Matrix2:
    """The gate diag(1, e^(i phi))."""
    return ((1.0, 0.0), (0.0, cmath.exp(1j * phi)))


def basis_state(n: int, index: int = 0) -> list[complex]:
    """The basis state |index> on n qubits."""
    if not 0 <= index < (1 << n):
        raise ValueError("index out of range")
    state = [0j] * (1 << n)
    state[index] = 1.0 + 0j
    return state


def apply_1q(state: list[complex], q: int, m: Matrix2) -> None:
    """Apply the 2 x 2 matrix m to qubit q, in place."""
    (a, b), (c, d) = m
    bit = 1 << q
    for i in range(len(state)):
        if i & bit == 0:
            x0 = state[i]
            x1 = state[i | bit]
            state[i] = a * x0 + b * x1
            state[i | bit] = c * x0 + d * x1


def apply_controlled_1q(state: list[complex], controls: Sequence[int], target: int, m: Matrix2) -> None:
    """Apply m to qubit target when every qubit in controls is 1, in place."""
    mask = 0
    for c in controls:
        mask |= 1 << c
    if mask & (1 << target):
        raise ValueError("the target is also a control")
    (a, b), (c, d) = m
    bit = 1 << target
    for i in range(len(state)):
        if i & bit == 0 and i & mask == mask:
            x0 = state[i]
            x1 = state[i | bit]
            state[i] = a * x0 + b * x1
            state[i | bit] = c * x0 + d * x1


def apply_permutation(state: list[complex], perm: Sequence[int]) -> None:
    """Map |i> to |perm[i]>, in place. perm must be a permutation of the indices."""
    if sorted(perm) != list(range(len(state))):
        raise ValueError("not a permutation")
    old = state[:]
    for i, j in enumerate(perm):
        state[j] = old[i]


def apply_diagonal(state: list[complex], phase: Callable[[int], complex]) -> None:
    """Multiply the amplitude of |i> by phase(i), in place. Each phase(i) must have modulus 1."""
    for i in range(len(state)):
        state[i] *= phase(i)


def apply_controlled_block(state: list[complex], control: int, n_low: int,
                           op: Callable[[list[complex]], list[complex]]) -> None:
    """Apply op to the low register (qubits 0 .. n_low - 1) when qubit control is 1.

    op takes and returns a list of 2^n_low amplitudes, and must be linear and
    unitary. The control must be a qubit outside the low register.
    """
    if control < n_low:
        raise ValueError("the control is inside the low register")
    size = 1 << n_low
    bit = 1 << control
    for base in range(0, len(state), size):
        if base & bit:
            block = op(state[base:base + size])
            if len(block) != size:
                raise ValueError("op changed the register size")
            state[base:base + size] = block


def probabilities(state: Sequence[complex]) -> list[float]:
    """The probability |a_i|^2 of each basis state."""
    return [abs(a) ** 2 for a in state]


def register_probabilities(state: Sequence[complex], low: int, width: int) -> list[float]:
    """The probability of each value of the register of qubits low .. low + width - 1."""
    out = [0.0] * (1 << width)
    mask = (1 << width) - 1
    for i, a in enumerate(state):
        out[(i >> low) & mask] += abs(a) ** 2
    return out


def norm(state: Sequence[complex]) -> float:
    return math.sqrt(sum(abs(a) ** 2 for a in state))


def sample(probs: Sequence[float], rng: random.Random) -> int:
    """Draw an index with the given probabilities."""
    r = rng.random() * sum(probs)
    acc = 0.0
    for i, p in enumerate(probs):
        acc += p
        if r < acc:
            return i
    for i in range(len(probs) - 1, -1, -1):
        if probs[i] > 0.0:
            return i
    raise ValueError("all probabilities are zero")


def measure(state: Sequence[complex], rng: random.Random) -> int:
    """Measure all qubits in the computational basis. Return the basis index."""
    return sample(probabilities(state), rng)
