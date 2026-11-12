# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/latent-dirichlet-allocation/. The authors are listed in prov/JHNS1Q.jsonl.

import itertools
import random
from fractions import Fraction

from latent_dirichlet_allocation import (Counts, collapsed_gibbs, collapsed_joint, conditional,
                                         estimates, generate, gibbs_sweep)

# The corpus of the page: 0 ball, 1 game, 2 goal, 3 vote, 4 law, 5 party
PAGE_DOCS = [[0, 1, 2, 0], [3, 4, 5, 3], [1, 2, 0, 2], [4, 5, 3, 4], [0, 3, 1, 4]]


def test_conditional_matches_ratios_of_the_collapsed_joint():
    rng = random.Random(1)
    alpha, beta = Fraction(1, 2), Fraction(1, 3)
    for _ in range(30):
        k, v = rng.randint(2, 3), rng.randint(2, 4)
        docs = [[rng.randrange(v) for _ in range(rng.randint(1, 4))] for _ in range(rng.randint(1, 3))]
        z = [[rng.randrange(k) for _ in doc] for doc in docs]
        d = rng.randrange(len(docs))
        i = rng.randrange(len(docs[d]))
        joints = []
        for t in range(k):
            z[d][i] = t
            joints.append(collapsed_joint(docs, z, k, v, alpha, beta))
        cnt = Counts(docs, z, k, v)
        cnt.add(d, docs[d][i], z[d][i], -1)
        p = conditional(cnt, d, docs[d][i], alpha, beta, v)
        for t in range(k):
            assert p[t] / sum(p) == joints[t] / sum(joints)


def test_count_tables_stay_consistent():
    rng = random.Random(2)
    docs = [[rng.randrange(7) for _ in range(rng.randint(1, 12))] for _ in range(10)]
    z, cnt = collapsed_gibbs(docs, 3, 7, 0.5, 0.1, 5, rng)
    for _ in range(5):
        gibbs_sweep(docs, z, cnt, 0.5, 0.1, 7, rng)
        fresh = Counts(docs, z, 3, 7)
        assert cnt.ndk == fresh.ndk and cnt.nkw == fresh.nkw and cnt.nk == fresh.nk
        assert sum(cnt.nk) == sum(len(doc) for doc in docs)
        assert all(sum(row) == len(doc) for row, doc in zip(cnt.ndk, docs))


def test_chain_has_the_exact_posterior_as_stationary_distribution():
    docs, k, v = [[0, 1], [1, 2]], 2, 3
    a, b = Fraction(1, 2), Fraction(1, 2)
    states = list(itertools.product(range(k), repeat=4))
    w = {s: collapsed_joint(docs, [list(s[:2]), list(s[2:])], k, v, a, b) for s in states}
    total = sum(w.values())
    rng = random.Random(3)
    z = [[0, 0], [0, 0]]
    cnt = Counts(docs, z, k, v)
    freq = dict.fromkeys(states, 0)
    sweeps = 40000
    for _ in range(sweeps):
        gibbs_sweep(docs, z, cnt, 0.5, 0.5, v, rng)
        freq[tuple(z[0] + z[1])] += 1
    tv = sum(abs(freq[s] / sweeps - float(w[s] / total)) for s in states) / 2
    assert tv < 0.02


def test_recovers_separated_topics_up_to_permutation():
    rng = random.Random(4)
    k, v = 3, 9
    topics = [[1 / 3 if w // 3 == t else 0.0 for w in range(v)] for t in range(k)]
    docs, _ = generate(rng, topics, 0.3, 60, 30)
    _, cnt = collapsed_gibbs(docs, k, v, 0.1, 0.01, 100, rng)
    phi, theta = estimates(cnt, 0.1, 0.01)
    best = min(max(sum(abs(p - q) for p, q in zip(phi[perm[t]], topics[t])) / 2 for t in range(k))
               for perm in itertools.permutations(range(k)))
    assert best < 0.05
    for row in phi + theta:
        assert abs(sum(row) - 1) < 1e-12


def test_example_of_the_page():
    rng = random.Random(2)
    z, cnt = collapsed_gibbs(PAGE_DOCS, 2, 6, 0.5, 0.1, 200, rng)
    assert z == [[0, 0, 0, 0], [1, 1, 1, 1], [0, 0, 0, 0], [1, 1, 1, 1], [0, 1, 0, 1]]
    phi, theta = estimates(cnt, 0.5, 0.1)
    assert [round(p, 3) for p in phi[0]] == [0.387, 0.292, 0.292, 0.009, 0.009, 0.009]
    assert [round(p, 3) for p in phi[1]] == [0.009, 0.009, 0.009, 0.387, 0.387, 0.198]
    assert [round(p, 3) for p in theta[0]] == [0.9, 0.1] and theta[4] == [0.5, 0.5]
    # one update by hand: remove the token "ball" of document 5 and resample it
    cnt.add(4, 0, 0, -1)
    p = conditional(cnt, 4, 0, 0.5, 0.1, 6)
    assert abs(p[0] - 1.5 * 3.1 / 9.6) < 1e-12 and abs(p[1] - 2.5 * 0.1 / 10.6) < 1e-12
    assert abs(p[0] / sum(p) - 0.9536) < 1e-4
