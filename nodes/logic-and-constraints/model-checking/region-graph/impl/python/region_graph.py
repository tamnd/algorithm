# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/region-graph/. The authors are listed in prov/VER2WP.jsonl.

"""The region graph of a diagonal-free timed automaton.

A timed automaton is a dict with
  "clocks": the number n of clocks, numbered 0 .. n-1,
  "init":   the initial location,
  "edges":  a list of (source, guard, resets, target),
  "inv":    a dict from location to its invariant (missing means true).
A guard or an invariant is a list of atomic constraints (x, op, c) with op in
"<", "<=", "==", ">=", ">" and c a non-negative int. Invariants may only use
"<" and "<=". All clocks start at 0.

A region is a triple (ints, zero, order):
  ints[x]  the integer part of clock x, or cmax[x] + 1 when x > cmax[x];
  zero     the set of bounded clocks whose fractional part is 0;
  order    a tuple of sets that splits the other bounded clocks by their
           fractional parts, from the smallest to the largest.
A clock x is bounded when its value is at most cmax[x].
"""

from math import factorial, prod

OPS = ("<", "<=", "==", ">=", ">")

Region = tuple[tuple[int, ...], frozenset, tuple[frozenset, ...]]


def max_constants(ta: dict) -> list[int]:
    """cmax[x]: the largest constant compared with clock x (0 if none)."""
    cmax = [0] * ta["clocks"]
    cons = [c for _, g, _, _ in ta["edges"] for c in g]
    cons += [c for inv in ta.get("inv", {}).values() for c in inv]
    for x, _, c in cons:
        cmax[x] = max(cmax[x], c)
    return cmax


def initial_region(n: int) -> Region:
    return (0,) * n, frozenset(range(n)), ()


def satisfies(region: Region, constraint: tuple[int, str, int], cmax: list[int]) -> bool:
    """Do all valuations of the region satisfy x op c? (They all agree.)"""
    ints, zero, _ = region
    x, op, c = constraint
    i = ints[x]
    if i > cmax[x]:  # x > cmax[x] >= c
        return op in (">", ">=")
    if x in zero:  # x == i
        return {"<": i < c, "<=": i <= c, "==": i == c, ">=": i >= c, ">": i > c}[op]
    # i < x < i + 1
    return {"<": i < c, "<=": i < c, "==": False, ">=": i >= c, ">": i >= c}[op]


def time_successor(region: Region, cmax: list[int]) -> Region | None:
    """The next region that letting time pass reaches, or None if time
    passing never leaves this region (all clocks are above their maxima)."""
    ints, zero, order = region
    ints = list(ints)
    if zero:  # @line L1
        moved = set()
        for x in zero:  # @line L2
            if ints[x] == cmax[x]:
                ints[x] = cmax[x] + 1  # @line L3
            else:
                moved.add(x)
        new_order = ((frozenset(moved),) if moved else ()) + order  # @line L4
        return tuple(ints), frozenset(), new_order  # @line L5
    if not order:  # @line L6
        return None
    last = order[-1]  # @line L7
    for x in last:
        ints[x] += 1  # @line L8
    return tuple(ints), frozenset(last), order[:-1]  # @line L9


def reset(region: Region, clocks) -> Region:
    """Set the given clocks to 0."""
    ints, zero, order = region
    ints = list(ints)
    rs = frozenset(clocks)
    for x in rs:
        ints[x] = 0
    new_order = tuple(k - rs for k in order if k - rs)
    return tuple(ints), frozenset(zero | rs), new_order


def _ok(region: Region, constraints, cmax) -> bool:
    return all(satisfies(region, c, cmax) for c in constraints)


def reachable(ta: dict) -> set[tuple[object, Region]]:
    """All (location, region) pairs of the region graph reachable from the
    initial state. Cost: linear in the number of reachable pairs times the
    number of edges, at most |L| n! 2^n prod(2 cmax[x] + 2) pairs."""
    cmax = max_constants(ta)
    inv = ta.get("inv", {})
    start = (ta["init"], initial_region(ta["clocks"]))
    if not _ok(start[1], inv.get(ta["init"], []), cmax):
        return set()
    seen = {start}
    stack = [start]
    while stack:
        loc, r = stack.pop()
        nxt = []
        s = time_successor(r, cmax)
        if s is not None and s != r and _ok(s, inv.get(loc, []), cmax):
            nxt.append((loc, s))
        for src, guard, resets, dst in ta["edges"]:
            if src == loc and _ok(r, guard, cmax):
                r2 = reset(r, resets)
                if _ok(r2, inv.get(dst, []), cmax):
                    nxt.append((dst, r2))
        for state in nxt:
            if state not in seen:
                seen.add(state)
                stack.append(state)
    return seen


def reachable_locations(ta: dict) -> set:
    return {loc for loc, _ in reachable(ta)}


def all_regions(cmax: list[int]) -> list[Region]:
    """Every region for the maximal constants cmax (for small inputs)."""
    n = len(cmax)
    kinds = []  # per clock: list of (int part, kind) with kind in zero, frac, top
    for c in cmax:
        kinds.append([(i, "zero") for i in range(c + 1)] + [(i, "frac") for i in range(c)] + [(c + 1, "top")])
    out = []

    def ordered_partitions(items):
        if not items:
            yield ()
            return
        first, rest = items[0], items[1:]
        for part in ordered_partitions(rest):
            for i in range(len(part)):  # put first into an existing class
                yield part[:i] + (part[i] | {first},) + part[i + 1:]
            for i in range(len(part) + 1):  # or into a new class
                yield part[:i] + (frozenset({first}),) + part[i:]

    def choose(x, ints, zero, fracs):
        if x == n:
            for part in ordered_partitions(fracs):
                out.append((tuple(ints), frozenset(zero), part))
            return
        for i, kind in kinds[x]:
            choose(x + 1, ints + [i], zero + ([x] if kind == "zero" else []), fracs + ([x] if kind == "frac" else []))

    choose(0, [], [], [])
    return out


def region_bound(cmax: list[int]) -> int:
    """The Alur-Dill bound n! 2^n prod(2 cmax[x] + 2) on the number of regions."""
    n = len(cmax)
    return factorial(n) * 2**n * prod(2 * c + 2 for c in cmax)
