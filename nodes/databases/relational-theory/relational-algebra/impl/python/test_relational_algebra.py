# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/relational-algebra/. The authors are listed in prov/NEME20.jsonl.

import random

from relational_algebra import (
    Relation,
    difference,
    division,
    evaluate,
    intersection,
    natural_join,
    natural_join_direct,
    product,
    project,
    rename,
    select,
    union,
)

EMP = Relation(
    ["Name", "Dept", "Salary"],
    [
        {"Name": "Ann", "Dept": "R&D", "Salary": 70},
        {"Name": "Bob", "Dept": "R&D", "Salary": 50},
        {"Name": "Cid", "Dept": "Sales", "Salary": 60},
        {"Name": "Dee", "Dept": "HR", "Salary": 40},
    ],
)
DEPT = Relation(
    ["Dept", "Building"],
    [{"Dept": "R&D", "Building": "B1"}, {"Dept": "Sales", "Building": "B2"}, {"Dept": "Ops", "Building": "B2"}],
)
DB = {"Emp": EMP, "Dept": DEPT}


def rand_rel(rng: random.Random, schema: list, n: int, d: int = 3) -> Relation:
    return Relation(schema, [{a: rng.randrange(d) for a in schema} for _ in range(n)])


def test_example() -> None:
    q = ("project", ["Name"], ("select", ("lt", ("const", 55), "Salary"), ("join", ("rel", "Emp"), ("rel", "Dept"))))
    assert evaluate(q, DB).tuples() == [{"Name": "Ann"}, {"Name": "Cid"}]
    j = evaluate(("join", ("rel", "Emp"), ("rel", "Dept")), DB)
    assert len(j) == 3
    assert len(product(EMP, rename(DEPT, {"Dept": "D2"}))) == 12
    q2 = ("diff", ("project", ["Dept"], ("rel", "Dept")), ("project", ["Dept"], ("rel", "Emp")))
    assert evaluate(q2, DB).tuples() == [{"Dept": "Ops"}]


def test_division() -> None:
    takes = Relation(
        ["S", "C"],
        [{"S": s, "C": c} for s, c in [("ann", "db"), ("ann", "os"), ("bob", "db"), ("cid", "os"), ("cid", "db"), ("cid", "ai")]],
    )
    req = Relation(["C"], [{"C": "db"}, {"C": "os"}])
    assert division(takes, req).tuples() == [{"S": "ann"}, {"S": "cid"}]
    assert division(takes, Relation(["C"], [])) == project(takes, ["S"])


def test_edges() -> None:
    empty = Relation(["A"], [])
    one = Relation(["A"], [{"A": 1}])
    assert len(product(one, Relation(["B"], []))) == 0
    assert product(one, Relation([], [{}])) == one
    assert project(one, []) == Relation([], [{}])
    assert project(empty, []) == Relation([], [])
    assert natural_join(one, Relation(["B"], [{"B": 2}])) == Relation(["A", "B"], [{"A": 1, "B": 2}])
    assert natural_join(one, one) == one


def test_join_derived_equals_direct() -> None:
    rng = random.Random(1)
    for _ in range(200):
        r = rand_rel(rng, ["A", "B", "C"], rng.randint(0, 8))
        s = rand_rel(rng, rng.sample(["B", "C", "D", "E"], rng.randint(1, 3)), rng.randint(0, 8))
        assert natural_join(r, s) == natural_join_direct(r, s)


def test_algebraic_laws() -> None:
    rng = random.Random(2)
    for _ in range(200):
        r = rand_rel(rng, ["A", "B", "C"], rng.randint(0, 8))
        r2 = rand_rel(rng, ["A", "B", "C"], rng.randint(0, 8))
        s = rand_rel(rng, ["C", "D"], rng.randint(0, 8))
        t = rand_rel(rng, ["D", "E"], rng.randint(0, 8))
        p = ("eq", "A", ("const", rng.randrange(3)))
        q = ("lt", "B", "C")
        # Selection pushes through a join when it uses only attributes of one side.
        assert select(natural_join(r, s), p) == natural_join(select(r, p), s)
        # Selections commute and merge.
        assert select(select(r, p), q) == select(select(r, q), p) == select(r, ("and", p, q))
        # Projection is idempotent, and a cascade of projections keeps the last one.
        assert project(project(r, ["A", "B"]), ["A", "B"]) == project(r, ["A", "B"])
        assert project(project(r, ["A", "B"]), ["A"]) == project(r, ["A"])
        # Join is commutative and associative.
        assert natural_join(r, s) == natural_join(s, r)
        assert natural_join(natural_join(r, s), t) == natural_join(r, natural_join(s, t))
        # Selection distributes over union and difference.
        assert select(union(r, r2), p) == union(select(r, p), select(r2, p))
        assert select(difference(r, r2), p) == difference(select(r, p), select(r2, p))
        # Intersection, from difference.
        assert intersection(r, r2).rows == r.rows & r2.rows
        # Projection distributes over union, and is a subset on difference.
        assert project(union(r, r2), ["A"]) == union(project(r, ["A"]), project(r2, ["A"]))
        assert difference(project(r, ["A"]), project(r2, ["A"])).rows <= project(difference(r, r2), ["A"]).rows
        # The size of a product.
        assert len(product(r, t)) == len(r) * len(t)


def test_projection_does_not_distribute_over_difference() -> None:
    r = Relation(["A", "B"], [{"A": 1, "B": 1}])
    s = Relation(["A", "B"], [{"A": 1, "B": 2}])
    assert project(difference(r, s), ["A"]).tuples() == [{"A": 1}]
    assert difference(project(r, ["A"]), project(s, ["A"])).tuples() == []
