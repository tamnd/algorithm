# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/forney-algorithm/. The authors are listed in prov/6QZVB2.jsonl.

import random

import pytest

from forney_algorithm import formal_derivative, forney, locator, poly_eval, poly_mul_mod, syndromes
from gf import GF2m, GFp

F16 = GF2m(4, 0b10011)  # x^4 + x + 1
QR = GF2m(8, 0x11D)  # ISO/IEC 18004
CCSDS = GF2m(8, 0x187)  # CCSDS 131.0-B-5, 4.3.3
F13 = GFp(13, 2)  # 2 has order 12 modulo 13


def error_syndromes(f, n: int, errors: dict[int, int], two_t: int, b: int, step: int = 1) -> list[int]:
    word = [0] * n
    for i, y in errors.items():
        word[i] = y
    return syndromes(f, word, two_t, b, step)


def test_worked_example() -> None:
    a = F16.alpha
    syn = [a(4), a(13), a(9), a(10)]  # S_1 .. S_4 of alpha^5 at 2 and alpha^11 at 7
    assert error_syndromes(F16, 15, {2: a(5), 7: a(11)}, 4, 1) == syn
    lam = locator(F16, [2, 7])
    assert lam == [1, a(12), a(9)]
    assert poly_mul_mod(F16, syn, lam, 4) == [a(4), a(12), 0, 0]  # Omega = a^4 + a^12 x
    assert formal_derivative(F16, lam) == [a(12), 0]  # Lambda' = a^12
    assert forney(F16, syn, lam, [2, 7], b=1) == [a(5), a(11)]


def test_qr_hello_world_correction() -> None:
    # Codeword from the Thonky QR code tutorial, HELLO WORLD 1-M, highest power first.
    data = [32, 91, 11, 120, 209, 114, 220, 77, 67, 64, 236, 17, 236, 17, 236, 17]
    ec = [196, 35, 39, 119, 235, 215, 231, 226, 93, 23]
    c = list(reversed(data + ec))  # c[i] is the coefficient of x^i
    assert syndromes(QR, c, 10, b=0) == [0] * 10
    r = list(c)
    errs = {0: 0x55, 9: 0x01, 17: 0xFF, 25: 0x80, 13: 0x3C}  # 5 errors, t = 5
    for i, y in errs.items():
        r[i] ^= y
    syn = syndromes(QR, r, 10, b=0)
    pos = sorted(errs)
    vals = forney(QR, syn, locator(QR, pos), pos, b=0)
    for i, y in zip(pos, vals):
        r[i] ^= y
    assert r == c


@pytest.mark.parametrize("b", [0, 1, 2, 5, 14])
def test_random_gf16_all_b(b: int) -> None:
    rng = random.Random(100 + b)
    t = 3
    for _ in range(150):
        pos = rng.sample(range(15), rng.randrange(1, t + 1))
        errs = {i: rng.randrange(1, 16) for i in pos}
        syn = error_syndromes(F16, 15, errs, 2 * t, b)
        assert forney(F16, syn, locator(F16, pos), pos, b) == [errs[i] for i in pos]


def test_wrong_b_gives_wrong_values() -> None:
    # The factor X^(1-b) matters: using the b = 1 formula for a b = 0 code fails.
    a = F16.alpha
    errs = {2: a(5), 7: a(11)}
    syn0 = error_syndromes(F16, 15, errs, 4, 0)
    lam = locator(F16, [2, 7])
    assert forney(F16, syn0, lam, [2, 7], b=0) == [a(5), a(11)]
    assert forney(F16, syn0, lam, [2, 7], b=1) != [a(5), a(11)]


def test_ccsds_conventions() -> None:
    # CCSDS: beta = alpha^11, zeros beta^(128-E) .. beta^(127+E), E = 16
    rng = random.Random(131)
    e = 16
    for _ in range(100):
        pos = rng.sample(range(255), rng.randrange(1, e + 1))
        errs = {i: rng.randrange(1, 256) for i in pos}
        syn = error_syndromes(CCSDS, 255, errs, 2 * e, 128 - e, 11)
        lam = locator(CCSDS, pos, 11)
        assert forney(CCSDS, syn, lam, pos, 128 - e, 11) == [errs[i] for i in pos]


def test_prime_field_needs_the_sign_and_the_derivative() -> None:
    # Over GF(13) the minus sign and the factor i in the derivative are not trivial.
    rng = random.Random(13)
    for b in (0, 1, 3):
        for _ in range(150):
            pos = rng.sample(range(12), rng.randrange(1, 4))
            errs = {i: rng.randrange(1, 13) for i in pos}
            syn = error_syndromes(F13, 12, errs, 6, b)
            assert forney(F13, syn, locator(F13, pos), pos, b) == [errs[i] for i in pos]
    assert formal_derivative(F13, [1, 2, 3, 4]) == [2, 6, 12]
    assert formal_derivative(F16, [1, 2, 3, 4]) == [2, 0, 4]


def test_erasures_up_to_2t() -> None:
    # With all positions known (erasures), Forney finds up to 2t values
    rng = random.Random(8)
    for _ in range(200):
        pos = rng.sample(range(255), rng.randrange(1, 11))
        errs = {i: rng.randrange(1, 256) for i in pos}
        syn = error_syndromes(QR, 255, errs, 10, 0)
        assert forney(QR, syn, locator(QR, pos), pos, 0) == [errs[i] for i in pos]


def test_omega_closed_form() -> None:
    # Omega(x) = sum_k Y_k X_k^b prod_(l != k) (1 - X_l x)
    rng = random.Random(21)
    for _ in range(100):
        b = rng.randrange(15)
        pos = rng.sample(range(15), 3)
        errs = {i: rng.randrange(1, 16) for i in pos}
        syn = error_syndromes(F16, 15, errs, 6, b)
        omega = poly_mul_mod(F16, syn, locator(F16, pos), 6)
        want = [0] * 6
        for k in pos:
            term = locator(F16, [l for l in pos if l != k])
            c = F16.mul(errs[k], F16.pow(F16.alpha(k), b))
            for d, v in enumerate(term):
                want[d] ^= F16.mul(c, v)
        assert omega == want
        assert poly_eval(F16, omega, 0) == F16.mul(1, syn[0])
