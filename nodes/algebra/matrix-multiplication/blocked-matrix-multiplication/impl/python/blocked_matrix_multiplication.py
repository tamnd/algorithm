# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/blocked-matrix-multiplication/. The authors are listed in prov/4VVM7H.jsonl.

from collections import OrderedDict
from typing import Iterator, Optional

Matrix = list[list[int]]


def blocked_matrix_multiplication(a: Matrix, b: Matrix, p: Optional[int] = None,
                                  mod: Optional[int] = None, tile: int = 32) -> Matrix:
    """Return a * b, computed tile by tile with square tiles of side `tile`.

    a is n x m and b is m x p (lists of rows); pass p when m = 0. The ring is
    Z, or Z/mod Z when mod is set. Edge tiles are smaller when a side is not a
    multiple of `tile`. Cost: n m p multiplications and additions, as for the
    triple loop; only the order of the operations changes.
    """
    if tile < 1:
        raise ValueError("the tile side must be at least 1")
    n, m = len(a), len(b)
    if p is None:
        p = len(b[0]) if m > 0 else 0
    if any(len(row) != m for row in a) or any(len(row) != p for row in b):
        raise ValueError("the shapes do not match")
    c = [[0] * p for _ in range(n)]
    for i0 in range(0, n, tile):  # @line L1
        i1 = min(i0 + tile, n)
        for j0 in range(0, p, tile):  # @line L2
            j1 = min(j0 + tile, p)
            ct = [c[i][j0:j1] for i in range(i0, i1)]  # @line L3
            for k0 in range(0, m, tile):  # @line L4
                k1 = min(k0 + tile, m)
                at = [a[i][k0:k1] for i in range(i0, i1)]  # @line L5
                bt = [b[k][j0:j1] for k in range(k0, k1)]
                for ii, arow in enumerate(at):  # @line L6
                    crow = ct[ii]
                    for kk, aik in enumerate(arow):
                        if aik:
                            brow = bt[kk]
                            for jj in range(j1 - j0):
                                crow[jj] += aik * brow[jj]
                if mod is not None:
                    ct = [[x % mod for x in row] for row in ct]
            for ii, i in enumerate(range(i0, i1)):  # @line L7
                c[i][j0:j1] = ct[ii]
    return c


def _lines(base: int, ld: int, r0: int, r1: int, c0: int, c1: int, line: int) -> set[int]:
    """Indices of the memory blocks of `line` words touched by rows r0..r1-1, columns c0..c1-1
    of a row-major matrix that starts at word `base` and has `ld` words per row."""
    out: set[int] = set()
    if c1 <= c0:
        return out
    for r in range(r0, r1):
        first, last = base + r * ld + c0, base + r * ld + c1 - 1
        out.update(range(first // line, last // line + 1))
    return out


def explicit_transfers(n: int, m: int, p: int, tile: int, line: int) -> int:
    """Block transfers of the tiled schedule in the external memory model.

    A, B and C are row-major and stored one after the other. Each tile of C is
    read once and written once, and each pair of tiles of A and B is read once
    for each tile of C, as in lines L3, L5 and L7. Memory needs room for three tiles.
    """
    base_a, base_b, base_c = 0, n * m, n * m + m * p
    total = 0
    for i0 in range(0, n, tile):
        i1 = min(i0 + tile, n)
        for j0 in range(0, p, tile):
            j1 = min(j0 + tile, p)
            total += 2 * len(_lines(base_c, p, i0, i1, j0, j1, line))
            for k0 in range(0, m, tile):
                k1 = min(k0 + tile, m)
                total += len(_lines(base_a, m, i0, i1, k0, k1, line))
                total += len(_lines(base_b, p, k0, k1, j0, j1, line))
    return total


def _trace(n: int, tile: Optional[int]) -> Iterator[int]:
    """Word addresses read by the n x n product in loop order i, k, j (tile=None) or tiled."""
    base_b, base_c = n * n, 2 * n * n
    t = n if tile is None else tile
    for i0 in range(0, n, t):
        for j0 in range(0, n, t):
            for k0 in range(0, n, t):
                for i in range(i0, min(i0 + t, n)):
                    for k in range(k0, min(k0 + t, n)):
                        yield i * n + k
                        for j in range(j0, min(j0 + t, n)):
                            yield base_b + k * n + j
                            yield base_c + i * n + j


def lru_misses(n: int, line: int, cache_words: int, tile: Optional[int] = None) -> int:
    """Misses of a fully associative LRU cache of cache_words words and lines of `line` words,
    for the n x n product in loop order i, k, j (tile=None) or with square tiles of side `tile`."""
    cap = cache_words // line
    cache: OrderedDict[int, None] = OrderedDict()
    misses = 0
    for addr in _trace(n, tile):
        blk = addr // line
        if blk in cache:
            cache.move_to_end(blk)
        else:
            misses += 1
            cache[blk] = None
            if len(cache) > cap:
                cache.popitem(last=False)
    return misses
