# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/generic-backtracking-algorithm/. The authors are listed in prov/BD5KA9.jsonl.

from collections.abc import Callable, Iterable, Iterator
from typing import TypeVar

T = TypeVar("T")

_DONE = object()


def backtrack(
    n: int,
    candidates: Callable[[tuple[T, ...]], Iterable[T]],
    accept: Callable[[tuple[T, ...]], bool],
) -> Iterator[tuple[T, ...]]:
    """Yield each sequence x_1 .. x_n that passes the test on every prefix.

    candidates(prefix) gives the ordered candidates for the next decision.
    accept(prefix) is the test P_k on a nonempty prefix. The sequences come
    in lexicographic order of the candidate orders. The recursion of the
    pseudocode is run with an explicit stack, so a large n does not overflow
    the Python call stack. Time: O(T d) calls of accept, where T is the number
    of prefixes that pass and d bounds the number of candidates. Extra space:
    O(n) besides the candidate iterators.
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    x: list[T] = []
    # One frame per active call of BACKTRACK(x, k), with k = len(x).
    # A frame is None before the call has run line L1, else the candidate iterator.
    stack: list[Iterator[T] | None] = [None]
    while stack:
        frame = stack[-1]
        if frame is None:
            if len(x) == n:  # @line L1
                yield tuple(x)  # @line L2
                stack.pop()  # @line L3
                if x:
                    x.pop()  # @line L8
                continue
            stack[-1] = iter(candidates(tuple(x)))
            continue
        c = next(frame, _DONE)  # @line L4
        if c is _DONE:
            stack.pop()
            if stack:
                x.pop()  # @line L8
            continue
        x.append(c)  # @line L5
        if accept(tuple(x)):  # @line L6
            stack.append(None)  # @line L7
        else:
            x.pop()  # @line L8


def count_nodes(
    n: int,
    candidates: Callable[[tuple[T, ...]], Iterable[T]],
    accept: Callable[[tuple[T, ...]], bool],
) -> list[int]:
    """Return the number of reachable prefixes of each length 0 .. n."""
    counts = [0] * (n + 1)

    def counting_accept(prefix: tuple[T, ...]) -> bool:
        ok = accept(prefix)
        if ok:
            counts[len(prefix)] += 1
        return ok

    counts[0] = 1
    for _ in backtrack(n, candidates, counting_accept):
        pass
    return counts


def n_queens(n: int) -> list[tuple[int, ...]]:
    """All placements of n non-attacking queens, as tuples of columns 1 .. n by row."""

    def no_attack(p: tuple[int, ...]) -> bool:
        k = len(p) - 1
        return all(p[i] != p[k] and abs(p[i] - p[k]) != k - i for i in range(k))

    return list(backtrack(n, lambda p: range(1, n + 1), no_attack))
