# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/group-by-aggregation/. The authors are listed in prov/KFFKTB.jsonl.

"""Group-by aggregation by sorting, with the three classes of aggregates.

sort_group_by sorts the rows on the grouping key and aggregates each run of
equal keys in one scan. Each aggregate is given by three functions in the style
of Gray et al. (1997): init makes a partial state from one value, merge joins
two partial states, and final turns a state into the answer. For a distributive
aggregate the state is the answer itself; for an algebraic one it is a tuple of
fixed size (AVG keeps (sum, count)); for a holistic one it must keep all values.

sort_aggregate_io gives the page I/O of the sort-based plan with B buffer pages.
"""

from collections.abc import Callable, Hashable, Iterable, Sequence
from fractions import Fraction


def _lower_median(vals: list) -> object:
    s = sorted(vals)
    return s[(len(s) - 1) // 2]


# name -> (class, init, merge, final)
AGGREGATES: dict[str, tuple[str, Callable, Callable, Callable]] = {
    "count": ("distributive", lambda v: 1, lambda a, b: a + b, lambda s: s),
    "sum": ("distributive", lambda v: v, lambda a, b: a + b, lambda s: s),
    "min": ("distributive", lambda v: v, min, lambda s: s),
    "max": ("distributive", lambda v: v, max, lambda s: s),
    "avg": ("algebraic", lambda v: (v, 1), lambda a, b: (a[0] + b[0], a[1] + b[1]),
            lambda s: Fraction(s[0], s[1])),
    "median": ("holistic", lambda v: [v], lambda a, b: a + b, _lower_median),
    "count_distinct": ("holistic", lambda v: {v}, lambda a, b: a | b, len),
}


def aggregate_values(name: str, vals: Iterable) -> object:
    """Apply one aggregate to a non-empty sequence of values."""
    _, init, merge, final = AGGREGATES[name]
    state = None
    for v in vals:
        state = init(v) if state is None else merge(state, init(v))
    return final(state)


def sort_group_by(rows: Sequence[tuple], key: Sequence[int],
                  aggs: Sequence[tuple[str, int]]) -> list[tuple[tuple, tuple]]:
    """Group rows on the columns in key, and apply each (aggregate, column).

    Returns a list of (key value, aggregate values), in increasing key order.
    Only groups with at least one row appear: this is SQL GROUP BY, which has
    no empty groups.
    """
    def kf(r: tuple) -> tuple:
        return tuple(r[i] for i in key)

    srt = sorted(rows, key=kf)
    out: list[tuple[tuple, tuple]] = []
    i = 0
    while i < len(srt):
        k = kf(srt[i])
        states = [AGGREGATES[a][1](srt[i][c]) for a, c in aggs]
        j = i + 1
        while j < len(srt) and kf(srt[j]) == k:
            for t, (a, c) in enumerate(aggs):
                states[t] = AGGREGATES[a][2](states[t], AGGREGATES[a][1](srt[j][c]))
            j += 1
        out.append((k, tuple(AGGREGATES[a][3](s) for s, (a, _) in zip(states, aggs))))
        i = j
    return out


def combine_partitions(parts: Sequence[Sequence[Hashable]], name: str) -> object:
    """Aggregate each part to a state, then merge the states (the partial plan).

    This is correct for every aggregate in AGGREGATES because the state of a
    holistic aggregate keeps all values; the point is the size of the state.
    """
    _, init, merge, final = AGGREGATES[name]
    total = None
    for part in parts:
        st = None
        for v in part:
            st = init(v) if st is None else merge(st, init(v))
        if st is not None:
            total = st if total is None else merge(total, st)
    return final(total)


def sort_aggregate_io(n_pages: int, b: int) -> tuple[int, int]:
    """Page I/Os of sort-based aggregation with b >= 3 buffer pages.

    External merge sort makes ceil(N/B) runs in pass 0, then merges B - 1 runs
    at a time. The last pass aggregates while it merges, so it reads but does
    not write. The output is not counted. Returns (passes, I/Os).
    """
    if b < 3:
        raise ValueError("need at least 3 buffer pages")
    if n_pages <= b:
        return 1, n_pages
    runs = -(-n_pages // b)
    passes = 1
    while runs > 1:
        runs = -(-runs // (b - 1))
        passes += 1
    return passes, 2 * n_pages * passes - n_pages
