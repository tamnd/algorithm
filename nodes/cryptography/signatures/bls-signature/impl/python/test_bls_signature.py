# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bls-signature/. The authors are listed in prov/BWP8XH.jsonl.

import random

from bls_signature import (
    C,
    GEN,
    P,
    R,
    add,
    aggregate,
    f2_pow,
    hash_to_g1,
    in_g1,
    keygen,
    mul,
    neg,
    pairing,
    pop_prove,
    pop_verify,
    rogue_key,
    sign,
    sign_aug,
    verify,
    verify_aug_aggregate,
    verify_same_message,
)


def test_parameters() -> None:
    assert P + 1 == C * R and P % 4 == 3
    assert in_g1(GEN)


def test_pairing_is_bilinear_and_nondegenerate() -> None:
    rng = random.Random(2001)
    base = pairing(GEN, GEN)
    assert base != (1, 0) and f2_pow(base, R) == (1, 0)
    for _ in range(3):
        a, b = rng.randrange(1, R), rng.randrange(1, R)
        assert pairing(mul(a, GEN), mul(b, GEN)) == f2_pow(base, a * b % R)
    h = hash_to_g1(b"x")
    assert pairing(h, GEN) == pairing(GEN, h)  # symmetric


def test_sign_and_verify() -> None:
    rng = random.Random(2004)
    x = rng.randrange(1, R)
    pk = keygen(x)
    sig = sign(x, b"hello")
    assert verify(pk, b"hello", sig)
    assert not verify(pk, b"hellp", sig)
    assert not verify(keygen(x + 1), b"hello", sig)
    assert not verify(pk, b"hello", add(sig, GEN))
    assert sign(x, b"hello") == sig  # unique: one valid signature per message


def test_rogue_key_attack_on_naive_same_message_aggregation() -> None:
    rng = random.Random(7)
    victim_x = rng.randrange(1, R)
    victim_pk = keygen(victim_x)
    beta = rng.randrange(1, R)
    pk_star = rogue_key(victim_pk, beta)
    msg = b"transfer everything to the attacker"
    forged = mul(beta, hash_to_g1(msg))  # the attacker alone makes it
    # The naive check accepts, as if both keys had signed.
    assert verify_same_message([victim_pk, pk_star], msg, forged)
    # Fix 1, proof of possession: the attacker cannot prove a key for pk_star.
    fake_proof = mul(beta, GEN)  # any guess; the right one needs log(pk_star)
    assert not pop_verify(pk_star, fake_proof)
    assert pop_verify(victim_pk, pop_prove(victim_x))
    # Fix 2, message augmentation: each signer signs pk_i || m.
    assert not verify_aug_aggregate([victim_pk, pk_star], [msg, msg], forged)


def test_honest_aggregation() -> None:
    rng = random.Random(9)
    xs = [rng.randrange(1, R) for _ in range(3)]
    pks = [keygen(x) for x in xs]
    msg = b"block 42"
    agg = aggregate([sign(x, msg) for x in xs])
    assert all(pop_verify(pk, pop_prove(x)) for pk, x in zip(pks, xs))
    assert verify_same_message(pks, msg, agg)
    agg_aug = aggregate([sign_aug(x, msg) for x in xs])
    assert verify_aug_aggregate(pks, [msg] * 3, agg_aug)
    assert not verify_aug_aggregate(pks, [msg] * 3, add(agg_aug, neg(sign_aug(xs[0], msg))))
