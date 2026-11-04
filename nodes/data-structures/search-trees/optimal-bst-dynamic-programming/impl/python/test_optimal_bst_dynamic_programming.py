# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/optimal-bst-dynamic-programming/. The authors are listed in prov/5HF5N0.jsonl.

import random
from fractions import Fraction

from optimal_bst_dynamic_programming import build_tree, optimal_bst, optimal_bst_knuth, tree_cost


def all_trees(i, j):
    """Yield (root, children) for every BST shape on keys i..j (root 0 if empty)."""
    if i > j:
        yield 0, {}
        return
    for r in range(i, j + 1):
        for lr, lc in all_trees(i, r - 1):
            for rr, rc in all_trees(r + 1, j):
                ch = dict(lc)
                ch.update(rc)
                ch[r] = (lr, rr)
                yield r, ch


def brute(p, q):
    n = len(q) - 1
    if n == 0:
        return q[0]
    return min(tree_cost(ch, r, p, q) for r, ch in all_trees(1, n))


def test_clrs_example() -> None:
    p = [0] + [Fraction(x, 100) for x in (15, 10, 5, 10, 20)]
    q = [Fraction(x, 100) for x in (5, 10, 5, 5, 5, 10)]
    e, root = optimal_bst(p, q)
    assert e[1][5] == Fraction(11, 4)
    assert root[1][5] == 2
    ch = build_tree(root, 5)
    assert ch == {2: (1, 5), 1: (0, 0), 5: (4, 0), 4: (3, 0), 3: (0, 0)}
    assert tree_cost(ch, 2, p, q) == Fraction(11, 4)
    assert optimal_bst_knuth(p, q)[0] == Fraction(11, 4)


def test_small() -> None:
    assert optimal_bst([0], [7])[0][1][0] == 7
    e, root = optimal_bst([0, 3], [1, 2])
    assert e[1][1] == 3 * 1 + 1 * 2 + 2 * 2 and root[1][1] == 1


def test_random_against_brute_force() -> None:
    rng = random.Random(5150)
    for _ in range(600):
        n = rng.randint(0, 6)
        p = [0] + [rng.randint(0, 9) for _ in range(n)]
        q = [rng.randint(0, 9) for _ in range(n + 1)]
        e, root = optimal_bst(p, q)
        best = brute(p, q)
        cost = e[1][n] if n else e[1][0]
        assert cost == best
        if n:
            ch = build_tree(root, n)
            assert len(ch) == n
            assert tree_cost(ch, root[1][n], p, q) == best
        assert optimal_bst_knuth(p, q)[0] == best


def test_knuth_large_random() -> None:
    rng = random.Random(77)
    for _ in range(20):
        n = rng.randint(10, 40)
        p = [0] + [rng.randint(0, 100) for _ in range(n)]
        q = [rng.randint(0, 100) for _ in range(n + 1)]
        e, _ = optimal_bst(p, q)
        assert optimal_bst_knuth(p, q)[0] == e[1][n]
