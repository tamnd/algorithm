# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fiduccia-mattheyses/. The authors are listed in prov/K9FVJG.jsonl.

from typing import Callable, Optional, Sequence


def cut_size(nets: Sequence[Sequence[int]], side: Sequence[int]) -> int:
    """Number of nets with pins on both sides (0 and 1)."""
    return sum(1 for e in nets if len({side[v] for v in e}) == 2)


def fiduccia_mattheyses(
    nets: Sequence[Sequence[int]],
    n: int,
    side: Sequence[int],
    lo: int,
    hi: int,
    on_step: Optional[Callable[[int, int, list[int], list[bool], list[int]], None]] = None,
) -> list[int]:
    """Improve a two-way partition of a hypergraph by Fiduccia-Mattheyses passes.

    The vertices are 0 .. n-1, and each net is a list of distinct vertices.
    side[v] is 0 or 1. The number of vertices on side 0 must lie in [lo, hi]
    at the start, and it stays in [lo, hi] at every step. The cut is the
    number of nets with pins on both sides.

    Returns the final sides as a new list. If on_step is given, it is called
    after each tentative move with (v, g, side, locked, gain), where v moved
    with gain g, side is the tentative partition after the move, and gain
    holds the stored gains (valid for unlocked vertices). It exists for tests.

    Cost per pass: O(n + P) time and space, where P is the total number of pins.
    """
    side = list(side)
    count0 = side.count(0)
    if not lo <= count0 <= hi:
        raise ValueError("the start partition is not balanced")
    vnets: list[list[int]] = [[] for _ in range(n)]
    for i, e in enumerate(nets):
        for v in e:
            vnets[v].append(i)
    pmax = max((len(x) for x in vnets), default=0)
    while True:  # @line L1
        cnt = [[0, 0] for _ in nets]  # @line L2
        for i, e in enumerate(nets):
            for v in e:
                cnt[i][side[v]] += 1
        lockcnt = [[0, 0] for _ in nets]
        gain = [0] * n
        for v in range(n):
            s = side[v]
            for i in vnets[v]:
                if cnt[i][s] == 1:
                    gain[v] += 1
                if cnt[i][1 - s] == 0:
                    gain[v] -= 1
        buckets = [[{} for _ in range(2 * pmax + 1)] for _ in range(2)]
        top = [-1, -1]
        for v in range(n):
            b = gain[v] + pmax
            buckets[side[v]][b][v] = None
            top[side[v]] = max(top[side[v]], b)
        locked = [False] * n
        tent = side[:]
        c0 = count0
        moves: list[int] = []
        gains: list[int] = []

        def bump(u: int, delta: int) -> None:
            su = tent[u]
            del buckets[su][gain[u] + pmax][u]
            gain[u] += delta
            b = gain[u] + pmax
            buckets[su][b][u] = None
            if b > top[su]:
                top[su] = b

        while True:  # @line L3
            best = None
            for s in (0, 1):
                if (s == 0 and c0 - 1 < lo) or (s == 1 and c0 + 1 > hi):
                    continue
                while top[s] >= 0 and not buckets[s][top[s]]:
                    top[s] -= 1
                if top[s] < 0:
                    continue
                size = c0 if s == 0 else n - c0
                key = (top[s], size, -s)
                if best is None or key > best[0]:
                    best = (key, s)
            if best is None:
                break
            s = best[1]  # @line L4
            v = next(reversed(buckets[s][top[s]]))
            t = 1 - s
            del buckets[s][top[s]][v]  # @line L5
            locked[v] = True
            moves.append(v)
            gains.append(gain[v])
            for i in vnets[v]:  # @line L6
                # Each scan below happens O(1) times per net in a pass: once a
                # side of the net holds a locked pin, its count never returns
                # to the triggering value with no locked pin.
                if cnt[i][t] == 0:
                    for u in nets[i]:
                        if not locked[u]:
                            bump(u, 1)
                elif cnt[i][t] == 1 and lockcnt[i][t] == 0:
                    for u in nets[i]:
                        if tent[u] == t:
                            bump(u, -1)
                cnt[i][s] -= 1
                cnt[i][t] += 1
                lockcnt[i][t] += 1
                if cnt[i][s] == 0:
                    for u in nets[i]:
                        if not locked[u]:
                            bump(u, -1)
                elif cnt[i][s] == 1 and lockcnt[i][s] == 0:
                    for u in nets[i]:
                        if tent[u] == s and not locked[u]:
                            bump(u, 1)
            tent[v] = t  # @line L7
            c0 += -1 if s == 0 else 1
            if on_step is not None:
                on_step(v, gains[-1], tent[:], locked[:], gain[:])
        best_k, best_total, total = 0, 0, 0  # @line L8
        for k, g in enumerate(gains, start=1):
            total += g
            if total > best_total:
                best_k, best_total = k, total
        if best_total <= 0:  # @line L9
            break
        for v in moves[:best_k]:  # @line L10
            count0 += -1 if side[v] == 0 else 1
            side[v] = 1 - side[v]
    return side  # @line L11
