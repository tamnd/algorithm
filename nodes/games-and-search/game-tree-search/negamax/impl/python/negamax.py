# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/negamax/. The authors are listed in prov/XN376A.jsonl.

"""The negamax value of a finite zero-sum game tree, from the point of view of the side to move."""

import math
from fractions import Fraction
from typing import Callable, List, Optional, Sequence, TypeVar, Union

S = TypeVar("S")
Value = Union[int, float, Fraction]  # any totally ordered number type that negates exactly

# A game tree written as nested lists: a leaf is a number, an interior node is
# a non-empty list of children. negamax_tree reads leaves as values for the
# side to move at that leaf; minimax_leaves_to_negamax converts MAX-view leaves.
Tree = Union[int, list]


def negamax(
    state: S,
    children: Callable[[S], Sequence[S]],
    evaluate: Callable[[S], Value],
    leaf_count: Optional[List[int]] = None,
) -> Value:
    """Return the value of `state` for the player to move at `state`.

    `children(state)` lists the positions after each legal move; an empty list
    means that `state` is terminal, and then `evaluate(state)` must return its
    value for the player who would move there. A win for that player is
    positive. If `leaf_count` is a list, leaf_count[0] is increased by one per
    terminal position.

    Precondition: the game is zero-sum, so the value for the other player is
    the negation, and the tree below `state` is finite.
    Cost: one call per node, so O(b^d) time on a uniform tree and O(d) stack.
    """
    kids = children(state)
    if not kids:  # @line L1
        if leaf_count is not None:
            leaf_count[0] += 1
        return evaluate(state)  # @line L1
    v: Value = -math.inf  # @line L2
    for c in kids:  # @line L3
        v = max(v, -negamax(c, children, evaluate, leaf_count))  # @line L3
    return v  # @line L4


def tree_children(node: Tree) -> Sequence[Tree]:
    """Children of a nested-list tree node; a leaf has none."""
    return node if isinstance(node, list) else []


def tree_evaluate(node: Tree) -> Value:
    """Value of a leaf of a nested-list tree, for the side to move at the leaf."""
    return node  # type: ignore[return-value]


def negamax_tree(tree: Tree, leaf_count: Optional[List[int]] = None) -> Value:
    """Negamax value of a nested-list tree whose leaves are side-to-move values."""
    return negamax(tree, tree_children, tree_evaluate, leaf_count)


def minimax_leaves_to_negamax(tree: Tree, max_to_move: bool = True) -> Tree:
    """Copy a tree whose leaves hold values for MAX into one whose leaves hold
    values for the side to move: a leaf where MIN would move is negated."""
    if not isinstance(tree, list):
        return tree if max_to_move else -tree
    return [minimax_leaves_to_negamax(c, not max_to_move) for c in tree]
