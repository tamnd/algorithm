# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/third-normal-form-synthesis/. The authors are listed in prov/NWV2WW.jsonl.

"""3NF synthesis: from a set F of FDs over U, build a decomposition of U that is
in 3NF, preserves F and has a lossless join.

The steps are those of Bernstein (1976) with the key schema of Biskup, Dayal
and Bernstein (1979): take a minimal cover, make one schema for each left
side, add a key if no schema holds one, and drop schemas that lie inside
another. is_lossless is a small tableau chase, used to check the result.

An FD is a pair (lhs, rhs) of frozensets of attribute names.
"""

from collections.abc import Hashable, Iterable, Sequence

FD = tuple[frozenset, frozenset]


def fd(lhs: Iterable[Hashable], rhs: Iterable[Hashable]) -> FD:
    return (frozenset(lhs), frozenset(rhs))


def closure(fds: Iterable[FD], x: Iterable[Hashable]) -> frozenset:
    fds = list(fds)
    out = set(x)
    changed = True
    while changed:
        changed = False
        for lhs, rhs in fds:
            if lhs <= out and not rhs <= out:
                out |= rhs
                changed = True
    return frozenset(out)


def _order(xs: Iterable[Hashable]) -> list:
    return sorted(xs, key=repr)


def minimal_cover(fds: Iterable[FD]) -> list[FD]:
    """Split right sides, remove extraneous left attributes, then redundant FDs."""
    fds = list(fds)
    g = {(lhs, frozenset([a])) for lhs, rhs in fds for a in rhs if a not in lhs}
    reduced = set()
    for lhs, rhs in g:
        x = set(lhs)
        for b in _order(lhs):
            if rhs <= closure(fds, x - {b}):
                x.discard(b)
        reduced.add((frozenset(x), rhs))
    g2 = sorted(reduced, key=lambda d: (_order(map(repr, d[0])), _order(map(repr, d[1]))))
    i = 0
    while i < len(g2):
        rest = g2[:i] + g2[i + 1 :]
        if g2[i][1] <= closure(rest, g2[i][0]):
            g2 = rest
        else:
            i += 1
    return g2


def find_key(universe: frozenset, fds: Sequence[FD]) -> frozenset:
    """Shrink U to a candidate key, one attribute at a time."""
    k = set(universe)
    for a in _order(universe):
        if closure(fds, k - {a}) >= universe:
            k.discard(a)
    return frozenset(k)


def synthesize(universe: Iterable[Hashable], fds: Iterable[FD]) -> list[frozenset]:
    """Return the schemas of a lossless, dependency-preserving 3NF decomposition."""
    u = frozenset(universe)
    g = minimal_cover(fds)  # @line L1
    groups: dict[frozenset, set] = {}
    for lhs, rhs in g:  # @line L2
        groups.setdefault(lhs, set(lhs)).update(rhs)  # @line L3
    schemas = [frozenset(s) for s in groups.values()]  # @line L4
    if not any(closure(g, s) >= u for s in schemas):  # @line L5
        schemas.append(find_key(u, g))  # @line L6
    schemas.sort(key=len, reverse=True)
    kept: list[frozenset] = []
    for s in schemas:  # @line L7
        if not any(s <= t for t in kept):
            kept.append(s)
    return kept  # @line L8


def is_lossless(universe: Iterable[Hashable], schemas: Sequence[frozenset], fds: Iterable[FD]) -> bool:
    """The tableau chase: the join of the schemas is lossless under fds if and
    only if the chase makes some row hold only distinguished symbols."""
    attrs = _order(set(universe))
    col = {a: j for j, a in enumerate(attrs)}
    fds = list(fds)
    rows = [[("a", a) if a in s else ("b", i, a) for a in attrs] for i, s in enumerate(schemas)]
    changed = True
    while changed:
        changed = False
        for lhs, rhs in fds:
            idx = [col[a] for a in _order(lhs)]
            groups: dict[tuple, list[list]] = {}
            for row in rows:
                groups.setdefault(tuple(row[j] for j in idx), []).append(row)
            for group in groups.values():
                for a in _order(rhs):
                    j = col[a]
                    syms = {row[j] for row in group}
                    if len(syms) > 1:
                        keep = min(syms)  # ("a", ...) sorts before ("b", ...)
                        for row in rows:
                            if row[j] in syms and row[j] != keep:
                                row[j] = keep
                        changed = True
    return any(all(sym[0] == "a" for sym in row) for row in rows)
