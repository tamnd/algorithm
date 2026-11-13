# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/frame-stewart-algorithm/. The authors are listed in prov/NSH7PT.jsonl.
"""The Frame-Stewart algorithm for the Tower of Hanoi with p >= 3 pegs.

Discs are numbered 1 (smallest) to n (largest). A move is a triple
(disc, from_peg, to_peg). Pegs are numbered 0 .. p - 1.
"""

from collections import deque
from functools import lru_cache
from typing import Dict, List, Sequence, Tuple

Move = Tuple[int, int, int]


@lru_cache(maxsize=None)
def frame_stewart_number(n: int, p: int) -> int:
    """S(n, p): the number of moves that the Frame-Stewart algorithm makes."""
    if p < 3:
        raise ValueError("need at least 3 pegs")
    if n == 0:
        return 0
    if n == 1:
        return 1
    if p == 3:
        return (1 << n) - 1
    return min(2 * frame_stewart_number(k, p) + frame_stewart_number(n - k, p - 1) for k in range(1, n))


def best_split(n: int, p: int) -> int:
    """The smallest k in 1 .. n - 1 that reaches the minimum in the recurrence."""
    best = None
    best_k = 0
    for k in range(1, n):
        v = 2 * frame_stewart_number(k, p) + frame_stewart_number(n - k, p - 1)
        if best is None or v < best:
            best, best_k = v, k
    return best_k


def frame_stewart_moves(n: int, p: int, src: int = 0, dst: int = -1) -> List[Move]:
    """The moves of the Frame-Stewart algorithm for n discs on p pegs.

    The work is done with an explicit stack, so large n does not hit the
    recursion limit.
    """
    if dst < 0:
        dst = p - 1
    moves: List[Move] = []
    # A task (lo, hi, src, dst, pegs) moves the discs lo .. hi, which sit on
    # src above all larger discs, to dst, using only the pegs in `pegs`.
    stack = [(1, n, src, dst, tuple(range(p)))]
    while stack:
        lo, hi, s, d, pegs = stack.pop()
        m = hi - lo + 1
        if m <= 0:  # @line L1
            continue
        if m == 1:  # @line L2
            moves.append((lo, s, d))
            continue
        spares = [q for q in pegs if q != s and q != d]
        a = spares[0]  # @line L3
        if len(spares) == 1:  # @line L4
            # Classical three-peg recursion: hi - 1 discs to a, hi to d, back.
            stack.append((lo, hi - 1, a, d, pegs))  # @line L5
            stack.append((hi, hi, s, d, pegs))
            stack.append((lo, hi - 1, s, a, pegs))
            continue
        k = best_split(m, len(pegs))  # @line L6
        rest = tuple(q for q in pegs if q != a)
        # Pushed in reverse order: the top k discs go to a with all pegs,
        # the other m - k go to d without peg a, then the k discs go to d.
        stack.append((lo, lo + k - 1, a, d, pegs))  # @line L9
        stack.append((lo + k, hi, s, d, rest))  # @line L8
        stack.append((lo, lo + k - 1, s, a, pegs))  # @line L7
    return moves


def apply_moves(n: int, p: int, moves: Sequence[Move], src: int = 0) -> List[List[int]]:
    """Play the moves from all discs on src; raise ValueError on an illegal move."""
    pegs: List[List[int]] = [[] for _ in range(p)]
    pegs[src] = list(range(n, 0, -1))
    for disc, a, b in moves:
        if not pegs[a] or pegs[a][-1] != disc:
            raise ValueError("disc %d is not on top of peg %d" % (disc, a))
        if pegs[b] and pegs[b][-1] < disc:
            raise ValueError("disc %d cannot go on a smaller disc" % disc)
        pegs[b].append(pegs[a].pop())
    return pegs


def hanoi_distances(n: int, p: int, src: int = 0) -> Dict[int, int]:
    """Breadth-first search over all p^n states, from all discs on src.

    A state is an integer whose base-p digit i is the peg of disc i + 1.
    """
    start = sum(src * p ** i for i in range(n))
    powers = [p ** i for i in range(n)]
    dist = {start: 0}
    queue = deque([start])
    while queue:
        s = queue.popleft()
        d = dist[s] + 1
        top = [n] * p  # index of the smallest disc on each peg, n if empty
        x = s
        for i in range(n):
            q = x % p
            x //= p
            if top[q] == n:
                top[q] = i
        for a in range(p):
            i = top[a]
            if i == n:
                continue
            for b in range(p):
                if b != a and top[b] > i:
                    t = s + (b - a) * powers[i]
                    if t not in dist:
                        dist[t] = d
                        queue.append(t)
    return dist


def optimal_by_search(n: int, p: int) -> int:
    """The true minimum number of moves from peg 0 to peg p - 1, by BFS."""
    dist = hanoi_distances(n, p)
    return dist[sum((p - 1) * p ** i for i in range(n))]
