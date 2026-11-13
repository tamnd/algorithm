# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sliding-tile-puzzle/. The authors are listed in prov/8BMZ6Z.jsonl.
"""The w x h sliding tile puzzle: moves, breadth-first search, Manhattan
distance, linear conflict and IDA*.

A state is a tuple of length w * h in reading order; 0 is the blank and the
goal is (1, 2, ..., w * h - 1, 0), with the blank in the bottom right corner.
"""

from collections import deque
from typing import Callable, Dict, Iterator, List, Optional, Sequence, Tuple

State = Tuple[int, ...]


def goal(w: int, h: int) -> State:
    return tuple(range(1, w * h)) + (0,)


def neighbours(state: State, w: int, h: int) -> Iterator[State]:
    """States one move away: a tile next to the blank slides into it."""
    b = state.index(0)
    r, c = divmod(b, w)
    for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        nr, nc = r + dr, c + dc
        if 0 <= nr < h and 0 <= nc < w:
            t = nr * w + nc
            s = list(state)
            s[b], s[t] = s[t], s[b]
            yield tuple(s)


def bfs_distances(w: int, h: int) -> Dict[State, int]:
    """Distance to the goal of every state that can reach it."""
    start = goal(w, h)
    dist = {start: 0}
    queue = deque([start])
    while queue:
        s = queue.popleft()
        d = dist[s] + 1
        for t in neighbours(s, w, h):
            if t not in dist:
                dist[t] = d
                queue.append(t)
    return dist


def manhattan(state: State, w: int, h: int) -> int:
    """Sum over tiles of the row and column distance to the goal cell."""
    total = 0
    for i, t in enumerate(state):
        if t:
            g = t - 1
            total += abs(i // w - g // w) + abs(i % w - g % w)
    return total


def _longest_increasing(seq: Sequence[int]) -> int:
    best: List[int] = []
    for x in seq:
        lo, hi = 0, len(best)
        while lo < hi:
            mid = (lo + hi) // 2
            if best[mid] < x:
                lo = mid + 1
            else:
                hi = mid
        if lo == len(best):
            best.append(x)
        else:
            best[lo] = x
    return len(best)


def linear_conflict(state: State, w: int, h: int) -> int:
    """Manhattan distance plus 2 for each tile that must leave its line.

    In each row, take the tiles whose goal is in that row. Tiles that are not
    in increasing order of goal column must pass one another, and one of each
    passing pair leaves the row and comes back, two extra moves. The fewest
    tiles to remove so that the rest are in order is the row length minus a
    longest increasing subsequence. Columns are treated in the same way. Rows
    and columns charge different moves (vertical against horizontal), so the
    sum stays admissible.
    """
    extra = 0
    for r in range(h):
        line = [state[r * w + c] - 1 for c in range(w) if state[r * w + c] and (state[r * w + c] - 1) // w == r]
        extra += len(line) - _longest_increasing([g % w for g in line])
    for c in range(w):
        line = [state[r * w + c] - 1 for r in range(h) if state[r * w + c] and (state[r * w + c] - 1) % w == c]
        extra += len(line) - _longest_increasing([g // w for g in line])
    return manhattan(state, w, h) + 2 * extra


def ida_star(state: State, w: int, h: int,
             heuristic: Callable[[State, int, int], int] = manhattan) -> Optional[List[State]]:
    """An optimal path from state to the goal by iterative deepening A*.

    The state must be solvable; the parity rule of the sliding puzzle
    solvability theorem tells which states are.
    """
    target = goal(w, h)
    path = [state]
    on_path = {state}

    def search(g: int, bound: int) -> int:
        s = path[-1]
        f = g + heuristic(s, w, h)
        if f > bound:
            return f
        if s == target:
            return -1
        nxt_bound = 1 << 30
        for t in neighbours(s, w, h):
            if t in on_path:
                continue
            path.append(t)
            on_path.add(t)
            r = search(g + 1, bound)
            if r == -1:
                return -1
            nxt_bound = min(nxt_bound, r)
            path.pop()
            on_path.discard(t)
        return nxt_bound

    bound = heuristic(state, w, h)
    while True:
        r = search(0, bound)
        if r == -1:
            return list(path)
        if r >= 1 << 30:
            return None
        bound = r


def scramble(w: int, h: int, steps: int, rnd) -> State:
    """A solvable state from a random walk of the blank."""
    s = goal(w, h)
    prev = None
    for _ in range(steps):
        options = [t for t in neighbours(s, w, h) if t != prev]
        prev, s = s, rnd.choice(options)
    return s
