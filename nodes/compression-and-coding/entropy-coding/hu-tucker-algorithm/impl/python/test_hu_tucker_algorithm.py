# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hu-tucker-algorithm/. The authors are listed in prov/6C5RSP.jsonl.

import random

import pytest

from hu_tucker_algorithm import build_from_depths, hu_tucker, leaf_depths, tree_depths


def interval_dp(weights) -> int:
    """The O(n^3) interval program for the optimal alphabetic tree."""
    n = len(weights)
    pre = [0]
    for w in weights:
        pre.append(pre[-1] + w)
    c = [[0] * n for _ in range(n)]
    for size in range(2, n + 1):
        for i in range(n - size + 1):
            j = i + size - 1
            c[i][j] = pre[j + 1] - pre[i] + min(c[i][k] + c[k + 1][j] for k in range(i, j))
    return c[0][n - 1]


def test_worked_example() -> None:
    # Phase 1 combines E F, then C D, then B with (E F), then A with (C D).
    w = [10, 8, 3, 6, 2, 1]
    cost, depths, tree = hu_tucker(w)
    assert depths == [2, 2, 3, 3, 3, 3]
    assert cost == 72 == interval_dp(w)
    assert tree == ((0, 1), ((2, 3), (4, 5)))
    # A tie: depths 3, 3, 2, 2, 2 and 2, 2, 2, 3, 3 both cost 37 here.
    assert hu_tucker([4, 1, 6, 2, 3])[:2] == (37, [3, 3, 2, 2, 2])


def test_combination_tree_is_not_alphabetic_but_levels_are_right() -> None:
    # Phase 1 first combines the middle 2 and 2 into a circle node of
    # weight 4. The outer squares 3 and 3 are then compatible across it,
    # and 3 + 3 < 3 + 4, so they are combined: the tree of phase 1 has the
    # leaves in the order 0, 3, 1, 2. Phase 3 puts them back in order.
    w = [3, 2, 2, 3]
    cost, depths, tree = hu_tucker(w)
    assert depths == [2, 2, 2, 2]
    assert cost == interval_dp(w) == 20
    assert tree == ((0, 1), (2, 3))


def test_equals_interval_dp_on_random_inputs() -> None:
    rng = random.Random(1971)
    for trial in range(1500):
        n = rng.randint(1, 12)
        top = 4 if trial % 2 else 100  # small weights give many ties
        w = [rng.randint(1, top) for _ in range(n)]
        cost, depths, tree = hu_tucker(w)
        assert cost == interval_dp(w), w
        assert tree_depths(tree, n) == depths


def test_sorted_weights_give_huffman_cost() -> None:
    w = [1, 1, 2, 3, 5, 8, 13, 21]
    # A Huffman tree has the depths 7, 7, 6, 5, 4, 3, 2, 1 and cost 132.
    assert hu_tucker(w)[0] == interval_dp(w) == 132


def test_build_rejects_bad_depths() -> None:
    with pytest.raises(ValueError):
        build_from_depths([1, 2, 1])
    assert build_from_depths([0]) == 0
    assert leaf_depths([9]) == [0]
