# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/best-move-selection/. The authors are listed in prov/Y4MTQZ.jsonl.

"""Choose a move, not only a value, at the root of a game tree.

Values are negamax values: from the point of view of the side to move. A
position is any object; `moves(p)` returns the positions after each legal
move, in the order the program wants to try them, and `evaluate(p)` scores a
position for the side to move. It is used at terminal positions and at the
depth limit. The returned move is an index into moves(root).
"""

import math
from typing import Callable, List, Optional, Sequence, Tuple

Moves = Callable[[object], Sequence[object]]
Evaluate = Callable[[object], float]


class BudgetExceeded(Exception):
    """Raised inside a search when it has used up its node budget."""


class Counter:
    """Counts nodes and stops the search when `budget` nodes have been visited."""

    def __init__(self, budget: Optional[int] = None):
        self.nodes = 0
        self.budget = budget

    def tick(self) -> None:
        self.nodes += 1
        if self.budget is not None and self.nodes > self.budget:
            raise BudgetExceeded


def negamax(p, depth: int, moves: Moves, evaluate: Evaluate, counter: Counter) -> float:
    """Full-width depth-limited negamax value of p for the side to move."""
    counter.tick()
    kids = moves(p)
    if depth == 0 or not kids:
        return evaluate(p)
    return max(-negamax(c, depth - 1, moves, evaluate, counter) for c in kids)


def alphabeta(p, depth: int, alpha: float, beta: float, moves: Moves, evaluate: Evaluate, counter: Counter) -> float:
    """Fail-soft alpha-beta in negamax form. If the result v satisfies
    alpha < v < beta it is exact; v <= alpha means the true value is at most v;
    v >= beta means it is at least v."""
    counter.tick()
    kids = moves(p)
    if depth == 0 or not kids:
        return evaluate(p)
    best = -math.inf
    for c in kids:
        v = -alphabeta(c, depth - 1, -beta, -max(alpha, best), moves, evaluate, counter)
        if v > best:
            best = v
            if best >= beta:
                break
    return best


def best_move(
    root,
    depth: int,
    moves: Moves,
    evaluate: Evaluate,
    first: Optional[int] = None,
    use_alphabeta: bool = True,
    counter: Optional[Counter] = None,
) -> Tuple[Optional[int], float]:
    """Return (index of a best move in moves(root), value of root), searching
    `depth` plies. The move at index `first` is tried first, as iterative
    deepening does with the best move of the last iteration. Ties go to the
    move tried first. With alpha-beta, a move whose search fails low returns
    only an upper bound, which is never more than the best value so far, so
    such a move is never chosen. Precondition: depth >= 1 and root has a move."""
    counter = counter or Counter()
    counter.tick()
    kids = list(moves(root))
    order = list(range(len(kids)))
    if first is not None:
        order.remove(first)
        order.insert(0, first)
    best: Optional[int] = None
    alpha = -math.inf
    for i in order:
        if use_alphabeta:
            v = -alphabeta(kids[i], depth - 1, -math.inf, -alpha, moves, evaluate, counter)
        else:
            v = -negamax(kids[i], depth - 1, moves, evaluate, counter)
        if v > alpha:  # strict: ties keep the move tried first
            alpha, best = v, i
    return best, alpha


def iterative_deepening(root, max_depth: int, moves: Moves, evaluate: Evaluate, node_budget: Optional[int] = None) -> Tuple[Optional[int], float, int]:
    """Search depths 1, 2, ... up to max_depth, each with the last best move
    first, and stop when the node budget runs out. Return the move and value of
    the last iteration that finished, and its depth. A partial iteration is
    thrown away. If not even depth 1 finishes, return (None, evaluate(root), 0)."""
    counter = Counter(node_budget)
    result: Tuple[Optional[int], float, int] = (None, evaluate(root), 0)
    first: Optional[int] = None
    for depth in range(1, max_depth + 1):
        try:
            move, value = best_move(root, depth, moves, evaluate, first, True, counter)
        except BudgetExceeded:
            break
        result = (move, value, depth)
        first = move
    return result
