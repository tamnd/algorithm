# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/parallel-pack/. The authors are listed in prov/AGKZS1.jsonl.

"""Parallel pack: flags, an exclusive +-scan, and a scatter.

Each parallel loop is simulated by a serial loop over its iterations, and
the counters record the work and the number of parallel rounds.
"""

from typing import Callable, TypeVar

T = TypeVar("T")


class Stats:
    def __init__(self) -> None:
        self.work = 0
        self.rounds = 0


def exclusive_plus_scan(f: list[int], st: Stats) -> tuple[list[int], int]:
    """Blelloch scan with +: returns (exclusive prefix sums, total)."""
    n = len(f)
    m = 1
    while m < n:
        m *= 2
    x = f + [0] * (m - n)
    d = 1
    while d < m:  # up-sweep: one round for each level
        for i in range(2 * d - 1, m, 2 * d):
            x[i] = x[i - d] + x[i]
            st.work += 1
        st.rounds += 1
        d *= 2
    total = x[m - 1]
    x[m - 1] = 0
    d = m // 2
    while d >= 1:  # down-sweep
        for i in range(2 * d - 1, m, 2 * d):
            t = x[i - d]
            x[i - d] = x[i]
            x[i] = x[i] + t
            st.work += 1
        st.rounds += 1
        d //= 2
    return x[:n], total


def pack_positions(keep: Callable[[T], bool], a: list[T], st: Stats | None = None) -> tuple[list[int], list[int], int]:
    """Returns (flags, exclusive scan of the flags, number kept)."""
    st = st if st is not None else Stats()
    n = len(a)
    flags = [1 if keep(a[i]) else 0 for i in range(n)]  # @line L1
    st.work += n
    st.rounds += 1
    x, k = exclusive_plus_scan(flags, st)  # @line L2
    return flags, x, k


def parallel_pack(keep: Callable[[T], bool], a: list[T], st: Stats | None = None) -> list[T]:
    """The items a[i] with keep(a[i]) true, in their original order."""
    st = st if st is not None else Stats()
    if not a:
        return []
    flags, x, k = pack_positions(keep, a, st)
    b: list[T | None] = [None] * k  # @line L3
    for i in range(len(a)):  # @line L4: in parallel, one round
        if flags[i] == 1:  # @line L5
            b[x[i]] = a[i]
        st.work += 1
    st.rounds += 1
    return b  # type: ignore[return-value]  # @line L6


def blocked_pack(keep: Callable[[T], bool], a: list[T], p: int) -> list[T]:
    """Pack with p blocks: count per block, scan the p counts, copy per block."""
    n = len(a)
    bounds = [(j * n // p, (j + 1) * n // p) for j in range(p)]
    counts = [sum(1 for i in range(lo, hi) if keep(a[i])) for lo, hi in bounds]
    offsets, k = exclusive_plus_scan(counts, Stats())
    b: list[T | None] = [None] * k
    for j, (lo, hi) in enumerate(bounds):  # each block in parallel
        r = offsets[j]
        for i in range(lo, hi):  # serial inside a block
            if keep(a[i]):
                b[r] = a[i]
                r += 1
    return b  # type: ignore[return-value]


def split(a: list[T], bit: Callable[[T], int]) -> list[T]:
    """Stable split: the items with bit 0, then the items with bit 1."""
    return parallel_pack(lambda v: bit(v) == 0, a) + parallel_pack(lambda v: bit(v) == 1, a)


def split_radix_sort(keys: list[int], bits: int) -> list[int]:
    """LSD radix sort of non-negative integers with one stable split per bit."""
    for b in range(bits):
        keys = split(keys, lambda v, b=b: (v >> b) & 1)
    return keys


def pack_with_inclusive_scan_wrong(keep: Callable[[T], bool], a: list[T]) -> list[T]:
    """A common bug: inclusive sums used as positions, which are off by one."""
    flags = [1 if keep(v) else 0 for v in a]
    incl, s = [], 0
    for f in flags:
        s += f
        incl.append(s)
    b: list[T | None] = [None] * s
    for i in range(len(a)):
        if flags[i]:
            b[incl[i]] = a[i]
    return b  # type: ignore[return-value]
