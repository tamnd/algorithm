# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bayesian-phylogenetic-inference/. The authors are listed in prov/SBJ5QF.jsonl.

import itertools
import math
import random

from bayesian_phylogenetic_inference import (
    LENGTHS,
    STATES,
    edge_splits,
    jc_prob,
    log_likelihood,
    mcmc,
    proposals,
    propose,
    topology_of,
)

# Five taxa A..E and six sites. The exact posterior gives 0.376 to each of ((A,B),C,(D,E))
# and ((A,B),D,(C,E)), so the chain must move between topologies to match it.
SEQS = ["ACGTTA", "ACGTTG", "ACATCG", "GCATTG", "GTATCG"]


def all_trees(n):
    trees = [{0: {n}, 1: {n}, 2: {n}, n: {0, 1, 2}}]
    for k in range(3, n):
        nxt = []
        for t in trees:
            new = n + k - 2
            for x, y in sorted((x, y) for x in t for y in t[x] if x < y):
                t2 = {v: set(nb) for v, nb in t.items()}
                t2[x].discard(y)
                t2[y].discard(x)
                t2[new] = {x, y, k}
                t2[x].add(new)
                t2[y].add(new)
                t2[k] = {new}
                nxt.append(t2)
        trees = nxt
    return trees


def all_states(n):
    for t in all_trees(n):
        splits = sorted(edge_splits(t, n).values(), key=sorted)
        for vals in itertools.product(LENGTHS, repeat=len(splits)):
            yield t, dict(zip(splits, vals))


def brute_likelihood(tree, lengths, seqs):
    """Sum over all assignments of states to internal vertices, times pi at leaf 0."""
    n = len(seqs)
    internal = sorted(v for v in tree if v >= n)
    es = edge_splits(tree, n)
    total = 1.0
    for j in range(len(seqs[0])):
        site = 0.0
        for lab in itertools.product(STATES, repeat=len(internal)):
            st = dict(zip(internal, lab))
            for i in range(n):
                st[i] = seqs[i][j]
            p = 0.25
            for (a, b), s in es.items():
                same, diff = jc_prob(lengths[s])
                p *= same if st[a] == st[b] else diff
            site += p
        total *= site
    return total


def exact_topology_posterior(seqs):
    n = len(seqs)
    logs = [(topology_of(l, n), log_likelihood(t, l, seqs)) for t, l in all_states(n)]
    top = max(x for _, x in logs)
    post = {}
    for k, x in logs:
        post[k] = post.get(k, 0.0) + math.exp(x - top)
    z = sum(post.values())
    return {k: v / z for k, v in post.items()}


def test_pruning_matches_brute_force():
    rng = random.Random(1)
    states = list(all_states(5))
    for _ in range(25):
        t, l = rng.choice(states)
        assert math.isclose(math.exp(log_likelihood(t, l, SEQS[:])), brute_likelihood(t, l, SEQS), rel_tol=1e-9)


def test_state_count():
    assert sum(1 for _ in all_states(5)) == 15 * 2**7


def test_proposals_are_symmetric_and_sum_to_one():
    n = 5
    rng = random.Random(2)
    states = list(all_states(n))
    for _ in range(60):
        t, l = rng.choice(states)
        moves = list(proposals(t, l, n))
        assert math.isclose(sum(q for q, _, _ in moves), 1.0)
        key = frozenset(l.items())
        for q, t2, l2 in moves:
            back = [q2 for q2, _, l3 in proposals(t2, l2, n) if frozenset(l3.items()) == key]
            assert len(back) == 1 and math.isclose(back[0], q)


def test_propose_draws_from_proposals():
    n = 5
    t, l = next(all_states(n))
    want = {frozenset(l2.items()): q for q, _, l2 in proposals(t, l, n)}
    rng = random.Random(3)
    draws = 12000
    got = {}
    for _ in range(draws):
        _, l2 = propose(t, l, n, rng)
        k = frozenset(l2.items())
        got[k] = got.get(k, 0) + 1
    assert set(got) == set(want)
    for k, q in want.items():
        assert abs(got[k] / draws - q) < 5 * math.sqrt(q * (1 - q) / draws)


def test_mcmc_matches_exact_posterior():
    exact = exact_topology_posterior(SEQS)
    start = all_trees(5)[0]
    est = mcmc(SEQS, start, 60000, 2000, random.Random(12345))
    tv = 0.5 * sum(abs(est.get(k, 0.0) - exact[k]) for k in exact)
    assert tv < 0.03
