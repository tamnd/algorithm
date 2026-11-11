# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sigma-protocol/. The authors are listed in prov/T1TB5Q.jsonl.
# There are no official test vectors for sigma protocols. The tests check the
# three properties on toy groups: completeness, special soundness (extraction
# from two transcripts) and special honest-verifier zero knowledge (the real
# and simulated transcripts are equal as distributions, by enumeration in the
# group of order 11).

import random
from collections import Counter
from itertools import product

from sigma_protocol import TINY, TOY, And, ChaumPedersen, Or, Schnorr, random_coins, run


def all_coins(n, q):
    return product(range(q), repeat=n)


def instances(G):
    """(protocol, statement, witness) for each instance in group G."""
    q = G.q
    x1, x2 = 7 % q, 3 % q
    y1, y2 = G.exp(G.g, x1), G.exp(G.g, x2)
    s, cp = Schnorr(G), ChaumPedersen(G)
    dh = (G.exp(G.g, x1), G.exp(G.h, x1))
    junk = G.exp(G.g, 5)                       # a key whose log we "forget"
    return [
        ("schnorr", s, y1, x1),
        ("chaum-pedersen", cp, dh, x1),
        ("and", And(s, cp), (y2, dh), (x2, x1)),
        ("or, branch 0", Or(s, s, q), (y1, junk), (0, x1)),
        ("or, branch 1", Or(s, s, q), (junk, y2), (1, x2)),
        ("or, mixed", Or(s, cp, q), (junk, dh), (1, x1)),
    ]


def test_completeness():
    rng = random.Random(1)
    for G in (TINY, TOY):
        for name, proto, stmt, w in instances(G):
            for _ in range(30):
                a, c, z = run(proto, stmt, w, G.q, rng)
                assert proto.verify(stmt, a, c, z), name


def test_special_soundness_extracts_the_witness():
    rng = random.Random(2)
    G = TOY
    for name, proto, stmt, w in instances(G):
        coins = random_coins(proto.ncoins, G.q, rng)
        a = proto.commit(stmt, w, coins)
        c1, c2 = 100, 917
        z1 = proto.respond(stmt, w, coins, c1)
        z2 = proto.respond(stmt, w, coins, c2)
        assert proto.verify(stmt, a, c1, z1) and proto.verify(stmt, a, c2, z2)
        # For the OR proofs the extractor finds the branch the prover really
        # knows: the simulated branch keeps its sub-challenge fixed, so only
        # the real branch has two different ones.
        assert proto.extract(stmt, a, c1, z1, c2, z2) == w, name


def test_or_extraction_finds_the_known_branch():
    # The prover fixes the sub-challenge of the simulated branch in its
    # coins, so two answers to different challenges differ on its own branch.
    G = TOY
    s = Schnorr(G)
    x0, x1 = 11, 22
    stmt = (G.exp(G.g, x0), G.exp(G.g, x1))
    proto = Or(s, s, G.q)
    for i, wi in ((0, x0), (1, x1)):
        coins = (5, 40, 77)
        a = proto.commit(stmt, (i, wi), coins)
        z1 = proto.respond(stmt, (i, wi), coins, 3)
        z2 = proto.respond(stmt, (i, wi), coins, 8)
        assert proto.extract(stmt, a, 3, z1, 8, z2) == (i, wi)


def test_simulator_outputs_verify():
    rng = random.Random(3)
    G = TOY
    for name, proto, stmt, w in instances(G):
        for _ in range(20):
            c = rng.randrange(G.q)
            a, z = proto.simulate(stmt, c, random_coins(proto.nsim, G.q, rng))
            assert proto.verify(stmt, a, c, z), name


def test_shvzk_exact_distribution():
    # For each challenge c, the real transcripts over all prover coins and
    # the simulated transcripts over all simulator coins are the same multiset.
    G = TINY
    for name, proto, stmt, w in instances(G):
        assert proto.ncoins == proto.nsim or name.startswith("or")
        for c in (0, 1, 6, 10):
            real = Counter()
            for coins in all_coins(proto.ncoins, G.q):
                a = proto.commit(stmt, w, coins)
                real[(a, proto.respond(stmt, w, coins, c))] += 1
            sim = Counter()
            for coins in all_coins(proto.nsim, G.q):
                sim[proto.simulate(stmt, c, coins)] += 1
            assert real == sim, (name, c)


def test_or_proof_is_witness_indistinguishable():
    # The transcripts made with the witness for branch 0 and with the witness
    # for branch 1 have the same distribution.
    G = TINY
    s = Schnorr(G)
    x0, x1 = 2, 9
    stmt = (G.exp(G.g, x0), G.exp(G.g, x1))
    proto = Or(s, s, G.q)
    for c in (0, 4):
        dists = []
        for w in ((0, x0), (1, x1)):
            d = Counter()
            for coins in all_coins(proto.ncoins, G.q):
                d[(proto.commit(stmt, w, coins), proto.respond(stmt, w, coins, c))] += 1
            dists.append(d)
        assert dists[0] == dists[1]


def test_chaum_pedersen_rejects_a_non_dh_tuple():
    # If v != h^x, then for each first message at most one challenge can be
    # answered: exhaustive over all a and all z in the group of order 11.
    G = TINY
    cp = ChaumPedersen(G)
    u, v = G.exp(G.g, 3), G.exp(G.h, 4)       # different logs
    elems = [G.exp(G.g, e) for e in range(G.q)]
    for a in product(elems, elems):
        good = {c for c in range(G.q) for z in range(G.q) if cp.verify((u, v), a, c, z)}
        assert len(good) <= 1


def test_schnorr_challenge_is_needed():
    # With the challenge known in advance, the simulator is a cheating prover:
    # this is why the verifier must pick c after it sees a.
    G = TOY
    s = Schnorr(G)
    y = G.exp(G.g, 999)
    a, z = s.simulate(y, 42, (123,))
    assert s.verify(y, a, 42, z)
    assert not s.verify(y, a, 43, z)
