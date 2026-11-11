# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/winternitz-one-time-signature/. The authors are listed in prov/39CCX3.jsonl.
"""Tests for classic WOTS and WOTS+.

There are no official test vectors for the bare one-time scheme in this
form (RFC 8391 and FIPS 205 give WOTS+ only inside XMSS and SLH-DSA), so the
tests check the parameters, the round trip, the rejection of changes, and the
forgery that the checksum stops, on a toy digest of 16 bits.
"""

import random

import pytest

from winternitz_one_time_signature import (
    Params,
    base_w,
    chain,
    checksum_digits,
    digits,
    keygen,
    message_digest,
    sign,
    verify,
)


def det_rand(seed: int):
    return random.Random(seed).randbytes


@pytest.mark.parametrize(
    "w, len1, len2, length",
    [(4, 128, 5, 133), (16, 64, 3, 67), (256, 32, 2, 34)],
)
def test_parameters_n32(w: int, len1: int, len2: int, length: int) -> None:
    p = Params(n=32, w=w, m=32)
    assert (p.len1, p.len2, p.length) == (len1, len2, length)


def test_base_w() -> None:
    assert base_w(bytes([0x12, 0x34]), 16, 4) == [1, 2, 3, 4]
    assert base_w(bytes([0x8F]), 4, 4) == [2, 0, 3, 3]


def test_example_digits() -> None:
    p = Params(n=32, w=4, m=1)
    assert message_digest(p, b"hi") == b"\x8f"
    assert digits(p, b"hi") == [2, 0, 3, 3, 1, 0]


@pytest.mark.parametrize("plus", [False, True])
@pytest.mark.parametrize("w", [4, 16, 256])
def test_round_trip(plus: bool, w: int) -> None:
    p = Params(w=w, plus=plus)
    sk, pk = keygen(p, det_rand(w))
    sig = sign(p, sk, pk, b"attack at dawn")
    assert len(sig) == p.length
    assert verify(p, pk, b"attack at dawn", sig)
    assert not verify(p, pk, b"attack at dusk", sig)


@pytest.mark.parametrize("plus", [False, True])
def test_changed_signature_fails(plus: bool) -> None:
    p = Params(plus=plus)
    sk, pk = keygen(p, det_rand(1))
    sig = sign(p, sk, pk, b"hello")
    for i in (0, 33, p.length - 1):
        bad = list(sig)
        bad[i] = bytes([bad[i][0] ^ 1]) + bad[i][1:]
        assert not verify(p, pk, b"hello", bad)
    assert not verify(p, pk, b"hello", sig[:-1])


def test_masks_matter_in_wots_plus() -> None:
    p = Params()
    sk, pk = keygen(p, det_rand(2))
    sig = sign(p, sk, pk, b"m")
    other = type(pk)(pk.ends, pk.k, [bytes(p.n)] * (p.w - 1))
    assert not verify(p, other, b"m", sig)


def test_chain_composes() -> None:
    p = Params()
    _, pk = keygen(p, det_rand(3))
    x = bytes(range(32))
    assert chain(p, pk, chain(p, pk, x, 0, 5), 5, 10) == chain(p, pk, x, 0, 15)


# ------------------------------------- the forgery without checksum (toy m)


def dominates(b_new: list[int], b_old: list[int]) -> bool:
    """A forger can walk each chain forward from b_old to b_new."""
    return all(x >= y for x, y in zip(b_new, b_old))


@pytest.mark.parametrize("plus", [False, True])
def test_forgery_without_checksum(plus: bool) -> None:
    # Toy digest of m = 2 bytes and w = 16: four message digits.
    p = Params(w=16, m=2, plus=plus)
    sk, pk = keygen(p, det_rand(4))
    m1 = b"pay Bob 10"
    sig = sign(p, sk, pk, m1)
    b1 = digits(p, m1)
    msg1 = b1[: p.len1]
    # The attacker walks the message chains forward and drops the checksum.
    for i in range(1 << 16):
        cand = b"pay Eve %d" % i
        b2 = digits(p, cand)
        if b2[: p.len1] != msg1 and dominates(b2[: p.len1], msg1):
            break
    forged = [chain(p, pk, sig[j], msg1[j], b2[j] - msg1[j]) for j in range(p.len1)]
    # A verifier with no checksum accepts.
    ok = all(
        chain(p, pk, forged[j], b2[j], p.w - 1 - b2[j]) == pk.ends[j] for j in range(p.len1)
    )
    assert ok
    # With the checksum some checksum digit went down, so the chain must go back.
    assert not dominates(b2[p.len1 :], b1[p.len1 :])


def test_checksum_stops_every_forward_walk() -> None:
    # Over all 2^16 digests: no other digest dominates the signed one.
    p = Params(w=16, m=2)
    signed = [3, 0, 12, 7]
    full = signed + checksum_digits(p, signed)
    count_plain = count_full = 0
    for v in range(1 << 16):
        d = [(v >> s) & 15 for s in (12, 8, 4, 0)]
        if d == signed:
            continue
        if dominates(d, signed):
            count_plain += 1
            if dominates(d + checksum_digits(p, d), full):
                count_full += 1
    assert count_plain == 13 * 16 * 4 * 9 - 1
    assert count_full == 0
