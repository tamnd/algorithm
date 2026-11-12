# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/split-system/. The authors are listed in prov/1ZMY7S.jsonl.

import itertools
import random

import pytest

from split_system import SplitSystem, splits_of_tree


def double_factorial(k: int) -> int:
    out = 1
    while k > 1:
        out *= k
        k -= 2
    return out


def edges(tree):
    return [(u, v) for u in tree for v in tree[u] if str(u) < str(v)]


def add_leaf_on_edge(tree, u, v, leaf, new_vertex):
    """Subdivide edge u-v by new_vertex and hang `leaf` from it. Return a new dict."""
    t = {a: list(b) for a, b in tree.items()}
    t[u][t[u].index(v)] = new_vertex
    t[v][t[v].index(u)] = new_vertex
    t[new_vertex] = [u, v, leaf]
    t[leaf] = [new_vertex]
    return t


def all_unrooted_binary(taxa):
    """Every unrooted binary tree on taxa (at least 3), by stepwise addition."""
    a, b, c = taxa[:3]
    trees = [{0: [a, b, c], a: [0], b: [0], c: [0]}]
    for k, x in enumerate(taxa[3:], start=1):
        trees = [add_leaf_on_edge(t, u, v, x, k) for t in trees for (u, v) in edges(t)]
    return trees


def random_unrooted(rng, taxa, contract=0.0):
    """A random unrooted binary tree, then each internal edge is contracted with probability `contract`."""
    a, b, c = taxa[:3]
    t = {0: [a, b, c], a: [0], b: [0], c: [0]}
    for k, x in enumerate(taxa[3:], start=1):
        u, v = rng.choice(edges(t))
        t = add_leaf_on_edge(t, u, v, x, k)
    for u, v in edges(t):
        if isinstance(u, int) and isinstance(v, int) and u in t and v in t and v in t[u] and rng.random() < contract:
            for w in t[v]:  # merge v into u
                if w != u:
                    t[w][t[w].index(v)] = u
                    t[u].append(w)
            t[u].remove(v)
            del t[v]
    return t


def names(n):
    return [f"t{i}" for i in range(n)]


def as_pairs(S: SplitSystem):
    return {frozenset([a, b]) for a, b in S.splits()}


def test_example_of_the_page():
    tree = {0: ["a", "b", 1], 1: [0, "c", 2], 2: [1, "d", "e"], "a": [0], "b": [0], "c": [1], "d": [2], "e": [2]}
    S = SplitSystem.from_tree(tree)
    assert len(S) == 7
    assert {S.side(m) for m in S.nontrivial()} == {frozenset("cde"), frozenset("de")}
    assert S.is_compatible()
    S.add("bc")
    assert not S.is_compatible()


def test_from_tree_matches_edge_removal():
    rng = random.Random(7)
    for _ in range(150):
        n = rng.randint(3, 25)
        t = random_unrooted(rng, names(n), contract=rng.choice([0.0, 0.3, 0.8]))
        assert as_pairs(SplitSystem.from_tree(t)) == splits_of_tree(t)


def test_to_tree_round_trip_and_degrees():
    rng = random.Random(11)
    for _ in range(150):
        n = rng.randint(3, 25)
        t = random_unrooted(rng, names(n), contract=rng.choice([0.0, 0.5]))
        S = SplitSystem.from_tree(t)
        t2 = S.to_tree()
        assert all(len(nb) != 2 for nb in t2.values())
        assert sorted(v for v, nb in t2.items() if len(nb) == 1) == sorted(names(n))
        assert SplitSystem.from_tree(t2, S.taxa).masks == S.masks
        # Any subset of the splits is compatible, and gives a contraction of the tree.
        sub = SplitSystem(S.taxa)
        sub.masks = {m for m in S.nontrivial() if rng.random() < 0.5}
        t3 = sub.to_tree()
        trivial = {m for m in S.masks if S.is_trivial(m)}
        assert SplitSystem.from_tree(t3, S.taxa).masks == sub.masks | trivial


def brute_compatible(X, A, C):
    B, D = X - A, X - C
    return not (A & C) or not (A & D) or not (B & C) or not (B & D)


def test_compatibility_against_definition():
    rng = random.Random(3)
    for _ in range(300):
        n = rng.randint(3, 8)
        taxa = names(n)
        X = frozenset(taxa)
        S = SplitSystem(taxa)
        sides = []
        for _ in range(rng.randint(0, 6)):
            A = frozenset(x for x in taxa if rng.random() < 0.5)
            if 0 < len(A) < n:
                S.add(A)
                sides.append(A)
        want = all(brute_compatible(X, A, C) for A, C in itertools.combinations(sides, 2))
        assert S.is_compatible() == want
        if want:
            t = S.to_tree()
            got = splits_of_tree(t)
            expect = {frozenset([A, X - A]) for A in sides} | {frozenset([frozenset([x]), X - {x}]) for x in taxa}
            assert got == expect
        else:
            with pytest.raises(ValueError):
                S.to_tree()


def test_split_systems_of_trees_are_distinct_and_counted():
    # (2n - 5)!! unrooted binary trees, and no two of them share a split system.
    for n in range(3, 8):
        trees = all_unrooted_binary(names(n))
        systems = {frozenset(SplitSystem.from_tree(t, names(n)).masks) for t in trees}
        assert len(trees) == len(systems) == double_factorial(2 * n - 5)
        assert all(len(s) == 2 * n - 3 for s in systems)


def test_rooted_binary_count():
    # Rooted binary trees as cluster sets; add leaf x above any of the 2n - 3 clusters.
    for n in range(2, 8):
        taxa = names(n)
        trees = [frozenset([frozenset([taxa[0]])])]
        for x in taxa[1:]:
            new = []
            for H in trees:
                root = max(H, key=len)
                for C in H:
                    H2 = {D | {x} if D > C else D for D in H}
                    H2 |= {C | {x}, frozenset([x])}
                    new.append(frozenset(H2))
                assert len(H) == 2 * len(root) - 1
            trees = new
        assert len(trees) == len(set(trees)) == double_factorial(2 * n - 3)


def test_bad_input():
    with pytest.raises(ValueError):
        SplitSystem(["a"])
    S = SplitSystem("abc")
    with pytest.raises(ValueError):
        S.add("")
    with pytest.raises(ValueError):
        S.add("abc")
