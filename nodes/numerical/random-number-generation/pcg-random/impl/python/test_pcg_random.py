# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pcg-random/. The authors are listed in prov/0VZS5V.jsonl.

import random
from collections import Counter

import pytest

from pcg_random import (
    MASK64,
    MULT,
    lcg_advance,
    pcg32_bounded,
    pcg32_next,
    pcg32_seed,
    pcg32_stream,
    rotr32,
    xsh_rr,
)


def test_reference_demo_outputs() -> None:
    # pcg32-demo of the pcg-c-basic distribution, pcg32_srandom_r(&rng, 42, 54).
    assert pcg32_stream(42, 54, 6) == [
        0xA15C02B7, 0x7B47F409, 0xBA1D3330, 0x83D2F293, 0xBFA4784B, 0xCBED606E,
    ]


def test_reference_bounded_values() -> None:
    # Six calls of pcg32_boundedrand_r(&rng, 6) after the six outputs above,
    # from the reference code compiled and run.
    state, inc = pcg32_seed(42, 54)
    for _ in range(6):
        state, _ = pcg32_next(state, inc)
    rolls = []
    for _ in range(6):
        state, v = pcg32_bounded(state, inc, 6)
        rolls.append(v)
    assert rolls == [5, 3, 0, 2, 0, 1]


def test_trace_of_the_page() -> None:
    state, inc = pcg32_seed(42, 54)
    assert inc == 109 and state == 0x185706B82C2E03F8
    state, v = pcg32_next(state, inc)
    assert state == 0x2B47FED88766BB05 and v == 0xA15C02B7


def test_output_matches_general_xsh_rr() -> None:
    rng = random.Random(1)
    for _ in range(500):
        s = rng.getrandbits(64)
        assert pcg32_next(s, 1)[1] == xsh_rr(s, 64, 32)


def test_advance_equals_stepping() -> None:
    state, inc = pcg32_seed(7, 11)
    s = state
    for k in range(1, 300):
        s = (s * MULT + inc) & MASK64
        assert lcg_advance(state, k, MULT, inc) == s
    assert lcg_advance(state, 2**64, MULT, inc) == state
    assert lcg_advance(lcg_advance(state, 12345, MULT, inc), -12345, MULT, inc) == state


def test_full_period_of_small_lcg_and_uniform_output() -> None:
    # A 16-bit LCG with a = 1 mod 4 and c odd has period 2^16 (Hull-Dobell), and the
    # XSH RR 16/8 output takes every 8-bit value exactly 2^8 times over one period.
    a, c, mask = 12829, 47989, 0xFFFF
    assert a % 4 == 1 and c % 2 == 1
    x, counts, n = 1, Counter(), 0
    while True:
        counts[xsh_rr(x, 16, 8)] += 1
        x = (a * x + c) & mask
        n += 1
        if x == 1:
            break
    assert n == 1 << 16
    assert len(counts) == 256 and set(counts.values()) == {256}


def test_bad_lcg_parameters_shorten_the_period() -> None:
    mask = 0xFFFF
    for a, c in [(12831, 47989), (12829, 47990)]:  # a = 3 mod 4, or c even
        x, n = 1, 0
        while True:
            x = (a * x + c) & mask
            n += 1
            if x == 1 or n > 1 << 16:
                break
        assert x == 1 and n < 1 << 16  # odd a makes the map a bijection, so x returns


def test_low_state_bits_have_short_periods() -> None:
    # Bit k of the LCG state has period at most 2^(k+1); pcg32 discards the low 27 bits.
    state, inc = pcg32_seed(42, 54)
    xs = []
    for _ in range(64):
        xs.append(state)
        state = (state * MULT + inc) & MASK64
    for k in range(4):
        bits = [(x >> k) & 1 for x in xs]
        p = 2 ** (k + 1)
        assert all(bits[i] == bits[i + p] for i in range(64 - p))


def test_streams_are_scaled_copies() -> None:
    # With increments c and c', the map y = u x, u = c' / c mod 2^64, sends one LCG to the other.
    c1, c2 = 109, 2 * 1000 + 1
    u = c2 * pow(c1, -1, 2**64) % 2**64
    x = 0x123456789
    y = u * x % 2**64
    for _ in range(100):
        x = (x * MULT + c1) & MASK64
        y = (y * MULT + c2) & MASK64
        assert y == u * x % 2**64


def test_bounded_is_uniform() -> None:
    # Chi-square for 7 cells with 6 degrees of freedom: the 0.999 quantile is 22.46.
    state, inc = pcg32_seed(2024, 1)
    counts = [0] * 7
    for _ in range(14000):
        state, v = pcg32_bounded(state, inc, 7)
        counts[v] += 1
    chi2 = sum((c - 2000) ** 2 / 2000 for c in counts)
    assert chi2 < 22.46


def test_bounded_edge_cases() -> None:
    state, inc = pcg32_seed(1, 1)
    assert pcg32_bounded(state, inc, 1)[1] == 0
    with pytest.raises(ValueError):
        pcg32_bounded(state, inc, 0)
    assert 0 <= pcg32_bounded(state, inc, 2**32 - 1)[1] < 2**32 - 1


def test_rotation() -> None:
    assert rotr32(1, 1) == 0x80000000
    assert rotr32(0xDEADBEEF, 0) == 0xDEADBEEF
