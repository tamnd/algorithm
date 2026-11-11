# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ntru-prime/. The authors are listed in prov/ECE9S6.jsonl.
# No official vector is used: the known answer tests of sntrup761 cover the
# full KEM with its encodings and hashes, which this core does not implement.

import random

from ntru_prime import P, Q, W, center, decrypt, encrypt, keygen, ring_mul, short


def test_parameters_meet_the_no_failure_bound():
    # Decryption never fails when q >= 16 w + 1 (the coefficients of 3 f c stay below q / 2).
    assert Q >= 16 * W + 1 and (P, Q, W) == (761, 4591, 286)


def test_reduction_rule():
    a = [0] * P
    a[P - 1] = 1
    b = [0] * P
    b[1] = 1
    xp = ring_mul(a, b, Q)  # x^(p-1) * x = x^p = x + 1
    assert xp[:2] == [1, 1] and not any(xp[2:])


def test_keygen_round_trips_bound_and_wrong_key():
    rng = random.Random(761)
    h, sk = keygen(rng)
    f, v = sk
    g = [center(x, Q) for x in ring_mul(h, [3 * x for x in f], Q)]  # h * 3f = g
    assert all(x in (-1, 0, 1) for x in g)
    assert ring_mul([x % 3 for x in g], v, 3) == [1] + [0] * (P - 1)
    for _ in range(3):
        r = short(rng)
        c = encrypt(h, r)
        assert all(x % 3 == 0 and abs(x) <= (Q + 1) // 2 for x in c)
        e = [center(x, Q) for x in ring_mul([3 * x for x in f], c, Q)]
        assert max(abs(x) for x in e) < Q // 2
        assert decrypt(sk, c) == r
    other = (f[1:] + f[:1], v)  # a different short f with the same weight
    assert decrypt(other, encrypt(h, r)) != r
