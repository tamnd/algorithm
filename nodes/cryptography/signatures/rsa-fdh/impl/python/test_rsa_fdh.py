# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rsa-fdh/. The authors are listed in prov/0866Z3.jsonl.
"""Tests for RSA-FDH. No standard fixes a full-domain hash, so there are no
official vectors: the tests check round trips, rejections, the MGF1 layer
against its definition, and Coron's reduction on a toy forger. The MGF1 code
is the same as on the RSA-PSS page, where an official PSS vector checks it."""

import hashlib
import math
import random

from rsa_fdh import (
    Abort,
    CoronReduction,
    coron_optimal_p,
    fdh_hash,
    generate_key,
    mgf1,
    sign,
    verify,
)


def test_mgf1_definition() -> None:
    # RFC 8017 Appendix B.2.1: T = Hash(seed || C(0)) || Hash(seed || C(1)) || ...
    seed = b"seed"
    out = mgf1(seed, 70)
    assert out[:32] == hashlib.sha256(seed + b"\x00\x00\x00\x00").digest()
    assert out[32:64] == hashlib.sha256(seed + b"\x00\x00\x00\x01").digest()
    assert out[64:] == hashlib.sha256(seed + b"\x00\x00\x00\x02").digest()[:6]


def test_round_trip_and_rejection() -> None:
    key = generate_key(1024, seed=1)
    for msg in (b"", b"a", b"hello world", bytes(300)):
        s = sign(key, msg)
        assert verify(key.n, key.e, msg, s)
        assert pow(int.from_bytes(s, "big"), key.e, key.n) == fdh_hash(key.n, msg)
    s = sign(key, b"x")
    assert not verify(key.n, key.e, b"y", s)
    bad = bytearray(s)
    bad[-1] ^= 1
    assert not verify(key.n, key.e, b"x", bytes(bad))
    assert not verify(key.n, key.e, b"x", key.n.to_bytes(128, "big"))


def test_full_domain_hash_spreads_over_zn() -> None:
    key = generate_key(512, seed=2)
    vals = [fdh_hash(key.n, i.to_bytes(4, "big")) for i in range(4000)]
    # About half of the values are below N/2, and the top quarter is used.
    below = sum(v < key.n // 2 for v in vals)
    assert 1800 < below < 2200
    assert sum(v > 3 * key.n // 4 for v in vals) > 800


def test_multiplicative_forgery_fails() -> None:
    key = generate_key(1024, seed=3)
    a, b = sign(key, b"m1"), sign(key, b"m2")
    prod = int.from_bytes(a, "big") * int.from_bytes(b, "big") % key.n
    assert not any(verify(key.n, key.e, m, prod.to_bytes(128, "big")) for m in (b"m1", b"m2", b"m1m2"))


def _cheating_forger(key, q_s: int, rng: random.Random):
    """A forger that holds d (a stand-in for a real forger): it asks q_s
    signing queries and then outputs a valid signature on a fresh message."""

    def run(hash_oracle, sign_oracle):
        for i in range(q_s):
            m = b"query %d %d" % (i, rng.randrange(10**9))
            hash_oracle(m)
            s = sign_oracle(m)
            assert pow(s, key.e, key.n) == hash_oracle(m)
        m_star = b"forgery %d" % rng.randrange(10**9)
        return m_star, pow(hash_oracle(m_star), key.d, key.n)

    return run


def test_coron_reduction_inverts_rsa() -> None:
    key = generate_key(512, seed=4)
    rng = random.Random(5)
    q_s = 3
    p = coron_optimal_p(q_s)
    expected = p**q_s * (1 - p)  # 27/256
    assert math.isclose(expected, 1 / (q_s * (1 + 1 / q_s) ** (q_s + 1)))
    trials, wins = 400, 0
    for _ in range(trials):
        y = rng.randrange(2, key.n)
        red = CoronReduction(key.n, key.e, y, p, rng)
        forger = _cheating_forger(key, q_s, rng)
        try:
            m_star, sigma = forger(red.hash, red.sign)
            x = red.extract(m_star, sigma)
        except Abort:
            continue
        assert pow(x, key.e, key.n) == y
        wins += 1
    assert abs(wins / trials - expected) < 0.05
