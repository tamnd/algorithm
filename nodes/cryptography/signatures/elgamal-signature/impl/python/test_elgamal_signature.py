# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/elgamal-signature/. The authors are listed in prov/D1G2DP.jsonl.
"""Tests for ElGamal signatures. No standard defines ElGamal signatures, so
there are no official test vectors; the fixed values come from the worked
example of the Handbook of Applied Cryptography, Example 11.65."""

import random

from elgamal_signature import (
    Group, keygen, recover_key_from_reused_k, sign, sign_message, solve_linear_congruence,
    toy_group, verify, verify_message,
)

# HAC Example 11.65: p = 2357, alpha = 2, a = 1751, y = 1185; h(m) = m;
# m = 1463, k = 1529 give r = 1490, k^-1 mod 2356 = 245, s = 1777; v1 = v2 = 1072.
HAC = Group(2357, 2)
HAC_X, HAC_Y = 1751, 1185


def test_hac_example_11_65() -> None:
    assert pow(HAC.g, HAC_X, HAC.p) == HAC_Y
    assert pow(1529, -1, 2356) == 245
    assert sign(HAC, HAC_X, 1463, k=1529) == (1490, 1777)
    assert verify(HAC, HAC_Y, 1463, (1490, 1777))
    assert pow(HAC_Y, 1490, HAC.p) * pow(1490, 1777, HAC.p) % HAC.p == 1072 == pow(2, 1463, HAC.p)


def test_hac_example_rejections() -> None:
    assert not verify(HAC, HAC_Y, 1464, (1490, 1777))
    assert not verify(HAC, HAC_Y, 1463, (1490, 1778))
    assert not verify(HAC, HAC_Y, 1463, (0, 1777))
    assert not verify(HAC, HAC_Y, 1463, (HAC.p, 1777))


def test_round_trips_on_toy_group() -> None:
    rng = random.Random(1)
    group = toy_group(128, seed=3)
    q = (group.p - 1) // 2
    assert pow(group.g, q, group.p) != 1 and pow(group.g, 2, group.p) != 1
    x, y = keygen(group, rng)
    for i in range(20):
        msg = b"message %d" % i
        sig = sign_message(group, x, msg, rng)
        assert verify_message(group, y, msg, sig)
        assert not verify_message(group, y, msg + b"!", sig)
        r, s = sig
        other_s = s + 1 if s < group.p - 2 else 1
        assert not verify_message(group, y, msg, (r, other_s))


def test_randomized() -> None:
    rng = random.Random(2)
    group = toy_group(128, seed=3)
    x, y = keygen(group, rng)
    a, b = sign_message(group, x, b"m", rng), sign_message(group, x, b"m", rng)
    assert a != b and verify_message(group, y, b"m", a) and verify_message(group, y, b"m", b)


def test_linear_congruence() -> None:
    assert solve_linear_congruence(4, 6, 10) == [4, 9]
    assert solve_linear_congruence(4, 5, 10) == []
    assert solve_linear_congruence(3, 1, 7) == [5]


def test_reused_k_reveals_key_toy_group() -> None:
    rng = random.Random(4)
    group = toy_group(128, seed=3)
    x, y = keygen(group, rng)
    found = 0
    for trial in range(10):
        k = rng.randrange(1, group.p - 1)
        if k % 2 == 0:
            k += 1
        h1, h2 = rng.randrange(group.p - 1), rng.randrange(group.p - 1)
        try:
            sig1, sig2 = sign(group, x, h1, k=k), sign(group, x, h2, k=k)
        except ValueError:
            continue
        assert sig1[0] == sig2[0]
        if recover_key_from_reused_k(group, y, h1, sig1, h2, sig2) == x:
            found += 1
    assert found >= 8


def test_reused_k_reveals_key_hac_group() -> None:
    sig1 = sign(HAC, HAC_X, 1463, k=1529)
    sig2 = sign(HAC, HAC_X, 1000, k=1529)
    assert recover_key_from_reused_k(HAC, HAC_Y, 1463, sig1, 1000, sig2) == HAC_X


def test_distinct_k_gives_no_shared_r() -> None:
    rng = random.Random(5)
    group = toy_group(128, seed=3)
    x, y = keygen(group, rng)
    s1, s2 = sign(group, x, 11, rng=rng), sign(group, x, 12, rng=rng)
    assert recover_key_from_reused_k(group, y, 11, s1, 12, s2) is None
