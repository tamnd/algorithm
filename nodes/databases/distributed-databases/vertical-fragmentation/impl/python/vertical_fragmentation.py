# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/vertical-fragmentation/. The authors are listed in prov/XEF5EY.jsonl.

"""Vertical fragmentation by projections that keep the key, and reconstruction by a join.

A relation is a schema (a tuple of attribute names) and a Counter from rows to
counts. A vertical fragmentation with key K and groups G_1, ..., G_n of the
other attributes has the fragments pi_{K u G_i}(R). It is complete when every
attribute is in some fragment, and disjoint when no attribute other than K is
in two fragments. It reconstructs R by a join of the fragments on K.

The join is lossless when K is a key of R: no NULL in K and no two rows with
the same K. A bag with duplicate rows has no key; with_tuple_id adds a
surrogate key, a tuple id, that makes the rows distinct first.
"""

from __future__ import annotations

from collections import Counter
from collections.abc import Sequence


def is_key(schema: Sequence[str], rows: Counter, key: Sequence[str]) -> bool:
    """K is a key of this instance: no NULL in K and no two rows (or copies) share K."""
    ki = [tuple(schema).index(a) for a in key]
    seen = set()
    for t, c in rows.items():
        k = tuple(t[i] for i in ki)
        if None in k or c > 1 or k in seen:
            return False
        seen.add(k)
    return True


def fragment(schema: Sequence[str], rows: Counter, key: Sequence[str], groups: Sequence[Sequence[str]]) -> list:
    """The fragments (schema_i, rows_i), with schema_i = K followed by G_i."""
    schema, key = tuple(schema), tuple(key)
    out = []
    for g in groups:  # @line L1
        fs = key + tuple(a for a in g if a not in key)
        pos = [schema.index(a) for a in fs]
        proj: Counter = Counter()
        for t, c in rows.items():
            proj[tuple(t[i] for i in pos)] += c  # @line L2
        out.append((fs, proj))
    return out


def reconstruct(fragments: Sequence[tuple], key: Sequence[str], schema: Sequence[str]) -> Counter:
    """The join of the fragments on K, with the columns put back in the order of schema.
    The join is a hash join on K; a NULL in K matches nothing."""
    key, schema = tuple(key), tuple(schema)
    cur_schema, cur = fragments[0]
    for fs, rows in fragments[1:]:  # @line L3
        common = [a for a in cur_schema if a in fs]
        rest = [a for a in fs if a not in common]
        table: dict = {}
        for t, c in rows.items():
            k = tuple(t[fs.index(a)] for a in common)
            if None not in k:
                table.setdefault(k, []).append((t, c))
        out: Counter = Counter()
        for t, c in cur.items():  # @line L4
            k = tuple(t[cur_schema.index(a)] for a in common)
            for u, d in table.get(k, ()):
                out[t + tuple(u[fs.index(a)] for a in rest)] += c * d
        cur_schema, cur = cur_schema + tuple(rest), out
    pos = [cur_schema.index(a) for a in schema]
    return Counter({tuple(t[i] for i in pos): c for t, c in cur.items()})  # @line L5


def is_complete(schema: Sequence[str], fragments: Sequence[tuple]) -> bool:
    return set(schema) <= {a for fs, _ in fragments for a in fs}


def is_disjoint(key: Sequence[str], fragments: Sequence[tuple]) -> bool:
    seen = set()
    for fs, _ in fragments:
        for a in fs:
            if a in key:
                continue
            if a in seen:
                return False
            seen.add(a)
    return True


def with_tuple_id(schema: Sequence[str], rows: Counter, name: str = "tid") -> tuple:
    """Give each copy of each row its own id: the result has the key (name,)."""
    out: Counter = Counter()
    n = 0
    for t in sorted(rows, key=repr):
        for _ in range(rows[t]):
            out[(n,) + t] = 1
            n += 1
    return (name,) + tuple(schema), out
