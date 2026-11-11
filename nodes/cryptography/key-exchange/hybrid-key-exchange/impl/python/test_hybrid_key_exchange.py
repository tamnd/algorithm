# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hybrid-key-exchange/. The authors are listed in prov/TTAAD5.jsonl.

import random

from hybrid_key_exchange import combine, kem_decaps, kem_encaps, kem_keygen, run, x25519, x25519_base

H = bytes.fromhex

# RFC 7748 Section 6.1, copied by hand.
ALICE_PRIV = "77076d0a7318a57d3c16c17251b26645df4c2f87ebc0992ab177fba51db92c2a"
ALICE_PUB = "8520f0098930a754748b7ddcb43ef75a0dbf3a0d26381af4eba4a98eaa9b4e6a"
BOB_PRIV = "5dab087e624a8a4b79e17f8b83800ee66f3bb1292618b6fd1c2f8b27ff88e0eb"
BOB_PUB = "de9edb7d7b7dc1b4d35b61c2ece435373f8343c85b78674dadfc7e146f882b4f"
SHARED = "4a5d9d5ba4ce2de1728e3bf480350f25e07e21c947d19e3376f09b3c1e161742"


def test_x25519_part_matches_rfc7748() -> None:
    assert x25519_base(H(ALICE_PRIV)).hex() == ALICE_PUB
    assert x25519_base(H(BOB_PRIV)).hex() == BOB_PUB
    assert x25519(H(ALICE_PRIV), H(BOB_PUB)).hex() == SHARED
    assert x25519(H(BOB_PRIV), H(ALICE_PUB)).hex() == SHARED


def test_toy_kem_is_correct() -> None:
    rng = random.Random(203)
    for _ in range(10):
        pk, sk = kem_keygen(rng)
        ct, ss = kem_encaps(pk, rng)
        assert kem_decaps(sk, ct) == ss


def test_both_sides_get_the_same_key() -> None:
    for seed in range(3):
        key_c, key_s, _ = run(seed)
        assert key_c == key_s and len(key_c) == 32


def test_key_stays_secret_if_one_component_leaks() -> None:
    _, key, s = run(42)
    rng = random.Random(7)
    # The classical part is broken: Eve learns ss_ec, but not ss_pq.
    for _ in range(100):
        assert combine(rng.randbytes(32), s["ss_ec"], s["transcript"]) != key
    # The post-quantum part is broken: Eve learns ss_pq, but not ss_ec.
    for _ in range(100):
        assert combine(s["ss_pq"], rng.randbytes(32), s["transcript"]) != key
    # Only both parts together give the key.
    assert combine(s["ss_pq"], s["ss_ec"], s["transcript"]) == key


def test_key_is_bound_to_the_transcript() -> None:
    _, key, s = run(43)
    assert combine(s["ss_pq"], s["ss_ec"], s["transcript"] + b"x") != key


def test_a_bad_combiner_falls_with_one_component() -> None:
    # A careless design that keeps only the first 32 bytes of ss_ec | ss_pq
    # is just ss_ec, so breaking X25519 alone gives the key.
    _, _, s = run(44)
    bad_key = (s["ss_ec"] + s["ss_pq"])[:32]
    assert bad_key == s["ss_ec"]
