# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/steane-code/. The authors are listed in prov/QGYZM1.jsonl.
"""The Steane seven-qubit code [[7, 1, 3]], the CSS code of the [7, 4, 3] Hamming code.

Hamming parity-check matrix: column j (positions j = 1..7) is j in binary, top row the most
significant bit. Position j is qubit j - 1. Qubit 0 is the least significant bit of a basis
index, and the rightmost letter of a Pauli word acts on qubit 0 (qsim.py).

|0_L> = 8^(-1/2) sum of |c> over the 8 words c of the dual (simplex) code, the row space of H.
|1_L> = X^(x7) |0_L>, the same sum over the other coset of the dual code inside the Hamming code.
"""

import math

from qsim import H, apply_1q, apply_cnot, apply_pauli, inner

N = 7
# rows of H as sets of qubits: positions with bit 4, bit 2, bit 1 set
ROWS = [[j - 1 for j in range(1, 8) if j >> (2 - r) & 1] for r in range(3)]


def word(ops: dict) -> str:
    return "".join(ops.get(q, "I") for q in range(N - 1, -1, -1))


X_CHECKS = [word({q: "X" for q in row}) for row in ROWS]
Z_CHECKS = [word({q: "Z" for q in row}) for row in ROWS]
GENERATORS = X_CHECKS + Z_CHECKS
LOGICAL_X = "X" * N
LOGICAL_Z = "Z" * N


def row_mask(row: list[int]) -> int:
    return sum(1 << q for q in row)


def dual_code() -> list[int]:
    """The 8 words of the simplex code (the row space of H), as qubit bit masks."""
    rows = [row_mask(r) for r in ROWS]
    return sorted({(rows[0] * (m & 1)) ^ (rows[1] * (m >> 1 & 1)) ^ (rows[2] * (m >> 2 & 1)) for m in range(8)})


def hamming_code() -> list[int]:
    """The 16 words c with H c = 0."""
    rows = [row_mask(r) for r in ROWS]
    return [c for c in range(1 << N) if all(bin(c & r).count("1") % 2 == 0 for r in rows)]


def code_basis() -> tuple[list[complex], list[complex]]:
    s = 1 / math.sqrt(8)
    zero = [0j] * (1 << N)
    one = [0j] * (1 << N)
    for c in dual_code():
        zero[c] += s
        one[c ^ ((1 << N) - 1)] += s
    return zero, one


def encode(alpha: complex, beta: complex) -> list[complex]:
    """Encoding circuit. The data starts on qubit 2. The pivots 0, 1, 3 (positions 1, 2, 4) each
    lie in exactly one row of H."""
    v = [0j] * (1 << N)
    v[0], v[1 << 2] = alpha, beta
    for t in (4, 5):  # qubits 2, 4, 5 are positions 3, 5, 6, a weight-3 Hamming codeword
        v = apply_cnot(v, 2, t)
    for row, pivot in zip(ROWS, (3, 1, 0)):
        v = apply_1q(v, H, pivot)
        for t in row:
            if t != pivot:
                v = apply_cnot(v, pivot, t)
    return v


def anticommute(a: str, b: str) -> bool:
    return sum(1 for p, q in zip(a, b) if p != "I" and q != "I" and p != q) % 2 == 1


def syndrome(error: str) -> tuple[int, ...]:
    """Six bits: three X checks (which see Z errors), then three Z checks (which see X errors)."""
    return tuple(int(anticommute(g, error)) for g in GENERATORS)


def decode(s: tuple[int, ...]) -> str:
    """Read each three-bit half as a binary number: it is the position of the error, as for the Hamming code."""
    zpos = 4 * s[0] + 2 * s[1] + s[2]  # from the X checks: a Z error
    xpos = 4 * s[3] + 2 * s[4] + s[5]  # from the Z checks: an X error
    ops: dict = {}
    if xpos:
        ops[xpos - 1] = "X"
    if zpos:
        ops[zpos - 1] = "Y" if ops.get(zpos - 1) == "X" else "Z"
    return word(ops)


def measured_syndrome(state: list[complex]) -> tuple[int, ...]:
    out = []
    for g in GENERATORS:
        e = inner(state, apply_pauli(state, g)).real
        if abs(abs(e) - 1) > 1e-9:
            raise ValueError("the state is not an eigenstate of the checks")
        out.append(0 if e > 0 else 1)
    return tuple(out)


def project_syndrome(state: list[complex], s: tuple[int, ...]) -> list[complex]:
    for g, bit in zip(GENERATORS, s):
        gv = apply_pauli(state, g)
        sg = -1 if bit else 1
        state = [(a + sg * b) / 2 for a, b in zip(state, gv)]
    return state


def correct_general(state: list[complex]) -> list[tuple[float, list[complex]]]:
    """Measure all 6 checks (all 64 outcomes), then apply the decoder. Returns the branches."""
    out = []
    for code in range(64):
        s = tuple(code >> (5 - i) & 1 for i in range(6))
        v = project_syndrome(state, s)
        p = inner(v, v).real
        if p > 1e-12:
            v = [a / math.sqrt(p) for a in v]
            out.append((p, apply_pauli(v, decode(s))))
    return out


def transversal(state: list[complex], u, n_qubits: int = N) -> list[complex]:
    for q in range(n_qubits):
        state = apply_1q(state, u, q)
    return state


def to_binary(w: str) -> int:
    x = z = 0
    for q, c in enumerate(reversed(w)):
        if c in "XY":
            x |= 1 << q
        if c in "ZY":
            z |= 1 << q
    return (x << N) | z


def in_span(v: int, rows: list[int]) -> bool:
    """Gaussian elimination over GF(2); the basis keeps distinct leading bits in decreasing order."""
    basis: list[int] = []
    for r in rows:
        for b in basis:
            r = min(r, r ^ b)
        if r:
            basis.append(r)
            basis.sort(reverse=True)
    for b in basis:
        v = min(v, v ^ b)
    return v == 0
