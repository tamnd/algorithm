# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gusfield-perfect-phylogeny/. The authors are listed in prov/TF5DB1.jsonl.

import random
from typing import FrozenSet, List, Sequence, Set, Tuple

from gusfield_perfect_phylogeny import (
    four_gamete_test,
    gusfield_rooted,
    gusfield_unrooted,
    newick,
    radix_sort_columns,
)


def rooted_binary_trees(labels: Sequence[int]) -> List[Set[FrozenSet[int]]]:
    """All rooted binary trees on the labels, each given by its set of clusters (all (2k-3)!! of them)."""
    trees: List[object] = [labels[0]]
    for x in labels[1:]:
        new: List[object] = []
        for t in trees:
            # insert x on every edge, including the edge above the root
            stack = [(t, ())]
            while stack:
                node, path = stack.pop()
                new.append(_replace(t, path, (node, x)))
                if isinstance(node, tuple):
                    stack.append((node[0], path + (0,)))
                    stack.append((node[1], path + (1,)))
        trees = new
    return [_clusters(t) for t in trees]


def _replace(t: object, path: Tuple[int, ...], sub: object) -> object:
    if not path:
        return sub
    assert isinstance(t, tuple)
    if path[0] == 0:
        return (_replace(t[0], path[1:], sub), t[1])
    return (t[0], _replace(t[1], path[1:], sub))


def _clusters(t: object) -> Set[FrozenSet[int]]:
    out: Set[FrozenSet[int]] = set()
    stack = [(t, False)]
    memo = {}
    while stack:
        node, done = stack.pop()
        if not isinstance(node, tuple):
            memo[id(node), node] = frozenset([node])
            out.add(frozenset([node]))
            continue
        if not done:
            stack.append((node, True))
            stack.append((node[0], False))
            stack.append((node[1], False))
            continue
        a = memo[id(node[0]), node[0]]
        b = memo[id(node[1]), node[1]]
        memo[id(node), node] = a | b
        out.add(a | b)
    return out


def brute_rooted(M: List[List[int]]) -> bool:
    """A rooted perfect phylogeny with all-zero ancestor exists iff some rooted binary tree
    on the distinct rows has every nonempty column set as a cluster."""
    distinct = sorted(set(tuple(r) for r in M))
    idx = list(range(len(distinct)))
    cols = []
    for c in range(len(M[0])):
        s = frozenset(i for i in idx if distinct[i][c] == 1)
        if s:
            cols.append(s)
    return any(all(s in cl for s in cols) for cl in rooted_binary_trees(idx))


def brute_unrooted(M: List[List[int]]) -> bool:
    """An unrooted perfect phylogeny exists iff some unrooted binary tree on the distinct rows
    shows every column split. An unrooted tree is a rooted tree on rows 1.. with row 0 above the root."""
    distinct = sorted(set(tuple(r) for r in M))
    k = len(distinct)
    if k <= 2:
        return True
    sides = []
    for c in range(len(M[0])):
        s = frozenset(i for i in range(k) if distinct[i][c] != distinct[0][c])
        if s:
            sides.append(s)  # the side without distinct row 0
    return any(all(s in cl for s in sides) for cl in rooted_binary_trees(list(range(1, k))))


def check_tree(M: List[List[int]], t) -> None:
    n, m = len(M), len(M[0])
    fl = set(t.flipped)
    N = [[(1 - M[i][c]) if c in fl else M[i][c] for c in range(m)] for i in range(n)]
    seen: List[int] = []
    for j in range(1, len(t.parent)):
        assert 0 <= t.parent[j] < j  # parents come earlier in the sorted order
        seen.extend(t.labels[j])
    nonzero = [c for c in range(m) if any(N[i][c] for i in range(n))]
    assert sorted(seen) == nonzero  # each nonzero column labels exactly one edge
    for i in range(n):
        assert t.path_characters(i) == [c for c in range(m) if N[i][c] == 1]


def tree_matrix(rng: random.Random, n: int, m: int) -> List[List[int]]:
    """Rows of a random rooted tree: each column is the set of leaves below a random node."""
    t: object = 0
    for x in range(1, n):
        path: Tuple[int, ...] = ()
        node = t
        while isinstance(node, tuple) and rng.random() < 0.6:
            b = rng.randrange(2)
            path += (b,)
            node = node[b]
        t = _replace(t, path, (node, x) if rng.random() < 0.5 else (x, node))
    cl = sorted(_clusters(t), key=sorted)
    M = [[0] * m for _ in range(n)]
    for c in range(m):
        s = rng.choice(cl)
        for i in s:
            M[i][c] = 1
    return M


def test_radix_sort_is_decreasing_binary_order():
    rng = random.Random(1)
    for _ in range(200):
        n, m = rng.randint(1, 7), rng.randint(1, 9)
        M = [[rng.randint(0, 1) for _ in range(m)] for _ in range(n)]
        order = radix_sort_columns(M, m)
        keys = [tuple(M[i][c] for i in range(n)) for c in order]
        assert sorted(order) == list(range(m))
        assert keys == sorted(keys, reverse=True)


def test_worked_example():
    M = [
        [1, 1, 0, 0, 0],
        [0, 0, 1, 0, 0],
        [1, 1, 0, 0, 1],
        [0, 0, 1, 1, 0],
        [0, 1, 0, 0, 0],
    ]
    assert radix_sort_columns(M, 5) == [1, 0, 2, 4, 3]
    t = gusfield_rooted(M)
    assert t is not None
    assert t.parent == [0, 0, 1, 0, 2, 3]
    assert t.labels == [[], [1], [0], [2], [4], [3]]
    assert t.leaf_of_row == [2, 3, 4, 5, 1]
    check_tree(M, t)
    assert newick(t, "ABCDE") == "((E,(A,(C)c4)c0)c1,(B,(D)c3)c2)"
    # adding column (1,0,0,0,1) makes columns 0 and 5 overlap without nesting
    M2 = [r + [x] for r, x in zip(M, [1, 0, 0, 0, 1])]
    assert gusfield_rooted(M2) is None
    assert not four_gamete_test(M2 + [[0] * 6])


def test_rooted_against_brute_force():
    rng = random.Random(7)
    agree = 0
    for trial in range(700):
        n, m = rng.randint(1, 6), rng.randint(1, 5)
        if trial % 2:
            M = tree_matrix(rng, n, m)
        else:
            M = [[int(rng.random() < 0.4) for _ in range(m)] for _ in range(n)]
        t = gusfield_rooted(M)
        assert (t is not None) == brute_rooted(M)
        if t is not None:
            check_tree(M, t)
            agree += 1
    assert agree > 250


def test_unrooted_against_brute_force_and_four_gametes():
    rng = random.Random(11)
    yes = no = 0
    for trial in range(1200):
        n, m = rng.randint(1, 6), rng.randint(1, 5)
        M = [[rng.randint(0, 1) for _ in range(m)] for _ in range(n)]
        if trial % 3 == 0:
            M = tree_matrix(rng, n, m)
            flips = [rng.randint(0, 1) for _ in range(m)]
            M = [[x ^ f for x, f in zip(r, flips)] for r in M]
        t = gusfield_unrooted(M)
        b = brute_unrooted(M)
        assert (t is not None) == b == four_gamete_test(M)
        if t is not None:
            assert t.leaf_of_row[0] == 0
            check_tree(M, t)
            yes += 1
        else:
            no += 1
    assert yes > 300 and no > 100


def test_duplicate_zero_and_full_columns():
    M = [[1, 0, 1, 1], [1, 0, 1, 0], [1, 0, 1, 0]]
    t = gusfield_rooted(M)
    assert t is not None
    assert t.labels[1] == [0, 2]  # equal columns share one edge, the all-zero column labels none
    check_tree(M, t)


def test_large_instance_from_a_tree():
    rng = random.Random(5)
    M = tree_matrix(rng, 300, 300)
    t = gusfield_rooted(M)
    assert t is not None
    check_tree(M, t)
