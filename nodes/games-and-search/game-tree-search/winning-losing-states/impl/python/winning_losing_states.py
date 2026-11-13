# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/winning-losing-states/. The authors are listed in prov/RX8R4R.jsonl.

"""Label every position of a finite two-player game graph as a win (W) or a
loss (L) for the player to move, or a draw (D) when neither player can force
a result. The graph may have cycles. The method works backward from the
terminal positions with a counter per position, in O(V + E) time."""

from collections import deque
from typing import Callable, Dict, Hashable, Iterable, List, Optional, Sequence

P = Hashable
WIN, LOSS, DRAW = "W", "L", "D"


def label_positions(
    positions: Iterable[P],
    moves: Callable[[P], Sequence[P]],
    terminal_label: Optional[Callable[[P], str]] = None,
) -> Dict[P, str]:
    """Return a dict from each position to "W", "L" or "D", for the player to move.

    `positions` must hold every position, and `moves(p)` the positions after
    each legal move from p, all inside `positions`. A move listed twice counts
    twice. A position with no moves is terminal; `terminal_label(p)` gives its
    label, and under the normal play rule (the player who cannot move loses)
    it is "L", the default. Only "W" and "L" spread to other positions.
    Cost: O(V + E) for V positions and E moves.
    """
    pos = list(positions)
    count: Dict[P, int] = {}
    preds: Dict[P, List[P]] = {p: [] for p in pos}
    label: Dict[P, str] = {}
    queue: deque = deque()
    for p in pos:  # @line L1
        kids = moves(p)
        count[p] = len(kids)  # @line L1
        for c in kids:
            preds[c].append(p)
    for p in pos:  # @line L2
        if count[p] == 0:
            label[p] = terminal_label(p) if terminal_label else LOSS  # @line L2
            if label[p] != DRAW:
                queue.append(p)  # @line L2
    while queue:  # @line L3
        q = queue.popleft()  # @line L3
        for p in preds[q]:  # @line L4
            if p in label:
                continue  # @line L4
            if label[q] == LOSS:  # @line L5
                label[p] = WIN  # @line L5
                queue.append(p)  # @line L5
            else:  # @line L6
                count[p] -= 1  # @line L6
                if count[p] == 0:  # @line L6
                    label[p] = LOSS  # @line L6
                    queue.append(p)  # @line L6
    for p in pos:  # @line L7
        label.setdefault(p, DRAW)  # @line L7
    return label


def reachable(start: P, moves: Callable[[P], Sequence[P]]) -> set:
    """All positions reachable from `start`, by an explicit-stack search."""
    seen = {start}
    stack = [start]
    while stack:
        p = stack.pop()
        for c in moves(p):
            if c not in seen:
                seen.add(c)
                stack.append(c)
    return seen


def subtraction_moves(s: Sequence[int]) -> Callable[[int], List[int]]:
    """Moves of the subtraction game with subtraction set s: take k counters, k in s."""
    return lambda n: [n - k for k in s if k <= n]
