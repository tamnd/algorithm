# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gost-28147-89/. The authors are listed in prov/QNHVZN.jsonl.

import random

from gost_28147_89 import decrypt_block, encrypt_block, g, round_keys, t

KEY = bytes.fromhex("ffeeddccbbaa99887766554433221100f0f1f2f3f4f5f6f7f8f9fafbfcfdfeff")


# RFC 8891 Appendix A.1, transformation t (S-box set id-tc26-gost-28147-param-Z).
def test_rfc8891_t() -> None:
    assert t(0xFDB97531) == 0x2A196F34
    assert t(0x2A196F34) == 0xEBD9F03A
    assert t(0xEBD9F03A) == 0xB039BB3D
    assert t(0xB039BB3D) == 0x68695433


# RFC 8891 Appendix A.2, transformation g.
def test_rfc8891_g() -> None:
    assert g(0x87654321, 0xFEDCBA98) == 0xFDCBC20C
    assert g(0xFDCBC20C, 0x87654321) == 0x7E791A4B
    assert g(0x7E791A4B, 0xFDCBC20C) == 0xC76549EC
    assert g(0xC76549EC, 0x7E791A4B) == 0x9791C849


# RFC 8891 Appendix A.3, key schedule.
def test_rfc8891_key_schedule() -> None:
    ks = round_keys(KEY)
    assert ks[0] == 0xFFEEDDCC
    assert ks[7] == 0xFCFDFEFF
    assert ks[24] == 0xFCFDFEFF
    assert ks[31] == 0xFFEEDDCC


# RFC 8891 Appendices A.4 and A.5, test encryption and decryption.
def test_rfc8891_encrypt_decrypt() -> None:
    pt = bytes.fromhex("fedcba9876543210")
    ct = bytes.fromhex("4ee901e5c2d8ca3d")
    assert encrypt_block(KEY, pt) == ct
    assert decrypt_block(KEY, ct) == pt


def test_round_trip_random_sboxes() -> None:
    rng = random.Random(7)
    for _ in range(10):
        sbox = [rng.sample(range(16), 16) for _ in range(8)]
        key, m = rng.randbytes(32), rng.randbytes(8)
        assert decrypt_block(key, encrypt_block(key, m, sbox), sbox) == m
