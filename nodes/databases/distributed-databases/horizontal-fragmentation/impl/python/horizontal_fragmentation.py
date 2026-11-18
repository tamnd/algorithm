# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/horizontal-fragmentation/. The authors are listed in prov/XH9D31.jsonl.

"""Primary and derived horizontal fragmentation, and the three correctness rules.

A relation is a schema (a tuple of attribute names) and a Counter from rows to
counts, so duplicates are kept (bag semantics). A simple predicate is a
function from a row, given as a dict, to True, False or None (UNKNOWN, as in
SQL when a NULL is compared).

A minterm over the simple predicates p_1, ..., p_k fixes, for each p_i, whether
"p_i is true" or "p_i is not true". "Not true" holds when p_i is False or
UNKNOWN. With this form, every row satisfies exactly one minterm, so the
minterm fragments are complete and disjoint even when the data has NULLs. The
naive form, which uses NOT p_i, loses the rows where p_i is UNKNOWN.

A derived fragmentation of a member relation S follows a fragmentation of an
owner relation R: S_m is S semijoin R_m on the common attributes. A NULL in a
join attribute matches nothing.
"""

from __future__ import annotations

from collections import Counter
from itertools import product
from collections.abc import Callable, Mapping, Sequence

Pred = Callable[[dict], "bool | None"]


def minterms(k: int) -> list[tuple[bool, ...]]:
    """All 2^k sign vectors; True at i means "p_i is true", False means "p_i is not true"."""
    return list(product((True, False), repeat=k))


def satisfies(row: dict, preds: Sequence[Pred], m: tuple[bool, ...]) -> bool:
    return all((p(row) is True) == want for p, want in zip(preds, m))


def primary_fragments(schema: Sequence[str], rows: Counter, preds: Sequence[Pred],
                      keep_empty: bool = False) -> dict:
    """The minterm fragments of the relation: minterm -> Counter of its rows."""
    schema = tuple(schema)
    out = {}
    for m in minterms(len(preds)):  # @line L1
        frag = Counter({t: c for t, c in rows.items() if satisfies(dict(zip(schema, t)), preds, m)})  # @line L2
        if frag or keep_empty:  # @line L3
            out[m] = frag
    return out


def naive_fragments(schema: Sequence[str], rows: Counter, preds: Sequence[Pred]) -> dict:
    """The fragments with "NOT p_i" in place of "p_i is not true". They are wrong when
    a predicate can be UNKNOWN: a row with UNKNOWN p_i is in no fragment."""
    schema = tuple(schema)

    def holds(v, want):
        return v is True if want else v is False   # NOT UNKNOWN is UNKNOWN, which is not True

    out = {}
    for m in minterms(len(preds)):
        frag = Counter({t: c for t, c in rows.items()
                        if all(holds(p(dict(zip(schema, t))), w) for p, w in zip(preds, m))})
        if frag:
            out[m] = frag
    return out


def derived_fragments(member_schema: Sequence[str], member_rows: Counter, owner_schema: Sequence[str],
                      owner_fragments: Mapping) -> dict:
    """S_m = S semijoin R_m for each fragment R_m of the owner R, on the common attributes."""
    member_schema, owner_schema = tuple(member_schema), tuple(owner_schema)
    common = [a for a in member_schema if a in owner_schema]
    mi = [member_schema.index(a) for a in common]
    oi = [owner_schema.index(a) for a in common]
    out = {}
    for m, frag in owner_fragments.items():  # @line L4
        keys = {tuple(t[i] for i in oi) for t in frag}
        keys = {k for k in keys if None not in k}
        out[m] = Counter({t: c for t, c in member_rows.items() if tuple(t[i] for i in mi) in keys})  # @line L5
    return out


def reconstruct(fragments: Mapping) -> Counter:
    """The bag union of the fragments (UNION ALL)."""
    out: Counter = Counter()
    for frag in fragments.values():  # @line L6
        out.update(frag)
    return out


def is_complete(rows: Counter, fragments: Mapping) -> bool:
    """Every row of the relation, with its full count, is in the bag union of the fragments
    at least as often as in the relation."""
    union = reconstruct(fragments)
    return all(union[t] >= c for t, c in rows.items())


def is_disjoint(fragments: Mapping) -> bool:
    """No row is in two fragments."""
    seen = set()
    for frag in fragments.values():
        for t in frag:
            if t in seen:
                return False
            seen.add(t)
    return True
