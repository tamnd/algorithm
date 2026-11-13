# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/principal-variation-search/. The authors are listed in prov/HEBCKY.jsonl.

"""Principal variation search (NegaScout): a full window for the first move, null windows for the rest."""

import math
from fractions import Fraction
from typing import Callable, Hashable, List, Optional, Sequence, Tuple, TypeVar, Union

S = TypeVar("S")
Value = Union[int, float, Fraction]
INF = math.inf

Moves = Callable[[S], Sequence[Tuple[Hashable, S]]]


def pvs(
    pos: S,
    depth: int,
    alpha: Value,
    beta: Value,
    moves: Moves,
    evaluate: Callable[[S], Value],
    grain: Value = 1,
    stats: Optional[List[int]] = None,
) -> Value:
    """Fail-soft principal variation search to the given depth, in negamax form.

    The result r satisfies the same bounds as fail-soft alpha-beta: r <= alpha
    means the value is at most r, r >= beta means it is at least r, and
    otherwise r is the value. `grain` is the width of the null window. It is
    correct for any grain > 0; it prunes as much as alpha-beta when every value
    is a multiple of grain. `stats`, if given, counts [null-window searches,
    re-searches].

    Precondition: alpha < beta. Cost: the minimal tree with the best move
    first; with bad order, re-searches can make it slower than alpha-beta.
    """
    kids = moves(pos)
    if depth == 0 or not kids:  # @line L1
        return evaluate(pos)
    m = -pvs(kids[0][1], depth - 1, -beta, -alpha, moves, evaluate, grain, stats)  # @line L2
    if m >= beta:  # @line L3
        return m
    for _, c in kids[1:]:  # @line L4
        a = max(alpha, m)  # @line L5
        t = -pvs(c, depth - 1, -a - grain, -a, moves, evaluate, grain, stats)  # @line L6  null window (a, a + grain)
        if stats is not None:
            stats[0] += 1
        if a < t < beta and depth > 1 and moves(c):  # @line L7  c is better: find its value
            if stats is not None:
                stats[1] += 1
            t = -pvs(c, depth - 1, -beta, -t, moves, evaluate, grain, stats)  # @line L8
        if t > m:  # @line L9
            m = t
        if m >= beta:  # @line L10
            return m
    return m  # @line L11
