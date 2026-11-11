# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/garsia-wachs-algorithm/. The authors are listed in prov/Y88NT5.jsonl.

"""The Garsia-Wachs algorithm (1977) for optimal alphabetic trees, in its
simple O(n^2) form.

Phase 1. Put infinite sentinels at both ends of the list of weights.
Find the leftmost three neighbours x, y, z with w(x) <= w(z). Remove x and
y, make a node t of weight w(x) + w(y) with children x and y, and insert
t just after the nearest item to the left of x's old place whose weight
is at least w(t). Repeat until one node is left.

Phase 2. Read the depth of every leaf in that tree.

Phase 3. Build the alphabetic tree with these depths by a stack.
"""

from typing import Sequence, Union

Tree = Union[int, tuple]  # a leaf index, or a pair (left, right)

INF = float("inf")


def leaf_depths(weights: Sequence[int]) -> list[int]:
    """Phases 1 and 2: the leaf depths of an optimal alphabetic tree."""
    n = len(weights)
    if n == 0:
        raise ValueError("need at least one symbol")
    if any(w <= 0 for w in weights):
        raise ValueError("weights must be positive")
    # items are (weight, tree); the sentinels have no tree
    a: list = [(INF, None)] + [(w, i) for i, w in enumerate(weights)] + [(INF, None)]  # @line L1
    while len(a) > 3:  # @line L2  more than one real item
        k = 2
        while a[k - 2][0] > a[k][0]:  # @line L3  x = a[k-2], y = a[k-1], z = a[k]
            k += 1
        x, y = a[k - 2], a[k - 1]
        t = (x[0] + y[0], (x[1], y[1]))  # @line L4
        del a[k - 2 : k]
        p = k - 3  # the item just left of x's old place
        while a[p][0] < t[0]:  # @line L5  move left past lighter items
            p -= 1
        a.insert(p + 1, t)
    depth = [0] * n  # @line L6
    stack = [(a[1][1], 0)]
    while stack:
        tree, d = stack.pop()
        if isinstance(tree, int):
            depth[tree] = d
        else:
            stack.append((tree[0], d + 1))
            stack.append((tree[1], d + 1))
    return depth


def build_from_depths(depths: Sequence[int]) -> Tree:
    """Phase 3: the alphabetic tree with these leaf depths."""
    stack: list = []
    for i, d in enumerate(depths):
        stack.append((d, i))
        while len(stack) >= 2 and stack[-1][0] == stack[-2][0]:
            d2, right = stack.pop()
            _, left = stack.pop()
            stack.append((d2 - 1, (left, right)))
    if len(stack) != 1 or stack[0][0] != 0:
        raise ValueError("no alphabetic tree has these depths")
    return stack[0][1]


def garsia_wachs(weights: Sequence[int]) -> tuple[int, list[int], Tree]:
    """Cost, leaf depths and an optimal alphabetic tree."""
    depths = leaf_depths(weights)
    tree = build_from_depths(depths)  # @line L7
    return sum(w * d for w, d in zip(weights, depths)), depths, tree
