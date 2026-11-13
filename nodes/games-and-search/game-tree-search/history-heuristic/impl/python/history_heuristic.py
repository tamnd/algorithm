# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/history-heuristic/. The authors are listed in prov/XSFAN1.jsonl.

"""Alpha-beta with the history heuristic: one score per move over the whole search."""

import math
from fractions import Fraction
from typing import Callable, Dict, Hashable, List, Optional, Sequence, Tuple, TypeVar, Union

S = TypeVar("S")
Value = Union[int, float, Fraction]
INF = math.inf


class HistoryTable:
    """A score for each move. `bonus(depth)` is the amount added when the move is best at a node.

    Schaeffer used 2^depth; depth * depth is also common.
    Cost: O(1) per lookup and per update; one entry per distinct move.
    """

    def __init__(self, bonus: Callable[[int], int] = lambda d: 1 << d):
        self.bonus = bonus
        self.score: Dict[Hashable, int] = {}

    def order(self, kids: Sequence[Tuple[Hashable, S]]) -> List[Tuple[Hashable, S]]:
        """Highest score first; moves with equal scores keep the given order."""
        return sorted(kids, key=lambda mc: -self.score.get(mc[0], 0))

    def reward(self, move: Hashable, depth: int) -> None:
        self.score[move] = self.score.get(move, 0) + self.bonus(depth)

    def age(self) -> None:
        """Halve every score, between two searches, so old results fade."""
        for k in self.score:
            self.score[k] //= 2


def history_alpha_beta(
    pos: S,
    depth: int,
    alpha: Value,
    beta: Value,
    moves: Callable[[S], Sequence[Tuple[Hashable, S]]],
    evaluate: Callable[[S], Value],
    history: Optional[HistoryTable],
    count: Optional[List[int]] = None,
) -> Value:
    """Fail-soft negamax alpha-beta that sorts the moves by their history score.

    `moves(pos)` lists (move, child) pairs in the base order; `evaluate(pos)`
    is the value for the side to move. At each inner node whose result is
    above alpha, the best move (the cutoff move, or the move of the exact
    value) gets the bonus of the remaining depth. A node that fails low
    gives no bonus, since none of its moves is known to be good.
    With history=None this is plain alpha-beta.

    Precondition: alpha < beta. The result does not depend on the table.
    Cost: a sort of the moves at each inner node, O(k log k) for k moves.
    """
    if count is not None:
        count[0] += 1
    kids = list(moves(pos))
    if depth == 0 or not kids:  # @line L1
        return evaluate(pos)
    if history is not None:
        kids = history.order(kids)  # @line L2
    m, best = -INF, None  # @line L3
    for mv, c in kids:  # @line L4
        t = -history_alpha_beta(c, depth - 1, -beta, -max(m, alpha), moves, evaluate, history, count)  # @line L5
        if t > m:  # @line L6
            m, best = t, mv
        if m >= beta:  # @line L7
            break
    if history is not None and m > alpha:  # @line L8  a cutoff or a new best value, not a fail low
        history.reward(best, depth)  # @line L9
    return m  # @line L10
