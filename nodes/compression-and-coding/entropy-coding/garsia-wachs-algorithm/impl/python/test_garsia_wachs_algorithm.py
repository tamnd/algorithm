# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/garsia-wachs-algorithm/. The authors are listed in prov/Y88NT5.jsonl.

import random

import pytest

from garsia_wachs_algorithm import build_from_depths, garsia_wachs, leaf_depths


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


def hu_tucker_cost(weights) -> int:
    """A plain Hu-Tucker combination phase: the least compatible pair,
    ties to the leftmost left node and then the leftmost right node.
    Its cost is the sum of the weights of the combined nodes."""
    nodes = [(w, True) for w in weights]  # (weight, is_square)
    cost = 0
    while len(nodes) > 1:
        best = None
        for i in range(len(nodes)):
            for j in range(i + 1, len(nodes)):
                cand = (nodes[i][0] + nodes[j][0], i, j)
                if best is None or cand < best:
                    best = cand
                if nodes[j][1]:
                    break  # a square node blocks the pairs beyond it
        s, i, j = best
        cost += s
        nodes.pop(j)
        nodes[i] = (s, False)
    return cost


def tree_leaves_and_depths(tree, n):
    out, order, stack = [0] * n, [], [(tree, 0)]
    while stack:
        t, d = stack.pop()
        if isinstance(t, int):
            out[t] = d
            order.append(t)
        else:
            stack.append((t[1], d + 1))
            stack.append((t[0], d + 1))
    return order, out


def test_worked_example() -> None:
    w = [10, 8, 3, 6, 2, 1]
    cost, depths, tree = garsia_wachs(w)
    assert depths == [2, 2, 3, 3, 3, 3]
    assert cost == 72 == interval_dp(w) == hu_tucker_cost(w)
    assert tree == ((0, 1), ((2, 3), (4, 5)))


def test_move_left_is_needed() -> None:
    # The first pair is (2, 1), at the middle; its sum 3 moves left past
    # the first 2, to the front. Then the two 2s are neighbours and combine.
    # If 3 stayed in place, the next steps would combine 3 with the last 2
    # and cost 15 in all, against the optimum 14.
    w = [2, 2, 1, 2]
    cost, depths, tree = garsia_wachs(w)
    assert (cost, depths, tree) == (14, [2, 2, 2, 2], ((0, 1), (2, 3)))
    assert interval_dp(w) == 14

    # A longer move: 2 + 2 = 4 passes 3 and stops after 5.
    w = [5, 3, 2, 2, 7]
    assert garsia_wachs(w)[:2] == (42, [2, 3, 4, 4, 1]) and interval_dp(w) == 42


def test_equals_hu_tucker_and_dp_on_random_inputs() -> None:
    rng = random.Random(1977)
    for trial in range(1500):
        n = rng.randint(1, 12)
        top = 4 if trial % 2 else 100
        w = [rng.randint(1, top) for _ in range(n)]
        cost, depths, tree = garsia_wachs(w)
        assert cost == interval_dp(w) == hu_tucker_cost(w), w
        order, d = tree_leaves_and_depths(tree, n)
        assert order == list(range(n)) and d == depths


def test_larger_inputs_against_hu_tucker() -> None:
    rng = random.Random(88)
    for _ in range(20):
        w = [rng.randint(1, 10**6) for _ in range(rng.randint(30, 80))]
        assert garsia_wachs(w)[0] == hu_tucker_cost(w) == interval_dp(w)


def test_edge_cases() -> None:
    assert leaf_depths([7]) == [0]
    assert garsia_wachs([1, 1]) == (2, [1, 1], (0, 1))
    with pytest.raises(ValueError):
        leaf_depths([1, 0, 2])
    with pytest.raises(ValueError):
        build_from_depths([2, 1, 2])
