# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/clifford-group/. The authors are listed in prov/5V9XE0.jsonl.

import itertools
import random

from clifford_group import (clifford_group_order, commute, conjugate, conjugate_gate, enumerate_tableaux, from_word,
                            generators, tableau, to_word)
from qsim import H, S, T, X, Z, apply_1q, apply_cnot, circuit_matrix, close, dagger, matmul, pauli_matrix, scale


def run_gate(state, g):
    if g[0] == "H":
        return apply_1q(state, H, g[1])
    if g[0] == "S":
        return apply_1q(state, S, g[1])
    return apply_cnot(state, g[1], g[2])


def circuit_unitary(circuit, n):
    def run(v):
        for g in circuit:
            v = run_gate(v, g)
        return v
    return circuit_matrix(n, run)


def pauli_of(p, n):
    phase, word = to_word(p, n)
    return scale(phase, pauli_matrix(word))


def words(n):
    return ["".join(w) for w in itertools.product("IXYZ", repeat=n)]


def test_word_round_trip() -> None:
    for n in (1, 2, 3):
        for w in words(n):
            for sign in (1, -1):
                assert to_word(from_word(w, sign), n) == (sign, w)
    assert from_word("Y") == (1, 1, 1)  # Y = i X Z


def test_one_qubit_table() -> None:
    expect = {
        ("H", "X"): (1, "Z"), ("H", "Z"): (1, "X"), ("H", "Y"): (-1, "Y"),
        ("S", "X"): (1, "Y"), ("S", "Y"): (-1, "X"), ("S", "Z"): (1, "Z"),
    }
    for (g, w), v in expect.items():
        assert to_word(conjugate_gate((g, 0), from_word(w)), 1) == v


def test_cnot_table() -> None:
    # control qubit 1 (left letter), target qubit 0 (right letter)
    g = ("CNOT", 1, 0)
    expect = {"XI": "XX", "IX": "IX", "ZI": "ZI", "IZ": "ZZ", "YI": "YX", "IY": "ZY", "XX": "XI", "ZZ": "IZ"}
    for w, v in expect.items():
        assert to_word(conjugate_gate(g, from_word(w)), 2) == (1, v)
    assert to_word(conjugate_gate(g, from_word("XZ")), 2) == (-1, "YY")


def test_every_gate_against_matrices() -> None:
    n = 3
    for g in generators(n):
        u = circuit_unitary([g], n)
        for w in words(n):
            p = from_word(w)
            lhs = matmul(matmul(u, pauli_of(p, n)), dagger(u))
            assert close(lhs, pauli_of(conjugate_gate(g, p), n))


def test_random_circuits_against_matrices() -> None:
    rng = random.Random(6061)
    n = 3
    gens = generators(n)
    for _ in range(25):
        circuit = [rng.choice(gens) for _ in range(rng.randrange(1, 30))]
        u = circuit_unitary(circuit, n)
        for _ in range(6):
            w = "".join(rng.choice("IXYZ") for _ in range(n))
            p = from_word(w, rng.choice((1, -1)))
            lhs = matmul(matmul(u, pauli_of(p, n)), dagger(u))
            assert close(lhs, pauli_of(conjugate(circuit, p), n))


def test_commutation_is_preserved() -> None:
    rng = random.Random(6062)
    n = 4
    gens = generators(n)
    for _ in range(40):
        circuit = [rng.choice(gens) for _ in range(25)]
        t = tableau(circuit, n)
        for i in range(2 * n):
            for j in range(2 * n):
                # X_a and Z_b anticommute exactly when a = b
                assert commute(t[i], t[j]) == (i // 2 != j // 2 or i % 2 == j % 2)
            assert to_word(t[i], n)[0] in (1, -1)  # images are Hermitian


def test_group_orders() -> None:
    assert [clifford_group_order(n) for n in (1, 2, 3)] == [24, 11520, 92897280]
    one = enumerate_tableaux(1)
    assert len(one) == 24
    assert max(len(c) for c in one.values()) == 6  # every one-qubit Clifford is a word of at most 6 gates H and S
    two = enumerate_tableaux(2)
    assert len(two) == 11520


def test_one_qubit_group_with_phases_has_192_elements() -> None:
    def key(m):
        return tuple(round(v.real, 9) + 1j * round(v.imag, 9) for row in m for v in row)

    start = [[1 + 0j, 0j], [0j, 1 + 0j]]
    seen = {key(start): start}
    frontier = [start]
    while frontier:
        nxt = []
        for m in frontier:
            for g in (H, S):
                p = matmul(g, m)
                if key(p) not in seen:
                    seen[key(p)] = p
                    nxt.append(p)
        frontier = nxt
    assert len(seen) == 192
    # modulo the eight phases e^(i pi k/4) these are the 24 Clifford elements
    assert len(seen) // 8 == 24


def test_t_gate_is_not_clifford() -> None:
    txt = matmul(matmul(T, X), dagger(T))
    # T X T^dagger = (X + Y)/sqrt(2): two Pauli coefficients are nonzero
    coeffs = [sum(pauli_matrix(w)[i][j] * txt[j][i] for i in range(2) for j in range(2)) / 2 for w in "IXYZ"]
    assert sum(1 for c in coeffs if abs(c) > 1e-9) == 2
    assert close(matmul(matmul(T, Z), dagger(T)), Z)
