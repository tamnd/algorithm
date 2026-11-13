# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/search-extensions/. The authors are listed in prov/42DKME.jsonl.

"""Search extensions in a fail-soft negamax alpha-beta search.

A move into a *forcing* position, one in which the opponent has exactly one
legal reply (as after most checks), does not use up a ply of depth, as long as
the line has extension budget left. This is the one-reply extension, and the
same template gives check and recapture extensions with another test.

A game is `kids[n]` (a list of children) and `static[n]` (the score for the
side to move at n). A node with no children is terminal.
"""

import random
from typing import Callable, Dict, List, Optional, Tuple

INF = 10**9
Kids = Dict[str, List[str]]
Static = Dict[str, int]


def one_reply(kids: Kids) -> Callable[[str, str], int]:
    """EXTENSION(n, c) = 1 when the position c has exactly one legal move."""
    return lambda n, c: 1 if len(kids.get(c, [])) == 1 else 0


def search(
    kids: Kids,
    static: Static,
    n: str,
    depth: int,
    alpha: int,
    beta: int,
    extension: Callable[[str, str], int],
    budget: int,
    counter: Optional[List[int]] = None,
) -> int:
    """Fail-soft alpha-beta to `depth` plies, where the move to c is searched with
    depth - 1 + e, e = min(EXTENSION(n, c), budget left on this path).

    Precondition: depth >= 0 and budget >= 0. The total extension on a path is
    at most `budget`, so a path has at most depth + budget moves and the search
    stops even in games with long forcing chains. Cost: O(b^(depth + budget)).
    """
    if counter is not None:
        counter[0] += 1
    ch = kids.get(n, [])
    if not ch or depth == 0:
        return static[n]
    m = -INF
    for c in ch:
        e = min(extension(n, c), budget)
        t = -search(kids, static, c, depth - 1 + e, -beta, -max(m, alpha), extension, budget - e, counter)
        if t > m:
            m = t
        if m >= beta:
            return m
    return m


def plain(kids: Kids, static: Static, n: str, depth: int) -> int:
    """Reference: negamax to a fixed depth, with no pruning and no extensions."""
    ch = kids.get(n, [])
    if not ch or depth == 0:
        return static[n]
    return max(-plain(kids, static, c, depth - 1) for c in ch)


def exact(kids: Kids, static: Static, n: str) -> int:
    """Reference: negamax value of the whole tree."""
    ch = kids.get(n, [])
    if not ch:
        return static[n]
    return max(-exact(kids, static, c) for c in ch)


def forced_tail_tree(rng: random.Random, b: int, d: int, k: int, swing: int = 9) -> Tuple[Kids, Static]:
    """A uniform tree of depth d with branching factor b, in which every node at
    depth d starts a forced line of k more moves, each with one reply. The
    static scores change by up to `swing` at each move, so the end of a forced
    line can be far from its start."""
    kids: Kids = {}
    static: Static = {"r": 0}
    frontier = ["r"]
    for level in range(d + k):
        width = b if level < d else 1
        nxt = []
        for n in frontier:
            row = []
            for i in range(width):
                c = f"{n}.{i}"
                static[c] = -(static[n] + rng.randint(-swing, swing))
                row.append(c)
            kids[n] = row
            nxt.extend(row)
        frontier = nxt
    return kids, static


def mixed_tree(rng: random.Random, height: int, p_forced: float = 0.3, b: int = 3) -> Tuple[Kids, Static]:
    """A random tree of the given height in which each inner node has one move
    with probability p_forced and b moves otherwise."""
    kids: Kids = {}
    static: Static = {"r": 0}
    frontier = ["r"]
    for _ in range(height):
        nxt = []
        for n in frontier:
            width = 1 if rng.random() < p_forced else b
            row = []
            for i in range(width):
                c = f"{n}.{i}"
                static[c] = -(static[n] + rng.randint(-5, 5))
                row.append(c)
            kids[n] = row
            nxt.extend(row)
        frontier = nxt
    return kids, static


def free_forced_value(kids: Kids, static: Static, n: str, depth: int, budget: int) -> int:
    """Reference for the one-reply extension: plain negamax in which a move into
    a position with one reply costs no depth while the budget lasts."""
    ch = kids.get(n, [])
    if not ch or depth == 0:
        return static[n]
    out = -INF
    for c in ch:
        e = 1 if (len(kids.get(c, [])) == 1 and budget > 0) else 0
        out = max(out, -free_forced_value(kids, static, c, depth - 1 + e, budget - e))
    return out
