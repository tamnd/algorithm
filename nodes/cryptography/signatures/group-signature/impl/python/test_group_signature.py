# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/group-signature/. The authors are listed in prov/852SRK.jsonl.
"""Tests for the toy linear-size group signature on the group p = 2039."""

import random
from dataclasses import replace

import pytest

from group_signature import G, P, Q, GroupKey, Opening, Signature, judge, keygen, open_signature, sign, verify

RNG = random.Random(1)
MEMBER_KEYS = [keygen(RNG) for _ in range(5)]
X_O, Y_O = keygen(RNG)
GK = GroupKey(tuple(y for _, y in MEMBER_KEYS), Y_O)


def test_group() -> None:
    assert P == 2 * Q + 1 and pow(G, Q, P) == 1 and G != 1
    assert len(set(GK.members)) == 5


def test_every_member_can_sign() -> None:
    rng = random.Random(2)
    for i, (x, _) in enumerate(MEMBER_KEYS):
        msg = b"vote %d" % i
        sig = sign(GK, i, x, msg, rng)
        assert verify(GK, msg, sig)
        assert not verify(GK, msg + b"!", sig)


def test_opener_finds_the_signer_and_proves_it() -> None:
    rng = random.Random(3)
    for i, (x, _) in enumerate(MEMBER_KEYS):
        sig = sign(GK, i, x, b"m", rng)
        op = open_signature(GK, X_O, b"m", sig, rng)
        assert op.index == i and judge(GK, b"m", sig, op)


def test_judge_rejects_a_false_opening() -> None:
    rng = random.Random(4)
    sig = sign(GK, 1, MEMBER_KEYS[1][0], b"m", rng)
    op = open_signature(GK, X_O, b"m", sig, rng)
    for k in range(5):
        if k != 1:
            assert not judge(GK, b"m", sig, replace(op, index=k, y=GK.members[k]))
    assert not judge(GK, b"m", sig, replace(op, z=(op.z + 1) % Q))


def test_anonymity_needs_the_opening_key() -> None:
    """Without x_o the ciphertext hides the signer (under DDH): decrypting with
    a wrong key gives a non-member or the wrong member."""
    rng = random.Random(5)
    wrong = (X_O + 1) % Q
    for i, (x, _) in enumerate(MEMBER_KEYS):
        sig = sign(GK, i, x, b"m", rng)
        assert sig.C2 * pow(sig.C1, -wrong, P) % P != GK.members[i]


def test_outsiders_and_the_opener_cannot_sign() -> None:
    rng = random.Random(6)
    outsider, _ = keygen(random.Random(99))
    with pytest.raises(ValueError):
        sign(GK, 0, outsider, b"m", rng)
    with pytest.raises(ValueError):
        sign(GK, 0, X_O, b"m", rng)  # the opener does not know x_0
    n = len(GK.members)
    fakes = [
        Signature(pow(G, rng.randrange(1, Q), P), pow(G, rng.randrange(1, Q), P),
                  tuple(rng.randrange(Q) for _ in range(n)), tuple(rng.randrange(Q) for _ in range(n)),
                  tuple(rng.randrange(Q) for _ in range(n)))
        for _ in range(30)
    ]
    assert not any(verify(GK, b"m", f) for f in fakes)


def test_ciphertext_cannot_be_changed() -> None:
    """Re-encrypting to point at another member breaks the proof."""
    rng = random.Random(7)
    sig = sign(GK, 2, MEMBER_KEYS[2][0], b"m", rng)
    shift = GK.members[3] * pow(GK.members[2], -1, P) % P
    assert not verify(GK, b"m", replace(sig, C2=sig.C2 * shift % P))
    assert not verify(GK, b"m", replace(sig, C1=sig.C1 * G % P))
    with pytest.raises(ValueError):
        open_signature(GK, X_O, b"m", replace(sig, C2=sig.C2 * shift % P), rng)
    assert isinstance(open_signature(GK, X_O, b"m", sig, rng), Opening)
