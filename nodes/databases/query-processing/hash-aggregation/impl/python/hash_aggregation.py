# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hash-aggregation/. The authors are listed in prov/ET3B5B.jsonl.

"""Hash aggregation with a bounded table, spilling to hash partitions.

The table maps a group key to a partial state, and holds at most mem_groups
keys. A row whose key is in the table updates that state at once (early
aggregation). When the table is full, a row of a new key is turned into a
state and appended to one of fanout partitions, chosen by a hash of the key
and the recursion level. After the scan the table is output, and each
partition is aggregated the same way, with a new hash function. Spilled
records are partial states, so a partition merges states, not raw rows.

The "disk" is a list of partitions; stats counts the records written to it.
"""

import zlib
from collections.abc import Hashable, Sequence
from fractions import Fraction

# name -> (init from a value, merge two states, final answer)
AGGS = {
    "count": (lambda v: 1, lambda a, b: a + b, lambda s: s),
    "sum": (lambda v: v, lambda a, b: a + b, lambda s: s),
    "min": (lambda v: v, min, lambda s: s),
    "max": (lambda v: v, max, lambda s: s),
    "avg": (lambda v: (v, 1), lambda a, b: (a[0] + b[0], a[1] + b[1]),
            lambda s: Fraction(s[0], s[1])),
}


def _bucket(key: Hashable, level: int, fanout: int) -> int:
    """A hash that does not depend on PYTHONHASHSEED, different at each level."""
    return zlib.crc32(repr((level, key)).encode()) % fanout


def hash_aggregate(rows: Sequence[tuple], key: Sequence[int], aggs: Sequence[tuple[str, int]],
                   mem_groups: int, fanout: int = 4, stats: dict | None = None) -> dict:
    """Return a dict from group key to the tuple of aggregate values.

    mem_groups >= 1 is the most keys the in-memory table may hold.
    """
    if mem_groups < 1 or fanout < 2:
        raise ValueError("need mem_groups >= 1 and fanout >= 2")
    if stats is not None:
        stats.update(spilled=0, levels=0)
    inits = [AGGS[a][0] for a, _ in aggs]
    merges = [AGGS[a][1] for a, _ in aggs]
    # Turn each row into (key, states); level 0 reads the input.
    first = [(tuple(r[i] for i in key), [f(r[c]) for f, (_, c) in zip(inits, aggs)]) for r in rows]
    out: dict = {}
    work = [(first, 0)]  # @line L1
    while work:  # @line L2
        recs, level = work.pop()  # @line L3
        if stats is not None:
            stats["levels"] = max(stats["levels"], level + 1)
        table: dict = {}  # @line L4
        parts: list[list] = [[] for _ in range(fanout)]
        for k, st in recs:  # @line L5
            cur = table.get(k)
            if cur is not None:  # @line L6
                table[k] = [m(x, y) for m, x, y in zip(merges, cur, st)]
            elif len(table) < mem_groups:  # @line L7
                table[k] = list(st)
            else:  # @line L8
                parts[_bucket(k, level, fanout)].append((k, st))
                if stats is not None:
                    stats["spilled"] += 1
        for k, st in table.items():  # @line L9
            out[k] = tuple(AGGS[a][2](s) for s, (a, _) in zip(st, aggs))
        for p in parts:  # @line L10
            if p:  # @line L11
                work.append((p, level + 1))
    return out
