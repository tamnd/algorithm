# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tower-of-hanoi/. The authors are listed in prov/BFC4VM.jsonl.
"""The Tower of Hanoi with three pegs: the optimal moves, the k-th move, and a BFS oracle.

Discs are 1 (smallest) to n (largest); pegs are 0, 1, 2. The tower starts on
peg 0 and must end on peg 2. A move is (disc, from_peg, to_peg).
"""

from collections import deque
from typing import Dict, List, Sequence, Tuple

Move = Tuple[int, int, int]


def hanoi_moves(n: int, src: int = 0, dst: int = 2) -> List[Move]:
    """The unique optimal solution, 2^n - 1 moves, with an explicit stack."""
    aux = 3 - src - dst
    moves: List[Move] = []
    # A task (m, s, d, a, single) either moves the top m discs from s to d
    # through a, or (single is True) moves disc m alone from s to d.
    stack = [(n, src, dst, aux, False)]
    while stack:
        m, s, d, a, single = stack.pop()
        if single:
            moves.append((m, s, d))
        elif m > 0:
            stack.append((m - 1, a, d, s, False))
            stack.append((m, s, d, a, True))
            stack.append((m - 1, s, a, d, False))
    return moves


def trailing_zeros(k: int) -> int:
    return (k & -k).bit_length() - 1


def kth_move(n: int, k: int) -> Move:
    """Move number k (1 <= k <= 2^n - 1) of the optimal solution, in O(n) bit operations.

    The disc is 1 plus the number of trailing zero bits of k. Odd discs cycle
    0 -> 2 -> 1 -> 0 and even discs cycle 0 -> 1 -> 2 -> 0 when n is odd; the
    directions swap when n is even.
    """
    if not 1 <= k < (1 << n):
        raise ValueError("k out of range")
    disc = trailing_zeros(k) + 1
    # Disc d moves at k = 2^(d-1) (2j + 1); this is its move number j.
    times = k >> disc
    step = 2 if (n - disc) % 2 == 0 else 1  # +2 is the cycle 0 -> 2 -> 1
    frm = (times * step) % 3
    to = (frm + step) % 3
    return (disc, frm, to)


def apply_moves(n: int, moves: Sequence[Move], src: int = 0) -> List[List[int]]:
    """Play the moves from the full tower on src; raise ValueError on an illegal move."""
    pegs: List[List[int]] = [[], [], []]
    pegs[src] = list(range(n, 0, -1))
    for disc, a, b in moves:
        if not pegs[a] or pegs[a][-1] != disc:
            raise ValueError("disc %d is not on top of peg %d" % (disc, a))
        if pegs[b] and pegs[b][-1] < disc:
            raise ValueError("disc %d cannot go on a smaller disc" % disc)
        pegs[b].append(pegs[a].pop())
    return pegs


def state_after(n: int, k: int) -> Tuple[int, ...]:
    """The peg of each disc 1 .. n after k optimal moves, without playing them.

    Disc d has moved floor((k + 2^(d-1)) / 2^d) times, and each of its moves
    goes one step around its cycle.
    """
    pegs = []
    for d in range(1, n + 1):
        times = (k + (1 << (d - 1))) >> d
        step = 2 if (n - d) % 2 == 0 else 1
        pegs.append((times * step) % 3)
    return tuple(pegs)


def distance_to_tower(state: Sequence[int], target: int) -> int:
    """The least number of moves from any state to the full tower on target.

    Go from the largest disc down. A disc already on the current goal peg
    costs nothing. Otherwise it must move once, after the smaller discs are
    gathered on the third peg, which costs 2^(d-1) moves for disc d, and the
    third peg becomes the goal for the smaller discs.
    """
    d = 0
    goal = target
    for i in range(len(state) - 1, -1, -1):
        if state[i] != goal:
            d += 1 << i
            goal = 3 - state[i] - goal
    return d


def neighbours(state: Tuple[int, ...]) -> List[Tuple[int, ...]]:
    """States one legal move away. state[i] is the peg of disc i + 1."""
    n = len(state)
    top = [n, n, n]
    for i in range(n - 1, -1, -1):
        top[state[i]] = i
    out = []
    for a in range(3):
        i = top[a]
        if i == n:
            continue
        for b in range(3):
            if b != a and top[b] > i:
                s = list(state)
                s[i] = b
                out.append(tuple(s))
    return out


def bfs(n: int, src: int = 0) -> Tuple[Dict[Tuple[int, ...], int], Dict[Tuple[int, ...], int]]:
    """Distances from the tower on src, and the number of shortest paths to each state."""
    start = (src,) * n
    dist = {start: 0}
    ways = {start: 1}
    queue = deque([start])
    while queue:
        s = queue.popleft()
        for t in neighbours(s):
            if t not in dist:
                dist[t] = dist[s] + 1
                ways[t] = ways[s]
                queue.append(t)
            elif dist[t] == dist[s] + 1:
                ways[t] += ways[s]
    return dist, ways
