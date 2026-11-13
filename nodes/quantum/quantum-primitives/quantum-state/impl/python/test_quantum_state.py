# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quantum-state/. The authors are listed in prov/WTP45P.jsonl.

import cmath
import math
import random

import pytest

from qsim import apply_1q, basis_state, inner, norm
from quantum_state import (
    amplitude, dimension, from_amplitudes, ghz, index_of, ket_label, nielsen_chuang_qubit, normalize, overlap,
    qubit_value, real_parameters, same_state, support,
)

X = [[0j, 1 + 0j], [1 + 0j, 0j]]


def test_labels_and_indices() -> None:
    assert ket_label(3, 6) == "|110>"
    assert index_of("110") == 6 and index_of("001") == 1
    assert [qubit_value(6, j) for j in range(3)] == [0, 1, 1]
    for n in range(1, 6):
        for x in range(dimension(n)):
            assert index_of(ket_label(n, x)[1:-1]) == x


def test_qubit_order_matches_the_simulator() -> None:
    # X on qubit 0 flips the rightmost symbol, X on qubit 2 flips the leftmost one.
    s = basis_state(3, index_of("110"))
    assert apply_1q(s, X, 0) == basis_state(3, index_of("111"))
    assert apply_1q(s, X, 2) == basis_state(3, index_of("010"))
    for n in range(1, 5):
        for x in range(dimension(n)):
            for j in range(n):
                assert apply_1q(basis_state(n, x), X, j) == basis_state(n, x ^ (1 << j))


def test_nielsen_chuang_numbering() -> None:
    # In "abc", Nielsen and Chuang call a qubit 1; here it is qubit 2.
    assert [nielsen_chuang_qubit(3, j) for j in (2, 1, 0)] == [1, 2, 3]


def test_dimension_and_parameters() -> None:
    assert [dimension(n) for n in range(5)] == [1, 2, 4, 8, 16]
    assert real_parameters(1) == 2 and real_parameters(2) == 6 and real_parameters(3) == 14


def test_worked_two_qubit_state() -> None:
    s = from_amplitudes(2, {"00": 0.5, "01": 0.5j, "10": -0.5, "11": -0.5j})
    assert amplitude(s, "01") == 0.5j and s[1] == 0.5j
    assert sum(abs(a) ** 2 for a in s) == 1.0
    assert support(s) == ["|00>", "|01>", "|10>", "|11>"]
    with pytest.raises(ValueError):
        from_amplitudes(2, {"00": 1, "11": 1})


def test_ghz_and_overlaps() -> None:
    g = ghz(3)
    assert support(g) == ["|000>", "|111>"]
    assert abs(overlap(g, basis_state(3, 0)) - 0.5) < 1e-12
    assert overlap(basis_state(3, 2), basis_state(3, 5)) == 0
    rng = random.Random(7)
    for _ in range(20):
        v = normalize([complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(8)])
        assert abs(norm(v) - 1) < 1e-12
        g = cmath.exp(1j * rng.uniform(0, 2 * math.pi))
        w = [g * a for a in v]
        # a different phase on each amplitude gives a different state in general
        u = [cmath.exp(1j * k) * a for k, a in enumerate(v)]
        assert not same_state(v, u)
        assert same_state(v, w)
        assert abs(inner(v, w)) > 1 - 1e-12
    assert not same_state(ghz(2), [math.sqrt(0.5), 0, 0, -math.sqrt(0.5)])
