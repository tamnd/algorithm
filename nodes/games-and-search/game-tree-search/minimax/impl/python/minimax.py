# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/minimax/. The authors are listed in prov/4KA77P.jsonl.

"""The minimax value of a finite game tree, with values from the point of view of MAX."""

import math
from fractions import Fraction
from typing import Callable, List, Optional, Sequence, TypeVar, Union

S = TypeVar("S")
Value = Union[int, float, Fraction]  # any totally ordered number type works

# A game tree written as nested lists: a leaf is a number (its value for MAX),
# an interior node is a non-empty list of children.
Tree = Union[int, list]


def minimax(
    state: S,
    max_to_move: bool,
    children: Callable[[S], Sequence[S]],
    utility: Callable[[S], Value],
    leaf_count: Optional[List[int]] = None,
) -> Value:
    """Return the minimax value of `state`, from the point of view of MAX.

    `children(state)` lists the positions after each legal move; an empty list
    means that `state` is terminal, and then `utility(state)` is its value for
    MAX. `max_to_move` says who moves at `state`. If `leaf_count` is a list,
    leaf_count[0] is increased by one for each terminal position evaluated.

    Precondition: the tree below `state` is finite. The recursion depth is the
    height of the tree, so this suits game trees of height up to a few hundred.
    Cost: one call per node of the tree, so O(b^d) time for a uniform tree of
    branching factor b and depth d, and O(d) frames on the stack.
    """
    kids = children(state)
    if not kids:  # @line L1
        if leaf_count is not None:
            leaf_count[0] += 1
        return utility(state)  # @line L1
    if max_to_move:  # @line L2
        v: Value = -math.inf  # @line L3
        for c in kids:  # @line L4
            v = max(v, minimax(c, False, children, utility, leaf_count))  # @line L4
    else:  # @line L5
        v = math.inf  # @line L6
        for c in kids:  # @line L7
            v = min(v, minimax(c, True, children, utility, leaf_count))  # @line L7
    return v  # @line L8


def tree_children(node: Tree) -> Sequence[Tree]:
    """Children of a nested-list tree node; a leaf has none."""
    return node if isinstance(node, list) else []


def tree_utility(node: Tree) -> Value:
    """Value of a leaf of a nested-list tree."""
    return node  # type: ignore[return-value]


def minimax_tree(tree: Tree, max_to_move: bool = True, leaf_count: Optional[List[int]] = None) -> Value:
    """Minimax value of a nested-list tree whose root is a MAX node by default."""
    return minimax(tree, max_to_move, tree_children, tree_utility, leaf_count)
