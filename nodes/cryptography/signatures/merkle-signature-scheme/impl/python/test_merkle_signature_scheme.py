# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/merkle-signature-scheme/. The authors are listed in prov/RTX97D.jsonl.
"""Tests for the Merkle signature scheme with Winternitz leaves.

The textbook MSS has no official test vectors (the standard forms are LMS
and XMSS, tested on their own pages), so the tests check the round trip for
every leaf, the state, and the rejection of changed signatures.
"""

import copy

import pytest

from merkle_signature_scheme import (
    MerkleSigner,
    Signature,
    leaf_from_wots_pk,
    parent,
    verify,
    wots_leaf,
    wots_pk_from_sig,
)

SEED = bytes(range(32))


@pytest.fixture(scope="module")
def signer4() -> MerkleSigner:
    return MerkleSigner(4, SEED)


def test_every_leaf_signs_once_h4(signer4: MerkleSigner) -> None:
    s = copy.deepcopy(signer4)
    for q in range(16):
        msg = b"message %d" % q
        sig = s.sign(msg)
        assert sig.q == q
        assert verify(s.root, 4, msg, sig)
        assert not verify(s.root, 4, msg + b"!", sig)
    with pytest.raises(RuntimeError):
        s.sign(b"one too many")


def test_height_6_round_trip() -> None:
    s = MerkleSigner(6, bytes(32))
    s.next_q = 45
    sig = s.sign(b"hello")
    assert sig.q == 45 and len(sig.auth) == 6
    assert verify(s.root, 6, b"hello", sig)


def test_leaf_rebuilt_from_signature(signer4: MerkleSigner) -> None:
    s = copy.deepcopy(signer4)
    s.next_q = 9
    sig = s.sign(b"x")
    assert leaf_from_wots_pk(wots_pk_from_sig(b"x", sig.ots)) == wots_leaf(SEED, 9)


def test_auth_path_by_hand(signer4: MerkleSigner) -> None:
    # Leaf 6 = 0110: siblings are leaf 7, node (1,2), node (2,0), node (3,1).
    t = signer4.tree
    assert signer4.auth_path(6) == [t[0][7], t[1][2], t[2][0], t[3][1]]
    node = parent(t[0][6], t[0][7])
    node = parent(t[1][2], node)
    node = parent(t[2][0], node)
    node = parent(node, t[3][1])
    assert node == signer4.root


def test_changed_parts_fail(signer4: MerkleSigner) -> None:
    s = copy.deepcopy(signer4)
    s.next_q = 5
    sig = s.sign(b"pay Bob 10")
    root = s.root
    assert verify(root, 4, b"pay Bob 10", sig)
    assert not verify(root, 4, b"pay Bob 10", Signature(4, sig.ots, sig.auth))
    bad_auth = list(sig.auth)
    bad_auth[2] = bytes(32)
    assert not verify(root, 4, b"pay Bob 10", Signature(5, sig.ots, bad_auth))
    assert not verify(root, 4, b"pay Bob 10", Signature(5, sig.ots, sig.auth[:-1]))
    assert not verify(root, 4, b"pay Bob 10", Signature(16, sig.ots, sig.auth))


def test_restored_state_reuses_a_leaf(signer4: MerkleSigner) -> None:
    # A backup of the signer, restored after a signature, signs with the same
    # one-time key again. This is the main danger of stateful schemes.
    s = copy.deepcopy(signer4)
    backup = copy.deepcopy(s)
    a = s.sign(b"first")
    b = backup.sign(b"second")
    assert a.q == b.q == 0
    assert verify(s.root, 4, b"first", a) and verify(s.root, 4, b"second", b)
