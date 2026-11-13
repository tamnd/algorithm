# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quiescence-search/. The authors are listed in prov/F29MJX.jsonl.

"""Quiescence search: at the frontier of a depth-limited alpha-beta search,
go on with captures only, and let the side to move "stand pat" on the static
evaluation instead of capturing. Values are negamax values, for the side to
move. The search returns fail-soft bounds of the quiescence value

    Q(n) = max(EVALUATE(n), max over captures c of -Q(c)).
"""

import random
from typing import Callable, Dict, List, Optional, Sequence, Tuple

INF = 10**9
Node = Tuple[int, ...]


def quiesce(
    n: Node,
    alpha: int,
    beta: int,
    evaluate: Callable[[Node], int],
    captures: Callable[[Node], Sequence[Node]],
    counter: Optional[List[int]] = None,
) -> int:
    """Return r with: r <= alpha if Q(n) <= alpha, r = Q(n) if alpha < Q(n) < beta,
    and r >= beta if Q(n) >= beta.

    `evaluate(n)` is the static score for the side to move at n, and
    `captures(n)` lists the positions after each capture, best capture first.
    Precondition: every chain of captures is finite (each capture removes a
    piece). Cost: one call per node of the capture tree that is not cut off.
    """
    if counter is not None:
        counter[0] += 1
    stand = evaluate(n)  # @line L1
    if stand >= beta:  # @line L2
        return stand
    m = stand  # @line L3
    alpha = max(alpha, stand)
    for c in captures(n):  # @line L4
        t = -quiesce(c, -beta, -alpha, evaluate, captures, counter)  # @line L5
        if t > m:  # @line L6
            m = t
        if m >= beta:  # @line L7
            return m
        alpha = max(alpha, m)  # @line L8
    return m  # @line L9


def search(
    n: Node,
    depth: int,
    alpha: int,
    beta: int,
    evaluate: Callable[[Node], int],
    moves: Callable[[Node], Sequence[Node]],
    captures: Callable[[Node], Sequence[Node]],
    use_quiescence: bool = True,
    counter: Optional[List[int]] = None,
) -> int:
    """Fail-soft alpha-beta to `depth` plies that calls QUIESCE at the frontier.

    With use_quiescence=False the frontier returns EVALUATE(n), which is the
    plain fixed-depth search that suffers from the horizon effect.
    A node with no moves is terminal and returns EVALUATE(n).
    """
    kids = moves(n)
    if not kids:  # @line L10
        if counter is not None:
            counter[0] += 1
        return evaluate(n)
    if depth == 0:  # @line L11
        if use_quiescence:
            return quiesce(n, alpha, beta, evaluate, captures, counter)
        if counter is not None:
            counter[0] += 1
        return evaluate(n)
    if counter is not None:
        counter[0] += 1
    m = -INF  # @line L12
    for c in kids:  # @line L13
        t = -search(c, depth - 1, -beta, -max(m, alpha), evaluate, moves, captures, use_quiescence, counter)
        if t > m:
            m = t
        if m >= beta:  # @line L14
            return m
    return m  # @line L15


def best_move(
    n: Node,
    depth: int,
    evaluate: Callable[[Node], int],
    moves: Callable[[Node], Sequence[Node]],
    captures: Callable[[Node], Sequence[Node]],
    use_quiescence: bool = True,
) -> Tuple[Node, int]:
    """The first child with the highest value at the root, and that value."""
    best, bv = None, -INF
    for c in moves(n):
        v = -search(c, depth - 1, -INF, -bv, evaluate, moves, captures, use_quiescence) if depth > 0 else -evaluate(c)
        if v > bv:
            best, bv = c, v
    return best, bv


class MaterialGame:
    """A random game tree with captures, generated lazily and reproducibly.

    A node is the tuple of move indices from the root. Each node has `b`
    moves until the depth `height`. A move is a capture with probability
    `capture_p`; a capture wins a piece worth one of `gains`, and a quiet move
    changes the score by at most `swing`. The static score is for the side to
    move, so a child scores -(score of the parent + gain of the move).
    """

    def __init__(self, seed: int, b: int, height: int, capture_p: float = 0.35,
                 swing: int = 1, gains: Sequence[int] = (1, 3, 3, 5, 9)) -> None:
        self.seed, self.b, self.height = seed, b, height
        self.capture_p, self.swing, self.gains = capture_p, swing, tuple(gains)
        self._static: Dict[Node, int] = {(): 0}
        self._kids: Dict[Node, List[Tuple[Node, bool]]] = {}

    def _expand(self, n: Node) -> List[Tuple[Node, bool]]:
        if n in self._kids:
            return self._kids[n]
        out: List[Tuple[Node, bool]] = []
        if len(n) < self.height:
            rng = random.Random(f"{self.seed}/{n}")
            s = self._static[n]
            for i in range(self.b):
                cap = rng.random() < self.capture_p
                gain = rng.choice(self.gains) if cap else rng.randint(-self.swing, self.swing)
                c = n + (i,)
                self._static[c] = -(s + gain)
                out.append((c, cap))
            out.sort(key=lambda e: (self._static[e[0]], e[0]))  # best move for the mover first
        self._kids[n] = out
        return out

    def evaluate(self, n: Node) -> int:
        if n not in self._static:
            self._expand(n[:-1])
        return self._static[n]

    def moves(self, n: Node) -> List[Node]:
        return [c for c, _ in self._expand(n)]

    def captures(self, n: Node) -> List[Node]:
        return [c for c, cap in self._expand(n) if cap]
