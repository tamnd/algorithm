# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pauli-gates/. The authors are listed in prov/KXAV0B.jsonl.
"""The Pauli matrices I, X, Y, Z, their products, the Pauli decomposition of a 2 x 2 matrix,
and Pauli strings on n qubits.

A Pauli string "P_{n-1} ... P_1 P_0" is written like a ket: the rightmost letter acts on qubit 0.
"""

from qsim import add, identity, matmul, scale

Matrix = list[list[complex]]

I = identity(2)  # noqa: E741
X = [[0j, 1 + 0j], [1 + 0j, 0j]]
Y = [[0j, -1j], [1j, 0j]]
Z = [[1 + 0j, 0j], [0j, -1 + 0j]]
PAULI = {"I": I, "X": X, "Y": Y, "Z": Z}

# PRODUCT[(a, b)] = (phase, c) with a b = phase * c
PRODUCT: dict[tuple[str, str], tuple[complex, str]] = {}
for _a in "IXYZ":
    PRODUCT[("I", _a)] = (1, _a)
    PRODUCT[(_a, "I")] = (1, _a)
    PRODUCT[(_a, _a)] = (1, "I")
for _a, _b, _c in (("X", "Y", "Z"), ("Y", "Z", "X"), ("Z", "X", "Y")):
    PRODUCT[(_a, _b)] = (1j, _c)
    PRODUCT[(_b, _a)] = (-1j, _c)


def trace(m: Matrix) -> complex:
    return sum(m[i][i] for i in range(len(m)))


def decompose(m: Matrix) -> dict[str, complex]:
    """Coefficients c_P = tr(P m) / 2 with m = c_I I + c_X X + c_Y Y + c_Z Z."""
    return {p: trace(matmul(PAULI[p], m)) / 2 for p in "IXYZ"}


def recompose(c: dict[str, complex]) -> Matrix:
    out = [[0j, 0j], [0j, 0j]]
    for p, v in c.items():
        out = add(out, scale(v, PAULI[p]))
    return out


def kron(a: Matrix, b: Matrix) -> Matrix:
    p = len(b)
    return [[a[r // p][c // p] * b[r % p][c % p] for c in range(len(a) * p)] for r in range(len(a) * p)]


def string_matrix(s: str) -> Matrix:
    """The matrix of the Pauli string s; s[0] acts on qubit n-1 and s[-1] on qubit 0."""
    out = [[1 + 0j]]
    for ch in s:
        out = kron(out, PAULI[ch])
    return out


def string_product(s: str, t: str) -> tuple[complex, str]:
    """(phase, u) with the matrix of s times the matrix of t equal to phase times the matrix of u."""
    phase: complex = 1
    out = []
    for a, b in zip(s, t):
        ph, c = PRODUCT[(a, b)]
        phase *= ph
        out.append(c)
    return phase, "".join(out)


def strings_commute(s: str, t: str) -> bool:
    """Two Pauli strings commute exactly when they differ, both not I, in an even number of places."""
    return sum(1 for a, b in zip(s, t) if a != "I" and b != "I" and a != b) % 2 == 0
