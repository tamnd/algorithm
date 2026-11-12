# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/spr-distance/. The authors are listed in prov/B2M14X.jsonl.

import random
from itertools import combinations

from spr_distance import (
    all_rooted,
    all_unrooted,
    bfs,
    leaves,
    root_at,
    rooted_key,
    rspr_distance,
    rspr_neighbors,
    tbr_distance,
    tbr_neighbors,
    to_newick,
    unroot,
    unrooted_key,
    uspr_distance,
    uspr_neighbors,
)


def double_factorial(k):
    r = 1
    while k > 1:
        r *= k
        k -= 2
    return r


def is_rooted_binary(T, X):
    """Clusters of a rooted binary tree: laminar, 2n - 1 of them, with all singletons and X."""
    if len(T) != 2 * len(X) - 1 or X not in T:
        return False
    if any(frozenset([x]) not in T for x in X):
        return False
    for A, B in combinations(T, 2):
        if A & B and not (A <= B or B <= A):
            return False
    return True


def test_tree_counts():
    for n in range(2, 8):
        R = all_rooted(range(n))
        assert len(R) == len(set(R)) == double_factorial(2 * n - 3)
        X = frozenset(range(n))
        assert all(is_rooted_binary(T, X) for T in R[:200])
    for n in range(3, 8):
        U = all_unrooted(range(n))
        assert len(U) == len(set(U)) == double_factorial(2 * n - 5)


def test_keys_ignore_child_order_and_root_position():
    assert rooted_key((("a", "b"), "c")) == rooted_key(("c", ("b", "a")))
    assert rooted_key((("a", "b"), "c")) != rooted_key((("a", "c"), "b"))
    # the same unrooted tree with the root on three different edges
    t1 = (("a", "b"), ("c", "d"))
    t2 = ("a", ("b", ("c", "d")))
    t3 = ((("a", "b"), "c"), "d")
    assert unrooted_key(t1) == unrooted_key(t2) == unrooted_key(t3)
    assert to_newick(rooted_key((("b", "a"), "c"))) == "((a,b),c)"


def test_root_and_unroot_are_inverse():
    for n in range(3, 7):
        X = frozenset(range(n))
        for U in all_unrooted(range(n)):
            for r in X:
                R = root_at(U, X, r)
                assert is_rooted_binary(R, X - {r})
                assert unroot(R, X, r) == U


def test_rspr_moves_give_binary_trees_and_are_symmetric():
    for n in range(3, 6):
        X = frozenset(range(n))
        for T in all_rooted(range(n)):
            nb = rspr_neighbors(T)
            assert T not in nb
            for T2 in nb:
                assert is_rooted_binary(T2, X)
                assert T in rspr_neighbors(T2)


def test_uspr_neighborhood_size():
    # every unrooted binary tree with n leaves has 2(n - 3)(2n - 7) uSPR neighbors
    for n in range(4, 7):
        X = frozenset(range(n))
        for U in all_unrooted(range(n)):
            assert len(uspr_neighbors(U, X)) == 2 * (n - 3) * (2 * n - 7)


def test_unrooted_moves_are_symmetric_and_nested():
    n = 5
    X = frozenset(range(n))
    for U in all_unrooted(range(n)):
        su, st = uspr_neighbors(U, X), tbr_neighbors(U, X)
        assert su <= st
        for V in st:
            assert U in tbr_neighbors(V, X)


def test_small_distances():
    assert rspr_distance((("a", "b"), "c"), (("a", "b"), "c")) == 0
    assert rspr_distance((("a", "b"), "c"), (("a", "c"), "b")) == 1
    # four leaves: a forest without the root leaf would suggest 1, the true value is 2
    assert rspr_distance((("a", ("b", "c")), "d"), ((("a", "d"), "b"), "c")) == 2
    # with the roots forgotten, both are the quartet ad|bc
    assert uspr_distance((("a", ("b", "c")), "d"), ((("a", "d"), "b"), "c")) == 0
    assert tbr_distance((("a", ("b", "c")), "d"), ((("a", "d"), "b"), "c")) == 0
    assert uspr_distance((("a", "b"), ("c", "d")), (("a", "c"), ("b", "d"))) == 1


def test_uspr_can_exceed_tbr():
    t1 = (("A", "B"), ("C", ("D", ("E", "F"))))
    t2 = (("A", "C"), ("B", ("F", ("D", "E"))))
    assert tbr_distance(t1, t2) == 1
    assert uspr_distance(t1, t2) == 2


def test_order_of_the_three_distances():
    # TBR <= uSPR <= rSPR on the unrooted versions, and every distance is symmetric
    n = 5
    X = frozenset(range(n))
    R = all_rooted(range(n))
    rng = random.Random(7)
    for a in rng.sample(R, 4):
        dr = bfs(a, rspr_neighbors)
        ua = unrooted_of(a, X)
        du = bfs(ua, lambda U: uspr_neighbors(U, X))
        dt = bfs(ua, lambda U: tbr_neighbors(U, X))
        for b in R:
            ub = unrooted_of(b, X)
            assert dt[ub] <= du[ub] <= dr[b]
        for b in rng.sample(R, 5):
            assert bfs(b, rspr_neighbors, a)[a] == dr[b]


def unrooted_of(T, X):
    """Forget the root of a rooted key: the splits, stored by the side without min(X)."""
    ref = min(X)
    return frozenset((X - C) if ref in C else C for C in T if C != X)


def mast_size(a, b, X):
    for k in range(len(X), 0, -1):
        for S in combinations(sorted(X), k):
            S = frozenset(S)
            if {C & S for C in a} - {frozenset()} == {C & S for C in b} - {frozenset()}:
                return k
    return 0


def test_rspr_at_most_n_minus_mast():
    # moving the leaves outside an agreement subtree one at a time is a valid rSPR sequence
    n = 6
    X = frozenset(range(n))
    R = all_rooted(range(n))
    rng = random.Random(11)
    a = rng.choice(R)
    d = bfs(a, rspr_neighbors)
    assert len(d) == len(R)
    for b in rng.sample(R, 150):
        assert d[b] <= n - mast_size(a, b, X)
    assert leaves(a) == X
