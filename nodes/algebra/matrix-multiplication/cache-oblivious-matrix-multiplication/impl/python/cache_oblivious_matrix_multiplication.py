# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cache-oblivious-matrix-multiplication/. The authors are listed in prov/M2GPXZ.jsonl.

from collections import OrderedDict
from typing import Callable, Optional

Matrix = list[list[int]]


def cache_oblivious_matrix_multiplication(a: Matrix, b: Matrix, p: Optional[int] = None,
                                          mod: Optional[int] = None, base: int = 1) -> Matrix:
    """Return a * b by halving the largest of the three dimensions recursively.

    a is m x n and b is n x p (lists of rows); pass p when n = 0. The ring is
    Z, or Z/mod Z when mod is set; commutativity is not used. Subproblems with
    all three sides at most `base` use the triple loop. Cost: m n p
    multiplications; recursion depth at most lg m + lg n + lg p + 3.
    """
    if base < 1:
        raise ValueError("the base size must be at least 1")
    m, n = len(a), len(b)
    if p is None:
        p = len(b[0]) if n > 0 else 0
    if any(len(row) != n for row in a) or any(len(row) != p for row in b):
        raise ValueError("the shapes do not match")
    c = [[0] * p for _ in range(m)]
    if m and n and p:
        _rec(a, b, c, 0, m, 0, n, 0, p, base)
    if mod is not None:
        c = [[x % mod for x in row] for row in c]
    return c


def _rec(a: Matrix, b: Matrix, c: Matrix, i0: int, i1: int, k0: int, k1: int,
         j0: int, j1: int, base: int) -> None:
    """C[i0:i1, j0:j1] += A[i0:i1, k0:k1] * B[k0:k1, j0:j1]."""
    m, n, p = i1 - i0, k1 - k0, j1 - j0
    if max(m, n, p) <= base:  # @line L1
        for i in range(i0, i1):
            ai, ci = a[i], c[i]
            for k in range(k0, k1):
                aik, bk = ai[k], b[k]
                for j in range(j0, j1):
                    ci[j] += aik * bk[j]
        return
    if m >= n and m >= p:  # @line L2
        h = i0 + m // 2
        _rec(a, b, c, i0, h, k0, k1, j0, j1, base)
        _rec(a, b, c, h, i1, k0, k1, j0, j1, base)
    elif n >= p:  # @line L3
        h = k0 + n // 2
        _rec(a, b, c, i0, i1, k0, h, j0, j1, base)
        _rec(a, b, c, i0, i1, h, k1, j0, j1, base)
    else:  # @line L4
        h = j0 + p // 2
        _rec(a, b, c, i0, i1, k0, k1, j0, h, base)
        _rec(a, b, c, i0, i1, k0, k1, h, j1, base)


def recursion_depth(m: int, n: int, p: int, base: int = 1) -> int:
    """Depth of the recursion tree of the method on an m x n by n x p product."""
    if max(m, n, p) <= base:
        return 0
    if m >= n and m >= p:
        return 1 + recursion_depth(m - m // 2, n, p, base)
    if n >= p:
        return 1 + recursion_depth(m, n - n // 2, p, base)
    return 1 + recursion_depth(m, n, p - p // 2, base)


def _trace(n: int, base: int, emit: Callable[[int], None]) -> None:
    """Word addresses read by the recursive method on n x n row-major matrices A, B, C."""
    off_b, off_c = n * n, 2 * n * n

    def rec(i0: int, i1: int, k0: int, k1: int, j0: int, j1: int) -> None:
        m, q, p = i1 - i0, k1 - k0, j1 - j0
        if max(m, q, p) <= base:
            for i in range(i0, i1):
                for k in range(k0, k1):
                    emit(i * n + k)
                    for j in range(j0, j1):
                        emit(off_b + k * n + j)
                        emit(off_c + i * n + j)
            return
        if m >= q and m >= p:
            h = i0 + m // 2
            rec(i0, h, k0, k1, j0, j1)
            rec(h, i1, k0, k1, j0, j1)
        elif q >= p:
            h = k0 + q // 2
            rec(i0, i1, k0, h, j0, j1)
            rec(i0, i1, h, k1, j0, j1)
        else:
            h = j0 + p // 2
            rec(i0, i1, k0, k1, j0, h)
            rec(i0, i1, k0, k1, h, j1)

    rec(0, n, 0, n, 0, n)


def lru_misses(n: int, line: int, cache_words: int, base: int = 1) -> int:
    """Misses of a fully associative LRU cache with cache_words words and lines of
    `line` words, for the recursive method on n x n row-major matrices."""
    cap = cache_words // line
    cache: OrderedDict[int, None] = OrderedDict()
    misses = 0

    def emit(addr: int) -> None:
        nonlocal misses
        blk = addr // line
        if blk in cache:
            cache.move_to_end(blk)
        else:
            misses += 1
            cache[blk] = None
            if len(cache) > cap:
                cache.popitem(last=False)

    _trace(n, base, emit)
    return misses
