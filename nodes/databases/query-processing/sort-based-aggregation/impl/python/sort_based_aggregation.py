# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sort-based-aggregation/. The authors are listed in prov/ZDF77H.jsonl.
"""Sort-based aggregation: external merge sort on the grouping key, with early aggregation.

The input is a file of N pages on a dbrel.Disk, with p records per page. The
memory holds B pages. Pass 0 reads B pages at a time, sorts their records on
the key and writes a sorted run. Each later pass merges B - 1 runs into one.
With early=True, every run holds one partial state per key: records with the
same key are combined when a run is formed and again in every merge. The last
merge does not write its output; it returns the final rows.

A partial state record takes the space of one input record. The cost model
counts page reads and page writes, and does not count the final output.

SQL semantics: GROUP BY puts all nulls of a column in one group; count_star
counts every row; the other aggregates skip nulls; sum, avg, min and max of
no non-null value give None. With an empty key, an empty input gives one row.
"""

import heapq
from collections.abc import Iterator, Sequence
from fractions import Fraction
from numbers import Number


def _vkey(v: object) -> tuple:
    """Sort order of one key value: None first, then numbers, then strings."""
    if v is None:
        return (0, 0)
    if isinstance(v, Number):
        return (1, v)
    if isinstance(v, str):
        return (2, v)
    return (3, repr(v))


def _kkey(k: tuple) -> tuple:
    return tuple(_vkey(v) for v in k)


# name -> (state of one value, merge two states, final answer from a state)
def _sum_merge(a: tuple, b: tuple) -> tuple:
    return (a[0] + b[0], a[1] + b[1])


def _min_merge(a: object, b: object) -> object:
    return b if a is None else a if b is None else min(a, b)


def _max_merge(a: object, b: object) -> object:
    return b if a is None else a if b is None else max(a, b)


def _avg_final(s: tuple) -> object:
    total, n = s
    if n == 0:
        return None
    if isinstance(total, (int, Fraction)):
        return Fraction(total, 1) / n
    return total / n


AGGS = {
    "count_star": (lambda v: 1, lambda a, b: a + b, lambda s: s),
    "count": (lambda v: 0 if v is None else 1, lambda a, b: a + b, lambda s: s),
    "sum": (lambda v: (0, 0) if v is None else (v, 1), _sum_merge, lambda s: s[0] if s[1] else None),
    "avg": (lambda v: (0, 0) if v is None else (v, 1), _sum_merge, _avg_final),
    "min": (lambda v: v, _min_merge, lambda s: s),
    "max": (lambda v: v, _max_merge, lambda s: s),
}


class _Run:
    """A sorted run on disk: its page ids and its number of state records."""

    def __init__(self, pages: list, size: int) -> None:
        self.pages = pages
        self.size = size


def sort_aggregate(disk, in_pages: Sequence[int], key: Sequence[int], aggs: Sequence[tuple],
                   B: int, per_page: int, early: bool = True, stats: dict | None = None) -> list:
    """Return the rows key + aggregates, sorted on the key.

    disk is a dbrel.Disk; in_pages are the page ids of the input file.
    aggs is a list of (func, column). B >= 3 is the number of buffer pages and
    per_page >= 1 the number of records in a page. If stats is a dict, it gets
    "runs" (the number of runs after each pass) and "passes".
    """
    if B < 3 or per_page < 1:
        raise ValueError("need B >= 3 and per_page >= 1")
    for f, _ in aggs:
        if f not in AGGS:
            raise ValueError("unknown aggregate %r" % (f,))
    key = list(key)
    funcs = [AGGS[f] for f, _ in aggs]

    def state(r: tuple) -> tuple:
        return (tuple(r[i] for i in key),
                [init(None if c is None else r[c]) for (init, _, _), (_, c) in zip(funcs, aggs)])

    def combine(recs) -> Iterator[tuple]:
        """Merge adjacent states with equal keys. The input is sorted on the key."""
        cur = None
        for k, st in recs:  # @line L14
            if cur is not None and cur[0] == k:  # @line L15
                cur = (k, [m(x, y) for (_, m, _), x, y in zip(funcs, cur[1], st)])  # @line L16
            else:
                if cur is not None:
                    yield cur  # @line L17
                cur = (k, list(st))
        if cur is not None:
            yield cur  # @line L18

    def finalize(recs) -> list:
        out = [k + tuple(fin(s) for (_, _, fin), s in zip(funcs, st)) for k, st in recs]
        if not key and not out:
            # A scalar aggregate of an empty input still returns one row.
            out = [tuple(fin(init(None)) if f != "count_star" else 0
                         for (init, _, fin), (f, _) in zip(funcs, aggs))]
        return out

    def write_run(recs) -> _Run:
        pages, buf, size = [], [], 0
        for rec in recs:
            buf.append(rec)
            size += 1
            if len(buf) == per_page:
                pid = disk.alloc()
                disk.write_page(pid, buf)
                pages.append(pid)
                buf = []
        if buf:
            pid = disk.alloc()
            disk.write_page(pid, buf)
            pages.append(pid)
        return _Run(pages, size)

    def scan(run: _Run) -> Iterator[tuple]:
        for pid in run.pages:  # one input buffer per run
            for rec in disk.read_page(pid):
                yield rec

    def merge(group: list) -> Iterator[tuple]:
        return heapq.merge(*[scan(r) for r in group], key=lambda rec: _kkey(rec[0]))  # @line L10

    def free(group: list) -> None:
        for r in group:
            for pid in r.pages:
                disk.free(pid)

    runs: list = []  # @line L1
    pages = list(in_pages)
    history = []
    for start in range(0, len(pages), B):  # @line L2
        recs = [state(r) for pid in pages[start:start + B] for r in disk.read_page(pid)]  # @line L3
        recs.sort(key=lambda rec: _kkey(rec[0]))  # @line L3
        if len(pages) <= B:  # @line L4
            if stats is not None:
                stats.update(runs=[], passes=1)
            return finalize(combine(recs))
        runs.append(write_run(combine(recs) if early else iter(recs)))  # @line L5 L6
    history.append(len(runs))
    while len(runs) > B - 1:  # @line L7
        new = []  # @line L8
        for start in range(0, len(runs), B - 1):  # @line L9
            group = runs[start:start + B - 1]
            merged = merge(group)
            new.append(write_run(combine(merged) if early else merged))  # @line L10 L11
            free(group)
        runs = new  # @line L12
        history.append(len(runs))
    if stats is not None:
        stats.update(runs=history, passes=len(history) + (1 if runs else 0))
    out = finalize(combine(merge(runs)))  # @line L13
    free(runs)
    return out


def sort_cost(N: int, B: int) -> int:
    """Page I/Os of sort_aggregate with early=False: 2 N P - N, where P is the number of passes."""
    if N == 0:
        return 0
    r = -(-N // B)
    passes = 1
    while r > 1:
        r = -(-r // (B - 1))
        passes += 1
    return 2 * N * passes - N
