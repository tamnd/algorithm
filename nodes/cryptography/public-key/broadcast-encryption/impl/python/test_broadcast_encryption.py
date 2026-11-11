# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/broadcast-encryption/. The authors are listed in prov/FF58G6.jsonl.
#
# The complete subtree method has no official test vectors (AACS uses the subset difference
# method with its own licensed keys). The tests check the worked example of the page, that the
# cover is exact for every revoked set of an 8-user tree and for random sets of a 64-user tree,
# the bound r log2(n/r) on the header,
# and that the other users decrypt while revoked users, alone or together, do not.

import math
import random
from itertools import combinations

import broadcast_encryption as be

MASTER = b"toy master secret, NOT for real use"


def test_worked_example_n8() -> None:
    assert be.path(8, 3) == [11, 5, 2, 1]
    assert be.cover(8, {2, 5}) == [4, 7, 11, 12]
    assert [list(be.leaves_under(8, v)) for v in (4, 7, 11, 12)] == [[0, 1], [6, 7], [3], [4]]
    assert be.cover(8, set()) == [1]
    assert be.cover(8, set(range(8))) == []


def _check_exact(n, revoked) -> None:
    covered = []
    for v in be.cover(n, revoked):
        covered.extend(be.leaves_under(n, v))
    assert sorted(covered) == [u for u in range(n) if u not in revoked]  # disjoint and exact


def test_cover_is_exact() -> None:
    for mask in range(1 << 8):  # every revoked set of an 8-user tree
        _check_exact(8, {u for u in range(8) if mask >> u & 1})
    rng = random.Random(16)
    for _ in range(300):  # random revoked sets of a 64-user tree
        _check_exact(64, set(rng.sample(range(64), rng.randrange(65))))


def test_header_size_bound() -> None:
    n = 1024
    rng = random.Random(2001)
    for r in (1, 2, 3, 5, 10, 32, 100, 300, 512):
        for _ in range(5):
            revoked = set(rng.sample(range(n), r))
            assert len(be.cover(n, revoked)) <= r * math.log2(n / r)
    assert len(be.cover(n, {0})) == 10  # one revoked user: log2(n) subtrees


def test_broadcast_and_revocation() -> None:
    n = 32
    rng = random.Random(1993)
    revoked = {3, 4, 17, 30}
    message = b"the episode key for tonight"
    ct = be.broadcast(MASTER, n, revoked, message, rng)
    assert len(ct[1]) <= len(revoked) * math.log2(n / len(revoked))
    for u in range(n):
        got = be.receive(be.user_keys(MASTER, n, u), ct)
        assert (got == message) == (u not in revoked)
        if u in revoked:
            assert got is None


def test_revoked_users_cannot_collude() -> None:
    n = 32
    rng = random.Random(7)
    revoked = {0, 9, 10, 31}
    ct = be.broadcast(MASTER, n, revoked, b"secret", rng)
    pooled = {}
    for u in revoked:
        pooled.update(be.user_keys(MASTER, n, u))
    assert be.receive(pooled, ct) is None
    for a, b in combinations(sorted(revoked), 2):
        both = {**be.user_keys(MASTER, n, a), **be.user_keys(MASTER, n, b)}
        assert be.receive(both, ct) is None


def test_no_revocation_and_tampering() -> None:
    n = 8
    rng = random.Random(3)
    ct = be.broadcast(MASTER, n, set(), b"hello all", rng)
    assert [v for v, _ in ct[1]] == [1]
    assert all(be.receive(be.user_keys(MASTER, n, u), ct) == b"hello all" for u in range(n))
    nonce, header, body, tag = ct
    bad = (nonce, header, bytes([body[0] ^ 1]) + body[1:], tag)
    assert be.receive(be.user_keys(MASTER, n, 0), bad) is None
