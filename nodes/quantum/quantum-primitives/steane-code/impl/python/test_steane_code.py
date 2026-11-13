# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/steane-code/. The authors are listed in prov/QGYZM1.jsonl.

import itertools
import math
import random

from qsim import H, R2, S, apply_1q, apply_cnot, apply_pauli, close, inner
from steane_code import (GENERATORS, LOGICAL_X, LOGICAL_Z, N, ROWS, anticommute, code_basis, correct_general, decode,
                         dual_code, encode, hamming_code, in_span, measured_syndrome, syndrome, to_binary, transversal,
                         word)


def same_ray(u, v):
    return abs(abs(inner(u, v)) - 1) < 1e-9


def random_amps(rng):
    a = complex(rng.gauss(0, 1), rng.gauss(0, 1))
    b = complex(rng.gauss(0, 1), rng.gauss(0, 1))
    s = math.sqrt(abs(a) ** 2 + abs(b) ** 2)
    return a / s, b / s


SINGLE = ["I" * N] + [word({q: p}) for q in range(N) for p in "XYZ"]


def test_classical_codes() -> None:
    assert ROWS == [[3, 4, 5, 6], [1, 2, 5, 6], [0, 2, 4, 6]]  # positions 4-7, 2 3 6 7, 1 3 5 7
    ham = hamming_code()
    dual = dual_code()
    assert len(ham) == 16 and len(dual) == 8 and set(dual) <= set(ham)
    assert sorted(bin(c).count("1") for c in dual) == [0, 4, 4, 4, 4, 4, 4, 4]
    odd = sorted(set(ham) - set(dual))
    assert sorted({bin(c).count("1") for c in odd}) == [3, 7]


def test_encoder_and_codewords() -> None:
    zero, one = code_basis()
    assert close(encode(1, 0), zero) and close(encode(0, 1), one)
    for g in GENERATORS:
        assert close(apply_pauli(zero, g), zero) and close(apply_pauli(one, g), one)
    for g, h in itertools.combinations(GENERATORS, 2):
        assert not anticommute(g, h)
    assert close(apply_pauli(zero, LOGICAL_X), one)
    assert close(apply_pauli(one, LOGICAL_Z), [-a for a in one])


def test_every_single_qubit_pauli_error_is_corrected() -> None:
    rng = random.Random(1101)
    states = [encode(*random_amps(rng)) for _ in range(4)] + list(code_basis())
    for psi in states:
        for e in SINGLE:  # all 21 single-qubit Pauli errors and no error
            bad = apply_pauli(psi, e)
            s = measured_syndrome(bad)
            assert s == syndrome(e)
            assert same_ray(apply_pauli(bad, decode(s)), psi)
    # nondegenerate: 22 errors, 22 syndromes
    assert len({syndrome(e) for e in SINGLE}) == 22


def test_arbitrary_single_qubit_errors() -> None:
    rng = random.Random(1102)
    for _ in range(10):
        psi = encode(*random_amps(rng))
        k = [[complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(2)] for _ in range(2)]
        v = apply_1q(psi, k, rng.randrange(N))
        s = math.sqrt(inner(v, v).real)
        branches = correct_general([a / s for a in v])
        assert len(branches) <= 4 and abs(sum(p for p, _ in branches) - 1) < 1e-9
        for _, w in branches:
            assert same_ray(w, psi)


def test_knill_laflamme_conditions_with_c_identity() -> None:
    zero, one = code_basis()
    images = [(apply_pauli(zero, e), apply_pauli(one, e)) for e in SINGLE]
    for a in range(len(SINGLE)):
        for b in range(len(SINGLE)):
            g00 = inner(images[a][0], images[b][0])
            g11 = inner(images[a][1], images[b][1])
            g01 = inner(images[a][0], images[b][1])
            assert abs(g01) < 1e-9 and abs(g00 - g11) < 1e-9
            assert abs(g00 - (1 if a == b else 0)) < 1e-9


def test_distance_is_three() -> None:
    rows = [to_binary(g) for g in GENERATORS]
    small = ["I" * N] + [word(dict(zip(qs, ps))) for w in (1, 2) for qs in itertools.combinations(range(N), w)
                         for ps in itertools.product("XYZ", repeat=w)]
    assert len(small) == 211
    for e in small:
        if not any(syndrome(e)):
            assert e == "I" * N  # every stabilizer has weight at least 4
    xbar3 = word({0: "X", 1: "X", 2: "X"})  # positions 1, 2, 3: a Hamming codeword of weight 3
    assert not any(syndrome(xbar3)) and not in_span(to_binary(xbar3), rows)


def test_transversal_hadamard_and_phase() -> None:
    zero, one = code_basis()
    plus = [R2 * (a + b) for a, b in zip(zero, one)]
    minus = [R2 * (a - b) for a, b in zip(zero, one)]
    assert close(transversal(zero, H), plus) and close(transversal(one, H), minus)
    # S on all seven qubits multiplies |c> by i^weight(c): weights 0, 4 on |0_L>, 3, 7 on |1_L>
    assert close(transversal(zero, S), zero)
    assert close(transversal(one, S), [-1j * a for a in one])  # logical S^dagger


def test_transversal_cnot() -> None:
    zero, one = code_basis()

    def pair(hi, lo):  # block 1 on qubits 7..13 (control), block 0 on qubits 0..6 (target)
        return [a * b for a in hi for b in lo]

    for c, t in itertools.product((0, 1), repeat=2):
        v = pair((zero, one)[c], (zero, one)[t])
        for q in range(N):
            v = apply_cnot(v, N + q, q)
        assert close(v, pair((zero, one)[c], (zero, one)[c ^ t]))
