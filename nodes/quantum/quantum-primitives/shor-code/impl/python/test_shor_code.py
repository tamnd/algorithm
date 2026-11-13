# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shor-code/. The authors are listed in prov/MXZFJW.jsonl.

import itertools
import math
import random

from qsim import apply_1q, apply_pauli, close, inner
from shor_code import (GENERATORS, LOGICAL_X, LOGICAL_Z, N, anticommute, code_basis, correct_general, decode, encode,
                       in_span, measured_syndrome, syndrome, to_binary, word)


def same_ray(u, v):
    return abs(abs(inner(u, v)) - 1) < 1e-9


def random_amps(rng):
    a = complex(rng.gauss(0, 1), rng.gauss(0, 1))
    b = complex(rng.gauss(0, 1), rng.gauss(0, 1))
    s = math.sqrt(abs(a) ** 2 + abs(b) ** 2)
    return a / s, b / s


SINGLE = ["I" * N] + [word({q: p}) for q in range(N) for p in "XYZ"]


def test_encoder_matches_definition() -> None:
    zero, one = code_basis()
    assert close(encode(1, 0), zero) and close(encode(0, 1), one)
    assert abs(inner(zero, one)) < 1e-12 and abs(inner(zero, zero) - 1) < 1e-12


def test_generators_fix_the_code_and_logicals_act() -> None:
    zero, one = code_basis()
    for g in GENERATORS:
        assert close(apply_pauli(zero, g), zero) and close(apply_pauli(one, g), one)
    for g, h in itertools.combinations(GENERATORS, 2):
        assert not anticommute(g, h)
    assert close(apply_pauli(zero, LOGICAL_X), one) and close(apply_pauli(one, LOGICAL_X), zero)
    assert close(apply_pauli(zero, LOGICAL_Z), zero) and close(apply_pauli(one, LOGICAL_Z), [-a for a in one])


def test_every_single_qubit_pauli_error_is_corrected() -> None:
    rng = random.Random(9091)
    states = [encode(*random_amps(rng)) for _ in range(3)] + [encode(1, 0), encode(0, 1)]
    for psi in states:
        for e in SINGLE:  # all 27 single-qubit Pauli errors and no error
            bad = apply_pauli(psi, e)
            s = measured_syndrome(bad)
            assert s == syndrome(e)
            fixed = apply_pauli(bad, decode(s))
            assert same_ray(fixed, psi)


def test_syndromes_are_degenerate() -> None:
    # 28 errors but only 22 syndromes: Z_a, Z_b, Z_c in one block share a syndrome
    syn = {}
    for e in SINGLE:
        syn.setdefault(syndrome(e), []).append(e)
    assert len(syn) == 22
    shared = [v for v in syn.values() if len(v) > 1]
    assert len(shared) == 3 and all(len(v) == 3 and all(set(w) <= {"I", "Z"} for w in v) for v in shared)


def test_arbitrary_single_qubit_errors() -> None:
    rng = random.Random(9092)
    for _ in range(6):
        psi = encode(*random_amps(rng))
        q = rng.randrange(N)
        # a random 2 x 2 matrix: not unitary, not small
        k = [[complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(2)] for _ in range(2)]
        v = apply_1q(psi, k, q)
        s = math.sqrt(inner(v, v).real)
        branches = correct_general([a / s for a in v], q)
        assert abs(sum(p for p, _ in branches) - 1) < 1e-9
        for _, w in branches:
            assert same_ray(w, psi)


def test_knill_laflamme_conditions_hold_and_c_is_not_diagonal() -> None:
    zero, one = code_basis()
    images = [(apply_pauli(zero, e), apply_pauli(one, e)) for e in SINGLE]
    m = len(SINGLE)
    c = [[0j] * m for _ in range(m)]
    for a in range(m):
        for b in range(m):
            g00 = inner(images[a][0], images[b][0])
            g11 = inner(images[a][1], images[b][1])
            g01 = inner(images[a][0], images[b][1])
            g10 = inner(images[a][1], images[b][0])
            assert abs(g01) < 1e-9 and abs(g10) < 1e-9 and abs(g00 - g11) < 1e-9
            c[a][b] = g00
    z0, z1 = SINGLE.index(word({0: "Z"})), SINGLE.index(word({1: "Z"}))
    assert abs(c[z0][z1] - 1) < 1e-9  # Z_0 Z_1 is a stabilizer: a degenerate code
    off = sum(1 for a in range(m) for b in range(m) if a != b and abs(c[a][b]) > 1e-9)
    assert off == 18  # the 3 x 3 blocks of Z errors in each block, off the diagonal


def all_paulis_of_weight_at_most(t):
    out = ["I" * N]
    for w in range(1, t + 1):
        for qs in itertools.combinations(range(N), w):
            for ps in itertools.product("XYZ", repeat=w):
                out.append(word(dict(zip(qs, ps))))
    return out


def test_distance_is_three() -> None:
    rows = [to_binary(g) for g in GENERATORS]
    small = all_paulis_of_weight_at_most(2)
    assert len(small) == 352
    for e in small:
        if not any(syndrome(e)):
            assert in_span(to_binary(e), rows)  # undetected only when it is a stabilizer
    # a weight-3 logical operator exists
    assert not any(syndrome(LOGICAL_X)) and not in_span(to_binary(LOGICAL_X), rows)


def test_two_x_errors_in_one_block_fail() -> None:
    psi = encode(0.6, 0.8)
    bad = apply_pauli(psi, word({0: "X", 1: "X"}))
    fixed = apply_pauli(bad, decode(measured_syndrome(bad)))
    assert same_ray(fixed, apply_pauli(psi, word({0: "X", 1: "X", 2: "X"})))
    assert not same_ray(fixed, psi)
