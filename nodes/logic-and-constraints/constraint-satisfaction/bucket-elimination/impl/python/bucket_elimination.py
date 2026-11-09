# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bucket-elimination/. The authors are listed in prov/GJ1MVJ.jsonl.

"""Bucket elimination (Dechter 1999) for CSPs with constraints of any arity.

The variables are 0 .. n-1. domains[i] is an iterable of the values of
variable i. A constraint is a pair (scope, allowed): scope is a tuple of
distinct variables and allowed is a set of tuples of values, one per variable
of the scope. order lists the variables; the default is 0, 1, ..., n-1.
"""

import itertools
from collections.abc import Iterable, Sequence

Constraint = tuple[tuple[int, ...], set[tuple[int, ...]]]


def induced_width(n: int, scopes: Iterable[Sequence[int]], order: Sequence[int]) -> int:
    """Return the induced width of the primal graph along the order."""
    pos = {v: k for k, v in enumerate(order)}
    nbrs: list[set[int]] = [set() for _ in range(n)]
    for s in scopes:
        for u, v in itertools.combinations(s, 2):
            nbrs[u].add(v)
            nbrs[v].add(u)
    width = 0
    for v in reversed(order):
        earlier = [u for u in nbrs[v] if pos[u] < pos[v]]
        width = max(width, len(earlier))
        for u, w in itertools.combinations(earlier, 2):
            nbrs[u].add(w)
            nbrs[w].add(u)
    return width


def _buckets(n: int, constraints: Iterable[Constraint], order: Sequence[int]):
    pos = {v: k for k, v in enumerate(order)}
    if sorted(pos) != list(range(n)):
        raise ValueError("order must list each variable once")
    buckets: list[list[Constraint]] = [[] for _ in range(n)]
    for scope, allowed in constraints:
        if not scope or len(set(scope)) != len(scope):
            raise ValueError("a scope is a non-empty tuple of distinct variables")
        last = max(scope, key=lambda v: pos[v])
        buckets[last].append((tuple(scope), set(allowed)))  # @line L1
    return pos, buckets


def _satisfies(value: dict[int, int], bucket: list[Constraint]) -> bool:
    return all(tuple(value[v] for v in scope) in allowed for scope, allowed in bucket)


def bucket_elimination(domains: Iterable[Iterable[int]], constraints: Iterable[Constraint],
                       order: Sequence[int] | None = None,
                       stats: dict[str, int] | None = None) -> list[int] | None:
    """Return a solution, or None if the CSP has no solution.

    stats, when given, receives the largest number of variables of a new constraint.
    """
    dom = [sorted(set(d)) for d in domains]
    n = len(dom)
    order = list(range(n)) if order is None else list(order)
    pos, buckets = _buckets(n, constraints, order)
    if stats is None:
        stats = {}
    stats["max_scope"] = 0
    for x in reversed(order):  # @line L2
        u = sorted({v for scope, _ in buckets[x] for v in scope} - {x}, key=lambda v: pos[v])  # @line L3
        stats["max_scope"] = max(stats["max_scope"], len(u))
        new = set()
        for t in itertools.product(*[dom[v] for v in u]):  # @line L4
            value = dict(zip(u, t))
            for a in dom[x]:
                value[x] = a
                if _satisfies(value, buckets[x]):
                    new.add(t)
                    break
        if not new:  # @line L5
            return None
        if u:  # @line L6
            buckets[u[-1]].append((tuple(u), new))
    value: dict[int, int] = {}
    for x in order:  # @line L7
        for a in dom[x]:
            value[x] = a
            if _satisfies(value, buckets[x]):  # @line L8
                break
        else:
            raise AssertionError("bucket elimination is backtrack-free; this cannot happen")
    return [value[v] for v in range(n)]  # @line L9


def bucket_count(domains: Iterable[Iterable[int]], constraints: Iterable[Constraint],
                 order: Sequence[int] | None = None) -> int:
    """Return the number of solutions, by sum-product bucket elimination."""
    dom = [sorted(set(d)) for d in domains]
    n = len(dom)
    order = list(range(n)) if order is None else list(order)
    pos, rel_buckets = _buckets(n, constraints, order)
    # a factor maps each tuple of its scope to a count; a constraint is a 0/1 factor
    buckets: list[list[tuple[tuple[int, ...], dict[tuple[int, ...], int]]]] = [
        [(scope, {t: 1 for t in allowed}) for scope, allowed in b] for b in rel_buckets]
    total = 1
    for x in reversed(order):
        u = sorted({v for scope, _ in buckets[x] for v in scope} - {x}, key=lambda v: pos[v])
        table: dict[tuple[int, ...], int] = {}
        for t in itertools.product(*[dom[v] for v in u]):
            value = dict(zip(u, t))
            s = 0
            for a in dom[x]:
                value[x] = a
                p = 1
                for scope, f in buckets[x]:
                    p *= f.get(tuple(value[v] for v in scope), 0)
                    if p == 0:
                        break
                s += p
            if s:
                table[t] = s
        if u:
            buckets[u[-1]].append((tuple(u), table))
        else:
            total *= table.get((), 0)
    return total
