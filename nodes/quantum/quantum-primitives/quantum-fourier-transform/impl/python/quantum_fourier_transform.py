# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quantum-fourier-transform/. The authors are listed in prov/9X30GG.jsonl.
"""The quantum Fourier transform on n qubits, as a list of gates.

QFT |j> = 2^(-n/2) sum_k e^(2 pi i j k / 2^n) |k>, with qubit 0 as the least
significant bit of j and k. A gate is one of
  ("h", q)            a Hadamard gate on qubit q
  ("cr", p, q, k)     the controlled phase diag(1, 1, 1, e^(2 pi i / 2^k)) on qubits p, q
  ("swap", a, b)      a swap of qubits a and b
The approximate QFT with parameter m keeps only the rotations with k <= m.
"""

import math

from qsim import H, apply_1q, apply_controlled_phase, apply_swap

Gate = tuple


def qft_circuit(n: int, m: int | None = None) -> list[Gate]:
    """The gates of the QFT on n qubits; with m < n, the approximate QFT."""
    if m is None:
        m = n
    gates: list[Gate] = []  # @line L1
    for q in range(n - 1, -1, -1):  # @line L2
        gates.append(("h", q))  # @line L3
        for p in range(q - 1, -1, -1):  # @line L4
            k = q - p + 1  # @line L5
            if k <= m:  # @line L6
                gates.append(("cr", p, q, k))  # @line L6
    for q in range(n // 2):  # @line L7
        gates.append(("swap", q, n - 1 - q))  # @line L8
    return gates  # @line L9


def inverse_circuit(gates: list[Gate]) -> list[Gate]:
    """The inverse: the gates in reverse order, each rotation with the opposite sign."""
    out: list[Gate] = []
    for g in reversed(gates):
        if g[0] == "cr":
            out.append(("cr", g[1], g[2], -g[3]))
        else:
            out.append(g)
    return out


def apply_circuit(state: list[complex], gates: list[Gate], offset: int = 0) -> None:
    """Apply the gates to the qubits offset, offset + 1, ... of the state.

    In ("cr", p, q, k) a negative k means the inverse rotation e^(-2 pi i / 2^|k|).
    """
    for g in gates:
        if g[0] == "h":
            apply_1q(state, g[1] + offset, H)
        elif g[0] == "cr":
            k = g[3]
            angle = (2 * math.pi / 2 ** abs(k)) * (1 if k > 0 else -1)
            apply_controlled_phase(state, g[1] + offset, g[2] + offset, angle)
        elif g[0] == "swap":
            apply_swap(state, g[1] + offset, g[2] + offset)
        else:
            raise ValueError(f"unknown gate {g!r}")


def qft(state: list[complex], n: int, m: int | None = None) -> None:
    """Apply the (approximate) QFT to the n-qubit state in place."""
    apply_circuit(state, qft_circuit(n, m))


def gate_counts(gates: list[Gate]) -> dict[str, int]:
    counts = {"h": 0, "cr": 0, "swap": 0}
    for g in gates:
        counts[g[0]] += 1
    return counts


def aqft_error_bound(n: int, m: int) -> float:
    """An operator norm bound on QFT - AQFT_m: sum over dropped rotations of |e^(i a) - 1|.

    The rotation R_k occurs n - k + 1 times, and |e^(2 pi i / 2^k) - 1| = 2 sin(pi / 2^k).
    """
    return sum((n - k + 1) * 2 * math.sin(math.ldexp(math.pi, -k)) for k in range(m + 1, n + 1))
