# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/reed-solomon-decoding/. The authors are listed in prov/KQB2R4.jsonl.

import itertools
import random

import pytest

from gf import GF2m
from rs_decoding import bm_errors_and_erasures, euclid_errors_and_erasures, locator, rs_decode, rs_encode, syndromes

F8 = GF2m(3, 0b1011)  # x^3 + x + 1
F16 = GF2m(4, 0b10011)  # x^4 + x + 1
QR = GF2m(8, 0x11D)  # ISO/IEC 18004
CCSDS = GF2m(8, 0x187)  # CCSDS 131.0-B-5, 4.3.3

METHODS = ("bm", "euclid")


def distance(a: list[int], b: list[int]) -> int:
    return sum(1 for x, y in zip(a, b) if x != y)


def test_worked_example() -> None:
    a = F16.alpha
    c = rs_encode(F16, [a(i) for i in range(11)], 4)
    r = list(c)
    r[2] ^= a(5)
    r[7] ^= a(11)
    for method in METHODS:
        assert rs_decode(F16, r, 4, method=method) == (c, [2, 7])


def test_qr_hello_world() -> None:
    # Codeword from the Thonky QR code tutorial, HELLO WORLD 1-M, highest power first.
    data = [32, 91, 11, 120, 209, 114, 220, 77, 67, 64, 236, 17, 236, 17, 236, 17]
    ec = [196, 35, 39, 119, 235, 215, 231, 226, 93, 23]
    c = list(reversed(data + ec))
    assert syndromes(QR, c, 10, b=0) == [0] * 10
    rng = random.Random(18004)
    for _ in range(200):
        nu = rng.randrange(0, 6)
        r = list(c)
        for i in rng.sample(range(26), nu):
            r[i] ^= rng.randrange(1, 256)
        for method in METHODS:
            out = rs_decode(QR, r, 10, b=0, method=method)
            assert out is not None and out[0] == c


def test_exhaustive_rs_7_3() -> None:
    # RS(7, 3) over GF(8), t = 2: every pattern of at most 2 errors is corrected,
    # and every pattern of 3 errors is either detected or decoded to a codeword within distance 2.
    c = rs_encode(F8, [3, 5, 6], 4)
    for method in METHODS:
        for nu in range(0, 4):
            for pos in itertools.combinations(range(7), nu):
                for vals in itertools.product(range(1, 8), repeat=nu):
                    r = list(c)
                    for i, v in zip(pos, vals):
                        r[i] ^= v
                    out = rs_decode(F8, r, 4, method=method)
                    if nu <= 2:
                        assert out == (c, list(pos))
                    elif out is not None:
                        assert not any(syndromes(F8, out[0], 4)) and distance(out[0], r) <= 2


def test_exhaustive_errors_and_erasures_rs_7_3() -> None:
    # all (nu errors, rho erasures) with 2 nu + rho <= 4 on RS(7, 3), b = 0
    rng = random.Random(7)
    c = rs_encode(F8, [1, 0, 6], 4, b=0)
    count = 0
    for rho in range(0, 5):
        for er in itertools.combinations(range(7), rho):
            rest = [i for i in range(7) if i not in er]
            for nu in range(0, (4 - rho) // 2 + 1):
                for pos in itertools.combinations(rest, nu):
                    for vals in itertools.product(range(1, 8), repeat=nu):
                        r = list(c)
                        for i, v in zip(pos, vals):
                            r[i] ^= v
                        for i in er:
                            r[i] = rng.randrange(8)  # an erased symbol may hold anything
                        for method in METHODS:
                            assert rs_decode(F8, r, 4, b=0, erasures=list(er), method=method)[0] == c
                            count += 1
    assert count > 2000


def test_exhaustive_rs_15_11() -> None:
    # every pattern of at most t = 2 errors on RS(15, 11) over GF(16)
    rng = random.Random(15)
    c = rs_encode(F16, [rng.randrange(16) for _ in range(11)], 4)
    for nu in (0, 1, 2):
        for pos in itertools.combinations(range(15), nu):
            for vals in itertools.product(range(1, 16), repeat=nu):
                r = list(c)
                for i, v in zip(pos, vals):
                    r[i] ^= v
                assert rs_decode(F16, r, 4) == (c, list(pos))


def test_bm_and_euclid_agree() -> None:
    rng = random.Random(1975)
    for _ in range(600):
        nsym = rng.choice((4, 6, 8))
        rho = rng.randrange(0, nsym + 1)
        nu = rng.randrange(0, (nsym - rho) // 2 + 1)
        pos = rng.sample(range(15), nu + rho)
        er, errs = pos[:rho], pos[rho:]
        w = [0] * 15
        for i in pos:
            w[i] = rng.randrange(1, 16)
        syn = syndromes(F16, w, nsym)
        gamma = locator(F16, er)
        psi, L = bm_errors_and_erasures(F16, syn, gamma)
        lam = euclid_errors_and_erasures(F16, syn, gamma)
        assert psi == F16.pmul(lam, gamma) == F16.pmul(locator(F16, errs), gamma)
        assert L == nu + rho


@pytest.mark.parametrize("method", METHODS)
def test_random_rs_255_223(method: str) -> None:
    # 16-error-correcting RS(255, 223) with the CCSDS field and zeros beta^112 .. beta^143, beta = alpha^11
    rng = random.Random(223)
    for trial in range(40):
        msg = [rng.randrange(256) for _ in range(223)]
        c = rs_encode(CCSDS, msg, 32, b=112, step=11)
        r = list(c)
        rho = rng.randrange(0, 33) if trial % 2 else 0
        nu = rng.randrange(0, (32 - rho) // 2 + 1)
        pos = rng.sample(range(255), nu + rho)
        for i in pos[rho:]:
            r[i] ^= rng.randrange(1, 256)
        for i in pos[:rho]:
            r[i] = rng.randrange(256)
        out = rs_decode(CCSDS, r, 32, b=112, step=11, erasures=pos[:rho], method=method)
        assert out is not None and out[0] == c


def test_shortened_code_and_detection() -> None:
    # A shortened RS(40, 32) over GF(256): roots outside 0 .. 39 mean a failure.
    rng = random.Random(40)
    detected = wrong = 0
    for _ in range(300):
        c = rs_encode(QR, [rng.randrange(256) for _ in range(32)], 8, b=0)
        r = list(c)
        for i in rng.sample(range(40), 5):  # t = 4, so 5 errors are too many
            r[i] ^= rng.randrange(1, 256)
        out = rs_decode(QR, r, 8, b=0)
        if out is None:
            detected += 1
        else:
            assert out[0] != c and distance(out[0], r) <= 4 and not any(syndromes(QR, out[0], 8, b=0))
            wrong += 1
    assert detected > 250  # most patterns beyond t are detected


def test_edges() -> None:
    c = rs_encode(F16, [0] * 11, 4)
    assert c == [0] * 15
    assert rs_decode(F16, c, 4) == (c, [])
    assert rs_decode(F16, c, 4, erasures=list(range(5))) is None  # rho > n - k
    r = [0] * 15
    r[14] = 1
    assert rs_decode(F16, r, 4) == (c, [14])
    with pytest.raises(ValueError):
        rs_decode(F16, r, 4, method="other")
