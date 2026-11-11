# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/schnorr-identification-protocol/. The authors are listed in prov/99NZYX.jsonl.
# There are no official test vectors for the Schnorr identification protocol.
# The group 14 prime is checked against the hexadecimal text of RFC 3526,
# Section 3, copied by hand. The protocol tests run local simulated parties.

import random
from fractions import Fraction

from schnorr_identification_protocol import (
    GROUP14,
    TOY,
    GuessingImpersonator,
    Prover,
    identify,
    is_probable_prime,
    key_from_nonce_reuse,
    keygen,
    rfc3526_group14_prime,
    simulate,
    verify,
)

RFC3526_GROUP14_HEX = """
FFFFFFFF FFFFFFFF C90FDAA2 2168C234 C4C6628B 80DC1CD1
29024E08 8A67CC74 020BBEA6 3B139B22 514A0879 8E3404DD
EF9519B3 CD3A431B 302B0A6D F25F1437 4FE1356D 6D51C245
E485B576 625E7EC6 F44C42E9 A637ED6B 0BFF5CB6 F406B7ED
EE386BFB 5A899FA5 AE9F2411 7C4B1FE6 49286651 ECE45B3D
C2007CB8 A163BF05 98DA4836 1C55D39A 69163FA8 FD24CF5F
83655D23 DCA3AD96 1C62F356 208552BB 9ED52907 7096966D
670C354E 4ABC9804 F1746C08 CA18217C 32905E46 2E36CE3B
E39E772C 180E8603 9B2783A2 EC07A28F B5C55DF0 6F4C52C9
DE2BCBF6 95581718 3995497C EA956AE5 15D22618 98FA0510
15728E5A 8AACAA68 FFFFFFFF FFFFFFFF
"""


def test_group14_prime_matches_rfc3526():
    p = int("".join(RFC3526_GROUP14_HEX.split()), 16)
    assert p.bit_length() == 2048
    assert rfc3526_group14_prime() == p
    assert GROUP14.p == p and GROUP14.g == 2


def test_group14_is_a_safe_prime_group():
    p, q = GROUP14.p, GROUP14.q
    assert is_probable_prime(p, bases=(2, 3, 5, 7))
    assert is_probable_prime(q, bases=(2, 3, 5, 7))
    assert p % 8 == 7                  # so 2 is a square and has order q
    assert pow(2, q, p) == 1


def test_toy_example_from_the_page():
    x, k = 123, 456
    y = pow(TOY.g, x, TOY.p)
    prover = Prover(TOY, x)
    a = prover.commit(k)
    assert (y, a) == (572, 1777)
    z = prover.respond(5)
    assert z == 52
    assert verify(TOY, y, a, 5, z, t=3)


def test_completeness_toy_and_group14():
    rng = random.Random(1)
    rand = rng.randrange
    for G, t, runs in ((TOY, 3, 200), (TOY, 10, 200), (GROUP14, 128, 5)):
        x, y = keygen(G, rand)
        prover = Prover(G, x, rand)
        for _ in range(runs):
            assert identify(G, prover, y, t, rand)


def test_guessing_impersonator_succeeds_with_probability_one_over_2_pow_t():
    # Exhaustive over the guess and the challenge for t = 3: success is
    # exactly 1/8, the knowledge error of the protocol.
    t = 3
    y = pow(TOY.g, 777, TOY.p)
    wins = total = 0
    for guess in range(2**t):
        imp = GuessingImpersonator(TOY, y, guess, z=314)
        a = imp.commit()
        for c in range(2**t):
            total += 1
            wins += verify(TOY, y, a, c, imp.respond(c), t)
    assert Fraction(wins, total) == Fraction(1, 2**t)


def test_any_first_message_answers_at_most_one_challenge_without_the_key():
    # If two challenges could be answered for one a, the key would follow:
    # for each a in the toy group, and each c, the accepting z is unique, and
    # answering two c needs z values that reveal x. We check uniqueness of z.
    t = 3
    y = pow(TOY.g, 777, TOY.p)
    a = pow(TOY.g, 5, TOY.p)
    for c in range(2**t):
        good = [z for z in range(TOY.q) if verify(TOY, y, a, c, z, t)]
        assert len(good) == 1


def test_nonce_reuse_reveals_the_key():
    x = 123
    prover = Prover(TOY, x)
    prover.commit(456)
    z1 = prover.respond(5)
    prover.commit(456)                  # the same k in a second session
    z2 = prover.respond(2)
    assert (z1, z2) == (52, 702)
    assert key_from_nonce_reuse(TOY, 5, z1, 2, z2) == x


def test_nonce_reuse_in_group14():
    rng = random.Random(2)
    x, y = keygen(GROUP14, rng.randrange)
    prover = Prover(GROUP14, x)
    k = rng.randrange(GROUP14.q)
    prover.commit(k)
    z1 = prover.respond(11)
    prover.commit(k)
    z2 = prover.respond(99)
    assert key_from_nonce_reuse(GROUP14, 11, z1, 99, z2) == x


def test_simulated_transcripts_verify_and_match_real_ones():
    # For a fixed challenge, real z = k + c x is uniform as k is, and the
    # simulator picks z uniform; a is then fixed by the check. Exhaustive in
    # the toy group for one challenge.
    x, c, t = 123, 6, 3
    y = pow(TOY.g, x, TOY.p)
    prover = Prover(TOY, x)
    real = set()
    for k in range(TOY.q):
        a = prover.commit(k)
        real.add((a, c, prover.respond(c)))
    sim = {simulate(TOY, y, c, z) for z in range(TOY.q)}
    assert real == sim and len(real) == TOY.q
    assert all(verify(TOY, y, *tr, t) for tr in list(sim)[:50])


def test_verifier_rejects_bad_inputs():
    x = 123
    y = pow(TOY.g, x, TOY.p)
    prover = Prover(TOY, x)
    a = prover.commit(456)
    z = prover.respond(5)
    assert not verify(TOY, y, TOY.p - 1, 5, z, 3)       # -1 is not in the subgroup
    assert not verify(TOY, y, a, 5, z + TOY.q, 3)       # z out of range
    assert not verify(TOY, y, a, 9, z, 3)               # c out of range
    assert not verify(TOY, TOY.p - 1, a, 5, z, 3)       # bad public key
