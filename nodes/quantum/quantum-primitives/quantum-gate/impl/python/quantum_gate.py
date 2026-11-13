# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quantum-gate/. The authors are listed in prov/H2C1T8.jsonl.
"""Quantum gates as unitary matrices on k qubits, applied to chosen qubits of an n-qubit register,
and circuits as lists of gates.

Qubit order: qubit j is bit j of the basis index. A k-qubit gate matrix uses the same order locally,
so its local qubit 0 is bit 0 of its row and column index. apply_gate(state, g, qubits) puts local qubit i
on the register qubit qubits[i].
"""

from qsim import circuit_matrix, dagger, is_unitary

Vector = list[complex]
Matrix = list[list[complex]]
Gate = tuple[Matrix, list[int]]


def apply_gate(state: Vector, gate: Matrix, qubits: list[int]) -> Vector:
    """Apply the 2^k x 2^k unitary gate to the listed qubits, where qubits[i] receives local qubit i."""
    k = len(qubits)
    n = len(state).bit_length() - 1
    if len(gate) != 1 << k or len(set(qubits)) != k or not all(0 <= q < n for q in qubits):
        raise ValueError("gate size and qubit list do not match")
    if not is_unitary(gate):
        raise ValueError("a gate must be unitary")
    mask = sum(1 << q for q in qubits)
    out = [0j] * len(state)
    for rest in range(len(state)):
        if rest & mask:
            continue
        # the 2^k basis states that agree with rest outside the gate qubits
        idx = []
        for local in range(1 << k):
            x = rest
            for i, q in enumerate(qubits):
                if (local >> i) & 1:
                    x |= 1 << q
            idx.append(x)
        amps = [state[x] for x in idx]
        for r, x in enumerate(idx):
            out[x] = sum(gate[r][c] * amps[c] for c in range(1 << k))
    return out


def run(state: Vector, circuit: list[Gate]) -> Vector:
    """Apply the gates in order: circuit[0] first."""
    for gate, qubits in circuit:
        state = apply_gate(state, gate, qubits)
    return state


def circuit_unitary(n: int, circuit: list[Gate]) -> Matrix:
    """The 2^n x 2^n matrix of the circuit. For the circuit [A, B] it is B times A."""
    return circuit_matrix(n, lambda s: run(s, circuit))


def inverse_circuit(circuit: list[Gate]) -> list[Gate]:
    """The gates in reverse order, each replaced by its conjugate transpose."""
    return [(dagger(g), list(q)) for g, q in reversed(circuit)]


def depth(circuit: list[Gate]) -> int:
    """The number of layers when each gate is placed in the first layer after the last gate on any of its qubits."""
    level: dict[int, int] = {}
    d = 0
    for _, qubits in circuit:
        t = 1 + max((level.get(q, 0) for q in qubits), default=0)
        for q in qubits:
            level[q] = t
        d = max(d, t)
    return d
