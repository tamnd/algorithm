# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rapid-type-analysis/. The authors are listed in prov/D3EG6T.jsonl.

import random

import oomodel
from oomodel import MAIN
from rapid_type_analysis import rapid_type_analysis


def test_page_example():
    reach, edges = rapid_type_analysis(oomodel.shapes())
    live = {("Circle", "grow"), ("Square", "grow")}
    assert reach == {MAIN} | live
    assert edges == {(s, t) for s in ("s1", "s2", "s3") for t in live}


def test_class_created_after_the_site_is_seen():
    # main calls a.m() on an A; A.m then creates a B, which overrides m.
    prog = {
        "classes": {"A": None, "B": "A"},
        "methods": {"m": ("A", "A", "A")},
        "fields": {},
        "bodies": {
            ("A", "m"): ({"this": "A", "p": "A", "ret": "A"}, [("new", "ret", "B")]),
            ("B", "m"): ({"this": "B", "p": "A", "ret": "A"}, []),
            MAIN: ({"a": "A"}, [("new", "a", "A"), ("call", "s1", "a", "a", "m", None)]),
        },
    }
    reach, edges = rapid_type_analysis(prog)
    assert edges == {("s1", ("A", "m")), ("s1", ("B", "m"))}
    assert reach == {MAIN, ("A", "m"), ("B", "m")}


def test_creation_in_unreachable_code_does_not_count():
    prog = oomodel.shapes()
    prog["bodies"][("Oval", "grow")] = ({"this": "Oval", "p": "Shape", "ret": "Shape"}, [])
    prog["bodies"][("Shape", "grow")][1].append(("new", "ret", "Oval"))
    reach, edges = rapid_type_analysis(prog)
    assert ("Oval", "grow") not in reach
    assert ("Shape", "grow") not in reach


def test_no_objects_no_edges():
    prog = oomodel.shapes()
    local, stmts = prog["bodies"][MAIN]
    prog["bodies"][MAIN] = (local, [st for st in stmts if st[0] == "call"])
    assert rapid_type_analysis(prog) == ({MAIN}, set())


def test_same_as_plain_iteration():
    rng = random.Random(1996)
    for _ in range(500):
        prog = oomodel.random_program(rng, rng.randint(1, 7), rng.randint(1, 4), rng.randint(0, 2), 8)
        assert rapid_type_analysis(prog) == oomodel.rta_spec(prog), oomodel.show(prog)


def test_sound_against_concrete_runs():
    rng = random.Random(78)
    for _ in range(300):
        prog = oomodel.random_program(rng, rng.randint(2, 7), rng.randint(1, 4), rng.randint(0, 2), 8)
        reach, edges = rapid_type_analysis(prog)
        for _ in range(5):
            seen_edges, entered = oomodel.run(prog, rng)
            assert seen_edges <= edges, oomodel.show(prog)
            assert entered <= reach


def test_inside_class_hierarchy_analysis():
    rng = random.Random(6)
    smaller = 0
    for _ in range(300):
        prog = oomodel.random_program(rng, rng.randint(2, 7), rng.randint(1, 4), rng.randint(0, 2), 8)
        reach, edges = rapid_type_analysis(prog)
        cha_reach, cha_edges = oomodel.cha_spec(prog)
        assert reach <= cha_reach and edges <= cha_edges
        smaller += edges != cha_edges
    assert smaller > 0
