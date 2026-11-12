# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/functional-dependency/. The authors are listed in prov/61TNHC.jsonl.

"""Check whether a functional dependency X -> Y holds in a relation.

A relation is a list of tuples, each a dict from attribute names to values.
holds() puts each tuple into a hash table keyed by its X-values and stores
the Y-values seen for that key. A second tuple with the same X-values and
different Y-values is a violation. This takes O(n (|X| + |Y|)) expected time
for n tuples. holds_pairwise() is the O(n^2) definition, kept as a reference.
"""

from collections.abc import Hashable, Mapping, Sequence

Row = Mapping[Hashable, Hashable]


def violation(rel: Sequence[Row], x: Sequence[Hashable], y: Sequence[Hashable]) -> tuple[int, int] | None:
    """Return positions (i, j), i < j, of two tuples that agree on X but not on Y, or None."""
    seen: dict[tuple, tuple[tuple, int]] = {}
    for j, t in enumerate(rel):
        key = tuple(t[a] for a in x)
        val = tuple(t[a] for a in y)
        if key in seen:
            first_val, i = seen[key]
            if first_val != val:
                return (i, j)
        else:
            seen[key] = (val, j)
    return None


def holds(rel: Sequence[Row], x: Sequence[Hashable], y: Sequence[Hashable]) -> bool:
    """True when every two tuples that agree on X also agree on Y."""
    return violation(rel, x, y) is None


def holds_pairwise(rel: Sequence[Row], x: Sequence[Hashable], y: Sequence[Hashable]) -> bool:
    """The definition, checked on all pairs of tuples."""
    for t in rel:
        for u in rel:
            if all(t[a] == u[a] for a in x) and any(t[a] != u[a] for a in y):
                return False
    return True


def holding_fds(rel: Sequence[Row], attrs: Sequence[Hashable]) -> list[tuple[frozenset, Hashable]]:
    """All FDs X -> A with A not in X that hold in rel, by trying every X (exponential)."""
    out = []
    n = len(attrs)
    for mask in range(1 << n):
        x = [attrs[i] for i in range(n) if mask >> i & 1]
        for a in attrs:
            if a not in x and holds(rel, x, [a]):
                out.append((frozenset(x), a))
    return out
