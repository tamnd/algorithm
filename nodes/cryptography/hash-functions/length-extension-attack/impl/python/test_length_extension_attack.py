# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/length-extension-attack/. The authors are listed in prov/8W23N6.jsonl.

import hashlib
import hmac
import random
import secrets

from length_extension_attack import extend, padding, sha256

# FIPS 180-4 example values (NIST CSRC "Examples with intermediate values", SHA-256),
# copied by hand: one-block "abc" and the two-block 448-bit message.
ABC = "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
TWO_BLOCK_MSG = b"abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq"
TWO_BLOCK = "248d6a61d20638b8e5c026930c3e6039a33ce45964ff2167f6ecedd419db06c1"
EMPTY = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"


def test_fips_vectors() -> None:
    assert sha256(b"abc").hex() == ABC
    assert sha256(TWO_BLOCK_MSG).hex() == TWO_BLOCK
    assert sha256(b"").hex() == EMPTY


def test_against_hashlib() -> None:
    rng = random.Random(180)
    for length in list(range(0, 130)) + [rng.randrange(1000) for _ in range(30)]:
        data = bytes(rng.getrandbits(8) for _ in range(length))
        assert sha256(data) == hashlib.sha256(data).digest()


def test_padding_length() -> None:
    for n in range(200):
        assert (n + len(padding(n))) % 64 == 0
        assert 9 <= len(padding(n)) <= 72


class NaiveMac:
    """The weak MAC tag = SHA-256(key || msg), with a secret 16-byte key. A local simulated oracle."""

    def __init__(self) -> None:
        self._key = secrets.token_bytes(16)

    def tag(self, msg: bytes) -> bytes:
        return hashlib.sha256(self._key + msg).digest()

    def verify(self, msg: bytes, tag: bytes) -> bool:
        return hmac.compare_digest(self.tag(msg), tag)


def test_forgery_on_naive_mac() -> None:
    mac = NaiveMac()
    msg = b"user=alice&amount=10"
    tag = mac.tag(msg)
    msg2, tag2 = extend(tag, 16, msg, b"&amount=1000000")
    assert msg2.startswith(msg) and msg2.endswith(b"&amount=1000000")
    assert msg2 != msg
    assert mac.verify(msg2, tag2)


def test_forgery_for_many_lengths() -> None:
    rng = random.Random(2009)
    for _ in range(40):
        key = bytes(rng.getrandbits(8) for _ in range(rng.randrange(1, 70)))
        msg = bytes(rng.getrandbits(8) for _ in range(rng.randrange(0, 150)))
        extra = bytes(rng.getrandbits(8) for _ in range(rng.randrange(0, 100)))
        tag = hashlib.sha256(key + msg).digest()
        msg2, tag2 = extend(tag, len(key), msg, extra)
        assert hashlib.sha256(key + msg2).digest() == tag2


def test_wrong_key_length_fails() -> None:
    key = b"k" * 16
    tag = hashlib.sha256(key + b"data").digest()
    msg2, tag2 = extend(tag, 15, b"data", b"more")
    assert hashlib.sha256(key + msg2).digest() != tag2


def test_hmac_and_truncation_resist() -> None:
    key, msg, extra = b"k" * 16, b"data", b"more"
    t = hmac.new(key, msg, hashlib.sha256).digest()
    msg2, tag2 = extend(t, 16, msg, extra)
    assert hmac.new(key, msg2, hashlib.sha256).digest() != tag2
    t3 = hashlib.sha3_256(key + msg).digest()
    msg3, tag3 = extend(t3, 16, msg, extra)
    assert hashlib.sha3_256(key + msg3).digest() != tag3
