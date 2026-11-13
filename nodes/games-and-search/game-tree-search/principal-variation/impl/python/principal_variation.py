# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/principal-variation/. The authors are listed in prov/Z9NCM4.jsonl.

"""Alpha-beta that returns its principal variation, and a helper to replay a line."""

import math
from fractions import Fraction
from typing import Callable, Hashable, List, Sequence, Tuple, TypeVar, Union

S = TypeVar("S")
Value = Union[int, float, Fraction]
INF = math.inf

Moves = Callable[[S], Sequence[Tuple[Hashable, S]]]


def pv_search(
    pos: S, depth: int, alpha: Value, beta: Value, moves: Moves, evaluate: Callable[[S], Value]
) -> Tuple[Value, List[Hashable]]:
    """Fail-soft negamax alpha-beta that also returns a line of moves.

    Returns (r, line). When alpha < r < beta, r is the depth-limited negamax
    value of pos and `line` is a principal variation: a legal line from pos to
    a terminal position or to the depth limit, along which both sides play a
    best move. Outside the window, `line` only shows the move that caused
    the bound. With the full window the result is always exact.

    Precondition: alpha < beta. Cost: that of alpha-beta, plus the copies
    of the lines, O(d) per new best move.
    """
    kids = moves(pos)
    if depth == 0 or not kids:
        return evaluate(pos), []
    m, line = -INF, []
    for mv, c in kids:
        t, sub = pv_search(c, depth - 1, -beta, -max(m, alpha), moves, evaluate)
        t = -t
        if t > m:
            m, line = t, [mv] + sub  # the best line so far: this move, then the line of the child
        if m >= beta:
            break
    return m, line


def follow(pos: S, line: Sequence[Hashable], moves: Moves) -> S:
    """Play the moves of `line` from pos and return the last position.

    Raises ValueError when a move is not legal where it is played.
    Cost: O(len(line)) calls of `moves`.
    """
    for mv in line:
        nxt = dict(moves(pos))
        if mv not in nxt:
            raise ValueError(f"illegal move {mv!r}")
        pos = nxt[mv]
    return pos
