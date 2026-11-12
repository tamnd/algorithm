# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rspr-maf-equivalence/. The authors are listed in prov/J6TD60.jsonl.

import random

from rspr_maf_equivalence import (
    RHO,
    all_rooted,
    bfs_parents,
    forest_from_path,
    forest_to_moves,
    from_tuple,
    is_agreement_forest,
    leaves,
    maf_size,
    rspr_distance,
    rspr_neighbors,
    spr,
)


def check_pair(T1, T2, parent=None):
    d, path = rspr_distance(T1, T2, parent)
    m, F = maf_size(T1, T2)
    assert d == m - 1
    # d <= m - 1: the forest gives m - 1 moves that reach T2
    moves = forest_to_moves(T1, T2, F)
    assert len(moves) == m - 1
    T = T1
    for P, Q in moves:
        T2_next = spr(T, P, Q)
        assert T2_next in rspr_neighbors(T)
        T = T2_next
    assert T == T2
    # m - 1 <= d: a shortest path gives a forest with d + 1 blocks
    G = forest_from_path(path)
    assert is_agreement_forest(T1, T2, G)
    assert len(G) <= d + 1
    return d


def test_worked_example():
    T1 = from_tuple((("a", ("b", "c")), "d"))
    T2 = from_tuple(((("a", "d"), "b"), "c"))
    assert check_pair(T1, T2) == 2
    # the forest {a, d}, {b, c} works for the trees without RHO, but no forest with RHO has 2 blocks
    assert not is_agreement_forest(T1, T2, [frozenset("ad"), frozenset({"b", "c", RHO})])
    assert not is_agreement_forest(T1, T2, [frozenset({"a", "d", RHO}), frozenset("bc")])
    F = [frozenset("a"), frozenset("b"), frozenset({"c", "d", RHO})]
    assert is_agreement_forest(T1, T2, F)
    assert len(forest_to_moves(T1, T2, F)) == 2


def test_all_pairs_up_to_four_leaves():
    for n in range(1, 5):
        R = all_rooted(list(range(n)))
        for a in R:
            parent = bfs_parents(a)
            for b in R:
                check_pair(a, b, parent)


def test_five_leaves_against_each_shape():
    R = all_rooted(list(range(5)))
    shapes = [
        ((((0, 1), 2), 3), 4),
        (((0, 1), (2, 3)), 4),
        (((0, 1), 2), (3, 4)),
    ]
    for s in shapes:
        a = from_tuple(s)
        assert a in R
        parent = bfs_parents(a)
        for b in R:
            check_pair(a, b, parent)


def test_six_leaves_sample():
    rng = random.Random(6)
    R = all_rooted(list(range(6)))
    a = rng.choice(R)
    parent = bfs_parents(a)
    assert len(parent) == len(R) == 945
    for b in rng.sample(R, 150):
        check_pair(a, b, parent)


def test_any_forest_gives_a_path():
    # forest_to_moves works for every agreement forest, not only maximum ones: m - 1 moves
    rng = random.Random(8)
    R = all_rooted(list(range(5)))
    for _ in range(40):
        a, b = rng.choice(R), rng.choice(R)
        X = leaves(a)
        singletons = [frozenset([x]) for x in sorted(X)] + [frozenset([RHO])]
        assert is_agreement_forest(a, b, singletons)
        assert len(forest_to_moves(a, b, singletons)) == len(X)
