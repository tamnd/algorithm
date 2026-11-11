# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lamport-signature/. The authors are listed in prov/4WMP39.jsonl.
"""Tests for the Lamport one-time signature.

Lamport's scheme has no official test vectors (no standard defines it), so
the tests check the round trip, the rejection of changed messages and
signatures, the sizes, and the key reuse attack on a toy digest length.
"""

import itertools
import random

import pytest

from lamport_signature import (
    OneTimeSigner,
    compress_public_key,
    digest_bits,
    keygen,
    sign,
    verify,
)


def det_rand(seed: int):
    r = random.Random(seed)
    return r.randbytes


def test_round_trip_full_size() -> None:
    sk, pk = keygen(256, det_rand(1))
    sig = sign(sk, b"attack at dawn")
    assert verify(pk, b"attack at dawn", sig)
    assert not verify(pk, b"attack at dusk", sig)


def test_sizes() -> None:
    sk, pk = keygen(256, det_rand(2))
    sig = sign(sk, b"m")
    assert sum(len(x) for pair in sk for x in pair) == 2 * 256 * 32 == 16384
    assert sum(len(y) for pair in pk for y in pair) == 16384
    assert sum(len(s) for s in sig) == 256 * 32 == 8192
    assert len(compress_public_key(pk)) == 32


def test_changed_signature_fails() -> None:
    sk, pk = keygen(256, det_rand(3))
    sig = sign(sk, b"hello")
    for i in (0, 100, 255):
        bad = list(sig)
        bad[i] = bytes([bad[i][0] ^ 1]) + bad[i][1:]
        assert not verify(pk, b"hello", bad)
    assert not verify(pk, b"hello", sig[:-1])


def test_signature_reveals_the_chosen_halves() -> None:
    sk, pk = keygen(16, det_rand(4))
    d = digest_bits(b"abc", 16)
    sig = sign(sk, b"abc")
    assert all(sig[i] == sk[i][d[i]] for i in range(16))
    assert all(sig[i] != sk[i][1 - d[i]] for i in range(16))


def test_one_time_signer_refuses_second_message() -> None:
    s = OneTimeSigner(32, det_rand(5))
    sig = s.sign(b"first")
    assert verify(s.pk, b"first", sig)
    with pytest.raises(RuntimeError):
        s.sign(b"second")


# ------------------------------------------------- key reuse attack (toy n)


def revealed_values(signed: list[tuple[bytes, list[bytes]]], n: int) -> list[dict[int, bytes]]:
    """For each position, the secret halves that the signatures revealed."""
    rev: list[dict[int, bytes]] = [{} for _ in range(n)]
    for msg, sig in signed:
        d = digest_bits(msg, n)
        for i in range(n):
            rev[i][d[i]] = sig[i]
    return rev


def try_forge(rev: list[dict[int, bytes]], msg: bytes) -> list[bytes] | None:
    n = len(rev)
    d = digest_bits(msg, n)
    if all(d[i] in rev[i] for i in range(n)):
        return [rev[i][d[i]] for i in range(n)]
    return None


def test_two_signatures_give_a_forgery_toy() -> None:
    # Toy digest of n = 16 bits. The signer wrongly signs two messages.
    n = 16
    sk, pk = keygen(n, det_rand(6))
    m1, m2 = b"pay Bob 10", b"pay Carol 20"
    signed = [(m1, sign(sk, m1)), (m2, sign(sk, m2))]
    d1, d2 = digest_bits(m1, n), digest_bits(m2, n)
    e = sum(a == b for a, b in zip(d1, d2))  # positions where only one half is known
    rev = revealed_values(signed, n)
    found = None
    tries = 0
    for i in range(1 << 16):
        tries += 1
        cand = b"pay Eve %d" % i
        f = try_forge(rev, cand)
        if f is not None:
            found = (cand, f)
            break
    assert found is not None
    cand, forged = found
    assert cand not in (m1, m2)
    assert verify(pk, cand, forged)
    # The chance that one random message is forgeable is 2^(-e).
    assert 0 < e < n
    assert tries < 40 * 2**e


def test_forgeable_fraction_is_two_to_minus_e() -> None:
    # Count every n-bit target digest that the revealed halves cover.
    n = 10
    rng = random.Random(7)
    for _ in range(20):
        d1 = [rng.randrange(2) for _ in range(n)]
        d2 = [rng.randrange(2) for _ in range(n)]
        e = sum(a == b for a, b in zip(d1, d2))
        covered = sum(
            all(t[i] in (d1[i], d2[i]) for i in range(n))
            for t in itertools.product((0, 1), repeat=n)
        )
        assert covered == 2 ** (n - e)


def test_average_over_k_signatures() -> None:
    # Over random digests, a random target is covered with chance (1 - 2^-k)^n.
    n, k = 8, 3
    total = 0
    rng = random.Random(8)
    trials = 4000
    for _ in range(trials):
        ds = [[rng.randrange(2) for _ in range(n)] for _ in range(k)]
        t = [rng.randrange(2) for _ in range(n)]
        total += all(any(d[i] == t[i] for d in ds) for i in range(n))
    expect = (1 - 2**-k) ** n
    assert abs(total / trials - expect) < 0.03
