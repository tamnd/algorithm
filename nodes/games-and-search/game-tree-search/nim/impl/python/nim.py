# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/nim/. The authors are listed in prov/02YCWR.jsonl.

"""Nim and some of its variants, with two kinds of solver for each: a closed
rule (the XOR of the heap sizes for Nim) and a brute-force search over all
positions, which the tests compare. A position is a tuple of heap sizes."""

from functools import lru_cache, reduce
from itertools import combinations, product
from math import isqrt
from typing import Iterator, List, Sequence, Tuple

Position = Tuple[int, ...]


def nim_sum(heaps: Sequence[int]) -> int:
    """Bitwise XOR of the heap sizes."""
    return reduce(lambda a, b: a ^ b, heaps, 0)


def moves(heaps: Sequence[int]) -> Iterator[Position]:
    """All positions one Nim move away: lower one heap to a smaller size."""
    for i, a in enumerate(heaps):
        for b in range(a):
            yield tuple(heaps[:i]) + (b,) + tuple(heaps[i + 1:])


def _key(heaps: Sequence[int]) -> Position:
    return tuple(sorted(h for h in heaps if h > 0))


@lru_cache(maxsize=None)
def _brute(key: Position, misere: bool) -> bool:
    nxt = list(moves(key))
    if not nxt:
        return misere  # no move: the mover loses in normal play, wins in misere play
    return any(not _brute(_key(q), misere) for q in nxt)


def brute_force_first_player_wins(heaps: Sequence[int], misere: bool = False) -> bool:
    """True when the player to move wins with best play, by search."""
    return _brute(_key(heaps), misere)


def first_player_wins(heaps: Sequence[int]) -> bool:
    """Bouton's rule for normal play: the mover wins exactly when the
    nim-sum is not zero."""
    return nim_sum(heaps) != 0


def winning_moves(heaps: Sequence[int]) -> List[Tuple[int, int]]:
    """All moves (heap index, new size) to a position of nim-sum 0."""
    x = nim_sum(heaps)
    return [(i, a ^ x) for i, a in enumerate(heaps) if (a ^ x) < a]


def misere_first_player_wins(heaps: Sequence[int]) -> bool:
    """Bouton's rule for misere play, where the player who takes the last
    token loses. If some heap has 2 or more tokens, the outcome is the one of
    normal play. If every heap has at most 1 token, the mover wins exactly
    when the number of nonempty heaps is even."""
    if any(h >= 2 for h in heaps):
        return nim_sum(heaps) != 0
    return sum(heaps) % 2 == 0


# Moore's Nim_k: a move takes tokens from at least 1 and at most k heaps.

def moore_moves(heaps: Sequence[int], k: int) -> Iterator[Position]:
    n = len(heaps)
    for r in range(1, k + 1):
        for idx in combinations(range(n), r):
            ranges = [range(heaps[i]) for i in idx]
            for new in product(*ranges):
                h = list(heaps)
                for i, b in zip(idx, new):
                    h[i] = b
                yield tuple(h)


def moore_brute_first_player_wins(heaps: Sequence[int], k: int) -> bool:
    @lru_cache(maxsize=None)
    def win(p: Position) -> bool:
        return any(not win(tuple(sorted(q))) for q in moore_moves(p, k))

    return win(tuple(sorted(heaps)))


def moore_first_player_wins(heaps: Sequence[int], k: int) -> bool:
    """Moore's rule: the mover loses exactly when, for every bit position,
    the number of heaps with a 1 there is a multiple of k + 1."""
    width = max(heaps, default=0).bit_length()
    for bit in range(width):
        if sum((h >> bit) & 1 for h in heaps) % (k + 1):
            return True
    return False


# Lasker's Nim: a move removes tokens from one heap, or splits a heap into
# two nonempty heaps.

def lasker_grundy_table(n: int) -> List[int]:
    g = [0] * (n + 1)
    for h in range(1, n + 1):
        opts = {g[b] for b in range(h)}
        opts |= {g[a] ^ g[h - a] for a in range(1, h // 2 + 1)}
        m = 0
        while m in opts:
            m += 1
        g[h] = m
    return g


def lasker_grundy_rule(h: int) -> int:
    if h == 0:
        return 0
    r = h % 4
    if r == 3:
        return h + 1
    if r == 0:
        return h - 1
    return h


# Wythoff's game: take any number from one heap, or the same number from both.

def wythoff_brute_losses(n: int) -> List[Tuple[int, int]]:
    """All P-positions (a, b) with a <= b <= n, by a table."""
    lose = [[False] * (n + 1) for _ in range(n + 1)]
    for a in range(n + 1):
        for b in range(n + 1):
            win = any(lose[c][b] for c in range(a))
            win = win or any(lose[a][c] for c in range(b))
            win = win or any(lose[a - t][b - t] for t in range(1, min(a, b) + 1))
            lose[a][b] = not win
    return [(a, b) for a in range(n + 1) for b in range(a, n + 1) if lose[a][b]]


def wythoff_pairs(n: int) -> List[Tuple[int, int]]:
    """The pairs (floor(k phi), floor(k phi^2)) with second entry at most n,
    in exact integer arithmetic: floor(k phi) = (k + isqrt(5 k^2)) // 2."""
    out = []
    k = 0
    while True:
        a = (k + isqrt(5 * k * k)) // 2
        b = a + k
        if b > n:
            return out
        out.append((a, b))
        k += 1
