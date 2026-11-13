# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/futility-pruning/. The authors are listed in prov/9FWPSR.jsonl.

"""Futility pruning in a fail-soft negamax alpha-beta search.

Near the leaves, a quiet move cannot change the score by much. If the static
score of the node plus a margin cannot reach alpha, the quiet moves are
skipped, and the node keeps the bound static + margin in their place.
Captures are always searched. `margins[d]` is the margin at remaining depth d;
depths without a margin are not pruned.

With margins[1] >= D and margins[2] >= 2 D, where every quiet move changes the
score of the mover by at most D and no move lowers it by more than D, the
pruned search returns the same value as plain alpha-beta. With smaller
margins it is a heuristic and can return another value.
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


def futility_search(g, n, depth: int, alpha: int, beta: int, margins: Dict[int, int],
                    counter: Optional[List[int]] = None) -> int:
    """Alpha-beta in which, at a remaining depth d with a margin, a quiet move
    is skipped when static(n) + margins[d] <= the current alpha.

    Returns a fail-soft value: a skipped move counts as the upper bound
    static(n) + margins[d]. Cost: at most the nodes of plain alpha-beta with
    the same move order, since it only skips subtrees.
    """
    if counter is not None:
        counter[0] += 1
    kids = g.moves(n)
    if depth == 0 or not kids:
        return g.static(n)
    s = g.static(n)
    margin = margins.get(depth)
    m = -INF
    for c in kids:
        a = max(m, alpha)
        if margin is not None and not g.is_capture(c) and s + margin <= a:
            m = max(m, s + margin)  # the bound for the skipped move
            continue
        t = -futility_search(g, c, depth - 1, -beta, -a, margins, counter)
        if t > m:
            m = t
        if m >= beta:
            return m
    return m


class MaterialGame:
    """A lazy random game tree with captures. A node is the tuple of move indices
    from the root. A capture wins one of `gains`, a quiet move changes the score
    of the mover by an integer in [-swing, swing], and the static score is for
    the side to move. Captures come first in the move order, larger gains first.
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
            out.sort(key=lambda c: (not self._cap[c], self._static[c], c))
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


def small_margin_example() -> ExplicitGame:
    """White moves at the frontier node R, with static score 0. The capture
    "cap" wins 3 points and is searched first. The quiet move "q" raises the
    score by 5, more than a margin of 1 allows, so a margin of 1 skips it."""
    kids = {"R": ["cap", "q"]}
    static = {"R": 0, "cap": -3, "q": -5}
    return ExplicitGame(kids, static, {"cap"})
