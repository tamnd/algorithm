# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/turbo-code/. The authors are listed in prov/NXDXWC.jsonl.

import random

from turbo_code import (
    LTE_QPP,
    ccsds_permutation,
    codeword_weight,
    min_weight_two_inputs,
    puncture_half,
    qpp_interleaver,
    rsc_parity,
    turbo_encode,
)

# 3GPP TS 36.212, Section 5.1.3.2.1: G(D) = [1, g1(D)/g0(D)],
# g0(D) = 1 + D^2 + D^3, g1(D) = 1 + D + D^3 (taps D^0 .. D^3 left to right).
LTE_FB, LTE_FF = 0b1011, 0b1101
# CCSDS 131.0-B-5, Section 6.3 h): backward G0 = 10011, forward G1 = 11011.
CCSDS_FB, CCSDS_FF = 0b10011, 0b11011


def test_worked_example() -> None:
    e = turbo_encode([1, 0, 1, 1, 0, 0, 1, 0], [3, 6, 1, 4, 7, 2, 5, 0], 7, 5, 3)
    assert e["par1"] == [1, 1, 0, 0, 1, 0, 0, 0]
    assert e["par2"] == [1, 0, 0, 1, 1, 1, 0, 1]
    assert e["tail1"] == [(1, 0), (1, 1)]
    assert len(puncture_half(e)) == 2 * 8 + 8


def test_qpp_tables_are_permutations() -> None:
    assert LTE_QPP[40] == (3, 10)
    for size, (f1, f2) in LTE_QPP.items():
        p = qpp_interleaver(size, f1, f2)
        assert sorted(p) == list(range(size))
    assert qpp_interleaver(40, 3, 10)[:4] == [0, 13, 6, 19]


def test_ccsds_permutation() -> None:
    for k in (1784, 3568, 7136, 8920):  # Table 6-1
        p = ccsds_permutation(k)
        assert sorted(p) == list(range(1, k + 1))


def test_recursive_encoder_needs_weight_two() -> None:
    # A weight 1 input never returns an RSC encoder to state 0 by itself.
    for n in (10, 30):
        par, _ = rsc_parity([1] + [0] * (n - 1), 7, 5, 3, terminate=False)
        assert sum(par) >= n // 3 * 2
    # 1 + D^3 is a multiple of 1 + D + D^2, so the parity is finite: 1 1 1 1.
    par, tail = rsc_parity([1, 0, 0, 1, 0, 0, 0, 0], 7, 5, 3)
    assert par == [1, 1, 1, 1, 0, 0, 0, 0] and tail == [(0, 0), (0, 0)]


def test_identity_interleaver_gives_weight_ten_words() -> None:
    size = 30
    ident = list(range(size))
    for j in range(size - 6):
        u = [0] * size
        u[j] = u[j + 3] = 1
        assert codeword_weight(u, ident, 7, 5, 3) == 10


def test_min_weight_two() -> None:
    w, _ = min_weight_two_inputs(qpp_interleaver(40, 3, 10), 7, 5, 3)
    assert w == 9
    w, _ = min_weight_two_inputs(list(range(40)), 7, 5, 3)
    assert w == 8


def test_linearity_and_termination() -> None:
    rng = random.Random(6)
    perm = qpp_interleaver(64, 7, 16)
    for fb, ff, k in ((7, 5, 3), (LTE_FB, LTE_FF, 4), (CCSDS_FB, CCSDS_FF, 5)):
        for _ in range(100):
            a = [rng.randrange(2) for _ in range(64)]
            b = [rng.randrange(2) for _ in range(64)]
            s = [x ^ y for x, y in zip(a, b)]
            ea, eb, es = (turbo_encode(v, perm, fb, ff, k) for v in (a, b, s))
            for key in ("sys", "par1", "par2"):
                assert es[key] == [x ^ y for x, y in zip(ea[key], eb[key])]
            # the tail drives the register to zero: re-run with the tail inputs
            state = 0
            for u in a + [t for t, _ in ea["tail1"]]:
                x = (u + bin(fb & state).count("1")) & 1
                state = ((x << (k - 1)) | state) >> 1
            assert state == 0
