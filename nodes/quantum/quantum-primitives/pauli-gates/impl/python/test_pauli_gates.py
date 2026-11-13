# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pauli-gates/. The authors are listed in prov/KXAV0B.jsonl.

import cmath
import itertools
import math
import random

from pauli_gates import (
    I, PAULI, PRODUCT, X, Y, Z, decompose, recompose, string_matrix, string_product, strings_commute, trace,
)
from qsim import apply_1q, basis_state, close, dagger, is_unitary, matmul, matvec, scale

R = math.sqrt(0.5)


def test_hermitian_unitary_involutions_with_trace_zero() -> None:
    for name in "XYZ":
        p = PAULI[name]
        assert p == dagger(p)
        assert is_unitary(p)
        assert matmul(p, p) == I
        assert trace(p) == 0


def test_eigenvalues_and_eigenvectors() -> None:
    eig = {
        "X": ([complex(R), complex(R)], [complex(R), complex(-R)]),
        "Y": ([complex(R), 1j * R], [complex(R), -1j * R]),
        "Z": ([1 + 0j, 0j], [0j, 1 + 0j]),
    }
    for name, (plus, minus) in eig.items():
        p = PAULI[name]
        assert close(matvec(p, plus), plus) and close(matvec(p, minus), [-a for a in minus])


def test_products_and_anticommutation() -> None:
    assert matmul(X, Y) == scale(1j, Z)
    assert matmul(Y, Z) == scale(1j, X)
    assert matmul(Z, X) == scale(1j, Y)
    assert matmul(matmul(X, Y), Z) == scale(1j, I)
    assert matmul(scale(1j, X), Z) == Y  # Y = i X Z
    for a, b in itertools.product("IXYZ", repeat=2):
        ph, c = PRODUCT[(a, b)]
        assert matmul(PAULI[a], PAULI[b]) == scale(ph, PAULI[c])
        ab, ba = matmul(PAULI[a], PAULI[b]), matmul(PAULI[b], PAULI[a])
        if a != b and "I" not in (a, b):
            assert ab == scale(-1, ba)  # anticommute
        else:
            assert ab == ba


def test_action_on_basis_states() -> None:
    for b in (0, 1):
        assert matvec(X, basis_state(1, b)) == basis_state(1, 1 - b)
        assert matvec(Z, basis_state(1, b)) == [(-1) ** b * a for a in basis_state(1, b)]
        assert matvec(Y, basis_state(1, b)) == [1j * (-1) ** b * a for a in basis_state(1, 1 - b)]
    # X on qubit j of a register flips bit j of the index
    for x in range(8):
        for j in range(3):
            assert apply_1q(basis_state(3, x), X, j) == basis_state(3, x ^ (1 << j))


def test_pauli_basis_and_decomposition() -> None:
    for a, b in itertools.product("IXYZ", repeat=2):
        assert trace(matmul(dagger(PAULI[a]), PAULI[b])) == (2 if a == b else 0)
    rng = random.Random(91)
    for _ in range(50):
        m = [[complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(2)] for _ in range(2)]
        assert close(recompose(decompose(m)), m)
        h = [[(m[i][j] + m[j][i].conjugate()) / 2 for j in range(2)] for i in range(2)]
        assert all(abs(c.imag) < 1e-12 for c in decompose(h).values())  # Hermitian: real coefficients
    # H = (X + Z) / sqrt 2
    assert close(recompose({"X": R, "Z": R}), [[R, R], [R, -R]])


def test_pauli_strings() -> None:
    # "XZ": X on qubit 1, Z on qubit 0, so |01> -> -|11>
    assert close(matvec(string_matrix("XZ"), basis_state(2, 1)), [-a for a in basis_state(2, 3)])
    strings = ["".join(s) for s in itertools.product("IXYZ", repeat=2)]
    mats = {s: string_matrix(s) for s in strings}
    for s, t in itertools.product(strings, repeat=2):  # 256 pairs
        st, ts = matmul(mats[s], mats[t]), matmul(mats[t], mats[s])
        assert (st == ts) == strings_commute(s, t)
        if not strings_commute(s, t):
            assert st == scale(-1, ts)
        ph, u = string_product(s, t)
        assert st == scale(ph, mats[u])
    assert strings_commute("XX", "ZZ") and not strings_commute("XI", "ZZ")


def test_the_pauli_group_has_16_elements() -> None:
    phases = (1, 1j, -1, -1j)
    group = {(ph, p) for ph in phases for p in "IXYZ"}
    for (pa, a), (pb, b) in itertools.product(group, repeat=2):
        ph, c = PRODUCT[(a, b)]
        prod = pa * pb * ph
        key = min(phases, key=lambda z: abs(z - prod))
        assert cmath.isclose(key, prod) and (key, c) in group
    assert len(group) == 16
    assert is_unitary(string_matrix("XYZ"))
