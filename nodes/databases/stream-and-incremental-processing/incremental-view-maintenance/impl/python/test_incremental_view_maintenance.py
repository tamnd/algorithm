# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/incremental-view-maintenance/. The authors are listed in prov/V5APR5.jsonl.

import random
from collections import Counter

from incremental_view_maintenance import (CountingView, Join, Project, Rel, Select, Union, apply_update, bag_add,
                                          delta, evaluate, join, row)

SCHEMA = {"R": ("a", "b"), "S": ("b", "c"), "T": ("c", "d")}


def rand_rows(rng, name, k, dom=3):
    return [tuple(sorted((a, rng.randrange(dom)) for a in SCHEMA[name])) for _ in range(k)]


def rand_set_db(rng):
    return {n: Counter(set(rand_rows(rng, n, rng.randrange(7)))) for n in SCHEMA}


def rand_set_update(rng, db):
    """Delete some existing tuples and insert some new ones (set semantics)."""
    d = {}
    for n in SCHEMA:
        dr = Counter()
        for t in list(db[n]):
            if rng.random() < 0.3:
                dr[t] -= 1
        for t in set(rand_rows(rng, n, rng.randrange(3))):
            if t not in db[n]:
                dr[t] += 1
        d[n] = dr
    return d


def rand_expr(rng):
    r, s, t = Rel("R"), Rel("S"), Rel("T")
    small_b = Select(lambda x: x["b"] < 2, s)
    choices = [
        Join(r, s),
        Project(frozenset("ac"), Join(r, s)),
        Project(frozenset("a"), Join(Join(r, s), t)),
        Project(frozenset("bd"), Join(s, t)),
        Join(Join(r, small_b), t),
        Union(Project(frozenset("b"), r), Project(frozenset("b"), s)),
        Project(frozenset("ad"), Join(Project(frozenset("ac"), Join(r, s)), t)),
        Union(Project(frozenset("c"), Join(r, s)), Project(frozenset("c"), Select(lambda x: x["d"] != 1, t))),
        Join(r, r),
        Project(frozenset("a"), Select(lambda x: x["a"] != x["c"], Join(r, s))),
    ]
    return rng.choice(choices)


def test_counting_view_matches_recomputation_on_random_updates():
    rng = random.Random(1993)
    checks = 0
    for _ in range(150):
        db = rand_set_db(rng)
        e = rand_expr(rng)
        v = CountingView(e, db)
        for _ in range(5):
            d = rand_set_update(rng, v.db)
            before = v.rows()
            ins, dele = v.maintain(d)
            want = evaluate(e, v.db)
            assert v.count == want  # counts are the bag multiplicities
            assert v.rows() == set(want)
            assert ins == v.rows() - before and dele == before - v.rows()
            assert all(c > 0 for c in v.count.values())
            checks += 1
    assert checks >= 500


def test_delta_rules_on_signed_bags():
    """E(D + dD) = E(D) + dE for bags with signed updates."""
    rng = random.Random(7)
    for _ in range(600):
        db = {n: Counter(rand_rows(rng, n, rng.randrange(6))) for n in SCHEMA}
        d = {}
        for n in SCHEMA:
            dr = Counter()
            for t in rand_rows(rng, n, rng.randrange(4)):
                dr[t] += rng.choice([-1, 1, 2])
            d[n] = dr
        e = rand_expr(rng)
        assert bag_add(evaluate(e, db), delta(e, db, d)) == evaluate(e, apply_update(db, d))


def test_join_needs_the_delta_delta_term():
    r = {"R": Counter({row(a=1, b=1): 1}), "S": Counter()}
    d = {"R": Counter({row(a=2, b=5): 1}), "S": Counter({row(b=5, c=9): 1})}
    e = Join(Rel("R"), Rel("S"))
    new = evaluate(e, apply_update(r, d))
    assert new == Counter({row(a=2, b=5, c=9): 1})
    two_terms = bag_add(join(d["R"], r["S"]), join(r["R"], d["S"]))
    assert bag_add(evaluate(e, r), two_terms) != new  # the new pair is missing
    assert bag_add(evaluate(e, r), delta(e, r, d)) == new


def test_worked_example_counts():
    # V = pi_a (R join S). Two derivations of a = 1: deleting one keeps it.
    db = {"R": Counter({row(a=1, b=1): 1, row(a=1, b=2): 1, row(a=2, b=3): 1}),
          "S": Counter({row(b=1, c=0): 1, row(b=2, c=0): 1, row(b=3, c=0): 1})}
    v = CountingView(Project(frozenset("a"), Join(Rel("R"), Rel("S"))), db)
    assert v.count == Counter({row(a=1): 2, row(a=2): 1})
    ins, dele = v.maintain({"S": Counter({row(b=1, c=0): -1})})
    assert (ins, dele) == (set(), set()) and v.count[row(a=1)] == 1
    ins, dele = v.maintain({"S": Counter({row(b=2, c=0): -1, row(b=4, c=0): 1}),
                            "R": Counter({row(a=3, b=4): 1})})
    assert ins == {row(a=3)} and dele == {row(a=1)}
    assert v.count == Counter({row(a=2): 1, row(a=3): 1})


def test_no_change_means_no_work():
    calls = Counter()

    def pred(x):
        calls["p"] += 1
        return True

    db = {"R": Counter({row(a=1, b=1): 1}), "S": Counter({row(b=1, c=1): 1})}
    e = Join(Select(pred, Rel("R")), Rel("S"))
    assert delta(e, db, {"T": Counter({row(c=1, d=1): 1})}) == Counter()
    assert calls["p"] == 0
