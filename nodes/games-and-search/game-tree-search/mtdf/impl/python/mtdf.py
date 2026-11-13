# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mtdf/. The authors are listed in prov/C2MWH2.jsonl.

"""MTD(f): the value of a game tree from null-window alpha-beta searches with memory."""

import math
from fractions import Fraction
from typing import Callable, Dict, Hashable, List, Optional, Sequence, Tuple, TypeVar, Union

S = TypeVar("S")
Value = Union[int, float, Fraction]
INF = math.inf

Moves = Callable[[S], Sequence[Tuple[Hashable, S]]]
Table = Dict[Tuple[Hashable, int], List[Value]]  # (key, depth) -> [lower bound, upper bound]


def alpha_beta_with_memory(
    pos: S,
    depth: int,
    alpha: Value,
    beta: Value,
    moves: Moves,
    evaluate: Callable[[S], Value],
    key: Callable[[S], Hashable],
    table: Table,
    count: Optional[List[int]] = None,
) -> Value:
    """Fail-soft negamax alpha-beta that keeps a lower and an upper bound per position.

    The table maps (key(pos), depth) to [lo, hi] with lo <= N(pos) <= hi. The
    result r obeys the fail-soft bounds: r <= alpha means N <= r, r >= beta
    means N >= r, otherwise r = N. The table may be shared between calls on
    the same tree. Precondition: alpha < beta. Cost: at most one visit per
    node and call, often much less when the table has bounds.
    """
    if count is not None:
        count[0] += 1
    k = (key(pos), depth)
    entry = table.get(k)
    if entry is not None:  # @line L8
        lo, hi = entry
        if lo >= beta or lo == hi:  # @line L9
            return lo
        if hi <= alpha:
            return hi
        alpha, beta = max(alpha, lo), min(beta, hi)  # @line L10
    kids = moves(pos)
    if depth == 0 or not kids:  # @line L11
        g = evaluate(pos)
        table[k] = [g, g]  # a terminal value is exact whatever the window
        return g
    else:
        g, a = -INF, alpha  # @line L12
        for _, c in kids:  # @line L13
            if g >= beta:
                break
            g = max(g, -alpha_beta_with_memory(c, depth - 1, -beta, -a, moves, evaluate, key, table, count))
            a = max(a, g)
    lo, hi = entry if entry is not None else (-INF, INF)
    if g <= alpha:  # @line L14  store against the narrowed window
        hi = g
    elif g < beta:
        lo = hi = g
    else:
        lo = g
    table[k] = [lo, hi]
    return g  # @line L15


def mtdf(
    pos: S,
    depth: int,
    guess: Value,
    moves: Moves,
    evaluate: Callable[[S], Value],
    key: Callable[[S], Hashable],
    grain: Value = 1,
    table: Optional[Table] = None,
    log: Optional[List[Tuple[Value, Value]]] = None,
    count: Optional[List[int]] = None,
) -> Value:
    """The depth-limited negamax value of pos, by null-window searches from `guess`.

    Each pass searches the window (beta - grain, beta) and moves the lower or
    the upper bound of the value to its result. `log` gets one (beta, result)
    pair per pass. With every value a multiple of `grain`, each pass moves a
    bound by at least one grain; with a coarser grain it is still correct.
    A pass that gets an exact value ends the loop.

    Precondition: grain > 0, a finite tree and a finite guess; for MTD(+inf),
    pass a guess above every value, since the window (inf - grain, inf) is
    empty and the loop would not end. Cost: one null-window search
    per pass; two passes when the guess is the value.
    """
    if table is None:
        table = {}
    g, lower, upper = guess, -INF, INF  # @line L1
    while lower < upper:  # @line L2
        beta = max(g, lower + grain)  # @line L3
        g = alpha_beta_with_memory(pos, depth, beta - grain, beta, moves, evaluate, key, table, count)  # @line L4
        if log is not None:
            log.append((beta, g))
        if g < beta:  # @line L5  fail low: the value is at most g
            upper = g
        if g > beta - grain:  # @line L6  fail high, or exact: the value is at least g
            lower = g
    return g  # @line L7
