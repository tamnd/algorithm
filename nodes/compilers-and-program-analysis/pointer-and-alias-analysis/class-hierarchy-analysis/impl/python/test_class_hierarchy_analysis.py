# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/class-hierarchy-analysis/. The authors are listed in prov/M6WV8Z.jsonl.

import random

import oomodel
from class_hierarchy_analysis import class_hierarchy_analysis
from oomodel import MAIN


def test_page_example():
    reach, edges = class_hierarchy_analysis(oomodel.shapes())
    grows = {("Shape", "grow"), ("Circle", "grow"), ("Square", "grow")}
    assert reach == {MAIN} | grows
    assert edges == {(s, t) for s in ("s1", "s2", "s3") for t in grows}


def test_lookup_walks_up_the_tree():
    prog = oomodel.shapes()
    assert oomodel.lookup(prog, "Oval", "grow") == ("Circle", "grow")
    assert oomodel.lookup(prog, "Square", "grow") == ("Square", "grow")


def test_no_calls():
    prog = {
        "classes": {"A": None},
        "methods": {},
        "fields": {},
        "bodies": {MAIN: ({"x": "A"}, [("new", "x", "A")])},
    }
    assert class_hierarchy_analysis(prog) == ({MAIN}, set())


def test_declared_type_limits_the_targets():
    # A receiver declared as Square cannot reach Circle.grow or Shape.grow.
    prog = oomodel.shapes()
    local, stmts = prog["bodies"][MAIN]
    local = dict(local, q="Square")
    prog["bodies"][MAIN] = (local, [("new", "q", "Square"), ("call", "s9", None, "q", "grow", None)])
    reach, edges = class_hierarchy_analysis(prog)
    assert edges == {("s9", ("Square", "grow"))}
    assert reach == {MAIN, ("Square", "grow")}


def test_unreachable_method_adds_no_edges():
    # The call in Shape.grow is never scanned when no site reaches Shape.grow.
    prog = oomodel.shapes()
    local, _ = prog["bodies"][MAIN]
    prog["bodies"][MAIN] = (local, [])
    prog["bodies"][("Shape", "grow")][1].append(("call", "s7", None, "this", "grow", None))
    assert class_hierarchy_analysis(prog) == ({MAIN}, set())


def test_same_as_plain_iteration():
    rng = random.Random(1995)
    for _ in range(500):
        prog = oomodel.random_program(rng, rng.randint(1, 7), rng.randint(1, 4), rng.randint(0, 2), 8)
        assert class_hierarchy_analysis(prog) == oomodel.cha_spec(prog), oomodel.show(prog)


def test_sound_against_concrete_runs():
    rng = random.Random(77)
    for _ in range(300):
        prog = oomodel.random_program(rng, rng.randint(2, 7), rng.randint(1, 4), rng.randint(0, 2), 8)
        reach, edges = class_hierarchy_analysis(prog)
        for _ in range(5):
            seen_edges, entered = oomodel.run(prog, rng)
            assert seen_edges <= edges, oomodel.show(prog)
            assert entered <= reach


def test_contains_rapid_type_analysis():
    rng = random.Random(5)
    for _ in range(300):
        prog = oomodel.random_program(rng, rng.randint(2, 7), rng.randint(1, 4), rng.randint(0, 2), 8)
        reach, edges = class_hierarchy_analysis(prog)
        rta_reach, rta_edges = oomodel.rta_spec(prog)
        assert rta_reach <= reach and rta_edges <= edges
