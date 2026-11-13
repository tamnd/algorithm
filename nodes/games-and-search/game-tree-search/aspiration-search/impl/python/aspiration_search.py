# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/aspiration-search/. The authors are listed in prov/K9327M.jsonl.

"""Aspiration search: alpha-beta at the root with a narrow window around a guess."""

import math
from fractions import Fraction
from typing import Callable, Hashable, List, Optional, Sequence, Tuple, TypeVar, Union

S = TypeVar("S")
Value = Union[int, float, Fraction]
INF = math.inf

Moves = Callable[[S], Sequence[Tuple[Hashable, S]]]


def alpha_beta(
    pos: S,
    depth: int,
    alpha: Value,
    beta: Value,
    moves: Moves,
    evaluate: Callable[[S], Value],
    count: Optional[List[int]] = None,
) -> Value:
    """Fail-soft negamax alpha-beta to the given depth.

    A result r <= alpha is an upper bound on the value, r >= beta is a lower
    bound, and alpha < r < beta is the value. Precondition: alpha < beta.
    """
    if count is not None:
        count[0] += 1
    kids = moves(pos)
    if depth == 0 or not kids:
        return evaluate(pos)
    m = -INF
    for _, c in kids:
        t = -alpha_beta(c, depth - 1, -beta, -max(m, alpha), moves, evaluate, count)
        if t > m:
            m = t
        if m >= beta:
            break
    return m


def aspiration(
    pos: S,
    depth: int,
    guess: Value,
    delta: Value,
    moves: Moves,
    evaluate: Callable[[S], Value],
    log: Optional[List[Tuple[Value, Value, Value]]] = None,
    count: Optional[List[int]] = None,
) -> Value:
    """The depth-limited negamax value of pos, by searches with windows around `guess`.

    The first window is (guess - delta, guess + delta). After a fail low or a
    fail high, the window moves to the side of the failure and its width
    doubles. `log` gets one (alpha, beta, result) triple per search.

    Precondition: delta > 0. Cost: one alpha-beta search per window; with a
    true value at distance D from the guess, at most about log2(D / delta) + 3
    searches.
    """
    lo, hi = -INF, INF  # @line L1  the value is always in [lo, hi]
    alpha, beta = guess - delta, guess + delta  # @line L2
    while True:  # @line L3
        v = alpha_beta(pos, depth, alpha, beta, moves, evaluate, count)  # @line L4
        if log is not None:
            log.append((alpha, beta, v))
        if alpha < v < beta:  # @line L5
            return v
        if v <= alpha:  # @line L6
            hi = v  # fail low: the value is at most v
        else:
            lo = v  # fail high: the value is at least v
        if lo == hi:  # @line L7
            return lo
        delta = 2 * delta  # @line L8
        if v <= alpha:  # @line L9  after a fail low, search below v
            alpha, beta = max(lo, v - delta), v
        else:  # @line L10  after a fail high, search above v
            alpha, beta = v, min(hi, v + delta)


def deepening_with_aspiration(
    pos: S,
    max_depth: int,
    delta: Value,
    moves: Moves,
    evaluate: Callable[[S], Value],
    count: Optional[List[int]] = None,
) -> List[Value]:
    """Iterative deepening: depth 1 with the full window, then each depth around the last value."""
    values = [alpha_beta(pos, 1, -INF, INF, moves, evaluate, count)]
    for d in range(2, max_depth + 1):
        values.append(aspiration(pos, d, values[-1], delta, moves, evaluate, count=count))
    return values
