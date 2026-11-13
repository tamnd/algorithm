# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/scout-search/. The authors are listed in prov/X5X0T8.jsonl.

"""Pearl's SCOUT in negamax form: test a move with a yes-or-no search before searching it for its value."""

from fractions import Fraction
from typing import Callable, Hashable, Sequence, Tuple, TypeVar, Union

S = TypeVar("S")
Value = Union[int, float, Fraction]

Moves = Callable[[S], Sequence[Tuple[Hashable, S]]]


def scout_test(
    pos: S,
    depth: int,
    v: Value,
    strict: bool,
    moves: Moves,
    evaluate: Callable[[S], Value],
) -> bool:
    """True iff N(pos) > v when strict, and iff N(pos) >= v when not strict.

    N is the depth-limited negamax value for the side to move. The search
    stops at the first move that proves the claim, so it returns a yes or a
    no and not a value. Cost: at most the size of the tree below pos.
    """
    kids = moves(pos)
    if depth == 0 or not kids:  # @line L7
        e = evaluate(pos)
        return e > v if strict else e >= v
    for _, c in kids:  # @line L8
        # N(pos) > v iff some child has -N(c) > v, that is N(c) < -v, that is not N(c) >= -v.
        if not scout_test(c, depth - 1, -v, not strict, moves, evaluate):  # @line L9
            return True
    return False  # @line L10


def scout(
    pos: S,
    depth: int,
    moves: Moves,
    evaluate: Callable[[S], Value],
) -> Value:
    """The depth-limited negamax value of pos.

    The first move is searched for its value. Each later move is first tested:
    only if the test shows that it is strictly better than the best value so
    far is it searched again for its value. Precondition: finite values.
    Cost: O(b^d) leaf visits in the worst case, with leaves visited more than
    once; on uniform trees with the best move first, the minimal tree of the
    Knuth-Moore theorem.
    """
    kids = moves(pos)
    if depth == 0 or not kids:  # @line L1
        return evaluate(pos)
    v = -scout(kids[0][1], depth - 1, moves, evaluate)  # @line L2
    for _, c in kids[1:]:  # @line L3
        # c is better iff -N(c) > v, that is iff not N(c) >= -v.
        if not scout_test(c, depth - 1, -v, False, moves, evaluate):  # @line L4
            v = -scout(c, depth - 1, moves, evaluate)  # @line L5
    return v  # @line L6
