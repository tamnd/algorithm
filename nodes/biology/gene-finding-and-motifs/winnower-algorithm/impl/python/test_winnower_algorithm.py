# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/winnower-algorithm/. The authors are listed in prov/561KFN.jsonl.

import itertools
import random

import pytest

from bioseq import DNA, hamming, random_dna
from winnower_algorithm import build_graph, cliques, consensus, edge_set, winnow, winnower


def plant(rng, n, G, L, d):
    """Plant a random motif with exactly d changes in each of n random sequences.

    Draw order: random_dna for the motif; then for each sequence random_dna(G),
    rng.randrange(G - L + 1), rng.sample(range(L), d) and one rng.choice per
    changed position.
    """
    motif = random_dna(rng, L)
    seqs, starts = [], []
    for _ in range(n):
        bg = random_dna(rng, G)
        q = rng.randrange(G - L + 1)
        inst = list(motif)
        for j in rng.sample(range(L), d):
            inst[j] = rng.choice([b for b in DNA if b != inst[j]])
        seqs.append(bg[:q] + "".join(inst) + bg[q + L:])
        starts.append(q)
    return motif, seqs, starts


def brute_cliques(seqs, L, d):
    ranges = [range(len(s) - L + 1) for s in seqs]
    out = []
    for p in itertools.product(*ranges):
        w = [s[q:q + L] for s, q in zip(seqs, p)]
        if all(hamming(a, b) <= 2 * d for a, b in itertools.combinations(w, 2)):
            out.append(p)
    return out


def winnow_in_random_order(seqs, L, d, rng):
    """The same pruning rule, one edge at a time, in a random order, until no edge can go."""
    n = len(seqs)
    adj = build_graph(seqs, L, d)
    while True:
        edges = sorted(edge_set(adj))
        rng.shuffle(edges)
        for u, v in edges:
            if any(adj[u][p].isdisjoint(adj[v][p]) for p in range(n) if p not in (u[0], v[0])):
                adj[u][v[0]].discard(v)
                adj[v][u[0]].discard(u)
                break
        else:
            return edge_set(adj)


def instances():
    rng = random.Random(21)
    out = []
    for _ in range(12):
        n, L, d = rng.randint(3, 4), rng.randint(3, 5), rng.randint(0, 1)
        if rng.random() < 0.5:
            out.append(([random_dna(rng, rng.randint(L, 10)) for _ in range(n)], L, d))
        else:
            out.append((plant(rng, n, 10, L, d)[1], L, d))
    return out


def test_cliques_equal_brute_force():
    for seqs, L, d in instances():
        r = winnower(seqs, L, d)
        assert sorted(r.cliques) == brute_cliques(seqs, L, d)
        # Backtracking on the unpruned graph gives the same list.
        assert cliques(build_graph(seqs, L, d), len(seqs)) == list(r.cliques)


def test_every_left_edge_is_extendable_and_pruning_is_idempotent():
    for seqs, L, d in instances():
        n = len(seqs)
        adj = build_graph(seqs, L, d)
        winnow(adj, n)
        for u, v in edge_set(adj):
            for p in range(n):
                if p not in (u[0], v[0]):
                    assert adj[u][p] & adj[v][p]
        before = edge_set(adj)
        assert winnow(adj, n) == 1 and edge_set(adj) == before


def test_result_does_not_depend_on_the_order():
    rng = random.Random(5)
    for seqs, L, d in instances()[:6]:
        assert winnow_in_random_order(seqs, L, d, rng) == winnower(seqs, L, d).edges


def test_planted_clique_survives():
    # Measured on seeds 0 to 2 at (n, G, L, d) = (8, 100, 11, 2): about 1900 to
    # 2100 edges before and 28 after, and the planted starts are the only clique.
    for seed in range(3):
        motif, seqs, starts = plant(random.Random(seed), 8, 100, 11, 2)
        r = winnower(seqs, 11, 2)
        assert r.edges_before > 1800 and r.edges_after == 28
        assert r.cliques == (tuple(starts),)
        # On these seeds the consensus of the clique is the planted motif (not true for every input).
        assert consensus([s[q:q + 11] for s, q in zip(seqs, starts)]) == motif


def test_errors():
    with pytest.raises(ValueError):
        winnower(["ACGT"], 2, 1)
    with pytest.raises(ValueError):
        winnower(["ACGT", "AC"], 3, 0)
    with pytest.raises(ValueError):
        winnower(["ACGT", "ACGT"], 2, -1)
    with pytest.raises(ValueError):
        winnower(["ACGT", "ACXT"], 2, 0)
