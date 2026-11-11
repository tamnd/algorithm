# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shake/. The authors are listed in prov/WR6HQ2.jsonl.

import hashlib

from shake import Shake, shake128, shake256

M1600 = bytes([0xA3]) * 200

# NIST, Cryptographic Standards and Guidelines, Example Values: SHAKE128_Msg0.pdf,
# SHAKE128_Msg1600.pdf, SHAKE256_Msg0.pdf and SHAKE256_Msg1600.pdf. Each example
# gives 4096 bits (512 bytes) of output; the first 32 and the last 32 bytes are copied by hand.
NIST = [
    (shake128, b"",
     "7f9c2ba4e88f827d616045507605853ed73b8093f6efbc88eb1a6eacfa66ef26",
     "43e41b45a653f2a5c4492c1add544512dda2529833462b71a41a45be97290b6f"),
    (shake128, M1600,
     "131ab8d2b594946b9c81333f9bb6e0ce75c3b93104fa3469d3917457385da037",
     "44c9fb359fd56ac0a9a75a743cff6862f17d7259ab075216c0699511643b6439"),
    (shake256, b"",
     "46b9dd2b0ba88d13233b3feb743eeb243fcd52ea62b81b82b50c27646ed5762f",
     "ab0bae316339894304e35877b0c28a9b1fd166c796b9cc258a064a8f57e27f2a"),
    (shake256, M1600,
     "cd8a920ed141aa0407a22d59288652e9d9f1a7ee0c1e7c1ca699424da84a904d",
     "6a1a9d7846436e4dca5728b6f760eef0ca92bf0be5615e96959d767197a0beeb"),
]


def test_nist_examples() -> None:
    for fn, msg, head, tail in NIST:
        out = fn(msg, 512)
        assert out[:32].hex() == head, fn.__name__
        assert out[-32:].hex() == tail, fn.__name__


def test_prefix_property() -> None:
    long = shake128(b"abc", 400)
    for n in (0, 1, 31, 32, 167, 168, 169, 336, 399):
        assert shake128(b"abc", n) == long[:n]


def test_read_in_pieces() -> None:
    whole = shake256(b"pieces", 500)
    for step in (1, 7, 136, 137):
        s = Shake(256, b"pieces")
        got = b""
        while len(got) < 500:
            got += s.read(min(step, 500 - len(got)))
        assert got == whole


def test_against_hashlib() -> None:
    for n in (0, 1, 135, 136, 137, 167, 168, 169, 300):
        msg = bytes((11 * i) & 255 for i in range(n))
        assert shake128(msg, 200) == hashlib.shake_128(msg).digest(200)
        assert shake256(msg, 200) == hashlib.shake_256(msg).digest(200)


def test_domain_separation_from_sha3() -> None:
    # SHAKE256 and SHA3-256 share the rate of 136 bytes but differ in the suffix bits.
    assert shake256(b"", 32) != hashlib.sha3_256(b"").digest()
