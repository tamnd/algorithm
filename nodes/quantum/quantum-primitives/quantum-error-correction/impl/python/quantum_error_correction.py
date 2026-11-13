# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quantum-error-correction/. The authors are listed in prov/BBMCQ5.jsonl.
"""Quantum error correction on small codes: the Knill-Laflamme conditions, syndrome measurement
and correction, checked on state vectors.

States are lists of 2**n amplitudes (qsim.py convention: qubit 0 is the least significant bit,
and the rightmost letter of a Pauli word acts on qubit 0). An error is any function from a state
to a state (a Kraus operator, not necessarily unitary), or a Pauli word.
"""

import math

from qsim import R2, apply_pauli, basis_state, inner

Vector = list[complex]


def plus_minus(n: int, signs: str) -> Vector:
    """The product state of |+> and |-> given by a string of '+' and '-' (rightmost on qubit 0)."""
    v = [1 + 0j]
    for c in signs:
        f = [R2 + 0j, (R2 if c == "+" else -R2) + 0j]
        v = [a * b for a in v for b in f]
    return v


def bit_flip_code() -> tuple[list[Vector], list[tuple[int, str]]]:
    """|0_L> = |000>, |1_L> = |111>; generators ZZI and IZZ."""
    return [basis_state(3, 0), basis_state(3, 7)], [(1, "ZZI"), (1, "IZZ")]


def phase_flip_code() -> tuple[list[Vector], list[tuple[int, str]]]:
    """|0_L> = |+++>, |1_L> = |--->; generators XXI and IXX."""
    return [plus_minus(3, "+++"), plus_minus(3, "---")], [(1, "XXI"), (1, "IXX")]


def encode(basis: list[Vector], amps: list[complex]) -> Vector:
    out = [0j] * len(basis[0])
    for a, b in zip(amps, basis):
        for i, x in enumerate(b):
            out[i] += a * x
    return out


def kl_matrix(basis: list[Vector], errors: list, tol: float = 1e-9) -> list[list[complex]] | None:
    """The Knill-Laflamme test: <i| E_a^dagger E_b |j> = c_ab delta_ij for all code basis states i, j.

    errors is a list of functions state -> state. Returns the matrix c_ab, or None if the
    condition fails.
    """
    images = [[e(v) for v in basis] for e in errors]
    m = len(errors)
    c = [[0j] * m for _ in range(m)]
    for a in range(m):
        for b in range(m):
            g = [[inner(images[a][i], images[b][j]) for j in range(len(basis))] for i in range(len(basis))]
            for i in range(len(basis)):
                for j in range(len(basis)):
                    if i != j and abs(g[i][j]) > tol:
                        return None
                if abs(g[i][i] - g[0][0]) > tol:
                    return None
            c[a][b] = g[0][0]
    return c


def pauli_error(word: str):
    return lambda v: apply_pauli(v, word)


def project_syndrome(state: Vector, gens: list[tuple[int, str]], s: tuple[int, ...]) -> Vector:
    """prod_i (I + (-1)^s_i g_i)/2 applied to the state (not normalized)."""
    for (sign, word), bit in zip(gens, s):
        sg = sign * (-1 if bit else 1)
        gv = apply_pauli(state, word)
        state = [(a + sg * b) / 2 for a, b in zip(state, gv)]
    return state


def measure_syndrome(state: Vector, gens: list[tuple[int, str]]) -> dict:
    """All outcomes of measuring the generators: syndrome -> (probability, normalized state)."""
    out = {}
    m = len(gens)
    for code in range(1 << m):
        s = tuple((code >> i) & 1 for i in range(m))
        v = project_syndrome(state, gens, s)
        p = inner(v, v).real
        if p > 1e-12:
            out[s] = (p, [a / math.sqrt(p) for a in v])
    return out


def correct(state: Vector, gens: list[tuple[int, str]], table: dict) -> list[tuple[float, Vector]]:
    """Measure the syndrome, then apply the Pauli word table[syndrome]. Returns every branch."""
    branches = []
    for s, (p, v) in measure_syndrome(state, gens).items():
        branches.append((p, apply_pauli(v, table[s])))
    return branches


def same_ray(u: Vector, v: Vector, tol: float = 1e-9) -> bool:
    """True if u = e^(i phi) v for unit vectors u and v."""
    return abs(abs(inner(u, v)) - 1) < tol


def bit_flip_table() -> dict:
    # syndrome bits for (ZZI, IZZ): X on qubit 0 -> (0, 1), qubit 1 -> (1, 1), qubit 2 -> (1, 0)
    return {(0, 0): "III", (0, 1): "IIX", (1, 1): "IXI", (1, 0): "XII"}


def quantum_hamming_ok(n: int, k: int, t: int) -> bool:
    """The quantum Hamming bound for nondegenerate codes: 2^(n-k) >= sum_{j <= t} C(n, j) 3^j."""
    return 2 ** (n - k) >= sum(math.comb(n, j) * 3 ** j for j in range(t + 1))
