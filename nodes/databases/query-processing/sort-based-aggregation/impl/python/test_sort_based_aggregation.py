# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sort-based-aggregation/. The authors are listed in prov/ZDF77H.jsonl.

import random
from collections import Counter
from fractions import Fraction

import pytest

import dbrel
from dbrel import Relation
from sort_based_aggregation import sort_aggregate, sort_cost

# ---------------------------------------------------------------- the helper dbrel
# A hand example with duplicates and a null for each operator.

R = Relation(("A", "B"), [(1, "x"), (1, "x"), (2, None), (None, "y")])
S = Relation(("B", "C"), [("x", 10), ("x", 20), (None, 30)])


def test_relation_counts_and_modes() -> None:
    assert R.rows == Counter({(1, "x"): 2, (2, None): 1, (None, "y"): 1})
    assert len(R) == 4
    assert R.with_mode("set").rows == Counter({(1, "x"): 1, (2, None): 1, (None, "y"): 1})
    assert Relation(("B", "A"), [("x", 1), ("x", 1), (None, 2), ("y", None)]) == R
    assert Relation(("A", "B"), {(1, "x"): 2}) != R
    assert R.sorted_rows() == [(None, "y"), (1, "x"), (1, "x"), (2, None)]
    with pytest.raises(ValueError):
        Relation(("A", "A"), [])
    with pytest.raises(ValueError):
        Relation(("A",), [(1, 2)])
    with pytest.raises(ValueError):
        dbrel.union(R, R.with_mode("set"))


def test_three_valued_logic() -> None:
    order = {False: 0, None: 1, True: 2}
    back = {0: False, 1: None, 2: True}
    vals = [True, False, None]
    for a in vals:
        assert dbrel.tv_not(a) == back[2 - order[a]]
        for b in vals:
            assert dbrel.tv_and(a, b) is back[min(order[a], order[b])]
            assert dbrel.tv_or(a, b) is back[max(order[a], order[b])]
    assert dbrel.cmp3("=", None, None) is None
    assert dbrel.cmp3("<>", 1, None) is None
    assert dbrel.cmp3("<", 1, 2) is True and dbrel.cmp3(">=", 1, 2) is False
    assert not dbrel.is_true(None) and dbrel.is_true(True)


def test_select_keeps_only_true() -> None:
    got = dbrel.select(R, lambda t: dbrel.cmp3("=", t["B"], "x"))
    assert got.rows == Counter({(1, "x"): 2})
    # NOT (B = 'x') drops the null row too: NOT UNKNOWN is UNKNOWN.
    got = dbrel.where(R, lambda t: dbrel.tv_not(dbrel.cmp3("=", t["B"], "x")))
    assert got.rows == Counter({(None, "y"): 1})


def test_project_rename_distinct() -> None:
    assert dbrel.project(R, ["B"]).rows == Counter({("x",): 2, (None,): 1, ("y",): 1})
    assert dbrel.project(R.with_mode("set"), ["B"]).rows == Counter({("x",): 1, (None,): 1, ("y",): 1})
    assert dbrel.rename(R, {"A": "Z"}).schema == ("Z", "B")
    assert dbrel.distinct(R).rows == Counter({(1, "x"): 1, (2, None): 1, (None, "y"): 1})
    with pytest.raises(ValueError):
        dbrel.rename(R, {"Q": "Z"})


def test_union_difference_intersection() -> None:
    T = Relation(("B", "A"), [("x", 1), (None, 2), (None, 2), ("z", 3)])
    assert dbrel.union(R, T).rows == Counter({(1, "x"): 3, (2, None): 3, (None, "y"): 1, (3, "z"): 1})
    # Bag difference is monus: max(0, m - n). Two nulls are the same value here.
    assert dbrel.difference(R, T).rows == Counter({(1, "x"): 1, (None, "y"): 1})
    assert dbrel.intersection(R, T).rows == Counter({(1, "x"): 1, (2, None): 1})
    Rs, Ts = R.with_mode("set"), T.with_mode("set")
    assert dbrel.difference(Rs, Ts).rows == Counter({(None, "y"): 1})
    assert dbrel.union(Rs, Ts).rows == Counter({(1, "x"): 1, (2, None): 1, (None, "y"): 1, (3, "z"): 1})


def test_product_and_joins() -> None:
    U = Relation(("C",), [(5,), (5,)])
    assert dbrel.product(R, U).rows == Counter({(1, "x", 5): 4, (2, None, 5): 2, (None, "y", 5): 2})
    with pytest.raises(ValueError):
        dbrel.product(R, S)
    # A null in a join attribute never matches, not even another null.
    assert dbrel.natural_join(R, S).rows == Counter({(1, "x", 10): 2, (1, "x", 20): 2})
    assert dbrel.natural_join(R, U) == dbrel.product(R, U)
    got = dbrel.theta_join(R, U, lambda t: dbrel.cmp3("<", t["A"], t["C"]))
    assert got.rows == Counter({(1, "x", 5): 4, (2, None, 5): 2})
    assert dbrel.semijoin(R, S).rows == Counter({(1, "x"): 2})
    assert dbrel.antijoin(R, S).rows == Counter({(2, None): 1, (None, "y"): 1})


def test_aggregate_sql_rules() -> None:
    aggs = [("count_star", None, "n"), ("count", "A", "c"), ("count_distinct", "A", "cd"),
            ("sum", "A", "s"), ("avg", "A", "a"), ("min", "A", "lo"), ("max", "A", "hi")]
    got = dbrel.aggregate(R, ["B"], aggs)
    assert got.schema == ("B", "n", "c", "cd", "s", "a", "lo", "hi")
    # GROUP BY puts the null in its own group; the 'y' group has only a null A.
    assert got.rows == Counter({(None, 1, 1, 1, 2, Fraction(2), 2, 2): 1,
                                ("x", 2, 2, 1, 2, Fraction(1), 1, 1): 1,
                                ("y", 1, 0, 0, None, None, None, None): 1})
    # A scalar aggregate of an empty input gives one row; a grouped one gives none.
    empty = Relation(("A", "B"), [])
    assert dbrel.aggregate(empty, [], aggs).rows == Counter({(0, 0, 0, None, None, None, None): 1})
    assert len(dbrel.aggregate(empty, ["B"], aggs)) == 0
    assert dbrel.agg_value("avg", [1, 2.5]) == 1.75
    with pytest.raises(ValueError):
        dbrel.aggregate(R, [], [("median", "A", "m")])


def test_evaluate_tree() -> None:
    db = {"R": R, "S": S}
    expr = ("project", ["A", "C"],
            ("join", ("scan", "R"), ("select", lambda t: dbrel.cmp3(">", t["C"], 10), ("scan", "S"))))
    assert dbrel.evaluate(expr, db).rows == Counter({(1, 20): 2})
    assert dbrel.evaluate(expr, db, "set").rows == Counter({(1, 20): 1})
    agg = ("aggregate", ["B"], [("count_star", None, "n")], ("scan", "R"))
    assert dbrel.evaluate(agg, db) == dbrel.aggregate(R, ["B"], [("count_star", None, "n")])
    for op in ("union", "difference", "intersection"):
        assert dbrel.evaluate((op, ("scan", "R"), ("scan", "R")), db) == getattr(dbrel, op)(R, R)
    for op, f in (("semijoin", dbrel.semijoin), ("antijoin", dbrel.antijoin)):
        assert dbrel.evaluate((op, ("scan", "R"), ("scan", "S")), db) == f(R, S)
    assert dbrel.evaluate(("distinct", ("rename", {"A": "Z"}, ("scan", "R"))), db).schema == ("Z", "B")
    with pytest.raises(ValueError):
        dbrel.evaluate(("sort", ("scan", "R")), db)


def test_disk_and_paginate() -> None:
    assert dbrel.paginate(range(5), 2) == [[0, 1], [2, 3], [4]]
    d = dbrel.Disk()
    ids = d.load([(i,) for i in range(5)], 2)
    assert ids == [0, 1, 2] and d.io() == 0
    assert d.read_page(2) == [(4,)]
    pid = d.alloc()
    d.write_page(pid, [(9,)])
    assert (d.reads, d.writes, d.io()) == (1, 1, 2)
    d.free(pid)
    assert pid not in d.pages
    d.reset_counters()
    assert d.io() == 0
    with pytest.raises(KeyError):
        d.write_page(99, [])


def test_random_relation() -> None:
    a = dbrel.random_relation(random.Random(7), ("A", "B"), 50, {"A": 3, "B": ["p", "q"]}, null_rate=0.2)
    b = dbrel.random_relation(random.Random(7), ("A", "B"), 50, {"A": 3, "B": ["p", "q"]}, null_rate=0.2)
    assert a == b and len(a) == 50
    assert any(None in t for t in a.rows)
    assert all(t[0] in (0, 1, 2, None) and t[1] in ("p", "q", None) for t in a.rows)
    assert len(dbrel.random_relation(random.Random(1), ("A",), 30, 3, mode="set")) <= 3


# ---------------------------------------------------------------- sort-based aggregation

FUNCS = ["count_star", "count", "sum", "avg", "min", "max"]


def run(rows, key, aggs, B, p, early=True):
    """Load rows on a fresh disk, aggregate, and return (result, disk, stats)."""
    disk = dbrel.Disk()
    ids = disk.load(rows, p)
    stats: dict = {}
    out = sort_aggregate(disk, ids, key, aggs, B, p, early=early, stats=stats)
    assert sorted(disk.pages) == ids  # every run page was freed
    return out, disk, stats


def reference(rel, key_attrs, aggs):
    """The same query by the definition, with dbrel.aggregate."""
    sch = rel.schema
    named = [(f, None if c is None else sch[c], "o%d" % i) for i, (f, c) in enumerate(aggs)]
    return dbrel.aggregate(rel, key_attrs, named)


def early_cost(rows, key, B, p):
    """Page I/Os with early aggregation, from the distinct keys of each input page.

    A run written for a set of input pages holds one record per distinct key of
    those pages, so it has ceil(keys / p) pages. No sorting is done here.
    """
    pages = [{tuple(r[i] for i in key) for r in pg} for pg in dbrel.paginate(rows, p)]
    N = len(pages)
    if N <= B:
        return N
    runs = [set().union(*pages[i:i + B]) for i in range(0, N, B)]
    size = lambda s: -(-len(s) // p)
    cost = N + sum(size(s) for s in runs)
    while len(runs) > B - 1:
        groups = [runs[i:i + B - 1] for i in range(0, len(runs), B - 1)]
        cost += sum(size(s) for s in runs)
        runs = [set().union(*g) for g in groups]
        cost += sum(size(s) for s in runs)
    return cost + sum(size(s) for s in runs)


def test_worked_example() -> None:
    rows = [("d", 4), ("b", 2), ("a", 5), ("c", 1), ("b", 7), ("a", 3), ("d", 6), ("c", None),
            ("a", 2), ("e", 8), ("b", 1), ("a", 4), ("e", 3), ("c", 5), ("d", 2), ("b", 6)]
    aggs = [("count_star", None), ("sum", 1)]
    want = [("a", 4, 14), ("b", 4, 16), ("c", 3, 6), ("d", 3, 12), ("e", 2, 11)]
    out, disk, st = run(rows, [0], aggs, B=3, p=2, early=False)
    assert out == want
    assert (disk.reads, disk.writes) == (24, 16) and st == {"runs": [3, 2], "passes": 3}
    assert disk.io() == sort_cost(8, 3) == 40
    out, disk, st = run(rows, [0], aggs, B=3, p=2, early=True)
    assert out == want
    # Pass 0 writes runs of 4, 5 and 4 keys (2 + 3 + 2 pages); pass 1 writes 3 + 2 pages.
    assert (disk.reads, disk.writes) == (20, 12) and st == {"runs": [3, 2], "passes": 3}
    assert disk.io() == early_cost(rows, [0], 3, 2) == 32


def test_against_definition_random() -> None:
    rng = random.Random(2024)
    for trial in range(120):
        n = rng.randrange(0, 80)
        rel = dbrel.random_relation(rng, ("A", "B", "C"), n, {"A": 4, "B": ["u", "v", "w"], "C": 5},
                                    null_rate=rng.choice([0.0, 0.15]))
        rows = rel.sorted_rows()
        rng.shuffle(rows)
        key = rng.choice([[], [0], [1], [0, 1], [1, 0]])
        aggs = [(f, None if f == "count_star" else 2) for f in rng.sample(FUNCS, 3)]
        B, p = rng.choice([3, 4, 5]), rng.choice([1, 2, 3])
        early = trial % 2 == 0
        out, disk, _ = run(rows, key, aggs, B, p, early)
        want = reference(rel, [rel.schema[i] for i in key], aggs)
        got = Relation(want.schema, out)
        assert got == want, (trial, key, aggs)
        ks = [dbrel.row_key(r[:len(key)]) for r in out]
        assert ks == sorted(ks) and len(set(ks)) == len(ks)
        if early:
            assert disk.io() == early_cost(rows, key, B, p)
        else:
            assert disk.io() == sort_cost(len(dbrel.paginate(rows, p)), B)


def test_cost_formula_without_early_aggregation() -> None:
    # 2 N P - N with P = 1 + ceil(log_{B-1} ceil(N / B)); N <= B is one read pass.
    for N, B, P in [(3, 3, 1), (6, 3, 2), (8, 3, 3), (20, 3, 4), (30, 3, 5), (40, 5, 3), (100, 11, 2)]:
        rows = [(i % 7, i) for i in range(2 * N)]
        _, disk, st = run(rows, [0], [("sum", 1)], B, 2, early=False)
        assert st["passes"] == P
        assert disk.io() == sort_cost(N, B) == 2 * N * P - N


def test_early_aggregation_saves_io() -> None:
    rng = random.Random(5)
    rows = [(rng.randrange(4), rng.randrange(10)) for _ in range(120)]
    plain, d1, s1 = run(rows, [0], [("sum", 1), ("max", 1)], 3, 2, early=False)
    early, d2, s2 = run(rows, [0], [("sum", 1), ("max", 1)], 3, 2, early=True)
    assert plain == early
    # 60 pages and 6 passes. With 4 keys, each early run has at most 2 pages,
    # so each pass after the input scan moves at most 2 pages per run.
    assert d1.io() == sort_cost(60, 3) == 2 * 60 * 6 - 60 == 660
    assert d2.io() == early_cost(rows, [0], 3, 2) == 208
    assert s1["runs"] == s2["runs"] == [20, 10, 5, 3, 2]


def test_edge_cases() -> None:
    aggs = [("count_star", None), ("count", 1), ("sum", 1), ("avg", 1), ("min", 1), ("max", 1)]
    assert run([], [0], aggs, 3, 2)[0] == []
    assert run([], [], aggs, 3, 2)[0] == [(0, 0, None, None, None, None)]
    assert run([("k", 4)], [0], aggs, 3, 2)[0] == [("k", 1, 1, 4, Fraction(4), 4, 4)]
    same = [("k", i) for i in range(30)]
    assert run(same, [0], aggs, 3, 2)[0] == [("k", 30, 30, 435, Fraction(29, 2), 0, 29)]
    nulls = [(None, None), (None, 3), ("k", None), (None, None)]
    assert run(nulls, [0], aggs, 3, 1)[0] == [(None, 3, 1, 3, Fraction(3), 3, 3),
                                              ("k", 1, 0, None, None, None, None)]
    with pytest.raises(ValueError):
        run([(1, 2)], [0], aggs, 2, 2)
    with pytest.raises(ValueError):
        run([(1, 2)], [0], [("median", 1)], 3, 2)
