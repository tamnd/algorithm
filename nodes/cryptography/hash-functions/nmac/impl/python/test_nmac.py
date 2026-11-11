# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/nmac/. The authors are listed in prov/81YGXR.jsonl.

import hashlib
import hmac
import random

from nmac import IV, compress, hmac_keys, hmac_via_nmac, keyed_hash, md_pad, nmac, sha256


def test_sha256_fips180_examples() -> None:
    # FIPS 180-4 examples (NIST "SHA256.pdf" example values): "abc" and the 448-bit message.
    assert sha256(b"abc").hex() == "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
    two_block = b"abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq"
    assert sha256(two_block).hex() == "248d6a61d20638b8e5c026930c3e6039a33ce45964ff2167f6ecedd419db06c1"


def test_compression_function_matches_hashlib_on_full_hash() -> None:
    rng = random.Random(1)
    for n in [0, 1, 55, 56, 63, 64, 65, 119, 120, 200]:
        x = rng.randbytes(n)
        assert sha256(x) == hashlib.sha256(x).digest()


def test_hmac_is_nmac_with_derived_keys() -> None:
    # Lemma 3 of the HMAC page: HMAC-SHA-256 = NMAC(k1, k2) with the padding offset 64.
    rng = random.Random(2)
    for _ in range(20):
        key = rng.randbytes(rng.randrange(0, 65))
        m = rng.randbytes(rng.randrange(0, 150))
        assert hmac_via_nmac(key, m) == hmac.new(key, m, "sha256").digest()


def test_rfc4231_case2_through_nmac() -> None:
    # RFC 4231, Section 4.3, Test Case 2, computed with the NMAC form.
    tag = hmac_via_nmac(b"Jefe", b"what do ya want for nothing?")
    assert tag.hex() == "5bdcc146bf60754e6a042426089575c75a003f089d2739839dec58b964ec3843"


def test_wrong_key_changes_tag() -> None:
    rng = random.Random(3)
    k1, k2 = rng.randbytes(32), rng.randbytes(32)
    m = b"transfer 10"
    t = nmac(k1, k2, m)
    assert nmac(k1, k2, m) == t
    assert nmac(rng.randbytes(32), k2, m) != t
    assert nmac(k1, rng.randbytes(32), m) != t
    assert nmac(k2, k1, m) != t


def test_inner_function_alone_has_length_extension() -> None:
    # F_k2 by itself is not a MAC: from F_k2(m) and |m| anyone computes F_k2 of an extension.
    rng = random.Random(4)
    k2 = rng.randbytes(32)
    m = b"amount=10"
    t = keyed_hash(k2, m)  # the "tag" an attacker sees
    suffix = b"&amount=1000000"
    glue = md_pad(len(m))
    forged_msg = m + glue + suffix
    forged = keyed_hash(t, suffix, offset=len(m) + len(glue))  # no key used
    assert forged == keyed_hash(k2, forged_msg)
    # The outer layer of NMAC stops this: the same trick fails on the full NMAC.
    k1 = rng.randbytes(32)
    tag = nmac(k1, k2, m)
    assert keyed_hash(tag, suffix, offset=len(m) + len(glue)) != nmac(k1, k2, forged_msg)


def test_avalanche() -> None:
    rng = random.Random(5)
    k1, k2 = rng.randbytes(32), rng.randbytes(32)
    total, trials = 0, 100
    for _ in range(trials):
        m = bytearray(rng.randbytes(20))
        a = int.from_bytes(nmac(k1, k2, bytes(m)), "big")
        m[rng.randrange(20)] ^= 1 << rng.randrange(8)
        b = int.from_bytes(nmac(k1, k2, bytes(m)), "big")
        total += bin(a ^ b).count("1")
    assert 118 < total / trials < 138


def test_derived_keys_are_compression_outputs() -> None:
    k1, k2 = hmac_keys(b"Jefe")
    kp = b"Jefe" + bytes(60)
    assert k1 == compress(IV, bytes(x ^ 0x5C for x in kp))
    assert k2 == compress(IV, bytes(x ^ 0x36 for x in kp))
    assert k1 != k2
