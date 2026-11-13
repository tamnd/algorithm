# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/move-ordering/. The authors are listed in prov/4VF43D.jsonl.

"""Alpha-beta with a move-ordering score, and two standard scores."""

import math
from fractions import Fraction
from typing import Callable, Hashable, List, Optional, Sequence, Tuple, TypeVar, Union

S = TypeVar("S")
Value = Union[int, float, Fraction]
INF = math.inf

Moves = Callable[[S], Sequence[Tuple[Hashable, S]]]
Score = Callable[[S, Hashable, S], Value]


def ordered_alpha_beta(
    pos: S,
    depth: int,
    alpha: Value,
    beta: Value,
    moves: Moves,
    evaluate: Callable[[S], Value],
    score: Optional[Score] = None,
    count: Optional[List[int]] = None,
    leaves: Optional[List[int]] = None,
) -> Value:
    """Fail-soft negamax alpha-beta that searches the moves with the highest score first.

    `moves(pos)` lists (move, child) pairs; `evaluate(pos)` is the value for
    the side to move. `score(pos, move, child)` rates a move; ties keep the
    order of `moves`. With score=None the order of `moves` is used.
    `count[0]` counts the nodes and `leaves[0]` the evaluated positions.

    Precondition: alpha < beta. The result does not depend on the order.
    Cost: one call of score per move of each expanded node, plus a sort.
    """
    if count is not None:
        count[0] += 1
    kids = list(moves(pos))
    if depth == 0 or not kids:  # @line L1
        if leaves is not None:
            leaves[0] += 1
        return evaluate(pos)
    if score is not None:
        s = {i: score(pos, mv, c) for i, (mv, c) in enumerate(kids)}  # @line L2
        order = sorted(range(len(kids)), key=lambda i: -s[i])  # @line L3
        kids = [kids[i] for i in order]
    m = -INF  # @line L4
    for _, c in kids:  # @line L5
        t = -ordered_alpha_beta(c, depth - 1, -beta, -max(m, alpha), moves, evaluate, score, count, leaves)  # @line L6
        if t > m:  # @line L7
            m = t
        if m >= beta:  # @line L8
            return m
    return m  # @line L9


def static_score(evaluate: Callable[[S], Value]) -> Score:
    """Rate a move by the static value of the child, for the side that makes the move."""
    return lambda pos, mv, c: -evaluate(c)


def shallow_search_score(depth: int, moves: Moves, evaluate: Callable[[S], Value]) -> Score:
    """Rate a move by a plain negamax search of the child to the given depth.

    With a depth that reaches every leaf this is the perfect order.
    Cost: the size of the shallow tree of each child.
    """

    def negamax(p, d):
        kids = moves(p)
        if d == 0 or not kids:
            return evaluate(p)
        return max(-negamax(c, d - 1) for _, c in kids)

    return lambda pos, mv, c: -negamax(c, depth)
