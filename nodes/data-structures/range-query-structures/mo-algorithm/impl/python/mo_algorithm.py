# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mo-algorithm/. The authors are listed in prov/S9FYEP.jsonl.

import math
from typing import Callable, Hashable, Sequence, TypeVar

T = TypeVar("T")


def default_block(n: int, q: int) -> int:
    """The block size max(1, min(n, ceil(n / sqrt(q))))."""
    if n <= 0 or q <= 0:
        return 1
    s = math.isqrt(q)
    if s * s < q:
        s += 1
    return max(1, min(n, -(-n // s)))


def mo_algorithm(
    n: int,
    queries: Sequence[tuple[int, int]],
    add: Callable[[int], None],
    remove: Callable[[int], None],
    answer: Callable[[], T],
    block: int = 0,
) -> list[T]:
    """Answer offline window queries [l, r) over positions 0..n-1.

    Precondition: 0 <= l <= r <= n for each query; add(i) puts position i
    into the window, remove(i) takes it out, and answer() reads the value
    of the current window. block <= 0 picks ceil(n / sqrt(q)).
    Cost: O(n sqrt(q)) calls of add and remove, plus O(q log q) to sort.
    """
    q = len(queries)
    b = block if block > 0 else default_block(n, q)
    order = sorted(range(q), key=lambda j: (queries[j][0] // b, queries[j][1]))  # @line L1
    cur_l = cur_r = 0  # @line L2
    ans: list[T] = [None] * q  # type: ignore[list-item]
    for j in order:  # @line L3
        l, r = queries[j]
        while cur_l > l:  # @line L4
            cur_l -= 1
            add(cur_l)
        while cur_r < r:  # @line L5
            add(cur_r)
            cur_r += 1
        while cur_l < l:  # @line L6
            remove(cur_l)
            cur_l += 1
        while cur_r > r:  # @line L7
            cur_r -= 1
            remove(cur_r)
        ans[j] = answer()  # @line L8
    return ans  # @line L9


def distinct_counts(a: Sequence[Hashable], queries: Sequence[tuple[int, int]], block: int = 0) -> list[int]:
    """The number of distinct values of a[l:r] for each query (l, r).

    Precondition: 0 <= l <= r <= len(a). Cost: O(n sqrt(q) + q log q)
    expected time with a hash map of counts, O(n + q) extra space.
    """
    cnt: dict[Hashable, int] = {}
    d = 0

    def add(i: int) -> None:
        nonlocal d
        c = cnt.get(a[i], 0)
        if c == 0:
            d += 1
        cnt[a[i]] = c + 1

    def remove(i: int) -> None:
        nonlocal d
        c = cnt[a[i]] - 1
        if c < 0:
            raise ValueError("remove of an item that is not in the window")
        if c == 0:
            d -= 1
        cnt[a[i]] = c

    return mo_algorithm(len(a), queries, add, remove, lambda: d, block)
