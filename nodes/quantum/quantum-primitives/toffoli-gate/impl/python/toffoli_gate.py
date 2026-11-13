# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/toffoli-gate/. The authors are listed in prov/8SZNQR.jsonl.
"""The Toffoli gate: its classical action, two exact decompositions, and the classical gates it gives.

Qubit order: qubit 0 is the least significant bit of a basis index (see qsim.py).
"""

from qsim import X, apply_controlled_1q


def toffoli_bits(a: int, b: int, c: int) -> tuple:
    """The Toffoli gate on three classical bits: (a, b, c) -> (a, b, c xor (a and b))."""
    return a, b, c ^ (a & b)


def toffoli(state, c1: int, c2: int, t: int):
    """Apply the Toffoli gate with controls c1, c2 and target t to a state vector."""
    return apply_controlled_1q(state, X, (c1, c2), t)


def clifford_t_toffoli(c1: int, c2: int, t: int) -> list:
    """An exact Clifford plus T circuit for the Toffoli gate: 6 CNOT, 7 T or T^dagger, 2 H."""
    return [
        ("h", t),
        ("cx", c2, t), ("tdg", t),
        ("cx", c1, t), ("t", t),
        ("cx", c2, t), ("tdg", t),
        ("cx", c1, t), ("t", c2), ("t", t),
        ("h", t),
        ("cx", c1, c2), ("t", c1), ("tdg", c2),
        ("cx", c1, c2),
    ]


# V is a square root of X: V V = X.
V = [[(1 + 1j) / 2, (1 - 1j) / 2], [(1 - 1j) / 2, (1 + 1j) / 2]]
V_DAG = [[(1 - 1j) / 2, (1 + 1j) / 2], [(1 + 1j) / 2, (1 - 1j) / 2]]


def two_qubit_toffoli(state, c1: int, c2: int, t: int):
    """The construction of Barenco et al. (1995) from five two-qubit gates:
    controlled-V (c2 -> t), CNOT (c1 -> c2), controlled-V^dagger (c2 -> t), CNOT (c1 -> c2),
    controlled-V (c1 -> t)."""
    state = apply_controlled_1q(state, V, (c2,), t)
    state = apply_controlled_1q(state, X, (c1,), c2)
    state = apply_controlled_1q(state, V_DAG, (c2,), t)
    state = apply_controlled_1q(state, X, (c1,), c2)
    state = apply_controlled_1q(state, V, (c1,), t)
    return state


def gate_counts(gates) -> dict:
    counts = {}
    for g in gates:
        counts[g[0]] = counts.get(g[0], 0) + 1
    return counts


# Classical gates built from one Toffoli and constant bits. Each returns the full output triple.
def and_gate(a: int, b: int) -> tuple:
    """AND: the target starts at 0, so it ends as a and b. Outputs (a, b, a and b)."""
    return toffoli_bits(a, b, 0)


def nand_gate(a: int, b: int) -> tuple:
    """NAND: the target starts at 1. Outputs (a, b, not (a and b))."""
    return toffoli_bits(a, b, 1)


def not_gate(c: int) -> tuple:
    """NOT: both controls are 1. Outputs (1, 1, not c)."""
    return toffoli_bits(1, 1, c)


def fanout_gate(a: int) -> tuple:
    """FANOUT (copy): the second control is 1 and the target is 0. Outputs (a, 1, a)."""
    return toffoli_bits(a, 1, 0)


def toffoli_permutation(n: int, c1: int = 0, c2: int = 1, t: int = 2) -> list:
    """The Toffoli gate on n wires as a permutation of the 2**n basis indices."""
    out = []
    for x in range(1 << n):
        if (x >> c1) & 1 and (x >> c2) & 1:
            x ^= 1 << t
        out.append(x)
    return out


def permutation_sign(perm) -> int:
    """+1 for an even permutation and -1 for an odd one, by counting cycles."""
    seen = [False] * len(perm)
    sign = 1
    for i in range(len(perm)):
        if seen[i]:
            continue
        j, length = i, 0
        while not seen[j]:
            seen[j] = True
            j = perm[j]
            length += 1
        if length % 2 == 0:
            sign = -sign
    return sign


def global_phase_free_equal(u, w, tol: float = 1e-9) -> bool:
    """True when the matrices u and w are equal exactly, with no global phase allowed."""
    return all(abs(u[i][j] - w[i][j]) <= tol for i in range(len(u)) for j in range(len(u)))


def proportional(u, w, tol: float = 1e-9) -> bool:
    """True when u = e^(i phi) w for some phase phi."""
    for i in range(len(w)):
        for j in range(len(w)):
            if abs(w[i][j]) > tol:
                ph = u[i][j] / w[i][j]
                if abs(abs(ph) - 1) > tol:
                    return False
                return all(abs(u[r][c] - ph * w[r][c]) <= tol for r in range(len(u)) for c in range(len(u)))
    return False
