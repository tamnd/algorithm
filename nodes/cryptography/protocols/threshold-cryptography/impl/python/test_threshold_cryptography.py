# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/threshold-cryptography/. The authors are listed in prov/HRY17J.jsonl.
#
# Threshold ElGamal has no official test vectors (the NIST threshold call,
# NIST IR 8214C, asks submitters for their own). The tests check the
# threshold property on a toy group with n = 5 and t = 3.

import secrets

import pytest

from threshold_cryptography import (
    G,
    P,
    Q,
    Server,
    combine,
    check_partial,
    deal,
    decode,
    dkg,
    encode,
    encrypt,
    lagrange_at_zero,
    poly_eval,
    shamir_combine,
    shamir_split,
    subsets,
    threshold_decrypt,
)

T, N = 3, 5


def is_probable_prime(n: int) -> bool:
    d, s = n - 1, 0
    while d % 2 == 0:
        d, s = d // 2, s + 1
    for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41):
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def test_group():
    assert P == 2 * Q + 1 and P.bit_length() == 128
    assert is_probable_prime(P) and is_probable_prime(Q)
    assert G != 1 and pow(G, Q, P) == 1


def test_encoding():
    for m in (1, 2, 3, 42, Q - 1, Q):
        e = encode(m)
        assert pow(e, Q, P) == 1 and decode(e) == m


def test_shamir_any_t_shares_reconstruct():
    s = secrets.randbelow(Q)
    shares, _ = shamir_split(s, T, N)
    for k in range(T, N + 1):
        for idx in subsets(list(shares), k):
            assert shamir_combine({i: shares[i] for i in idx}) == s
    assert sum(lagrange_at_zero([1, 2, 3], i) for i in (1, 2, 3)) % Q == 1


def test_t_minus_1_shares_fit_every_secret():
    s = secrets.randbelow(Q)
    shares, _ = shamir_split(s, T, N)
    known = {1: shares[1], 4: shares[4]}
    for guess in (0, 1, s, secrets.randbelow(Q)):
        # the unique polynomial of degree 2 through (0, guess) and the two shares
        pts = dict(known)
        pts[0] = guess
        assert all(sum(v * _basis(pts, i, x) for i, v in pts.items()) % Q == pts[x] for x in (0, 1, 4))


def _basis(pts, i, x):
    num, den = 1, 1
    for j in pts:
        if j != i:
            num, den = num * (x - j) % Q, den * (i - j) % Q
    return num * pow(den, -1, Q) % Q


def test_every_t_subset_decrypts():
    pk, servers = deal(T, N)
    m = 123456789
    c = encrypt(pk, m)
    count = 0
    for k in range(T, N + 1):
        for group in subsets(servers, k):
            assert combine(c, {s.index: s.partial(c[0]) for s in group}) == m
            count += 1
    assert count == 10 + 5 + 1


def test_no_t_minus_1_subset_decrypts():
    pk, servers = deal(T, N)
    m = 987654321
    c = encrypt(pk, m)
    for group in subsets(servers, T - 1):
        assert combine(c, {s.index: s.partial(c[0]) for s in group}) != m
    with pytest.raises(ValueError):
        threshold_decrypt(pk, servers[: T - 1], c)


def test_bad_partial_is_detected_and_skipped():
    pk, servers = deal(T, N)
    m = 31337
    c = encrypt(pk, m)
    bad = Server(servers[0].index, (servers[0].share + 1) % Q)  # a server with a wrong share
    assert not check_partial(pk, bad, c[0], bad.partial(c[0]))
    assert all(check_partial(pk, s, c[0], s.partial(c[0])) for s in servers)
    assert threshold_decrypt(pk, [bad] + servers[1:], c) == m
    # Without the check, the wrong partial gives a wrong plaintext.
    assert combine(c, {s.index: s.partial(c[0]) for s in [bad] + servers[1:T]}) != m


def test_dkg_without_a_dealer():
    pk, servers, disq = dkg(T, N)
    assert disq == []
    m = 2024
    c = encrypt(pk, m)
    for group in subsets(servers, T):
        assert combine(c, {s.index: s.partial(c[0]) for s in group}) == m
    for s in servers:
        assert pow(G, s.share, P) == pk.verification[s.index]


def test_dkg_disqualifies_a_cheating_dealer():
    pk, servers, disq = dkg(T, N, cheater=4)
    assert disq == [4]
    c = encrypt(pk, 77)
    assert threshold_decrypt(pk, servers, c) == 77


def test_polynomial_evaluation():
    assert poly_eval([5, 0, 1], 3) == 14
