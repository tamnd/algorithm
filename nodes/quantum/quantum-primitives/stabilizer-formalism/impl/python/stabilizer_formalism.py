# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/stabilizer-formalism/. The authors are listed in prov/YFZYCG.jsonl.
"""Stabilizer groups, the states and codes they fix, and syndromes of Pauli errors.

A generator is (sign, word) with sign in {1, -1} and word a Pauli string; the rightmost letter
of a word acts on qubit 0. The code space of commuting independent generators g_1..g_m on n
qubits is the image of the projector prod_i (I + g_i)/2, of dimension 2^(n - m).
The matrices are dense, so this module is for small n only (it checks the formalism; the fast
algorithms are on the clifford-group and gottesman-knill-theorem pages).
"""

from collections import deque

from qsim import H, S, add, apply_1q, apply_cnot, basis_state, identity, matmul, pauli_matrix, scale


def anticommute(a: str, b: str) -> bool:
    """True if the Pauli strings a and b anticommute."""
    k = sum(1 for p, q in zip(a, b) if p != "I" and q != "I" and p != q)
    return k % 2 == 1


def multiply(a: tuple[int, str], b: tuple[int, str]) -> tuple[complex, str]:
    """The product of two signed Pauli strings, as (phase, word)."""
    table = {("X", "Y"): (1j, "Z"), ("Y", "Z"): (1j, "X"), ("Z", "X"): (1j, "Y"),
             ("Y", "X"): (-1j, "Z"), ("Z", "Y"): (-1j, "X"), ("X", "Z"): (-1j, "Y")}
    phase: complex = a[0] * b[0]
    out = []
    for p, q in zip(a[1], b[1]):
        if p == "I":
            out.append(q)
        elif q == "I":
            out.append(p)
        elif p == q:
            out.append("I")
        else:
            f, r = table[(p, q)]
            phase *= f
            out.append(r)
    return phase, "".join(out)


def is_valid_stabilizer(gens: list[tuple[int, str]]) -> bool:
    """Generators commute in pairs, and no product of a nonempty subset is +-I (so -I is not in the group)."""
    for i in range(len(gens)):
        for j in range(i + 1, len(gens)):
            if anticommute(gens[i][1], gens[j][1]):
                return False
    n = len(gens[0][1])
    for mask in range(1, 1 << len(gens)):
        prod: tuple = (1, "I" * n)
        for i, g in enumerate(gens):
            if mask >> i & 1:
                prod = multiply(prod, g)
        if prod[1] == "I" * n:
            return False
    return True


def projector(gens: list[tuple[int, str]]) -> list[list[complex]]:
    """prod_i (I + g_i)/2, the projector onto the joint +1 eigenspace."""
    n = len(gens[0][1])
    p = identity(1 << n)
    for sign, word in gens:
        p = matmul(p, scale(0.5, add(identity(1 << n), scale(sign, pauli_matrix(word)))))
    return p


def code_dimension(gens: list[tuple[int, str]]) -> int:
    p = projector(gens)
    return round(sum(p[i][i] for i in range(len(p))).real)


def stabilizer_state(gens: list[tuple[int, str]]) -> list[complex]:
    """The state fixed by n independent commuting generators on n qubits (one column of the projector, normalized)."""
    p = projector(gens)
    j = max(range(len(p)), key=lambda c: abs(p[c][c]))
    col = [p[i][j] for i in range(len(p))]
    s = abs(p[j][j]) ** 0.5
    return [a / s for a in col]


def syndrome(gens: list[tuple[int, str]], error: str) -> tuple[int, ...]:
    """Bit i is 1 when the error anticommutes with generator i (the measured eigenvalue is -1)."""
    return tuple(1 if anticommute(g[1], error) else 0 for g in gens)


def stabilizer_state_count(n: int) -> int:
    """The number of n-qubit stabilizer states: 2^n prod_{k=1..n} (2^k + 1)."""
    r = 1 << n
    for k in range(1, n + 1):
        r *= (1 << k) + 1
    return r


def enumerate_stabilizer_states(n: int) -> int:
    """Count the states reached from |0...0> by H, S and CNOT, modulo global phase (breadth-first search)."""
    def key(v):
        j = next(i for i, a in enumerate(v) if abs(a) > 1e-9)
        ph = abs(v[j]) / v[j]
        return tuple((round((a * ph).real, 6), round((a * ph).imag, 6)) for a in v)

    start = basis_state(n, 0)
    seen = {key(start)}
    queue = deque([start])
    while queue:
        v = queue.popleft()
        nxt = []
        for q in range(n):
            nxt.append(apply_1q(v, H, q))
            nxt.append(apply_1q(v, S, q))
            for t in range(n):
                if t != q:
                    nxt.append(apply_cnot(v, q, t))
        for w in nxt:
            k = key(w)
            if k not in seen:
                seen.add(k)
                queue.append(w)
    return len(seen)
