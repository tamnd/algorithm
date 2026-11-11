# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sha-1/. The authors are listed in prov/THSRT9.jsonl.

import hashlib

from sha_1 import IV, compress, pad, sha1

ABC = b"abc"
M448 = b"abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq"

# The first 320 bytes of shattered-1.pdf and shattered-2.pdf (https://shattered.io/, 2017):
# a common 192-byte prefix, then two different pairs of 64-byte blocks.
PREFIX = bytes.fromhex(
    "255044462d312e330a25e2e3cfd30a0a0a312030206f626a0a3c3c2f57696474"
    "682032203020522f4865696768742033203020522f547970652034203020522f"
    "537562747970652035203020522f46696c7465722036203020522f436f6c6f72"
    "53706163652037203020522f4c656e6774682038203020522f42697473506572"
    "436f6d706f6e656e7420383e3e0a73747265616d0affd8fffe00245348412d31"
    "20697320646561642121212121852fec092339759c39b1a1c63c4c97e1fffe01"
)
BLOCKS1 = bytes.fromhex(
    "7346dc9166b67e118f029ab621b2560ff9ca67cca8c7f85ba84c79030c2b3de2"
    "18f86db3a90901d5df45c14f26fedfb3dc38e96ac22fe7bd728f0e45bce046d2"
    "3c570feb141398bb552ef5a0a82be331fea48037b8b5d71f0e332edf93ac3500"
    "eb4ddc0decc1a864790c782c76215660dd309791d06bd0af3f98cda4bc4629b1"
)
BLOCKS2 = bytes.fromhex(
    "7f46dc93a6b67e013b029aaa1db2560b45ca67d688c7f84b8c4c791fe02b3df6"
    "14f86db1690901c56b45c1530afedfb76038e972722fe7ad728f0e4904e046c2"
    "30570fe9d41398abe12ef5bc942be33542a4802d98b5d70f2a332ec37fac3514"
    "e74ddc0f2cc1a874cd0c78305a21566461309789606bd0bf3f98cda8044629a1"
)


# NIST, Cryptographic Standards and Guidelines, Example Values, SHA1.pdf, "SHA-1 Example (One-Block Message)".
def test_nist_one_block() -> None:
    assert sha1(ABC).hex() == "a9993e364706816aba3e25717850c26c9cd0d89d"


# NIST Example Values, SHA1.pdf, "SHA-1 Example (Multi-Block Message)", the 448-bit message.
def test_nist_two_block() -> None:
    assert len(M448) * 8 == 448
    assert sha1(M448).hex() == "84983e441c3bd26ebaae4aa1f95129e5e54670f1"


# NIST Example Values, SHA1.pdf, the register values A..E for "abc" after steps t = 0 and t = 1.
def test_nist_trace() -> None:
    trace: list = []
    compress(IV, pad(ABC), trace)
    assert trace[0] == (0x0116FC33, 0x67452301, 0x7BF36AE2, 0x98BADCFE, 0x10325476)
    assert trace[1][0] == 0x8990536D


def test_shattered_prefix_collides() -> None:
    m1 = PREFIX + BLOCKS1
    m2 = PREFIX + BLOCKS2
    assert m1 != m2 and len(m1) == 320
    assert sha1(m1) == sha1(m2)
    # The chaining values agree after the 5 blocks, so a common suffix keeps the collision.
    assert sha1(m1 + b"%%EOF") == sha1(m2 + b"%%EOF")
    assert hashlib.sha1(m1).digest() == hashlib.sha1(m2).digest()


def test_against_hashlib() -> None:
    for n in range(0, 150, 11):
        msg = bytes((7 * i) & 255 for i in range(n))
        assert sha1(msg) == hashlib.sha1(msg).digest()
