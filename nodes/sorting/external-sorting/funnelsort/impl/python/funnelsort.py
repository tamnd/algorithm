# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/funnelsort/. The authors are listed in prov/VCKGXK.jsonl.

import math
from collections import deque
from typing import Generic, Optional, Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: "Ordered", /) -> bool: ...


T = TypeVar("T", bound=Ordered)

BASE = 8


class Node(Generic[T]):
    """A node of a lazy funnel: a leaf holds an input run, an inner node a bounded buffer."""

    __slots__ = ("buf", "cap", "left", "right", "done")

    def __init__(self, left: "Optional[Node[T]]" = None, right: "Optional[Node[T]]" = None) -> None:
        self.buf: deque[T] = deque()
        self.cap = 0
        self.left, self.right = left, right
        self.done = left is None  # a leaf is complete once its run is loaded


def build_funnel(runs: list[list[T]]) -> Node[T]:
    """A complete binary funnel with the runs as leaves, padded with empty runs.

    The buffer sizes follow the rule of Frigo et al.: a funnel with k = 2^h
    leaves is a top funnel of height h // 2 and bottom funnels of height
    h - h // 2, and the buffers between them hold ceil(k^(3/2)) items. The
    same rule applies inside the top and the bottom funnels.
    """
    h = 0
    while (1 << h) < len(runs):
        h += 1
    level: list[Node[T]] = []
    for i in range(1 << h):
        leaf: Node[T] = Node()
        if i < len(runs):
            leaf.buf.extend(runs[i])
        level.append(leaf)
    while len(level) > 1:
        level = [Node(level[i], level[i + 1]) for i in range(0, len(level), 2)]
    root = level[0]

    def assign(v: Node[T], height: int) -> None:
        if height <= 1:
            return
        top = height // 2
        cap = math.isqrt((1 << height) ** 3 - 1) + 1  # ceil(k^(3/2)), k = 2^height
        frontier = [v]
        for _ in range(top):
            frontier = [c for u in frontier for c in (u.left, u.right) if c is not None]
        for u in frontier:
            if u.left is not None:
                u.cap = cap
            assign(u, height - top)
        assign(v, top)

    assign(root, h)
    return root


def fill(v: Node[T]) -> None:
    """Fill the buffer of v from its children, filling a child whenever its buffer is empty."""
    assert v.left is not None and v.right is not None
    kids = (v.left, v.right)
    while len(v.buf) < v.cap:  # @line L6
        for c in kids:  # @line L7
            if not c.buf and not c.done:
                fill(c)
        live = [c for c in kids if c.buf]
        if not live:  # @line L8
            v.done = True
            return
        c = live[0] if len(live) == 1 or not live[1].buf[0] < live[0].buf[0] else live[1]
        v.buf.append(c.buf.popleft())  # @line L9


def funnelsort(xs: list[T]) -> None:
    """Sort xs in place with funnelsort, a cache-oblivious stable merge sort.

    Precondition: the items are mutually comparable. The algorithm does not know
    the cache size M or the line size B. With a tall cache, M = Omega(B^2), it
    makes O((N/B) log_M N) cache misses; the work is O(N log N).
    """
    n = len(xs)
    if n <= BASE:  # @line L1
        for i in range(1, n):
            x, j = xs[i], i
            while j > 0 and x < xs[j - 1]:
                xs[j] = xs[j - 1]
                j -= 1
            xs[j] = x
        return
    k = 1
    while k ** 3 < n:  # @line L2
        k += 1
    size = -(-n // k)
    parts = [xs[i:i + size] for i in range(0, n, size)]
    for p in parts:  # @line L3
        funnelsort(p)
    root = build_funnel(parts)  # @line L4
    root.cap = n
    fill(root)
    xs[:] = list(root.buf)  # @line L5
