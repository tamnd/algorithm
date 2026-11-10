# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/parallel-reduce/. The authors are listed in prov/7TMWGJ.jsonl.

"""Parallel reduce in the work-span model.

The fork-join version runs the spawned call before the other call, which is
a legal schedule of the parallel program. Each function returns the result
together with the work and the span, counted in applications of the
operator: the work is the number of applications, and the span is the
largest number of applications on one path from an input to the result.
"""

from typing import Callable, TypeVar

T = TypeVar("T")


def parallel_reduce(op: Callable[[T, T], T], identity: T, a: list[T]) -> tuple[T, int, int]:
    """Return (a[0] op a[1] op ... op a[n-1], work, span), or (identity, 0, 0) for n = 0."""
    if not a:  # @line L7
        return identity, 0, 0
    return _reduce(op, a, 0, len(a))  # @line L8


def _reduce(op: Callable[[T, T], T], a: list[T], lo: int, hi: int) -> tuple[T, int, int]:
    """Reduce a[lo:hi] with hi - lo >= 1 by a balanced tree."""
    if hi - lo == 1:  # @line L1
        return a[lo], 0, 0
    mid = lo + (hi - lo + 1) // 2  # @line L2: the left part has ceil((hi - lo) / 2) items
    x, wx, sx = _reduce(op, a, lo, mid)  # @line L3: spawned
    y, wy, sy = _reduce(op, a, mid, hi)  # @line L4
    span = max(sx, sy)  # @line L5: sync waits for the longer branch
    return op(x, y), wx + wy + 1, span + 1  # @line L6: left operand first


def reduce_rounds(op: Callable[[T, T], T], identity: T, a: list[T]) -> tuple[T, int, int]:
    """The same tree computed level by level.

    Each round combines adjacent pairs; an odd last item moves up unchanged.
    The combines of one round are independent, so one round is one step of
    span. Returns (result, work, rounds).
    """
    if not a:
        return identity, 0, 0
    level = list(a)
    work = rounds = 0
    while len(level) > 1:
        pairs = len(level) // 2
        nxt = [op(level[2 * i], level[2 * i + 1]) for i in range(pairs)]  # parallel
        if len(level) % 2 == 1:
            nxt.append(level[-1])
        work += pairs
        rounds += 1
        level = nxt
    return level[0], work, rounds
