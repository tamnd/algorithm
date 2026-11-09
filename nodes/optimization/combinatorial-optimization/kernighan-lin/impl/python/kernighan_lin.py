# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kernighan-lin/. The authors are listed in prov/NEYJA8.jsonl.

from typing import Callable, Optional, Sequence


def cut_weight(c: Sequence[Sequence[int]], side: Sequence[int]) -> int:
    """Total weight of the edges whose ends have different sides (0 or 1)."""
    n = len(c)
    return sum(c[u][v] for u in range(n) for v in range(u + 1, n) if side[u] != side[v])


def kernighan_lin(
    c: Sequence[Sequence[int]],
    a: Sequence[int],
    on_step: Optional[Callable[[list[int], list[int], list[bool], int, int, int], None]] = None,
) -> tuple[list[int], list[int]]:
    """Improve the bisection (a, rest) of a weighted graph by Kernighan-Lin passes.

    c is a symmetric n by n matrix of non-negative integer edge weights with
    a zero diagonal. a lists the vertices of side A; the other vertices form
    side B. The sizes of the two sides never change.

    Returns the final sides (A, B) as sorted lists. If on_step is given, it is
    called after each tentative swap with (side, D, locked, a, b, g), where
    side and D describe the tentative state after the swap of a and b with
    gain g. It exists for tests.

    Cost per pass: O(n^3) time with this simple pair search, O(n) extra space.
    """
    n = len(c)
    side = [1] * n
    for v in a:
        side[v] = 0
    while True:  # @line L1
        d = [0] * n  # @line L2
        for v in range(n):
            for u in range(n):
                if u != v:
                    d[v] += c[v][u] if side[u] != side[v] else -c[v][u]
        locked = [False] * n
        tent = side[:]
        gains: list[int] = []
        pairs: list[tuple[int, int]] = []
        steps = min(tent.count(0), tent.count(1))
        for _ in range(steps):  # @line L3
            best = None
            for x in range(n):  # @line L4
                if locked[x] or tent[x] != 0:
                    continue
                for y in range(n):
                    if locked[y] or tent[y] != 1:
                        continue
                    g = d[x] + d[y] - 2 * c[x][y]
                    if best is None or g > best[0]:
                        best = (g, x, y)
            g, x, y = best
            gains.append(g)  # @line L5
            pairs.append((x, y))
            locked[x] = locked[y] = True
            for v in range(n):
                if locked[v]:
                    continue
                if tent[v] == 0:  # @line L6
                    d[v] += 2 * c[v][x] - 2 * c[v][y]
                else:  # @line L7
                    d[v] += 2 * c[v][y] - 2 * c[v][x]
            tent[x], tent[y] = 1, 0
            if on_step is not None:
                on_step(tent[:], d[:], locked[:], x, y, g)
        best_k, best_total, total = 0, 0, 0  # @line L8
        for k, g in enumerate(gains, start=1):
            total += g
            if total > best_total:
                best_k, best_total = k, total
        if best_total <= 0:  # @line L9
            break
        for x, y in pairs[:best_k]:  # @line L10
            side[x], side[y] = 1, 0
    return (
        [v for v in range(n) if side[v] == 0],
        [v for v in range(n) if side[v] == 1],
    )  # @line L11
