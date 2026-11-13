# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cnot-gate/. The authors are listed in prov/TC4WH0.jsonl.
"""The CNOT gate |a, b> -> |a, a XOR b>, on two qubits and inside an n-qubit register, and the Bell circuit.

Qubit order: qubit j is bit j of the basis index, and |a, b> = |a> (x) |b> has the index 2a + b.
So in the 4 x 4 matrix the control is the left symbol (qubit 1) and the target is the right symbol (qubit 0).
"""

import math

from qsim import apply_1q, apply_permutation, basis_state

Vector = list[complex]
Matrix = list[list[complex]]

R2 = math.sqrt(0.5)
H = [[complex(R2), complex(R2)], [complex(R2), complex(-R2)]]
X = [[0j, 1 + 0j], [1 + 0j, 0j]]

CNOT = [
    [1 + 0j, 0j, 0j, 0j],
    [0j, 1 + 0j, 0j, 0j],
    [0j, 0j, 0j, 1 + 0j],
    [0j, 0j, 1 + 0j, 0j],
]


def cnot_permutation(n: int, control: int, target: int) -> list[int]:
    """The basis map x -> x XOR (bit control of x) * 2^target."""
    if control == target or not (0 <= control < n and 0 <= target < n):
        raise ValueError("control and target must be two different qubits of the register")
    return [x ^ (((x >> control) & 1) << target) for x in range(1 << n)]


def cnot(state: Vector, control: int, target: int) -> Vector:
    n = len(state).bit_length() - 1
    return apply_permutation(state, cnot_permutation(n, control, target))


def bell_state(a: int, b: int) -> Vector:
    """The Bell state beta_ab: H on the control qubit 1 of |a, b>, then CNOT from qubit 1 to qubit 0."""
    s = basis_state(2, 2 * a + b)
    s = apply_1q(s, H, 1)
    return cnot(s, 1, 0)


def is_product_2q(state: Vector, tol: float = 1e-12) -> bool:
    """A two-qubit state a00|00> + a01|01> + a10|10> + a11|11> is a product state exactly when a00 a11 = a01 a10."""
    a00, a01, a10, a11 = state
    return abs(a00 * a11 - a01 * a10) < tol
