# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cyclic-code/. The authors are listed in prov/Z6M51W.jsonl.

import itertools
import random

from cyclic_code import (check_polynomial, codewords, cyclic_shift, deg, divisors_of_xn1,
                         encode_nonsystematic, encode_systematic, generator_rows, is_generator,
                         parity_check_rows, pdivmod, pmul, syndrome, zeros)

HAMMING_G = 0b1011  # 1 + x + x^3


def weight(c: int) -> int:
    return bin(c).count("1")


def test_factorization_of_x7_minus_1() -> None:
    # x^7 - 1 = (x + 1)(x^3 + x + 1)(x^3 + x^2 + 1) over GF(2)
    assert pmul(pmul(0b11, 0b1011), 0b1101) == (1 << 7) | 1
    divs = divisors_of_xn1(7)
    assert len(divs) == 8  # 2^3 cyclic codes of length 7
    assert check_polynomial(HAMMING_G, 7) == 0b10111  # 1 + x + x^2 + x^4


def test_number_of_cyclic_codes_of_length_15() -> None:
    # x^15 - 1 has 5 irreducible factors over GF(2): degrees 1, 2, 4, 4, 4
    assert len(divisors_of_xn1(15)) == 2 ** 5


def test_every_shift_is_a_codeword() -> None:
    for n in (7, 9, 15):
        for g in divisors_of_xn1(n):
            if deg(g) == n:
                continue
            code = set(codewords(g, n))
            for c in code:
                assert cyclic_shift(c, n) in code


def test_shift_is_multiplication_by_x() -> None:
    rng = random.Random(7)
    for _ in range(200):
        c = rng.randrange(1 << 15)
        assert cyclic_shift(c, 15) == pdivmod(c << 1, (1 << 15) | 1)[1]


def test_systematic_encoder() -> None:
    rng = random.Random(1)
    for n, g in ((7, HAMMING_G), (15, 0b111010001), (15, 0b10100110111)):
        k = n - deg(g)
        code = set(codewords(g, n))
        for m in range(1 << k) if k <= 7 else (rng.randrange(1 << k) for _ in range(100)):
            c = encode_systematic(m, k, g)
            assert c >> deg(g) == m  # the message sits in the top k positions
            assert syndrome(c, g) == 0
            assert c in code


def test_systematic_example() -> None:
    # m = 1 + x^3, g = 1 + x + x^3: x^3 m = x^3 + x^6 = (x + 1) + (x^2 + 1) = x + x^2 mod g,
    # so c = x + x^2 + x^3 + x^6, the word (0, 1, 1, 1, 0, 0, 1)
    c = encode_systematic(0b1001, 4, HAMMING_G)
    assert c == 0b1001110
    assert encode_nonsystematic(0b1001, HAMMING_G) == 0b1010011


def test_crc_is_the_same_register() -> None:
    # CRC catalogue (Greg Cook), CRC-8/SMBUS: width 8, poly 0x07, init 0, no reflection,
    # xorout 0, check = 0xF4 for the ASCII string "123456789".
    msg = int.from_bytes(b"123456789", "big")
    c = encode_systematic(msg, 72, 0x107)
    assert c & 0xFF == 0xF4
    # CRC catalogue, CRC-16/XMODEM: poly 0x1021, init 0, no reflection, check = 0x31C3
    c = encode_systematic(msg, 72, 0x11021)
    assert c & 0xFFFF == 0x31C3


def test_generator_and_parity_check_matrices() -> None:
    for n in (7, 15):
        for g in divisors_of_xn1(n):
            if deg(g) in (0, n):
                continue
            rows_g = generator_rows(g, n)
            rows_h = parity_check_rows(g, n)
            for a in rows_g:
                for b in rows_h:
                    assert weight(a & b) % 2 == 0
            code = set(codewords(g, n))
            # a word is a codeword exactly when every parity check is satisfied
            for v in range(1 << n) if n == 7 else []:
                ok = all(weight(v & b) % 2 == 0 for b in rows_h)
                assert ok == (v in code)


def test_syndrome_depends_only_on_error() -> None:
    rng = random.Random(3)
    g = 0b111010001
    for _ in range(300):
        m = rng.randrange(1 << 7)
        e = rng.randrange(1 << 15)
        c = encode_systematic(m, 7, g)
        assert syndrome(c ^ e, g) == syndrome(e, g)


def test_hamming_7_4_corrects_one_error_by_syndrome() -> None:
    table = {syndrome(1 << i, HAMMING_G): i for i in range(7)}
    assert len(table) == 7
    for m in range(16):
        c = encode_systematic(m, 4, HAMMING_G)
        for i in range(7):
            r = c ^ (1 << i)
            assert r ^ (1 << table[syndrome(r, HAMMING_G)]) == c


def test_zeros_and_bch_bound() -> None:
    # alpha a root of x^3 + x + 1: the zeros of 1 + x + x^3 are alpha, alpha^2, alpha^4
    assert zeros(HAMMING_G, 3, 0b1011) == [1, 2, 4]
    # BCH bound: delta - 1 consecutive zeros give d >= delta. Check on all codes of length 15.
    for g in divisors_of_xn1(15):
        if deg(g) in (0, 15):
            continue
        z = set(zeros(g, 4, 0b10011))
        run = 0
        for b in range(15):
            r = 0
            while r < 15 and (b + r) % 15 in z:
                r += 1
            run = max(run, r)
        d = min(weight(c) for c in codewords(g, 15) if c)
        assert d >= run + 1


def test_not_cyclic() -> None:
    assert not is_generator(0b111, 7)  # 1 + x + x^2 does not divide x^7 - 1
    assert is_generator(0b111, 3) and is_generator(0b111, 9)
    # the [7, 4] code spanned by these rows is linear but not cyclic
    rows = [0b1000110, 0b0100101, 0b0010011, 0b0001111]
    code = {0}
    for r in rows:
        code |= {c ^ r for c in code}
    assert any(cyclic_shift(c, 7) not in code for c in code)
    assert list(itertools.islice(code, 1))  # non-empty
