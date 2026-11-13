# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/solved-game/. The authors are listed in prov/97PW5C.jsonl.

"""Solving a small finite game: the value of every reachable position (a strong
solution), a strategy that keeps the value (a weak solution), a check that the
strategy never does worse than the value, and counts of the game tree.

A game is given by three functions on hashable positions:
  moves(p)        the positions after each legal move; empty when p is over,
  outcome(p)      the result for MAX at a position that is over,
  max_to_move(p)  True when MAX moves at p.
The game must be acyclic: no position can follow itself. Every search below
uses an explicit stack, so long games do not hit the recursion limit.
"""

from collections import Counter
from typing import Callable, Dict, Hashable, Iterable, List, Sequence, Tuple

P = Hashable
Moves = Callable[[P], Sequence[P]]


def reachable(start: P, moves: Moves) -> set:
    """All positions that can be reached from `start`, by depth-first search."""
    seen = {start}
    stack = [start]
    while stack:
        p = stack.pop()
        for c in moves(p):
            if c not in seen:
                seen.add(c)
                stack.append(c)
    return seen


def solve_all(start: P, moves: Moves, outcome: Callable[[P], int], max_to_move: Callable[[P], bool]) -> Dict[P, int]:
    """Strong solution: the minimax value for MAX of every position reachable
    from `start`. Each position is solved once, after all its children, so the
    cost is O(V + E) calls of `moves` for V positions and E moves."""
    value: Dict[P, int] = {}
    open_: set = set()  # positions whose children are being solved
    stack: List[Tuple[P, bool]] = [(start, False)]
    while stack:
        p, children_done = stack.pop()
        if p in value:
            continue
        kids = moves(p)
        if not kids:
            value[p] = outcome(p)
        elif not children_done:
            if p in open_:
                raise ValueError("the game has a cycle")
            open_.add(p)
            stack.append((p, True))
            stack.extend((c, False) for c in kids if c not in value)
        else:
            open_.discard(p)
            vals = [value[c] for c in kids]
            value[p] = max(vals) if max_to_move(p) else min(vals)
    return value


def value_keeping_strategy(value: Dict[P, int], moves: Moves) -> Dict[P, P]:
    """For each position that is not over, the first move whose result has the
    value of the position. Following it gives a weak solution for both players."""
    strat = {}
    for p, v in value.items():
        for c in moves(p):
            if value[c] == v:
                strat[p] = c
                break
    return strat


def guaranteed(start: P, moves: Moves, outcome: Callable[[P], int], max_to_move: Callable[[P], bool], strat: Dict[P, P], for_max: bool) -> int:
    """The worst result for the player (MAX if `for_max`) who follows `strat`,
    over every possible sequence of replies of the other player. The result is
    for MAX. A weak solution is checked by comparing this with the value."""
    best_for_opponent = min if for_max else max
    res: Dict[P, int] = {}
    stack: List[Tuple[P, bool]] = [(start, False)]
    while stack:
        p, done = stack.pop()
        if p in res:
            continue
        kids = moves(p)
        if not kids:
            res[p] = outcome(p)
            continue
        mine = max_to_move(p) == for_max
        follow = [strat[p]] if mine else list(kids)
        if not done:
            stack.append((p, True))
            stack.extend((c, False) for c in follow if c not in res)
        else:
            vals = [res[c] for c in follow]
            res[p] = vals[0] if mine else best_for_opponent(vals)
    return res[start]


def tree_statistics(start: P, moves: Moves, outcome: Callable[[P], int]) -> dict:
    """Counts of the game tree (one node per history), without walking it: a
    layer maps each position to the number of histories of that length that
    reach it. Returns the nodes per depth, the leaves, inner nodes and edges,
    the leaves by outcome, and the total length of all games."""
    layer: Dict[P, int] = {start: 1}
    per_depth: List[int] = []
    leaves = inner = edges = total_length = 0
    outcomes: Counter = Counter()
    depth = 0
    while layer:
        per_depth.append(sum(layer.values()))
        nxt: Dict[P, int] = {}
        for p, k in layer.items():
            kids = moves(p)
            if not kids:
                leaves += k
                total_length += k * depth
                outcomes[outcome(p)] += k
                continue
            inner += k
            edges += k * len(kids)
            for c in kids:
                nxt[c] = nxt.get(c, 0) + k
        layer = nxt
        depth += 1
    return {"per_depth": per_depth, "nodes": sum(per_depth), "leaves": leaves, "inner": inner, "edges": edges, "outcomes": dict(outcomes), "total_length": total_length}


# Tic-tac-toe. A position is a string of 9 cells, "X", "O" or ".", row by row.
# X is MAX and moves first.

LINES = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))
EMPTY = "." * 9


def ttt_winner(b: str):
    for i, j, k in LINES:
        if b[i] != "." and b[i] == b[j] == b[k]:
            return b[i]
    return None


def ttt_max_to_move(b: str) -> bool:
    return b.count("X") == b.count("O")


def ttt_moves(b: str) -> List[str]:
    if ttt_winner(b) or "." not in b:
        return []
    p = "X" if ttt_max_to_move(b) else "O"
    return [b[:i] + p + b[i + 1 :] for i in range(9) if b[i] == "."]


def ttt_outcome(b: str) -> int:
    w = ttt_winner(b)
    return 1 if w == "X" else -1 if w == "O" else 0


_ROT = (6, 3, 0, 7, 4, 1, 8, 5, 2)
_REF = (2, 1, 0, 5, 4, 3, 8, 7, 6)


def ttt_symmetries(b: str) -> Iterable[str]:
    """The 8 images of a board under the rotations and reflections of the square."""
    for _ in range(4):
        yield b
        yield "".join(b[i] for i in _REF)
        b = "".join(b[i] for i in _ROT)


def ttt_canonical(b: str) -> str:
    return min(ttt_symmetries(b))
