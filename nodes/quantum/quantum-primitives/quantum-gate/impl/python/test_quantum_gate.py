# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quantum-gate/. The authors are listed in prov/H2C1T8.jsonl.

import math
import random

import pytest

from qsim import apply_1q, apply_controlled, basis_state, close, identity, matmul
from quantum_gate import apply_gate, circuit_unitary, depth, inverse_circuit, run

R = math.sqrt(0.5)
H = [[complex(R), complex(R)], [complex(R), complex(-R)]]
X = [[0j, 1 + 0j], [1 + 0j, 0j]]
Z = [[1 + 0j, 0j], [0j, -1 + 0j]]
S = [[1 + 0j, 0j], [0j, 1j]]
# CNOT with the control on local qubit 1 and the target on local qubit 0
CNOT = [[1 + 0j if (r, c) in ((0, 0), (1, 1), (2, 3), (3, 2)) else 0j for c in range(4)] for r in range(4)]
TOFFOLI = [[1 + 0j if r == (c ^ 1 if c >> 1 == 3 else c) else 0j for c in range(8)] for r in range(8)]


def rand_state(rng: random.Random, d: int) -> list[complex]:
    v = [complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(d)]
    s = math.sqrt(sum(abs(a) ** 2 for a in v))
    return [a / s for a in v]


def test_one_qubit_gates_match_the_simulator() -> None:
    rng = random.Random(81)
    for n in range(1, 5):
        s = rand_state(rng, 1 << n)
        for j in range(n):
            assert close(apply_gate(s, H, [j]), apply_1q(s, H, j))


def test_qubit_list_orders_the_gate() -> None:
    rng = random.Random(82)
    s = rand_state(rng, 8)
    # qubits = [target, control]: local qubit 0 is the target, local qubit 1 the control
    assert close(apply_gate(s, CNOT, [0, 2]), apply_controlled(s, X, [2], 0))
    assert close(apply_gate(s, CNOT, [2, 0]), apply_controlled(s, X, [0], 2))
    assert close(apply_gate(s, TOFFOLI, [1, 0, 2]), apply_controlled(s, X, [0, 2], 1))
    # |a b> with a on qubit 1: CNOT maps |10> to |11>
    assert apply_gate(basis_state(2, 2), CNOT, [0, 1]) == basis_state(2, 3)


def test_circuit_matrix_order() -> None:
    # the circuit "H, then S" on one qubit has the matrix S H, not H S
    u = circuit_unitary(1, [(H, [0]), (S, [0])])
    assert close(u, matmul(S, H)) and not close(u, matmul(H, S))


def test_gates_on_disjoint_qubits_commute() -> None:
    rng = random.Random(83)
    s = rand_state(rng, 8)
    a = run(s, [(H, [0]), (CNOT, [1, 2])])
    b = run(s, [(CNOT, [1, 2]), (H, [0])])
    assert close(a, b)
    # on the same qubit they need not commute
    assert not close(run(s, [(H, [0]), (Z, [0])]), run(s, [(Z, [0]), (H, [0])]))


def test_inverse_and_depth() -> None:
    circuit = [(H, [0]), (CNOT, [1, 0]), (S, [1]), (H, [2]), (TOFFOLI, [2, 0, 1]), (X, [0])]
    full = circuit + inverse_circuit(circuit)
    assert close(circuit_unitary(3, full), identity(8))
    assert depth(circuit) == 5
    assert depth([(H, [0]), (H, [1]), (H, [2])]) == 1


def test_rejects_bad_gates() -> None:
    s = basis_state(2, 0)
    with pytest.raises(ValueError):
        apply_gate(s, [[1, 1], [0, 1]], [0])
    with pytest.raises(ValueError):
        apply_gate(s, CNOT, [0, 0])
    with pytest.raises(ValueError):
        apply_gate(s, H, [2])
