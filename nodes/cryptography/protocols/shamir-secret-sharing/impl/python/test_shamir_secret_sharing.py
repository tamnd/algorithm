# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shamir-secret-sharing/. The authors are listed in prov/95YWP2.jsonl.
# There are no official test vectors for Shamir's scheme: its shares are
# random. The GF(2^8) arithmetic is checked against the two products given in
# FIPS 197 (AES), Sections 4.2 and 4.2.1. Perfect secrecy is checked exactly
# by enumeration in GF(11) with t = 3 and in GF(256) with t = 2.

import itertools
import random
from collections import Counter

from shamir_secret_sharing import (
    add_shares,
    consistent,
    gf_inv,
    gf_mul,
    gf_reconstruct_byte,
    gf_reconstruct_bytes,
    gf_share_byte,
    gf_share_bytes,
    lagrange_at_zero,
    reconstruct,
    refresh,
    share,
)

P = 2**127 - 1


def seq(values):
    it = iter(values)
    return lambda: next(it)


def test_worked_example():
    # f(X) = 7 + 3X + 5X^2 over GF(11).
    shares = share(7, 3, 5, 11, seq([3, 5]))
    assert shares == [(1, 4), (2, 0), (3, 6), (4, 0), (5, 4)]
    assert lagrange_at_zero([1, 2, 3], 11) == [3, 8, 1]
    assert reconstruct(shares[:3], 11) == 7


def test_every_t_subset_reconstructs():
    rng = random.Random(1)
    for t, n in ((1, 1), (2, 3), (3, 5), (5, 7)):
        s = rng.randrange(P)
        shares = share(s, t, n, P, lambda: rng.randrange(P))
        for subset in itertools.combinations(shares, t):
            assert reconstruct(list(subset), P) == s
        for subset in itertools.combinations(shares, min(t + 1, n)):
            assert reconstruct(list(subset), P) == s        # more shares also work


def test_t_minus_1_shares_fit_every_secret_gf11():
    p, t = 11, 3
    for xs in itertools.combinations(range(1, 6), t - 1):
        dists = []
        for s in range(p):
            c = Counter()
            for a in itertools.product(range(p), repeat=t - 1):
                shares = dict(share(s, t, 5, p, seq(a)))
                c[tuple(shares[x] for x in xs)] += 1
            assert len(c) == p ** (t - 1) and set(c.values()) == {1}   # a bijection
            dists.append(c)
        assert all(d == dists[0] for d in dists)


def test_t_minus_1_shares_fit_every_secret_gf256():
    for x in (1, 2, 200, 255):
        for s in (0, 0x53, 0xFF):
            ys = sorted(gf_share_byte(s, 2, max(x, 2), seq([a]))[x - 1][1] for a in range(256))
            assert ys == list(range(256))


def test_gf256_field():
    assert gf_mul(0x57, 0x83) == 0xC1        # FIPS 197, Section 4.2
    assert gf_mul(0x53, 0xCA) == 0x01        # FIPS 197, Section 4.2.1
    assert gf_inv(0x53) == 0xCA
    for a in range(1, 256):
        assert gf_mul(a, gf_inv(a)) == 1


def test_gf256_bytes():
    secret = b"attack at dawn"
    shares = gf_share_bytes(secret, 3, 6)
    for subset in itertools.combinations(shares, 3):
        assert gf_reconstruct_bytes(list(subset)) == secret
    # Worked example: s = 0x53, f(X) = 0x53 + 0xCA X.
    sh = gf_share_byte(0x53, 2, 3, seq([0xCA]))
    assert sh == [(1, 0x99), (2, 0xDC), (3, 0x16)]
    assert gf_reconstruct_byte(sh[:2]) == 0x53


def test_bad_share_gives_wrong_secret_silently():
    rng = random.Random(2)
    s = rng.randrange(P)
    shares = share(s, 3, 5, P, lambda: rng.randrange(P))
    bad = [shares[0], shares[1], (shares[2][0], (shares[2][1] + 1) % P)]
    out = reconstruct(bad, P)
    assert out != s and 0 <= out < P            # no error, just a wrong value
    # The error is lambda_3 times the change: the result is predictable.
    lam = lagrange_at_zero([1, 2, 3], P)
    assert out == (s + lam[2]) % P


def test_consistency_check_with_t_plus_1_shares():
    rng = random.Random(3)
    shares = share(1234, 3, 5, P, lambda: rng.randrange(P))
    assert consistent(shares, 3, P)
    for k in range(5):
        bad = list(shares)
        bad[k] = (bad[k][0], (bad[k][1] + 1) % P)
        assert not consistent(bad, 3, P)
        assert not consistent(bad[:4] if k < 4 else bad[1:], 3, P)


def test_linearity():
    rng = random.Random(4)
    a = share(100, 3, 5, P, lambda: rng.randrange(P))
    b = share(23, 3, 5, P, lambda: rng.randrange(P))
    assert reconstruct(add_shares(a, b, P)[2:], P) == 123
    scaled = [(x, 3 * y % P) for x, y in a]
    assert reconstruct(scaled[:3], P) == 300


def test_refresh():
    rng = random.Random(5)
    old = share(42, 3, 5, P, lambda: rng.randrange(P))
    new = refresh(old, 3, P, lambda: rng.randrange(P))
    assert all(o != n for o, n in zip(old, new))
    for subset in itertools.combinations(new, 3):
        assert reconstruct(list(subset), P) == 42
    # Old and new shares do not mix: two old and one new give a wrong value.
    assert reconstruct([old[0], old[1], new[2]], P) != 42
