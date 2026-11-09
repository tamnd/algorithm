# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/difference-bound-matrix/. The authors are listed in prov/0E95QY.jsonl.

import random
from fractions import Fraction
from itertools import product

from difference_bound_matrix import (
    INF,
    LE0,
    canonical,
    constrain,
    contains,
    extrapolate,
    includes,
    max_constants,
    reachable_locations,
    reset,
    tighten,
    universe,
    up,
    zero,
)

N = 2
STEP = Fraction(1, N + 1)
GRID = [STEP * i for i in range(0, 9 * (N + 1) + 1)]  # 0 .. 9
# delays and free values: a witness never needs to exceed 9 + 3 (the largest difference bound)
FINE = [Fraction(1, 2 * (N + 1)) * i for i in range(0, 2 * 13 * (N + 1) + 1)]
POINTS = list(product(GRID, repeat=N))


def random_dbm(rng, n=N):
    """A DBM from a few random difference constraints, not closed."""
    d = universe(n)
    for _ in range(rng.randint(0, 4)):
        i, j = rng.sample(range(n + 1), 2)
        c = rng.randint(-3, 3) if i and j else (rng.randint(0, 4) if i else -rng.randint(0, 4))
        d[i][j] = min(d[i][j], (c, rng.randint(0, 1)))
    return d


def members(d):
    return {v for v in POINTS if contains(d, v)}


def test_example() -> None:
    # x in [1, 3], y in [0, 2], x - y <= 2, then closed by Floyd-Warshall
    d = universe(2)
    d[1][0], d[0][1] = (3, 1), (-1, 1)
    d[2][0], d[0][2] = (2, 1), (0, 1)
    d[1][2] = (2, 1)
    c = canonical(d)
    assert c[1][0] == (3, 1) and c[2][1] == (1, 1) and c[0][2] == (0, 1)
    # adding y < 1 tightens x to < 3 through x - y <= 2
    t = tighten(c, 2, 0, (1, 0))
    assert t[1][0] == (3, 0)
    assert t == canonical(constrain(c, (2, "<", 1)))
    # x - y >= 3 together with the rest is empty
    assert tighten(c, 2, 1, (-3, 1)) is None
    assert includes(c, t) and not includes(t, c)


def test_canonical_keeps_the_set_and_detects_emptiness() -> None:
    rng = random.Random(41)
    for _ in range(150):
        d = random_dbm(rng)
        c = canonical(d)
        pts = members(d)
        if c is None:
            assert not pts
            continue
        assert pts and members(c) == pts
        # canonical means every entry is the tightest bound: idempotent
        assert canonical(c) == c
        for i in range(N + 1):
            for j in range(N + 1):
                for k in range(N + 1):
                    assert c[i][j] <= (c[i][k][0] + c[k][j][0], min(c[i][k][1], c[k][j][1]))


def test_operations_match_the_semantics() -> None:
    rng = random.Random(42)
    done = 0
    while done < 25:
        c = canonical(random_dbm(rng))
        if c is None:
            continue
        done += 1
        pts = members(c)
        # up: w in up(Z) iff w - t is in Z for some t >= 0
        u = up(c)
        assert canonical(u) == u
        for w in POINTS:
            want = any(min(w) - t >= 0 and contains(c, tuple(a - t for a in w)) for t in FINE)
            assert contains(u, w) == want
        # reset of clock 1: w in Z[x1 := 0] iff w[0] = 0 and some value of x1 gives a point of Z
        r = reset(c, 1)
        assert canonical(r) == r
        for w in POINTS:
            want = w[0] == 0 and any(contains(c, (t, w[1])) for t in FINE)
            assert contains(r, w) == want
        # constrain and the incremental tightening agree with the full closure
        for _ in range(5):
            con = (rng.randint(1, N), rng.choice(["<", "<=", "==", ">=", ">"]), rng.randint(0, 4))
            z = constrain(c, con)
            x, op, k = con
            want = {v for v in pts if {"<": v[x - 1] < k, "<=": v[x - 1] <= k, "==": v[x - 1] == k, ">=": v[x - 1] >= k, ">": v[x - 1] > k}[op]}
            if z is None:
                assert not want
            else:
                assert z == canonical(z) and members(z) == want
        # inclusion is the entrywise order on canonical forms
        other = canonical(random_dbm(rng))
        if other is not None:
            assert includes(c, other) == (members(other) <= pts)
        # extrapolation only grows the zone
        e = extrapolate(c, [0] + [rng.randint(0, 3) for _ in range(N)])
        assert e is not None and pts <= members(e)


def test_extrapolation_is_finite() -> None:
    # without extrapolation, x - y grows with each loop and the zones never repeat
    k = [0, 1, 1]
    seen = set()
    z = zero(2)
    for _ in range(50):
        z = extrapolate(up(z), k)
        z = constrain(z, (2, "==", 1))
        z = reset(z, 2)
        seen.add(tuple(map(tuple, z)))
    assert len(seen) <= 3
    # the last zone is x > 2, y = 0: the extrapolated x > 1, then y = 1, then reset y
    assert z[1][0] == INF and z[0][1] == (-2, 0) and z[2][0] == LE0


# Oracles for reachability: the region graph and integer-step runs.


def region_locations(ta):
    n, k = ta["clocks"], max_constants(ta)
    inv = ta.get("inv", {})

    def sat(r, con):
        ints, zs, _ = r
        x, op, c = con
        i = ints[x]
        if i > k[x]:
            return op in (">", ">=")
        if x in zs:
            return {"<": i < c, "<=": i <= c, "==": i == c, ">=": i >= c, ">": i > c}[op]
        return {"<": i < c, "<=": i < c, "==": False, ">=": i >= c, ">": i >= c}[op]

    def succ(r):
        ints, zs, order = r
        ints = list(ints)
        if zs:
            moved = set()
            for x in zs:
                if ints[x] == k[x]:
                    ints[x] += 1
                else:
                    moved.add(x)
            return tuple(ints), frozenset(), ((frozenset(moved),) if moved else ()) + order
        if not order:
            return None
        for x in order[-1]:
            ints[x] += 1
        return tuple(ints), order[-1], order[:-1]

    def rst(r, ys):
        ints, zs, order = r
        ints = list(ints)
        for x in ys:
            ints[x] = 0
        ys = frozenset(ys)
        return tuple(ints), zs | ys, tuple(s - ys for s in order if s - ys)

    ok = lambda r, cons: all(sat(r, c) for c in cons)  # noqa: E731
    start = (ta["init"], ((0,) * (n + 1), frozenset(range(1, n + 1)), ()))
    if not ok(start[1], inv.get(ta["init"], [])):
        return set()
    seen, stack = {start}, [start]
    while stack:
        loc, r = stack.pop()
        nxt = []
        s = succ(r)
        if s is not None and ok(s, inv.get(loc, [])):
            nxt.append((loc, s))
        for src, g, ys, dst in ta["edges"]:
            if src == loc and ok(r, g):
                r2 = rst(r, ys)
                if ok(r2, inv.get(dst, [])):
                    nxt.append((dst, r2))
        for st in nxt:
            if st not in seen:
                seen.add(st)
                stack.append(st)
    return {loc for loc, _ in seen}


def integer_runs(ta):
    """Location reachability with integer delays only."""
    n, k = ta["clocks"], max_constants(ta)
    inv = ta.get("inv", {})

    def ok(v, cons):
        return all({"<": v[x] < c, "<=": v[x] <= c, "==": v[x] == c, ">=": v[x] >= c, ">": v[x] > c}[op] for x, op, c in cons)

    start = (ta["init"], (0,) * (n + 1))
    if not ok(start[1], inv.get(ta["init"], [])):
        return set()
    seen, stack = {start}, [start]
    while stack:
        loc, v = stack.pop()
        nxt = []
        d = (0,) + tuple(min(a + 1, k[x] + 1) for x, a in enumerate(v) if x)
        if ok(d, inv.get(loc, [])):
            nxt.append((loc, d))
        for src, g, ys, dst in ta["edges"]:
            if src == loc and ok(v, g):
                v2 = tuple(0 if x in ys else a for x, a in enumerate(v))
                if ok(v2, inv.get(dst, [])):
                    nxt.append((dst, v2))
        for st in nxt:
            if st not in seen:
                seen.add(st)
                stack.append(st)
    return {loc for loc, _ in seen}


def random_ta(rng, closed):
    n = rng.randint(1, 3)
    locs = [f"l{i}" for i in range(rng.randint(2, 5))]
    ops = ["<=", "==", ">="] if closed else ["<", "<=", "==", ">=", ">"]
    edges = []
    for _ in range(rng.randint(2, 7)):
        guard = [(rng.randint(1, n), rng.choice(ops), rng.randint(0, 3)) for _ in range(rng.randint(0, 2))]
        ys = [x for x in range(1, n + 1) if rng.random() < 0.4]
        edges.append((rng.choice(locs), guard, ys, rng.choice(locs)))
    inv = {}
    for loc in locs:
        if rng.random() < 0.3:
            inv[loc] = [(rng.randint(1, n), "<=" if closed or rng.random() < 0.5 else "<", rng.randint(1, 3))]
    return {"clocks": n, "init": locs[0], "edges": edges, "inv": inv}


def test_zone_graph_agrees_with_regions_and_integer_runs() -> None:
    rng = random.Random(43)
    for trial in range(500):
        closed = trial % 2 == 0
        ta = random_ta(rng, closed)
        locs = reachable_locations(ta)
        assert locs == region_locations(ta), ta
        if closed:
            assert locs == integer_runs(ta), ta
        else:
            assert integer_runs(ta) <= locs, ta


def test_example_automaton() -> None:
    ta = {
        "clocks": 2,
        "init": "l0",
        "edges": [
            ("l0", [(1, "<=", 1)], [2], "l1"),
            ("l1", [(1, ">=", 2), (2, "<=", 1)], [], "l2"),
            ("l1", [(1, ">=", 2), (2, "<", 1)], [], "l3"),
            ("l2", [], [1, 2], "l0"),
        ],
        "inv": {},
    }
    assert reachable_locations(ta) == {"l0", "l1", "l2"}
