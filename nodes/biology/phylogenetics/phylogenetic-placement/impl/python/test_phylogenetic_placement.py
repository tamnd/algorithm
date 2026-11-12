# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/phylogenetic-placement/. The authors are listed in prov/YT5XE3.jsonl.

import itertools
import math
import random

from phylogenetic_placement import edge_log_likelihood, directed_partials, edges_of, likelihood_weight_ratios, place

STATES = "ACGT"


def random_tree(n, rng):
    """A random unrooted binary tree on leaves 0 .. n - 1, by random stepwise addition."""
    tree = {0: {n}, 1: {n}, 2: {n}, n: {0, 1, 2}}
    for k in range(3, n):
        x, y = rng.choice(edges_of(tree))
        new = n + k - 2
        tree[x].discard(y)
        tree[y].discard(x)
        tree[new] = {x, y, k}
        tree[x].add(new)
        tree[y].add(new)
        tree[k] = {new}
    lengths = {frozenset(e): rng.choice([0.05, 0.1, 0.2, 0.4]) for e in edges_of(tree)}
    return tree, lengths


def jc(t, x, y):
    e = math.exp(-4.0 * t / 3.0)
    return 0.25 + 0.75 * e if x == y else 0.25 - 0.25 * e


def augment(tree, lengths, u, v, a, p):
    """The tree with a new vertex on edge {u, v} at distance a from u and a leaf "q" on it."""
    t = {x: set(nb) for x, nb in tree.items()}
    ln = dict(lengths)
    total = ln.pop(frozenset((u, v)))
    t[u].discard(v)
    t[v].discard(u)
    t["x"] = {u, v, "q"}
    t[u].add("x")
    t[v].add("x")
    t["q"] = {"x"}
    ln[frozenset((u, "x"))] = a
    ln[frozenset(("x", v))] = total - a
    ln[frozenset(("x", "q"))] = p
    return t, ln


def brute_log_likelihood(tree, lengths, leaf_seq):
    """Sum over all states of the internal vertices, with the stationary 1/4 at one vertex."""
    internal = sorted((x for x in tree if x not in leaf_seq), key=str)
    edges = [(x, y) for x in tree for y in tree[x] if str(x) < str(y)]
    m = len(next(iter(leaf_seq.values())))
    total = 0.0
    for j in range(m):
        site = 0.0
        for lab in itertools.product(STATES, repeat=len(internal)):
            st = dict(zip(internal, lab))
            for leaf, s in leaf_seq.items():
                st[leaf] = s[j]
            pr = 0.25
            for x, y in edges:
                pr *= jc(lengths[frozenset((x, y))], st[x], st[y])
            site += pr
        total += math.log(site)
    return total


def pruning_log_likelihood(tree, lengths, leaf_seq):
    """Plain Felsenstein pruning rooted at an internal vertex, recomputed from scratch."""
    root = next(x for x in tree if x not in leaf_seq)
    parent = {root: None}
    order = [root]
    stack = [root]
    while stack:
        x = stack.pop()
        for y in tree[x]:
            if y not in parent:
                parent[y] = x
                order.append(y)
                stack.append(y)
    m = len(next(iter(leaf_seq.values())))
    total = 0.0
    for j in range(m):
        part = {}
        for x in reversed(order):
            if x in leaf_seq:
                part[x] = [1.0 if c == leaf_seq[x][j] else 0.0 for c in STATES]
                continue
            vec = [1.0] * 4
            for y in tree[x]:
                if parent.get(y) == x:
                    t = lengths[frozenset((x, y))]
                    vec = [vec[i] * sum(jc(t, STATES[i], STATES[k]) * part[y][k] for k in range(4)) for i in range(4)]
            part[x] = vec
        total += math.log(0.25 * sum(part[root]))
    return total


def leaf_map(seqs, query):
    d = {i: s for i, s in enumerate(seqs)}
    d["q"] = query
    return d


def test_edge_likelihood_matches_brute_force_sum():
    rng = random.Random(1)
    for n in (4, 5):
        for _ in range(3):
            tree, lengths = random_tree(n, rng)
            seqs = ["".join(rng.choice(STATES) for _ in range(3)) for _ in range(n)]
            query = "".join(rng.choice(STATES) for _ in range(3))
            down = directed_partials(tree, lengths, seqs)
            for u, v in edges_of(tree):
                t = lengths[frozenset((u, v))]
                a, p = rng.choice([0.0, 0.3, 0.5, 1.0]) * t, rng.choice([0.01, 0.2])
                fast = edge_log_likelihood(down[(u, v)], down[(v, u)], t, a, p, query)
                at, al = augment(tree, lengths, u, v, a, p)
                assert math.isclose(fast, brute_log_likelihood(at, al, leaf_map(seqs, query)), rel_tol=1e-9)


def test_place_matches_full_recomputation_on_every_edge():
    rng = random.Random(2)
    fractions, pendants = (0.25, 0.5, 0.75), (0.02, 0.1, 0.3)
    for n in (5, 7, 9):
        tree, lengths = random_tree(n, rng)
        seqs = ["".join(rng.choice(STATES) for _ in range(12)) for _ in range(n)]
        query = "".join(rng.choice(STATES) for _ in range(12))
        best = place(tree, lengths, seqs, query, fractions, pendants)
        assert set(best) == set(edges_of(tree)) and len(best) == 2 * n - 3
        for u, v in edges_of(tree):
            t = lengths[frozenset((u, v))]
            scores = []
            for f in fractions:
                for p in pendants:
                    at, al = augment(tree, lengths, u, v, f * t, p)
                    scores.append(pruning_log_likelihood(at, al, leaf_map(seqs, query)))
            assert math.isclose(best[(u, v)][0], max(scores), rel_tol=1e-9)


def test_likelihood_weight_ratios():
    rng = random.Random(3)
    tree, lengths = random_tree(6, rng)
    seqs = ["".join(rng.choice(STATES) for _ in range(10)) for _ in range(6)]
    best = place(tree, lengths, seqs, seqs[2][:7] + "ACG", (0.5,), (0.05, 0.2))
    lwr = likelihood_weight_ratios(best)
    assert math.isclose(sum(lwr.values()), 1.0)
    assert all(0.0 < x <= 1.0 for x in lwr.values())
    top = max(best, key=lambda e: best[e][0])
    assert lwr[top] == max(lwr.values())


def test_same_point_on_two_edges_gives_same_likelihood():
    """Attaching at an internal vertex u is the same tree whichever edge of u is used."""
    rng = random.Random(4)
    tree, lengths = random_tree(7, rng)
    seqs = ["".join(rng.choice(STATES) for _ in range(8)) for _ in range(7)]
    query = "".join(rng.choice(STATES) for _ in range(8))
    down = directed_partials(tree, lengths, seqs)
    for u in (x for x in tree if len(tree[x]) == 3):
        vals = []
        for v in tree[u]:
            x, y = min(u, v), max(u, v)
            t = lengths[frozenset((x, y))]
            a = 0.0 if x == u else t
            vals.append(edge_log_likelihood(down[(x, y)], down[(y, x)], t, a, 0.1, query))
        assert all(math.isclose(vals[0], z, rel_tol=1e-9) for z in vals)


def test_query_equal_to_a_leaf_goes_next_to_it():
    # Reference tree ((0,1),2,(3,4)) with equal branch lengths, and the query a copy of taxon 3.
    tree = {0: {5}, 1: {5}, 2: {6}, 3: {7}, 4: {7}, 5: {0, 1, 6}, 6: {2, 5, 7}, 7: {3, 4, 6}}
    lengths = {frozenset(e): 0.1 for e in edges_of(tree)}
    seqs = ["AAAAAAAAAA", "AAAAAAAAAC", "AAAACCCCCC", "GGGGTTTTTT", "GGGTTTTTTT"]
    best = place(tree, lengths, seqs, seqs[3], (0.1, 0.5, 0.9), (0.01, 0.1))
    assert max(best, key=lambda e: best[e][0]) == (3, 7)
