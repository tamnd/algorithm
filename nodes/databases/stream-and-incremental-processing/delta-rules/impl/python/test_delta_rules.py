# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/delta-rules/. The authors are listed in prov/Q8ZX00.jsonl.

import random
from collections import Counter

import dbrel
from delta_rules import delta, maintain, new_db, zjoin

R = ("scan", "R")
S = ("scan", "S")
T = ("scan", "T")

EXPRS = [
    ("join", R, S),
    ("project", ("A",), ("join", R, S)),
    ("select", lambda r: dbrel.cmp3("<>", r["B"], 1), R),
    ("union", R, T),
    ("difference", R, T),
    ("intersection", R, T),
    ("distinct", ("project", ("A",), R)),
    ("aggregate", ("B",), [("count_star", None, "n"), ("sum", "A", "s"), ("count", "A", "k")], ("join", R, S)),
    ("aggregate", (), [("count_star", None, "n"), ("sum", "C", "s")], S),
    ("join", ("join", R, S), ("rename", {"A": "C", "B": "E"}, T)),
    ("difference", ("project", ("A",), R), ("project", ("A",), T)),
    ("distinct", ("difference", R, T)),
    ("product", ("project", ("A",), R), ("rename", {"B": "E", "C": "F"}, S)),
]


def random_db(rng, null_rate=0.1):
    return {
        "R": dbrel.random_relation(rng, ("A", "B"), rng.randrange(0, 9), 3, null_rate=null_rate),
        "S": dbrel.random_relation(rng, ("B", "C"), rng.randrange(0, 9), 3, null_rate=null_rate),
        "T": dbrel.random_relation(rng, ("A", "B"), rng.randrange(0, 9), 3, null_rate=null_rate),
    }


def random_change(rng, db, null_rate=0.1):
    dd = {}
    for name, rel in db.items():
        d = Counter()
        for t, c in rel.rows.items():
            if rng.random() < 0.4:
                d[t] -= rng.randrange(1, c + 1)
        ins = dbrel.random_relation(rng, rel.schema, rng.randrange(0, 4), 3, null_rate=null_rate)
        d.update(ins.rows)
        dd[name] = Counter({t: w for t, w in d.items() if w})
    return dd


def test_page_example() -> None:
    db = {"R": dbrel.Relation(("A", "B"), [(1, 10), (2, 10), (3, 20)]),
          "S": dbrel.Relation(("B", "C"), [(10, "x"), (20, "y")])}
    dd = {"R": Counter({(4, 20): 1, (1, 10): -1}), "S": Counter({(20, "z"): 1})}
    sch, d = delta(("join", R, S), db, dd)
    assert sch == ("A", "B", "C")
    assert d == Counter({(1, 10, "x"): -1, (3, 20, "z"): 1, (4, 20, "y"): 1, (4, 20, "z"): 1})
    # Without the term dR join dS the change misses (4, 20, z).
    _, a = zjoin(("A", "B"), dd["R"], ("B", "C"), db["S"].rows)
    _, b = zjoin(("A", "B"), db["R"].rows, ("B", "C"), dd["S"])
    assert (a + b)[(4, 20, "z")] == 0 and len(+(a + b)) == 2
    # Monus: R has (5, 1) twice, T once; deleting it from T raises R - T from 1 to 2.
    db2 = {"R": dbrel.Relation(("A", "B"), [(5, 1), (5, 1)]), "T": dbrel.Relation(("A", "B"), [(5, 1)])}
    assert delta(("difference", R, T), db2, {"T": Counter({(5, 1): -1})})[1] == Counter({(5, 1): 1})
    # Deleting one of the two copies from R instead lowers R - T to 0.
    assert delta(("difference", R, T), db2, {"R": Counter({(5, 1): -1})})[1] == Counter({(5, 1): -1})


def test_against_recomputation() -> None:
    for seed in range(120):
        rng = random.Random(seed)
        db = random_db(rng)
        for expr in EXPRS:
            view = dbrel.evaluate(expr, db)
            cur = db
            for _ in range(3):
                dd = random_change(rng, cur)
                view = maintain(view, expr, cur, dd)
                cur = new_db(cur, dd)
                assert view == dbrel.evaluate(expr, cur)


def test_only_changed_tuples_appear() -> None:
    # A change that touches no tuple gives an empty delta for every expression.
    rng = random.Random(1)
    db = random_db(rng, 0.0)
    for expr in EXPRS:
        assert not delta(expr, db, {})[1]


def test_set_case_by_distinct() -> None:
    # Set semantics: the view distinct(project_A(R)) changes only when a value appears or disappears.
    db = {"R": dbrel.Relation(("A", "B"), [(1, 1), (1, 2), (2, 1)])}
    expr = ("distinct", ("project", ("A",), R))
    assert delta(expr, db, {"R": Counter({(1, 1): -1})})[1] == Counter()
    assert delta(expr, db, {"R": Counter({(2, 1): -1, (3, 3): 1})})[1] == Counter({(2,): -1, (3,): 1})
