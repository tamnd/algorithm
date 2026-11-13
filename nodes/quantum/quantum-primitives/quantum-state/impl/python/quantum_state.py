# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quantum-state/. The authors are listed in prov/WTP45P.jsonl.
"""Pure states of n qubits as state vectors, with the qubit order convention of the encyclopedia.

Convention: qubit j is bit j of the basis index x, so qubit 0 is the least significant bit.
The label |b_{n-1} ... b_1 b_0> is the binary numeral of x: the leftmost symbol is qubit n-1.
"""

import math

from qsim import TOL, inner, norm


def dimension(n: int) -> int:
    """The dimension 2^n of the state space of n qubits."""
    return 1 << n


def real_parameters(n: int) -> int:
    """Real parameters of a pure state of n qubits: 2 * 2^n, less one for the norm and one for the global phase."""
    return 2 * dimension(n) - 2


def ket_label(n: int, x: int) -> str:
    """The label |b_{n-1} ... b_0> of the basis state with index x."""
    return "|" + format(x, f"0{n}b") + ">"


def index_of(bits: str) -> int:
    """The index x of the basis state |bits>, where bits[0] is qubit n-1 and bits[-1] is qubit 0."""
    if not bits or set(bits) - {"0", "1"}:
        raise ValueError("a basis label is a nonempty string of 0 and 1")
    return int(bits, 2)


def qubit_value(x: int, j: int) -> int:
    """The value of qubit j in the basis state |x>."""
    return (x >> j) & 1


def nielsen_chuang_qubit(n: int, j: int) -> int:
    """The number (1 to n, from the left) that Nielsen and Chuang give to qubit j of this convention."""
    return n - j


def from_amplitudes(n: int, amps: dict[str, complex]) -> list[complex]:
    """The state vector with the given amplitudes, keyed by basis labels such as "011". It must be a unit vector."""
    v = [0j] * dimension(n)
    for bits, a in amps.items():
        if len(bits) != n:
            raise ValueError("label length differs from n")
        v[index_of(bits)] += complex(a)
    if abs(norm(v) - 1) > TOL:
        raise ValueError("a state vector has norm 1")
    return v


def normalize(v: list[complex]) -> list[complex]:
    r = norm(v)
    if r == 0:
        raise ValueError("the zero vector is not a state")
    return [a / r for a in v]


def amplitude(state: list[complex], bits: str) -> complex:
    return state[index_of(bits)]


def overlap(phi: list[complex], psi: list[complex]) -> float:
    """|<phi|psi>|^2, which is 1 exactly when the two unit vectors are the same state."""
    return abs(inner(phi, psi)) ** 2


def same_state(phi: list[complex], psi: list[complex]) -> bool:
    return abs(overlap(phi, psi) - 1) <= TOL


def support(state: list[complex], tol: float = TOL) -> list[str]:
    """Labels of the basis states with a nonzero amplitude."""
    n = len(state).bit_length() - 1
    return [ket_label(n, x) for x, a in enumerate(state) if abs(a) > tol]


def ghz(n: int) -> list[complex]:
    """(|0...0> + |1...1>)/sqrt(2)."""
    v = [0j] * dimension(n)
    v[0] = v[-1] = complex(math.sqrt(0.5))
    return v
