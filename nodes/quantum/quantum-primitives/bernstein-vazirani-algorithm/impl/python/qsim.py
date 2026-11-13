# SPDX-License-Identifier: MIT
# Shared helper of the qp3 quantum pages of https://algorithm.tamnd.com/. The authors are listed in prov/.
"""A small state-vector simulator that uses only the standard library.

Convention: a state on n qubits is a list of 2^n complex amplitudes.
Qubit 0 is the least significant bit of the basis index, so the basis
state with qubit q equal to b_q has the index sum of b_q * 2^q.

The functions change the state in place, except where the name says
otherwise. This file holds only gates, measurement and small matrix
tools. Each algorithm lives in the file of its own page.
"""

import math
import random

Matrix = list[list[complex]]

SQRT1_2 = 1.0 / math.sqrt(2.0)
H: Matrix = [[SQRT1_2, SQRT1_2], [SQRT1_2, -SQRT1_2]]
X: Matrix = [[0.0, 1.0], [1.0, 0.0]]


def basis_state(n: int, index: int = 0) -> list[complex]:
    """The basis state |index> on n qubits."""
    if not 0 <= index < (1 << n):
        raise ValueError("index out of range")
    state = [0j] * (1 << n)
    state[index] = 1.0 + 0j
    return state


def apply_1q(state: list[complex], q: int, u: Matrix) -> None:
    """Apply the 2 x 2 matrix u to qubit q."""
    bit = 1 << q
    u00, u01, u10, u11 = u[0][0], u[0][1], u[1][0], u[1][1]
    for i in range(len(state)):
        if not i & bit:
            a, b = state[i], state[i | bit]
            state[i] = u00 * a + u01 * b
            state[i | bit] = u10 * a + u11 * b


def apply_controlled_1q(state: list[complex], controls: list[int], target: int, u: Matrix) -> None:
    """Apply u to the target qubit on the basis states where every control qubit is 1."""
    mask = 0
    for c in controls:
        mask |= 1 << c
    bit = 1 << target
    if mask & bit:
        raise ValueError("the target is also a control")
    u00, u01, u10, u11 = u[0][0], u[0][1], u[1][0], u[1][1]
    for i in range(len(state)):
        if not i & bit and i & mask == mask:
            a, b = state[i], state[i | bit]
            state[i] = u00 * a + u01 * b
            state[i | bit] = u10 * a + u11 * b


def apply_controlled_phase(state: list[complex], a: int, b: int, angle: float) -> None:
    """Multiply by e^(i angle) the basis states where qubits a and b are both 1."""
    if a == b:
        raise ValueError("two different qubits are needed")
    mask = (1 << a) | (1 << b)
    w = complex(math.cos(angle), math.sin(angle))
    for i in range(len(state)):
        if i & mask == mask:
            state[i] *= w


def apply_swap(state: list[complex], a: int, b: int) -> None:
    """Exchange qubits a and b."""
    if a == b:
        return
    ba, bb = 1 << a, 1 << b
    for i in range(len(state)):
        if i & ba and not i & bb:
            j = (i ^ ba) | bb
            state[i], state[j] = state[j], state[i]


def apply_permutation(state: list[complex], perm: list[int]) -> None:
    """Map each basis state |i> to |perm[i]>. perm must be a permutation."""
    if len(perm) != len(state) or sorted(perm) != list(range(len(state))):
        raise ValueError("not a permutation of the basis")
    new = [0j] * len(state)
    for i, p in enumerate(perm):
        new[p] = state[i]
    state[:] = new


def apply_diagonal(state: list[complex], phases: list[complex]) -> None:
    """Multiply the amplitude of |i> by phases[i]."""
    if len(phases) != len(state):
        raise ValueError("length mismatch")
    for i, w in enumerate(phases):
        state[i] *= w


def apply_controlled_matrix(state: list[complex], control: int | None, first: int, k: int, m: Matrix) -> None:
    """Apply the 2^k x 2^k matrix m to the qubits first, ..., first + k - 1.

    Qubit first is the least significant bit of the row and column index of m.
    If control is not None, apply m only where the control qubit is 1.
    """
    size = 1 << k
    if len(m) != size or any(len(row) != size for row in m):
        raise ValueError("matrix size does not match k")
    block = (size - 1) << first
    cbit = 0 if control is None else 1 << control
    if cbit & block:
        raise ValueError("the control is inside the target block")
    for base in range(len(state)):
        if base & block or (cbit and not base & cbit):
            continue
        idx = [base | (r << first) for r in range(size)]
        old = [state[i] for i in idx]
        for r in range(size):
            row = m[r]
            state[idx[r]] = sum(row[c] * old[c] for c in range(size))


def probabilities(state: list[complex]) -> list[float]:
    """The exact probability of each basis state."""
    return [abs(a) ** 2 for a in state]


def marginal_probabilities(state: list[complex], qubits: list[int]) -> list[float]:
    """The exact distribution of the outcome of measuring the given qubits.

    Bit i of an outcome is the value of qubits[i].
    """
    out = [0.0] * (1 << len(qubits))
    for i, a in enumerate(state):
        p = abs(a) ** 2
        if p:
            o = 0
            for pos, q in enumerate(qubits):
                o |= ((i >> q) & 1) << pos
            out[o] += p
    return out


def sample(probs: list[float], rng: random.Random) -> int:
    """Draw an index with the given probabilities."""
    r = rng.random() * sum(probs)
    acc = 0.0
    for i, p in enumerate(probs):
        acc += p
        if r < acc:
            return i
    return max(i for i, p in enumerate(probs) if p > 0)


def measure(state: list[complex], qubits: list[int], rng: random.Random) -> int:
    """Measure the given qubits in the computational basis.

    Return the outcome (bit i is qubits[i]) and collapse the state in place.
    """
    o = sample(marginal_probabilities(state, qubits), rng)
    keep = 0.0
    for i in range(len(state)):
        v = 0
        for pos, q in enumerate(qubits):
            v |= ((i >> q) & 1) << pos
        if v != o:
            state[i] = 0j
        else:
            keep += abs(state[i]) ** 2
    scale = 1.0 / math.sqrt(keep)
    for i in range(len(state)):
        state[i] *= scale
    return o


def norm(state: list[complex]) -> float:
    return math.sqrt(sum(abs(a) ** 2 for a in state))


def inner(a: list[complex], b: list[complex]) -> complex:
    """The inner product <a|b>, linear in b."""
    return sum(x.conjugate() * y for x, y in zip(a, b))


def dagger(m: Matrix) -> Matrix:
    return [[m[j][i].conjugate() for j in range(len(m))] for i in range(len(m[0]))]


def matmul(a: Matrix, b: Matrix) -> Matrix:
    cols = list(zip(*b))
    return [[sum(x * y for x, y in zip(row, col)) for col in cols] for row in a]


def matrix_of(n: int, apply) -> Matrix:
    """The 2^n x 2^n matrix of the linear map apply, which changes a state in place."""
    size = 1 << n
    cols = []
    for j in range(size):
        s = basis_state(n, j)
        apply(s)
        cols.append(s)
    return [[cols[j][i] for j in range(size)] for i in range(size)]
