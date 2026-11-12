# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/parsimony-ratchet/. The authors are listed in prov/GM2NX0.jsonl.

import itertools
import random

from parsimony_ratchet import fitch_changes, length, parsimony_ratchet, tbr_moves, tbr_search


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


def topology(tree, n):
    parent = {0: -1}
    order = [0]
    stack = [0]
    while stack:
        v = stack.pop()
        for w in tree[v]:
            if w not in parent:
                parent[w] = v
                order.append(w)
                stack.append(w)
    below = {}
    for v in reversed(order):
        s = {v} if v < n else set()
        for w in tree[v]:
            if parent.get(w) == v:
                s |= below[w]
        below[v] = s
    return frozenset(frozenset(below[v]) for v in order[1:] if 2 <= len(below[v]) <= n - 2)


def brute_changes(tree, seqs):
    n = len(seqs)
    internal = sorted(v for v in tree if v >= n)
    edges = [(x, y) for x in tree for y in tree[x] if x < y]
    out = []
    for j in range(len(seqs[0])):
        best = None
        for lab in itertools.product("ACGT", repeat=len(internal)):
            st = dict(zip(internal, lab))
            for i in range(n):
                st[i] = seqs[i][j]
            c = sum(st[x] != st[y] for x, y in edges)
            best = c if best is None or c < best else best
        out.append(best)
    return out


# Seven taxa A..G and ten DNA sites. The tree ((A,G),D,((B,F),(C,E))) has length 33 and no
# TBR move makes it shorter, but the unique shortest tree ((A,D),B,(F,(G,(C,E)))) has length 32.
SEQS = ["CTAGCTTCGC", "TGGAACTAAT", "ATCCATGTCT", "CAGAACTAGC", "GGCCGAGAAT", "GGGTTCCGAA", "TCCTAAACTC"]
TRAP = frozenset(map(frozenset, [{1, 2, 3, 4, 5}, {1, 2, 4, 5}, {1, 5}, {2, 4}]))
OPT = frozenset(map(frozenset, [{1, 2, 4, 5, 6}, {2, 4}, {2, 4, 5, 6}, {2, 4, 6}]))


def test_fitch_matches_brute_force():
    rng = random.Random(1)
    trees = all_trees(5)
    for _ in range(30):
        seqs = ["".join(rng.choice("ACGT") for _ in range(4)) for _ in range(5)]
        t = rng.choice(trees)
        assert fitch_changes(t, seqs) == brute_changes(t, seqs)


def test_tbr_moves_reach_the_tbr_neighborhood():
    for n in (5, 6, 7):
        for t in all_trees(n)[:: 40 if n == 7 else 3]:
            keys = {topology(x, n) for x in tbr_moves(t, n)} - {topology(t, n)}
            gamma = sum(len(s) * (n - len(s)) for s in topology(t, n))
            assert len(keys) == 4 * gamma - (4 * n - 2) * (n - 3)


def test_trap_instance_escaped_by_ratchet():
    n = 7
    w = [1] * 10
    trees = all_trees(n)
    lens = {topology(t, n): length(t, SEQS, w) for t in trees}
    assert min(lens.values()) == 32 and lens[OPT] == 32 and lens[TRAP] == 33
    start = next(t for t in trees if topology(t, n) == TRAP)
    stuck, s = tbr_search(start, SEQS, w)
    assert s == 33 and topology(stuck, n) == TRAP
    best, b = parsimony_ratchet(SEQS, 3, 0.25, random.Random(1), start=start)
    assert b == 32 and topology(best, n) == OPT


def test_ratchet_properties_against_exhaustive_search():
    rng = random.Random(7)
    trees6 = all_trees(6)
    for _ in range(8):
        seqs = ["".join(rng.choice("ACGT") for _ in range(8)) for _ in range(6)]
        w = [1] * 8
        opt = min(length(t, seqs, w) for t in trees6)
        start = rng.choice(trees6)
        _, plain = tbr_search(start, seqs, w)
        best, b = parsimony_ratchet(seqs, 4, 0.25, random.Random(2), start=start)
        assert b == length(best, seqs, w)
        assert opt <= b <= plain
        assert all(length(x, seqs, w) >= b for x in tbr_moves(best, 6))


def test_default_start_runs():
    best, b = parsimony_ratchet(SEQS[:5], 2, 0.25, random.Random(3))
    assert b == length(best, SEQS[:5], [1] * 10)
    assert sorted(v for v in best if v < 5) == [0, 1, 2, 3, 4]
