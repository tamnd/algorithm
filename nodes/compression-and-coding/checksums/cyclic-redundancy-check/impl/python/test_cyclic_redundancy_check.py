# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cyclic-redundancy-check/. The authors are listed in prov/JEXCDN.jsonl.

import binascii
import random

from cyclic_redundancy_check import (
    CATALOGUE, append_crc, crc, crc_by_division, crc_reflected, crc_register, forge_suffix,
    poly_mod, reflect, residue_of,
)

RNG = random.Random(1961)
CHECK = b"123456789"

# Check values copied by hand from the CRC catalogue (Greg Cook, reveng),
# entry by entry: "check" is the CRC of the ASCII string "123456789".
CATALOGUE_CHECKS = {
    "CRC-8/SMBUS": 0xF4,
    "CRC-16/ARC": 0xBB3D,
    "CRC-16/IBM-3740": 0x29B1,  # alias CRC-16/CCITT-FALSE
    "CRC-16/KERMIT": 0x2189,
    "CRC-16/XMODEM": 0x31C3,
    "CRC-16/MODBUS": 0x4B37,
    "CRC-32/ISO-HDLC": 0xCBF43926,
    "CRC-32/ISCSI": 0xE3069283,
    "CRC-32/BZIP2": 0xFC891918,
    "CRC-32/MPEG-2": 0x0376E6E7,
    "CRC-64/XZ": 0x995DC9BBDF1939FA,
}


def test_catalogue_check_values() -> None:
    for name, want in CATALOGUE_CHECKS.items():
        assert crc(CHECK, CATALOGUE[name]) == want, name


def test_catalogue_residues() -> None:
    # Residues from the same catalogue entries.
    for p in CATALOGUE.values():
        for n in (0, 1, 9, 33):
            data = bytes(RNG.randrange(256) for _ in range(n))
            assert residue_of(append_crc(data, p), p) == p.residue, p.name


def test_against_binascii() -> None:
    iso = CATALOGUE["CRC-32/ISO-HDLC"]
    xmodem = CATALOGUE["CRC-16/XMODEM"]
    for n in list(range(20)) + [100, 257]:
        data = bytes(RNG.randrange(256) for _ in range(n))
        assert crc(data, iso) == binascii.crc32(data)
        assert crc(data, xmodem) == binascii.crc_hqx(data, 0)
        # binascii.crc_hqx with start value 0xFFFF is CRC-16/IBM-3740.
        assert crc(data, CATALOGUE["CRC-16/IBM-3740"]) == binascii.crc_hqx(data, 0xFFFF)


def test_reflected_register_form_agrees() -> None:
    for p in CATALOGUE.values():
        if p.refin and p.refout:
            for n in range(12):
                data = bytes(RNG.randrange(256) for _ in range(n))
                assert crc_reflected(data, p) == crc(data, p)


def test_register_is_division() -> None:
    # With init = 0 the register holds M(x) x^r mod G(x).
    for width, poly in ((8, 0x07), (16, 0x1021), (32, 0x04C11DB7)):
        for n in range(10):
            data = bytes(RNG.randrange(256) for _ in range(n))
            p = CATALOGUE["CRC-32/MPEG-2"]
            p = p.__class__("t", width, poly, 0, False, False, 0, 0, 0)
            assert crc_register(data, p) == crc_by_division(data, width, poly)


def test_init_is_xor_into_first_bits() -> None:
    # init I adds I(x) x^k, k = number of message bits: the same as XOR of I
    # into the first r message bits when k >= r.
    p = CATALOGUE["CRC-32/BZIP2"]
    g = (1 << 32) | p.poly
    for n in range(0, 12):
        data = bytes(RNG.randrange(256) for _ in range(n))
        k = 8 * n
        want = poly_mod((p.init << k) ^ (int.from_bytes(data, "big") << 32), g)
        assert crc_register(data, p) == want


def test_codeword_divisible() -> None:
    p = CATALOGUE["CRC-16/XMODEM"]
    g = (1 << 16) | p.poly
    for n in range(1, 20):
        data = bytes(RNG.randrange(256) for _ in range(n))
        cw = append_crc(data, p)
        assert poly_mod(int.from_bytes(cw, "big"), g) == 0


def test_errors_detected_and_affine() -> None:
    # The CRC is affine: crc(a ^ b ^ c) = crc(a) ^ crc(b) ^ crc(c) for equal lengths.
    for p in CATALOGUE.values():
        for n in (1, 4, 17):
            a, b, c = (bytes(RNG.randrange(256) for _ in range(n)) for _ in range(3))
            x = bytes(i ^ j ^ k for i, j, k in zip(a, b, c))
            assert crc(x, p) == crc(a, p) ^ crc(b, p) ^ crc(c, p)
            # Every single-bit error changes the CRC.
            pos = RNG.randrange(8 * n)
            e = bytearray(a)
            e[pos // 8] ^= 1 << (pos % 8)
            assert crc(bytes(e), p) != crc(a, p)


def test_forgery_is_easy() -> None:
    for name in ("CRC-32/ISO-HDLC", "CRC-32/BZIP2", "CRC-16/ARC", "CRC-64/XZ"):
        p = CATALOGUE[name]
        for n in (0, 3, 20):
            data = bytes(RNG.randrange(256) for _ in range(n))
            target = RNG.getrandbits(p.width)
            assert crc(data + forge_suffix(data, target, p), p) == target


def test_augmented_init_equivalence() -> None:
    # Williams's augmented form with register 0xFFFF equals the direct form
    # with init 0xFFFF * x^16 mod G = 0x1D0F.
    assert poly_mod(0xFFFF << 16, 0x11021) == 0x1D0F


def test_reflect() -> None:
    assert reflect(0x04C11DB7, 32) == 0xEDB88320
    assert reflect(0x1EDC6F41, 32) == 0x82F63B78
    assert reflect(0b1, 8) == 0b10000000
