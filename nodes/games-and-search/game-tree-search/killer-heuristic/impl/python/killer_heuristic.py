# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/killer-heuristic/. The authors are listed in prov/V7ZSNV.jsonl.

"""Alpha-beta with killer moves: per ply, the last moves that caused a cutoff are tried first."""

import math
from fractions import Fraction
from typing import Callable, Dict, Hashable, List, Optional, Sequence, Tuple, TypeVar, Union

S = TypeVar("S")
Value = Union[int, float, Fraction]
INF = math.inf


class KillerTable:
    """For each ply, up to `slots` moves, the most recent cutoff move first.

    Cost: O(slots) per order and per record; O(slots) space per ply.
    """

    def __init__(self, slots: int = 2):
        self.slots = slots
        self.table: Dict[int, List[Hashable]] = {}

    def killers(self, ply: int) -> List[Hashable]:
        return self.table.get(ply, [])

    def order(self, ply: int, kids: Sequence[Tuple[Hashable, S]]) -> List[Tuple[Hashable, S]]:
        """The killers of this ply that are legal here first, in slot order; then the rest in the given order."""
        ks = self.killers(ply)
        rank = {k: i for i, k in enumerate(ks)}
        first = sorted((mc for mc in kids if mc[0] in rank), key=lambda mc: rank[mc[0]])
        return first + [mc for mc in kids if mc[0] not in rank]

    def record(self, ply: int, move: Hashable) -> None:
        ks = self.table.setdefault(ply, [])
        if ks and ks[0] == move:
            return
        if move in ks:
            ks.remove(move)
        ks.insert(0, move)
        del ks[self.slots :]


def killer_alpha_beta(
    pos: S,
    depth: int,
    alpha: Value,
    beta: Value,
    moves: Callable[[S], Sequence[Tuple[Hashable, S]]],
    evaluate: Callable[[S], Value],
    killers: Optional[KillerTable],
    is_quiet: Callable[[S, Hashable], bool] = lambda pos, mv: True,
    ply: int = 0,
    count: Optional[List[int]] = None,
) -> Value:
    """Fail-soft negamax alpha-beta that tries the killer moves of each ply first.

    `moves(pos)` lists (move, child) pairs in the base order; `evaluate(pos)`
    is the value for the side to move. Only quiet moves become killers.
    With killers=None this is plain alpha-beta in the base order.

    Precondition: alpha < beta. The result does not depend on the killers.
    Cost: O(slots) extra work per node.
    """
    if count is not None:
        count[0] += 1
    kids = list(moves(pos))
    if depth == 0 or not kids:  # @line L1
        return evaluate(pos)
    if killers is not None:
        kids = killers.order(ply, kids)  # @line L2
    m = -INF  # @line L3
    for mv, c in kids:  # @line L4
        t = -killer_alpha_beta(c, depth - 1, -beta, -max(m, alpha), moves, evaluate, killers, is_quiet, ply + 1, count)  # @line L5
        if t > m:  # @line L6
            m = t
        if m >= beta:  # @line L7
            if killers is not None and is_quiet(pos, mv):
                killers.record(ply, mv)  # @line L8
            return m  # @line L9
    return m  # @line L10
