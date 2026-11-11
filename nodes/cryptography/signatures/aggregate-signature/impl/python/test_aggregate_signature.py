# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/aggregate-signature/. The authors are listed in prov/YB3MDA.jsonl.

import random

from aggregate_signature import (
    GEN,
    R,
    add,
    aggregate,
    aggregate_verify,
    f2_pow,
    hash_to_g1,
    keygen,
    mul,
    neg,
    pairing,
    rogue_key,
    sign,
)


def test_pairing_is_bilinear() -> None:
    base = pairing(GEN, GEN)
    assert base != (1, 0)
    assert pairing(mul(3, GEN), mul(5, GEN)) == f2_pow(base, 15)


def test_aggregate_of_distinct_messages_verifies() -> None:
    rng = random.Random(2003)
    xs = [rng.randrange(1, R) for _ in range(4)]
    pks = [keygen(x) for x in xs]
    msgs = [b"tx %d" % i for i in range(4)]
    agg = aggregate([sign(x, m) for x, m in zip(xs, msgs)])
    assert aggregate_verify(pks, msgs, agg)
    # A changed message, a dropped signature or a swapped key fails.
    assert not aggregate_verify(pks, msgs[:3] + [b"tx 9"], agg)
    assert not aggregate_verify(pks, msgs, add(agg, neg(sign(xs[0], msgs[0]))))
    assert not aggregate_verify([pks[1], pks[0]] + pks[2:], msgs, agg)


def test_rogue_key_with_equal_messages_and_no_pop() -> None:
    rng = random.Random(2004)
    victim_pk = keygen(rng.randrange(1, R))
    beta = rng.randrange(1, R)
    pk_star = rogue_key(victim_pk, beta)
    msg = b"the victim agrees to pay"
    forged = mul(beta, hash_to_g1(msg))
    # Without the distinct-message rule the forgery passes as a signature of both keys.
    assert aggregate_verify([victim_pk, pk_star], [msg, msg], forged, distinct=False)
    # With the rule of BGLS it is rejected.
    assert not aggregate_verify([victim_pk, pk_star], [msg, msg], forged)
    # With distinct messages the same trick does not work.
    assert not aggregate_verify([victim_pk, pk_star], [msg, msg + b"!"], forged, distinct=False)


def test_splitting_zero() -> None:
    # Two wrong signatures that add up to the right aggregate pass: an aggregate
    # proves the set, not each member.
    rng = random.Random(5)
    xs = [rng.randrange(1, R) for _ in range(2)]
    msgs = [b"a", b"b"]
    sigs = [sign(x, m) for x, m in zip(xs, msgs)]
    delta = mul(77, GEN)
    bad = [add(sigs[0], delta), add(sigs[1], neg(delta))]
    assert aggregate_verify([keygen(x) for x in xs], msgs, aggregate(bad))
