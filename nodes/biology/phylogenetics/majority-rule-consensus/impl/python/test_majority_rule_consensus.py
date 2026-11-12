# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/majority-rule-consensus/. The authors are listed in prov/X4MGF9.jsonl.

import random
from itertools import combinations

import pytest

from majority_rule_consensus import cluster_masks, majority_rule_consensus


def random_tree(n, rng):
    """Random rooted tree on leaves 0..n-1: merge two or three random parts at a time."""
    parts = list(range(n))
    while len(parts) > 1:
        m = 2 if len(parts) == 2 or rng.random() < 0.7 else 3
        rng.shuffle(parts)
        parts = parts[m:] + [tuple(parts[:m])]
    return parts[0]


def nontrivial(tree, n):
    """Oracle side: the clusters of size 2 to n-1, as frozensets."""
    out = set()
    stack = [(tree, False)]
    below = {}
    while stack:
        t, done = stack.pop()
        if not isinstance(t, tuple):
            below[id(t)] = frozenset([t])
            continue
        if not done:
            stack.append((t, True))
            stack.extend((c, False) for c in t)
            continue
        s = frozenset()
        for c in t:
            s |= below[id(c)] if isinstance(c, tuple) else frozenset([c])
        below[id(t)] = s
        if len(s) < n:
            out.add(s)
    return out


def compatible(a, b):
    return not (a & b) or a <= b or b <= a


def all_hierarchies(n):
    """Every rooted tree on n leaves, as its set of nontrivial clusters."""
    cand = [frozenset(c) for s in range(2, n) for c in combinations(range(n), s)]
    out = []
    stack = [(0, [])]
    while stack:
        i, chosen = stack.pop()
        if i == len(cand):
            out.append(frozenset(chosen))
            continue
        stack.append((i + 1, chosen))
        if all(compatible(cand[i], c) for c in chosen):
            stack.append((i + 1, chosen + [cand[i]]))
    return out


HIER = {n: all_hierarchies(n) for n in range(2, 6)}


def rf_sum(cl, profile):
    return sum(len(cl ^ p) for p in profile)


A, B, C, D, E, F = range(6)


def test_example_from_page():
    trees = [(((A, B), C), (D, (E, F))), (((A, B), D), (C, (E, F))), ((A, (B, C)), (D, (E, F)))]
    out, support = majority_rule_consensus(trees)
    assert out == (((A, B), C), (D, (E, F)))
    assert support == {0b000011: 2, 0b000111: 2, 0b111000: 2, 0b110000: 3}


def test_counts_of_hierarchies():
    assert [len(HIER[n]) for n in range(2, 6)] == [1, 4, 26, 236]


@pytest.mark.parametrize("seed", range(5))
def test_random_against_counting_oracle(seed):
    rng = random.Random(seed)
    for _ in range(120):
        n = rng.randint(2, 9)
        k = rng.randint(1, 7)
        trees = [random_tree(n, rng) for _ in range(k)]
        out, support = majority_rule_consensus(trees)
        freq = {}
        for t in trees:
            for c in nontrivial(t, n):
                freq[c] = freq.get(c, 0) + 1
        want = {c for c, f in freq.items() if 2 * f > k}
        assert nontrivial(out, n) == want
        assert {frozenset(x for x in range(n) if m >> x & 1) for m in support} == want
        for c in want:
            assert support[sum(1 << x for x in c)] == freq[c]


@pytest.mark.parametrize("seed", range(3))
def test_median_for_robinson_foulds(seed):
    rng = random.Random(50 + seed)
    for _ in range(60):
        n = rng.randint(3, 5)
        k = rng.randint(1, 6)
        trees = [random_tree(n, rng) for _ in range(k)]
        profile = [nontrivial(t, n) for t in trees]
        out, _ = majority_rule_consensus(trees)
        best = min(rf_sum(h, profile) for h in HIER[n])
        mine = rf_sum(nontrivial(out, n), profile)
        assert mine == best
        if k % 2 == 1:
            assert sum(1 for h in HIER[n] if rf_sum(h, profile) == best) == 1


def test_cluster_masks_and_errors():
    masks, full = cluster_masks(((0, 1), 2))
    assert sorted(masks) == [0b011, 0b111] and full == 0b111
    with pytest.raises(ValueError):
        majority_rule_consensus([((0, 1), 2), ((0, 1), 3)])
    with pytest.raises(ValueError):
        majority_rule_consensus([((0, 0), 1)])
