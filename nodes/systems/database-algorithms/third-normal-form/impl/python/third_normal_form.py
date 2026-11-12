# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/third-normal-form/. The authors are listed in prov/SA5P36.jsonl.

"""Test whether a relation schema (U, F) is in third normal form.

The test follows Zaniolo's form of the definition: for each nontrivial
X -> A, X is a superkey or A is prime. It finds all keys by brute force over
the subsets of U, so it is exponential in |U|. This is expected: the problem
is NP-complete (Jou and Fischer, 1982). is_3nf checks only the FDs of F;
is_3nf_by_definition checks every implied FD, and the tests compare the two.

An FD is a pair (lhs, rhs) of frozensets of attribute names.
"""

from collections.abc import Hashable, Iterable, Sequence
from itertools import combinations

FD = tuple[frozenset, frozenset]


def fd(lhs: Iterable[Hashable], rhs: Iterable[Hashable]) -> FD:
    return (frozenset(lhs), frozenset(rhs))


def closure(fds: Sequence[FD], x: Iterable[Hashable]) -> frozenset:
    out = set(x)
    changed = True
    while changed:
        changed = False
        for lhs, rhs in fds:
            if lhs <= out and not rhs <= out:
                out |= rhs
                changed = True
    return frozenset(out)


def subsets(universe: Iterable[Hashable]) -> list[frozenset]:
    u = sorted(set(universe), key=repr)
    return [frozenset(c) for n in range(len(u) + 1) for c in combinations(u, n)]


def keys(universe: Iterable[Hashable], fds: Sequence[FD]) -> list[frozenset]:
    """All candidate keys, by brute force over subsets in order of size."""
    u = frozenset(universe)
    found: list[frozenset] = []
    for s in subsets(u):
        if not any(k <= s for k in found) and closure(fds, s) >= u:
            found.append(s)
    return found


def prime_attributes(universe: Iterable[Hashable], fds: Sequence[FD]) -> frozenset:
    out: frozenset = frozenset()
    for k in keys(universe, fds):
        out |= k
    return out


def violations(universe: Iterable[Hashable], fds: Sequence[FD]) -> list[tuple[frozenset, Hashable]]:
    """The pairs (X, A) with X -> A in F, A not in X, X not a superkey and A not prime."""
    u = frozenset(universe)
    prime = prime_attributes(u, fds)
    out = []
    for lhs, rhs in fds:
        superkey = closure(fds, lhs) >= u
        for a in sorted(rhs - lhs, key=repr):
            if not superkey and a not in prime:
                out.append((lhs, a))
    return out


def is_3nf(universe: Iterable[Hashable], fds: Sequence[FD]) -> bool:
    return not violations(universe, fds)


def is_3nf_by_definition(universe: Iterable[Hashable], fds: Sequence[FD]) -> bool:
    """Check every nontrivial implied FD X -> A with X a subset of U."""
    u = frozenset(universe)
    prime = prime_attributes(u, fds)
    for x in subsets(u):
        c = closure(fds, x)
        if c >= u:
            continue
        if not (c - x) <= prime:
            return False
    return True


def is_bcnf(universe: Iterable[Hashable], fds: Sequence[FD]) -> bool:
    """BCNF, for comparison: the left side of each nontrivial FD of F is a superkey."""
    u = frozenset(universe)
    return all(rhs <= lhs or closure(fds, lhs) >= u for lhs, rhs in fds)
