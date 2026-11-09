# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/difference-bound-matrix/. The authors are listed in prov/0E95QY.jsonl.

"""Difference bound matrices (DBMs) for clock zones.

Clocks are numbered 1 .. n, and index 0 is the reference clock, always 0.
Entry D[i][j] is a bound (c, le) on x_i - x_j: the constraint x_i - x_j < c
when le == 0 and x_i - x_j <= c when le == 1. Python compares the pairs in
the right order: (c, 0) < (c, 1) < (c + 1, 0). INF = (inf, 0) means no bound.
A DBM is a list of lists. The functions return new DBMs, or None for the
empty zone, and keep the canonical (shortest path) form.
"""

from math import inf

INF = (inf, 0)
LE0 = (0, 1)  # the bound <= 0


def add(a, b):
    """The bound on x - z given a on x - y and b on y - z."""
    return (a[0] + b[0], min(a[1], b[1]))


def zero(n):
    """The zone with every clock equal to 0."""
    return [[LE0] * (n + 1) for _ in range(n + 1)]


def universe(n):
    """All valuations: every clock is at least 0."""
    d = [[INF] * (n + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        d[i][i] = LE0
        d[0][i] = LE0
    return d


def canonical(d):
    """Floyd-Warshall closure. Returns the canonical DBM, or None if the
    zone is empty (a negative cycle). O(n^3) time."""
    d = [row[:] for row in d]
    m = len(d)
    for k in range(m):  # @line L1
        for i in range(m):  # @line L2
            dik = d[i][k]
            if dik == INF:
                continue
            for j in range(m):  # @line L3
                s = add(dik, d[k][j])
                if s < d[i][j]:  # @line L4
                    d[i][j] = s  # @line L5
    for i in range(m):  # @line L6
        if d[i][i] < LE0:
            return None  # @line L7
    return d  # @line L8


def contains(d, v):
    """Is the valuation v (a sequence of n numbers) in the zone?"""
    w = [0, *v]
    for i, row in enumerate(d):
        for j, (c, le) in enumerate(row):
            diff = w[i] - w[j]
            if diff > c or (diff == c and not le):
                return False
    return True


def up(d):
    """Let time pass: drop the upper bounds x_i - x_0. Keeps canonical form."""
    d = [row[:] for row in d]
    for i in range(1, len(d)):
        d[i][0] = INF
    return d


def tighten(d, i, j, b):
    """Add x_i - x_j bounded by b to a canonical DBM, in O(n^2) time."""
    if add(d[j][i], b) < LE0:
        return None
    if not b < d[i][j]:
        return [row[:] for row in d]
    d = [row[:] for row in d]
    d[i][j] = b
    m = len(d)
    for p in range(m):
        for q in range(m):
            s = add(add(d[p][i], b), d[j][q])
            if s < d[p][q]:
                d[p][q] = s
    return d


def constrain(d, constraint):
    """Intersect with an atomic constraint (x, op, c), clock x in 1 .. n."""
    x, op, c = constraint
    if op in ("<", "<=", "=="):
        d = tighten(d, x, 0, (c, int(op != "<")))
        if d is None:
            return None
    if op in (">", ">=", "=="):
        d = tighten(d, 0, x, (-c, int(op != ">")))
    return d


def constrain_all(d, constraints):
    for con in constraints:
        if d is None:
            return None
        d = constrain(d, con)
    return d


def reset(d, x):
    """Set clock x to 0. Keeps canonical form."""
    d = [row[:] for row in d]
    for j in range(len(d)):
        d[x][j] = d[0][j]
        d[j][x] = d[j][0]
    d[x][x] = LE0
    return d


def includes(big, small):
    """Is the zone small a subset of the zone big? Both must be canonical."""
    return all(s <= b for rb, rs in zip(big, small) for b, s in zip(rb, rs))


def extrapolate(d, k):
    """Extra_M (k-normalization) with k[i] the largest constant of clock i
    (k[0] = 0). Bounds above k[i] are dropped, and lower bounds below -k[j]
    are relaxed to -k[j] strict. Returns a canonical DBM."""
    d = [row[:] for row in d]
    m = len(d)
    for i in range(m):
        for j in range(m):
            if i == j or d[i][j] == INF:
                continue
            if d[i][j] > (k[i], 1):
                d[i][j] = INF
            elif d[i][j] < (-k[j], 0):
                d[i][j] = (-k[j], 0)
    return canonical(d)


def max_constants(ta):
    """k[0] = 0 and k[x] the largest constant compared with clock x."""
    k = [0] * (ta["clocks"] + 1)
    cons = [c for _, g, _, _ in ta["edges"] for c in g]
    cons += [c for inv in ta.get("inv", {}).values() for c in inv]
    for x, _, c in cons:
        k[x] = max(k[x], c)
    return k


def zone_graph(ta):
    """Forward reachability over zones with extrapolation and inclusion.

    The automaton has "clocks" n (numbered 1 .. n), "init", "edges" as
    (source, guard, resets, target), and "inv" from location to constraints.
    Returns a dict from location to the list of its stored zones."""
    n = ta["clocks"]
    k = max_constants(ta)
    inv = ta.get("inv", {})

    def post_delay(loc, z):
        z = constrain_all(up(z), inv.get(loc, []))
        return None if z is None else extrapolate(z, k)

    z0 = constrain_all(zero(n), inv.get(ta["init"], []))
    z0 = None if z0 is None else post_delay(ta["init"], z0)
    passed = {}
    if z0 is None:
        return passed
    passed[ta["init"]] = [z0]
    waiting = [(ta["init"], z0)]
    while waiting:
        loc, z = waiting.pop()
        for src, guard, resets, dst in ta["edges"]:
            if src != loc:
                continue
            z2 = constrain_all(z, guard)
            if z2 is None:
                continue
            for x in resets:
                z2 = reset(z2, x)
            z2 = constrain_all(z2, inv.get(dst, []))
            if z2 is None:
                continue
            z2 = post_delay(dst, z2)
            if z2 is None:
                continue
            stored = passed.setdefault(dst, [])
            if any(includes(old, z2) for old in stored):
                continue
            stored[:] = [old for old in stored if not includes(z2, old)]
            stored.append(z2)
            waiting.append((dst, z2))
    return passed


def reachable_locations(ta):
    return set(zone_graph(ta))
