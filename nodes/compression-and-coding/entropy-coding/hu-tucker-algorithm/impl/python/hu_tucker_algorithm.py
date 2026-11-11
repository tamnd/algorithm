# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hu-tucker-algorithm/. The authors are listed in prov/6C5RSP.jsonl.

"""The Hu-Tucker algorithm (1971) for optimal alphabetic trees, in its
simple O(n^2) form.

Phase 1 (combination). Keep a list of nodes. At first every node is a
square node, one per leaf. Two nodes are compatible when no square node
lies strictly between them. Repeatedly take the compatible pair with the
least weight sum (ties: the leftmost left node, then the leftmost right
node), replace the left node by a circle node of the summed weight and
remove the right node. Circle nodes do not block compatibility.

Phase 2 (levels). Read the depth of every leaf in the tree of phase 1.

Phase 3 (recombination). Build the alphabetic tree with these leaf
depths, left to right, with a stack.

Each step of phase 1 scans the list once. The list splits into blocks:
the nodes from one square node to the next, both included. Two nodes are
compatible exactly when they lie in a common block, and in a block the
best pair is its two smallest nodes by (weight, position).
"""

from typing import Sequence, Union

Tree = Union[int, tuple]  # a leaf index, or a pair (left, right)


def _best_pair(nodes: list) -> tuple[int, int]:
    """Positions (i, j), i < j, of the least compatible pair."""
    best = None
    squares = [p for p, node in enumerate(nodes) if node[1]]
    bounds = [0] + squares + [len(nodes) - 1]
    for a, b in zip(bounds, bounds[1:]):
        # the block is nodes[a..b]; skip blocks that hold fewer than two nodes
        first = second = None
        for p in range(a, b + 1):
            key = (nodes[p][0], p)
            if first is None or key < first:
                first, second = key, first
            elif second is None or key < second:
                second = key
        if second is None:
            continue
        i, j = sorted((first[1], second[1]))
        cand = (first[0] + second[0], i, j)
        if best is None or cand < best:
            best = cand
    return best[1], best[2]


def leaf_depths(weights: Sequence[int]) -> list[int]:
    """Phases 1 and 2: the depth of each leaf in an optimal alphabetic tree."""
    n = len(weights)
    if n == 0:
        raise ValueError("need at least one symbol")
    # a node is (weight, is_square, tree), where tree is a leaf index or a pair
    nodes = [(w, True, i) for i, w in enumerate(weights)]  # @line L1
    while len(nodes) > 1:  # @line L2
        i, j = _best_pair(nodes)  # @line L3
        wi, _, ti = nodes[i]  # @line L4
        wj, _, tj = nodes.pop(j)
        nodes[i] = (wi + wj, False, (ti, tj))
    depth = [0] * n  # @line L5
    stack = [(nodes[0][2], 0)]
    while stack:
        t, d = stack.pop()
        if isinstance(t, int):
            depth[t] = d
        else:
            stack.append((t[0], d + 1))
            stack.append((t[1], d + 1))
    return depth


def build_from_depths(depths: Sequence[int]) -> Tree:
    """Phase 3: the alphabetic tree with these leaf depths, if one exists."""
    stack: list[tuple[int, Tree]] = []
    for i, d in enumerate(depths):
        stack.append((d, i))
        while len(stack) >= 2 and stack[-1][0] == stack[-2][0]:
            d2, right = stack.pop()
            _, left = stack.pop()
            stack.append((d2 - 1, (left, right)))
    if len(stack) != 1 or stack[0][0] != 0:
        raise ValueError("no alphabetic tree has these depths")
    return stack[0][1]


def hu_tucker(weights: Sequence[int]) -> tuple[int, list[int], Tree]:
    """Cost, leaf depths and an optimal alphabetic tree."""
    depths = leaf_depths(weights)
    tree = build_from_depths(depths)  # @line L6
    return sum(w * d for w, d in zip(weights, depths)), depths, tree


def tree_depths(tree: Tree, n: int) -> list[int]:
    out = [0] * n
    stack = [(tree, 0)]
    order = []
    while stack:
        t, d = stack.pop()
        if isinstance(t, int):
            out[t] = d
            order.append(t)
        else:
            stack.append((t[1], d + 1))
            stack.append((t[0], d + 1))
    if order != list(range(n)):
        raise ValueError("leaves are not in order")
    return out
