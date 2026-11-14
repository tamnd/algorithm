# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hybrid-cycle-detection/. The authors are listed in prov/NC36D7.jsonl.

import random

import ptsgen
from hybrid_cycle_detection import hybrid, offline_plan, points_to

PAGE = """
entry:
  a = &x
  a = &y
  b = *a
  c = b
  *a = c
  y = &z
  ret 0
"""

MODES = [(True, True), (True, False), (False, True), (False, False)]


def test_page_example():
    stmts = ptsgen.parse(PAGE)
    groups, table = offline_plan(stmts)
    assert groups == [] and table == {"a": [("b", ())]}
    pts, stats = hybrid(stmts)
    assert pts == ptsgen.least_solution(stmts)
    assert pts["a"] == {"x", "y"}
    assert pts["b"] == pts["c"] == pts["x"] == pts["y"] == {"z"}
    assert stats == {"offline": 0, "hcd": 2, "lcd": 1, "searches": 1}


def test_offline_copy_cycle():
    stmts = ptsgen.parse("p = &a\nq = p\nr = q\np = r")
    pts, stats = hybrid(stmts)
    assert stats["offline"] == 2 and stats["searches"] == 0
    assert pts["p"] == pts["q"] == pts["r"] == {"a"}


def test_hcd_waits_for_other_ref_nodes():
    # The offline cycle *a -> b -> *c -> q -> *a needs a target for c too.
    # While c points nowhere, x and b do not have equal least sets.
    stmts = ptsgen.parse("a = &x\nb = &w\nb = *a\n*c = b\nq = *c\n*a = q")
    groups, table = offline_plan(stmts)
    assert table["a"] == [("b", ("c",))]
    pts, stats = hybrid(stmts)
    assert stats["hcd"] == 0
    assert pts["x"] == set() and pts["b"] == {"w"}
    assert pts == ptsgen.least_solution(stmts)
    # Once c has a target, the cycle is real and the merge is safe.
    more = stmts + [("addr", "c", "y")]
    pts, stats = hybrid(more)
    assert stats["hcd"] >= 1
    assert pts == ptsgen.least_solution(more)
    assert pts["x"] == pts["b"]


def test_equals_andersen_on_random_programs():
    rng = random.Random(6100)
    total = {"offline": 0, "hcd": 0, "lcd": 0}
    for trial in range(300):
        stmts = ptsgen.random_program(rng, rng.randint(2, 12), rng.randint(1, 30))
        least = ptsgen.least_solution(stmts)
        for lazy, offline in MODES:
            pts, stats = hybrid(stmts, lazy, offline)
            assert pts == least, (lazy, offline, ptsgen.show(stmts))
            if lazy and offline:
                for k in total:
                    total[k] += stats[k]
    assert all(total[k] > 20 for k in total)  # every kind of merge happens


def test_merged_nodes_have_equal_least_sets():
    rng = random.Random(6200)
    for trial in range(300):
        stmts = ptsgen.random_program(rng, rng.randint(2, 12), 30, (2, 4, 3, 3))
        assert hybrid(stmts)[0] == ptsgen.least_solution(stmts), ptsgen.show(stmts)


def test_sound_against_concrete_runs():
    rng = random.Random(6300)
    for trial in range(150):
        stmts = ptsgen.random_program(rng, rng.randint(3, 10), 30)
        pts = points_to(ptsgen.show(stmts))
        for p, a in ptsgen.concrete_facts(stmts, rng, runs=10, steps=150):
            assert a in pts[p]


def test_long_cycles():
    n = 2000
    text = "\n".join(["v0 = &a"] + ["v%d = v%d" % ((i + 1) % n, i) for i in range(n)])
    pts, stats = hybrid(ptsgen.parse(text))
    assert all(pts["v%d" % i] == {"a"} for i in range(n))
    assert stats["offline"] == n - 1
    # The same cycle, found online by the lazy check alone.
    pts, stats = hybrid(ptsgen.parse(text), lazy=True, offline=False)
    assert all(pts["v%d" % i] == {"a"} for i in range(n))
    assert stats["lcd"] == n - 1 and stats["searches"] == 1
