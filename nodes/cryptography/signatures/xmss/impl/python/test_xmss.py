# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/xmss/. The authors are listed in prov/CAW1KT.jsonl.
"""Tests for XMSS with small, non-standard tree heights (h = 4 and 5).

RFC 8391 has no test vectors in its text, so these tests check round trips,
the state, the L-tree, the sizes, and the rejection of changed signatures.
"""

import copy

import pytest

from xmss import (
    LEN,
    N,
    Adrs,
    XmssSigner,
    ltree,
    rand_hash,
    signature_bytes,
    verify,
    wots_digits,
)

SEEDS = (bytes([1]) * 32, bytes([2]) * 32, bytes([3]) * 32)


@pytest.fixture(scope="module")
def signer4() -> XmssSigner:
    return XmssSigner(4, *SEEDS)


def test_all_leaves_h4(signer4: XmssSigner) -> None:
    s = copy.deepcopy(signer4)
    pk = s.public_key()
    for i in range(16):
        sig = s.sign(b"msg %d" % i)
        assert sig[0] == i
        assert verify(pk, 4, b"msg %d" % i, sig)
        assert not verify(pk, 4, b"msg %d?" % i, sig)
    with pytest.raises(RuntimeError):
        s.sign(b"too many")


def test_h5_and_size() -> None:
    s = XmssSigner(5, bytes(32), bytes([9]) * 32, bytes([7]) * 32)
    s.idx = 21
    sig = s.sign(b"hello")
    assert verify(s.public_key(), 5, b"hello", sig)
    # 4 + n + len * n + h * n bytes, as in RFC 8391 Section 4.1.8
    assert len(signature_bytes(sig)) == 4 + N + LEN * N + 5 * N == 2340


def test_changes_rejected(signer4: XmssSigner) -> None:
    s = copy.deepcopy(signer4)
    s.idx = 6
    idx, r, ots, auth = s.sign(b"pay Bob 10")
    pk = s.public_key()
    assert verify(pk, 4, b"pay Bob 10", (idx, r, ots, auth))
    assert not verify(pk, 4, b"pay Bob 10", (7, r, ots, auth))
    assert not verify(pk, 4, b"pay Bob 10", (idx, bytes(32), ots, auth))
    assert not verify(pk, 4, b"pay Bob 10", (idx, r, ots, auth[:-1] + [bytes(32)]))
    assert not verify(pk, 4, b"pay Bob 10", (16, r, ots, auth))
    # A different public seed gives different bitmasks and keys.
    assert not verify((pk[0], bytes(32)), 4, b"pay Bob 10", (idx, r, ots, auth))


def test_randomized_message_hash_differs_per_index(signer4: XmssSigner) -> None:
    s = copy.deepcopy(signer4)
    a = s.sign(b"same")
    b = s.sign(b"same")
    assert a[1] != b[1] and a[2] != b[2]


def test_checksum_digits() -> None:
    d = wots_digits(bytes(32))  # all message digits 0: checksum 64 * 15 = 960
    assert d[:64] == [0] * 64
    assert d[64:] == [0x3, 0xC, 0x0]  # 960 = 0x3C0


def test_ltree_carries_odd_node() -> None:
    seed = bytes(32)
    vals = [bytes([i]) * 32 for i in range(3)]
    a = Adrs()
    a.set_type(1)
    got = ltree(vals, seed, a.copy())
    b = Adrs()
    b.set_type(1)
    b.set_chain(0)
    b.set_hash(0)
    first = rand_hash(vals[0], vals[1], seed, b)
    b.set_chain(1)
    b.set_hash(0)
    assert got == rand_hash(first, vals[2], seed, b)


def test_restored_state_reuses_index(signer4: XmssSigner) -> None:
    s = copy.deepcopy(signer4)
    backup = copy.deepcopy(s)
    assert s.sign(b"a")[0] == backup.sign(b"b")[0] == 0
