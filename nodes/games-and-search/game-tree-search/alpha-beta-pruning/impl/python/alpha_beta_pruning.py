# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/alpha-beta-pruning/. The authors are listed in prov/AYQW86.jsonl.

"""Alpha-beta pruning in negamax form, in the fail-soft and the fail-hard (Knuth-Moore F2) versions."""

import math
from fractions import Fraction
from typing import Callable, List, Optional, Sequence, Tuple, TypeVar, Union

S = TypeVar("S")
Value = Union[int, float, Fraction]  # any totally ordered number type that negates exactly

INF = math.inf

# A game tree written as nested lists: a leaf is a number, an interior node is
# a non-empty list of children. Leaves hold values for the side to move there.
Tree = Union[int, Fraction, list]


def alpha_beta(
    state: S,
    children: Callable[[S], Sequence[S]],
    evaluate: Callable[[S], Value],
    alpha: Value = -INF,
    beta: Value = INF,
    fail_soft: bool = True,
    leaf_count: Optional[List[int]] = None,
) -> Value:
    """Search `state` with the window (alpha, beta) and return a value r.

    Let V be the negamax value of `state`, the value for the side to move.
    Both versions give: r <= alpha implies V <= alpha, alpha < r < beta implies
    r = V, and r >= beta implies V >= beta. The fail-soft version also gives
    V <= r when r <= alpha and V >= r when r >= beta.

    `children(state)` lists the positions after each move, in the order to
    search them; an empty list means a terminal position, and `evaluate`
    then gives its value for the side to move there. If `leaf_count` is a
    list, leaf_count[0] is increased by one for each call of `evaluate`.

    Precondition: alpha < beta, and the tree below `state` is finite.
    Cost: at most one call per node, so O(b^d) time in the worst case and
    O(b^ceil(d/2) + b^floor(d/2)) leaves with perfect move ordering; O(d) stack.
    """
    kids = children(state)
    if not kids:  # @line L1
        if leaf_count is not None:
            leaf_count[0] += 1
        return evaluate(state)
    m = -INF if fail_soft else alpha  # @line L2
    for c in kids:  # @line L3
        t = -alpha_beta(c, children, evaluate, -beta, -max(m, alpha), fail_soft, leaf_count)  # @line L4
        if t > m:  # @line L5
            m = t
        if m >= beta:  # @line L6
            return m
    return m  # @line L7


def tree_children(node: Tuple[Tree, tuple]) -> List[Tuple[Tree, tuple]]:
    """Children of a (subtree, path) pair; the path is the tuple of child indices."""
    sub, path = node
    if not isinstance(sub, list):
        return []
    return [(c, path + (i,)) for i, c in enumerate(sub)]


def alpha_beta_tree(
    tree: Tree,
    alpha: Value = -INF,
    beta: Value = INF,
    fail_soft: bool = True,
    visited: Optional[List[tuple]] = None,
) -> Value:
    """Alpha-beta on a nested-list tree with negamax leaves.

    If `visited` is a list, the path of each evaluated leaf is appended to it,
    in the order of evaluation.
    """

    def ev(node):
        if visited is not None:
            visited.append(node[1])
        return node[0]

    return alpha_beta((tree, ()), tree_children, ev, alpha, beta, fail_soft)


def minimax_leaves_to_negamax(tree: Tree, max_to_move: bool = True) -> Tree:
    """Turn leaves that hold values for MAX into values for the side to move."""
    if not isinstance(tree, list):
        return tree if max_to_move else -tree
    return [minimax_leaves_to_negamax(c, not max_to_move) for c in tree]
