# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/xoshiro-xoroshiro/. The authors are listed in prov/XXBA1W.jsonl.

from xoshiro_xoroshiro import (
    JUMP128,
    JUMP256,
    LONG_JUMP128,
    LONG_JUMP256,
    MASK64,
    jump_by_polynomial,
    rotl,
    seed_xoshiro256,
    words_to_int,
    xoroshiro128_jump,
    xoroshiro128_step,
    xoroshiro128p_next,
    xoroshiro128ss_next,
    xoshiro256_jump,
    xoshiro256_long_jump,
    xoshiro256_step,
    xoshiro256pp_next,
    xoshiro256ss_next,
)

# Reference values: the C reference code of Blackman and Vigna (prng.di.unimi.it),
# compiled and run from the states {1, 2, 3, 4} and {1, 2}.

CHARPOLY256 = words_to_int((0x9D116F2BB0F0F001, 0x0280002BCEFD1A5E, 0x04B4EDCF26259F85, 0x0003C03C3F3ECB19)) | (1 << 256)
CHARPOLY128 = words_to_int((0x095B8F76579AA001, 0x0008828E513B43D5)) | (1 << 128)

FERMAT_FACTORS = [3, 5, 17, 257, 65537, 641, 6700417, 274177, 67280421310721,
                  59649589127497217, 5704689200685129054721]


def run(next_fn, s, n):
    return [next_fn(s) for _ in range(n)]


def test_xoshiro256ss_reference() -> None:
    s = [1, 2, 3, 4]
    assert run(xoshiro256ss_next, s, 6) == [
        11520, 0, 1509978240, 1215971899390074240, 1216172134540287360, 607988272756665600,
    ]
    xoshiro256_jump(s)
    assert s == [0x1A06CE59A8DDA48D, 0xB32B2B669A1680CE, 0xCA7CA09057BFB30F, 0x7D9AEC7BE8DB7696]
    assert xoshiro256ss_next(s) == 5426983283421486391
    s = [1, 2, 3, 4]
    xoshiro256_long_jump(s)
    assert s == [0x096A8EB71295A400, 0xDBF84991E50F4516, 0x534EE745810D2A0E, 0x31655CA1A2215BF1]


def test_xoshiro256pp_reference() -> None:
    s = [1, 2, 3, 4]
    assert run(xoshiro256pp_next, s, 6) == [
        41943041, 58720359, 3588806011781223, 3591011842654386,
        9228616714210784205, 9973669472204895162,
    ]


def test_xoroshiro128_reference() -> None:
    s = [1, 2]
    assert run(xoroshiro128p_next, s, 6) == [
        3, 412333834243, 2360170716294286339, 9295852285959843169,
        2797080929874688578, 6019711933173041966,
    ]
    xoroshiro128_jump(s)
    assert s == [0x2E7BBECD6BA6572B, 0x6FD4147C4E84C5D8]
    s = [1, 2]
    assert run(xoroshiro128ss_next, s, 6) == [
        5760, 97769243520, 9706862127477703552, 9223447511460779954,
        8358291023205304566, 15695619998649302768,
    ]
    s = [1, 2]
    jump_by_polynomial(s, words_to_int(LONG_JUMP128), xoroshiro128_step)
    assert s == [0x3CE44494D47D323A, 0x2AA25CA8D61DE643]


# Exact polynomial arithmetic over GF(2): an int, bit i is the coefficient of x^i.

def mulmod(a: int, b: int, p: int) -> int:
    deg = p.bit_length() - 1
    r = 0
    while b:
        if b & 1:
            r ^= a
        b >>= 1
        a <<= 1
        if (a >> deg) & 1:
            a ^= p
    return r


def x_power(e: int, p: int) -> int:
    r, base = 1, 2
    while e:
        if e & 1:
            r = mulmod(r, base, p)
        base = mulmod(base, base, p)
        e >>= 1
    return r


def x_power_of_two(k: int, p: int) -> int:
    """x^(2^k) mod p by k squarings."""
    r = 2
    for _ in range(k):
        r = mulmod(r, r, p)
    return r


def berlekamp_massey(bits: list[int]) -> tuple[int, int]:
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


def reversed_poly(c: int, ell: int) -> int:
    p = 0
    for i in range(ell + 1):
        if (c >> i) & 1:
            p |= 1 << (ell - i)
    return p


def is_prime(n: int) -> bool:
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


def test_factorization_of_2_to_256_minus_1() -> None:
    prod = 1
    for f in FERMAT_FACTORS:
        prod *= f
    assert prod == 2**256 - 1
    for f in FERMAT_FACTORS:  # each factor is below 3.3 * 10^24, so the test is exact
        assert is_prime(f)
    assert all((2**128 - 1) % f == 0 for f in FERMAT_FACTORS[:9])


def is_primitive(p: int, factors: list[int]) -> bool:
    n = 2 ** (p.bit_length() - 1) - 1
    return x_power(n, p) == 1 and all(x_power(n // q, p) != 1 for q in factors)


def test_characteristic_polynomials_are_primitive() -> None:
    assert is_primitive(CHARPOLY128, FERMAT_FACTORS[:9])
    assert is_primitive(CHARPOLY256, FERMAT_FACTORS)


def test_characteristic_polynomial_matches_the_engine() -> None:
    s, bits = [1, 2, 3, 4], []
    for _ in range(512):
        xoshiro256_step(s)
        bits.append(s[0] & 1)
    c, ell = berlekamp_massey(bits)
    assert ell == 256 and reversed_poly(c, ell) == CHARPOLY256
    s, bits = [1, 2], []
    for _ in range(256):
        xoroshiro128_step(s)
        bits.append(s[0] & 1)
    c, ell = berlekamp_massey(bits)
    assert ell == 128 and reversed_poly(c, ell) == CHARPOLY128


def test_jump_constants_are_powers_of_x() -> None:
    assert x_power_of_two(128, CHARPOLY256) == words_to_int(JUMP256)
    assert x_power_of_two(192, CHARPOLY256) == words_to_int(LONG_JUMP256)
    assert x_power_of_two(64, CHARPOLY128) == words_to_int(JUMP128)
    assert x_power_of_two(96, CHARPOLY128) == words_to_int(LONG_JUMP128)


def test_small_jump_equals_stepping() -> None:
    for J in (1, 2, 3, 1000):
        s = [5, 6, 7, 8]
        t = list(s)
        jump_by_polynomial(s, x_power(J, CHARPOLY256), xoshiro256_step)
        for _ in range(J):
            xoshiro256_step(t)
        assert s == t


def rank(vectors: list[int]) -> int:
    basis: dict[int, int] = {}
    for v in vectors:
        while v:
            h = v.bit_length() - 1
            if h in basis:
                v ^= basis[h]
            else:
                basis[h] = v
                break
    return len(basis)


def tuple_rank(step, words: int, word: int, k: int) -> int:
    vectors = []
    for i in range(64 * words):
        s = [0] * words
        s[i // 64] = 1 << (i % 64)
        out = 0
        for j in range(k):
            out |= s[word] << (64 * j)
            step(s)
        vectors.append(out)
    return rank(vectors)


def test_equidistribution_of_the_starstar_outputs() -> None:
    # The ** output depends on s1 (xoshiro256) or s0 (xoroshiro128) through a bijection.
    # The map from the state to k consecutive values of that word is onto for k = 4 and k = 2.
    assert tuple_rank(xoshiro256_step, 4, 1, 4) == 256
    assert tuple_rank(xoroshiro128_step, 2, 0, 2) == 128
    # The starstar scrambler is a bijection of words: 5 and 9 are odd.
    assert pow(5, -1, 2**64) * 5 % 2**64 == 1 and pow(9, -1, 2**64) * 9 % 2**64 == 1


def test_lowest_bit_of_plus_is_linear() -> None:
    s, bits = [1, 2], []
    for _ in range(512):
        bits.append(xoroshiro128p_next(s) & 1)
    _, ell = berlekamp_massey(bits)
    assert ell <= 128


def test_zero_state_is_fixed_and_seeding_avoids_it() -> None:
    s = [0, 0, 0, 0]
    assert xoshiro256ss_next(s) == 0 and s == [0, 0, 0, 0]
    for seed in (0, 1, 2**64 - 1):
        st = seed_xoshiro256(seed)
        assert any(st) and all(0 <= w <= MASK64 for w in st)
    assert seed_xoshiro256(1234567)[0] == 6457827717110365317


def test_rotl() -> None:
    assert rotl(1 << 63, 1) == 1
    assert rotl(0x8000000000000001, 4) == 0x18
