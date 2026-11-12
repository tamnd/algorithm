# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/adams-consensus/. The authors are listed in prov/V4J1S8.jsonl.

import random
from itertools import combinations

import pytest

from adams_consensus import adams_consensus, clusters


def random_tree(n, rng):
    """Random rooted tree on leaves 0..n-1: merge two or three random parts at a time."""
    parts = list(range(n))
    while len(parts) > 1:
        m = 2 if len(parts) == 2 or rng.random() < 0.7 else 3
        rng.shuffle(parts)
        parts = parts[m:] + [tuple(parts[:m])]
    return parts[0]


def all_clusters_with_leaves(t, n):
    return clusters(t) | {frozenset([x]) for x in range(n)}


def brute_adams(trees, n):
    """Oracle: the Adams clusters from the cluster sets, by the definition."""
    fams = [all_clusters_with_leaves(t, n) for t in trees]
    out = set()
    todo = [frozenset(range(n))]
    while todo:
        b = todo.pop()
        if len(b) < 2:
            continue
        out.add(b)
        pieces = [b]
        for fam in fams:
            top = min((c for c in fam if b <= c), key=len)
            kids = [c for c in fam if c < top and not any(c < d < top for d in fam)]
            pieces = [p & c for p in pieces for c in kids if p & c]
        todo.extend(pieces)
    return out


def nested(fam, a, b):
    """a is nested in b in the tree with cluster family fam."""
    return any(a <= c and not b <= c for c in fam)


A, B, C, D, E, F = range(6)


def test_example_from_page():
    t1 = ((((A, B), C), D), (E, F))
    t2 = ((A, (B, (C, D))), (E, F))
    out = adams_consensus([t1, t2])
    assert out == ((A, (B, C), D), (E, F))
    bc = frozenset([B, C])
    assert bc in clusters(out)
    assert all(bc not in clusters(t) for t in (t1, t2))


def test_consensus_page_profile():
    t1 = (((A, B), C), (D, (E, F)))
    t2 = (((A, B), D), (C, (E, F)))
    t3 = ((A, (B, C)), (D, (E, F)))
    assert adams_consensus([t1, t2, t3]) == ((A, B), C, D, (E, F))


@pytest.mark.parametrize("seed", range(5))
def test_random_against_definition(seed):
    rng = random.Random(seed)
    for _ in range(120):
        n = rng.randint(1, 9)
        k = rng.randint(1, 4)
        trees = [random_tree(n, rng) for _ in range(k)]
        out = adams_consensus(trees)
        if n == 1:
            assert out == 0
            continue
        assert clusters(out) == brute_adams(trees, n)
        strict = set.intersection(*(clusters(t) for t in trees))
        assert strict <= clusters(out)


@pytest.mark.parametrize("seed", range(3))
def test_nestings_are_kept(seed):
    rng = random.Random(100 + seed)
    for _ in range(40):
        n = rng.randint(3, 6)
        trees = [random_tree(n, rng) for _ in range(rng.randint(1, 3))]
        fams = [all_clusters_with_leaves(t, n) for t in trees]
        out = all_clusters_with_leaves(adams_consensus(trees), n)
        for size_b in range(2, n + 1):
            for b in combinations(range(n), size_b):
                fb = frozenset(b)
                for size_a in range(1, size_b):
                    for a in combinations(b, size_a):
                        fa = frozenset(a)
                        if all(nested(f, fa, fb) for f in fams):
                            assert nested(out, fa, fb)


def test_rejects_bad_input():
    with pytest.raises(ValueError):
        adams_consensus([((0, 1), 2), ((0, 1), 3)])
