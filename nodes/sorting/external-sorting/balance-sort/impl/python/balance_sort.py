# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/balance-sort/. The authors are listed in prov/A6ZN06.jsonl.

from bisect import bisect_right
from typing import Any, Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: Any, /) -> bool: ...


T = TypeVar("T", bound=Ordered)


class Rec:
    """An item with its position in the input. Ties on the key go by position, so all records differ."""

    __slots__ = ("key", "pos")

    def __init__(self, key: Any, pos: int) -> None:
        self.key, self.pos = key, pos

    def __lt__(self, other: "Rec") -> bool:
        if self.key < other.key:
            return True
        if other.key < self.key:
            return False
        return self.pos < other.pos


class Stats:
    """Counts of parallel I/O steps, and the smallest share of a write step."""

    def __init__(self) -> None:
        self.ios = 0
        self.writes: list[tuple[int, int]] = []  # (blocks ready, blocks written) per write step


File = list[list[list[Rec]]]  # disk -> blocks on that disk -> items


def striped(items: list[Rec], b: int, d: int) -> File:
    """Lay out items in blocks of b, block j on disk j mod d."""
    f: File = [[] for _ in range(d)]
    for j, i in enumerate(range(0, len(items), b)):
        f[j % d].append(items[i:i + b])
    return f


def size(f: File) -> int:
    return sum(len(blk) for disk in f for blk in disk)


def read_cost(f: File) -> int:
    """Parallel reads of a whole file: one block from each disk per step."""
    return max((len(disk) for disk in f), default=0)


def place(counts: list[int], total: int, used: set[int], d: int) -> int:
    """The disk for the next block of a bucket, or -1.

    counts[e] blocks of the bucket are on disk e, total in all. A disk is
    allowed if it is not used in this write step and if after the write it
    holds at most 2 * ceil((total + 1) / d) blocks of the bucket. Among the
    allowed disks take one with the fewest blocks of the bucket.
    """
    cap = 2 * (-(-(total + 1) // d))
    best = -1
    for e in range(d):
        if e not in used and counts[e] + 1 <= cap and (best < 0 or counts[e] < counts[best]):
            best = e
    return best


def distribute(f: File, splitters: list[Rec], b: int, d: int, st: Stats) -> list[File]:
    """One distribution pass. Bucket j holds the records x with s_j <= x < s_(j+1)."""
    k = len(splitters) + 1
    out: list[File] = [[[] for _ in range(d)] for _ in range(k)]
    counts = [[0] * d for _ in range(k)]
    totals = [0] * k
    partial: list[list[Rec]] = [[] for _ in range(k)]
    ready: list[tuple[int, list[Rec]]] = []

    def write_step() -> None:  # one parallel write
        nonlocal ready
        used: set[int] = set()
        rest: list[tuple[int, list[Rec]]] = []
        for j, blk in ready:
            e = place(counts[j], totals[j], used, d) if len(used) < d else -1  # @line L7
            if e < 0:
                rest.append((j, blk))
                continue
            used.add(e)
            out[j][e].append(blk)  # @line L8
            counts[j][e] += 1
            totals[j] += 1
        st.writes.append((len(ready), len(used)))
        st.ios += 1
        ready = rest

    for step in range(read_cost(f)):  # @line L5
        st.ios += 1
        for disk in f:
            if step < len(disk):
                for x in disk[step]:
                    j = bisect_right(splitters, x)  # @line L6
                    partial[j].append(x)
                    if len(partial[j]) == b:
                        ready.append((j, partial[j]))
                        partial[j] = []
        while len(ready) >= d:
            write_step()
    for j in range(k):
        if partial[j]:
            ready.append((j, partial[j]))
    while ready:
        write_step()
    return out


def splitters_of(f: File, m: int, b: int, d: int, s: int, st: Stats) -> list[Rec]:
    """Deterministic sampling: every q-th record of each sorted memoryload, then equal ranks."""
    q = max(2, -(-m // (4 * s)))
    sample: list[Rec] = []
    load: list[Rec] = []
    blocks_per_load = m // b
    for step in range(read_cost(f)):
        st.ios += 1
        for disk in f:
            if step < len(disk):
                load.extend(disk[step])
        if len(load) >= blocks_per_load * b or step == read_cost(f) - 1:
            load.sort()
            sample.extend(load[q - 1::q])
            load = []
    if len(sample) > m:  # the sample does not fit: write it and sort it the same way
        g = striped(sample, b, d)
        st.ios += -(-(-(-len(sample) // b)) // d)
        sample = sort_file(g, m, b, d, st)
    else:
        sample.sort()
    r = max(2, len(sample) // s)
    return [sample[i * r - 1] for i in range(1, s) if i * r <= len(sample)]


def sort_file(f: File, m: int, b: int, d: int, st: Stats) -> list[Rec]:
    n = size(f)
    if n <= m:  # @line L1
        st.ios += read_cost(f)
        items = sorted(x for disk in f for blk in disk for x in blk)
        st.ios += -(-(-(-n // b)) // d)
        return items
    s = max(2, min(m // b - 2 * d, -(-4 * n // m)))  # @line L2
    sp = splitters_of(f, m, b, d, s, st)  # @line L3
    result: list[Rec] = []
    for g in distribute(f, sp, b, d, st):  # @line L4
        result.extend(sort_file(g, m, b, d, st))  # @line L9
    return result


def balance_sort(xs: list[T], m: int = 64, b: int = 4, d: int = 4, stats: "Stats | None" = None) -> int:
    """Sort xs in place with a simulated Balance Sort on d disks; return the parallel I/O steps.

    Precondition: the items are mutually comparable, b >= 1, d >= 1 and
    m >= (2d + 4) b, where m is the memory in items and b the block size.
    The sort is stable and deterministic. Each bucket ends with at most
    2 ceil(X/d) of its X blocks on any disk, and each write step writes at
    least min(ready, floor(d/2) + 1) blocks, so a level costs O(n/d) parallel
    I/Os with n = N/b, and the sort costs O((n/d) log_(m/b) n).
    """
    if b < 1 or d < 1 or m < (2 * d + 4) * b:
        raise ValueError("need b >= 1, d >= 1 and m >= (2d + 4) b")
    st = stats if stats is not None else Stats()
    recs = [Rec(x, i) for i, x in enumerate(xs)]
    out = sort_file(striped(recs, b, d), m, b, d, st)
    xs[:] = [r.key for r in out]
    return st.ios
