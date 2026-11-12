# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bit-flipping-decoding/. The authors are listed in prov/8C2WTA.jsonl.

import math
import random

from bit_flipping_decoding import (
    bit_flip_decode,
    gallager_a,
    gallager_a_de,
    gallager_a_threshold,
    gallager_b,
    gallager_b_de,
    weighted_bit_flip,
)

# Bazzi, Richardson and Urbanke, IEEE Trans. Inf. Theory 50(9), 2004: the
# threshold of algorithm A on the (3, 6) ensemble over the BSC is about 0.0394.
CITED_A_36 = 0.0394


def array_code(p, j):
    """The array LDPC code: j block rows of p x p circulants, block (a, b) is
    the permutation P^(a b). Column weight j, row weight p, length p^2."""
    n = p * p
    h = []
    for a in range(j):
        for r in range(p):
            row = [0] * n
            for b in range(p):
                row[b * p + (r + a * b) % p] = 1
            h.append(row)
    return h


H = array_code(7, 3)
N = 49


def test_array_code_has_no_four_cycles() -> None:
    cols = [{i for i in range(len(H)) if H[i][j]} for j in range(N)]
    assert all(len(c) == 3 for c in cols)
    assert all(len(cols[a] & cols[b]) <= 1 for a in range(N) for b in range(a + 1, N))


def test_example_and_codeword_fixed_point() -> None:
    word, it, ok = bit_flip_decode(H, [0] * N, 5)
    assert word == [0] * N and it == 0 and ok
    e = [0] * N
    e[10] = 1
    word, it, ok = bit_flip_decode(H, e, 5)
    # Bit 10 sits in 3 unsatisfied checks; any other bit shares at most one of them.
    assert word == [0] * N and it == 1 and ok


def test_all_single_and_double_errors() -> None:
    decoders = (
        lambda w: bit_flip_decode(H, w, 10)[0],
        lambda w: gallager_a(H, w, 10)[0],
        lambda w: gallager_b(H, w, 10, 2)[0],
    )
    for f in decoders:
        for j1 in range(N):
            assert f([int(k == j1) for k in range(N)]) == [0] * N
            for j2 in range(j1 + 1, N):
                assert f([int(k in (j1, j2)) for k in range(N)]) == [0] * N


def test_weighted_rule_uses_reliability() -> None:
    # With |y| all equal the weights carry no data: singles are still fixed,
    # but for two errors in one check a correct bit can tie with them.
    for j in range(N):
        y = [1.0] * N
        y[j] = -1.0
        assert weighted_bit_flip(H, y, 10)[0] == [0] * N
    ties = 0
    for j1 in range(N):
        for j2 in range(j1 + 1, N):
            y = [1.0] * N
            y[j1] = y[j2] = -1.0
            ties += weighted_bit_flip(H, y, 10)[0] != [0] * N
            # When the wrong samples are weak, the weights point at them.
            y[j1] = y[j2] = -0.2
            assert weighted_bit_flip(H, y, 10)[0] == [0] * N
    assert ties == 196


def test_gallager_a_threshold() -> None:
    thr = gallager_a_threshold(3, 6)
    assert abs(thr - CITED_A_36) < 1e-4
    assert gallager_a_de(0.039, 3, 6, 5000) < 1e-12
    assert gallager_a_de(0.040, 3, 6, 5000) > 0.2
    # With dv = 3, algorithm B with b = 2 is algorithm A.
    for p in (0.01, 0.03, 0.05):
        assert abs(gallager_b_de(p, 3, 6, 2, 50) - gallager_a_de(p, 3, 6, 50)) < 1e-15


def test_monte_carlo() -> None:
    rng = random.Random(1)
    raw = flip = alg_a = 0
    for _ in range(200):
        w = [int(rng.random() < 0.02) for _ in range(N)]
        raw += sum(w)
        flip += sum(bit_flip_decode(H, w, 20)[0])
        alg_a += sum(gallager_a(H, w, 20)[0])
    assert flip < raw and alg_a < raw
    rng = random.Random(2)
    rate = 1 - 19 / 49  # H has rank 3 p - 2 = 19
    s = math.sqrt(1 / (2 * rate * 10 ** (4.0 / 10)))
    flip = weighted = 0
    for _ in range(200):
        y = [1 + rng.gauss(0, s) for _ in range(N)]
        flip += sum(bit_flip_decode(H, [0 if v >= 0 else 1 for v in y], 20)[0])
        weighted += sum(weighted_bit_flip(H, y, 20)[0])
    assert weighted < flip
