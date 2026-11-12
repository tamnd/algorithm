# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/minimal-cover-problem/. The authors are listed in prov/M2Z1TE.jsonl.

"""Minimal covers of a set of functional dependencies.

minimal_cover runs the three standard steps in their required order:
split the right sides, remove extraneous left attributes, then remove
redundant FDs. is_minimal checks the three conditions of a minimal cover
directly, and is a reference for the tests.

An FD is a pair (lhs, rhs) of frozensets of attribute names.
"""

from collections.abc import Hashable, Iterable, Sequence

FD = tuple[frozenset, frozenset]


def fd(lhs: Iterable[Hashable], rhs: Iterable[Hashable]) -> FD:
    return (frozenset(lhs), frozenset(rhs))


def closure(fds: Iterable[FD], x: Iterable[Hashable]) -> frozenset:
    """X+ by the fixpoint loop (the sets here are small)."""
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


def equivalent(f: Sequence[FD], g: Sequence[FD]) -> bool:
    return all(r <= closure(f, l) for l, r in g) and all(r <= closure(g, l) for l, r in f)


def _key(d: FD) -> tuple:
    return (sorted(map(repr, d[0])), sorted(map(repr, d[1])))


def minimal_cover(fds: Iterable[FD]) -> list[FD]:
    """Return a minimal cover of fds: single right sides, left-reduced, nonredundant."""
    fds = list(fds)
    # Step 1: one attribute on each right side; trivial FDs are dropped.
    g = sorted({(lhs, frozenset([a])) for lhs, rhs in fds for a in rhs if a not in lhs}, key=_key)
    # Step 2: remove extraneous left attributes. Closures are taken under the
    # original FDs: each replacement keeps an equivalent set, so they do not change.
    reduced = []
    for lhs, rhs in g:
        x = set(lhs)
        for b in sorted(lhs, key=repr):
            if rhs <= closure(fds, x - {b}):
                x.discard(b)
        reduced.append((frozenset(x), rhs))
    g = sorted(set(reduced), key=_key)
    # Step 3: remove redundant FDs, one at a time, against the current set.
    i = 0
    while i < len(g):
        rest = g[:i] + g[i + 1 :]
        if g[i][1] <= closure(rest, g[i][0]):
            g = rest
        else:
            i += 1
    return g


def is_minimal(g: Sequence[FD]) -> bool:
    """Check the three conditions of a minimal cover by brute force."""
    g = list(g)
    if len(set(g)) != len(g):
        return False
    for i, (lhs, rhs) in enumerate(g):
        if len(rhs) != 1 or rhs <= lhs:
            return False
        rest = g[:i] + g[i + 1 :]
        if equivalent(rest, g):
            return False
        for b in lhs:
            if equivalent(rest + [(lhs - {b}, rhs)], g):
                return False
    return True
