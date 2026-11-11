# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/twofish/. The authors are listed in prov/HJZJTY.jsonl.

import random

import pytest

from twofish import Q0, Q1, Twofish, key_schedule

# Twofish paper (Schneier et al., 1998), Appendix A.1 "Intermediate Values"
# (file ecb_ival.txt), plaintext all zero.
IVAL = [
    ("00000000000000000000000000000000", "9F589F5CF6122C32B6BFEC2F2AE8C35A"),
    ("0123456789ABCDEFFEDCBA98765432100011223344556677", "CFD1D2E5A9BE9CDF501F13B892BD2248"),
    ("0123456789ABCDEFFEDCBA987654321000112233445566778899AABBCCDDEEFF", "37527BE0052334B89F0CFCCAE87CFA20"),
]


@pytest.mark.parametrize("key,ct", IVAL)
def test_appendix_a1(key: str, ct: str) -> None:
    tf = Twofish(bytes.fromhex(key))
    assert tf.encrypt_block(bytes(16)).hex().upper() == ct
    assert tf.decrypt_block(bytes.fromhex(ct)) == bytes(16)


def test_appendix_a1_subkeys_zero_key() -> None:
    k, s = key_schedule(bytes(16))
    assert s == [0, 0]
    assert k[:8] == [0x52C54DDE, 0x11F0626D, 0x7CAC9D4A, 0x4D1B4AAA,
                     0xB7B83A10, 0x1E7D0BEB, 0xEE9C341F, 0xCFE14BE4]
    assert k[8:10] == [0xF98FFEF9, 0x9C5B3C17]


# Appendix A.2 "Full Encryptions" (file ecb_tbl.txt): for I = 1..49, the
# plaintext is the previous ciphertext, and the key is the previous plaintext
# followed by the previous key, cut to the key size.
TBL = [
    (16, 1, "9F589F5CF6122C32B6BFEC2F2AE8C35A"),
    (16, 2, "D491DB16E7B1C39E86CB086B789F5419"),
    (16, 3, "019F9809DE1711858FAAC3A3BA20FBC3"),
    (16, 49, "5D9D4EEFFA9151575524F115815A12E0"),
    (24, 49, "E75449212BEEF9F4A390BD860A640941"),
    (32, 1, "57FF739D4DC92C1BD7FC01700CC8216F"),
    (32, 2, "D43BB7556EA32E46F2A282B7D45B4E0D"),
    (32, 49, "37FE26FF1CF66175F5DDF4C33B97A205"),
]


def _chain(keylen: int, steps: int) -> list[bytes]:
    key, pt, out = bytes(keylen), bytes(16), []
    for _ in range(steps):
        ct = Twofish(key).encrypt_block(pt)
        out.append(ct)
        key, pt = (pt + key)[:keylen], ct
    return out


def test_appendix_a2_tables() -> None:
    chains = {n: _chain(n, 49) for n in (16, 24, 32)}
    for keylen, i, ct in TBL:
        assert chains[keylen][i - 1].hex().upper() == ct


def test_q_are_permutations() -> None:
    assert sorted(Q0) == list(range(256))
    assert sorted(Q1) == list(range(256))


def test_round_trip_random() -> None:
    rng = random.Random(13)
    for n in (16, 24, 32):
        tf = Twofish(rng.randbytes(n))
        for _ in range(5):
            m = rng.randbytes(16)
            assert tf.decrypt_block(tf.encrypt_block(m)) == m
