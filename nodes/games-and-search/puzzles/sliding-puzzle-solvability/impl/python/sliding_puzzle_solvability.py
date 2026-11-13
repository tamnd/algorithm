# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sliding-puzzle-solvability/. The authors are listed in prov/9Q436M.jsonl.
"""The parity test for sliding puzzles, and the breadth-first search that checks it.

A board of width w and height h is a tuple of length w*h in row-major order.
The value 0 is the blank and 1 .. w*h - 1 are the tiles. The standard goal is
(1, 2, ..., w*h - 1, 0): the tiles in reading order and the blank at the
bottom right.
"""

from collections import deque
from typing import Dict, Iterable, List, Optional, Sequence, Set, Tuple

Board = Tuple[int, ...]


def standard_goal(w: int, h: int) -> Board:
    return tuple(range(1, w * h)) + (0,)


def permutation_parity(seq: Sequence[int]) -> int:
    """Parity (0 even, 1 odd) of the number of inversions of seq, in O(n) time.

    The values of seq must be distinct. The parity of the inversions equals
    the parity of n minus the number of cycles of the permutation that sorts seq.
    """
    order = sorted(range(len(seq)), key=seq.__getitem__)
    seen = [False] * len(seq)
    cycles = 0
    for i in range(len(seq)):
        if not seen[i]:
            cycles += 1
            j = i
            while not seen[j]:
                seen[j] = True
                j = order[j]
    return (len(seq) - cycles) & 1


def inversions(seq: Sequence[int]) -> int:
    """The number of pairs i < j with seq[i] > seq[j], in O(n^2) time."""
    n = len(seq)
    return sum(1 for i in range(n) for j in range(i + 1, n) if seq[i] > seq[j])


def invariant(board: Board, w: int) -> int:
    """The quantity that no move changes.

    It is the parity of the inversions of the tiles (blank removed), plus,
    when w is even, the parity of the row of the blank.
    """
    tiles = [t for t in board if t != 0]
    p = permutation_parity(tiles)
    if w % 2 == 0:
        p ^= (board.index(0) // w) & 1
    return p


def is_solvable(board: Board, w: int, h: int, goal: Optional[Board] = None) -> bool:
    """True when board can reach goal (default: the standard goal), for w, h >= 2."""
    if w < 2 or h < 2:
        raise ValueError("the parity rule needs w >= 2 and h >= 2")
    if goal is None:
        goal = standard_goal(w, h)
    return invariant(board, w) == invariant(goal, w)


def is_solvable_standard(board: Board, w: int) -> bool:
    """The rule in its textbook form, for the standard goal.

    Odd width: the number of inversions is even. Even width: the number of
    inversions plus the row of the blank counted from the bottom (the bottom
    row is 1) is odd.
    """
    h = len(board) // w
    inv = inversions([t for t in board if t != 0])
    if w % 2 == 1:
        return inv % 2 == 0
    row_from_bottom = h - board.index(0) // w
    return (inv + row_from_bottom) % 2 == 1


def grid_adjacency(w: int, h: int) -> List[List[int]]:
    adj: List[List[int]] = [[] for _ in range(w * h)]
    for i in range(w * h):
        r, c = divmod(i, w)
        if r > 0:
            adj[i].append(i - w)
        if r < h - 1:
            adj[i].append(i + w)
        if c > 0:
            adj[i].append(i - 1)
        if c < w - 1:
            adj[i].append(i + 1)
    return adj


def reachable(start: Board, adj: Sequence[Sequence[int]]) -> Set[Board]:
    """All arrangements reachable from start when the blank (0) slides along adj."""
    seen = {start}
    queue = deque([start])
    while queue:
        b = queue.popleft()
        z = b.index(0)
        for y in adj[z]:
            nb = list(b)
            nb[z], nb[y] = nb[y], 0
            t = tuple(nb)
            if t not in seen:
                seen.add(t)
                queue.append(t)
    return seen


def bfs_distances(start: Board, adj: Sequence[Sequence[int]]) -> Dict[Board, int]:
    """Distance in single-tile moves from start to each reachable arrangement."""
    dist = {start: 0}
    queue = deque([start])
    while queue:
        b = queue.popleft()
        d = dist[b] + 1
        z = b.index(0)
        for y in adj[z]:
            nb = list(b)
            nb[z], nb[y] = nb[y], 0
            t = tuple(nb)
            if t not in dist:
                dist[t] = d
                queue.append(t)
    return dist


def theta_graph(a: int, b: int, c: int) -> List[List[int]]:
    """Two vertices 0 and 1 joined by three internally disjoint paths of a, b and c edges."""
    adj: Dict[int, Set[int]] = {0: set(), 1: set()}
    nxt = 2
    for length in (a, b, c):
        prev = 0
        for _ in range(length - 1):
            adj[nxt] = set()
            adj[prev].add(nxt)
            adj[nxt].add(prev)
            prev = nxt
            nxt += 1
        adj[prev].add(1)
        adj[1].add(prev)
    return [sorted(adj[v]) for v in range(nxt)]


def puzzle_group_order(adj: Sequence[Sequence[int]], blank: int = 0) -> int:
    """The number of arrangements with the blank at `blank` that the start reaches.

    This is the order of the group of tile permutations that the puzzle on the
    graph can make (Wilson 1974).
    """
    n = len(adj)
    start = [0] * n
    k = 1
    for v in range(n):
        if v != blank:
            start[v] = k
            k += 1
    return sum(1 for b in reachable(tuple(start), adj) if b[blank] == 0)


def is_bipartite(adj: Sequence[Iterable[int]]) -> bool:
    color = [-1] * len(adj)
    for s in range(len(adj)):
        if color[s] != -1:
            continue
        color[s] = 0
        queue = deque([s])
        while queue:
            u = queue.popleft()
            for v in adj[u]:
                if color[v] == -1:
                    color[v] = color[u] ^ 1
                    queue.append(v)
                elif color[v] == color[u]:
                    return False
    return True
