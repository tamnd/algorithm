# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ring-signature/. The authors are listed in prov/6JAF6Z.jsonl.
"""Tests for the AOS Schnorr ring signature on the toy group p = 2039."""

import random
from dataclasses import replace

import pytest

from ring_signature import G, P, Q, Signature, coins_for, keygen, sign, verify


def ring_of(n: int, seed: int) -> tuple[list[int], list[int]]:
    rng = random.Random(seed)
    keys = [keygen(rng) for _ in range(n)]
    return [x for x, _ in keys], [y for _, y in keys]


def test_group() -> None:
    assert P == 2 * Q + 1 and pow(G, Q, P) == 1 and G != 1


@pytest.mark.parametrize("n", [1, 2, 5])
def test_every_member_can_sign(n: int) -> None:
    xs, ring = ring_of(n, n)
    for s in range(n):
        msg = b"leak %d" % s
        sig = sign(ring, s, xs[s], msg)
        assert verify(ring, msg, sig)
        assert not verify(ring, msg + b"!", sig)
        if n > 1:
            assert not verify(ring[1:] + ring[:1], msg, sig)  # another ring order


def test_signature_does_not_reveal_the_signer() -> None:
    """A signature made by member 2 could have been made, with the same
    probability, by any member: each has exactly one choice of coins that
    gives this very signature."""
    xs, ring = ring_of(4, 7)
    msg = b"the minister lied"
    sig = sign(ring, 2, xs[2], msg)
    for j in range(4):
        again = sign(ring, j, xs[j], msg, coins=coins_for(ring, msg, sig, j, xs[j]))
        assert again == sig


def test_non_members_cannot_sign() -> None:
    xs, ring = ring_of(3, 11)
    outsider, _ = keygen(random.Random(99))
    with pytest.raises(ValueError):
        sign(ring, 0, outsider, b"m")
    rng = random.Random(5)
    fakes = [Signature(rng.randrange(Q), tuple(rng.randrange(Q) for _ in ring)) for _ in range(30)]
    assert not any(verify(ring, b"m", f) for f in fakes)
    sig = sign(ring, 1, xs[1], b"m")
    assert not verify(ring, b"m", replace(sig, e0=(sig.e0 + 1) % Q))
    assert not verify(ring[:2] + [1], b"m", sig)  # 1 is not a valid key
