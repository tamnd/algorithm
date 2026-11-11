# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/non-malleability/. The authors are listed in prov/TMD2FZ.jsonl.
"""Tests for the NM-CPA experiment against ElGamal. Non-malleability is a
definition, so there are no official test vectors; the tests use fixed seeds.
"""

import random

from non_malleability import G, P, Q, decrypt, encrypt, keygen, mauling_adversary, nm_cpa_experiment, nm_from_ind


def test_group() -> None:
    assert P == 2 * Q + 1 and pow(G, Q, P) == 1 and G != 1


def test_mauled_ciphertext_decrypts_to_related_message() -> None:
    rng = random.Random(1991)
    h, x = keygen(rng)
    for _ in range(50):
        m = pow(G, rng.randrange(Q), P)
        c = encrypt(h, m, rng)
        relation, ys = mauling_adversary(c)
        assert ys[0] != c
        assert relation(m, decrypt(x, ys[0]))


def test_elgamal_is_not_nm_cpa() -> None:
    rng = random.Random(1998)
    trials = 300
    real = sum(nm_cpa_experiment(rng, real=True) for _ in range(trials))
    rand = sum(nm_cpa_experiment(rng, real=False) for _ in range(trials))
    # Real: the relation always holds. Random: it holds with probability 1/Q.
    assert real == trials
    assert rand == 0


def test_nm_adversary_from_ind_adversary() -> None:
    # A perfect IND-CPA guesser (it cheats with the key, to stand in for any
    # guesser) gives an NM-CPA adversary with advantage 1/2: the relation
    # 'equal' holds always in the real run and half the time in the random run.
    rng = random.Random(2006)
    m0, m1 = pow(G, 5, P), pow(G, 7, P)
    real = rand = 0
    trials = 2000
    for _ in range(trials):
        h, sk = keygen(rng)
        x, x_tilde = (m0, m1)[rng.randrange(2)], (m0, m1)[rng.randrange(2)]
        y = encrypt(h, x, rng)
        relation, ys = nm_from_ind(lambda c: 0 if decrypt(sk, c) == m0 else 1, m0, m1, h, y, rng)
        assert y not in ys
        xp = decrypt(sk, ys[0])
        real += relation(x, xp)
        rand += relation(x_tilde, xp)
    assert real == trials
    assert abs(rand / trials - 0.5) < 0.04
