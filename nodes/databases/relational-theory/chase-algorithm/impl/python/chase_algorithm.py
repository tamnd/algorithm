# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chase-algorithm/. The authors are listed in prov/JMAKT7.jsonl.
"""The chase of a tableau with functional dependencies and join dependencies.

A schema is a tuple of attribute names. A tableau is a set of rows; a row is a tuple
with one symbol for each attribute. Symbols are integers, and the symbol 0 is the
distinguished symbol of every column. Each column has its own symbols.

An FD X -> Y is a pair (X, Y) of frozensets of attributes. A JD is a list of
frozensets of attributes whose union is the schema. An MVD X ->> Y is the JD
[X | Y, X | (R - Y)].
"""

FD = tuple[frozenset, frozenset]


def mvd_as_jd(schema: tuple, x: frozenset, y: frozenset) -> list[frozenset]:
    """The JD of the MVD X ->> Y over the schema."""
    r = frozenset(schema)
    return [x | y, x | (r - y)]


def _join_of_projections(schema: tuple, rows: set, parts: list[frozenset]) -> set:
    """The natural join of the projections of rows on parts, as rows over schema."""
    pos = {a: i for i, a in enumerate(schema)}
    partial = [{}]
    for part in parts:
        cols = sorted(pos[a] for a in part)
        proj = {tuple(row[c] for c in cols) for row in rows}
        nxt = []
        for p in partial:
            for vals in proj:
                ok = True
                for c, v in zip(cols, vals):
                    if c in p and p[c] != v:
                        ok = False
                        break
                if ok:
                    q = dict(p)
                    q.update(zip(cols, vals))
                    nxt.append(q)
        partial = nxt
    return {tuple(p[i] for i in range(len(schema))) for p in partial}


def chase(schema: tuple, rows, fds: list[FD], jds: list[list[frozenset]]) -> set:
    """Chase the tableau rows with fds and jds until no rule applies. Return the final tableau."""
    pos = {a: i for i, a in enumerate(schema)}
    t = set(map(tuple, rows))  # @line L1
    changed = True
    while changed:  # @line L2
        changed = False  # @line L3
        for lhs, rhs in fds:  # @line L4
            lcols = [pos[a] for a in lhs]
            rcols = [pos[a] for a in rhs]
            pair = _fd_violation(t, lcols, rcols)
            while pair is not None:  # @line L5
                u, v = pair
                c = next(c for c in rcols if u[c] != v[c])
                old, new = max(u[c], v[c]), min(u[c], v[c])  # @line L6
                t = {row[:c] + (new,) + row[c + 1:] if row[c] == old else row for row in t}  # @line L7
                changed = True
                pair = _fd_violation(t, lcols, rcols)
        for parts in jds:  # @line L8
            joined = _join_of_projections(schema, t, parts)  # @line L9
            if not joined <= t:  # @line L10
                t |= joined  # @line L11
                changed = True
    return t  # @line L12


def _fd_violation(t: set, lcols: list[int], rcols: list[int]):
    """Two rows that agree on the left columns and differ on a right column, or None."""
    seen = {}
    for row in t:
        key = tuple(row[c] for c in lcols)
        other = seen.get(key)
        if other is None:
            seen[key] = row
        elif any(other[c] != row[c] for c in rcols):
            return other, row
    return None


def implies_fd(schema: tuple, fds: list[FD], jds: list[list[frozenset]], x: frozenset, y: frozenset) -> bool:
    """Decide whether the FDs and JDs imply X -> Y.

    Start with two rows: all 0, and 0 on X with the symbol 1 elsewhere. X -> Y follows
    exactly when, in each column of Y, the symbol 1 has been replaced by 0.
    """
    u = tuple(0 for _ in schema)
    v = tuple(0 if a in x else 1 for a in schema)
    t = chase(schema, [u, v], fds, jds)
    cols = [i for i, a in enumerate(schema) if a in y]
    return all(row[c] == 0 for row in t for c in cols)


def jd_tableau(schema: tuple, parts: list[frozenset]) -> list[tuple]:
    """One row for each part: 0 on the part, and a symbol of its own elsewhere."""
    return [tuple(0 if a in part else i + 1 for a in schema) for i, part in enumerate(parts)]


def implies_jd(schema: tuple, fds: list[FD], jds: list[list[frozenset]], parts: list[frozenset]) -> bool:
    """Decide whether the FDs and JDs imply the JD over parts: the chase must make an all-0 row."""
    t = chase(schema, jd_tableau(schema, parts), fds, jds)
    return tuple(0 for _ in schema) in t


def lossless(schema: tuple, parts: list[frozenset], fds: list[FD]) -> bool:
    """The lossless-join test of Aho, Beeri and Ullman: implication of the JD of the parts."""
    return implies_jd(schema, fds, [], parts)


def satisfies_fd(schema: tuple, rel: set, x: frozenset, y: frozenset) -> bool:
    pos = {a: i for i, a in enumerate(schema)}
    return _fd_violation(set(rel), [pos[a] for a in x], [pos[a] for a in y]) is None


def satisfies_jd(schema: tuple, rel: set, parts: list[frozenset]) -> bool:
    return _join_of_projections(schema, set(rel), parts) <= set(rel)


def satisfies_all(schema: tuple, rel: set, fds: list[FD], jds: list[list[frozenset]]) -> bool:
    return all(satisfies_fd(schema, rel, x, y) for x, y in fds) and all(satisfies_jd(schema, rel, p) for p in jds)
