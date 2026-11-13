# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/late-move-reductions/. The authors are listed in prov/EJ7NFT.jsonl.

"""Late move reductions (LMR) in a fail-soft negamax alpha-beta search.

The moves of a node are searched in order. The first `full` moves, and every
capture, get the full depth. A later quiet move is first searched to the
reduced depth d - 1 - r with the null window (a, a + 1), where a is the best
value so far or alpha. If that search fails low, the move is taken as no
better than a. If it fails high, the move is searched again at the full depth
with the full window. This is a heuristic: a move that looks bad at the
reduced depth but is good at the full depth is missed.

A game object has `static(n)`, `moves(n)` (ordered, best first) and
`is_capture(n)`. Values are for the side to move.
"""

import random
from typing import Dict, List, Optional, Tuple

INF = 10**9
Node = Tuple[int, ...]


def alphabeta(g, n, depth: int, alpha: int, beta: int, counter: Optional[List[int]] = None) -> int:
    """Plain fail-soft alpha-beta to `depth` plies, the reference search."""
    if counter is not None:
        counter[0] += 1
    kids = g.moves(n)
    if depth == 0 or not kids:
        return g.static(n)
    m = -INF
    for c in kids:
        t = -alphabeta(g, c, depth - 1, -beta, -max(m, alpha), counter)
        if t > m:
            m = t
        if m >= beta:
            return m
    return m


def lmr_search(g, n, depth: int, alpha: int, beta: int, full: int = 1, r: int = 1,
               counter: Optional[List[int]] = None) -> int:
    """Alpha-beta with late move reductions.

    Precondition: full >= 1 and r >= 1. A move is reduced only when its index
    is at least `full`, it is quiet, and depth - 1 - r >= 0. Cost: at most the
    nodes of the reduced searches plus the re-searches and the full searches.
    """
    if counter is not None:
        counter[0] += 1
    kids = g.moves(n)
    if depth == 0 or not kids:
        return g.static(n)
    m = -INF
    for i, c in enumerate(kids):
        a = max(m, alpha)
        if i >= full and depth - 1 - r >= 0 and not g.is_capture(c) and a > -INF:
            t = -lmr_search(g, c, depth - 1 - r, -a - 1, -a, full, r, counter)
            if t > a:  # the reduced search fails high: search again in full
                t = -lmr_search(g, c, depth - 1, -beta, -a, full, r, counter)
        else:
            t = -lmr_search(g, c, depth - 1, -beta, -a, full, r, counter)
        if t > m:
            m = t
        if m >= beta:
            return m
    return m


class MaterialGame:
    """A lazy random game tree with captures. A node is the tuple of move indices
    from the root. A capture wins one of `gains`, a quiet move changes the score
    of the mover by an integer in [-swing, swing], and the static score is for
    the side to move. Moves are ordered by their static score, best for the
    mover first, which is the order an LMR program relies on.
    """

    def __init__(self, seed: int, b: int, height: int, capture_p: float = 0.3,
                 swing: int = 2, gains: Tuple[int, ...] = (1, 3, 3, 5, 9)) -> None:
        self.seed, self.b, self.height = seed, b, height
        self.capture_p, self.swing, self.gains = capture_p, swing, gains
        self._static: Dict[Node, int] = {(): 0}
        self._cap: Dict[Node, bool] = {(): False}
        self._kids: Dict[Node, List[Node]] = {}

    def moves(self, n: Node) -> List[Node]:
        if n in self._kids:
            return self._kids[n]
        out: List[Node] = []
        if len(n) < self.height:
            rng = random.Random(f"{self.seed}/{n}")
            s = self._static[n]
            for i in range(self.b):
                cap = rng.random() < self.capture_p
                gain = rng.choice(self.gains) if cap else rng.randint(-self.swing, self.swing)
                c = n + (i,)
                self._static[c] = -(s + gain)
                self._cap[c] = cap
                out.append(c)
            out.sort(key=lambda c: (self._static[c], c))
        self._kids[n] = out
        return out

    def static(self, n: Node) -> int:
        if n not in self._static:
            self.moves(n[:-1])
        return self._static[n]

    def is_capture(self, n: Node) -> bool:
        if n not in self._cap:
            self.moves(n[:-1])
        return self._cap[n]


class ExplicitGame:
    """A hand-made game with `kids`, `static` and the set of capture nodes."""

    def __init__(self, kids: Dict[str, List[str]], static: Dict[str, int], captures: set) -> None:
        self.kids, self._static, self.captures = kids, static, captures

    def moves(self, n: str) -> List[str]:
        return self.kids.get(n, [])

    def static(self, n: str) -> int:
        return self._static[n]

    def is_capture(self, n: str) -> bool:
        return n in self.captures


def late_threat_example() -> ExplicitGame:
    """White moves at R with two plies left. The first move "m0" wins 1 point.
    The late quiet move "m1" keeps the score at 0 but makes a threat that Black
    cannot meet: each Black reply leaves White 4 points up."""
    kids = {"R": ["m0", "m1"], "m0": ["m0a"], "m1": ["m1a", "m1b"]}
    static = {"R": 0, "m0": -1, "m0a": 1, "m1": 0, "m1a": 4, "m1b": 4}
    return ExplicitGame(kids, static, set())
