# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/convolutional-code/. The authors are listed in prov/F34YG7.jsonl.

import itertools
import random

from convolutional_code import (
    depuncture,
    encode,
    free_distance,
    gf2_gcd,
    is_catastrophic,
    octal_taps,
    puncture,
    rsc_encode,
    weight_spectrum,
)

# CCSDS 131.0-B-5, TM Synchronization and Channel Coding, Section 3.3 (basic
# convolutional code): rate 1/2, K = 7, G1 = 1111001 (171 octal), G2 = 1011011
# (133 octal), G1 symbol first, symbol inversion on the output path of G2.
CCSDS_G1, CCSDS_G2 = 0b1111001, 0b1011011
# IEEE 802.11, Clause 17 (OFDM PHY), convolutional encoder: g0 = 133 octal,
# g1 = 171 octal, output A (g0) before output B (g1), no inversion.
WIFI_G0, WIFI_G1 = octal_taps("133"), octal_taps("171")


def test_standard_parameters_agree() -> None:
    assert CCSDS_G1 == octal_taps("171") and CCSDS_G2 == octal_taps("133")
    assert (WIFI_G0, WIFI_G1) == (CCSDS_G2, CCSDS_G1)


def test_worked_example() -> None:
    assert encode([1, 0, 1, 1], [7, 5], 3) == [1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1]


def test_free_distance_known_codes() -> None:
    # Optimum rate 1/2 codes (Odenwalder tables, see Lin and Costello, Chapter 12).
    assert free_distance([7, 5], 3) == 5
    assert free_distance([octal_taps("15"), octal_taps("17")], 4) == 6
    assert free_distance([octal_taps("23"), octal_taps("35")], 5) == 7
    assert free_distance([octal_taps("53"), octal_taps("75")], 6) == 8
    assert free_distance([CCSDS_G1, CCSDS_G2], 7) == 10


def test_free_distance_against_brute_force() -> None:
    # Every first-event path of length at most L is a nonzero input that starts
    # with 1, then K - 1 zeros. Search all short inputs.
    for gens, k in [([7, 5], 3), ([octal_taps("15"), octal_taps("17")], 4)]:
        best = min(
            sum(encode((1,) + rest, gens, k))
            for length in range(0, 9)
            for rest in itertools.product((0, 1), repeat=length)
        )
        assert best == free_distance(gens, k)


def test_spectrum() -> None:
    # T(D, N) = D^5 N / (1 - 2 D N) for the (7, 5) code: A_d = 2^(d-5), B_d = (d - 4) 2^(d-5).
    spec = weight_spectrum([7, 5], 3, 10)
    for d in range(5, 11):
        assert spec[d] == (2 ** (d - 5), (d - 4) * 2 ** (d - 5))
    k7 = weight_spectrum([CCSDS_G1, CCSDS_G2], 7, 14)
    assert k7 == {10: (11, 36), 12: (38, 211), 14: (193, 1404)}


def test_linearity() -> None:
    rng = random.Random(5)
    for _ in range(200):
        a = [rng.randrange(2) for _ in range(12)]
        b = [rng.randrange(2) for _ in range(12)]
        s = [x ^ y for x, y in zip(a, b)]
        ca, cb, cs = (encode(v, [CCSDS_G1, CCSDS_G2], 7) for v in (a, b, s))
        assert cs == [x ^ y for x, y in zip(ca, cb)]


def test_catastrophic() -> None:
    assert gf2_gcd(0b11, 0b101) == 0b11  # 1 + D divides 1 + D^2
    assert is_catastrophic([0b110, 0b101], 3)  # 1 + D and 1 + D^2
    assert not is_catastrophic([7, 5], 3)
    assert not is_catastrophic([CCSDS_G1, CCSDS_G2], 7)
    # The all-ones input has infinite weight, but its output weight stays 3.
    for n in (10, 50, 200):
        out = encode([1] * n, [0b110, 0b101], 3, terminate=False)
        assert sum(out) == 3


def test_puncture_roundtrip() -> None:
    rng = random.Random(7)
    pattern = [[1, 1], [1, 0]]  # rate 2/3 from the rate 1/2 mother code
    for _ in range(100):
        c = encode([rng.randrange(2) for _ in range(rng.randrange(1, 30))], [7, 5], 3)
        p = puncture(c, pattern)
        assert len(p) == len(c) - len(c) // 4 - (1 if len(c) % 4 == 3 else 0)
        back = depuncture([float(x) for x in p], pattern, len(c), fill=-1.0)
        for i, x in enumerate(back):
            assert x == -1.0 or x == c[i]


def test_rsc_same_code_as_feedforward() -> None:
    # (1, 5/7) RSC and the (7, 5) feedforward encoder generate the same code:
    # input u(D) to the feedforward encoder equals 7(D) times the RSC input.
    rng = random.Random(9)
    for _ in range(200):
        x = [rng.randrange(2) for _ in range(10)] + [0, 0]
        y = rsc_encode(x, 7, 5, 3)
        sysbits = [a for a, _ in y]
        assert sysbits == x
        # the feedforward input is the register sequence a of the RSC encoder
        state, a_seq = 0, []
        for u in x:
            a = (u + bin(7 & state).count("1")) & 1
            a_seq.append(a)
            state = ((a << 2) | state) >> 1
        ff = encode(a_seq, [7, 5], 3, terminate=False)
        assert ff[0::2] == sysbits and ff[1::2] == [p for _, p in y]
