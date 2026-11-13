# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shor-code/. The authors are listed in prov/MXZFJW.jsonl.
"""The Shor nine-qubit code [[9, 1, 3]]: encoder, syndrome, decoder and code checks.

Qubits 0..8 form three blocks {0, 1, 2}, {3, 4, 5}, {6, 7, 8}. Qubit 0 is the least significant
bit of a basis index, and the rightmost letter of a Pauli word acts on qubit 0 (qsim.py).

|0_L> = (|000> + |111>)^(x3) / (2 sqrt 2),  |1_L> = (|000> - |111>)^(x3) / (2 sqrt 2).
"""

import math

from qsim import H, apply_1q, apply_cnot, apply_pauli, basis_state, inner

N = 9
BLOCKS = [(0, 1, 2), (3, 4, 5), (6, 7, 8)]


def word(ops: dict) -> str:
    """The 9-letter Pauli word with letter ops[q] on qubit q and I elsewhere."""
    return "".join(ops.get(q, "I") for q in range(N - 1, -1, -1))


# Six Z checks (two in each block) and two X checks of weight six.
Z_CHECKS = [word({a: "Z", b: "Z"}) for blk in BLOCKS for a, b in ((blk[0], blk[1]), (blk[1], blk[2]))]
X_CHECKS = [word({q: "X" for q in range(0, 6)}), word({q: "X" for q in range(3, 9)})]
GENERATORS = Z_CHECKS + X_CHECKS
LOGICAL_X = word({0: "Z", 3: "Z", 6: "Z"})  # maps |0_L> to |1_L>
LOGICAL_Z = word({q: "X" for q in range(N)})  # |0_L> -> |0_L>, |1_L> -> -|1_L>


def code_basis() -> tuple[list[complex], list[complex]]:
    """|0_L> and |1_L> built from their definition."""
    s = 1 / (2 * math.sqrt(2))
    zero = [0j] * (1 << N)
    one = [0j] * (1 << N)
    for pattern in range(8):  # which blocks are |111>
        x = 0
        for b in range(3):
            if pattern >> b & 1:
                x |= 0b111 << (3 * b)
        zero[x] += s
        one[x] += s * (-1) ** bin(pattern).count("1")
    return zero, one


def encode(alpha: complex, beta: complex) -> list[complex]:
    """The encoding circuit: alpha|0> + beta|1> on qubit 0 goes to alpha|0_L> + beta|1_L>."""
    v = [0j] * (1 << N)
    v[0], v[1] = alpha, beta
    v = apply_cnot(v, 0, 3)
    v = apply_cnot(v, 0, 6)  # phase-flip code on the block leaders 0, 3, 6 ...
    for q in (0, 3, 6):
        v = apply_1q(v, H, q)  # ... in the Hadamard basis
    for lead in (0, 3, 6):
        v = apply_cnot(v, lead, lead + 1)
        v = apply_cnot(v, lead, lead + 2)  # bit-flip code inside each block
    return v


def anticommute(a: str, b: str) -> bool:
    return sum(1 for p, q in zip(a, b) if p != "I" and q != "I" and p != q) % 2 == 1


def syndrome(error: str) -> tuple[int, ...]:
    """Bit i is 1 when the Pauli error anticommutes with generator i (6 Z checks, then 2 X checks)."""
    return tuple(int(anticommute(g, error)) for g in GENERATORS)


def measured_syndrome(state: list[complex]) -> tuple[int, ...]:
    """Read the syndrome from a state that is an eigenstate of every generator (a Pauli error on a codeword)."""
    out = []
    for g in GENERATORS:
        e = inner(state, apply_pauli(state, g)).real
        if abs(abs(e) - 1) > 1e-9:
            raise ValueError("the state is not an eigenstate of the checks")
        out.append(0 if e > 0 else 1)
    return tuple(out)


def decode(s: tuple[int, ...]) -> str:
    """The correction for a syndrome: at most one X in each block and one Z for the whole code."""
    ops: dict = {}
    for b, blk in enumerate(BLOCKS):
        s1, s2 = s[2 * b], s[2 * b + 1]  # checks Z_a Z_b and Z_b Z_c of the block (a, b, c)
        q = {(1, 0): blk[0], (1, 1): blk[1], (0, 1): blk[2]}.get((s1, s2))
        if q is not None:
            ops[q] = "X"
    blk = {(1, 0): 0, (1, 1): 1, (0, 1): 2}.get((s[6], s[7]))
    if blk is not None:
        q = BLOCKS[blk][0]  # any qubit of the block; Z_a Z_b is in the stabilizer
        ops[q] = "Y" if ops.get(q) == "X" else "Z"
    return word(ops)


def project_syndrome(state: list[complex], s: tuple[int, ...]) -> list[complex]:
    """prod_i (I + (-1)^s_i g_i)/2 applied to the state (not normalized)."""
    for g, bit in zip(GENERATORS, s):
        gv = apply_pauli(state, g)
        sg = -1 if bit else 1
        state = [(a + sg * b) / 2 for a, b in zip(state, gv)]
    return state


def correct_general(state: list[complex], qubit: int) -> list[tuple[float, list[complex]]]:
    """Correct an arbitrary error on one known-or-unknown qubit: measure the syndrome (only the
    syndromes of I, X, Y, Z on that qubit can occur), then apply the decoder's correction.
    Returns the branches (probability, state)."""
    out = []
    seen = set()
    for p in "IXYZ":
        s = syndrome(word({qubit: p}) if p != "I" else "I" * N)
        if s in seen:
            continue
        seen.add(s)
        v = project_syndrome(state, s)
        pr = inner(v, v).real
        if pr > 1e-12:
            v = [a / math.sqrt(pr) for a in v]
            out.append((pr, apply_pauli(v, decode(s))))
    return out


def to_binary(w: str) -> int:
    """Pauli word (up to sign) as an 18-bit vector: x part in bits 9..17, z part in bits 0..8."""
    x = z = 0
    for q, c in enumerate(reversed(w)):
        if c in "XY":
            x |= 1 << q
        if c in "ZY":
            z |= 1 << q
    return (x << N) | z


def in_span(v: int, rows: list[int]) -> bool:
    """Gaussian elimination over GF(2) on bit vectors. The basis is kept with distinct leading
    bits in decreasing order, so min(r, r ^ b) clears the leading bit of b from r."""
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
