# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mo-algorithm-with-updates/. The authors are listed in prov/XFPAYN.jsonl.

from typing import Callable, Hashable, Sequence, TypeVar

T = TypeVar("T")
V = TypeVar("V")


def default_block(n: int) -> int:
    """The block size max(1, ceil(n^(2/3)))."""
    b = 1
    while b * b * b < n * n:
        b += 1
    return max(1, b)


def mo_with_updates(
    a: Sequence[V],
    queries: Sequence[tuple[int, int, int]],
    updates: Sequence[tuple[int, V]],
    add: Callable[[V], None],
    remove: Callable[[V], None],
    answer: Callable[[], T],
    block: int = 0,
) -> list[T]:
    """Answer offline window queries (l, r, t) on the array after t updates.

    A query (l, r, t) asks about a[l:r] after the first t updates of
    updates have been applied; an update (p, x) sets a[p] = x. add(x) and
    remove(x) put the value x into the window or take it out, and answer()
    reads the window. block <= 0 picks ceil(n^(2/3)).
    Cost: O(q B + n^2 / B + m n^2 / B^2) calls of add and remove for q
    queries and m updates, plus O(q log q) to sort.
    """
    arr = list(a)
    upd = [list(u) for u in updates]
    n, q = len(arr), len(queries)
    b = block if block > 0 else default_block(n)
    order = sorted(range(q), key=lambda j: (queries[j][0] // b, queries[j][1] // b, queries[j][2]))  # @line L2
    cur_l = cur_r = cur_t = 0  # @line L3
    ans: list[T] = [None] * q  # type: ignore[list-item]

    def apply(j: int) -> None:
        p = upd[j][0]  # @line L10
        inside = cur_l <= p < cur_r
        if inside:  # @line L11
            remove(arr[p])
        arr[p], upd[j][1] = upd[j][1], arr[p]  # @line L12
        if inside:  # @line L13
            add(arr[p])

    for j in order:  # @line L4
        l, r, t = queries[j]
        while cur_t < t:  # @line L5
            apply(cur_t)
            cur_t += 1
        while cur_t > t:  # @line L6
            cur_t -= 1
            apply(cur_t)
        while cur_l > l:  # @line L7
            cur_l -= 1
            add(arr[cur_l])
        while cur_r < r:
            add(arr[cur_r])
            cur_r += 1
        while cur_l < l:
            remove(arr[cur_l])
            cur_l += 1
        while cur_r > r:
            cur_r -= 1
            remove(arr[cur_r])
        ans[j] = answer()  # @line L8
    return ans  # @line L9


def distinct_counts_with_updates(a: Sequence[Hashable], ops: Sequence[tuple[str, int, object]]) -> list[int]:
    """Answers of ("Q", l, r) operations, the number of distinct values of
    a[l:r], interleaved with ("U", p, x) operations that set a[p] = x."""
    queries: list[tuple[int, int, int]] = []
    updates: list[tuple[int, Hashable]] = []
    for kind, u, w in ops:  # @line L1
        if kind == "U":
            if not 0 <= u < len(a):
                raise IndexError(f"update position {u} out of range")
            updates.append((u, w))  # type: ignore[arg-type]
        else:
            r = int(w)  # type: ignore[call-overload]
            if not 0 <= u <= r <= len(a):
                raise IndexError(f"bad range [{u}, {r})")
            queries.append((u, r, len(updates)))
    count: dict[Hashable, int] = {}
    distinct = [0]

    def add(x: Hashable) -> None:
        c = count.get(x, 0)
        if c == 0:
            distinct[0] += 1
        count[x] = c + 1

    def remove(x: Hashable) -> None:
        c = count[x] - 1
        count[x] = c
        if c == 0:
            distinct[0] -= 1

    return mo_with_updates(a, queries, updates, add, remove, lambda: distinct[0])
