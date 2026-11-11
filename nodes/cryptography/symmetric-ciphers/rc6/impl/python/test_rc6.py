# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rc6/. The authors are listed in prov/FKPS33.jsonl.

import random

import pytest

from rc6 import decrypt_block, encrypt_block

# Rivest, Robshaw, Sidney and Yin, "The RC6 Block Cipher", version 1.1,
# August 20, 1998, Appendix, "Test vectors for encryption with RC6" (RC6-32/20/b).
VECTORS = [
    ("00000000000000000000000000000000",
     "00000000000000000000000000000000",
     "8fc3a53656b1f778c129df4e9848a41e"),
    ("02132435465768798a9bacbdcedfe0f1",
     "0123456789abcdef0112233445566778",
     "524e192f4715c6231f51f6367ea43f18"),
    ("00000000000000000000000000000000",
     "000000000000000000000000000000000000000000000000",
     "6cd61bcb190b30384e8a3f168690ae82"),
    ("02132435465768798a9bacbdcedfe0f1",
     "0123456789abcdef0112233445566778899aabbccddeeff0",
     "688329d019e505041e52e92af95291d4"),
    ("00000000000000000000000000000000",
     "0000000000000000000000000000000000000000000000000000000000000000",
     "8f5fbd0510d15fa893fa3fda6e857ec2"),
    ("02132435465768798a9bacbdcedfe0f1",
     "0123456789abcdef0112233445566778899aabbccddeeff01032547698badcfe",
     "c8241816f0d7e48920ad16a1674e5d48"),
]


@pytest.mark.parametrize("pt,key,ct", VECTORS)
def test_rc6_paper_appendix(pt: str, key: str, ct: str) -> None:
    k = bytes.fromhex(key)
    assert encrypt_block(k, bytes.fromhex(pt)).hex() == ct
    assert decrypt_block(k, bytes.fromhex(ct)).hex() == pt


def test_round_trip_other_parameters() -> None:
    rng = random.Random(9)
    for w in (16, 32, 64):
        for r in (1, 8, 20):
            key = rng.randbytes(rng.randrange(0, 40))
            m = rng.randbytes(w // 2)
            assert decrypt_block(key, encrypt_block(key, m, r, w), r, w) == m
