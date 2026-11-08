# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/jump-ahead/. The authors are listed in prov/CRH15P.jsonl.

import random

import pytest

from jump_ahead import (
    berlekamp_massey_gf2,
    f2_jump,
    f2_jump_by_polynomial,
    gf2_mulmod,
    gf2_xpow_mod,
    lcg_jump,
    lcg_jump_coefficients,
    leapfrog_parameters,
    output_bits,
    xorshift32_step,
    xoshiro256_step,
)

MMIX_A = 6364136223846793005
MMIX_C = 1442695040888963407

# Published jump constants of xoshiro256 (Blackman and Vigna, xoshiro256starstar.c).
XOSHIRO256_JUMP = [0x180EC6D33CFD0ABA, 0xD5A61266F0C9392C, 0xA9582618E03FC9AA, 0x39ABDC4529B1661C]
XOSHIRO256_LONG_JUMP = [0x76E15D3EFEFDCBBF, 0xC5004E441C522FB3, 0x77710069854EE241, 0x39109BB02ACBE635]


def walk(m, a, c, s, n):
    for _ in range(n):
        s = (a * s + c) % m
    return s


def pack(words):
    return sum(w << (64 * i) for i, w in enumerate(words))


def test_minstd_check_value():
    # Park and Miller: 10000 steps of 16807 s mod 2^31 - 1 from seed 1.
    assert lcg_jump(2**31 - 1, 16807, 0, 1, 10000) == 1043618065


def test_numerical_recipes_quick_generator():
    outs = [lcg_jump(2**32, 1664525, 1013904223, 0, n) for n in range(1, 5)]
    assert outs == [1013904223, 1196435762, 3519870697, 2868466484]


def test_lcg_jump_matches_walk_small_parameters():
    rng = random.Random(1)
    for _ in range(300):
        m = rng.randint(1, 200)
        a, c, s = rng.randrange(m), rng.randrange(m), rng.randrange(m)
        n = rng.randint(0, 300)
        assert lcg_jump(m, a, c, s, n) == walk(m, a, c, s, n)


def test_lcg_jump_zero_is_identity_and_composition():
    m = 2**64
    assert lcg_jump_coefficients(m, MMIX_A, MMIX_C, 0) == (1, 0)
    s = m - 1  # largest word value
    for n1, n2 in [(1, 1), (123, 456), (2**40, 2**41 + 7)]:
        once = lcg_jump(m, MMIX_A, MMIX_C, s, n1 + n2)
        twice = lcg_jump(m, MMIX_A, MMIX_C, lcg_jump(m, MMIX_A, MMIX_C, s, n1), n2)
        assert once == twice


def test_lcg_full_period_jump_returns_to_start():
    # Hull-Dobell conditions hold, so the period is the modulus.
    for s in (0, 1, 2**64 - 1):
        assert lcg_jump(2**64, MMIX_A, MMIX_C, s, 2**64) == s
        assert lcg_jump(2**64, MMIX_A, MMIX_C, s, 2**63) != s
    assert lcg_jump(2**64, MMIX_A, MMIX_C, 5, 1000) == walk(2**64, MMIX_A, MMIX_C, 5, 1000)


def test_lcg_counter_and_tiny_modulus():
    assert lcg_jump(1000, 1, 7, 3, 10**12) == (3 + 7 * 10**12) % 1000
    assert lcg_jump(2, 1, 1, 0, 5) == 1
    assert lcg_jump(1, 0, 0, 0, 9) == 0


def test_leapfrog_streams_interleave():
    m, a, c, s0, p = 2**16, 25173, 13849, 4321, 3
    seq = [s0]
    for _ in range(60):
        seq.append((a * seq[-1] + c) % m)
    ap, cp = leapfrog_parameters(m, a, c, p)
    for j in range(p):
        stream = [seq[j]]
        for _ in range(10):
            stream.append((ap * stream[-1] + cp) % m)
        assert stream == seq[j::p][:11]


def test_negative_n_rejected():
    with pytest.raises(ValueError):
        lcg_jump(16, 5, 3, 1, -1)


def test_gf2_xpow_mod_against_direct_reduction():
    mod = 0b11001  # x^4 + x^3 + 1
    r = 1
    for n in range(40):
        assert gf2_xpow_mod(n, mod) == r
        r = gf2_mulmod(r, 2, mod)
    assert gf2_xpow_mod(15, mod) == 1  # primitive: x has order 15
    assert gf2_xpow_mod(5, 0b11) == 1  # modulo x + 1
    assert gf2_xpow_mod(5, 0b10) == 0  # modulo x


def test_berlekamp_massey_on_lfsr():
    # s_n = s_(n-1) + s_(n-4) has characteristic polynomial x^4 + x^3 + 1.
    bits = [1, 0, 0, 0]
    while len(bits) < 30:
        bits.append(bits[-1] ^ bits[-4])
    assert berlekamp_massey_gf2(bits) == 0b11001
    # s_n = s_(n-3) + s_(n-4) has characteristic polynomial x^4 + x + 1.
    bits = [1, 0, 0, 0]
    while len(bits) < 30:
        bits.append(bits[-3] ^ bits[-4])
    assert berlekamp_massey_gf2(bits) == 0b10011


def test_xorshift32_is_linear_and_jumps():
    rng = random.Random(2)
    for _ in range(100):
        x, y = rng.getrandbits(32), rng.getrandbits(32)
        assert xorshift32_step(x ^ y) == xorshift32_step(x) ^ xorshift32_step(y)
    cp = berlekamp_massey_gf2(output_bits(xorshift32_step, 1, 64))
    assert cp.bit_length() - 1 == 32
    s = 2463534242
    t = s
    for n in range(1, 2001):
        t = xorshift32_step(t)
        if n % 97 == 0 or n == 2000:
            assert f2_jump(xorshift32_step, cp, s, n) == t
    assert f2_jump(xorshift32_step, cp, s, 0) == s
    assert f2_jump(xorshift32_step, cp, s, 2**32 - 1) == s  # full period
    assert f2_jump(xorshift32_step, cp, 0, 12345) == 0  # zero state is fixed


def test_xoshiro256_published_jump_polynomials():
    start = pack([1, 2, 3, 4])
    cp = berlekamp_massey_gf2(output_bits(xoshiro256_step, start, 512))
    assert cp.bit_length() - 1 == 256
    assert gf2_xpow_mod(2**128, cp) == pack(XOSHIRO256_JUMP)
    assert gf2_xpow_mod(2**192, cp) == pack(XOSHIRO256_LONG_JUMP)
    seed = pack([2**64 - 1, 0x0123456789ABCDEF, 0, 1])
    assert f2_jump(xoshiro256_step, cp, seed, 2**128) == f2_jump_by_polynomial(
        xoshiro256_step, pack(XOSHIRO256_JUMP), seed
    )
    t = seed
    for _ in range(3000):
        t = xoshiro256_step(t)
    assert f2_jump(xoshiro256_step, cp, seed, 3000) == t
