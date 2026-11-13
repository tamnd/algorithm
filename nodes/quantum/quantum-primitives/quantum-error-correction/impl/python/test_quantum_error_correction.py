# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quantum-error-correction/. The authors are listed in prov/BBMCQ5.jsonl.

import cmath
import math
import random

from qsim import X, apply_1q, apply_pauli
from quantum_error_correction import (bit_flip_code, bit_flip_table, correct, encode, kl_matrix, measure_syndrome,
                                      pauli_error, phase_flip_code, quantum_hamming_ok, same_ray)


def random_amps(rng):
    a = complex(rng.gauss(0, 1), rng.gauss(0, 1))
    b = complex(rng.gauss(0, 1), rng.gauss(0, 1))
    s = math.sqrt(abs(a) ** 2 + abs(b) ** 2)
    return [a / s, b / s]


def one_qubit(word_letter, q, n=3):
    return "I" * (n - 1 - q) + word_letter + "I" * q


def test_bit_flip_code_meets_knill_laflamme_for_x_errors() -> None:
    basis, _ = bit_flip_code()
    errors = [pauli_error(w) for w in ("III", "IIX", "IXI", "XII")]
    c = kl_matrix(basis, errors)
    assert c is not None
    # nondegenerate: the four errors map the code to orthogonal spaces, so c is the identity
    for a in range(4):
        for b in range(4):
            assert abs(c[a][b] - (1 if a == b else 0)) < 1e-12


def test_a_phase_error_violates_knill_laflamme() -> None:
    basis, _ = bit_flip_code()
    # <0_L|Z_0|0_L> = 1 but <1_L|Z_0|1_L> = -1: Z_0 acts on the code as a logical Z
    assert kl_matrix(basis, [pauli_error("III"), pauli_error("IIZ")]) is None
    # the set {X_0, Z_0} alone is correctable (X_0 Z_0 is a Y error, which leaves the code),
    # but not together with "no error"
    assert kl_matrix(basis, [pauli_error("IIX"), pauli_error("IIZ")]) is not None
    assert kl_matrix(basis, [pauli_error("III"), pauli_error("IIX"), pauli_error("IIZ")]) is None


def test_phase_flip_code_is_the_bit_flip_code_in_the_hadamard_basis() -> None:
    basis, _ = phase_flip_code()
    assert kl_matrix(basis, [pauli_error(w) for w in ("III", "IIZ", "IZI", "ZII")]) is not None
    assert kl_matrix(basis, [pauli_error("III"), pauli_error("IIX")]) is None


def test_every_single_x_error_is_corrected() -> None:
    rng = random.Random(8081)
    basis, gens = bit_flip_code()
    table = bit_flip_table()
    for _ in range(20):
        psi = encode(basis, random_amps(rng))
        for w in ("III", "IIX", "IXI", "XII"):
            branches = correct(apply_pauli(psi, w), gens, table)
            assert len(branches) == 1  # a Pauli error gives one syndrome with certainty
            p, v = branches[0]
            assert abs(p - 1) < 1e-9 and same_ray(v, psi)


def test_two_x_errors_cause_a_logical_error() -> None:
    basis, gens = bit_flip_code()
    psi = encode(basis, [0.6, 0.8])
    (p, v), = correct(apply_pauli(psi, "IXX"), gens, bit_flip_table())
    assert same_ray(v, apply_pauli(psi, "XXX"))  # the decoder applied X_2: logical X
    assert not same_ray(v, psi)


def test_discretization_continuous_rotation() -> None:
    # exp(-i theta X_q) = cos(theta) I - i sin(theta) X_q: a superposition of "no error" and "X error"
    rng = random.Random(8082)
    basis, gens = bit_flip_code()
    table = bit_flip_table()
    for _ in range(30):
        psi = encode(basis, random_amps(rng))
        q = rng.randrange(3)
        th = rng.uniform(0, math.pi)
        u = [[math.cos(th) + 0j, -1j * math.sin(th)], [-1j * math.sin(th), math.cos(th) + 0j]]
        branches = correct(apply_1q(psi, u, q), gens, table)
        assert abs(sum(p for p, _ in branches) - 1) < 1e-9
        for p, v in branches:
            assert same_ray(v, psi)
        # the syndrome outcome is random, with probabilities cos^2 and sin^2
        probs = sorted(p for p, _ in branches)
        assert abs(probs[-1] - max(math.cos(th) ** 2, math.sin(th) ** 2)) < 1e-9


def test_discretization_non_unitary_error() -> None:
    # any Kraus operator a I + b X on one qubit is corrected, for any complex a, b
    rng = random.Random(8083)
    basis, gens = bit_flip_code()
    table = bit_flip_table()
    for _ in range(30):
        psi = encode(basis, random_amps(rng))
        a = complex(rng.gauss(0, 1), rng.gauss(0, 1))
        b = complex(rng.gauss(0, 1), rng.gauss(0, 1))
        k = [[a, b], [b, a]]  # a I + b X
        v = apply_1q(psi, k, rng.randrange(3))
        s = math.sqrt(sum(abs(t) ** 2 for t in v))
        for _, w in correct([t / s for t in v], gens, table):
            assert same_ray(w, psi)


def test_knill_laflamme_is_linear_in_the_errors() -> None:
    rng = random.Random(8084)
    basis, _ = bit_flip_code()
    paulis = ["III", "IIX", "IXI", "XII"]
    combos = []
    for _ in range(5):
        cs = [complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in paulis]

        def e(v, cs=cs):
            out = [0j] * len(v)
            for c, w in zip(cs, paulis):
                for i, t in enumerate(apply_pauli(v, w)):
                    out[i] += c * t
            return out
        combos.append(e)
    assert kl_matrix(basis, combos) is not None


def test_syndrome_reveals_nothing_about_the_data() -> None:
    rng = random.Random(8085)
    basis, gens = bit_flip_code()
    q, th = 1, 0.7
    u = [[cmath.cos(th), -1j * cmath.sin(th)], [-1j * cmath.sin(th), cmath.cos(th)]]
    ref = None
    for _ in range(10):
        psi = encode(basis, random_amps(rng))
        probs = {s: round(p, 9) for s, (p, _) in measure_syndrome(apply_1q(psi, u, q), gens).items()}
        ref = ref or probs
        assert probs == ref


def test_quantum_hamming_bound() -> None:
    # one logical qubit, any single-qubit error: n = 5 is the smallest length
    assert [n for n in range(1, 10) if quantum_hamming_ok(n, 1, 1)][0] == 5
    assert quantum_hamming_ok(5, 1, 1) and 2 ** 4 == 1 + 3 * 5  # the five-qubit code is perfect
    assert not quantum_hamming_ok(3, 1, 1)
    assert X[0][1] == 1  # qsim's X is the bit flip
