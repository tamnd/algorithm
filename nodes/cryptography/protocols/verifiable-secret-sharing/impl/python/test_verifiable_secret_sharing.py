# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/verifiable-secret-sharing/. The authors are listed in prov/T3AHK6.jsonl.
# There are no official test vectors for Feldman or Pedersen VSS: dealings are
# random. The tests check the worked example in the group of order 11, that
# honest shares verify and every wrong share fails, that Feldman's C_0 = g^s
# gives the secret away in a toy group, that Pedersen's commitments and t - 1
# shares are independent of the secret (by enumeration), and the bias attack
# on the joint-Feldman DKG against local simulated parties.

import itertools
import random
from collections import Counter

from verifiable_secret_sharing import (
    TINY,
    TOY,
    Verifier,
    bias_attack,
    brute_force_secret,
    complaints,
    feldman_deal,
    feldman_verify,
    joint_feldman,
    pedersen_deal,
    pedersen_verify,
    reconstruct,
)


def seq(values):
    it = iter(values)
    return lambda: next(it)


def test_groups():
    for G in (TINY, TOY):
        assert pow(G.g, G.q, G.p) == 1 and G.g != 1
        assert pow(G.h, G.q, G.p) == 1 and G.h != 1


def test_worked_example():
    # f(X) = 7 + 3X over Z_11, g = 4 in Z_23^*.
    C, shares = feldman_deal(7, 2, 3, TINY, seq([3]))
    assert C == [8, 18]
    assert shares == {1: 10, 2: 2, 3: 5}
    assert all(feldman_verify(i, s, C, TINY) for i, s in shares.items())
    assert pow(4, 2, 23) == 16 == 8 * 18**2 % 23
    assert not feldman_verify(2, 3, C, TINY)
    assert brute_force_secret(8, TINY) == 7
    # Pedersen with b(X) = 5 + 2X and h = 9.
    C, shares = pedersen_deal(7, 2, 3, TINY, seq([3, 5, 2]))
    assert C == [4**7 * 9**5 % 23, 4**3 * 9**2 % 23] == [18, 9]
    assert shares[2] == (2, 9)
    assert pedersen_verify(2, (2, 9), C, TINY)
    assert 4**2 * 9**9 % 23 == 18 * 9**2 % 23 == 9


def test_honest_shares_verify_and_reconstruct():
    rng = random.Random(1)
    rand = lambda: rng.randrange(TOY.q)
    for t, n in ((1, 1), (2, 3), (3, 5), (4, 7)):
        s = rng.randrange(TOY.q)
        C, shares = feldman_deal(s, t, n, TOY, rand)
        assert complaints(C, shares, TOY) == []
        assert reconstruct(shares, t, Verifier(C, TOY)) == s
        C, shares = pedersen_deal(s, t, n, TOY, rand)
        assert complaints(C, shares, TOY, pedersen=True) == []
        assert reconstruct(shares, t, Verifier(C, TOY, pedersen=True)) == s


def test_every_wrong_share_fails():
    rng = random.Random(2)
    rand = lambda: rng.randrange(TOY.q)
    C, shares = feldman_deal(500, 3, 5, TOY, rand)
    for i, s in shares.items():
        bad = [v for v in range(TOY.q) if v != s and feldman_verify(i, v, C, TOY)]
        assert bad == []          # g has order q, so g^v = g^s only for v = s
    C, shares = pedersen_deal(500, 3, 5, TOY, rand)
    for i, (s, r) in shares.items():
        assert not pedersen_verify(i, ((s + 1) % TOY.q, r), C, TOY)
        assert not pedersen_verify(i, (s, (r + 1) % TOY.q), C, TOY)


def test_bad_share_is_filtered_at_reconstruction():
    rng = random.Random(3)
    rand = lambda: rng.randrange(TOY.q)
    C, shares = feldman_deal(321, 3, 5, TOY, rand)
    shares[1] = (shares[1] + 1) % TOY.q
    assert complaints(C, shares, TOY) == [1]
    assert reconstruct(shares, 3, Verifier(C, TOY)) == 321
    # Plain Shamir with the same bad share gives a wrong secret.
    assert reconstruct(shares, 3, _AcceptAll(C, TOY)) != 321


class _AcceptAll(Verifier):
    """No check at all, as in plain Shamir sharing."""

    def __call__(self, i, share):
        return True


def test_pedersen_with_trapdoor_opens_two_ways():
    # Binding rests on log_g h. In TINY, h = 9 = 4^8, so a dealer who knows
    # 8 can change (s, r) to (s + 8d, r - d) without changing g^s h^r.
    G, w = TINY, 8
    assert pow(G.g, w, G.p) == G.h
    s, r, d = 2, 9, 1
    s2, r2 = (s + w * d) % G.q, (r - d) % G.q
    assert pow(G.g, s, G.p) * pow(G.h, r, G.p) % G.p == pow(G.g, s2, G.p) * pow(G.h, r2, G.p) % G.p


def _view(deal, s, rand, parties):
    C, shares = deal(s, 2, 3, TINY, rand)
    return (tuple(C), tuple(shares[i] for i in parties))


def test_pedersen_view_is_independent_of_secret():
    # t = 2: one party plus all commitments. Randomness (a_1, b_0, b_1) in Z_11^3.
    for party in (1, 2, 3):
        dists = []
        for s in range(TINY.q):
            c = Counter(_view(pedersen_deal, s, seq(r), [party])
                        for r in itertools.product(range(TINY.q), repeat=3))
            dists.append(c)
        assert all(d == dists[0] for d in dists)
    # C_0 = g^s h^{b_0} alone is uniform over the subgroup for every s.
    subgroup = {pow(TINY.g, k, TINY.p) for k in range(TINY.q)}
    for s in range(TINY.q):
        assert {pow(TINY.g, s, TINY.p) * pow(TINY.h, b, TINY.p) % TINY.p
                for b in range(TINY.q)} == subgroup


def test_feldman_view_depends_on_secret():
    views = set()
    for s in range(TINY.q):
        C, _ = feldman_deal(s, 2, 3, TINY, seq([0]))
        views.add(C[0])
    assert len(views) == TINY.q          # C_0 = g^s differs for every secret
    for s in (0, 5, 1018):
        C, _ = feldman_deal(s, 3, 5, TOY)
        assert brute_force_secret(C[0], TOY) == s


def test_dkg_and_bias_attack():
    G, n, t = TOY, 4, 2
    rng = random.Random(4)
    rand = lambda: rng.randrange(G.q)
    qual, y, x = joint_feldman(n, t, G, rand)
    assert qual == [1, 2, 3, 4]
    lams = {1: 2, 2: G.q - 1}           # lambda at 0 for the points 1 and 2
    secret = (lams[1] * x[1] + lams[2] * x[2]) % G.q
    assert pow(G.g, secret, G.p) == y
    # Honest runs: y is even about half the time. With one corrupt dealer
    # that drops out when that helps, about 3/4 of the time.
    even = lambda v: v % 2 == 0
    trials = 300
    honest = sum(even(joint_feldman(n, t, G, rand)[1]) for _ in range(trials))
    attacked, dropped = 0, 0
    for _ in range(trials):
        qual, y, x = joint_feldman(n, t, G, rand, cheat=bias_attack(4, even, G))
        attacked += even(y)
        dropped += 4 not in qual
        secret = (lams[1] * x[1] + lams[2] * x[2]) % G.q
        assert pow(G.g, secret, G.p) == y          # still a valid key, just biased
    assert 0.38 < honest / trials < 0.62
    assert 0.65 < attacked / trials < 0.85
    assert dropped > 0
