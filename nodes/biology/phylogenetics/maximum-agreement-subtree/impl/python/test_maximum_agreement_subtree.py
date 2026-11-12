# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/maximum-agreement-subtree/. The authors are listed in prov/THDNB4.jsonl.

import random
from typing import List

from maximum_agreement_subtree import agree_on, brute_force_mast, leaves_of, mast, restrict


def random_binary_tree(labels: List[object], rng: random.Random) -> object:
    """Join two random parts again and again, which gives a random rooted binary tree."""
    parts: List[object] = list(labels)
    rng.shuffle(parts)
    while len(parts) > 1:
        i, j = rng.sample(range(len(parts)), 2)
        a, b = parts[i], parts[j]
        parts = [p for k, p in enumerate(parts) if k not in (i, j)] + [(a, b)]
    return parts[0]


def random_tree(labels: List[object], rng: random.Random) -> object:
    """A random rooted tree in which internal nodes may have up to four children."""
    parts: List[object] = list(labels)
    rng.shuffle(parts)
    while len(parts) > 1:
        k = min(len(parts), rng.choice((2, 2, 3, 4)))
        idx = rng.sample(range(len(parts)), k)
        group = tuple(parts[i] for i in idx)
        parts = [p for q, p in enumerate(parts) if q not in idx] + [group]
    return parts[0]


def check(t1, t2):
    r = mast(t1, t2)
    assert r.size == len(r.leaves)
    assert agree_on(t1, t2, r.leaves)
    assert r.size == brute_force_mast(t1, t2)
    return r


def test_worked_example():
    t1 = (("A", "B"), ("C", ("D", "E")))
    t2 = (("A", "C"), ("B", ("D", "E")))
    r = check(t1, t2)
    assert r.size == 3
    assert brute_force_mast(t1, t2) == 3
    assert r.leaves >= {"D", "E"}
    assert not agree_on(t1, t2, {"A", "B", "D", "E"})
    assert restrict(t1, {"A", "B", "D", "E"}) == (("A", "B"), ("D", "E"))
    assert restrict(t2, {"A", "B", "D", "E"}) == ("A", ("B", ("D", "E")))


def test_caterpillars_in_opposite_order():
    # (((1,2),3),4)... against (((n,n-1),n-2),...): any three leaves disagree, so MAST = 2
    n = 7
    t1: object = 1
    t2: object = n
    for x in range(2, n + 1):
        t1 = (t1, x)
    for x in range(n - 1, 0, -1):
        t2 = (t2, x)
    r = check(t1, t2)
    assert r.size == 2


def test_identical_trees():
    rng = random.Random(3)
    for n in range(1, 30):
        t = random_binary_tree(list(range(n)), rng)
        r = mast(t, t)
        assert r.size == n
        assert r.tree == t


def test_binary_against_brute_force():
    rng = random.Random(1)
    for _ in range(400):
        n = rng.randint(2, 9)
        labels = list(range(n))
        check(random_binary_tree(labels, rng), random_binary_tree(labels, rng))


def test_general_degree_against_brute_force():
    rng = random.Random(2)
    for _ in range(300):
        n = rng.randint(2, 9)
        labels = list(range(n))
        check(random_tree(labels, rng), random_tree(labels, rng))


def test_different_label_sets():
    rng = random.Random(4)
    for _ in range(200):
        a = rng.sample(range(10), rng.randint(2, 8))
        b = rng.sample(range(10), rng.randint(2, 8))
        if len(set(a) & set(b)) == 0:
            continue
        check(random_binary_tree(a, rng), random_tree(b, rng))


def test_larger_binary_trees_run_fast():
    rng = random.Random(5)
    labels = list(range(200))
    t1 = random_binary_tree(labels, rng)
    t2 = random_binary_tree(labels, rng)
    r = mast(t1, t2)
    assert agree_on(t1, t2, r.leaves)
    assert 2 <= r.size <= 200
    assert sorted(leaves_of(r.tree)) == sorted(r.leaves)
