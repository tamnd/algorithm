# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/null-move-pruning/. The authors are listed in prov/Q2C8WC.jsonl.

"""Null-move pruning in a fail-soft negamax alpha-beta search.

Before the moves of a node n are searched, the side to move passes (the null
move), and the opponent's best reply is searched to a depth reduced by R with
the null window (beta - 1, beta). If even after a pass the result is at least
beta, the node is cut off. This is a heuristic: it is wrong in zugzwang, where
passing would be the best move but is not legal.

A game object has `static(n)` (the score for the side to move), `moves(n)`
(the children) and `null(n)` (the position after a pass, with the other side
to move). Values are for the side to move.
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


def null_move_search(g, n, depth: int, alpha: int, beta: int, r: int = 2,
                     null_ok: bool = True, counter: Optional[List[int]] = None) -> int:
    """Alpha-beta with null-move pruning, reduction r, and no two null moves in a row.

    The null move is tried when depth >= r + 1 and the static score is at least
    beta. Precondition: r >= 1. Cost: at most the nodes of plain alpha-beta plus
    the nodes of the null-move searches, which have depth depth - 1 - r.
    """
    if counter is not None:
        counter[0] += 1
    kids = g.moves(n)
    if depth == 0 or not kids:
        return g.static(n)
    if null_ok and depth >= r + 1 and g.static(n) >= beta:
        t = -null_move_search(g, g.null(n), depth - 1 - r, -beta, -beta + 1, r, False, counter)
        if t >= beta:
            return t
    m = -INF
    for c in kids:
        t = -null_move_search(g, c, depth - 1, -beta, -max(m, alpha), r, True, counter)
        if t > m:
            m = t
        if m >= beta:
            return m
    return m


def verified_search(g, n, depth: int, alpha: int, beta: int, r: int = 3, verify: bool = True,
                    null_ok: bool = True, counter: Optional[List[int]] = None) -> int:
    """Verified null-move pruning, after David-Tabibi and Netanyahu (2002).

    In a subtree with verify true, a null-move fail high does not cut off the
    node. The node is searched with depth - 1 and verify false instead, and if
    that search does not fail high, a zugzwang is suspected and the node is
    searched again at the full depth.
    """
    if counter is not None:
        counter[0] += 1
    kids = g.moves(n)
    if depth == 0 or not kids:
        return g.static(n)
    fail_high = False
    if null_ok and depth >= r + 1 and g.static(n) >= beta:
        t = -verified_search(g, g.null(n), depth - 1 - r, -beta, -beta + 1, r, verify, False, counter)
        if t >= beta:
            if not verify:
                return t
            depth, verify, fail_high = depth - 1, False, True
    while True:
        m = -INF
        for c in kids:
            t = -verified_search(g, c, depth - 1, -beta, -max(m, alpha), r, verify, True, counter)
            if t > m:
                m = t
            if m >= beta:
                return m
        if fail_high and m < beta:
            depth, verify, fail_high = depth + 1, True, False
            continue
        return m


class RandomGame:
    """A lazy random game tree. A node is the tuple of move indices from the
    root, and -1 stands for a null move. Each node below `height` has `b`
    moves, and a move changes the score of the mover by a random integer in
    [-swing, swing]. A pass keeps the score and gives the move to the opponent.
    """

    def __init__(self, seed: int, b: int, height: int, swing: int = 4) -> None:
        self.seed, self.b, self.height, self.swing = seed, b, height, swing
        self._static: Dict[Node, int] = {(): 0}
        self._kids: Dict[Node, List[Node]] = {}

    def static(self, n: Node) -> int:
        if n not in self._static:
            p = n[:-1]
            if n[-1] == -1:
                self._static[n] = -self.static(p)
            else:
                self.moves(p)
        return self._static[n]

    def moves(self, n: Node) -> List[Node]:
        if n in self._kids:
            return self._kids[n]
        out: List[Node] = []
        if len(n) < self.height:
            rng = random.Random(f"{self.seed}/{n}")
            s = self.static(n)
            for i in range(self.b):
                c = n + (i,)
                self._static[c] = -(s + rng.randint(-self.swing, self.swing))
                out.append(c)
            out.sort(key=lambda c: (self._static[c], c))
        self._kids[n] = out
        return out

    def null(self, n: Node) -> Node:
        return n + (-1,)


class ExplicitGame:
    """A hand-made game: `kids` maps a node to its children, `static` gives the
    scores, and `nulls` maps a node to the position after a pass."""

    def __init__(self, kids: Dict[str, List[str]], static: Dict[str, int], nulls: Dict[str, str]) -> None:
        self.kids, self._static, self.nulls = kids, static, nulls

    def static(self, n: str) -> int:
        return self._static[n]

    def moves(self, n: str) -> List[str]:
        return self.kids.get(n, [])

    def null(self, n: str) -> str:
        return self.nulls[n]


def zugzwang_example() -> ExplicitGame:
    """White moves at R. Move "quiet" (searched first) is worth +1. Move "zug"
    puts Black in zugzwang: every Black move loses 5 points, but if Black could
    pass, the score would stay 0."""
    kids = {
        "R": ["quiet", "zug"],
        "quiet": ["q1"], "q1": ["q2"], "q2": ["q3"],
        "zug": ["z1", "z2"], "z1": ["z1a"], "z1a": ["z1b"], "z2": ["z2a"], "z2a": ["z2b"],
        "zug*": ["p1"], "p1": ["p2"],
    }
    static = {
        "R": 0, "quiet": -1, "q1": 1, "q2": -1, "q3": 1,
        "zug": 0, "z1": 5, "z1a": -5, "z1b": 5, "z2": 5, "z2a": -5, "z2b": 5,
        "zug*": 0, "p1": 0, "p2": 0,
    }
    return ExplicitGame(kids, static, {"zug": "zug*"})
