# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/path-based-scheduling/. The authors are listed in prov/60ZARY.jsonl.

import itertools
import random

from path_based_scheduling import (all_paths, all_rows, exact_hitting_set, greedy_hitting_set,
                                   is_valid, path_based_schedule, path_constraints, stab_intervals)

# a = x * y (delay 2), b = a + 1 (delay 1), then c = b + u or d = b - u (delay 1). Period 3.
SUCC = {"a": ["b"], "b": ["c", "d"]}
KIND = {"a": "mul", "b": "add", "c": "add", "d": "add"}
DELAY = {"a": 2, "b": 1, "c": 1, "d": 1}


def random_cfg(rng: random.Random, max_ops: int):
    """A chain of single operations and if/else diamonds with at most max_ops operations."""
    succ: dict = {}
    kind: dict = {}
    delay: dict = {}
    count = 0

    def new():
        nonlocal count
        v = count
        count += 1
        kind[v] = rng.choice("mma")
        delay[v] = rng.randint(1, 3)
        return v

    entry = new()
    tails = [entry]
    while count < max_ops:
        if count + 3 <= max_ops and rng.random() < 0.5:
            left = [new() for _ in range(rng.randint(1, 2 if count + 4 <= max_ops else 1))]
            right = [new() for _ in range(1)]
            for arm in (left, right):
                for t in tails:
                    succ.setdefault(t, []).append(arm[0])
                for x, y in zip(arm, arm[1:]):
                    succ.setdefault(x, []).append(y)
            tails = [left[-1], right[-1]]
        else:
            v = new()
            for t in tails:
                succ.setdefault(t, []).append(v)
            tails = [v]
    return succ, entry, kind, delay


def test_example():
    rows = all_rows(SUCC, "a", KIND, DELAY, {"mul"}, 3)
    assert rows == {frozenset({("a", "b"), ("b", "c")}), frozenset({("a", "b"), ("b", "d")})}
    cuts, per_path = path_based_schedule(SUCC, "a", KIND, DELAY, {"mul"}, 3)
    assert cuts == {("a", "b")}
    assert [(a, b) for (_, a, b) in per_path] == [(2, 2), (2, 2)]
    assert is_valid(SUCC, "a", KIND, DELAY, {"mul"}, 3, cuts)
    # The right end cut of each path alone needs two edges.
    union = set()
    for p in all_paths(SUCC, "a"):
        for t in stab_intervals(path_constraints(p, KIND, DELAY, {"mul"}, 3)):
            union.add((p[t], p[t + 1]))
    assert union == {("b", "c"), ("b", "d")}


def test_stabbing_against_all_subsets():
    rng = random.Random(31)
    for _ in range(300):
        m = rng.randint(1, 7)
        iv = []
        for _ in range(rng.randint(0, 6)):
            lo = rng.randrange(m)
            iv.append((lo, rng.randint(lo, m - 1)))
        cuts = stab_intervals(iv)
        assert all(any(lo <= c <= hi for c in cuts) for lo, hi in iv)
        best = next(k for k in range(m + 1) for s in itertools.combinations(range(m), k)
                    if all(any(lo <= c <= hi for c in s) for lo, hi in iv))
        assert len(cuts) == best


def test_schedule_is_valid_and_between_bounds():
    rng = random.Random(32)
    worse = 0
    for _ in range(150):
        succ, entry, kind, delay = random_cfg(rng, 8)
        cuts, per_path = path_based_schedule(succ, entry, kind, delay, {"m"}, 3)
        assert is_valid(succ, entry, kind, delay, {"m"}, 3, cuts)
        best = exact_hitting_set(all_rows(succ, entry, kind, delay, {"m"}, 3))
        assert is_valid(succ, entry, kind, delay, {"m"}, 3, best)
        lower = max(a for (_, a, _) in per_path) - 1
        assert lower <= len(best) <= len(cuts)
        for (_, a, b) in per_path:
            assert a <= b
        worse += len(cuts) > len(best)
    assert worse < 150


def test_valid_cuts_are_exactly_hitting_sets():
    rng = random.Random(33)
    for _ in range(60):
        succ, entry, kind, delay = random_cfg(rng, 6)
        rows = all_rows(succ, entry, kind, delay, {"m"}, 3)
        edges = sorted({(u, v) for u in succ for v in succ[u]})
        for mask in range(1 << len(edges)):
            s = {e for i, e in enumerate(edges) if mask >> i & 1}
            assert is_valid(succ, entry, kind, delay, {"m"}, 3, s) == all(r & s for r in rows)


def vertex_cover_dag(n: int, graph_edges):
    """The reduction of the page: one edge x_i per vertex and a connector per graph edge."""
    succ: dict = {}
    for i in range(n):
        succ.setdefault(("a", i), []).append(("b", i))
    rows = set()
    for i, k in graph_edges:
        succ.setdefault(("b", i), []).append(("a", k))
        rows.add(frozenset({(("a", i), ("b", i)), (("b", i), ("a", k)), (("a", k), ("b", k))}))
    return succ, rows


def test_vertex_cover_reduction():
    rng = random.Random(34)
    for _ in range(80):
        n = rng.randint(1, 6)
        ge = [(i, k) for i in range(n) for k in range(i + 1, n) if rng.random() < 0.4]
        _, rows = vertex_cover_dag(n, ge)
        vc = next(k for k in range(n + 1) for s in itertools.combinations(range(n), k)
                  if all(i in s or k2 in s for i, k2 in ge))
        assert len(exact_hitting_set(rows)) == vc


def test_greedy_hitting_set_hits_everything():
    rng = random.Random(35)
    for _ in range(200):
        universe = list(range(rng.randint(1, 8)))
        rows = {frozenset(rng.sample(universe, rng.randint(1, len(universe)))) for _ in range(rng.randint(0, 6))}
        h = greedy_hitting_set(rows)
        assert all(r & h for r in rows)
        assert len(exact_hitting_set(rows)) <= len(h)
