# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/splitmix64/. The authors are listed in prov/V3VE7E.jsonl.

import random

import pytest

from splitmix64 import (
    GOLDEN_GAMMA,
    MASK64,
    mix64,
    seed_state,
    splitmix64_next,
    splitmix64_stream,
    unmix64,
)


def test_reference_outputs() -> None:
    # Values from the reference C code splitmix64.c of Vigna (prng.di.unimi.it).
    assert splitmix64_stream(1234567, 5) == [
        6457827717110365317,
        3203168211198807973,
        9817491932198370423,
        4593380528125082431,
        16408922859458223821,
    ]
    assert splitmix64_stream(0, 1) == [16294208416658607535]


def test_trace_of_the_page() -> None:
    assert splitmix64_stream(0, 3) == [
        0xE220A8397B1DCDAF, 0x6E789E6AA1B965F4, 0x06C45D188009454F,
    ]
    x, z = splitmix64_next(0)
    assert x == GOLDEN_GAMMA and z == 16294208416658607535


def test_mix_is_a_bijection() -> None:
    rng = random.Random(64)
    for z in [0, 1, MASK64, GOLDEN_GAMMA] + [rng.getrandbits(64) for _ in range(2000)]:
        assert unmix64(mix64(z)) == z
    assert mix64(0) == 0


def test_seed_zero_is_fine() -> None:
    out = splitmix64_stream(0, 100)
    assert len(set(out)) == 100
    assert all(0 <= v <= MASK64 for v in out)


def test_seed_state_fills_words() -> None:
    s = seed_state(1234567, 4)
    assert s == splitmix64_stream(1234567, 4)
    assert any(s)


def test_even_gamma_is_rejected() -> None:
    with pytest.raises(ValueError):
        splitmix64_stream(1, 1, gamma=2)


def small_mix(z: int, w: int, m1: int, m2: int) -> int:
    mask = (1 << w) - 1
    z = ((z ^ (z >> (w // 2 - 2))) * m1) & mask
    z = ((z ^ (z >> (w // 2 - 3))) * m2) & mask
    return z ^ (z >> (w // 2 - 1))


def test_full_period_permutation_on_small_words() -> None:
    # Scaled to 16 bits: an odd gamma gives period 2^16, and the outputs of one
    # period are a permutation of all 16-bit words.
    w = 16
    mask = (1 << w) - 1
    for gamma, m1, m2 in [(0x9E37, 0xBF59, 0x94D1), (1, 3, 5), (0x7F4B, 0x1CE5, 0x3111)]:
        x, seen, outs = 0x1234, set(), set()
        for _ in range(1 << w):
            x = (x + gamma) & mask
            seen.add(x)
            outs.add(small_mix(x, w, m1, m2))
        assert x == 0x1234
        assert len(seen) == 1 << w and len(outs) == 1 << w


def test_even_gamma_period_is_short() -> None:
    w, mask = 16, (1 << 16) - 1
    x, n = 5, 0
    while True:
        x = (x + 6) & mask
        n += 1
        if x == 5:
            break
    assert n == (1 << w) // 2


def test_bit_balance() -> None:
    # Each output bit is 1 about half the time: 20000 outputs, 4.5 standard deviations.
    out = splitmix64_stream(2024, 20000)
    for bit in range(64):
        ones = sum((v >> bit) & 1 for v in out)
        assert abs(ones - 10000) < 4.5 * 70.72
