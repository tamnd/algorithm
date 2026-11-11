# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/deterministic-nonce-generation/. The authors are listed in prov/DR8QGH.jsonl.

import hashlib
import random

from deterministic_nonce_generation import (
    Q,
    bits2int,
    det_sign,
    hedged_sign,
    recover_from_fault,
    rfc6979_k,
)

# RFC 6979, Appendix A.2.5 (ECDSA, 256 bits, P-256), copied by hand.
P256_N = 0xFFFFFFFF00000000FFFFFFFFFFFFFFFFBCE6FAADA7179E84F3B9CAC2FC632551
P256_X = 0xC9AFA9D845BA75166B5C215767B1D6934E50C3DB36E89B127B8A622B120F6721
K_SAMPLE_SHA256 = 0xA6E3C57DD01ABE90086538398355DD4C3B17AA873382B0F24D6129493D8AAD60
K_TEST_SHA256 = 0xD16B6AE827F17175E040871A1C7EC3500192C4C92677336EC2537ACAEE0008E0


def test_rfc6979_a25_sample() -> None:
    h1 = hashlib.sha256(b"sample").digest()
    assert rfc6979_k(P256_X, h1, P256_N) == K_SAMPLE_SHA256


def test_rfc6979_a25_test() -> None:
    h1 = hashlib.sha256(b"test").digest()
    assert rfc6979_k(P256_X, h1, P256_N) == K_TEST_SHA256


def test_bits2int_keeps_leftmost_digits() -> None:
    assert bits2int(b"\xff\x00", 4) == 0xF
    assert bits2int(b"\x12\x34", 16) == 0x1234


def test_small_group_nonces_are_in_range_and_stable() -> None:
    ks = [rfc6979_k(77, hashlib.sha256(b"m%d" % i).digest(), Q) for i in range(200)]
    assert all(1 <= k < Q for k in ks)
    assert len(set(ks)) > 150  # different messages give different nonces
    assert ks[5] == rfc6979_k(77, hashlib.sha256(b"m5").digest(), Q)


def test_fault_on_deterministic_signer_leaks_key() -> None:
    x, msg = 345, b"pay 10 coins"
    good = det_sign(x, msg)
    assert det_sign(x, msg) == good  # deterministic
    bad = det_sign(x, msg, fault=True)
    assert recover_from_fault(msg, good, bad) == x


def test_hedged_signer_resists_the_same_fault() -> None:
    rng = random.Random(6979)
    x, msg = 345, b"pay 10 coins"
    leaks = 0
    for _ in range(50):
        good = hedged_sign(x, msg, rng)
        bad = hedged_sign(x, msg, rng, fault=True)
        leaks += recover_from_fault(msg, good, bad) == x
    assert leaks <= 2  # only by chance, about 1 in Q per try
