# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sss-star/. The authors are listed in prov/QXZG5Q.jsonl.

"""SSS*: Stockman's best-first search for the minimax value of a game tree."""

import heapq
import math
from collections import defaultdict
from fractions import Fraction
from typing import Callable, Dict, Hashable, List, Optional, Sequence, Tuple, TypeVar, Union

S = TypeVar("S")
Value = Union[int, float, Fraction]
Path = Tuple[int, ...]
INF = math.inf
LIVE, SOLVED = 0, 1

Moves = Callable[[S], Sequence[Tuple[Hashable, S]]]


def sss_star(
    pos: S,
    depth: int,
    moves: Moves,
    evaluate: Callable[[S], Value],
    leaves: Optional[List[Path]] = None,
    stats: Optional[dict] = None,
) -> Value:
    """The depth-limited minimax value of pos, with MAX to move at pos.

    `evaluate` scores a position for the side to move there, as in negamax.
    A node at an odd depth is a MIN node, so its score for MAX is the
    negation, and the result equals the negamax value of pos. `leaves` gets
    the path (a tuple of child indexes) of each evaluated leaf, in order.
    `stats["open"]` gets the largest number of states in OPEN.

    Precondition: a finite tree. Cost: each leaf is evaluated at most once,
    and never a leaf that left-to-right alpha-beta skips. Each step costs
    O(log |OPEN| + d): removed states stay in the heap and are skipped.
    """
    at: Dict[Path, S] = {(): pos}  # the position at each path in use
    below: Dict[Path, int] = defaultdict(int)  # states in OPEN at or below a path
    dead = set()  # MAX nodes solved by L10: the states below them are removed
    heap: List[Tuple[Value, Path, int]] = []
    biggest = 0

    def insert(h: Value, path: Path, status: int) -> None:
        # A heap entry is (-h, path, status): the highest h first and, for
        # equal h, the leftmost path.
        nonlocal biggest
        heapq.heappush(heap, (-h, path, status))
        for i in range(len(path) + 1):
            below[path[:i]] += 1
        biggest = max(biggest, below[()])

    insert(INF, (), LIVE)  # @line L1
    while True:  # @line L2
        neg_h, path, status = heapq.heappop(heap)  # @line L3
        if any(path[:i] in dead for i in range(len(path))):
            continue  # removed by L10 before
        for i in range(len(path) + 1):
            below[path[:i]] -= 1
        h = -neg_h
        if not path and status == SOLVED:  # @line L4
            if stats is not None:
                stats["open"] = biggest
            return h
        is_min = len(path) % 2 == 1
        if status == LIVE:  # @line L5
            kids = moves(at[path]) if len(path) < depth else []
            if not kids:  # @line L6
                v = evaluate(at[path])
                if leaves is not None:
                    leaves.append(path)
                insert(min(h, -v if is_min else v), path, SOLVED)
            elif is_min:  # @line L7
                at[path + (0,)] = kids[0][1]
                insert(h, path + (0,), LIVE)
            else:  # @line L8
                for i, (_, c) in enumerate(kids):
                    at[path + (i,)] = c
                    insert(h, path + (i,), LIVE)
            continue
        up = path[:-1]
        if is_min:  # @line L9
            gone = below[up]  # @line L10  solve the MAX parent and remove all below it
            for i in range(len(up) + 1):
                below[up[:i]] -= gone
            dead.add(up)
            insert(h, up, SOLVED)
            continue
        siblings = moves(at[up])
        i = path[-1] + 1
        if i < len(siblings):  # @line L11
            at[up + (i,)] = siblings[i][1]
            insert(h, up + (i,), LIVE)
        else:  # @line L12
            insert(h, up, SOLVED)
