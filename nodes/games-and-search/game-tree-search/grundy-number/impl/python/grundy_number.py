# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/grundy-number/. The authors are listed in prov/VC5H7C.jsonl.

"""Grundy numbers of finite impartial games: a general memoized recursion,
tables for subtraction games and octal games, the Guy-Smith test for
periodicity, and a brute-force win/loss labeling to compare with."""

from functools import lru_cache
from typing import Callable, Hashable, Iterable, List, Optional, Sequence, Tuple


def mex(values: Iterable[int]) -> int:
    s = set(values)
    m = 0
    while m in s:
        m += 1
    return m


def grundy(position: Hashable, options: Callable[[Hashable], Iterable[Hashable]]) -> int:
    """g(p) = mex of g over the options of p, with a memo. The game must be
    finite and acyclic."""

    @lru_cache(maxsize=None)
    def g(p: Hashable) -> int:
        return mex(g(q) for q in options(p))

    return g(position)


def mover_loses(position: Hashable, options: Callable[[Hashable], Iterable[Hashable]]) -> bool:
    """Brute force: the player to move loses under normal play."""

    @lru_cache(maxsize=None)
    def lose(p: Hashable) -> bool:
        return all(not lose(q) for q in options(p))

    return lose(position)


def subtraction_table(moves: Sequence[int], n: int) -> List[int]:
    g: List[int] = []
    for i in range(n + 1):
        g.append(mex(g[i - m] for m in moves if m <= i))
    return g


def octal_table(digits: Sequence[int], n: int) -> List[int]:
    """Grundy values of the octal game 0.d1 d2 d3 ... for heaps 0..n.
    Digit d_k allows removing k tokens from a heap and leaving zero heaps
    (bit 1, only when the heap has exactly k tokens), one nonempty heap
    (bit 2) or two nonempty heaps (bit 4)."""
    g = [0] * (n + 1)
    for h in range(1, n + 1):
        opts = set()
        for k, d in enumerate(digits, start=1):
            if k > h:
                break
            rest = h - k
            if d & 1 and rest == 0:
                opts.add(0)
            if d & 2 and rest > 0:
                opts.add(g[rest])
            if d & 4 and rest >= 2:
                for a in range(1, rest // 2 + 1):
                    opts.add(g[a] ^ g[rest - a])
        g[h] = mex(opts)
    return g


KAYLES = (7, 7)
DAWSONS_KAYLES = (0, 7)


def last_exception(g: Sequence[int], period: int) -> int:
    """Largest n with g[n] != g[n + period] inside the table, or -1."""
    last = -1
    for n in range(len(g) - period):
        if g[n] != g[n + period]:
            last = n
    return last


def guy_smith_certifies(g: Sequence[int], n0: int, period: int, t: int) -> bool:
    """Guy and Smith: for an octal game whose moves remove at most t tokens,
    if g(n + p) = g(n) for all n with n0 <= n < 2 n0 + p + t, then this holds
    for all n >= n0. Return whether the table proves it."""
    hi = 2 * n0 + period + t
    if hi + period > len(g):
        raise ValueError("table too short")
    return all(g[n + period] == g[n] for n in range(n0, hi))


def eventual_period(g: Sequence[int], window: int) -> Optional[Tuple[int, int]]:
    """For a subtraction game whose largest move is window, the value at n
    depends only on the window values before n, so a repeated window proves
    periodicity. Return (start, period) for the first repeat."""
    seen = {}
    for n in range(window, len(g)):
        key = tuple(g[n - window:n])
        if key in seen:
            return seen[key], n - seen[key]
        seen[key] = n
    return None


def grundys_game_table(n: int) -> List[int]:
    """Grundy's game: split one heap into two nonempty heaps of different sizes."""
    g = [0] * (n + 1)
    for h in range(3, n + 1):
        g[h] = mex(g[a] ^ g[h - a] for a in range(1, (h + 1) // 2) if a != h - a)
    return g
