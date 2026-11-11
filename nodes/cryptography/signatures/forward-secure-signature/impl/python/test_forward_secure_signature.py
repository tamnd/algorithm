# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/forward-secure-signature/. The authors are listed in prov/CZN1Q6.jsonl.
"""Tests for the tree-based forward-secure signature (8 periods, 2 keys each)."""

import dataclasses

import pytest

from forward_secure_signature import (
    G,
    FixedSeedSigner,
    ForwardSecureSigner,
    Signature,
    sign_with_leak,
    verify,
)

H_, B_ = 3, 1
SEED = bytes(range(32))


def test_all_periods_sign_and_verify() -> None:
    s = ForwardSecureSigner(H_, B_, SEED)
    pk = s.public_key
    old: list[tuple[bytes, Signature]] = []
    for t in range(1 << H_):
        for k in range(1 << B_):
            m = b"period %d message %d" % (t, k)
            sig = s.sign(m)
            assert (sig.t, sig.j) == (t, k)
            assert verify(pk, H_, B_, m, sig)
            old.append((m, sig))
        with pytest.raises(RuntimeError):
            s.sign(b"one too many")
        if t + 1 < 1 << H_:
            s.update()
    with pytest.raises(RuntimeError):
        s.update()
    # Signatures of past periods stay valid after the key has moved on.
    assert all(verify(pk, H_, B_, m, sig) for m, sig in old)


def test_signature_binds_message_and_period() -> None:
    s = ForwardSecureSigner(H_, B_, SEED)
    s.update()
    sig = s.sign(b"contract")
    assert verify(s.public_key, H_, B_, b"contract", sig)
    assert not verify(s.public_key, H_, B_, b"contract!", sig)
    assert not verify(s.public_key, H_, B_, b"contract", dataclasses.replace(sig, t=0))
    assert not verify(s.public_key, H_, B_, b"contract", dataclasses.replace(sig, t=8))


def test_leak_does_not_help_for_earlier_periods() -> None:
    s = ForwardSecureSigner(H_, B_, SEED)
    for _ in range(4):
        s.update()
    leak = s.leak()
    assert leak[0] == 4
    pk = s.public_key
    # The leaked key contains no seed of periods 0 to 3.
    earlier = [SEED, G(SEED), G(G(SEED)), G(G(G(SEED)))]
    assert leak[1] == G(earlier[3])
    assert not any(e in leak for e in earlier)
    # The attacker can sign now and later: forward security does not protect the future.
    for t in (4, 7):
        assert verify(pk, H_, B_, b"evil", sign_with_leak(leak, t, B_, 0, b"evil"))
    # Using the leaked seed as if it were an earlier seed gives wrong keys.
    for t in range(4):
        fake = sign_with_leak((t, leak[1], leak[2]), t, B_, 0, b"backdated")
        assert not verify(pk, H_, B_, b"backdated", fake)
    with pytest.raises(ValueError):
        sign_with_leak(leak, 1, B_, 0, b"backdated")


def test_fixed_master_seed_is_not_forward_secure() -> None:
    s = FixedSeedSigner(H_, B_, SEED)
    for _ in range(4):
        s.update()
    master = s.master  # part of the secret key in every period
    attacker = FixedSeedSigner(H_, B_, master)  # period 0 again
    sig = attacker.sign(b"backdated")
    assert sig.t == 0
    assert verify(s.public_key, H_, B_, b"backdated", sig)
