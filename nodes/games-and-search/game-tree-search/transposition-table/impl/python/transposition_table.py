# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/transposition-table/. The authors are listed in prov/25X300.jsonl.

"""A transposition table and a fail-soft negamax alpha-beta search that uses it."""

import math
from fractions import Fraction
from typing import Callable, Hashable, List, Optional, Sequence, Tuple, TypeVar, Union

S = TypeVar("S")
Value = Union[int, float, Fraction]
INF = math.inf

EXACT, LOWER, UPPER = "exact", "lower", "upper"


class Entry:
    """One slot: the full key, the remaining depth, the bound flag, the value and the best move."""

    __slots__ = ("key", "depth", "flag", "value", "move")

    def __init__(self, key, depth, flag, value, move):
        self.key, self.depth, self.flag, self.value, self.move = key, depth, flag, value, move


class TranspositionTable:
    """A table of 2^k slots, indexed by the low k bits of a 64-bit key.

    policy "always" replaces the old entry on every store; policy "depth"
    keeps the old entry when it holds a deeper search of another position.
    Cost: O(1) time per probe and per store; O(2^k) space.
    """

    def __init__(self, k: int = 16, policy: str = "depth"):
        self.mask = (1 << k) - 1
        self.slots: List[Optional[Entry]] = [None] * (1 << k)
        self.policy = policy
        self.stores = 0
        self.hits = 0

    def probe(self, key: int) -> Optional[Entry]:
        e = self.slots[key & self.mask]  # @line L1
        if e is not None and e.key == key:  # @line L2
            self.hits += 1
            return e
        return None  # @line L3

    def store(self, key: int, depth: int, flag: str, value: Value, move) -> None:
        i = key & self.mask
        old = self.slots[i]  # @line L4
        if self.policy == "depth" and old is not None and old.key != key and old.depth > depth:  # @line L5
            return  # keep the deeper entry of another position
        self.slots[i] = Entry(key, depth, flag, value, move)  # @line L6
        self.stores += 1


def search(
    pos: S,
    depth: int,
    alpha: Value,
    beta: Value,
    moves: Callable[[S], Sequence[Tuple[Hashable, S]]],
    evaluate: Callable[[S], Value],
    key: Callable[[S], int],
    tt: TranspositionTable,
    use_flags: bool = True,
    count: Optional[List[int]] = None,
) -> Value:
    """Fail-soft negamax alpha-beta with a transposition table.

    `moves(pos)` lists (move, child) pairs; an empty list means a terminal
    position. `evaluate(pos)` is the value for the side to move, used at
    terminal positions and when `depth` reaches 0. With use_flags=False every
    result is stored as exact, which is the bug shown on the page.

    Precondition: alpha < beta; `key` is one-to-one on the positions met; the
    depth-d value of a position does not depend on the path to it, and every
    depth at which the search meets a position gives it the same value.
    Cost: O(1) table work per node, on top of the work of alpha-beta.
    """
    if count is not None:
        count[0] += 1
    k = key(pos)
    e = tt.probe(k)  # @line L7
    if e is not None and e.depth >= depth:  # @line L8
        if e.flag == EXACT:  # @line L9
            return e.value
        if e.flag == LOWER and e.value >= beta:
            return e.value
        if e.flag == UPPER and e.value <= alpha:
            return e.value
    kids = moves(pos)
    if depth == 0 or not kids:  # @line L10
        v = evaluate(pos)  # @line L11
        tt.store(k, depth, EXACT, v, None)
        return v
    if e is not None and e.move is not None:  # @line L12
        kids = sorted(kids, key=lambda mc: mc[0] != e.move)  # the stored best move first
    m, best = -INF, None  # @line L13
    for mv, c in kids:  # @line L14
        t = -search(c, depth - 1, -beta, -max(m, alpha), moves, evaluate, key, tt, use_flags, count)  # @line L15
        if t > m:  # @line L16
            m, best = t, mv
        if m >= beta:  # @line L17
            break
    if not use_flags:
        flag = EXACT  # wrong: a cut-off result is only a bound
    elif m <= alpha:  # @line L18
        flag = UPPER
    elif m >= beta:
        flag = LOWER
    else:
        flag = EXACT
    tt.store(k, depth, flag, m, best)  # @line L19
    return m  # @line L20
