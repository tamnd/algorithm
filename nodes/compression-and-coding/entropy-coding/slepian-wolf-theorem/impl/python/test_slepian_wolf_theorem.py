# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/slepian-wolf-theorem/. The authors are listed in prov/VX919M.jsonl.

import math

from slepian_wolf_theorem import N, R_BITS, coset, decode, encode_x, joint_entropy_bits, syndrome

ERRORS = [0] + [1 << i for i in range(N)]


def test_syndrome_is_linear() -> None:
    for a in range(128):
        for b in range(128):
            assert syndrome(a ^ b) == syndrome(a) ^ syndrome(b)


def test_hamming_code_has_16_codewords_of_distance_3() -> None:
    code = coset(0)
    assert len(code) == 16
    dmin = min(bin(a ^ b).count("1") for a in code for b in code if a != b)
    assert dmin == 3
    # The weight distribution of the [7, 4, 3] Hamming code: 1, 7, 7, 1 at weights 0, 3, 4, 7.
    weights = sorted(bin(c).count("1") for c in code)
    assert [weights.count(w) for w in (0, 3, 4, 7)] == [1, 7, 7, 1]


def test_bins_partition_all_words() -> None:
    bins = [coset(s) for s in range(8)]
    assert all(len(b) == 16 for b in bins)
    assert sorted(x for b in bins for x in b) == list(range(128))


def test_decoding_is_always_correct() -> None:
    for x in range(128):
        s = encode_x(x)
        assert 0 <= s < 1 << R_BITS
        for e in ERRORS:
            assert decode(s, x ^ e) == x


def test_rates_meet_the_joint_entropy() -> None:
    hxy = joint_entropy_bits()
    assert math.isclose(hxy, 10.0)
    assert R_BITS + N == 10
    # H(Y) = 7 since Y is uniform, so H(X | Y) = 3 = R_BITS.
    assert math.isclose(hxy - 7, R_BITS)


def test_y_alone_cannot_find_x() -> None:
    # Without the syndrome, each y fits 8 different x. The syndrome picks one of them.
    for y in range(128):
        cands = [y ^ e for e in ERRORS]
        assert len(set(cands)) == 8
        assert len({syndrome(c) for c in cands}) == 8


def test_two_errors_are_not_corrected() -> None:
    bad = 0
    for x in range(128):
        for i in range(N):
            for j in range(i + 1, N):
                if decode(encode_x(x), x ^ (1 << i) ^ (1 << j)) != x:
                    bad += 1
    assert bad == 128 * 21
