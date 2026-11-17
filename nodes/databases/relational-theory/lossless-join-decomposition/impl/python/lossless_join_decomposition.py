# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lossless-join-decomposition/. The authors are listed in prov/M09NZ8.jsonl.
"""Tests for a lossless-join decomposition under functional dependencies.

A schema is a tuple of attribute names. A relation over a schema is a set of tuples in the
order of the schema. An FD X -> Y is a pair of frozensets of attribute names.
"""

FD = tuple[frozenset, frozenset]


def closure(x: frozenset, fds: list[FD]) -> frozenset:
    """X+ under fds."""
    result = set(x)
    changed = True
    while changed:
        changed = False
        for lhs, rhs in fds:
            if lhs <= result and not rhs <= result:
                result |= rhs
                changed = True
    return frozenset(result)


def binary_lossless(r1: frozenset, r2: frozenset, fds: list[FD]) -> bool:
    """The binary test: R1 & R2 -> R1 or R1 & R2 -> R2. Cost: one closure."""
    c = closure(r1 & r2, fds)
    return r1 <= c or r2 <= c


def chase_lossless(schema: tuple, parts: list[frozenset], fds: list[FD]) -> bool:
    """The tableau chase of Aho, Beeri and Ullman for FDs.

    Row i has the distinguished symbol 0 in the columns of part i and the symbol i + 1
    elsewhere. The FD rule makes two rows that agree on X agree on Y, keeping the smaller
    symbol (so 0 wins). The decomposition is lossless iff some row ends all zero.
    Cost: at most k * n merges, each pass O(|F| k^2 n) for k parts and n attributes.
    """
    col = {a: j for j, a in enumerate(schema)}
    rows = [[0 if a in p else i + 1 for a in schema] for i, p in enumerate(parts)]
    changed = True
    while changed:
        changed = False
        for lhs, rhs in fds:
            li = [col[a] for a in lhs]
            for i in range(len(rows)):
                for j in range(i + 1, len(rows)):
                    if all(rows[i][c] == rows[j][c] for c in li):
                        for a in rhs:
                            c = col[a]
                            u, v = rows[i][c], rows[j][c]
                            if u != v:
                                keep, drop = min(u, v), max(u, v)
                                for row in rows:
                                    if row[c] == drop:
                                        row[c] = keep
                                changed = True
    return any(all(s == 0 for s in row) for row in rows)


def project(schema: tuple, rel: set, part: tuple) -> set:
    """The projection of rel onto the attributes of part, in the order of part."""
    idx = [schema.index(a) for a in part]
    return {tuple(t[i] for i in idx) for t in rel}


def join_of_projections(schema: tuple, rel: set, parts: list[tuple]) -> set:
    """The natural join of the projections of rel on parts, as tuples over schema."""
    partial: list[dict] = [{}]
    for part in parts:
        proj = project(schema, rel, part)
        nxt = []
        for env in partial:
            for t in proj:
                if all(env.get(a, v) == v for a, v in zip(part, t)):
                    e = dict(env)
                    e.update(zip(part, t))
                    nxt.append(e)
        partial = nxt
    return {tuple(e[a] for a in schema) for e in partial}


def spurious_tuples(schema: tuple, rel: set, parts: list[tuple]) -> set:
    """The tuples that the join of the projections adds to rel."""
    return join_of_projections(schema, rel, parts) - set(rel)


def satisfies(schema: tuple, rel: set, fds: list[FD]) -> bool:
    """True when rel satisfies every FD."""
    for lhs, rhs in fds:
        seen: dict = {}
        li = [schema.index(a) for a in sorted(lhs)]
        ri = [schema.index(a) for a in sorted(rhs)]
        for t in rel:
            key = tuple(t[i] for i in li)
            val = tuple(t[i] for i in ri)
            if seen.setdefault(key, val) != val:
                return False
    return True
