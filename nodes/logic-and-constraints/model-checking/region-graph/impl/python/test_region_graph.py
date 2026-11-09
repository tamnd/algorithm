# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/region-graph/. The authors are listed in prov/VER2WP.jsonl.

import random

from region_graph import (
    all_regions,
    initial_region,
    max_constants,
    reachable,
    reachable_locations,
    region_bound,
    reset,
    satisfies,
    time_successor,
)

# The worked example: from l1 the guard x >= 2 and y <= 1 can be met only
# at the single point x = 2, y = 1, so l2 is reachable and l3 is not.
EXAMPLE = {
    "clocks": 2,
    "init": "l0",
    "edges": [
        ("l0", [(0, "<=", 1)], [1], "l1"),
        ("l1", [(0, ">=", 2), (1, "<=", 1)], [], "l2"),
        ("l1", [(0, ">=", 2), (1, "<", 1)], [], "l3"),
    ],
    "inv": {},
}


def discretized(ta, k):
    """Location reachability with every delay a multiple of 1/k."""
    n = ta["clocks"]
    cmax = max_constants(ta)
    inv = ta.get("inv", {})
    cap = [c * k + 1 for c in cmax]

    def ok(v, cons):
        return all(
            {"<": v[x] < c * k, "<=": v[x] <= c * k, "==": v[x] == c * k, ">=": v[x] >= c * k, ">": v[x] > c * k}[op]
            for x, op, c in cons
        )

    start = (ta["init"], (0,) * n)
    if not ok(start[1], inv.get(ta["init"], [])):
        return set()
    seen, stack = {start}, [start]
    while stack:
        loc, v = stack.pop()
        nxt = []
        d = tuple(min(a + 1, cap[x]) for x, a in enumerate(v))
        if ok(d, inv.get(loc, [])):
            nxt.append((loc, d))
        for src, guard, resets, dst in ta["edges"]:
            if src == loc and ok(v, guard):
                v2 = tuple(0 if x in resets else a for x, a in enumerate(v))
                if ok(v2, inv.get(dst, [])):
                    nxt.append((dst, v2))
        for s in nxt:
            if s not in seen:
                seen.add(s)
                stack.append(s)
    return {loc for loc, _ in seen}


# A small zone (DBM) explorer, written independently, as a second oracle.
INF = 1 << 60


def _add(a, b):
    if a >= INF or b >= INF:
        return INF
    return ((a & ~1) + (b & ~1)) | (a & b & 1)


def _bound(c, strict):
    return 2 * c + (0 if strict else 1)


def _close(m):
    n = len(m)
    for k in range(n):
        for i in range(n):
            for j in range(n):
                s = _add(m[i][k], m[k][j])
                if s < m[i][j]:
                    m[i][j] = s
    return m


def _empty(m):
    return any(m[i][i] < _bound(0, False) for i in range(len(m)))


def _constrain(m, cons):
    m = [row[:] for row in m]
    for x, op, c in cons:
        i = x + 1
        if op in ("<", "<=", "=="):
            m[i][0] = min(m[i][0], _bound(c, op == "<"))
        if op in (">", ">=", "=="):
            m[0][i] = min(m[0][i], _bound(-c, op == ">"))
    return _close(m)


def _up(m):
    m = [row[:] for row in m]
    for i in range(1, len(m)):
        m[i][0] = INF
    return m


def _reset(m, resets):
    m = [row[:] for row in m]
    for x in resets:
        i = x + 1
        for j in range(len(m)):
            m[i][j] = m[0][j]
            m[j][i] = m[j][0]
        m[i][i] = _bound(0, False)
    return m


def _extra(m, cmax):
    m = [row[:] for row in m]
    k = [0] + cmax
    for i in range(len(m)):
        for j in range(len(m)):
            if i == j or m[i][j] >= INF:
                continue
            if m[i][j] > _bound(k[i], False):
                m[i][j] = INF
            elif m[i][j] < _bound(-k[j], True):
                m[i][j] = _bound(-k[j], True)
    return _close(m)


def zone_locations(ta):
    n = ta["clocks"]
    cmax = max_constants(ta)
    inv = ta.get("inv", {})
    z0 = [[_bound(0, False)] * (n + 1) for _ in range(n + 1)]

    def norm(loc, z):
        z = _constrain(_up(z), inv.get(loc, []))
        return None if _empty(z) else _extra(z, cmax)

    start = _constrain(z0, inv.get(ta["init"], []))
    if _empty(start):
        return set()
    first = norm(ta["init"], start)
    seen = {(ta["init"], tuple(map(tuple, first)))}
    stack = [(ta["init"], first)]
    while stack:
        loc, z = stack.pop()
        for src, guard, resets, dst in ta["edges"]:
            if src != loc:
                continue
            z2 = _constrain(z, guard)
            if _empty(z2):
                continue
            z2 = _constrain(_reset(z2, resets), inv.get(dst, []))
            if _empty(z2):
                continue
            z2 = norm(dst, z2)
            if z2 is None:
                continue
            key = (dst, tuple(map(tuple, z2)))
            if key not in seen:
                seen.add(key)
                stack.append((dst, z2))
    return {loc for loc, _ in seen}


def random_ta(rng, closed):
    n = rng.randint(1, 3)
    locs = [f"l{i}" for i in range(rng.randint(2, 4))]
    ops = ["<=", "==", ">="] if closed else list(("<", "<=", "==", ">=", ">"))
    edges = []
    for _ in range(rng.randint(2, 6)):
        guard = [(rng.randrange(n), rng.choice(ops), rng.randint(0, 2)) for _ in range(rng.randint(0, 2))]
        resets = [x for x in range(n) if rng.random() < 0.4]
        edges.append((rng.choice(locs), guard, resets, rng.choice(locs)))
    inv = {}
    for loc in locs:
        if rng.random() < 0.3:
            inv[loc] = [(rng.randrange(n), "<=" if closed or rng.random() < 0.5 else "<", rng.randint(1, 3))]
    return {"clocks": n, "init": locs[0], "edges": edges, "inv": inv}


def test_example() -> None:
    assert reachable_locations(EXAMPLE) == {"l0", "l1", "l2"}
    cmax = max_constants(EXAMPLE)
    assert cmax == [2, 1]
    # the time successors of the initial region, as on the page
    r = initial_region(2)
    chain = [r]
    while (r := time_successor(r, cmax)) is not None:
        chain.append(r)
    assert chain[1] == ((0, 0), frozenset(), (frozenset({0, 1}),))
    assert chain[2] == ((1, 1), frozenset({0, 1}), ())
    assert chain[3] == ((1, 2), frozenset(), (frozenset({0}),))
    assert chain[-1] == ((3, 2), frozenset(), ())
    assert len(chain) == 6


def test_region_operations() -> None:
    cmax = [2, 1]
    r = ((1, 0), frozenset({0}), (frozenset({1}),))  # x = 1, 0 < y < 1
    assert satisfies(r, (0, "==", 1), cmax) and satisfies(r, (1, "<", 1), cmax)
    assert not satisfies(r, (1, "==", 0), cmax) and satisfies(r, (1, ">", 0), cmax)
    assert reset(r, [1]) == ((1, 0), frozenset({0, 1}), ())
    assert time_successor(r, cmax) == ((1, 0), frozenset(), (frozenset({0}), frozenset({1})))


def test_region_count() -> None:
    for cmax in ([0], [3], [1, 1], [2, 1], [1, 1, 1], [2, 0, 1]):
        regions = all_regions(cmax)
        assert len(set(regions)) == len(regions) <= region_bound(cmax)
        if len(cmax) == 1:
            assert len(regions) == 2 * cmax[0] + 2
        # time successors and resets stay inside the set of regions
        rs = set(regions)
        for r in regions:
            s = time_successor(r, cmax)
            assert s is None or s in rs
            assert reset(r, [0]) in rs


def test_against_zones_and_discretized_runs() -> None:
    rng = random.Random(31)
    for trial in range(400):
        closed = trial % 2 == 0
        ta = random_ta(rng, closed)
        locs = reachable_locations(ta)
        assert locs == zone_locations(ta), ta
        n = ta["clocks"]
        grid = discretized(ta, 2 * (n + 1))
        assert grid <= locs, ta  # runs on a grid are real runs
        if closed:  # digitization: integer delays suffice without strict constraints
            assert discretized(ta, 1) == locs, ta


def test_reachable_pairs_are_bounded() -> None:
    rng = random.Random(32)
    for _ in range(50):
        ta = random_ta(rng, False)
        pairs = reachable(ta)
        nlocs = len({e[0] for e in ta["edges"]} | {e[3] for e in ta["edges"]} | {ta["init"]})
        assert len(pairs) <= nlocs * region_bound(max_constants(ta))
