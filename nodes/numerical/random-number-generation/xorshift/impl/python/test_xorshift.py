# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/xorshift/. The authors are listed in prov/ZZ9CEX.jsonl.

import pytest

from xorshift import (
    MASK32,
    MASK64,
    xorshift128_next,
    xorshift32_next,
    xorshift64_next,
    xorshift64star_next,
    xorshift_next,
    xorshift_stream,
)

# Reference outputs were produced by compiling the C code of Marsaglia (2003),
# section 3 and section 4, and the xorshift64* code of Vigna (2016).


def test_xor32_reference_outputs() -> None:
    x = 2463534242  # the seed in Marsaglia's xor32 listing
    out = []
    for _ in range(5):
        x = xorshift32_next(x)
        out.append(x)
    assert out == [723471715, 2497366906, 2064144800, 2008045182, 3532304609]


def test_trace_of_the_page() -> None:
    assert xorshift_stream(1, 3) == [270369, 67634689, 2647435461]
    assert xorshift_stream(1, 5)[3:] == [307599695, 2398689233]


def test_xor64_reference_outputs() -> None:
    x = 88172645463325252
    out = []
    for _ in range(5):
        x = xorshift64_next(x)
        out.append(x)
    assert out == [
        8748534153485358512, 3040900993826735515, 3453997556048239312,
        16431732851926010853, 8204724074003728306,
    ]


def test_xor128_reference_outputs() -> None:
    s = (123456789, 362436069, 521288629, 88675123)
    out = []
    for _ in range(5):
        s, v = xorshift128_next(s)
        out.append(v)
    assert out == [3701687786, 458299110, 2500872618, 3633119408, 516391518]


def test_xorshift64star_reference_outputs() -> None:
    x = 1
    out = []
    for _ in range(5):
        x, v = xorshift64star_next(x)
        out.append(v)
    assert out == [
        5180492295206395165, 12380297144915551517, 13389498078930870103,
        5599127315341312413, 1036278371763004928,
    ]


# Exact arithmetic over GF(2). A polynomial is an int; bit i is the coefficient of x^i.

def berlekamp_massey(bits: list[int]) -> tuple[int, int]:
    """Return the connection polynomial C and the linear complexity L."""
    c, b, ell, m = 1, 1, 0, 1
    for n, bit in enumerate(bits):
        d = bit
        for i in range(1, ell + 1):
            d ^= ((c >> i) & 1) & bits[n - i]
        if d == 0:
            m += 1
            continue
        t = c
        c ^= b << m
        if 2 * ell <= n:
            ell, b, m = n + 1 - ell, t, 1
        else:
            m += 1
    return c, ell


def mulmod(a: int, b: int, p: int, deg: int) -> int:
    r = 0
    while b:
        if b & 1:
            r ^= a
        b >>= 1
        a <<= 1
        if (a >> deg) & 1:
            a ^= p
    return r


def x_power(e: int, p: int, deg: int) -> int:
    r, base = 1, 2
    while e:
        if e & 1:
            r = mulmod(r, base, p, deg)
        base = mulmod(base, base, p, deg)
        e >>= 1
    return r


def prime_factors(n: int) -> list[int]:
    out, d = [], 2
    while d * d <= n:
        if n % d == 0:
            out.append(d)
            while n % d == 0:
                n //= d
        d += 1
    if n > 1:
        out.append(n)
    return out


# 2^n - 1 for n = 32, 64, 128 is a product of the Fermat numbers F0 .. F6 and their factors.
FACTORS = {
    32: [3, 5, 17, 257, 65537],
    64: [3, 5, 17, 257, 641, 65537, 6700417],
    128: [3, 5, 17, 257, 641, 65537, 274177, 6700417, 67280421310721],
}


def is_probable_prime(n: int) -> bool:
    """Miller-Rabin with the first 13 prime bases, which is exact for n < 3.3 * 10^24."""
    bases = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41]
    if n < 2:
        return False
    for p in bases:
        if n % p == 0:
            return n == p
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in bases:
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def is_primitive(p: int, deg: int, factors: list[int]) -> bool:
    """x has order 2^deg - 1 modulo p, which is primitivity for a polynomial of degree deg."""
    n = (1 << deg) - 1
    if x_power(n, p, deg) != 1:
        return False
    return all(x_power(n // q, p, deg) != 1 for q in factors)


def output_polynomial(bits: list[int], deg: int) -> int | None:
    """Minimal polynomial of a bit sequence, reversed to the characteristic form, if its degree is deg."""
    c, ell = berlekamp_massey(bits)
    if ell != deg:
        return None
    p = 0
    for i in range(ell + 1):
        if (c >> i) & 1:
            p |= 1 << (ell - i)
    return p


def generator_is_full_period(step, seed: int, deg: int, factors: list[int]) -> bool:
    s, bits = seed, []
    for _ in range(2 * deg):
        s = step(s)
        bits.append(s & 1)
    p = output_polynomial(bits, deg)
    return p is not None and is_primitive(p, deg, factors)


def test_factor_lists_are_exact() -> None:
    assert prime_factors(2**32 - 1) == FACTORS[32]
    assert prime_factors(2**64 - 1) == FACTORS[64]
    prod = 1
    for f in FACTORS[128]:
        assert is_probable_prime(f)
        prod *= f
    assert prod == 2**128 - 1


def test_published_triples_have_full_period() -> None:
    assert generator_is_full_period(xorshift32_next, 1, 32, FACTORS[32])
    assert generator_is_full_period(xorshift64_next, 1, 64, FACTORS[64])

    def step128(s: int) -> int:
        st = ((s >> 96) & MASK32, (s >> 64) & MASK32, (s >> 32) & MASK32, s & MASK32)
        (x, y, z, w), _ = xorshift128_next(st)
        return (x << 96) | (y << 64) | (z << 32) | w

    seed = (123456789 << 96) | (362436069 << 64) | (521288629 << 32) | 88675123
    assert generator_is_full_period(step128, seed, 128, FACTORS[128])

    def step64star(s: int) -> int:
        return xorshift64star_next(s)[0]

    assert generator_is_full_period(step64star, 1, 64, FACTORS[64])


def test_bad_triple_is_rejected() -> None:
    # (1, 1, 1) on 32 bits is not one of Marsaglia's 81 triples.
    assert not generator_is_full_period(lambda s: xorshift_next(s, 1, 1, 1, 32), 1, 32, FACTORS[32])


def test_brute_force_periods_agree_with_primitivity() -> None:
    # For w = 8, every triple: the period from seed 1 is 255 exactly when the polynomial is primitive.
    w, full = 8, 0
    fac = prime_factors(2**w - 1)
    for a in range(1, w):
        for b in range(1, w):
            for c in range(1, w):
                x, n = 1, 0
                while True:
                    x = xorshift_next(x, a, b, c, w)
                    n += 1
                    if x == 1:
                        break
                is_full = n == 2**w - 1
                full += is_full
                prim = generator_is_full_period(lambda s: xorshift_next(s, a, b, c, w), 1, w, fac)
                assert is_full == prim
    assert full == 24


def test_step_is_a_bijection_on_small_words() -> None:
    for w, (a, b, c) in [(8, (1, 1, 2)), (8, (3, 5, 1)), (10, (2, 7, 3))]:
        images = {xorshift_next(x, a, b, c, w) for x in range(2**w)}
        assert len(images) == 2**w
        assert xorshift_next(0, a, b, c, w) == 0


def test_linearity() -> None:
    import random

    rng = random.Random(5)
    for _ in range(200):
        u, v = rng.getrandbits(64), rng.getrandbits(64)
        assert xorshift64_next(u ^ v) == xorshift64_next(u) ^ xorshift64_next(v)


def test_low_bit_of_xorshift64star_is_linear() -> None:
    # The multiplier is odd, so the lowest output bit equals the lowest state bit.
    x = 12345
    for _ in range(1000):
        x, v = xorshift64star_next(x)
        assert v & 1 == x & 1


def test_zero_seed_is_rejected() -> None:
    with pytest.raises(ValueError):
        xorshift_stream(0, 1)
    with pytest.raises(ValueError):
        xorshift_stream(2**32, 1)


def test_outputs_stay_in_range() -> None:
    for v in xorshift_stream(0xDEADBEEF, 1000):
        assert 0 < v <= MASK32
    x = 1
    for _ in range(1000):
        x = xorshift64_next(x)
        assert 0 < x <= MASK64
