# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/nonce-reuse-attack/. The authors are listed in prov/A3D86P.jsonl.

import random

from nonce_reuse_attack import (
    G,
    N,
    ecdsa_sign,
    ecdsa_verify,
    hnp_attack,
    leaky_signatures,
    lll,
    point_mul,
    recover_from_reuse,
    toy_dsa_group,
)


def test_reused_nonce_gives_the_key() -> None:
    rng = random.Random(2010)
    d = rng.randrange(1, N)
    q_pt = point_mul(G, d)
    k = rng.randrange(1, N)  # the same k for two messages: the mistake
    m1, m2 = b"game update 1", b"game update 2"
    sig1, sig2 = ecdsa_sign(d, m1, k), ecdsa_sign(d, m2, k)
    assert ecdsa_verify(q_pt, m1, *sig1) and ecdsa_verify(q_pt, m2, *sig2)
    assert sig1[0] == sig2[0]  # the repeated r shows the reuse
    k2, d2 = recover_from_reuse(m1, sig1, m2, sig2)
    assert (k2, d2) == (k, d)
    # With the key, the attacker signs a message of its choice.
    forged = ecdsa_sign(d2, b"attacker's program", 12345)
    assert ecdsa_verify(q_pt, b"attacker's program", *forged)


def test_toy_dsa_group() -> None:
    p, q, g = toy_dsa_group()
    assert q.bit_length() == 40 and (p - 1) % q == 0
    assert g != 1 and pow(g, q, p) == 1


def test_lll_on_a_small_basis() -> None:
    reduced = lll([[1, 0, 0, 1345], [0, 1, 0, 35], [0, 0, 1, 154]])
    shortest = min(sum(x * x for x in row) for row in reduced)
    assert shortest <= 1 + 1 + 1 + 1345  # far shorter than the first input row


def test_lattice_attack_with_ten_known_top_digits() -> None:
    for seed in (1996, 2001, 2002):
        (p, q, g, y), x, sigs = leaky_signatures(seed, count=12, unknown_bits=30)
        cands = hnp_attack(q, sigs, unknown_bits=30)
        assert any(pow(g, c, p) == y for c in cands)
        assert x in cands


def test_lattice_attack_fails_with_too_little_leak() -> None:
    # With only 2 known digits of 40 per nonce and 12 signatures, the hidden
    # vector is not short enough, and the reduction does not reveal x.
    (p, q, g, y), x, sigs = leaky_signatures(2020, count=12, unknown_bits=38)
    assert x not in hnp_attack(q, sigs, unknown_bits=38)
